"""S200/S201 structure optimization phase recorder.
Registers notes carrying OPT-S200 / OPT-S201 blocks (or created by this phase) in
research/structure-opt-note-hashes.json and back-writes their current hashes into
every other *note-hashes.json that already tracks them (same pattern as Attach-FineDetails.py).
Does not render or rewrite note text."""
from pathlib import Path
import hashlib, json, re
ROOT = Path(__file__).resolve().parents[2]
V = ROOT / 'design'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
NEW = ['design/09_系统逻辑/后果分级与重边.md', 'design/09_系统逻辑/终局互斥条款.md',
       'design/03_势力/势力利益冲突矩阵.md', 'design/04_人物/人物_坎沃·岩.md',
       'design/09_系统逻辑/城市主线回流S201.md']
rel = set(n for n in NEW if (ROOT / n).exists())
for p in V.rglob('*.md'):
    t = p.read_bytes().decode('utf-8-sig')
    if re.search(r'<!--\s*OPT-S20[0-9]:BEGIN\s*-->', t) or re.search(r'<!--\s*OPT-S20[0-9]-RULE:BEGIN\s*-->', t):
        rel.add(p.relative_to(ROOT).as_posix())
own = ROOT / 'research/structure-opt-note-hashes.json'
manifest = {r: sha(ROOT / r) for r in sorted(rel)}
updated = 0
for hp in sorted((ROOT / 'research').glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict): continue
    ch = False
    for r in list(h):
        if r in manifest and h[r] != manifest[r]: h[r] = manifest[r]; ch = True; updated += 1
    if ch: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for ip in [ROOT / 'research/brynn-continuation-integration.json']:
    raw = ip.read_bytes(); nl = '\r\n' if b'\r\n' in raw else '\n'
    j = json.loads(raw.decode('utf-8')); ch = False
    for sec in ('generated', 'updated_existing'):
        for r in list(j.get(sec, {})):
            if r in manifest and j[sec][r] != manifest[r]: j[sec][r] = manifest[r]; ch = True; updated += 1
    if ch: ip.write_bytes((json.dumps(j, ensure_ascii=False, indent=2) + '\n').replace('\n', nl).encode('utf-8'))
own.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'registered': len(manifest), 'backwritten': updated}, ensure_ascii=False))
