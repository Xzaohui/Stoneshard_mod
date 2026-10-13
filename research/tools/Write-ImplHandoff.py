"""S122: implementation hand-off index for the design vault.

One page that lists the artifacts an implementer needs, the build order, the
per-step acceptance checks, the standing gates, and the items still open. Counts
are read live from the validation reports.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'IMPL-HANDOFF-S122'
CARD = '11_管理/实现交接总表.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
ARTIFACTS = [
 ('research/corpus-flows.json', '条件流（130 脚本节点与引用）', '[[全库条件流投影]]'),
 ('research/state-keys.json', '状态键（1385）', '[[状态键映射总表]]'),
 ('research/event-stubs.json', '事件桩（1735）', '[[事件桩映射总表]]'),
 ('research/field-scene-flows.json', '野外人物条件流（28 人）', '[[野外对白条件流]]'),
 ('research/field-npc-dialogue.json', '野外人物对白（中英）', '[[台本_FX_野外人物对白]]'),
 ('research/field-docs.json', '野外文书（中英）', '[[文书_FX_野外地点短稿]]'),
 ('research/field-signs.json', '野外迹象（中英）', '[[野外迹象与观察]]'),
 ('research/ambient-gossip.json', '地区闲谈（中英）', '[[地区闲谈池]]'),
 ('research/town-gossip.json', '城镇闲谈（中英）', '[[城镇闲谈池]]'),
 ('research/band-gossip.json', '声望档街头反应（中英）', '[[声望档街头反应]]'),
 ('research/town-reputation.json', '城镇声望与信任（五档）', '[[城镇声望与信任系统]]'),
 ('research/service-registry.json', '城市服务班（十五城）', '[[城市服务班与有限库存]]'),
 ('research/item-registry.json', '物品与术语对照', '[[原创物品与装备总表]]'),
 ('research/npc-fine-details.json', '人物细描（172）', '[[人物细描与随身物]]'),
 ('research/special-location-inventory.json', '原作地点清点', '[[特殊地点与野外NPC清点]]'),
 ('research/region-content-map.json', '原作区域映射', '[[原作地图区域与Mod内容映射]]'),
 ('research/production-protocol.json', '制作与校准规程', '[[特殊地点阶段制作与校准规程]]'),
 ('research/bilingual-coverage.json', '中英对照覆盖', '[[中英对照覆盖报告]]'),
]
STEPS = [
 ('状态键落库', '按 [[状态键映射总表]] 建存档字段：`resolve_*`（结算前 none）、`encountered_*`、`callback_*`、`consent_*`、`paid_*`、`order_*`、`presence_*`、`receipt_*`；旧字段不自动迁移。',
  '键名与取值与表一致；读档后未结算脚本仍为 none；不写入未登记键。'),
 ('事件桩建事件', '按 [[事件桩映射总表]] 逐桩建事件：触发、读写键、冷却；引擎事件号自行分配并回写本表。',
  '桩与节点一一对应；hub 类不写键；入口写 encountered；route 类读 resolve。'),
 ('台词与守卫接线', '按 [[全库条件流投影]] 的 refs 接线台词：refs 文本必须与台本逐字一致；守卫按节点 notes 与台本 guards 落地。',
  '播放条件与顺序正确；拒绝有出口；缺席不代播。'),
 ('服务班与声望档', '按 [[城市服务班与有限库存]] 与 [[城镇声望与信任系统]] 实现档位便利、边界与刷新；柜台台词与街头反应分池播放。',
  '低档只限范围、不删基本安全；不新增柜台；两池不串台词。'),
 ('野外人物与文书迹象', '按 [[台本_FX_野外人物对白]]、[[文书_FX_野外地点短稿]]、[[野外迹象与观察]] 落地：存在性四态、缺席替代、文书只给信息。',
  '缺席只播 proxy；文书阅读不推进任务、不发物品；迹象判定不含数值掉落。'),
 ('闲谈池播放', '按地区/城镇/声望档三池与条件词表播放；`after` 只改未来台词。',
  '三池互不克隆；中间档不播档位池；闲谈不改任何结算。'),
]
GATES = [
 '更新前备份 data.win、MSL 设置、本 Mod 旧包与用户数据；不主动删除角色、不覆盖存档。',
 '游戏或 MSL 占用文件时暂停部署；不强制结束用户进程。',
 '候选包 SHA 与校验场景匹配后才部署（沿用 tools/ 下既有链与检查）。',
 '运行验证按 [[特殊地点阶段制作与校准规程]] 记录：版本指纹、步骤、观察、截图/日志、差异与结论。',
 '未跑过的内容不得标“已验证”；静态校验不替代运行结果。',
]
OPEN_ITEMS = [
 '引擎事件号、触发距离、作息与生成点：实现阶段分配与测量。',
 '存档字段名与旧档迁移：本表只给键语义，迁移策略另定。',
 '经济数值：服务与材料价格须实机采样（规程已定口径，未采样不写数字）。',
 '比例地图与碰撞：地点卡只给相对布局与可认锚点。',
 '内部散文英文：人物细描、条件流、键与桩、阅读摘要仍中文先行（不计缺口）。',
 '配音与本地化终审：未做。',
]
missing = [a for a, _, _ in ARTIFACTS if not (ROOT / a).exists()]
assert not missing, missing
val = {n: read(f'research/{n}-validation.json')['checks_passed'] for n in
       ['corpus-flows', 'state-keys', 'event-stubs', 'field-flows', 'field-npc', 'field-docs', 'field-signs',
        'ambient-gossip', 'town-gossip', 'band-gossip', 'town-reputation', 'service-registry', 'fine-details',
        'special-location', 'region-map', 'prod-protocol', 'bilingual-coverage']}
out = dict(date='2026-10-13', scope='S122 implementation hand-off: artifact list, build order, per-step acceptance, standing gates and open items; counts read live from validation reports',
           artifacts=[dict(path=a, what=w, entry=e) for a, w, e in ARTIFACTS],
           steps=[dict(name=n, how=h, accept=a) for n, h, a in STEPS],
           gates=GATES, open_items=OPEN_ITEMS, validation=val)
(ROOT / 'research' / 'impl-handoff.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "实现交接总表"\nid: MGMT-IMPL-HANDOFF-S122\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S122, guide, implementation]\naliases: []\n---\n\n'
     '# 实现交接总表\n\n'
     '本页把设计库交给实现阶段：需要读哪些文件、按什么顺序建、每步怎么验、哪些门槛不变、哪些还没定。数据 `research/impl-handoff.json`；计数取自各校验报告（实时）。\n\n'
     '## 输入清单\n\n| 文件 | 内容 | 入口 |\n|---|---|---|\n')
for a, w, e in ARTIFACTS:
    n += f"| `{a}` | {w} | {e} |\n"
n += '\n## 实现顺序与验收\n\n首批执行按 [[试点批次总表]] 的三批推进（P1 主链 → P2 系统层 → P3 野外层）：每批含现场提取的输入、落地顺序、建议 GML 文件与验收场景；本节的六步是它们的共同骨架。\n\n'
n += '| 步 | 怎么做 | 验收 |\n|---|---|---|\n'
for name, how, acc in STEPS:
    n += f"| {name} | {how} | {acc} |\n"
n += '\n## 不变门槛\n\n' + '\n'.join('- ' + g for g in GATES) + '\n\n'
n += '## 尚未确定\n\n' + '\n'.join('- ' + o for o in OPEN_ITEMS) + '\n\n'
n += ('## 校验计数（实时）\n\n| 校验报告 | 项数 |\n|---|---:|\n')
for k, v in val.items():
    n += f"| `{k}` | {v} |\n"
n += ('\n## 边界\n\n- 本页不新增设计内容：只做索引、顺序与门槛；任何实现改动须回写对应登记文件并重跑校验。\n'
      '- 未跑过的实现不得标“已验证”；静态校验不替代运行结果。\n\n'
      '[[状态键映射总表]] · [[事件桩映射总表]] · [[全库条件流投影]] · [[特殊地点阶段制作与校准规程]] · [[设计库生成与校验流程]] · [[逻辑验收记录]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S122实现交接总表（当前登记）\n\n'
           f"[[实现交接总表]]：输入清单 {len(ARTIFACTS)} 项、实现顺序 {len(STEPS)} 步（含每步验收）、不变门槛 {len(GATES)} 条与尚未确定 {len(OPEN_ITEMS)} 项；计数取自实时校验报告。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/impl-handoff-note-hashes.json'
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
rule = ('\n<!-- IMPL-HANDOFF-S122:BEGIN -->\n2026-10-13 S122：实现交接总表。'
        f'research/impl-handoff.json 列输入清单 {len(ARTIFACTS)} 项、实现顺序 {len(STEPS)} 步（含每步验收）、不变门槛与尚未确定项；入口design/11_管理/实现交接总表.md；计数取自实时校验报告。'
        '不新增设计内容；运行Validate-ImplHandoff.py及既有检查；实现与运行验证仍待进行，不部署游戏包。\n<!-- IMPL-HANDOFF-S122:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- IMPL-HANDOFF-S122:BEGIN -->.*?<!-- IMPL-HANDOFF-S122:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- IMPL-HANDOFF-S122:BEGIN -->.*?<!-- IMPL-HANDOFF-S122:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/实现交接总表.md', '入口 [实现交接总表](design/11_管理/实现交接总表.md)'), encoding='utf-8')
print(json.dumps(dict(artifacts=len(ARTIFACTS), steps=len(STEPS), gates=len(GATES), open=len(OPEN_ITEMS), notes=len(generated)), ensure_ascii=False))
