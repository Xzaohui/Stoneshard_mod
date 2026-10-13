"""S118: map every flow node to an implementation event stub.

Deterministic projection of the corpus flows and field flows onto event stubs:
naming, trigger, state reads/writes, cooldown. Reads/writes must exist in the
state-key map; no reward semantics.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'EVENT-STUBS-S118'
CARD = '09_系统逻辑/事件桩映射总表.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
cf = read('research/corpus-flows.json'); ff = read('research/field-scene-flows.json'); sk = read('research/state-keys.json')
keys = {x['key']: x for x in sk['keys']}
by_script = {}
for x in sk['keys']: by_script.setdefault(x['script'], []).append(x['key'])
def k(s): return s.replace('-', '_')
TRIGGERS = {
 'first_meet': 'on_first_interaction', 'any': 'on_interaction', 'night': 'on_interaction_if_night',
 'task_done': 'on_state_change', 'task_open': 'on_state_read', 'order_early': 'on_state_read', 'order_late': 'on_state_read',
 'refused': 'on_refusal', 'npc_absent': 'on_presence_check',
}
stubs = []
def stub(script_id, node, when, reads, writes, cooldown, notes):
    m = re.fullmatch(r'route\(([A-Za-z0-9_]+)\)', when)
    trigger = TRIGGERS.get(when) or (f'on_route_selected' if m else 'on_interaction')
    safe = re.sub(r'[^A-Za-z0-9_]', '_', node)
    stubs.append(dict(event=f'evt_{k(script_id)}_{safe}', script=script_id, node=node, when=when, trigger=trigger,
                      reads=sorted(reads), writes=sorted(writes), cooldown=cooldown, notes=list(notes)))
for f in cf['flows']:
    sid = f['id']
    sks = by_script.get(sid, [])
    res = f'resolve_{k(sid)}'
    enc = f'encountered_{k(sid)}'
    pres = f'presence_{k(sid)}'
    for nd in f['nodes']:
        when = nd['when']; reads, writes = [], []
        notes = [n[0] for n in nd['notes']]
        if when == 'first_meet':
            reads = [enc]; writes = [enc]
        elif when == 'any':
            reads = [enc]
        elif when == 'task_done':
            reads = [res]; writes = [c for c in sks if c.startswith('callback_') and nd['id'].startswith('feedback')]
        elif when in ('order_early', 'order_late'):
            reads = [c for c in sks if c.startswith('order_')]
        elif when == 'refused':
            reads = [pres] if pres in keys else []
        elif when == 'npc_absent':
            reads = [pres] if pres in keys else []
        m = re.fullmatch(r'route\(([A-Za-z0-9_]+)\)', when)
        if m:
            reads = [res]
            writes = [c for c in sks if c.startswith('callback_') or c.startswith('consent_') or c.startswith('paid_')]
        if nd['id'].startswith('effect.'):
            writes = [c for c in sks if c.startswith('receipt_') and c.split('_', 1)[1] in k(nd['id']).upper()]
        cooldown = 'once' if (when == 'first_meet' or m or nd['id'].startswith('feedback') or nd['id'].startswith('effect.')) else 'repeatable'
        stub(sid, nd['id'], when, reads, writes, cooldown, notes)
# field flows: script id from the related task stem
corpus_ids = {f['id'] for f in cf['flows']}
for f in ff['flows']:
    stem = f['task']
    sid = stem[len('台本_'):].split('_')[0]
    assert sid in corpus_ids, (f['npc'], stem)
    sks = by_script.get(sid, [])
    res = f'resolve_{k(sid)}'
    pres = f'presence_{k(f["npc"])}'
    for nd in f['nodes']:
        when = nd['when']; reads, writes = [], []
        if when == 'first_meet':
            reads = [pres]
        elif when == 'task_open':
            reads = [res]
        elif when == 'task_done':
            reads = [res]
        elif when in ('order_early', 'order_late'):
            reads = [c for c in sks if c.startswith('order_')]
        elif when == 'npc_absent':
            reads = [pres]
        elif when == 'refused':
            reads = [pres]
        cooldown = 'once' if when in ('first_meet', 'task_done', 'order_early', 'order_late') else 'repeatable'
        stub(f['npc'], f'field.{nd["id"]}', when, reads, writes, cooldown, [])
seen = set()
for s in stubs:
    assert s['event'] not in seen, s['event']
    seen.add(s['event'])
    assert re.fullmatch(r'evt_[A-Za-z0-9_]+', s['event']), s['event']
    for key in s['reads'] + s['writes']:
        assert key in keys, s['event'] + ' unknown key ' + key
    assert not re.search(r'reward|gold|price|coin', s['event']), s['event']
trig_counts = {}
for s in stubs: trig_counts[s['trigger']] = trig_counts.get(s['trigger'], 0) + 1
out = dict(date='2026-10-13', scope='S118 implementation event stubs: naming, trigger, state reads/writes and cooldown for every corpus and field flow node; projection only, no engine ids claimed',
           conventions=['事件名 `evt_<脚本>_<节点>`，ID 中的 `-` 与 `.` 换成 `_`',
                        'reads/writes 必须是 [[状态键映射总表]] 里的键；写键只由结算/回执类节点写',
                        'cooldown：入口、结算、回执类 once；hub/any 类 repeatable',
                        '本表不声明真实引擎事件号；引擎号在实现阶段分配'],
           trigger_counts=trig_counts, stubs=stubs)
(ROOT / 'research' / 'event-stubs.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "事件桩映射总表"\nid: SYS-EVENT-STUBS-S118\ntype: system\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S118, system, implementation]\naliases: []\n---\n\n'
     '# 事件桩映射总表\n\n'
     f"把 [[全库条件流投影]] 与 [[野外对白条件流]] 的每个节点映射成事件桩（共 {len(stubs)} 个）：命名、触发、读写的状态键与冷却。"
     '数据在 `research/event-stubs.json`；本表不声明真实引擎事件号——引擎号在实现阶段分配。\n\n**约定**：\n\n' + '\n'.join('- ' + c for c in out['conventions']) + '\n\n'
     '| 触发 | 桩数 |\n|---|---:|\n')
for tname, cnt in sorted(trig_counts.items(), key=lambda x: -x[1]):
    n += f"| `{tname}` | {cnt} |\n"
n += '\n## 取样（每类触发）\n\n| 事件 | 脚本 | 条件 | 读 | 写 | 冷却 |\n|---|---|---|---|---|---|\n'
shown = set()
for s in stubs:
    if s['trigger'] in shown: continue
    shown.add(s['trigger'])
    n += (f"| `{s['event']}` | {s['script']} | `{s['when']}` | " + ('、'.join('`' + x + '`' for x in s['reads']) or '—') +
          ' | ' + ('、'.join('`' + x + '`' for x in s['writes'][:3]) or '—') + f" | {s['cooldown']} |\n")
n += ('\n## 与实现的关系\n\n- 引擎实现按本表建事件：读键判断、写键记录、冷却控制重复；节点台词与守卫仍以各台本与条件流为准。\n'
      '- 写键只出现在结算（`resolve_*`）、回执（`callback_*`、`receipt_*`）与授权（`consent_*`）类节点；hub 类只读不写。\n'
      '- 未做：真实引擎事件号、触发距离与作息、存档字段名与迁移。\n\n'
      '## 边界\n\n- 本页是实现用桩表：不含奖励、不含数值；不改任何台本内容。\n'
      '- 桩名可重排、可合并，但读写的键与守卫语义不得改变；改动须回写本表并重跑校验。\n\n'
      '[[状态键映射总表]] · [[全库条件流投影]] · [[野外对白条件流]] · [[特殊地点阶段制作与校准规程]] · [[设计库生成与校验流程]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S118事件桩映射（当前登记）\n\n'
           f"[[事件桩映射总表]]：{len(stubs)} 个事件桩（命名 evt_<脚本>_<节点>、触发/读写状态键/冷却），由条件流与状态键确定性投影；不声明真实引擎事件号。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/event-stubs-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted((ROOT / 'research').glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- EVENT-STUBS-S118:BEGIN -->\n2026-10-13 S118：事件桩映射（实现桥末端）。'
        f'research/event-stubs.json 把条件流每个节点映射成事件桩（共 {len(stubs)} 个：命名/触发/读写状态键/冷却），读写键必须在状态键表内；不声明真实引擎事件号。'
        '入口design/09_系统逻辑/事件桩映射总表.md；运行Validate-EventStubs.py及既有检查；引擎号、触发距离与存档字段仍待实现阶段。\n<!-- EVENT-STUBS-S118:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- EVENT-STUBS-S118:BEGIN -->.*?<!-- EVENT-STUBS-S118:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- EVENT-STUBS-S118:BEGIN -->.*?<!-- EVENT-STUBS-S118:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/09_系统逻辑/事件桩映射总表.md', '入口 [事件桩映射总表](design/09_系统逻辑/事件桩映射总表.md)'), encoding='utf-8')
print(json.dumps(dict(stubs=len(stubs), triggers=trig_counts, notes=len(generated)), ensure_ascii=False))
