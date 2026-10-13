"""S108: production and calibration protocol for the special-location stage.

Records how the remaining items (economy figures, proportions and spawn points,
runtime checks, engine-side triggers) are to be measured, what evidence must be
kept, and what may not be written before measurement. No numeric claims.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'PROD-PROTOCOL-S108'
CARD = '11_管理/特殊地点阶段制作与校准规程.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
SECTIONS = [
 dict(id='economy', title='经济数值校准',
      target='每城服务班一次普通交易的实付与实收、普通材料的市场价带、任务报酬的区间与上限。',
      fields=['日期与版本指纹（data.win/组合包 SHA）', '城镇与服务班 ID、档位（−2..+2）', '物品或服务 ID 与数量',
              '实付、实收、找零或拒收', '来源定位（日志行号或截图文件名）', '异常（折扣、拒收、缺货）与原因'],
      sample='至少 3 座城 × 3 个档位 × 2 种材料；服务班与普通商店分别采样，不混用。',
      pass_cond='实测区间与[[城市服务班与有限库存]]的档位语义一致，或在记录中列出差异与原因。',
      forbid='未采样不得在库内写任何具体数字；不得把原作商店价格直接当作本 Mod 价格。'),
 dict(id='maps', title='比例与生成点',
      target='地点入口锚点坐标、可行走网格边界、房间或场地尺寸、生成点位置与触发半径。',
      fields=['地点 ID（`rumor_*`）与地点卡链接', '入口锚点坐标与可认参照（灯、旗、基座等）',
              '可行走区域边界与障碍', '生成点坐标、朝向与触发半径', '与地点卡“入口与安全回程”的一致性核对'],
      sample='每个有人物或文书的地点至少 1 次实测；猎场与巢穴类按区域各测 1 处代表点。',
      pass_cond='实测锚点与地点卡所列可认参照一致；不一致时改卡或改点，并记录原因。',
      forbid='未测量不得画比例图、不得在库内写尺寸数字；不得用自制传送替代原生转场。'),
 dict(id='runtime', title='运行验证',
      target='可达性、对白播放条件、拒绝与缺席路径、文书读取、迹象观察、奖励泄漏检查。',
      fields=['验证项与地点/人物 ID', '执行步骤（进入、触发、退出）', '观察结果（播放/未播放、是否可退）',
              '截图或日志定位', '与设计口径的差异', '结论（通过/差异/未通过）'],
      sample='每人物的初遇、复访与一条条件回访各验一次；文书与迹象各验 1 份/处代表。',
      pass_cond='对白按条件播放、拒绝有出口、缺席不代播、文书只给信息、无奖励泄漏。',
      forbid='未在游戏内跑过不得标记“已验证”；模拟或替身结果不计入运行验证。'),
 dict(id='triggers', title='引擎侧触发',
      target='触发距离、作息与生成权重的最终值，以及条件流到引擎事件的映射。',
      fields=['节点 ID（[[野外对白条件流]]）与引擎事件名', '触发条件（距离、时段、任务状态）',
              '冷却与重复策略', '与条件流的偏差记录'],
      sample='每人至少映射初遇与一条条件回访；同一地点多人物时按优先顺序各测一次。',
      pass_cond='引擎事件与条件流节点一一对应；偏差在记录中列明并回写条件流。',
      forbid='不得新增条件流之外的分支；不得把触发距离写成奖励或门槛。'),
]
assert len({s['id'] for s in SECTIONS}) == len(SECTIONS)
for s in SECTIONS:
    assert all(s[k].strip() for k in ('title', 'target', 'sample', 'pass_cond', 'forbid'))
    assert len(s['fields']) >= 4
out = dict(date='2026-10-13', scope='S108 production and calibration protocol: what to measure for economy, proportions/spawns, runtime and engine triggers; evidence fields; pass conditions; prohibitions',
           sections=SECTIONS)
(ROOT / 'research' / 'production-protocol.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "特殊地点阶段制作与校准规程"\nid: MGMT-PROD-PROTOCOL-S108\ntype: guide\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S108, guide]\naliases: []\n---\n\n'
     '# 特殊地点阶段制作与校准规程\n\n'
     '[[特殊地点与野外NPC阶段验收记录]]剩余四项（经济数值、比例与生成点、运行验证、引擎侧触发）的测量与记录口径。本页只写“怎么测、记什么、什么算通过、什么不许写”，不含任何实测数字；'
     '未测量的内容不得在库内补成具体值。\n\n'
     '| 项 | 测量对象 | 采样要求 | 通过条件 |\n|---|---|---|---|\n')
for s in SECTIONS:
    n += f"| {s['title']} | {s['target']} | {s['sample']} | {s['pass_cond']} |\n"
for s in SECTIONS:
    n += f"\n## {s['title']}\n\n**测量对象**：{s['target']}\n\n**记录字段**：\n\n" + '\n'.join('- ' + f for f in s['fields']) + \
         f"\n\n**采样要求**：{s['sample']}\n\n**通过条件**：{s['pass_cond']}\n\n**禁止**：{s['forbid']}\n"
n += ('\n## 通用要求\n\n- 一切测量先记录版本与指纹（`vanilla.win` 与当前组合包 SHA），并保留部署前备份；不覆盖玩家存档。\n'
      '- 结果写入 `research/` 对应记录文件；与设计口径不一致时改设计或改实现，并在[[逻辑验收记录]]留一行差异。\n'
      '- 未测、部分测或替身验证一律标“未验证”；设计库静态通过不替代运行结果。\n\n'
      '## 边界\n\n- 本页不含数值、尺寸与坐标；它定义记录格式与门槛。\n'
      '- 部署仍走 `tools/` 下的构建/部署链与既有备份约定；本页不授权跳过任何备份或校验步骤。\n\n'
      '[[特殊地点与野外NPC阶段验收记录]] · [[特殊地点与野外NPC对白扩展计划]] · [[设计库生成与校验流程]] · [[城市服务班与有限库存]] · [[野外对白条件流]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S108制作与校准规程（当前登记）\n\n'
           "[[特殊地点阶段制作与校准规程]]：经济数值、比例与生成点、运行验证、引擎侧触发四项的测量对象/记录字段/采样要求/通过条件/禁止清单；不含任何实测数字，未测量不得补值。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/prod-protocol-note-hashes.json'
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
rule = ('\n<!-- PROD-PROTOCOL-S108:BEGIN -->\n2026-10-13 S108：特殊地点阶段剩余四项（经济数值、比例与生成点、运行验证、引擎侧触发）出制作与校准规程。'
        'research/production-protocol.json 定义测量对象/记录字段/采样/通过条件/禁止清单；入口design/11_管理/特殊地点阶段制作与校准规程.md。'
        '不含实测数字，未测量不得补值；运行与数值仍待实机。运行Validate-ProdProtocol.py及既有检查；不部署游戏包。\n<!-- PROD-PROTOCOL-S108:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- PROD-PROTOCOL-S108:BEGIN -->.*?<!-- PROD-PROTOCOL-S108:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- PROD-PROTOCOL-S108:BEGIN -->.*?<!-- PROD-PROTOCOL-S108:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/特殊地点阶段制作与校准规程.md', '入口 [特殊地点阶段制作与校准规程](design/11_管理/特殊地点阶段制作与校准规程.md)'), encoding='utf-8')
print(json.dumps(dict(sections=len(SECTIONS), notes=len(generated)), ensure_ascii=False))
