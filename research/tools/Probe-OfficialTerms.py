"""Read-only probe: verify official terms and their English slots in STRG.

For every terminology entry in research/item-registry.json, searches vanilla.win
for the STRG entry whose Chinese slot equals the recorded official term, takes
the smallest index that also carries an English slot, and records the verified
locator, the English term and a game fingerprint into
research/official-term-probe.json. The old contains-term indices are kept as
historical locators. The game file is opened read-only.
"""
from pathlib import Path
import json, hashlib, re, struct
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard/vanilla.win')
ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'research/item-registry.json'
OUT = ROOT / 'research/official-term-probe.json'
CJK = re.compile(r'[\u4e00-\u9fff]')
KANA = re.compile(r'[\u3040-\u30ff]')
LATIN_TERM = re.compile(r"[A-Za-z][A-Za-z0-9 '\-]{1,40}$")
def read_strg(path):
    b = path.read_bytes()
    i = b.find(b'STRG')
    count = struct.unpack('<I', b[i+8:i+12])[0]
    offs = [struct.unpack('<I', b[i+12+4*k:i+16+4*k])[0] for k in range(count)]
    def parts(o):
        n = struct.unpack('<I', b[o:o+4])[0]
        return b[o+4:o+4+n].split(b';')
    return b, [parts(o) for o in offs]
def slots(parts):
    zh, en = '', ''
    for p in parts[1:]:
        s = p.decode('utf-8', 'replace').strip()
        if not s: continue
        if not zh and CJK.search(s) and not KANA.search(s): zh = s
        if not en and not CJK.search(s) and LATIN_TERM.fullmatch(s): en = s
    return zh, en
b, entries = read_strg(GAME)
sha = hashlib.sha256(b).hexdigest().upper()
data = json.loads(SRC.read_text(encoding='utf-8'))
prev = {}
if OUT.exists():
    try:
        for r in json.loads(OUT.read_text(encoding='utf-8'))['entries']:
            prev[r['concept']] = r
    except Exception:
        prev = {}
records = []
for x in data['terminology_alignment']:
    term = x['official_cn']
    if not term.strip():
        records.append(dict(concept=x['concept'], official_cn='', contains_index=prev.get(x['concept'], {}).get('contains_index'),
                            verified_index=None, official_en=None, candidates=0, with_en=0, note='no recorded official term; index untouched'))
        old_idx = prev.get(x['concept'], {}).get('contains_index')
        if isinstance(old_idx, int):
            x['official_index'] = old_idx
        else:
            x['official_index'] = None
            x.pop('official_en', None)
        continue
    candidates = []
    for idx, parts in enumerate(entries):
        zh, en = slots(parts)
        if zh != term: continue
        candidates.append((idx, en))
    with_en = [c for c in candidates if c[1]]
    pick = min(with_en or candidates, key=lambda c: c[0]) if candidates else None
    rec = dict(concept=x['concept'], official_cn=term,
               contains_index=x.get('official_index'),
               verified_index=pick[0] if pick else None,
               official_en=pick[1] if pick else None,
               candidates=len(candidates), with_en=len(with_en))
    if pick:
        hist = prev.get(x['concept'], {}).get('contains_index', x.get('official_index'))
        if isinstance(hist, int) and hist != pick[0]:
            x['official_index_contains'] = hist
        x['official_index'] = pick[0]
        if pick[1]: x['official_en'] = pick[1]
        else: x.pop('official_en', None)
    else:
        x.pop('official_en', None)
        rec['note'] = 'exact Chinese term not found in STRG; index kept as contains-term locator'
    records.append(rec)
probe = dict(date='2026-10-13', game_file=str(GAME), sha256=sha, bytes=len(b),
             method='Exact Chinese-slot match for each recorded official term; smallest index with an English slot; read-only',
             entries=records)
OUT.write_text(json.dumps(probe, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
data['official_en_source'] = dict(game_file=str(GAME), sha256=sha,
                                  note='official_index verified by exact Chinese-slot match; official_en read from the same STRG entry',
                                  probe='research/official-term-probe.json')
SRC.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
found = [r for r in records if r['verified_index'] is not None]
print(json.dumps(dict(terms=len(records), found=len(found), missing=[r['concept'] for r in records if r['verified_index'] is None],
                      en_missing=[r['concept'] for r in records if r['verified_index'] is not None and not r['official_en']]), ensure_ascii=False))
