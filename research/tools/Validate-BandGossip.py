"""Validate the S117 reputation-band street reactions: coverage, parity, chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
bg = read('research/band-gossip.json')
model = read('research/city-campaign.json'); rep = read('research/town-reputation.json')
tg = read('research/town-gossip.json'); ag = read('research/ambient-gossip.json')
stems = {p.stem for p in V.rglob('*.md')}
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
cities = {c['id']: c for c in model['cities']}
regions = {'R01', 'R02', 'R03', 'R04', 'R05', 'R06'}
check(len(bg['lines']) == 42, 'line-count-42')
check(bg['vocabulary'] == ['band:-1', 'band:+2'], 'vocabulary-fixed')
counter = {b['line_cn'] for t in rep['towns'] for b in t['bands']} | {b['line_en'] for t in rep['towns'] for b in t['bands']}
prior = {x['cn'] for x in tg['lines']} | {x['en'] for x in tg['lines']} | {x['cn'] for x in ag['lines']} | {x['en'] for x in ag['lines']}
per = {}
seen_cn, seen_en = {}, {}
for x in bg['lines']:
    per[x['place']] = per.get(x['place'], 0) + 1
    check(x['place'] in cities or x['place'] in regions, x['id'] + '-place')
    check(x['when'] in ('band:-1', 'band:+2'), x['id'] + '-when')
    check(bool(CJK.search(x['cn'])) and not re.search(r'[A-Za-z]', x['cn']), x['id'] + '-cn-purity')
    check(not CJK.search(x['en']) and len(x['en']) <= 150, x['id'] + '-en-purity')
    check(not BACK.search(x['cn'] + ' ' + x['en']), x['id'] + '-no-backstage')
    check(x['cn'] not in seen_cn and x['en'] not in seen_en, x['id'] + '-unique')
    check(x['cn'] not in counter and x['en'] not in counter, x['id'] + '-no-counter-clone')
    check(x['cn'] not in prior and x['en'] not in prior, x['id'] + '-no-pool-clone')
    seen_cn[x['cn']] = x['id']; seen_en[x['en']] = x['id']
    check(x['link'] in stems, x['id'] + '-link')
    if x['place'] in cities:
        check(x['link'] == Path(cities[x['place']]['file']).stem, x['id'] + '-city-link')
    check(bool(x['speaker'].strip()), x['id'] + '-speaker')
expect = {**{cid: 2 for cid in cities}, **{r: 2 for r in regions}}
check(per == expect, 'per-place-2')
card = (V / '02_世界与地图/特殊地点与野外NPC/声望档街头反应.md').read_text(encoding='utf-8')
check('# 声望档街头反应' in card and '## 边界' in card, 'card-structure')
for x in bg['lines']:
    check(f"「{x['cn']}」" in card and x['en'] in card and f"[[{x['link']}]]" in card, x['id'] + '-rendered')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('BAND-GOSSIP-S117:BEGIN' in plan and '[[声望档街头反应]]' in plan, 'plan-block-and-link')
check('BAND-GOSSIP-S117:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/band-gossip-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S117 band reactions: per-place cold/warm coverage, CN/EN parity, no counter-line or pool clones, links and chain; tone only, not triggers or runtime',
              lines=len(bg['lines']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/band-gossip-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
