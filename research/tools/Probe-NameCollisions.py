"""S132 probe: check Mod-original proper names against the vanilla string table.

Read-only scan: every Mod-original name (items, NPCs, satellites, districts,
interiors, continuation spaces, regions) is compared with the Simplified slots
of vanilla.win for exact and near collisions. Results are metadata only.
"""
from pathlib import Path
import json, hashlib, re, struct
GAME = Path('D:/SteamLibrary/steamapps/common/Stoneshard/vanilla.win')
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research' / 'name-collision-probe.json'
CJK = re.compile(r'[\u4e00-\u9fff]')
KANA = re.compile(r'[\u3040-\u30ff]')
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
b = GAME.read_bytes(); i = b.find(b'STRG')
count = struct.unpack('<I', b[i+8:i+12])[0]
offs = [struct.unpack('<I', b[i+12+4*k:i+16+4*k])[0] for k in range(count)]
def tb(o):
    n = struct.unpack('<I', b[o:o+4])[0]
    return b[o+4:o+4+n]
zh_slots = {}
for k in range(count):
    ps = tb(offs[k]).split(b';')
    if len(ps) < 2: continue
    for p in ps[1:]:
        s = p.decode('utf-8', 'replace').strip()
        if s and CJK.search(s) and not KANA.search(s):
            zh_slots.setdefault(s, []).append(k)
            break
items = read('research/item-registry.json')['items']
fx = read('research/field-npc-dialogue.json')['npcs']
fine = read('research/npc-fine-details.json')['npcs']
model = read('research/city-campaign.json')
cont = read('research/brynn-continuation.json')
CATS = {
 'items': [(x['id'], x['name_cn']) for x in items],
 'field_npcs': [(x['id'], x['name']) for x in fx],
 'fine_detail_npcs': [(x['id'], x['name']) for x in fine],
 'satellites': [(s['id'], s['resident']['name']) for c in model['cities'] for s in c['satellites']],
 'districts': [(n['id'], n['name']) for c in model['cities'] for n in c['nodes'] if n['kind'] == 'district'],
 'interiors': [(n['id'], n['name']) for c in model['cities'] for n in c['nodes'] if n['kind'] == 'interior'],
 'continuation_spaces': [(s['id'], s['name']) for s in cont['spaces']],
}
report = dict(date='2026-10-13', game_file=str(GAME), sha256=hashlib.sha256(b).hexdigest().upper(), bytes=len(b), strg_count=count,
              method='Exact Simplified-slot match plus short-substring match for every Mod-original proper name; read-only, no text stored',
              categories={}, collisions=[], near_matches=[])
for cat, rows in CATS.items():
    exact = []; near = []
    for ident, name in rows:
        if not name: continue
        if name in zh_slots:
            exact.append(dict(id=ident, name=name, strg=zh_slots[name][:3]))
        else:
            hits = [k for k in zh_slots if name in k and len(k) <= len(name) + 4 and k != name]
            if hits: near.append(dict(id=ident, name=name, samples=hits[:3]))
    report['categories'][cat] = dict(names=len(rows), exact=len(exact), near=len(near))
    report['collisions'] += [dict(category=cat, **e) for e in exact]
    report['near_matches'] += [dict(category=cat, **n) for n in near]
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(dict(categories=report['categories'], collisions=len(report['collisions']), near=len(report['near_matches'])), ensure_ascii=False))
