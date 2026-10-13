"""S156: pilot implementation batch CS-BRY-01 (systems layer).

Extracts the city case's stubs/keys/flow/methods plus the BRY systems wiring
(service desk, trust bands, gossip pools) and renders the batch + scenario page.
Planning only: no implementation, no engine change.
"""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'PILOT-BRY01-S156'
CARD = '11_管理/试点实现批次CS-BRY-01.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
QID = 'CS-BRY-01'
st = json.loads((R / 'event-stubs.json').read_text(encoding='utf-8'))['stubs']
sk = json.loads((R / 'state-keys.json').read_text(encoding='utf-8'))['keys']
cf = json.loads((R / 'corpus-flows.json').read_text(encoding='utf-8'))['flows']
sv = json.loads((R / 'service-registry.json').read_text(encoding='utf-8'))['services']
tr = json.loads((R / 'town-reputation.json').read_text(encoding='utf-8'))
tg = json.loads((R / 'town-gossip.json').read_text(encoding='utf-8'))
bg = json.loads((R / 'band-gossip.json').read_text(encoding='utf-8'))
qst = [s for s in st if s['script'] == QID]
qkeys = [k for k in sk if k['script'] == QID]
qf = [f for f in cf if f['id'] == QID][0]
script = next(V.rglob('台本_CS-BRY-01_*.md')).read_text(encoding='utf-8')
sec = re.search(r'\n## 可执行方案与回访\n(.*?)(?=\n## )', script, re.S)
methods = [f"{m.group(1)}：{m.group(2).strip()}" for m in re.finditer(r'^###\s+([^\s：:]{1,24})[：:]\s*(.+?)\s*$', sec.group(1) if sec else '', re.M)]
edges = sorted({'X' + x for x in re.findall(r'\bX(\d\d)\b', script)})
svc = next(s for s in sv if s['id'] == 'SVC-BRY')
towns = tr['towns'] if isinstance(tr.get('towns'), list) else []
bry_town = next((t for t in towns if t.get('id') == 'BRY' or t.get('city') == 'BRY'), None)
tg_lines = [l for l in tg['lines'] if 'BRY' in json.dumps(l, ensure_ascii=False)[:200]]
bg_lines = [l for l in bg['lines'] if 'BRY' in json.dumps(l, ensure_ascii=False)[:200]]
SCEN = [
    dict(id='BRY01-T01', name='接取与首见', steps=['在布林找到本案入口并首次交谈'], writes=[('encountered_CS_BRY_01', 'true')],
         invariants=['resolve 保持 none', '不写 consent/paid']),
    dict(id='BRY01-T02', name='continuity 路线结算', steps=['完成实际核验', '选 continuity 并二次确认'],
         writes=[('resolve_CS_BRY_01', 'continuity'), ('callback_CS_BRY_01_continuity', 'true'),
                 ('consent_CS_BRY_01_continuity', 'true'), ('paid_CS_BRY_01_continuity', 'true')],
         invariants=['exit 组键不写', '未二次确认保持 pending']),
    dict(id='BRY01-T03', name='exit 路线结算', steps=['完成实际核验', '选 exit 并二次确认'],
         writes=[('resolve_CS_BRY_01', 'exit'), ('callback_CS_BRY_01_exit', 'true'),
                 ('consent_CS_BRY_01_exit', 'true'), ('paid_CS_BRY_01_exit', 'true')],
         invariants=['continuity 组键不写', '两路线互斥']),
    dict(id='BRY01-T04', name='拒绝与缺席', steps=['明确拒绝本案', '再接近同一人物'],
         writes=[('presence_CS_BRY_01', 'refused')],
         invariants=['resolve 保持 none', '缺席时只播代理句']),
    dict(id='BRY01-T05', name='早到/晚到回执', steps=['先做后续章再回本案', '或先结本案再做后续章'],
         writes=[('order_CS_BRY_01', 'early'), ('order_CS_BRY_01', 'late')],
         invariants=['两种顺序只改未来台词', '不回滚已结案', '不重复结算']),
    dict(id='BRY01-T06', name='服务班档位', steps=['以 0 档与 +1 档分别访问 BRY 服务班'],
         writes=[], invariants=['0 档按基础范围与正常价', '+1 档只多一处小便利', '不越权、不无限供给']),
    dict(id='BRY01-T07', name='闲谈池分离', steps=['分别以 0 档与 +1 档听街头反应'],
         writes=[], invariants=['城镇池与声望档池不串', '中间档不播档位池', '闲谈不改任何结算']),
]
rows = []
kmap = {k['key']: k for k in qkeys}
for s in SCEN:
    for key, val in s['writes']:
        spec = kmap.get(key)
        assert spec is not None, (s['id'], key)
        assert val in spec['values'], (s['id'], key, val, spec['values'])
        rows.append(dict(scenario=s['id'], key=key, value=val, kind=spec['kind']))
