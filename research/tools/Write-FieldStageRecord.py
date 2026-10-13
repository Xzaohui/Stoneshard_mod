"""S102 wrap-up: render the special-location/field-NPC stage acceptance record.

Summarises what the stage delivered (inventory, reading, people, sites, signs,
documents, cross-check, ledger references) and states what remains pending
(economy calibration, proportional maps, spawn points, runtime, English).
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'FIELD-STAGE-S102'
CARD = '11_管理/特殊地点与野外NPC阶段验收记录.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
inv = read('research/special-location-inventory.json')
rd = read('research/original-npc-reading.json')
fx = read('research/field-npc-dialogue.json')
sg = read('research/field-signs.json')
fd = read('research/field-docs.json')
xc = read('research/mod-location-crosscheck.json')
led = read('research/foreshadow-ledger.json')
val = {n: read(f'research/{n}-validation.json') for n in
       ['special-location', 'npc-reading', 'field-npc', 'site-cards', 'mod-loc-xcheck', 'field-docs', 'field-signs',
        'field-flows', 'region-map', 'foreshadow-ledger']}
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "特殊地点与野外NPC阶段验收记录"\nid: MGMT-FIELD-STAGE-S102\ntype: review\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S102, review]\naliases: []\n---\n\n'
     '# 特殊地点与野外NPC阶段验收记录\n\n'
     '本页汇总[[特殊地点与野外NPC对白扩展计划]]的执行结果与剩余项。全部为设计库内产出：只读清点与原创设计；未改游戏包、未部署、未做运行验证。\n\n'
     '## 交付\n\n| 项 | 数量 | 入口 | 校验 |\n|---|---:|---|---|\n')
rows = [
 ('世界地图区域 / 特殊地点候选 / 地形类型', f"{len(inv['map_regions'])} / {len(inv['rumor_sites'])} / {len(inv['site_types'])}", '[[特殊地点与野外NPC清点]]', val['special-location']['checks_passed']),
 ('问候·闲谈阅读（说话人槽归组）', f"{rd['slots']} 槽 / {len(rd['groups'])} 组", '[[野外NPC口吻与闲谈参照]]', val['npc-reading']['checks_passed']),
 ('npc 行为槽分组 / 场景族结论', f"{len(rd['npc_tags'])} 组 / 引擎侧", '[[野外NPC口吻与闲谈参照]]', val['npc-reading']['checks_passed']),
 ('野外人物（含条件回访）', f"{len(fx['npcs'])} 人 / {sum(len(x['greetings']) + len(x['chats']) + len(x['site_lines']) + sum(len(x['visits'][k]) for k in ('before', 'after', 'early', 'late', 'proxy')) for x in fx['npcs'])} 条", '[[台本_FX_野外人物对白]]', val['field-npc']['checks_passed']),
 ('地点设计卡', f"{len(inv['rumor_sites'])} 处 / 6 地域", '[[特殊地点设计卡总表]]', val['site-cards']['checks_passed']),
 ('野外迹象', f"{len(sg['signs'])} 处", '[[野外迹象与观察]]', val['field-signs']['checks_passed']),
 ('野外文书', f"{len(fd['docs'])} 份", '[[文书_FX_野外地点短稿]]', val['field-docs']['checks_passed']),
 ('Mod 地点/人物交叉核对', f"{len(xc['dungeons'])} 副本 / {len(xc['brynn_spaces'])} 场景 / {len(xc['field_npcs'])} 人", '[[Mod特殊地点与人物交叉核对]]', val['mod-loc-xcheck']['checks_passed']),
 ('伏笔台账引用组', f"{sum(1 for t in led['threads'] if t['bucket'] == 'reference')} 组 / 共 {len(led['threads'])} 线程", '[[伏笔与回收台账]]', val['foreshadow-ledger']['checks_passed']),
 ('野外对白条件流', '28 人 / 9 节点模板', '[[野外对白条件流]]', val['field-flows']['checks_passed']),
 ('原作区域映射', '8 区域', '[[原作地图区域与Mod内容映射]]', val['region-map']['checks_passed']),
 ('中英对照（人物/文书/迹象）', '28人×14槽＋12文书＋16迹象', '[[台本_FX_野外人物对白]]', val['field-npc']['checks_passed']),
]
for name, count, entry, checks in rows:
    n += f"| {name} | {count} | {entry} | {checks} 项 |\n"
n += ('\n## 覆盖结论\n\n'
      f"- 44 处传闻地点全部有内容落点：28 处有人物（{len(fx['npcs'])} 名，含任务进行中/完成后与先做/后做回访）、16 处有迹象。\n"
      '- 地点卡逐处给出用途、固定可观察物、特殊危险与关联；地域级给出入口与安全回程锚点、服务（一律不新增）与原作避让。\n'
      '- 全部对白、文书与迹象为 Mod 原创：不复用原句、不新增奖励、不占原生服务、不做全巡前置；阅读与观察只给信息。\n'
      '- 台账以引用组登记（FS-33—FS-36），与主线/续篇/回执机制分开计数，不合并、不重复。\n\n'
      '## 剩余项\n\n'
      '- 经济数值：服务与材料的价格区间未定，须实机校准；本阶段不承诺任何数值。\n'
      '- 比例地图与生成点：地点卡只给相对位置与可认锚点，瓦片比例、碰撞、生成权重与触发范围未做。\n'
      '- 运行验证：未进游戏核对可达性与对白播放；键存在不证明可触发。\n'
      '- 英文稿：野外人物的对白（28×14 槽）、12 份文书与 16 处迹象已出中英对照（S106/S107，英文为 Mod 原创、不冒充原版译文）；地点卡、区域映射与验收页仍中文先行。\n'
      '- 逐地点条件流已出（[[野外对白条件流]]，S105）；引擎侧触发距离、作息与生成点仍留待实现阶段。\n\n'
      '## 校验记录\n\n'
      '- 阶段新增校验器：SpecialLocationInventory、OriginalNpcReading、FieldNpcDialogue、SpecialSiteCards、ModLocationCrosscheck、FieldDocs、FieldSigns；全量套件与 `Test-DesignVault.ps1` 通过。\n'
      '- 对白独特性审计已并入野外对白源（全库含克隆与后台泄漏检查）。\n'
      '- 详细记录见[[逻辑验收记录]] S92—S102 各块。\n\n'
      '[[特殊地点与野外NPC对白扩展计划]] · [[特殊地点与野外NPC清点]] · [[城市扩展验收记录]] · [[设计库生成与校验流程]] · [[设计总览]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S102阶段验收记录（当前登记）\n\n'
           f"[[特殊地点与野外NPC阶段验收记录]]：清点8区域/44地点/13类型、阅读{rd['slots']}槽/17组与npc行为槽、{len(fx['npcs'])}名野外人物、44地点卡、16迹象、12文书、Mod交叉核对与台账引用组（FS-33—FS-36）；剩余：经济数值、比例与生成点、运行验证、英文稿、交互脚本。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
# ---- index entry blocks (discoverability from the navigation notes) ----
a2 = '<!-- FIELD-STAGE-S111:BEGIN -->'; z2 = '<!-- FIELD-STAGE-S111:END -->'
entry = ('## 追加阶段入口（S92—S111）\n\n'
         '[[特殊地点与野外NPC阶段验收记录]] · [[特殊地点与野外NPC清点]] · [[台本_FX_野外人物对白]] · [[文书_FX_野外地点短稿]] · [[野外迹象与观察]] · [[野外对白条件流]] · [[特殊地点设计卡总表]] · [[原作地图区域与Mod内容映射]] · [[野外内容规则一致性审计]] · [[特殊地点阶段制作与校准规程]]。'
         '8区域/44地点清点、28名野外人物（中英对照）、44地点卡、16迹象、12文书、条件流与规则审计；剩余经济/比例/运行见规程。')
for rel in ['00_导航/任务台本总索引.md', '00_导航/城市与聚落设计总索引.md']:
    p2 = V / rel
    if not p2.exists(): continue
    t2 = p2.read_text(encoding='utf-8-sig')
    nb2 = a2 + '\n' + entry + '\n' + z2
    t3 = re.sub(re.escape(a2) + '.*?' + re.escape(z2), lambda _: nb2, t2, flags=re.S) if a2 in t2 else t2.rstrip() + '\n\n' + nb2 + '\n'
    put(rel, t3)
own = ROOT / 'research/field-stage-note-hashes.json'
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
rule = ('\n<!-- FIELD-STAGE-S102:BEGIN -->\n2026-10-13 S102：特殊地点与野外NPC阶段收口。'
        '入口design/11_管理/特殊地点与野外NPC阶段验收记录.md：清点8区域/44地点/13类型、阅读72槽/17组+npc行为槽与场景族结论、28名野外人物（392条含条件回访）、44地点卡、16迹象、12文书、Mod交叉核对与伏笔台账引用组FS-33..36；'
        '剩余经济数值、比例与生成点、运行验证、英文稿与逐地点交互脚本。运行Validate-FieldStage.py及既有检查；不部署游戏包。\n<!-- FIELD-STAGE-S102:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- FIELD-STAGE-S102:BEGIN -->.*?<!-- FIELD-STAGE-S102:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- FIELD-STAGE-S102:BEGIN -->.*?<!-- FIELD-STAGE-S102:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/11_管理/特殊地点与野外NPC阶段验收记录.md', '入口 [特殊地点与野外NPC阶段验收记录](design/11_管理/特殊地点与野外NPC阶段验收记录.md)'), encoding='utf-8')
print(json.dumps(dict(rows=len(rows), notes=len(generated)), ensure_ascii=False))
