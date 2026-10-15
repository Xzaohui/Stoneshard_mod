"""Render the S89 fine-detail registries (items/equipment and NPC detail) into the vault."""
from pathlib import Path
import json, hashlib, re
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'FINE-DETAILS-S89'
HP = ROOT / 'research/fine-details-generated-note-hashes.json'
ITEM_DOC = '05_主线/原创物品与装备总表.md'
NPC_DOC = '04_人物/人物细描与随身物.md'
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def front(t, i, k, tags): return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [{tags}]\naliases: []\n---\n\n# {t}\n\n'

items = read('research/item-registry.json')
npcs = read('research/npc-fine-details.json')
model = read('research/city-campaign.json')

manifests = {}
for p in sorted((ROOT / 'research').glob('*note-hashes.json')):
    try: h = read('research/' + p.name)
    except Exception: continue
    if not isinstance(h, dict) or not all(isinstance(v, str) for v in h.values()): continue
    for rel, expected in h.items():
        if sha(ROOT / rel) != expected: raise SystemExit('Preserve/reconcile prior note: ' + rel)
    manifests[p] = h

changed = set(); generated = {}
def put(rel, text, own=False):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8'); changed.add('design/' + rel)
    if own: generated['design/' + rel] = sha(p)

# ---------- items doc ----------
t = front('原创物品与装备总表', 'SYS-ITEMS-S89', 'system', 'stoneshard, S89, items')
t += '本页是Mod原创物品与装备的细粒度登记：名称（中英）、来源、游戏风格描述与处置规则。描述口径按原作样例校准（见[[原作剧情与对话系统参照]]的「物品与任务描述风格」节）：1–2句、落在地点/用途/行业视角、允许一处冷幽默；不复制原作文本。长文书正文仍在[[文书与现场文本台本]]与各城市篇章文书页；本表只给条目卡与规则。\n\n## 风格规则\n\n'
for r in items['style_rules']:
    t += f'- {r}\n'
probe_path = ROOT / 'research/official-term-probe.json'
probe = json.loads(probe_path.read_text(encoding='utf-8')) if probe_path.exists() else {'entries': []}
probe_by = {r['concept']: r for r in probe.get('entries', [])}
t += '\n## 与原作术语对照\n\n只作词形对照（官方词条来自本地 STRG 中文段索引；「已核」表示中文段与该词条逐字相等并取到官方英文，「含词定位」表示该索引只作含词定位），不代表物件等价；`new` 表示 STRG 中文段无命中的模组原创词。\n\n| 概念 | 官方用词 | 官方英文 | 定位 | 模组用法 | 判定 | 说明 |\n| --- | --- | --- | --- | --- | --- | --- |\n'
for x in items['terminology_alignment']:
    pr = probe_by.get(x['concept'], {})
    if x.get('official_index'):
        loc = f"STRG[{x['official_index']}]" + ('（已核）' if pr.get('verified_index') == x['official_index'] else '（含词定位）')
    else:
        loc = '无命中'
    t += f"| {x['concept']} | {x['official_cn'] or '—'} | {x.get('official_en') or '—'} | {loc} | {x['mod_usage']} | {x['verdict']} | {x['note_cn']} |\n"
def item_table(kind, title, note):
    rows = [x for x in items['items'] if x['kind'] == kind]
    s = f"\n## {title}\n\n{note}\n\n| 名称 | Name | 来源 | 描述 | 处置规则 |\n| --- | --- | --- | --- | --- |\n"
    for x in rows:
        src = '、'.join(x['origin'])
        s += f"| {x['name_cn']}<br>`{x['id']}` | {x['name_en']} | {src} | {x['desc_cn']}<br>{x['desc_en']} | {x['rules_cn']}<br>{x['rules_en']} |\n"
    return s
t += item_table('document', '文书与可读物', '正文另存；条目卡只给名称、来源与一次性/副件规则。')
t += item_table('keepsake', '信物与案情物件', '可留背包的副件须本人准许；原件交出后不留。')
t += item_table('tool', '工具与有限装备', '借用闭环、限一次、不转卖；不超同档原版装备；完整「额外装备」线仍按[[内容清单与优先级]]P3，不在此承诺数值。')
t += '\n## 边界\n\n- 物品不刷新、不复制、不无限供给；同款同物只占一次（含SKO/YOS共用采购人）。\n- 数值与价格仍待实机校准；本页只写设计口径。\n- 英译供未来本地化参考，未宣称与原作译名对齐。\n\n[[文书与现场文本台本]] · [[经济与奖励]] · [[时序与奖励总表]] · [[任务台本总索引]] · [[设计库生成与校验流程]]\n'
put(ITEM_DOC, t, own=True)

# ---------- npc doc ----------
order = ['BRY', 'DEN', 'OSB', 'MNS', 'ALD', 'SKO', 'YOS', 'KOR', 'EED', 'FOR', 'RAT', 'PAS', 'ASH', 'HIG', 'MAE']
names = {c['id']: c['name'] for c in model['cities']}
by_id = {}
for p in sorted(V.rglob('*.md')):
    t = p.read_text(encoding='utf-8-sig')
    m = re.search(r'^id:\s*(\S+)', t, re.M)
    if m and m.group(1) not in by_id: by_id[m.group(1)] = p.relative_to(V).as_posix()
DUAL = {'NPC-N-MARA': 'CHAR-N1', 'NPC-N-IVO': 'CHAR-N1'}
def cell(x):
    rel = by_id.get(DUAL.get(x['id'], '')) or by_id.get('CITY-NPC-' + x['id']) or by_id.get(x['id'])
    name = f"[[{Path(rel).stem}|{x['name']}]]" if rel else x['name']
    return f"{name}<br>`{x['id']}`"
