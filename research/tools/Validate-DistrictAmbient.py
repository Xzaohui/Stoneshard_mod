"""Validate the S129 district ambient pool: coverage, parity, links, chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
da = read('research/district-ambient.json')
model = read('research/city-campaign.json')
districts = {n['id']: (c['id'], n['name'], Path(c['file']).stem) for c in model['cities'] for n in c['nodes'] if n['kind'] == 'district'}
stems = {p.stem for p in V.rglob('*.md')}
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
check(len(da['lines']) == 66, 'line-count-66')
check({x['id'] for x in da['lines']} == set(districts), 'ids-match-districts')
prior_cn, prior_en = set(), set()
for f in ['ambient-gossip', 'town-gossip', 'band-gossip', 'interior-ambient']:
    d = read(f'research/{f}.json')
    for x in d['lines']:
        prior_cn.add(x['cn']); prior_en.add(x['en'])
fx = read('research/field-npc-dialogue.json')
for n in fx['npcs']:
    for _, t in n['greetings'] + n['site_lines'] + [(None, c) for c in n['chats']]:
        prior_cn.add(t)
    for kk in ('before', 'after', 'early', 'late', 'proxy'):
        for v in n['visits'][kk]: prior_cn.add(v)
    for v in (n.get('english') or {}).values(): prior_en.add(v)
seen_cn, seen_en = {}, {}
for x in da['lines']:
    cid, dname, link = districts[x['id']]
    check(x['city'] == cid and x['district'] == dname, x['id'] + '-meta')
    check(x['link'] == link and link in stems, x['id'] + '-link')
    check(bool(x['voice'].strip()), x['id'] + '-voice')
    check(bool(CJK.search(x['cn'])) and not re.search(r'[A-Za-z]', x['cn']), x['id'] + '-cn-purity')
    check(not CJK.search(x['en']) and len(x['en']) <= 150, x['id'] + '-en-purity')
    check(not BACK.search(x['cn'] + ' ' + x['en']), x['id'] + '-no-backstage')
    check(x['cn'] not in seen_cn and x['en'] not in seen_en, x['id'] + '-unique')
    check(x['cn'] not in prior_cn and x['en'] not in prior_en, x['id'] + '-no-pool-clone')
    seen_cn[x['cn']] = x['id']; seen_en[x['en']] = x['id']
card = (V / '02_世界与地图/特殊地点与野外NPC/街区氛围句.md').read_text(encoding='utf-8')
check('# 街区氛围句' in card and '## 边界' in card, 'card-structure')
for x in da['lines']:
    check(f"「{x['cn']}」" in card and x['en'] in card and f"[[{x['link']}]]" in card, x['id'] + '-rendered')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('DISTRICT-AMBIENT-S129:BEGIN' in plan and '[[街区氛围句]]' in plan, 'plan-block-and-link')
check('DISTRICT-AMBIENT-S129:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/district-ambient-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S129 district ambient: 66 districts covered, parity, purity, no pool clones, links and chain; not triggers or runtime',
              lines=len(da['lines']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/district-ambient-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
