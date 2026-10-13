"""Read-only structural probe of Stoneshard vanilla.win string table.

Two string shapes are indexed:
- identifiers: single-part entries that are engine/GML names (e.g. Reputation1_Steppe);
- localized: `key;...languages...` entries where part slots vary per entry (a
  full dialogue entry carries metadata slots; find the CJK part and the Latin
  dialogue part per entry instead of assuming fixed indexes).

Outputs namespace histograms, curated system families (reputation, greeting,
follower loyalty scenes, rumors, contracts, quests, situations) and bounded
locator snippets. Full dialogue text is never stored.
"""
from pathlib import Path
import hashlib, json, re, struct

GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
SRC = GAME / 'vanilla.win'
OUT = Path(__file__).resolve().parents[1] / 'original-key-index.json'
IDENT = re.compile(r'^[A-Za-z][A-Za-z0-9_]*$')
CJK = re.compile(r'[\u4e00-\u9fff]')

def read_strg(path):
    b = path.read_bytes()
    i = b.find(b'STRG')
    if i < 0:
        raise SystemExit('STRG chunk not found')
    count = struct.unpack('<I', b[i+8:i+12])[0]
    offs = [struct.unpack('<I', b[i+12+4*k:i+16+4*k])[0] for k in range(count)]
    def text_bytes(o):
        n = struct.unpack('<I', b[o:o+4])[0]
        return b[o+4:o+4+n]
    return b, count, [text_bytes(o) for o in offs]

def zh_part(parts):
    best, best_n = '', 0
    for p in parts[1:]:
        n = len(CJK.findall(p))
        if n > best_n:
            best, best_n = p, n
    return best if best_n >= 3 else ''

def en_part(parts):
    for p in parts[1:]:
        if len(p) >= 12 and re.fullmatch(r"[A-Za-z0-9 ,.'!?%\-:;()\[\]…\"]+", p) and ' ' in p:
            return p
    return ''

FAMILIES = {
    'reputation_keys': re.compile(r'^(?:Reputation|rep)[A-Za-z0-9_]*$'),
    'greeting_keys': re.compile(r'^greeting[A-Za-z0-9_]*$'),
    'loyalty_scene_keys': re.compile(r'^scene\d+(?:Loyalty|.*Loyalty)[A-Za-z0-9_]*$'),
    'scene_keys': re.compile(r'^scene[A-Za-z0-9_]*$'),
    'npc_keys': re.compile(r'^npc[A-Za-z0-9_]*$'),
    'chat_keys': re.compile(r'^chat[A-Za-z0-9_]*$'),
    'rumor_keys': re.compile(r'^rumor[A-Za-z0-9_]*$'),
    'contract_keys': re.compile(r'^contract[A-Za-z0-9_]*$'),
    'quest_keys': re.compile(r'^quest[A-Za-z0-9_]*$'),
    'situation_keys': re.compile(r'^situation[A-Za-z0-9_]*$'),
    'treatise_keys': re.compile(r'^treatise[A-Za-z0-9_]*$'),
    'follower_keys': re.compile(r'^follower[A-Za-z0-9_]*$'),
}
TEXT_TERMS_ZH = ['声誉', '声望', '信赖', '好感', '通缉', '传闻', '契据', '聚落', '契据任务', '声誉历史', '影响因素']
TEXT_TERMS_EN = ['Reputation', 'Loyalty', 'rumou', 'bounty', 'wanted']

