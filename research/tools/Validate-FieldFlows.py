"""Validate the S105 field-NPC condition flows: refs, nodes, vocabulary and chain."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
fl = read('research/field-scene-flows.json')
fx = read('research/field-npc-dialogue.json')
by_id = {n['id']: n for n in fx['npcs']}
stems = {p.stem for p in V.rglob('*.md')}
VOCAB = {'first_meet', 'night', 'any', 'task_open', 'task_done', 'order_early', 'order_late', 'refused', 'npc_absent'}
check(fl['vocabulary'] == ['first_meet', 'night', 'any', 'task_open', 'task_done', 'order_early', 'order_late', 'refused', 'npc_absent'], 'vocabulary-fixed')
check(len(fl['flows']) == 36, 'flow-count-36')
check({f['npc'] for f in fl['flows']} == set(by_id), 'flows-match-registry')
REQUIRED = {'first_meet', 'night', 'task_open', 'task_done', 'order_early', 'order_late', 'refused', 'npc_absent'}
for f in fl['flows']:
    n = by_id[f['npc']]
    check(f['task'] == n['visits']['task'], f['npc'] + '-task-matches')
    check(f['site'] == n['site'] and f['region'] == n['region'], f['npc'] + '-site-region')
    whens = {nd['when'] for nd in f['nodes']}
    check(REQUIRED <= whens, f['npc'] + '-required-states')
    check(whens <= VOCAB, f['npc'] + '-vocab-only')
    ids = {nd['id'] for nd in f['nodes']}
    check(len(ids) == len(f['nodes']), f['npc'] + '-node-ids-unique')
    for nd in f['nodes']:
        check(nd['next'] in ids | {'end'}, f['npc'] + '-next-resolves-' + nd['id'])
        for r in nd['lines']:
            check(r in f['refs'], f['npc'] + '-ref-known-' + r)
    for key, txt in f['refs'].items():
        found = any(txt == t for _, t in n['greetings'] + n['site_lines'] + [(None, c) for c in n['chats']]
                    + [(None, v) for k in ('before', 'after', 'early', 'late', 'proxy') for v in n['visits'][k]])
        check(found, f['npc'] + '-ref-text-' + key)
    check(f['chats'] and all(r in f['refs'] for r in f['chats']), f['npc'] + '-chats-refs')
    check(all(r in f['refs'] for r in f['arrival'] + f['warning']), f['npc'] + '-site-refs')
    check(len(f['guards']) >= 4, f['npc'] + '-guards')
    proxy = next(nd for nd in f['nodes'] if nd['when'] == 'npc_absent')
    check(proxy.get('speaker') == 'proxy', f['npc'] + '-proxy-speaker')
card = (V / '02_世界与地图/特殊地点与野外NPC/野外对白条件流.md').read_text(encoding='utf-8')
check('# 野外对白条件流' in card and '## 口径' in card, 'card-structure')
check('**条件词表**' in card and card.count('`task_open`') >= 1, 'card-vocabulary')
for f in fl['flows']:
    check(f"[[人物_{f['npc']}_{f['name']}]]" in card and f"`{f['npc']}`" in card, f['npc'] + '-card-row')
    for nd in f['nodes']:
        check(f"| `{nd['id']}` | `{nd['when']}` |" in card, f['npc'] + '-node-rendered-' + nd['id'])
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('FIELD-FLOWS-S105:BEGIN' in plan and '[[野外对白条件流]]' in plan, 'plan-block-and-link')
check('FIELD-FLOWS-S105:BEGIN' in (ROOT / 'CHANGELOG.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/field-flows-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S105 field condition flows: vocabulary, node graph, line references, refusal/absence exits, rendering and chain; not engine triggers or runtime',
              flows=len(fl['flows']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/field-flows-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
