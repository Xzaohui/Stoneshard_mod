"""Validate the S116 town ambient gossip: coverage, parity, links and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
tg = read('research/town-gossip.json')
model = read('research/city-campaign.json')
ag = read('research/ambient-gossip.json'); fx = read('research/field-npc-dialogue.json')
stems = {p.stem for p in V.rglob('*.md')}
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
cities = {c['id']: c for c in model['cities']}
CM = {c['id']: Path(next(q for q in model['quests'] if q['id'] == c['main_id'])['file']).stem for c in model['cities']}
check(len(tg['lines']) == 60, 'line-count-60')
check(tg['vocabulary'] == ['any', 'night', 'after:<CM chapter>'], 'vocabulary-fixed')
per = {}
prior_cn = {x['cn'] for x in ag['lines']}
prior_en = {x['en'] for x in ag['lines']}
field_cn = {t for n in fx['npcs'] for _, t in n['greetings'] + n['site_lines'] + [(None, c) for c in n['chats']]
            + [(None, v) for kk in ('before', 'after', 'early', 'late', 'proxy') for v in n['visits'][kk]]}
seen_cn, seen_en = {}, {}
for x in tg['lines']:
    per[x['city']] = per.get(x['city'], 0) + 1
    check(x['city'] in cities, x['id'] + '-city')
    check(x['when'] in ('any', 'night') or x['when'] in stems, x['id'] + '-when')
    if x['when'] not in ('any', 'night'):
        check(x['when'] == CM[x['city']], x['id'] + '-when-is-own-chapter')
    check(bool(CJK.search(x['cn'])) and not re.search(r'[A-Za-z]', x['cn']), x['id'] + '-cn-purity')
    check(not CJK.search(x['en']) and len(x['en']) <= 150, x['id'] + '-en-purity')
    check(not BACK.search(x['cn'] + ' ' + x['en']), x['id'] + '-no-backstage')
    check(x['cn'] not in seen_cn and x['en'] not in seen_en, x['id'] + '-unique')
    check(x['cn'] not in prior_cn and x['en'] not in prior_en, x['id'] + '-no-region-clone')
    check(x['cn'] not in field_cn, x['id'] + '-no-field-clone')
    seen_cn[x['cn']] = x['id']; seen_en[x['en']] = x['id']
    check(x['link'] in stems, x['id'] + '-link')
    check(x['chapter'] == CM[x['city']] and x['chapter'] in stems, x['id'] + '-chapter')
check(per == {cid: 4 for cid in cities}, 'per-city-4')
check(len(per) == 15, 'cities-15')
card = (V / '02_世界与地图/特殊地点与野外NPC/城镇闲谈池.md').read_text(encoding='utf-8')
check('# 城镇闲谈池' in card and '## 边界' in card, 'card-structure')
for cid, c in cities.items():
    check(f"## {c['name']}（4）" in card, cid + '-section')
for x in tg['lines']:
    check(f"「{x['cn']}」" in card and x['en'] in card, x['id'] + '-rendered')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('TOWN-GOSSIP-S116:BEGIN' in plan and '[[城镇闲谈池]]' in plan, 'plan-block-and-link')
check('TOWN-GOSSIP-S116:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/town-gossip-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S116 town gossip: 15 towns x4 lines, condition vocabulary, CN/EN parity and purity, uniqueness against region and field pools, links and chain; not triggers or runtime',
              lines=len(tg['lines']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/town-gossip-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
