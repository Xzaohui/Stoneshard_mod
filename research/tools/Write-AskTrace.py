"""S173: traceability from the user's request clauses to deliverables and guards."""
from pathlib import Path
import hashlib, json, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'; R = ROOT / 'research'
MARK = 'ASK-TRACE-S173'
CARD = '11_管理/用户要求与交付对照.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
ROWS = [
    dict(ask='继续完善游戏背景故事', deliver=['[[世界背景与译名]]', '[[城市与聚落设计总索引]]', '[[新区域设计与任务总表]]'],
         guard='Test-DesignVault.ps1（双链/ID/锚点）', status='done', note='十五地域＋33 卫星＋区域卡；地方篇章不代替国策。'),
    dict(ask='台词', deliver=['[[逐角色稿完成度核对]]', '[[说话人与人物卡闭合核对]]', '[[对白去重与独特性核对]]'],
         guard='Validate-DialogueCoverage／SpeakerClosure／DialogueDistinctiveness', status='done',
         note='131 篇台本、2,717 行；说话人 232 位全闭合；重复 18 组全为主章—副本配对。'),
    dict(ask='任务设计', deliver=['[[任务台本总索引]]', '[[城市篇章与跨区域任务网]]', '[[时序与奖励总表]]'],
         guard='Validate-StoryScripts／CityCampaign／TimelineRegistry／CorpusFlows', status='done',
         note='N1—N18＋SQ＋DT＋D＋CS＋CM 共 131 篇；方法数守卫保证每篇 ≥2 条解法。'),
    dict(ask='各城镇声望系统', deliver=['[[城镇声望与信任系统]]', '[[城市服务班与有限库存]]', '[[原作声誉档位与地方状态参照]]'],
         guard='Validate-TownReputation／ServiceRegistry／ReputationReference', status='done',
         note='三层分账（原作声誉／阵营承诺／城镇信任）；信任档只改范围与便利，不照搬原版数值。'),
    dict(ask='中英对照版本', deliver=['[[城镇声望系统中英对照]]', '[[中英对照覆盖报告]]'],
         guard='Validate-BilingualCoverage', status='done', note='用户可见条目成对 1,384、中文单列 0。'),
    dict(ask='参照优秀游戏剧情设计', deliver=['[[参考游戏叙事与声望机制对照]]'],
         guard='Validate-ReferenceGames', status='done', note='BG3／DOS1／DOS2／Drova 四款机制＋教训＋取舍映射，引用 15 条 URL。'),
    dict(ask='网状叙述、任务关联', deliver=['[[叙事交叉影响矩阵]]', '[[全库条件流投影]]', '[[任务状态与依赖]]'],
         guard='Validate-NarrativeNetwork＋质量守卫「X边闭合」', status='done', note='74 条 X 边双向闭合（无脚本引用 0、悬空 0）。'),
    dict(ask='埋伏笔与回收伏笔', deliver=['[[伏笔与回收台账]]', '[[布林续篇任务与伏笔回收总表]]'],
         guard='Validate-ForeshadowLedger', status='done', note='主线丝线＋成组引用＋有意留白三档。'),
    dict(ask='丰富的 NPC、独特的对话', deliver=['[[人物细描与随身物]]', '[[说话人与人物卡闭合核对]]'],
         guard='Validate-FineDetails／CastRoster', status='done', note='217 张人物卡、172 名细描；无卡说话人 0。'),
    dict(ask='扒原作剧情与对话系统作参照', deliver=['[[原作剧情与对话系统参照]]', '[[原作契据任务与声誉结构参照]]', '[[原作声誉档位与地方状态参照]]', '[[原作名与原创名碰撞核对]]', '[[特殊地点与野外NPC清点]]'],
         guard='Probe-*（只读）＋Validate-OriginalNpcReading／NameCollision', status='done',
         note='只存键名/定位/≤46 字片段；不落原作全文。'),
    dict(ask='当前设计作为重要参考', deliver=['[[设计总览]]', '[[叙事内容清单]]', '[[质量守卫总表]]'],
         guard='Validate-ContentInventory／NavBlock／QualityGuards', status='done', note='645 篇设计库、86 校验器、13 万项检查。'),
    dict(ask='（阶段规则）本轮不部署新包', deliver=['[[实现侧现状核对]]', '[[构建前置核对]]', '[[试点批次总表]]'],
         guard='Validate-ImplState／BuildReadiness／PilotIndex', status='done',
         note='只构建候选（S170），未部署、未改游戏目录；部署与实机登记为 OI-10／OI-11。'),
]
reg = dict(date='2026-10-13',
           scope='S173 traceability: each clause of the user request mapped to delivered pages, their guards and status; deferred items point at the open-item register',
           rows=ROWS)
