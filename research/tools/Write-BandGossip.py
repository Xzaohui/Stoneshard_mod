"""S117: author street-level reputation-band reactions (15 towns + 6 regions).

Two lines per place: cold (`band:-1`) and warm (`band:+2`), tone only. They do
not promise services, items or knowledge; counter lines stay with the town
reputation registry.
"""
from pathlib import Path
import pathlib
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'BAND-GOSSIP-S117'
CARD = '02_世界与地图/特殊地点与野外NPC/声望档街头反应.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
model = read('research/city-campaign.json'); rep = read('research/town-reputation.json')
CITIES = {c['id']: c for c in model['cities']}
REGNAME = {'R01': '布林外港与旧渠', 'R02': '丹布里西路与渡口', 'R03': '曼恩边地', 'R04': '王廷关隘与边城', 'R05': '灰烬湿地与疫村', 'R06': '无名修院山地'}
LINES = [
 ('BRY', 'band:-1', '摊主', '布林人不记仇，只记账。你那笔，最近没人替你划。', "Brynn folk keep no grudges, only ledgers. Lately nobody strikes your entry."),
 ('BRY', 'band:+2', '摊主', '你走这条街，摊主会先点头。点头不算折扣，算熟。', "Walk this street and the stalls nod first. A nod is not a discount - it is being known."),
 ('DEN', 'band:-1', '渡工', '渡口的风认得人。你现在站上风处，没人跟你换位。', "The ford wind knows faces. You stand upwind now and nobody trades places with you."),
 ('DEN', 'band:+2', '渡工', '船家会给你留靠里的位置。里面不湿鞋。', "The boatmen save you the inner seat. Inner seats stay dry."),
 ('OSB', 'band:-1', '乡民', '村里借东西讲个来回。你的来回还没走完。', "Borrowing in this village goes both ways. Your way back is not walked yet."),
 ('OSB', 'band:+2', '乡民', '你来借筛子，会有人先应一声。', "Come for the sieve and someone answers before you finish asking."),
 ('MNS', 'band:-1', '店主', '酒馆的杯子都干净，给你那只例外。', "The tavern cups are all clean. Yours is the exception."),
 ('MNS', 'band:+2', '店主', '你进门不用报名字，柜台知道给你倒哪一壶。', "You do not give your name here; the counter knows which jug is yours."),
 ('ALD', 'band:-1', '匠人', '铺子肯收你的活，但不肯让你碰料。', "The shop takes your work but will not let you touch the stock."),
 ('ALD', 'band:+2', '匠人', '匠人会让你看衬里的针脚。看针脚是给熟人的。', "The smith lets you see the lining stitches. Stitches are shown to familiars."),
 ('SKO', 'band:-1', '炉工', '炉边热，你站的地方不热。', "The furnace side is warm. The spot you stand in is not."),
 ('SKO', 'band:+2', '炉工', '炉工会替你留一铲煤。留煤是给常来的人。', "The furnace men keep a shovel of coal for you. Kept coal is for regulars."),
 ('YOS', 'band:-1', '织工', '织机的声音会停一下，你走过去再响。', "The loom pauses while you pass, then starts again."),
 ('YOS', 'band:+2', '织工', '牧人会让你摸摸新剪的毛。摸毛是给熟客的。', "The shepherds let you feel the new fleece. Fleece is for familiar hands."),
 ('KOR', 'band:-1', '寄存人', '寄存的条子会多写一行日期。写细的，是防你的。', "Your storage slip gains an extra date line. Fine writing is written against you."),
 ('KOR', 'band:+2', '寄存人', '库房会先给你开门，再问你办什么。', "The storeroom opens for you first and asks what for second."),
 ('EED', 'band:-1', '护林人', '护林人跟你说话会看着斧子。', "The forester talks to you with one eye on your axe."),
 ('EED', 'band:+2', '护林人', '护林人会指给你一条新踩出来的路。', "The forester points you down a freshly walked path."),
 ('FOR', 'band:-1', '矿工', '井口的灯不会为你多点一盏。', "No extra lamp is lit at the shaft mouth for you."),
 ('FOR', 'band:+2', '矿工', '矿工会先指给你水桶在哪，再问你要下到哪层。', "The miners point out the water pail first, then ask which level you are going down to."),
 ('RAT', 'band:-1', '农人', '量地的人把绳子收得快。', "The surveyor winds the rope up fast."),
 ('RAT', 'band:+2', '农人', '量地的人会告诉你去年的界在哪。', "The surveyor tells you where last year's line ran."),
 ('PAS', 'band:-1', '关兵', '关兵翻你的文书会多翻两页。', "The gate men leaf two pages further through your papers."),
 ('PAS', 'band:+2', '关兵', '关兵会先放你过，再补一句路上小心。', "The gate men wave you through first, then add: mind the road."),
 ('ASH', 'band:-1', '护理者', '护理者会先问你来过几次。', "The carers ask how many times you have come before."),
 ('ASH', 'band:+2', '护理者', '门口的名册会先翻到有你名字的那页。', "The list at the door opens first to the page with your name."),
 ('HIG', 'band:-1', '挑夫', '药棚的水壶会收进去，等你走远再放出来。', "The shed puts its water jug away until you are well past."),
 ('HIG', 'band:+2', '挑夫', '山道上的人会先招呼你歇一歇。', "People on the trail greet you and tell you to rest a while."),
 ('MAE', 'band:-1', '学者', '学院的听差会先看你的鞋。', "The college porter looks at your shoes first."),
 ('MAE', 'band:+2', '学者', '学者会停下讲半句，等你想清楚再问。', "A scholar stops mid-sentence and waits for you to think before asking."),
 ('R01', 'band:-1', '渠口工人', '渠口的人会停下说话，等你走开再继续。', "The culvert men stop talking and pick it up once you are gone."),
 ('R01', 'band:+2', '渠口工人', '渠口的灯会为你多留一刻。', "The culvert lamp is kept burning a while longer for you."),
 ('R02', 'band:-1', '摆渡人', '摆渡的会先问你去对岸做什么。', "The ferryman asks what you want on the far bank before he poles off."),
 ('R02', 'band:+2', '摆渡人', '摆渡的会把船往你这边靠半尺。', "The ferryman brings the boat half a foot closer to your side."),
 ('R03', 'band:-1', '农人', '草场上的陷，没人会告诉你新摆在哪。', "Nobody tells you where the new snares went in the meadow."),
 ('R03', 'band:+2', '农人', '设陷的人会喊一声，让你别踩那条线。', "The trapper calls out so you do not step on that line."),
 ('R04', 'band:-1', '石工', '关道上的石工会停下手里的活看你走过去。', "The quarrymen on the pass stop working to watch you walk by."),
 ('R04', 'band:+2', '石工', '石工会让开半边道，让你先过。', "The quarrymen step aside and let you pass first."),
 ('R05', 'band:-1', '乡民', '湿地边的人会绕开你走。', "Folk on the wetland edge walk around you."),
 ('R05', 'band:+2', '乡民', '湿地边的人会替你指那条横着走的路。', "Folk on the wetland edge point out the way to cross sideways."),
 ('R06', 'band:-1', '药农', '山道上的人会先问你从哪来，再决定说不说话。', "On the trail they ask where you came from before deciding to talk."),
 ('R06', 'band:+2', '药农', '山道上的人会分你半壶热水。', "On the trail someone shares half a flask of hot water with you."),
]
assert len(LINES) == 42, len(LINES)
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
counter_lines = {b['line_cn'] for t in rep['towns'] for b in t['bands']} | {b['line_en'] for t in rep['towns'] for b in t['bands']}
rows = []
seen_cn, seen_en = {}, {}
for cid, when, spk, cn, en in LINES:
    rid = f'BG-{cid}-{"low" if when.endswith("-1") else "high"}'
    assert CJK.search(cn) and not re.search(r'[A-Za-z]', cn), rid + ' cn'
    assert not CJK.search(en) and len(en) <= 150, rid + ' en'
    assert not BACK.search(cn + ' ' + en), rid + ' backstage'
    assert cn not in seen_cn and en not in seen_en, rid + ' dup'
    assert cn not in counter_lines and en not in counter_lines, rid + ' counter-clone'
    seen_cn[cn] = rid; seen_en[en] = rid
    if cid in CITIES:
        link = pathlib.Path(CITIES[cid]['file']).stem
    else:
        link = {'R01': '区域_R01_布林外港与旧渠', 'R02': '区域_R02_丹布里西路与渡口', 'R03': '区域_R03_曼恩边地',
                'R04': '区域_R04_王廷关隘与边城', 'R05': '区域_R05_灰烬湿地与疫村', 'R06': '区域_R06_无名修院山地'}[cid]
    assert link in {p.stem for p in V.rglob('*.md')}, rid + ' link'
    rows.append(dict(id=rid, place=cid, speaker=spk, when=when, cn=cn, en=en, link=link))
