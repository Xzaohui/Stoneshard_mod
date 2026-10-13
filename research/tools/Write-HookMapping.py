"""S171: hook mapping - how each stub trigger kind attaches to the engine.

Extracts the trigger distribution from the stub registry and the concrete hook
patterns from the implemented sample, then renders the wiring page. Read-only.
"""
from pathlib import Path
import hashlib, json, collections, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'HOOK-MAP-S171'
CARD = '11_管理/触发器接线点映射.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
STUBS_PAGE = '09_系统逻辑/事件桩映射总表.md'
stubs = json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs']
counts = collections.Counter(s['trigger'] for s in stubs)
cooldowns = collections.Counter(s['cooldown'] for s in stubs)
codes = ROOT / 'src/EmbersAndOaths/Codes'
def ev(symbol, file):
    for i, line in enumerate((codes / file).read_text(encoding='utf-8').splitlines(), 1):
        if symbol in line:
            return dict(file=file, line=i, code=line.strip()[:110])
    return None
HOOKS = {
    'on_first_interaction': dict(pattern='对象创建 + 原生对白流登记', evidence=[ev('instance_create_depth', 'night_controller_step.gml'), ev('__dialogue_flow_data', 'night_controller_step.gml')],
                                 rule='首见对象只在原生前置满足时生成；对话经 `__dialogue_flow_data` 登记，写 encountered 一次。'),
    'on_interaction': dict(pattern='对象存在 + 可重复对白', evidence=[ev('instance_exists', 'night_controller_step.gml')],
                           rule='对象已存在即播；不写键（可重复），只按既有回执分流。'),
    'on_route_selected': dict(pattern='结算提交点 + 键写入', evidence=[ev('ds_map_set', 'controller_step.gml')],
                              rule='只在"实际处置 + 二次确认"之后写 resolve/callback/consent/paid；预览与关闭不写。'),
    'on_state_change': dict(pattern='键写入 + 后续重评', evidence=[ev('ds_map_set', 'night_entry_alarm.gml')],
                            rule='状态变化只重评未来行动；不回溯已结案，不重复结算。'),
    'on_state_read': dict(pattern='只读判定（对话线选择）', evidence=[ev('ds_map_find_value', 'night_controller_step.gml')],
                          rule='读取只用于选线与守卫；读不改状态，也不构成"已知"授权。'),
    'on_refusal': dict(pattern='拒绝分支（不写 resolve）', evidence=[ev('ds_map_find_value', 'test_teleport_execute.gml')],
                       rule='拒绝写 presence=refused；resolve 保持 none，拒绝后只播拒绝回应。'),
    'on_presence_check': dict(pattern='存在性四态评估 + 缺席替代', evidence=[ev('instance_exists', 'controller_step.gml')],
                              rule='present/absent/dead/refused 四态先判；缺席只播代理句，死亡/拒绝停本人新句。'),
    'on_interaction_if_night': dict(pattern='昼夜条件 + 对白', evidence=[ev('instance_exists', 'night_controller_step.gml')],
                                    rule='按房间/时段条件决定是否播；条件不满足时保留基础入口，不吞掉对话。'),
}
for k in counts:
    assert k in HOOKS, k
facts = dict(date='2026-10-13',
             scope='S171 hook mapping: eight trigger kinds mapped to concrete engine hook patterns with evidence from the implemented sample; read-only',
             trigger_counts=dict(counts), cooldown_counts=dict(cooldowns), hooks=HOOKS)
(R / 'hook-mapping.json').write_text(json.dumps(facts, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "触发器接线点映射"\nid: MGMT-HOOK-MAP-S171\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S171, guide, implementation]\naliases: []\n---\n\n'
     '# 触发器接线点映射\n\n'
     f"[[事件桩映射总表]] 的 **{len(stubs)}** 个桩共用 **{len(counts)} 种触发**；本页把每种触发接到已实现小样里**可核对的原生钩子**（对象创建、对白流登记、键读写、原生前置），供实现轮照此接线。只读提取，不改源码；数据 `research/hook-mapping.json`。\n\n"
     '## 触发 → 钩子\n\n| 触发 | 桩数 | 钩子形态 | 证据（小样） | 口径 |\n| --- | ---: | --- | --- | --- |\n')
