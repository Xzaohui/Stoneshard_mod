"""S125: content inventory — one page listing every user-facing narrative asset.

Counts are computed live from the registries: city/story scripts, field people,
documents, signs, gossip pools, band reactions, interior/daily ambient, plus the
bridge artifacts. Read-only projection; no content changes.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'CONTENT-INVENTORY-S125'
CARD = '00_导航/叙事内容清单.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
model = read('research/city-campaign.json'); cont = read('research/brynn-continuation.json')
fx = read('research/field-npc-dialogue.json'); fd = read('research/field-docs.json'); sg = read('research/field-signs.json')
ag = read('research/ambient-gossip.json'); tg = read('research/town-gossip.json'); bg = read('research/band-gossip.json')
ia = read('research/interior-ambient.json'); rep = read('research/town-reputation.json')
svc = read('research/service-registry.json'); items = read('research/item-registry.json')
cf = read('research/corpus-flows.json'); sk = read('research/state-keys.json'); es = read('research/event-stubs.json')
story = {n: read(f'research/{n}') for n in ['story-main.json', 'story-side.json', 'story-main-late.json', 'story-daily.json', 'story-dungeon.json']}
def count_lines(flow_list):
    return sum(len(f['nodes']) for f in flow_list)
ROWS = [
 dict(kind='城市支线台本', count=len(model['quests']), unit='篇', entry='[[城市与聚落设计总索引]]', note='十五城；含逐路线方法、早晚回执与例外'),
 dict(kind='布林续篇台本', count=len(cont['quests']), unit='篇', entry='[[布林续篇任务与伏笔回收总表]]', note='六案；桥组回执与缺席替代'),
 dict(kind='主线/支线/后章/副本台本', count=sum(len(v) for k, v in story.items() if k != 'story-daily.json'), unit='篇', entry='[[任务台本总索引]]', note='N1—N18、SQ、后章与 D02—D10'),
 dict(kind='日常台本', count=len(story['story-daily.json']), unit='篇', entry='[[任务台本总索引]]', note='DT01—DT16；一次地方人物事件'),
 dict(kind='野外人物（含条件回访）', count=len(fx['npcs']), unit='人', entry='[[台本_FX_野外人物对白]]', note='每人 14 槽中英对照；存在性四态'),
 dict(kind='野外文书', count=len(fd['docs']), unit='份', entry='[[文书_FX_野外地点短稿]]', note='原件/副件/残件分记；只给信息'),
 dict(kind='野外迹象', count=len(sg['signs']), unit='处', entry='[[野外迹象与观察]]', note='观察/判定/退路；不含数值'),
 dict(kind='地区闲谈', count=len(ag['lines']), unit='条', entry='[[地区闲谈池]]', note='六地域；any/night/band/after'),
 dict(kind='城镇闲谈', count=len(tg['lines']), unit='条', entry='[[城镇闲谈池]]', note='十五城镇各 4 条'),
 dict(kind='声望档街头反应', count=len(bg['lines']), unit='条', entry='[[声望档街头反应]]', note='冷/热档口气；与柜台台词不重复'),
 dict(kind='副本与日常氛围句', count=len(ia['lines']), unit='条', entry='[[副本与日常氛围句]]', note='9 副本×3＋16 日常×2'),
 dict(kind='声望档柜台台词', count=sum(len(t['bands']) for t in rep['towns']), unit='条', entry='[[城镇声望与信任系统]]', note='五档×十五城，中英对照'),
 dict(kind='城市服务班', count=len(svc['services']), unit='班', entry='[[城市服务班与有限库存]]', note='档位便利与刷新规则'),
 dict(kind='原创物品', count=len(items['items']), unit='条', entry='[[原创物品与装备总表]]', note='文书/信物/工具；术语对照已核'),
 dict(kind='条件流节点（桥接）', count=count_lines(cf['flows']), unit='节点', entry='[[全库条件流投影]]', note='实现用；refs 回指原句'),
 dict(kind='状态键（桥接）', count=len(sk['keys']), unit='键', entry='[[状态键映射总表]]', note='含 329 条跨任务回执'),
 dict(kind='事件桩（桥接）', count=len(es['stubs']), unit='桩', entry='[[事件桩映射总表]]', note='不声明引擎事件号'),
]
user_lines = (sum(len(x['greetings']) + len(x['chats']) + len(x['site_lines']) + sum(len(x['visits'][k]) for k in ('before', 'after', 'early', 'late', 'proxy')) for x in fx['npcs'])
              + len(fd['docs']) * 3 + len(sg['signs']) * 4 + len(ag['lines']) + len(tg['lines']) + len(bg['lines']) + len(ia['lines'])
              + sum(len(t['bands']) for t in rep['towns']))
out = dict(date='2026-10-13', scope='S125 content inventory: live counts of narrative assets and bridge artifacts with entry links; read-only projection',
           rows=ROWS, user_facing_units=user_lines)
(ROOT / 'research' / 'content-inventory.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "叙事内容清单"\nid: NAV-CONTENT-S125\ntype: index\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S125, index]\naliases: []\n---\n\n'
     '# 叙事内容清单\n\n'
     f"一页看全当前叙事资产（计数取自各登记文件，实时）。用户可见文本合计约 **{user_lines}** 个单元（对白行、文书字段、迹象字段、闲谈与柜台台词）；桥接层不计入。\n\n"
     '| 内容 | 数量 | 入口 | 说明 |\n|---|---:|---|---|\n')
for r in ROWS:
    n += f"| {r['kind']} | {r['count']} {r['unit']} | {r['entry']} | {r['note']} |\n"
n += ('\n## 阅读顺序建议\n\n- 先看 [[城市与聚落设计总索引]] 与 [[任务台本总索引]] 了解任务面；再看 [[特殊地点与野外NPC阶段验收记录]] 了解野外与闲谈面。\n'
      '- 实现前看 [[实现交接总表]]；键名口径见 [[键名口径对账]]；中英对照覆盖见 [[中英对照覆盖报告]]。\n'
      '- 校验与生成链见 [[设计库生成与校验流程]]；每阶段证据见 [[逻辑验收记录]]。\n\n'
      '## 边界\n\n- 本页只做索引与计数：不新增内容、不改变任何登记；计数随源变化，重跑本工具即可刷新。\n'
      '- 计数不等于文学质量或运行验证；未做项见 [[实现交接总表]] 的“尚未确定”。\n\n'
      '[[设计总览]] · [[特殊地点与野外NPC阶段验收记录]] · [[中英对照覆盖报告]] · [[实现交接总表]] · [[设计库生成与校验流程]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S125叙事内容清单（当前登记）\n\n'
           f"[[叙事内容清单]]：一页列全叙事资产（城市/续篇/主线/日常/副本台本、28 野外人物、文书与迹象、四套闲谈池、柜台台词、服务班与物品，以及条件流/状态键/事件桩桥接层），用户可见文本约 {user_lines} 个单元。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/content-inventory-note-hashes.json'
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
rule = ('\n<!-- CONTENT-INVENTORY-S125:BEGIN -->\n2026-10-13 S125：叙事内容清单。'
        f'research/content-inventory.json 一页列全叙事资产与桥接层（用户可见文本约 {user_lines} 个单元）；入口design/00_导航/叙事内容清单.md；计数取自源、重跑刷新。'
        '只做索引与计数；运行Validate-ContentInventory.py及既有检查；不部署游戏包。\n<!-- CONTENT-INVENTORY-S125:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- CONTENT-INVENTORY-S125:BEGIN -->.*?<!-- CONTENT-INVENTORY-S125:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- CONTENT-INVENTORY-S125:BEGIN -->.*?<!-- CONTENT-INVENTORY-S125:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/00_导航/叙事内容清单.md', '入口 [叙事内容清单](design/00_导航/叙事内容清单.md)'), encoding='utf-8')
print(json.dumps(dict(rows=len(ROWS), user_units=user_lines, notes=len(generated)), ensure_ascii=False))