n = front('人物细描与随身物', 'SYS-NPC-DETAIL-S89', 'system', 'stoneshard, S89, character')
n += '本页为Mod原创NPC的细粒度设计（体貌/衣着/随身/举止/风格守卫），供美术、动画与台词参考；人物所求、口吻与弧光仍以各自人物卡与演出审查页为准。写法与原作一致：具体物件、行业痕迹、可演的小动作；不写美貌评语与万能道具。**同名分人**：NPC-N-ENA（灰堤，纳拉之妻）与MAE-S03-NPC艾娜（冷窗驿）不是同一人；莉葵（TRADE-NPC-LIQUI）为SKO/YOS共用同一身体。\n\n'
buckets = {}
for x in npcs['npcs']:
    key = x['id'].split('-')[0]
    buckets.setdefault(key, []).append(x)
known = set(order) | {'TRADE'}
merged = {}
for k, v in buckets.items():
    merged.setdefault(k if k in known else 'NPC', []).extend(v)
buckets = merged
for cid in order:
    rows = buckets.get(cid, [])
    if not rows: continue
    n += f"\n## {names.get(cid, cid)}\n\n| 人物 | 体貌 | 衣着与磨损 | 随身物 | 举止 | 风格守卫 |\n| --- | --- | --- | --- | --- | --- |\n"
    for x in rows:
        n += f"| {cell(x)} | {x['look_cn']} | {x['wear_cn']} | {x['carry_cn']} | {x['manner_cn']} | {x['avoid_cn']} |\n"
for key, title in [('TRADE', '共用人物（跨城同一身体）'), ('NPC', '剧情线配角（晶石主线）')]:
    rows = buckets.get(key, [])
    if not rows: continue
    n += f"\n## {title}\n\n| 人物 | 体貌 | 衣着与磨损 | 随身物 | 举止 | 风格守卫 |\n| --- | --- | --- | --- | --- | --- |\n"
    for x in rows:
        n += f"| {cell(x)} | {x['look_cn']} | {x['wear_cn']} | {x['carry_cn']} | {x['manner_cn']} | {x['avoid_cn']} |\n"
n += f"\n## 覆盖与后续\n\n- 本批覆盖 {len(npcs['npcs'])} 名Mod原创人物：15城新增演员、各城『已有』演员、布林续篇演员、33名卫星住户与主线原创人物。\n- 每名人物在各自人物卡内附『形象细描（S89登记）』块（S91回灌，块标记FINE-DETAILS-CARD-S91）；本表是汇总口径，人物名链到各自卡片。\n- 原作人物（维伦、葛文涅尔、雷奥、莫伦、工匠Darrel等）不在此表：其形象以游戏内为准，本库只续写其剧情；重画需另立美术任务。\n- 年龄、体态与衣着均为设计口径；不替代美术终稿与角色存档。\n\n[[人物弧光与关系转折]] · [[台本新增人物与知识边界]] · [[城市与聚落设计总索引]] · [[设计库生成与校验流程]]\n"
put(NPC_DOC, n, own=True)

# ---------- index blocks ----------
summary = '## S89细粒度设计（当前登记）\n\n[[原创物品与装备总表]]（63条：文书26/信物30/工具7，中英描述＋处置规则）与[[人物细描与随身物]]（172名Mod原创NPC的体貌/衣着/随身/举止/风格守卫）。描述按原作样例校准（来源地/用途/行业视角，1-2句）；S91已把逐人细描回灌到各自人物卡；数值与美术终稿未定。'
for name in ['文书与现场文本台本', '人物弧光与关系转折', '经济与奖励', '任务台本总索引']:
    p = next(V.rglob(name + '.md'))
    rel = p.relative_to(V).as_posix()
    body = p.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; blk = a + '\n' + summary + '\n' + z
    p.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + blk + '\n', encoding='utf-8')
    changed.add('design/' + rel)

for p2, h in manifests.items():
    touched = False
    for rel in changed & set(h):
        h[rel] = sha(ROOT / rel); touched = True
    if touched:
        p2.write_text(json.dumps(h, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
HP.write_text(json.dumps(generated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

rule = '2026-10-12 S89：用户要求细粒度设计（NPC/物品/装备描述，贴合原作与新作风格）。research/item-registry.json（63条：文书26/信物30/工具7，名称中英＋风格描述＋处置规则＋14条原作术语对照）与research/npc-fine-details.json（172名Mod原创NPC：各城新增与『已有』演员、续篇演员、卫星住户与主线原创人物；体貌/衣着/随身/举止/风格守卫；含同名分人与共用身体说明；原作人物只续写剧情、不重画形象）。入口design/05_主线/原创物品与装备总表.md与design/04_人物/人物细描与随身物.md；描述按原作样例校准（1-2句、来源地/用途/行业视角），不复制原作文本。运行Validate-FineDetails.py及既有检查；数值、美术与游戏未验收，不部署。'
for p3 in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md', ROOT / 'CHANGELOG.md']:
    body = p3.read_text(encoding='utf-8-sig')
    a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'; blk = a + '\n' + rule + '\n' + z
    p3.write_text(re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: blk, body, flags=re.S) if a in body else body.rstrip() + '\n\n' + blk + '\n')
print(json.dumps({'items': len(items['items']), 'npcs': len(npcs['npcs']), 'generated': len(generated), 'changed': len(changed)}, ensure_ascii=False))