for k, c in counts.most_common():
    h = HOOKS[k]
    evd = h['evidence'][0]
    evtxt = f"`{evd['file']}:{evd['line']}`" if evd else '—'
    n += f"| `{k}` | {c} | {h['pattern']} | {evtxt} | {h['rule']} |\n"
n += (f"\n冷却分布：`once` {cooldowns.get('once', 0)}／`repeatable` {cooldowns.get('repeatable', 0)}——一次性桩负责结算与回执，可重复桩只改未来台词。\n\n"
      '## 原生钩子清单（小样证据）\n\n| 钩子 | 用途 | 证据 |\n| --- | --- | --- |\n')
seen = {}
for k, h in HOOKS.items():
    for e in h['evidence']:
        if e and e['file'] + str(e['line']) not in seen:
            seen[e['file'] + str(e['line'])] = e
for key, e in sorted(seen.items()):
    n += f"| `{e['code'][:48]}` | {k} 的接线依据 | `{e['file']}:{e['line']}` |\n"
n += ('\n说明：小样用 `characterDataMap` 存键、`__dialogue_flow_data`／`npc_lines_map` 登记对白、`instance_create_depth` 生成对象、`event_user(N)` 驱动控制器生命周期、`scr_quest_get_complete` 作原生前置——新内容沿用同一组钩子，不另造第二套。\n\n'
      '## 边界\n\n'
      '- 小样是 0.3.0 期原型：钩子名与调用方式可核对，但**不代表新内容已接线**；实现轮按本表落位并逐桩回写。\n'
      '- 触发距离、作息与生成权重仍待实机（见 [[待办与已知缺口登记]]）。\n'
      '- 本页不改源码、不构建、不部署。\n\n'
      '[[事件桩映射总表]] · [[试点批次总表]] · [[事件号分配方案]] · [[引擎键名前缀与遗留键登记]] · [[实现交接总表]]\n')
put(CARD, n)
sp = (V / STUBS_PAGE).read_text(encoding='utf-8')
if '触发器接线点映射' not in sp:
    sp = sp.rstrip() + '\n\n<!-- HOOK-MAP-S171:BEGIN -->\n[[触发器接线点映射]]：八种触发接到小样可核对的原生钩子（对象创建／对白流登记／键读写／原生前置），供实现轮照此接线。\n<!-- HOOK-MAP-S171:END -->\n'
    put(STUBS_PAGE, sp)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S171触发器接线点映射（当前登记）\n\n[[触发器接线点映射]]：{len(stubs)} 桩的 **{len(counts)} 种触发**逐一接到小样原生钩子（`characterDataMap`／`__dialogue_flow_data`／`instance_create_depth`／`event_user`／`scr_quest_get_complete`），附证据行号与口径。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'hook-map-note-hashes.json'
own.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
for hp in sorted(R.glob('*note-hashes.json')):
    if hp == own: continue
    try: h = json.loads(hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    touched = False
    for rel in list(h):
        if rel in changed and h[rel] != generated[rel]: h[rel] = generated[rel]; touched = True
    if touched: hp.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
rule = ('\n<!-- HOOK-MAP-S171:BEGIN -->\n2026-10-13 S171：触发器接线点映射（只读）。'
        f"{len(stubs)}桩的{len(counts)}种触发逐一接到小样原生钩子（characterDataMap/__dialogue_flow_data/instance_create_depth/event_user/scr_quest_get_complete），附证据行号与口径；"
        '实现轮照此接线并逐桩回写；不改源码、不构建、不部署。'
        '入口design/11_管理/触发器接线点映射.md；运行Validate-HookMapping.py及既有检查。\n<!-- HOOK-MAP-S171:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- HOOK-MAP-S171:BEGIN -->.*?<!-- HOOK-MAP-S171:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- HOOK-MAP-S171:BEGIN -->.*?<!-- HOOK-MAP-S171:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(triggers=len(counts), stubs=len(stubs), once=cooldowns.get('once'), repeatable=cooldowns.get('repeatable')), ensure_ascii=False))
