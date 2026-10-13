"""Validate the S124 interior/daily ambient pool: coverage, parity, links, chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
ia = read('research/interior-ambient.json')
dun = {x['id']: x for x in read('research/story-dungeon.json')}
daily = {x['id']: x for x in read('research/story-daily.json')}
pools = [read('research/ambient-gossip.json'), read('research/town-gossip.json'), read('research/band-gossip.json'),
         read('research/field-npc-dialogue.json'), read('research/field-signs.json')]
prior_cn, prior_en = set(), set()
for p in pools:
    if 'lines' in p:
        for x in p['lines']:
            prior_cn.add(x.get('cn', '')); prior_en.add(x.get('en', ''))
    if 'npcs' in p:
        for n in p['npcs']:
            for _, t in n['greetings'] + n['site_lines'] + [(None, c) for c in n['chats']]:
                prior_cn.add(t)
            for kk in ('before', 'after', 'early', 'late', 'proxy'):
                for v in n['visits'][kk]: prior_cn.add(v)
            for v in (n.get('english') or {}).values(): prior_en.add(v)
    if 'signs' in p:
        for s in p['signs']:
            prior_cn.add(s['obs']); prior_cn.add(s['judge']); prior_cn.add(s['danger'])
            prior_en.add(s.get('obs_en', '')); prior_en.add(s.get('judge_en', '')); prior_en.add(s.get('danger_en', ''))
stems = {p.stem for p in V.rglob('*.md')}
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
check(len(ia['lines']) == 59, 'line-count-59')
check(ia['vocabulary'] == ['on_arrival', 'inside', 'on_exit', 'any', 'after'], 'vocabulary-fixed')
seen_cn, seen_en = {}, {}
per_dun, per_daily = {}, {}
for x in ia['lines']:
    if x['kind'] == 'dungeon':
        per_dun[x['owner']] = per_dun.get(x['owner'], 0) + 1
        check(x['when'] in ('on_arrival', 'inside', 'on_exit'), x['id'] + '-when')
        check(x['owner'] in dun, x['id'] + '-owner')
    else:
        per_daily[x['owner']] = per_daily.get(x['owner'], 0) + 1
        check(x['when'] in ('any', 'after'), x['id'] + '-when')
        check(x['owner'] in daily, x['id'] + '-owner')
    check(bool(CJK.search(x['cn'])) and not re.search(r'[A-Za-z]', x['cn']), x['id'] + '-cn-purity')
    check(not CJK.search(x['en']) and len(x['en']) <= 170, x['id'] + '-en-purity')
    check(not BACK.search(x['cn'] + ' ' + x['en']), x['id'] + '-no-backstage')
    check(x['cn'] not in seen_cn and x['en'] not in seen_en, x['id'] + '-unique')
    check(x['cn'] not in prior_cn and x['en'] not in prior_en, x['id'] + '-no-pool-clone')
    seen_cn[x['cn']] = x['id']; seen_en[x['en']] = x['id']
    check(x['link'] in stems, x['id'] + '-link')
check(per_dun == {d: 3 for d in dun}, 'per-dungeon-3')
check(per_daily == {d: 2 for d in daily}, 'per-daily-2')
card = (V / '02_世界与地图/特殊地点与野外NPC/副本与日常氛围句.md').read_text(encoding='utf-8')
check('# 副本与日常氛围句' in card and '## 边界' in card and '## 副本现场（9×3）' in card and '## 日常周边（16×2）' in card, 'card-structure')
for x in ia['lines']:
    check(f"「{x['cn']}」" in card and x['en'] in card and f"[[{x['link']}]]" in card, x['id'] + '-rendered')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('INTERIOR-AMBIENT-S124:BEGIN' in plan and '[[副本与日常氛围句]]' in plan, 'plan-block-and-link')
check('INTERIOR-AMBIENT-S124:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/interior-ambient-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S124 interior/daily ambient: 9x3 and 16x2 coverage, parity, purity, no pool clones, links and chain; not triggers or runtime',
              lines=len(ia['lines']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/interior-ambient-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
