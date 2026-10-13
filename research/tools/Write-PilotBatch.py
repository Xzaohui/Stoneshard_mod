"""S153: pilot implementation batch N2 - extract registry inputs and render the plan.

Reads the live registries for N2 (stubs, keys, flow nodes, script methods, X
edges) and writes the batch registry and the plan page. Planning only: nothing
is implemented, compiled or deployed.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'PILOT-N2-S153'
CARD = '11_管理/试点实现批次N2.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
st = json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs']
sk = json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys']
cf = json.loads((R / 'corpus-flows.json').read_text(encoding='utf-8'))['flows']
n2st = [s for s in st if s['script'] == 'N2']
n2k = [k for k in sk if k['script'] == 'N2']
n2f = [f for f in cf if f['id'] == 'N2'][0]
script = (V / '05_主线/台本/台本_N2_灰堤没有墓碑.md').read_text(encoding='utf-8')
methods = sorted({m for m in re.findall(r'\b(N2-R-[A-Za-z0-9\-]+)', script) if not m.endswith(('-L01', '-L02'))})
edges = sorted({'X' + x for x in re.findall(r'\bX(\d\d)\b', script)})
batch = dict(
    date='2026-10-13',
    scope='S153 pilot implementation batch N2: registry inputs extracted read-only; planning only, nothing implemented or deployed',
    script='N2', title='灰堤没有墓碑',
    stubs=[dict(event=s['event'], node=s['node'], when=s['when'], trigger=s['trigger'], reads=s['reads'], writes=s['writes'], cooldown=s['cooldown']) for s in n2st],
    keys=[dict(key=k['key'], kind=k['kind'], values=k['values']) for k in n2k],
    flow_nodes=[n['id'] for n in n2f['nodes']],
    methods=methods, x_edges=edges,
    gml_files=[f'n2_{s["node"].replace(".", "_")}.gml' for s in n2st],
)
(R / 'pilot-batch-n2.json').write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "试点实现批次N2"\nid: MGMT-PILOT-N2-S153\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S153, guide, implementation]\naliases: []\n---\n\n'
     '# 试点实现批次N2\n\n'
     '把 [[实现交接总表]] 的六步收敛成**第一个可验收的切片**：`N2 灰堤没有墓碑`（接在已实现的 N1 之后，X02 边）。本页只做**排程与输入提取**，不实现、不编译、不部署；数据 `research/pilot-batch-n2.json`（由登记现场提取）。\n\n'
     '## 输入（现场提取）\n\n| 项 | 数量 | 明细 |\n| --- | ---: | --- |\n'
     f"| 事件桩 | {len(n2st)} | {'、'.join('`' + s['event'] + '`' for s in n2st)} |\n"
     f"| 状态键 | {len(n2k)} | {'、'.join('`' + k['key'] + '`' for k in n2k)} |\n"
     f"| 条件流节点 | {len(n2f['nodes'])} | {'、'.join('`' + x + '`' for x in batch['flow_nodes'])} |\n"
     f"| 解法（R） | {len(methods)} | {'、'.join('`' + m + '`' for m in methods)} |\n"
     f"| X 边（本脚本引用） | {len(edges)} | {'、'.join('`' + e + '`' for e in edges)} |\n\n"
     '## 建议的落地顺序\n\n'
     '1. **键落库**：先建 5 个键（`encountered_N2` 二值、`resolve_N2` 三值 `none/protected/public`、两个 `callback_*` 二值、`presence_N2` 四态）；未结算保持 `none`，旧档缺键按 `none` 读。\n'
     '2. **桩→事件**：5 个桩一一对应到事件（引擎事件号在实现阶段分配并回写 [[事件桩映射总表]]）；`entry` 写 `encountered_N2`，`hub` 可重复且不写键，两个 `choice.*` 读 `resolve_N2`、写对应 `callback_*`，`refusal` 写 `presence_N2=refused`。\n'
     '3. **台词接线**：按 [[全库条件流投影]] 的 `refs` 逐字接入（入口 3 句、hub 3 句、两条解法与拒绝各按节点）；守卫沿用台本既有门槛（实际观察后才可回答）。\n'
     '4. **回访**：`X04`（→N3）与 `X05`（→SQ01）按"已结案只追加新回应、不回滚"落地；`X57/X58`（副本侧）在副本批次处理。\n'
     '5. **验收**：编译指令场景沿用既有链（33/8/5 项与新增场景须匹配同一候选 SHA）；运行按 [[试玩路线与检查单]] 记录——本条至少覆盖：接取、两条解法、拒绝、离场/死亡、回访、存读档不回退。\n\n'
     '## 建议新增文件（沿用既有命名）\n\n'
     + '\n'.join(f"- `src/EmbersAndOaths/Codes/{f}`（由对应桩生成：{s['trigger']}／{s['cooldown']}）" for f, s in zip(batch['gml_files'], n2st)) + '\n\n'
     '## 前置与边界\n\n'
     '- 键名口径：落库时引擎键＝`EAO_`＋登记键名（见 [[引擎键名前缀与遗留键登记]]）；小样 `EAO_N1_stage` 与登记 `resolve_N1` 的取舍属 OI-03。\n'
     '- 前置：OI-02（引擎事件号分配）、OI-03（存档字段命名与旧档策略）；两项未定则事件号与键名只作占位。\n'
     '- 本页**不含**实现代码、不分配事件号、不写数值；经济、比例与触发距离仍待实机（见 [[待办与已知缺口登记]]）。\n'
     '- 未跑过的运行项不得标"已验证"；静态校验不替代游戏内结果。\n\n'
     '[[实现交接总表]] · [[事件桩映射总表]] · [[状态键映射总表]] · [[全库条件流投影]] · [[实现侧现状核对]] · [[试玩路线与检查单]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S153试点实现批次（当前登记）\n\n[[试点实现批次N2]]：把六步收敛为第一个可验收切片——N2 共 {len(n2st)} 桩、{len(n2k)} 键、{len(n2f['nodes'])} 流节点、{len(methods)} 解法；落地顺序、建议新增 GML 文件与验收项已列；仅排程，不含实现代码。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'pilot-batch-note-hashes.json'
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
rule = ('\n<!-- PILOT-N2-S153:BEGIN -->\n2026-10-13 S153：试点实现批次N2。'
        f"把实现交接六步收敛为首个可验收切片（N2）：{len(n2st)}桩、{len(n2k)}键、{len(n2f['nodes'])}流节点、{len(methods)}解法、X边{len(edges)}条；"
        '给出落地顺序、建议GML文件与验收项；仅排程与输入提取，不含实现代码、不分配事件号、不部署。'
        '入口design/11_管理/试点实现批次N2.md；运行Validate-PilotBatch.py及既有检查。\n<!-- PILOT-N2-S153:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- PILOT-N2-S153:BEGIN -->.*?<!-- PILOT-N2-S153:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- PILOT-N2-S153:BEGIN -->.*?<!-- PILOT-N2-S153:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(stubs=len(n2st), keys=len(n2k), nodes=len(n2f['nodes']), methods=len(methods), edges=edges), ensure_ascii=False))
