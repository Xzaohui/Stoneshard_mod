"""Validate the S118 event-stub map by recomputing stubs from flows and keys."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
es = read('research/event-stubs.json')
cf = read('research/corpus-flows.json'); ff = read('research/field-scene-flows.json'); sk = read('research/state-keys.json')
keys = {x['key']: x for x in sk['keys']}
def k(s): return s.replace('-', '_')
# every corpus flow node has exactly one stub
expect_events = set()
for f in cf['flows']:
    for nd in f['nodes']:
        safe = re.sub(r'[^A-Za-z0-9_]', '_', nd['id'])
        expect_events.add(f'evt_{k(f["id"])}_{safe}')
for f in ff['flows']:
    for nd in f['nodes']:
        safe = re.sub(r'[^A-Za-z0-9_]', '_', f'field.{nd["id"]}')
        expect_events.add(f'evt_{k(f["npc"])}_{safe}')
stub_events = [s['event'] for s in es['stubs']]
check(len(stub_events) == len(set(stub_events)), 'events-unique')
check(set(stub_events) == expect_events, 'events-match-nodes')
check(len(es['stubs']) == 1807, 'stub-count-1807')
TRIGGERS = {'on_first_interaction', 'on_interaction', 'on_interaction_if_night', 'on_state_change',
            'on_state_read', 'on_refusal', 'on_presence_check', 'on_route_selected'}
for s in es['stubs']:
    check(re.fullmatch(r'evt_[A-Za-z0-9_]+', s['event']) is not None, s['event'] + '-format')
    check(s['trigger'] in TRIGGERS, s['event'] + '-trigger')
    for key in s['reads'] + s['writes']:
        check(key in keys, s['event'] + '-key-known-' + key)
    check(s['cooldown'] in ('once', 'repeatable'), s['event'] + '-cooldown')
    check(not re.search(r'reward|gold|price|coin', s['event']), s['event'] + '-no-reward')
    if s['when'] == 'any':
        check(not s['writes'], s['event'] + '-hub-writes-nothing')
    if s['when'] == 'first_meet':
        check(f'encountered_{k(s["script"])}' in s['writes'] or s['script'].startswith('FX-'), s['event'] + '-entry-writes-encountered')
    m = re.fullmatch(r'route\(([A-Za-z0-9_]+)\)', s['when'])
    if m:
        check(f'resolve_{k(s["script"])}' in s['reads'], s['event'] + '-route-reads-resolve')
check(es['trigger_counts'] == {'on_first_interaction': 166, 'on_interaction': 166, 'on_route_selected': 247, 'on_state_change': 365,
                               'on_state_read': 552, 'on_refusal': 166, 'on_presence_check': 109, 'on_interaction_if_night': 36}, 'trigger-counts')
card = (V / '09_系统逻辑/事件桩映射总表.md').read_text(encoding='utf-8')
check('# 事件桩映射总表' in card and '## 边界' in card and '**约定**' in card, 'card-structure')
check('不声明真实引擎事件号' in card, 'card-no-engine-ids-claim')
for tname, cnt in es['trigger_counts'].items():
    check(f"| `{tname}` | {cnt} |" in card, 'card-row-' + tname)
stems = {p.stem for p in V.rglob('*.md')}
for lm in re.finditer(r'\[\[([^\]]+)\]\]', card):
    check(lm.group(1) in stems, 'link-resolves-' + lm.group(1))
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('EVENT-STUBS-S118:BEGIN' in plan and '[[事件桩映射总表]]' in plan, 'plan-block-and-link')
check('EVENT-STUBS-S118:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/event-stubs-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S118 event stubs: one stub per flow node, naming, triggers, reads/writes exist in the key map, cooldown and rendering; projection only, no engine ids',
              stubs=len(es['stubs']), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/event-stubs-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
