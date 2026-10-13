"""Read-only inventory of vanilla special locations and field-NPC entry points.

Metadata only: keys, STRG indices, zh availability and short site names taken
from the localization table (rumor_*/map_* display names). Dialogue text is
never stored; per-NPC reading is a separate design step.
"""
from pathlib import Path
import hashlib, json, re, struct

GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard')
SRC = GAME / 'vanilla.win'
OUT = Path(__file__).resolve().parents[1] / 'special-location-inventory.json'
CJK = re.compile(r'[\u4e00-\u9fff]')
KANA = re.compile(r'[\u3040-\u30ff]')
HANGUL = re.compile(r'[\uac00-\ud7af]')

def read_strg(path):
    b = path.read_bytes()
    i = b.find(b'STRG')
    if i < 0: raise SystemExit('STRG chunk not found')
    count = struct.unpack('<I', b[i+8:i+12])[0]
    offs = [struct.unpack('<I', b[i+12+4*k:i+16+4*k])[0] for k in range(count)]
    def tb(o):
        n = struct.unpack('<I', b[o:o+4])[0]
        return b[o+4:o+4+n]
    return b, count, [tb(o) for o in offs]

def zh_slot(parts):
    """First part with hanzi and neither kana nor hangul is the Simplified slot."""
    for p in parts[1:]:
        s = p.decode('utf-8', 'replace')
        if len(CJK.findall(s)) >= 2 and not KANA.search(s) and not HANGUL.search(s):
            return s
    return ''

def en_slot(parts):
    """Short English display name: Latin-only part with a space, no CJK."""
    for p in parts[2:3] + parts[1:]:
        s = p.decode('utf-8', 'replace').strip()
        if 2 <= len(s) <= 48 and re.fullmatch(r"[A-Za-z0-9 ,.'\-]+", s) and not CJK.search(s):
            return s
    return ''

def kana_only(parts):
    return not zh_slot(parts) and any(KANA.search(p.decode('utf-8', 'replace')) and CJK.search(p.decode('utf-8', 'replace')) for p in parts[1:])

def main():
    b, count, entries = read_strg(SRC)
    sha = hashlib.sha256(b).hexdigest().upper()
    parsed = []
    for k in range(count):
        parts = entries[k].split(b';')
        parsed.append(dict(index=k, key=parts[0].decode('utf-8', 'replace'), parts=len(parts),
                           zh=zh_slot(parts), en=en_slot(parts), kana_only=kana_only(parts),
                           town=parts[5].decode('utf-8', 'replace') if len(parts) >= 19 else ''))
    def collect(prefix_re):
        rows = {}
        for e in parsed:
            if e['parts'] < 2 or not prefix_re.match(e['key']): continue
            rows.setdefault(e['key'], []).append(e)
        return rows
    regions = []
    defects = []
    for key, hits in sorted(collect(re.compile(r'^map_[a-z0-9_]+$')).items()):
        names = [e for e in hits if e['zh'].endswith('地图') and len(e['zh']) <= 24]
        for e in hits:
            if e['kana_only']: defects.append(dict(index=e['index'], key=key, note='no zh slot; kana-only fallback to verify in game'))
        if not names or not any(x['en'] for x in hits):
            defects.append(dict(index=hits[0]['index'], key=key, note='no english display name found in string table'))
        if not names: continue
        e = sorted(names, key=lambda x: len(x['zh']))[0]
        regions.append(dict(index=e['index'], key=key, name_zh=e['zh'], name_en=e['en'], zh_entries=sum(1 for x in hits if x['zh'])))
    sites = []
    for key, hits in sorted(collect(re.compile(r'^rumor_[A-Za-z0-9_]+$')).items()):
        short = [e for e in hits if 2 <= len(e['zh']) <= 16 and e['parts'] == 14]
        if not short: continue
        e = short[0]
        towns = sorted({x['town'] for x in hits if x['town'] and re.fullmatch(r'[A-Za-z ]{3,}', x['town'])})
        sites.append(dict(index=e['index'], key=key, name_zh=e['zh'], name_en=e['en'], towns=towns,
                          dialogue_entries=sum(1 for x in hits if x['parts'] >= 19)))
    types = []
    missing_types = []
    for key, hits in sorted(collect(re.compile(r'^(?:Cave\d{2}|Camp|Field|Area_Wilderness|Wilderness)$')).items()):
        short = [e for e in hits if 2 <= len(e['zh']) <= 10 and '。' not in e['zh']]
        if not short:
            missing_types.append(key); continue
        e = sorted(short, key=lambda x: x['index'])[0]
        types.append(dict(index=e['index'], key=key, name_zh=e['zh'], name_en=e['en']))
    typed = {t['key'] for t in types}
    identifier_only = sorted({e['key'] for e in parsed
                              if re.fullmatch(r'Cave\d{2}', e['key']) and e['parts'] == 1 and e['key'] not in typed})
    families = {}
    for fam, rx in [('scene', r'^scene[A-Za-z0-9_]*$'), ('greeting', r'^greeting[A-Za-z0-9_]*$'),
                    ('chat', r'^chat[A-Za-z0-9_]*$'), ('npc', r'^npc[A-Za-z0-9_]*$'),
                    ('follower', r'^follower[A-Za-z0-9_]*$')]:
        families[fam] = sum(1 for e in parsed if e['parts'] >= 2 and re.match(rx, e['key']))
    report = dict(
        source=str(SRC), sha256=sha, bytes=len(b), strg_count=count, checked_at='2026-10-13',
        method='Read-only STRG scan of vanilla.win; keys, indices, zh availability and short site names only; no dialogue text stored',
        map_regions=regions, rumor_sites=sites, site_types=types,
        site_types_without_zh=missing_types,
        site_type_identifier_only=identifier_only,
        dialogue_families=families,
        localization_defects=defects,
        limits='Key presence does not prove runtime reachability; per-NPC CN/EN reading, field-encounter mapping and design cards are later steps of the plan.',
    )
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(dict(regions=len(regions), rumor_sites=len(sites), site_types=len(types),
                          defects=len(defects), families=families), ensure_ascii=False))

if __name__ == '__main__':
    main()
