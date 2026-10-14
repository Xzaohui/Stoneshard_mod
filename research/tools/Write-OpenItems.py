"""S133: consolidated open-items register plus navigation refresh.

Aggregates every known gap from the stage records into one page with owner,
prerequisite and evidence pointer, and adds a navigation block to the design
overview linking the newest entry pages.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'OPEN-ITEMS-S133'
CARD = '11_管理/待办与已知缺口登记.md'
OVERVIEW = '00_导航/设计总览.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
ITEMS = [
 dict(id='OI-01', area='引擎实现', what='按 [[实现交接总表]] 六步建事件：状态键落库、事件桩、台词接线、服务班与声望、野外人物与文书迹象、闲谈池；首批执行见 [[试点批次总表]]（P1→P2→P3）。', owner='实现', prereq='无（设计侧已就绪）', status='open', evidence='research/event-stubs.json · research/state-keys.json · [[试点批次总表]]（2026-10-14：P1/N2 已落地，五桩五键三景两解法拒绝回访，0.3.2 候选过全部离线检查，未部署；P2/P3 待做）'),
 dict(id='OI-02', area='引擎实现', what='分配真实引擎事件号并回写 [[事件桩映射总表]]；桩名可重排但读写键不得变。', owner='实现', prereq='OI-01', status='open', evidence='research/event-stubs.json · [[事件桩映射总表]]（2026-10-14：P1 五桩已回写 10640–10644；其余 1,802 桩待各批次）'),
 dict(id='OI-03', area='引擎实现', what='存档字段命名与旧档迁移策略；旧字段不自动迁移，缺键按 none 处理。', owner='实现', prereq='OI-01', status='open', evidence='[[状态键映射总表]]（2026-10-14：OI-03 口径定稿并经 P1 五键离线落地；实机读档验证随 OI-10）'),
 dict(id='OI-04', area='引擎实现', what='触发距离、作息与生成点；按 [[特殊地点阶段制作与校准规程]] 的“引擎侧触发”节记录。', owner='实现', prereq='OI-01', status='open', evidence='research/production-protocol.json'),
 dict(id='OI-05', area='实机校准', what='经济数值采样：每城服务班实付/实收、材料价带、任务报酬区间；未采样不写数字。', owner='实机', prereq='OI-01', status='open', evidence='research/production-protocol.json'),
 dict(id='OI-06', area='制作', what='比例平面与碰撞：按地点卡“入口与安全回程”锚点测量入口坐标、可行走边界与尺寸。', owner='制作', prereq='OI-01', status='open', evidence='[[特殊地点设计卡总表]]'),
 dict(id='OI-07', area='制作', what='美术终稿与资源映射：概念板只作风貌参考，未定像素原点与碰撞。', owner='制作', prereq='无', status='open', evidence='[[城市美术与图片目录]]'),
 dict(id='OI-08', area='制作', what='配音与本地化终审：四套闲谈池与人物对白未录音、未做界面排版。', owner='制作', prereq='OI-01', status='open', evidence='[[氛围层总览与冻结建议]]'),
 dict(id='OI-09', area='设计（可选）', what='内部散文英文：人物细描、条件流、键与桩、阅读摘要仍中文先行，按计划不计缺口。', owner='设计', prereq='无', status='open', evidence='[[中英对照覆盖报告]]'),
 dict(id='OI-10', area='实机验证', what='按 [[试玩路线与检查单]] 十一段记录运行证据；未跑过的段不得标“已验证”。', owner='实机', prereq='OI-01', status='open', evidence='research/playtest-walkthrough.json'),
 dict(id='OI-11', area='交付', what='部署与回滚：候选包 SHA 与检查匹配后部署；更新前备份 data.win、MSL 设置、旧包与用户数据。基线指纹见 [[实现侧现状核对]]。', owner='实现', prereq='OI-01, OI-10', status='blocked', evidence='AGENTS.md 门槛 · [[实现侧现状核对]]'),
 dict(id='OI-12', area='内容', what='新增氛围句只在新增地点/聚落/派系时进行；氛围层冻结于 S129 尺度。', owner='设计', prereq='无', status='policy', evidence='[[氛围层总览与冻结建议]]'),
 dict(id='OI-14', area='验证', what='验证快照不得清理：11 份 `backups/…` 是保留性检查的“变更前”基线，缺失则对应校验器无法运行。', owner='实现', prereq='无', status='policy', evidence='[[验证快照依赖登记]]'),
 dict(id='OI-15', area='引擎实现', what='按 [[实现侧现状核对]] 的基线在既有工程上新建事件：现有 0.3.0 包不含 S62+ 设计稿，GML 代码 20 个、构建/部署脚本齐备。', owner='实现', prereq='无', status='open', evidence='[[实现侧现状核对]] · [[实现交接总表]]（2026-10-14：已在 0.3.1 工程定向更新出 0.3.2 候选，含 N2 五桩；未部署）'),
]
stems = {p.stem for p in V.rglob('*.md')}
for x in ITEMS:
    for m in re.finditer(r'\[\[([^\]]+)\]\]', x['what'] + ' ' + x['evidence']):
        assert m.group(1) in stems, x['id'] + ' link ' + m.group(1)
out = dict(date='2026-10-13', scope='S133 open-items register: consolidated gaps with owner, prerequisite, status and evidence pointer; register only, no design changes',
           items=ITEMS)
(ROOT / 'research' / 'open-items.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "待办与已知缺口登记"\nid: MGMT-OPEN-ITEMS-S133\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S133, review]\naliases: []\n---\n\n'
     '# 待办与已知缺口登记\n\n'
     f"把各阶段记录里的“未做/待核”汇总成一张表（{len(ITEMS)} 项），标明负责方、前置与证据位置。设计侧可做的已做完；下表除 OI-09（可选）与 OI-12（口径）外，都需要实现或实机。\n\n"
     '| 项 | 领域 | 内容 | 负责 | 前置 | 状态 | 证据 |\n|---|---|---|---|---|---|---|\n')
for x in ITEMS:
    n += f"| {x['id']} | {x['area']} | {x['what']} | {x['owner']} | {x['prereq']} | {x['status']} | {x['evidence']} |\n"
n += ('\n## 口径\n\n- `open`＝可做但未做；`blocked`＝须先完成前置；`policy`＝已定的口径而非待办。\n'
      '- 证据列指向可复核的登记文件或页；任何一项完成后须回写本表并留验收记录。\n'
      '- 未跑过的运行项不得标“已验证”；静态校验不替代运行结果。\n\n'
      '## 边界\n\n- 本页只汇总，不新增设计内容，也不改变任何门槛。\n'
      '- 各门槛原文仍以 `AGENTS.md` 与 [[特殊地点阶段制作与校准规程]] 为准。\n\n'
      '[[实现交接总表]] · [[特殊地点阶段制作与校准规程]] · [[试玩路线与检查单]] · [[叙事内容清单]] · [[逻辑验收记录]]\n')
put(CARD, n)
# navigation block on the overview (writer-owned note; blocks are preserved)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
nav = ('## 最新入口（S125—S163）\n\n'
       '**清点与交接**：[[叙事内容清单]] · [[中英对照覆盖报告]] · [[实现交接总表]] · [[试玩路线与检查单]] · [[待办与已知缺口登记]] · [[设计阶段收束核对]]。\n\n'
       '**原作参照**：[[原作名与原创名碰撞核对]] · [[原作契据任务与声誉结构参照]] · [[原作声誉档位与地方状态参照]]。\n\n'
       '**质量守卫**：[[质量守卫总表]] · [[逐角色稿完成度核对]] · [[说话人与人物卡闭合核对]] · [[对白去重与独特性核对]] · [[R-X头部补齐记录]] · [[验证快照依赖登记]] · [[登记文件覆盖分类]] · [[键名口径对账]]。\n\n'
       '**实现准备**：[[实现侧现状核对]] · [[工具链离线自检记录]] · [[试点批次总表]] · [[试点实现批次N2]] · [[试点批次验收场景N2]] · [[试点实现批次CS-BRY-01]] · [[试点实现批次FX野外层]] · [[引擎键名前缀与遗留键登记]] · [[N1小样键语义与迁移建议]] · [[事件号分配方案]] · [[全链复跑演练S145]]。')
t = (V / OVERVIEW).read_text(encoding='utf-8-sig')
nb = a + '\n' + nav + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(OVERVIEW, t2)
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb2 = a + '\n## S133待办与缺口登记（当前登记）\n\n[[待办与已知缺口登记]]：汇总 12 项待办/缺口（实现 5、制作 3、实机 3、设计 1 可选＋1 口径），标明负责方、前置与证据；设计总览补最新入口块。\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb2, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb2 + '\n'
put(PLAN, t2)
own = ROOT / 'research/open-items-note-hashes.json'
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
rule = ('\n<!-- OPEN-ITEMS-S133:BEGIN -->\n2026-10-13 S133：待办与已知缺口登记。'
        'research/open-items.json 汇总 12 项（实现5/制作3/实机3/设计可选1/口径1），标明负责方、前置与证据；设计总览补最新入口块。'
        '入口design/11_管理/待办与已知缺口登记.md；只汇总不改门槛。运行Validate-OpenItems.py及既有检查；不部署游戏包。\n<!-- OPEN-ITEMS-S133:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- OPEN-ITEMS-S133:BEGIN -->.*?<!-- OPEN-ITEMS-S133:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- OPEN-ITEMS-S133:BEGIN -->.*?<!-- OPEN-ITEMS-S133:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(items=len(ITEMS), notes=len(generated)), ensure_ascii=False))