(R / 'ask-traceability.json').write_text(json.dumps(reg, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = hashlib.sha256(p.read_bytes()).hexdigest()
n = ('---\ntitle: "用户要求与交付对照"\nid: MGMT-ASK-TRACE-S173\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S173, review, traceability]\naliases: []\n---\n\n'
     '# 用户要求与交付对照\n\n'
     f"把用户提出的每一条要求对着**已交付页面与守卫**逐条核对（{len(ROWS)} 行），便于一眼审阅“要的都在不在”。数据 `research/ask-traceability.json`；未完成项指向 [[待办与已知缺口登记]]。\n\n"
     '| 要求 | 交付 | 守卫 | 状态 | 说明 |\n| --- | --- | --- | --- | --- |\n')
for r in ROWS:
    n += f"| {r['ask']} | {' · '.join(r['deliver'])} | {r['guard']} | {r['status']} | {r['note']} |\n"
n += ('\n## 口径\n\n'
      '- 「done」＝设计侧已交付且**有守卫**（可重跑核对）；不表示游戏内已实现或已运行。\n'
      '- 实现、制作、实机与部署不在本表——见 [[待办与已知缺口登记]]（OI-01…OI-15 中除已完成项外的 14 条）。\n'
      '- 表中每个交付页都由对应校验器或库检查覆盖；链接失效即由 `Validate-AskTraceability.py` 报错。\n\n'
      '## 边界\n\n'
      '- 本表是**索引**，不重复各页内容；守卫数量与检查数取各自报告现场值。\n'
      '- 文学质量、经济数值与运行表现不在守卫范围（见 [[质量守卫总表]] 边界）。\n\n'
      '[[设计阶段收束核对]] · [[质量守卫总表]] · [[待办与已知缺口登记]] · [[试点批次总表]] · [[逻辑验收记录]]\n')
put(CARD, n)
t = (V / PLAN).read_text(encoding='utf-8-sig')
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
blk = (a + f"\n## S173用户要求与交付对照（当前登记）\n\n[[用户要求与交付对照]]：{len(ROWS)} 行逐条对应“要求→交付页→守卫→状态”，便于审阅；未完成项指向 [[待办与已知缺口登记]]。\n" + z)
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + blk + '\n'
put(PLAN, t2)
own = R / 'ask-trace-note-hashes.json'
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
rule = ('\n<!-- ASK-TRACE-S173:BEGIN -->\n2026-10-13 S173：用户要求与交付对照。'
        '12行逐条对应“要求→交付页→守卫→状态”（背景/台词/任务/声望/中英对照/参照游戏/网状/伏笔/NPC/原作参照/设计参考/阶段规则），未完成项指向待办登记。'
        '入口design/11_管理/用户要求与交付对照.md；运行Validate-AskTraceability.py及既有检查。\n<!-- ASK-TRACE-S173:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- ASK-TRACE-S173:BEGIN -->.*?<!-- ASK-TRACE-S173:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- ASK-TRACE-S173:BEGIN -->.*?<!-- ASK-TRACE-S173:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
print(json.dumps(dict(rows=len(ROWS), pages=sum(len(r['deliver']) for r in ROWS)), ensure_ascii=False))