def main():
    b, count, raws = read_strg(SRC)
    sha = hashlib.sha256(b).hexdigest().upper()
    text = [r.decode('utf-8', errors='replace') for r in raws]
    identifiers = []          # (idx, key)
    localized = []            # (idx, parts)
    other = 0
    for idx, t in enumerate(text):
        if ';' not in t and IDENT.match(t):
            identifiers.append((idx, t))
            continue
        parts = t.split(';')
        if len(parts) >= 2 and IDENT.match(parts[0] or ''):
            localized.append((idx, parts))
        else:
            other += 1
    # Dialogue-entry inventory for the future per-NPC reference work: keys, locators,
    # detected speaker slot and language availability only; no text is stored.
    DIALOGUE = {
        'scene': re.compile(r'^scene[A-Za-z0-9_]*$'),
        'greeting': re.compile(r'^greeting[A-Za-z0-9_]*$'),
        'chat': re.compile(r'^chat[A-Za-z0-9_]*$'),
        'npc': re.compile(r'^npc[A-Za-z0-9_]*$'),
        'follower': re.compile(r'^follower[A-Za-z0-9_]*$'),
    }
    inventory = {name: [] for name in DIALOGUE}
    speakers = {}
    for idx, parts in localized:
        for name, pat in DIALOGUE.items():
            if pat.match(parts[0]):
                zh = zh_part(parts)
                speaker = parts[2] if len(parts) >= 6 and re.fullmatch(r'[A-Za-z][A-Za-z ]{1,24}', parts[2] or '') else ''
                entry = {'index': idx, 'key': parts[0], 'parts': len(parts), 'zh': bool(zh), 'len': len(zh)}
                if speaker:
                    entry['speaker'] = speaker
                    speakers[speaker] = speakers.get(speaker, 0) + 1
                inventory[name].append(entry)
                break
    inv = {
        'source': str(SRC), 'sha256': sha,
        'note': 'Read-only dialogue-entry inventory: keys, indices, speaker slot and zh availability; no text stored.',
        'families': {k: {'count': len(v), 'entries': v} for k, v in inventory.items()},
        'speaker_histogram': sorted(speakers.items(), key=lambda kv: -kv[1]),
    }
    (Path(__file__).resolve().parents[1] / 'original-dialogue-inventory.json').write_text(
        json.dumps(inv, ensure_ascii=False, indent=1), encoding='utf-8')
    def prefix_hist(items, keyf, n=100):
        h = {}
        for it in items:
            k = keyf(it)
            p = k.split('_', 1)[0]
            h[p] = h.get(p, 0) + 1
        return sorted(h.items(), key=lambda kv: -kv[1])[:n]
    family_report = {}
    for name, pat in FAMILIES.items():
        hits = [(idx, k) for idx, k in identifiers if pat.match(k)]
        hits += [(idx, parts[0]) for idx, parts in localized if pat.match(parts[0])]
        sample = [{'index': i, 'key': k} for i, k in hits[:40]]
        detail = ''
        if name == 'loyalty_scene_keys':
            marks = {'25': 0, '50': 0, '75': 0, '100': 0}
            names = set()
            for _, k in hits:
                m = re.match(r'^scene(\d+)Loyalty([A-Z][A-Za-z]*?)(\d+[a-z]?|_?pc)?$', k)
                if m:
                    marks[m.group(1)] = marks.get(m.group(1), 0) + 1
                    names.add(m.group(2))
            detail = {'thresholds': marks, 'names': sorted(names)}
        family_report[name] = {'count': len(hits), 'samples': sample, 'detail': detail}
    zh_hits = {}
    en_hits = {}
    for idx, parts in localized:
        zh = zh_part(parts); en = en_part(parts)
        for term in TEXT_TERMS_ZH:
            if zh and term in zh:
                lst = zh_hits.setdefault(term, [])
                if len(lst) < 40:
                    m = re.search(r'.{0,12}' + re.escape(term) + r'.{0,32}', zh)
                    lst.append({'index': idx, 'key': parts[0], 'snippet': m.group(0)})
                elif len(lst) < 500:
                    lst.append(None)
        for term in TEXT_TERMS_EN:
            if en and term.lower() in en.lower():
                lst = en_hits.setdefault(term, [])
                if len(lst) < 40:
                    m = re.search(r'.{0,12}' + re.escape(term) + r'.{0,40}', en, re.I)
                    lst.append({'index': idx, 'key': parts[0], 'snippet': m.group(0)})
                elif len(lst) < 500:
                    lst.append(None)
    def summarize(h):
        return {k: {'count': len(v), 'examples': [x for x in v if x][:24]} for k, v in h.items()}
    report = {
        'source': str(SRC),
        'sha256': sha,
        'bytes': len(b),
        'strg_count': count,
        'identifier_entries': len(identifiers),
        'localized_entries': len(localized),
        'unshaped_entries': other,
        'identifier_prefix_histogram_top': prefix_hist(identifiers, lambda it: it[1]),
        'localized_prefix_histogram_top': prefix_hist(localized, lambda it: it[1][0]),
        'families': family_report,
        'dialogue_inventory': {k: len(v) for k, v in inventory.items()},
        'dialogue_speakers': len(speakers),
        'zh_text_hits': summarize(zh_hits),
        'en_text_hits': summarize(en_hits),
        'notes': [
            'Localized entries: key + per-entry slot list; languages appear in order ru,en,zh,de,es,fr,it,pt,pl,tr,ja,ko with metadata slots inserted in dialogue entries.',
            'zh part is detected by CJK density; snippets <=46 chars around matches; full table text is not stored.',
            'Read-only probe; game files untouched.',
        ],
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({
        'sha256': sha, 'strg_count': count, 'identifiers': len(identifiers), 'localized': len(localized),
        'families': {k: v['count'] for k, v in family_report.items()},
        'dialogue_inventory': {k: len(v) for k, v in inventory.items()},
        'dialogue_speakers': len(speakers),
        'zh': {k: v['count'] for k, v in report['zh_text_hits'].items()},
        'en': {k: v['count'] for k, v in report['en_text_hits'].items()},
        'written': str(OUT),
    }, ensure_ascii=False, indent=1))

if __name__ == '__main__':
    main()