out = dict(date='2026-10-13', scope='S117 street-level reputation-band reactions: cold/warm tone lines per town and region, CN/EN parity; tone only, no service promises, no items, no knowledge',
           vocabulary=['band:-1', 'band:+2'],
           rules=['只写口气与场面：不承诺服务、不发物品、不给情报',
                  '服务台口径仍归[[城镇声望与信任系统]]；本池不得与柜台台词重复',
                  'band:-1 代表 ≤−1 的冷档，band:+2 代表 ≥+2 的热档；中间档不播本池',
                  '不含奖励、不推进任务、不写状态键'],
           lines=rows)
(ROOT / 'research' / 'band-gossip.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "声望档街头反应"\nid: FX-BAND-GOSSIP\ntype: script\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S117, dialogue, reputation]\naliases: []\n---\n\n'
     '# 声望档街头反应\n\n'
     f"十五城镇与六地域各 2 条街头口气（冷档 `band:-1`、热档 `band:+2`），共 {len(rows)} 条（中英对照）。只写口气与场面：不承诺服务、不发物品、不给情报；服务台口径仍归[[城镇声望与信任系统]]，本池不得与柜台台词重复。\n\n"
     '| 地点 | 档位 | 说话人 | 中文 | English | 关联 |\n|---|---|---|---|---|---|\n')