batch = dict(date='2026-10-13',
             scope='S156 pilot batch CS-BRY-01: city case with systems wiring (service desk, trust bands, gossip pools); planning only, nothing implemented',
             quest=QID,
             stubs=[dict(event=s['event'], node=s['node'], trigger=s['trigger'], cooldown=s['cooldown']) for s in qst],
             keys=[dict(key=k['key'], kind=k['kind'], values=k['values']) for k in qkeys],
             flow_nodes=[n['id'] for n in qf['nodes']], methods=methods, x_edges=edges,
             systems=dict(service=dict(id=svc['id'], name=svc['name_cn'], operator=svc['operator'], stock=svc['stock']),
                          trust_town=(bry_town or {}).get('id', 'BRY'),
                          town_gossip_lines=len(tg_lines), band_gossip_lines=len(bg_lines)),
             scenarios=[dict(id=s['id'], name=s['name'], steps=s['steps'], writes=s['writes'], invariants=s['invariants']) for s in SCEN],
             write_matrix=rows,
             gml_files=[f'cs_bry_01_{s["node"].replace(".", "_")}.gml' for s in qst])
(R / 'pilot-batch-cs-bry-01.json').write_text(json.dumps(batch, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "试点实现批次CS-BRY-01"\nid: MGMT-PILOT-BRY01-S156\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S156, guide, implementation]\naliases: []\n---\n\n'
     '# 试点实现批次CS-BRY-01\n\n'
     '[[试点实现批次N2]] 覆盖主章单案；本页是**系统层**试点：城市支线 `CS-BRY-01 一年之后`——含两条互斥路线、早到/晚到回执、拒绝/缺席、以及**服务班／信任档／闲谈池**三套系统的接线。仅排程与输入提取，不含实现代码、不部署；数据 `research/pilot-batch-cs-bry-01.json`。\n\n'
     '## 输入（现场提取）\n\n| 项 | 数量 | 明细 |\n| --- | ---: | --- |\n'
     f"| 事件桩 | {len(qst)} | {'、'.join('`' + s['event'] + '`' for s in qst)} |\n"
     f"| 状态键 | {len(qkeys)} | {'、'.join('`' + k['key'] + '`' for k in qkeys)} |\n"
     f"| 条件流节点 | {len(qf['nodes'])} | {'、'.join('`' + x + '`' for x in batch['flow_nodes'])} |\n"
     f"| 解法（R） | {len(methods)} | {'、'.join('`' + m + '`' for m in methods)} |\n"
     f"| X 边 | {len(edges)} | {'、'.join('`' + e + '`' for e in edges) or '—'} |\n\n"
     '## 系统层接线（与本案的关系）\n\n'
     f"- **服务班**：`{svc['id']}`「{svc['name_cn']}」（经办 `{svc['operator']}`），有限库存 {'、'.join(svc['stock'])}；本案只走普通运单誊写，不触银行／海关／货栈账。\n"
     f"- **信任档**：布林五档只改范围与便利（−2 关闭／−1 限范围／0 基础／+1 一处小便利／+2 预约与转介）；本案结算不因档位改结论。\n"
     f"- **闲谈池**：城镇池（本案相关 {len(tg_lines)} 条）与声望档池（{len(bg_lines)} 条）**分池播放**；中间档不播档位池，闲谈不改任何结算。\n\n"
     '## 落地顺序\n\n'
     '1. **键落库**：先建 10 键——`encountered_CS_BRY_01`、`resolve_CS_BRY_01`（none/continuity/exit）、两条路线各自的 `callback_/consent_/paid_`、`presence_CS_BRY_01`（四态）、`order_CS_BRY_01`（early/late/unknown）。\n'
     '2. **桩→事件**：14 桩一一对应（入口/枢纽/两条路线/三组早晚回执/拒绝/缺席/城前/城后）；回执桩读 `order_*` 决定早或晚。\n'
     '3. **台词接线**：按 [[全库条件流投影]] 的 `refs` 逐字接入；`consent_*` 只在本人分项授权后写，`paid_*` 只在真实交付后写。\n'
     '4. **系统接线**：服务班与闲谈池按上节规则落地；柜台句与街头反应分池，低档不删基本安全。\n'
     '5. **验收**：见下节场景；编译侧须与候选包同一 SHA，运行按 [[试玩路线与检查单]] 记录。\n\n'
     '## 验收场景\n\n| 场景 | 名称 | 期望写入 | 不得发生 |\n| --- | --- | --- | --- |\n')
