"""Validate the S96 Mod location/person cross-check and its review note."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
x = read('research/mod-location-crosscheck.json')
stems = {p.stem for p in V.rglob('*.md')}
check(len(x['dungeons']) == 9, 'dungeon-count-9')
rewards = [d['reward'] for d in x['dungeons']]
check(len(set(rewards)) == len(rewards), 'dungeon-rewards-unique')
for d in x['dungeons']:
    check(d['region'] in {'R01', 'R02', 'R03', 'R04', 'R05', 'R06'}, d['id'] + '-region')
    check(bool(d['main']), d['id'] + '-main-task')
    check(bool(d['reward']), d['id'] + '-reward')
    check(bool(d['route']), d['id'] + '-route')
    check(bool(d['links']), d['id'] + '-links')
check(len(x['brynn_spaces']) == 6, 'space-count-6')
for s in x['brynn_spaces']:
    check(s['city'] == 'BRY' and s['region'] == 'R01', s['id'] + '-city-region')
    check(f"空间_{s['id']}_{s['name']}" in stems, s['id'] + '-space-note')
check(len(x['field_npcs']) == 36, 'npc-count-36')
ids = [n['id'] for n in x['field_npcs']]
check(len(set(ids)) == 36, 'npc-ids-unique')
sites = [n['site'] for n in x['field_npcs']]
check(len(set(sites)) == 36, 'npc-sites-unique')
for n in x['field_npcs']:
    check(f"人物_{n['id']}_{n['name']}" in stems, n['id'] + '-card')
    check(n['region'] in {'R01', 'R02', 'R03', 'R04', 'R05', 'R06'}, n['id'] + '-region')
c = x['checks']
for k in ['clash_person', 'clash_resident', 'duplicate_sites', 'duplicate_dungeon_names', 'multi_task_reward_owner']:
    check(c[k] in ([], {}), 'check-empty-' + k)
card = (V / '11_管理/Mod特殊地点与人物交叉核对.md').read_text(encoding='utf-8')
check('# Mod特殊地点与人物交叉核对' in card and '## 交叉结论' in card and '## 边界' in card, 'card-structure')
for d in x['dungeons']:
    check(d['name'] in card and f"`{d['id']}`" in card, d['id'] + '-card-row')
for s in x['brynn_spaces']:
    check(f"[[空间_{s['id']}_{s['name']}]]" in card, s['id'] + '-card-row')
for n in x['field_npcs']:
    check(f"[[人物_{n['id']}_{n['name']}]]" in card, n['id'] + '-card-row')
check('多主核对：无' in card and '重名：无' in card, 'card-conclusions')
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('MOD-LOC-XCHECK-S96:BEGIN' in plan and '[[Mod特殊地点与人物交叉核对]]' in plan, 'plan-block-and-link')
check('MOD-LOC-XCHECK-S96:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/mod-loc-xcheck-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S96 Mod location/person cross-check: dungeon regions and unique task settlement, continuation spaces, field NPC uniqueness, card and chain; not coordinates, placement or runtime',
              dungeons=len(x['dungeons']), spaces=len(x['brynn_spaces']), npcs=len(x['field_npcs']),
              checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/mod-loc-xcheck-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