for x in rows:
    place = CITIES[x['place']]['name'] if x['place'] in CITIES else REGNAME[x['place']]
    n += f"| {place} | `{x['when']}` | {x['speaker']} | 「{x['cn']}」 | {x['en']} | [[{x['link']}]] |\n"
n += ('\n## 边界\n\n- 冷档只写疏远与提防，不写敌意行为；热档只写熟络与让路，不写折扣与赠予。\n'
      '- 中间档（−1..+2 之间）不播本池；档位变化只改未来口气，不回滚旧事。\n'
      '- 未做：触发距离、作息与配音；与柜台台词的合并播放规则待实现阶段确定。\n\n'
      '[[城镇声望与信任系统]] · [[城镇闲谈池]] · [[地区闲谈池]] · [[野外NPC口吻与闲谈参照]] · [[特殊地点与野外NPC对白扩展计划]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S117声望档街头反应（当前登记）\n\n'
           f"[[声望档街头反应]]：十五城镇与六地域各 2 条冷/热档街头口气（中英对照，共 {len(rows)} 条）；只写口气与场面，不承诺服务、不发物品、不给情报，且与柜台台词不重复。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/band-gossip-note-hashes.json'
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
rule = ('\n<!-- BAND-GOSSIP-S117:BEGIN -->\n2026-10-13 S117：声望档街头反应（原创，中英对照）。'
        f'research/band-gossip.json 十五城镇与六地域各2条冷/热档口气（band:-1 / band:+2）共 {len(rows)} 条；只写口气与场面，不承诺服务、不发物品、不给情报，且与柜台台词不重复。'
        '入口design/02_世界与地图/特殊地点与野外NPC/声望档街头反应.md；运行Validate-BandGossip.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。\n<!-- BAND-GOSSIP-S117:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- BAND-GOSSIP-S117:BEGIN -->.*?<!-- BAND-GOSSIP-S117:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- BAND-GOSSIP-S117:BEGIN -->.*?<!-- BAND-GOSSIP-S117:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/声望档街头反应.md', '入口 [声望档街头反应](design/02_世界与地图/特殊地点与野外NPC/声望档街头反应.md)'), encoding='utf-8')
print(json.dumps(dict(lines=len(rows), notes=len(generated)), ensure_ascii=False))
