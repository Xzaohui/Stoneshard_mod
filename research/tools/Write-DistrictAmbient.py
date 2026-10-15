"""S129: district-level ambient lines for all 66 city districts (CN/EN).

One line per district node, spoken by a plausible local voice and tied to the
district's function; linked to the city page. No rewards, no task progress.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'DISTRICT-AMBIENT-S129'
CARD = '02_世界与地图/特殊地点与野外NPC/街区氛围句.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
model = read('research/city-campaign.json')
CITIES = {c['id']: c for c in model['cities']}
LINES = {
 'BRY-D01': ('市民', '告示一贴三份，缺街那份总是最后补。', "Notices go up in three copies; the one missing a street gets patched last."),
 'BRY-D02': ('租客', '门框上的年刻比租牌准。租牌能补，年刻补不了。', "The year cuts on the doorframe outlast the rent plates. Plates get replaced; cuts do not."),
 'BRY-D03': ('船工', '这条街认吃水，不认旗子。', "This street reads draft lines, not banners."),
 'BRY-D04': ('学徒', '副工场的活按件算。件数清，人就不清。', "Side-workshop work is counted by the piece. The count is clear; the people are not."),
 'BRY-D05': ('守卫', '水门开合看潮，不看人。', "The water gate opens by the tide, not by faces."),
 'BRY-D06': ('掌灯人', '夜里谈事的都坐墙边。墙边听得清，也退得快。', "Night talkers sit by the wall. By the wall you hear well and leave fast."),
 'DEN-D01': ('乡民', '岸上的屋修了三回。第三回换了地基。', "The shore house was rebuilt three times. The third time we changed the foundation."),
 'DEN-D02': ('旅人', '驻点外街白天忙，夜里空。', "The outer street is busy by day and empty by night."),
 'DEN-D03': ('织网人', '补网先补洞眼大的，小的自己会拉大。', "Mend the big holes first; small ones widen on their own."),
 'DEN-D04': ('渡工', '摆渡看水位桩，不看天色。', "The ferryman reads the gauge post, not the sky."),
 'OSB-D01': ('农人', '后场晒粮，前场议事。两场不混。', "The back yard dries grain; the front yard argues. They do not mix."),
 'OSB-D02': ('乡民', '磨停了，侧院还堆着磨石。', "The mill stopped; the side yard still holds the stones."),
 'OSB-D03': ('看仓人', '粮棚记进出，不记名字。', "The grain shed logs what comes and goes, not who."),
 'OSB-D04': ('旅人', '溪桥过一辆车就够窄了。', "The creek bridge is narrow enough for one cart."),
 'MNS-D01': ('酒工', '坡上的葡萄归谁，看藤架不看地契。', "Who owns the slope grapes follows the trellis, not the deed."),
 'MNS-D02': ('窖工', '共用的窖，位子比酒贵。', "In a shared cellar the slot costs more than the wine."),
 'MNS-D03': ('工头', '后街的活计不挂牌，靠喊。', "Back-street work is not posted; it is shouted."),
 'MNS-D04': ('店主', '小院只卖当批的酒。批号写在桶沿。', "The yard sells only the current batch; the batch number is on the cask rim."),
 'ALD-D01': ('匠人', '外街的炉子只烧小件。大件进院。', "Outer-street forges fire small pieces; big work goes inside."),
 'ALD-D02': ('修甲人', '护具修院不接急活。急了，就修不好。', "The armour yard takes no rush jobs. Rushed, it will not mend right."),
 'ALD-D03': ('门房', '外庭先看来意，再看衣冠。', "The outer court asks your business first, your dress second."),
 'ALD-D04': ('石工', '旧墙拆一半就停。剩下的那半是界线。', "The old wall was half pulled down. The rest is the boundary."),
 'ALD-D05': ('学徒', '试装小场量三处：肩、肘、膝。', "The fitting yard measures three points: shoulder, elbow, knee."),
 'ALD-D06': ('会首', '会馆只认登记的手艺，不认口头师承。', "The hall honours registered crafts, not spoken lineage."),
 'SKO-D01': ('炉工', '工棚记炉次，不记人情。', "The shed logs furnace runs, not favours."),
 'SKO-D02': ('柜员', '寄柜只收现，不收欠条。', "The deposit cabinet takes coin, not notes."),
 'SKO-D03': ('工人', '支沟的水烫过手，别试。', "The cooling channel has scalded hands. Do not test it."),
 'SKO-D04': ('料商', '料市按批卖。批完了就收摊。', "The material market sells by batch. Batch done, stall closed."),
 'YOS-D01': ('织工', '晒架上的毛按天翻。翻晚了会霉。', "Fleece on the racks is turned daily. Turn it late and it moulds."),
 'YOS-D02': ('学徒', '侧棚的机子慢，慢的织得匀。', "The side shed loom runs slow; slow weaves even."),
 'YOS-D03': ('工人', '水堰洗毛，洗三次才算净。', "The weir washes fleece; three rinses to be clean."),
 'YOS-D04': ('商贩', '布市限匹数，谁也不能多拿。', "The cloth market limits bolts; nobody takes extra."),
 'KOR-D01': ('寄存人', '新院先立条，再收货。', "The new yard sets its slips before taking goods."),
 'KOR-D02': ('乡民', '住棚街的名字还是拟定的。', "The shelter street is still only provisionally named."),
 'KOR-D03': ('见证人', '见证亭只记谁在场，不记谁有理。', "The witness pavilion records who was present, not who was right."),
 'KOR-D04': ('看守', '侧门道没名字，走的人不少。', "The side gate path has no name, and no shortage of walkers."),
 'EED-D01': ('伐木工', '边院堆的是等锯的料。', "The side yard stacks timber waiting for the saw."),
 'EED-D02': ('护林人', '岗外三步是林线，越线要问。', "Three steps past the post is the tree line; crossing needs asking."),
 'EED-D03': ('放排人', '木排靠岸要看水，不看力气。', "Rafts beach by water, not by strength."),
 'EED-D04': ('弓匠', '弓料要阴干，棚里不见太阳。', "Bow staves dry in the shade; no sun in this shed."),
 'FOR-D01': ('矿工', '支井口封过两次，两次都开了。', "The side shaft was sealed twice, and opened twice."),
 'FOR-D02': ('称工', '粗矿过秤先扣石。', "Coarse ore is weighed with the rock deducted first."),
 'FOR-D03': ('工头', '通风院的人先下，最后上。', "Ventilation crews go down first and come up last."),
 'FOR-D04': ('柜员', '存柜只收旧物，不收新货。', "The cabinet stores old goods only, never new stock."),
 'RAT-D01': ('乡民', '外坡种的是纪念树，不结果。', "The slope grows memorial trees; they bear no fruit."),
 'RAT-D02': ('农人', '家院里的人都活着，地还没分完。', "The household survived; the land is not divided yet."),
 'RAT-D03': ('牧人', '围栏道只修一半，另一半靠喊。', "Half the fence path is mended; the other half relies on shouting."),
 'RAT-D04': ('匠人', '小亭只修旧物，不做新件。', "The kiosk mends old things, never makes new ones."),
 'PAS-D01': ('驿丞', '驿馆登记来处，不问去处。', "The post house logs where you came from, not where you go."),
 'PAS-D02': ('秤工', '外场复量一遍，少的自己补。', "The yard re-measures; shortfalls are made up by the carrier."),
 'PAS-D03': ('石工', '旁路是运石踩出来的。', "The side path was worn by hauling stone."),
 'PAS-D04': ('军需官', '交换场只换物，不换人情。', "The exchange trades goods, not favours."),
 'ASH-D01': ('护理者', '营里分区，先分区再分人。', "The camp is zoned first, staffed second."),
 'ASH-D02': ('挑水人', '水堤上不许洗东西。', "Nothing is washed on the water bank."),
 'ASH-D03': ('维护者', '井口的风比井里冷。', "The wind at the well mouth is colder than below."),
 'ASH-D04': ('接收人', '接收棚先问自愿，再问名字。', "The shelter asks willingness first, names second."),
 'HIG-D01': ('维护者', '钟站不敲钟了，螺栓还在换。', "The station rings no bells; the bolts still get replaced."),
 'HIG-D02': ('工人', '维护廊只走外圈，不进内院。', "The maintenance walk circles outside; it never enters the inner court."),
 'HIG-D03': ('学者', '议桌不设主位。', "The table has no head seat."),
 'HIG-D04': ('看守', '封条路按季度查，不看人情。', "The sealed road is checked quarterly, not by favour."),
 'MAE-D01': ('市民', '民粮巷的价一天一变。', "Prices in the grain lane change daily."),
 'MAE-D02': ('学徒', '迁藏屋的书箱编了号，号对不上就停。', "The moving-store crates are numbered; a mismatch stops the work."),
 'MAE-D03': ('学生', '残庭只留石座，不种花。', "The broken court keeps stone seats, not flowers."),
 'MAE-D04': ('织工', '旧织街的机子还在响，只是没人听了。', "The old weaving street still clatters; fewer listen."),
 'MAE-D05': ('看守', '封火小院只留一盏火。', "The banked-fire yard keeps a single flame."),
 'MAE-D06': ('接应人', '接应棚不问旧名，只问去向。', "The receiving shed asks not your old name, only where you go."),
}
districts = {n['id']: (c, n) for c in model['cities'] for n in c['nodes'] if n['kind'] == 'district'}
assert set(LINES) == set(districts), (set(districts) - set(LINES), set(LINES) - set(districts))
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
prior_cn, prior_en = set(), set()
for f in ['ambient-gossip', 'town-gossip', 'band-gossip', 'interior-ambient']:
    d = read(f'research/{f}.json')
    for x in d['lines']:
        prior_cn.add(x['cn']); prior_en.add(x['en'])
fx = read('research/field-npc-dialogue.json')
for n in fx['npcs']:
    for _, t in n['greetings'] + n['site_lines'] + [(None, c) for c in n['chats']]:
        prior_cn.add(t)
    for kk in ('before', 'after', 'early', 'late', 'proxy'):
        for v in n['visits'][kk]: prior_cn.add(v)
    for v in (n.get('english') or {}).values(): prior_en.add(v)
rows = []
seen_cn, seen_en = {}, {}
for did, (voice, cn, en) in LINES.items():
    c, n = districts[did]
    assert CJK.search(cn) and not re.search(r'[A-Za-z]', cn), did
    assert not CJK.search(en) and len(en) <= 150, did
    assert not BACK.search(cn + ' ' + en), did
    assert cn not in seen_cn and en not in seen_en, did
    assert cn not in prior_cn and en not in prior_en, did + ' clone'
    seen_cn[cn] = did; seen_en[en] = did
    rows.append(dict(id=did, city=c['id'], district=n['name'], voice=voice, cn=cn, en=en,
                     link=Path(c['file']).stem))
out = dict(date='2026-10-13', scope='S129 district ambient: one line per city district (66), CN/EN parity, tied to district function; no rewards, no task progress, no knowledge leaks',
           rules=['按街区写：只谈本街的功能、规矩与街面，不替台本当事人发言',
                  '不含奖励、不推进任务、不写状态键；与四套闲谈池不重复',
                  '每街区一句，链接本城卡；不改任何结算'],
           lines=rows)
(ROOT / 'research' / 'district-ambient.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n2 = ('---\ntitle: "街区氛围句"\nid: FX-DISTRICT-AMBIENT\ntype: script\nstatus: draft\ncanon: mod-original\n'
      'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S129, dialogue, ambient]\naliases: []\n---\n\n'
      '# 街区氛围句\n\n'
      f"十五城 {len(rows)} 个街区各 1 条氛围句（中英对照），按各街区功能与规矩写；只谈本街街面，不替台本当事人发言，不发奖励、不推进任务、不写状态键。\n\n"
      '| 城 | 街区 | 说话人 | 中文 | English | 关联 |\n|---|---|---|---|---|---|\n')
for x in rows:
    n2 += f"| {CITIES[x['city']]['name']} | {x['district']}（`{x['id']}`） | {x['voice']} | 「{x['cn']}」 | {x['en']} | [[{x['link']}]] |\n"
n2 += ('\n## 边界\n\n- 全部为Mod原创；每街区一句，不构成任何必访清单。\n'
       '- 与 [[地区闲谈池]]、[[城镇闲谈池]]、[[声望档街头反应]]、[[副本与日常氛围句]] 互不重复。\n'
       '- 未做：触发距离、作息与配音（见[[特殊地点阶段制作与校准规程]]）。\n\n'
       '[[城市与聚落设计总索引]] · [[任务空间与地点关联审查]] · [[城镇闲谈池]] · [[特殊地点与野外NPC阶段验收记录]] · [[特殊地点与野外NPC对白扩展计划]]\n')
put(CARD, n2)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S129街区氛围句（当前登记）\n\n'
           f"[[街区氛围句]]：十五城 {len(rows)} 个街区各 1 条中英对照氛围句，按街区功能写；与四套闲谈池不重复，不发奖励、不推进任务。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/district-ambient-note-hashes.json'
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
rule = ('\n<!-- DISTRICT-AMBIENT-S129:BEGIN -->\n2026-10-13 S129：街区氛围句（原创，中英对照）。'
        f'research/district-ambient.json 十五城 {len(rows)} 街区各1条，按街区功能写；与四套闲谈池不重复、不发奖励、不推进任务、不写状态键。'
        '入口design/02_世界与地图/特殊地点与野外NPC/街区氛围句.md；运行Validate-DistrictAmbient.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。\n<!-- DISTRICT-AMBIENT-S129:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- DISTRICT-AMBIENT-S129:BEGIN -->.*?<!-- DISTRICT-AMBIENT-S129:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- DISTRICT-AMBIENT-S129:BEGIN -->.*?<!-- DISTRICT-AMBIENT-S129:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/街区氛围句.md', '入口 [街区氛围句](design/02_世界与地图/特殊地点与野外NPC/街区氛围句.md)'), encoding='utf-8')
print(json.dumps(dict(lines=len(rows), districts=len(districts), notes=len(generated)), ensure_ascii=False))