for s in SCEN:
    writes = '；'.join(f"`{k}`＝`{v}`" for k, v in s['writes']) or '无写入'
    n += f"| {s['id']} | {s['name']} | {writes} | {'；'.join(s['invariants'])} |\n"
n += ('\n写入矩阵逐条对照 [[状态键映射总表]] 取值集合校验（登记 `research/pilot-batch-cs-bry-01.json`）：\n\n| 场景 | 键 | 取值 | 类型 |\n| --- | --- | --- | --- |\n')
for r in rows:
    n += f"| {r['scenario']} | `{r['key']}` | `{r['value']}` | {r['kind']} |\n"
n += ('\n## 建议新增文件（沿用既有命名）\n\n'
      + '\n'.join(f"- `src/EmbersAndOaths/Codes/{f}`（{s['trigger']}／{s['cooldown']}）" for f, s in zip(batch['gml_files'], qst)) + '\n\n'
      '## 边界\n\n'
      '- 键名口径：引擎键＝`EAO_`＋登记键名（见 [[引擎键名前缀与遗留键登记]]）。\n'
      '- 前置同 N2：OI-02（事件号）、OI-03（存档字段与迁移）；经济数值、比例与触发距离仍待实机。\n'
      '- 本页**不含实现代码、不分配事件号、不写数值、不部署**；未跑过的运行项不得标"已验证"。\n\n'
      '[[试点实现批次N2]] · [[试点批次验收场景N2]] · [[城市服务班与有限库存]] · [[城镇声望与信任系统]] · [[全库条件流投影]] · [[实现交接总表]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S156试点实现批次CS-BRY-01（当前登记）\n\n[[试点实现批次CS-BRY-01]]：系统层试点——{len(qst)} 桩、{len(qkeys)} 键、{len(qf['nodes'])} 流节点、{len(methods)} 解法，含早到/晚到、拒绝/缺席与**服务班／信任档／闲谈池**三套系统接线；7 条验收场景。仅排程。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'pilot-bry01-note-hashes.json'
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
rule = ('\n<!-- PILOT-BRY01-S156:BEGIN -->\n2026-10-13 S156：试点实现批次CS-BRY-01（系统层）。'
        f"{len(qst)}桩、{len(qkeys)}键、{len(qf['nodes'])}流节点、{len(methods)}解法；含服务班/信任档/闲谈池接线与7条验收场景（早到晚到、拒绝缺席、服务档位、闲谈分池）。"
        '键名口径同S155；仅排程与输入提取，不含实现代码、不部署。'
        '入口design/11_管理/试点实现批次CS-BRY-01.md；运行Validate-PilotBry01.py及既有检查。\n<!-- PILOT-BRY01-S156:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- PILOT-BRY01-S156:BEGIN -->.*?<!-- PILOT-BRY01-S156:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- PILOT-BRY01-S156:BEGIN -->.*?<!-- PILOT-BRY01-S156:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(stubs=len(qst), keys=len(qkeys), nodes=len(qf['nodes']), methods=len(methods),
                      scenarios=len(SCEN), gossip=[len(tg_lines), len(bg_lines)]), ensure_ascii=False))
