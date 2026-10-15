"""Validate the S114 state-key map by recomputing keys from the sources."""
from pathlib import Path
import json, hashlib, re
from HeavyEdges import resolve_keys
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
checks = []; errors = []
def check(ok, label): (checks if ok else errors).append(label)
sk = read('research/state-keys.json')
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json'); fx = read('research/field-npc-dialogue.json')
cf = read('research/corpus-flows.json')
def k(s): return s.replace('-', '_')
keys = {x['key']: x for x in sk['keys']}
check(len(sk['keys']) == len(keys), 'keys-unique')
expect = {}
def add(key, kind, script, values):
    expect[key] = (kind, script, values)
for q in model['quests']:
    sid = q['id']; routes = [r['key'] for r in q.get('routes') or []]
    add(f'encountered_{k(sid)}', 'encounter', sid, ['false', 'true'])
    add(f'resolve_{k(sid)}', 'resolve', sid, ['none'] + routes)
    for r in q.get('routes') or []:
        add(f'callback_{k(sid)}_{k(r["key"])}', 'callback', sid, ['false', 'true'])
        add(f'consent_{k(sid)}_{k(r["key"])}', 'consent', sid, ['false', 'true'])
        if r.get('cost'): add(f'paid_{k(sid)}_{k(r["key"])}', 'paid', sid, ['false', 'true'])
    ex = q.get('dramatic_exceptions') or {}
    if ex.get('dead') or ex.get('refusal'): add(f'presence_{k(sid)}', 'presence', sid, ['present', 'absent', 'dead', 'refused'])
    if ex.get('before_city') or ex.get('after_city'): add(f'order_{k(sid)}', 'order', sid, ['early', 'late', 'unknown'])
for q in cont['quests']:
    sid = q['id']; routes = [r['key'] for r in q.get('routes') or []]
    add(f'encountered_{k(sid)}', 'encounter', sid, ['false', 'true'])
    add(f'resolve_{k(sid)}', 'resolve', sid, ['none'] + routes)
    for r in q.get('routes') or []:
        add(f'callback_{k(sid)}_{k(r["key"])}', 'callback', sid, ['false', 'true'])
        add(f'consent_{k(sid)}_{k(r["key"])}', 'consent', sid, ['false', 'true'])
        if r.get('cost'): add(f'paid_{k(sid)}_{k(r["key"])}', 'paid', sid, ['false', 'true'])
    if q.get('interruption'): add(f'presence_{k(sid)}', 'presence', sid, ['present', 'absent', 'dead', 'refused'])
for name in ['story-main.json', 'story-side.json', 'story-main-late.json', 'story-dungeon.json']:
    for x in read('research/' + name):
        sid = x['id']; choices = [c[0] for c in x.get('choices') or []]
        add(f'encountered_{k(sid)}', 'encounter', sid, ['false', 'true'])
        add(f'resolve_{k(sid)}', 'resolve', sid, ['none'] + choices)
        for c in choices: add(f'callback_{k(sid)}_{k(c)}', 'callback', sid, ['false', 'true'])
        if x.get('recovery'): add(f'presence_{k(sid)}', 'presence', sid, ['present', 'absent', 'dead', 'refused'])
for x in read('research/story-daily.json'):
    sid = x['id']
    add(f'encountered_{k(sid)}', 'encounter', sid, ['false', 'true'])
    add(f'resolve_{k(sid)}', 'resolve', sid, ['none', 'done', 'failed'])
for n in fx['npcs']:
    add(f'presence_{k(n["id"])}', 'presence', n['id'], ['present', 'absent', 'dead', 'refused'])
for e in model['effects']: add(f'receipt_{k(e["id"])}', 'receipt', e['id'], ['false', 'true'])
for e in cont['effects']: add(f'receipt_{k(e["id"])}', 'receipt', e['id'], ['false', 'true'])
# Current S62 operational routes supersede the historical choices vocabulary.
network=read('research/story-network.json')
for sid, task in network['tasks'].items():
    name='resolve_'+k(sid)
    if name in expect and name in resolve_keys(network):
        kind, script, _ = expect[name]
        expect[name]=(kind,script,['none']+[r['key'] for r in task['routes']])
check(set(keys) == set(expect), 'keys-match-sources')
for key, (kind, script, values) in expect.items():
    item = keys.get(key)
    check(item is not None and item['kind'] == kind, key + '-kind')
    check(item is not None and item['script'] == script, key + '-script')
    check(item is not None and item['values'] == values, key + '-values')
    check(re.fullmatch(r'[a-z]+_[A-Za-z0-9_]+', key) is not None, key + '-format')
    check(not re.search(r'reward|gold|price|coin', key), key + '-no-reward-word')
check(len([x for x in keys.values() if x['kind'] == 'receipt']) == len(model['effects']) + len(cont['effects']), 'receipt-count-matches-effects')
check(sk['families'] == {'encounter': 130, 'resolve': 130, 'callback': 247, 'consent': 167, 'paid': 167, 'presence': 150, 'order': 73, 'receipt': 329}, 'family-counts')
# every corpus flow has a resolve key and encounter key
for f in cf['flows']:
    check(f'encountered_{k(f["id"])}' in keys, f['id'] + '-encounter-key')
    check(f'resolve_{k(f["id"])}' in keys, f['id'] + '-resolve-key')
# conditions in flows map to key families
conds = {nd['when'] for f in cf['flows'] for nd in f['nodes']}
check({'first_meet', 'any', 'task_done'} <= conds, 'flow-conditions-present')
card = (V / '09_系统逻辑/状态键映射总表.md').read_text(encoding='utf-8')
check('# 状态键映射总表' in card and '## 与条件流的对应' in card and '## 边界' in card, 'card-structure')
check('**约定**' in card and 'CS-BRY-01 → CS_BRY_01' in card, 'card-conventions')
for fam, cnt in sk['families'].items():
    check(f"| {fam} | {cnt} |" in card, 'card-row-' + fam)
receipts = [x for x in sk['keys'] if x['kind'] == 'receipt']
for x in receipts[:20]:
    check(f"`{x['key']}`" in card, 'card-receipt-' + x['key'])
plan = (V / '11_管理/特殊地点与野外NPC对白扩展计划.md').read_text(encoding='utf-8')
check('STATE-KEYS-S114:BEGIN' in plan and '[[状态键映射总表]]' in plan, 'plan-block-and-link')
check('STATE-KEYS-S114:BEGIN' in (ROOT / 'AGENTS.md').read_text(encoding='utf-8-sig'), 'agents-block')
h = read('research/state-keys-note-hashes.json')
check(len(h) == 2, 'own-manifest-2')
for rel, exp in h.items(): check(sha(ROOT / rel) == exp, rel + '-hash')
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    m = json.loads(p.read_text(encoding='utf-8'))
    if not isinstance(m, dict) or not all(isinstance(v, str) for v in m.values()): continue
    for rel, exp in m.items(): check((ROOT / rel).exists() and sha(ROOT / rel) == exp, rel + '-manifest-reconciled')
report = dict(date='2026-10-13', scope='S114 state keys: recomputed key set, formats, values, receipt count, flow linkage, rendering and chain; not engine read/write or save migration',
              keys=len(keys), receipts=len(receipts), checks_passed=len(checks), errors=errors, passed=not errors, runtimeVerified=False)
(ROOT / 'research/state-keys-validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False))
raise SystemExit(0 if report['passed'] else 1)
