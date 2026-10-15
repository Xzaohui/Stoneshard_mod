"""S116: author the Mod-original town ambient gossip pool (15 towns, CN/EN).

Four lines per town (any/any/night/after:<CM chapter>), tied to city notes and
their main chapters. No rewards, no task progress, no knowledge leaks.
"""
from pathlib import Path
import pathlib
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'TOWN-GOSSIP-S116'
CARD = '02_世界与地图/特殊地点与野外NPC/城镇闲谈池.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
model = read('research/city-campaign.json')
CITIES = {c['id']: c for c in model['cities']}
CM = {c['id']: pathlib.Path(next(q for q in model['quests'] if q['id'] == c['main_id'])['file']).stem for c in model['cities']}
LINES = [
 ('BRY', '市民', 'any', '新会定了工价以后，手艺好的和手艺差的拿一样的钱。有人欢喜有人骂。', "Since the Guild set the rates, good hands and clumsy hands earn the same. Some cheer, some curse."),
 ('BRY', '商贩', 'any', '布林的买卖看码头，码头看风向。风向一变，价就跟着变。', "Brynn's trade watches the docks, and the docks watch the wind. Wind shifts, prices follow."),
 ('BRY', '卫兵', 'night', '夜里巡的是老楼那几条巷子。灯亮着的地方反而少去。', "Night patrols stick to the old-tower lanes. The well-lit spots we visit least."),
 ('BRY', '工头', 'after', '城墙之内的事办完以后，工班换了两次人。换人不换活。', "After the matter inside the walls, the crew changed twice. The work did not."),
 ('DEN', '渡工', 'any', '潮水退去以后，滩上的东西比水里多。捡的人也多。', "When the tide pulls back, the beach holds more than the water did. More pickers too."),
 ('DEN', '农人', 'any', '村里的屋修了三回，塌了两回。第三回我们换了地基。', "The village house was rebuilt three times and fell twice. The third time we changed the foundation."),
 ('DEN', '乡民', 'night', '夜里风从水面来，门要拴两道。', "At night the wind comes off the water. Two bolts on the door."),
 ('DEN', '乡民', 'after', '潮水的事过去以后，码头照旧按潮水开。人倒是记得久一点。', "Once the tide business passed, the dock opened by the tide as always. People remembered longer."),
 ('OSB', '农人', 'any', '留到来年的一袋种，谁家都有。借的时候说清楚，还的时候也清楚。', "Everyone keeps a sack of seed for next year. Clear terms when borrowing, clear terms when returning."),
 ('OSB', '村长', 'any', '村里的事我管得细。细是因为人手少，不是因为我爱管。', "I run village matters close. Close because hands are few, not because I like it."),
 ('OSB', '乡民', 'night', '夜里麦田里有动静，先看是风还是人。多半是风。', "Something moves in the wheat at night. First ask: wind or man. Mostly wind."),
 ('OSB', '农人', 'after', '来年那一袋留住了以后，谁家借粮都写名字。写字比记性稳。', "Once next year's sack was kept, every loan got a name. Writing holds better than memory."),
 ('MNS', '酒工', 'any', '没有年份的酒也能喝。就是喝的时候得说清是哪一批。', "Wine without a year drinks fine. You just have to say which batch it is."),
 ('MNS', '学徒', 'any', '学院那边一开课，酒馆就空一半。散课以后又满回来。', "When the college holds lectures, half the tavern empties. When it lets out, it fills again."),
 ('MNS', '店主', 'night', '夜里酒馆只卖不赊。赊出去的人，第二天就不来了。', "At night the tavern sells, never lends. Those who owe stop coming the next day."),
 ('MNS', '酒工', 'after', '没有年份那件事之后，账上开始写批次。写批次，比写年份老实。', "After the business of the missing year, the ledger records batches. Batches are more honest than years."),
 ('ALD', '匠人', 'any', '护甲里面的名字是缝在衬里的。不是给买主看的。', "The name inside the armour is stitched into the lining. Not for the buyer."),
 ('ALD', '商贩', 'any', '这城的铺子看手艺，也看谁家师承。师承比手艺贵。', "Shops here judge hands, and also lineage. Lineage costs more."),
 ('ALD', '学徒', 'night', '夜里炉子要压火。压不好，第二天整条街都是烟。', "At night the forge fire must be banked. Bank it badly and the whole street smokes."),
 ('ALD', '匠人', 'after', '名字的事翻出来以后，有几家把衬里拆了重缝。拆的时候没人说话。', "After the names came out, a few houses unpicked their linings. Nobody spoke while they worked."),
 ('SKO', '炉工', 'any', '第二次赎回的价，炉户们自己算了三遍。三遍三个数。', "The furnace men worked the second redemption price three times. Three times, three numbers."),
 ('SKO', '乡民', 'any', '烟囱一停，半个镇子就没饭吃。停不停，不由我们定。', "Stop the stacks and half the town goes hungry. Whether they stop is not ours to decide."),
 ('SKO', '炉工', 'night', '夜里炉温要看着。看着的人不许睡，睡了就换人。', "Someone watches the furnace heat at night. The watcher must not sleep; sleep and you are replaced."),
 ('SKO', '乡民', 'after', '赎回的事定了以后，烟囱照旧冒烟。定了的只是账。', "With the redemption closed, the stacks smoked as before. Only the ledger changed."),
 ('YOS', '牧人', 'any', '最后一匹家纹的布，是留着做样子的。不是留着穿的。', "The last bolt with the family crest is kept for a pattern, not for wearing."),
 ('YOS', '织工', 'any', '羊毛的价看雨。雨多草好，毛就好，价就低。', "Wool prices follow rain. Good rain, good grass, good wool, low price."),
 ('YOS', '织工', 'night', '夜里机子不能停。停了线就乱，乱了要拆半天。', "The loom must not stop at night. Stop and the thread tangles; untangling takes half a day."),
 ('YOS', '牧人', 'after', '家纹的事办完以后，最后那匹布还在架上。谁都没动它。', "After the crest business, the last bolt stayed on the rack. Nobody touched it."),
 ('KOR', '寄存人', 'any', '不是你的姓，就不能签你的名。这话写在墙上，也写在账上。', "If it is not your name, you cannot sign it. That is on the wall and in the ledger."),
 ('KOR', '商贩', 'any', '寄存的货，认条不认人。条丢了，就认账上的日期。', "Stored goods answer to the slip, not the face. Lose the slip and the date in the ledger decides."),
 ('KOR', '看守', 'night', '夜里库房只开一道门。开两道，就有人记不住关哪道。', "At night only one storeroom door opens. Two doors and nobody remembers which to shut."),
 ('KOR', '寄存人', 'after', '姓的事说开以后，账上多了两栏：来处和去处。', "After the name business, the ledger gained two columns: where from, where to."),
 ('EED', '伐木工', 'any', '林线以外不许砍。不是规矩严，是砍了就没了。', "No cutting past the tree line. Not strictness - cut it and it is gone."),
 ('EED', '护林人', 'any', '林子认得脚印。走多了，那条路就自己长出来。', "The forest knows footprints. Walk often and the path grows itself."),
 ('EED', '伐木工', 'night', '夜里林子里有响动别追。多半是獾，也可能不是。', "At night do not chase noises in the woods. Usually a badger. Usually."),
 ('EED', '护林人', 'after', '林线以外的事定了以后，界桩挪了半步。就半步。', "The tree-line case closed, and the boundary post moved half a step. Half a step."),
 ('FOR', '矿工', 'any', '金价之外，还有命价。矿上先算金，后算人。', "Beyond the gold price there is the price of a life. The mine counts gold first, people second."),
 ('FOR', '矿工', 'any', '井下的水要抽，抽水的钱要有人出。谁出，年年吵。', "The water below must be pumped, and someone pays for the pumping. Who pays is argued every year."),
 ('FOR', '看守', 'night', '夜里矿井口留一盏灯。灯灭过两回，两回都出事。', "One lamp stays at the shaft mouth at night. It went out twice, and both times something happened."),
 ('FOR', '矿工', 'after', '金价的事过去以后，井口多了块牌子：先算人。牌子新，字旧。', "After the gold-price business a sign went up at the shaft: count people first. New sign, old words."),
 ('RAT', '乡民', 'any', '兽死之后，地归谁种，吵了整整一个冬天。', "After the beast died, who farms the land was argued the whole winter."),
 ('RAT', '农人', 'any', '纪念的事有人记，地的事有人抢。两件事不是一件事。', "Some remember the memorial; others grab the land. Not the same matter."),
 ('RAT', '乡民', 'night', '夜里别走旧猎径。那路上的坑是旧的，人是新的。', "Do not take the old hunting path at night. The pits are old; the people are new."),
 ('RAT', '农人', 'after', '兽死之后的事办完，地界重新量过。量地的人喝了三壶酒。', "With the aftermath done, the boundary was re-measured. The surveyor drank three jugs."),
 ('PAS', '关兵', 'any', '关口两边，一边看文书，一边看人。两边都累。', "Both sides of the pass: one reads papers, one reads people. Both are tired."),
 ('PAS', '乡民', 'any', '关外种的粮，进关要交一次。交了才叫粮，不交叫私货。', "Grain grown outside the pass pays once to enter. Pay and it is grain; do not and it is contraband."),
 ('PAS', '关兵', 'night', '夜里关楼只留一个火盆。火盆一挪，就是换岗。', "At night the gate tower keeps one brazier. Move the brazier and the watch changes."),
 ('PAS', '乡民', 'after', '关口两边的事谈完以后，粮车排得比从前直。', "After the two sides talked, the grain carts queued straighter than before."),
 ('ASH', '护理者', 'any', '不是空床的村庄，床是留给人的，不是留给数的。', "A village of no empty beds: beds are kept for people, not for numbers."),
 ('ASH', '乡民', 'any', '盆地的风从北边来，晒的衣裳要压石头。', "The basin wind comes from the north. Laundry needs stones on it."),
 ('ASH', '护理者', 'night', '夜里查房两回。第二回是听，不是看。', "Two rounds at night. The second round is for listening, not looking."),
 ('ASH', '乡民', 'after', '床位的事定了以后，门口的名册还是手写的。手写慢，改得清。', "With the bed matter closed, the list at the door stayed handwritten. Slow, and clear to amend."),
 ('HIG', '药农', 'any', '回程也是答案。上山的人先想好怎么下来。', "The way back is also an answer. Before climbing, plan the descent."),
 ('HIG', '挑夫', 'any', '山道上的药棚不问来历，只问你要不要水。', "The shed on the trail asks no names, only whether you want water."),
 ('HIG', '挑夫', 'night', '夜里雾从谷底上来。看见雾，就找石头坐着等。', "At night fog climbs from the valley. See the fog and find a stone to sit and wait."),
 ('HIG', '药农', 'after', '回程的事办完以后，药棚多挂了一盏灯。', "The descent case closed, and the shed hung one more lamp."),
 ('MAE', '学者', 'any', '留下来的城里，学院的门照旧开。开给谁，另说。', "In the city that stayed, the college doors open as before. For whom is another matter."),
 ('MAE', '市民', 'any', '曼恩的墙比别处厚。厚墙也挡不住风向变。', "Maen's walls are thicker than elsewhere. Thick walls do not stop the wind from turning."),
 ('MAE', '市民', 'night', '夜里学院那边安静得过头。安静的地方，人容易多想。', "The college quarter is too quiet at night. Quiet places breed thinking."),
 ('MAE', '学者', 'after', '去留的事定下以后，名册上划掉了三个名字，又添了两个。', "With staying and leaving decided, three names were struck from the roll and two added."),
]
assert len(LINES) == 60, len(LINES)
CJK = re.compile(r'[\u4e00-\u9fff]')
BACK = re.compile(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', re.I)
rows = []
seen_cn, seen_en = {}, {}
for i, (cid, spk, when, cn, en) in enumerate(LINES, 1):
    c = CITIES[cid]
    cond = CM[cid] if when == 'after' else when
    rid = f'TG-{cid}-{i:02d}'
    assert cid in CITIES and spk and cn and en, rid
    assert CJK.search(cn) and not re.search(r'[A-Za-z]', cn), rid + ' cn'
    assert not CJK.search(en) and len(en) <= 150, rid + ' en'
    assert not BACK.search(cn + ' ' + en), rid + ' backstage'
    assert cn not in seen_cn and en not in seen_en, rid + ' dup'
    seen_cn[cn] = rid; seen_en[en] = rid
    if when == 'after': assert cond in {p.stem for p in V.rglob('*.md')}, rid + ' cm'
    rows.append(dict(id=rid, city=cid, speaker=spk, when=cond, cn=cn, en=en,
                     link=pathlib.Path(c['file']).stem, chapter=CM[cid]))
out = dict(date='2026-10-13', scope='S116 Mod-original town ambient gossip: four lines per town with condition vocabulary, CN/EN parity, links to city notes and chapters; no rewards, no task progress, no knowledge leaks',
           vocabulary=['any', 'night', 'after:<CM chapter>'],
           rules=['按城镇写：只谈本城生活、行业与旧事，不替台本当事人发言',
                  '不含奖励、不推进任务、不给库存；闲谈不改任何结算',
                  'after:<CM> 只改未来台词，不回滚旧结；与主章结论不冲突',
                  '与地区闲谈池分工：城镇内说行当与街面，城外说路与景物'],
           lines=rows)
(ROOT / 'research' / 'town-gossip.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "城镇闲谈池"\nid: FX-TOWN-GOSSIP\ntype: script\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S116, dialogue, ambient]\naliases: []\n---\n\n'
     '# 城镇闲谈池\n\n'
     f"十五座城镇各 4 条原创闲谈，共 {len(rows)} 条（中英对照；英文为Mod原创新稿）。城镇内说行当与街面，城外见[[地区闲谈池]]；不替台本当事人发言，不发奖励、不推进任务、不写状态键。\n\n"
     '**条件词表**：`any`、`night`、`after:<主章台本>`；`after` 只改未来台词，与主章结论不冲突。\n\n')
for cid, c in CITIES.items():
    sub = [x for x in rows if x['city'] == cid]
    n += f"## {c['name']}（{len(sub)}）\n\n| 说话人 | 条件 | 中文 | English | 关联 |\n|---|---|---|---|---|\n"
    for x in sub:
        cond = f"`{x['when']}`" if x['when'] in ('any', 'night') else f"`after:{x['when']}`"
        n += f"| {x['speaker']} | {cond} | 「{x['cn']}」 | {x['en']} | [[{x['link']}]] · [[{x['chapter']}]] |\n"
    n += '\n'
n += ('## 边界\n\n- 全部为Mod原创，不复用原作文本；同一事实在不同城镇说法不同，允许含糊与错传。\n'
      '- 闲谈只读 `encountered/resolve/order/presence`、城镇档位与时段；不发物品、不改结算。\n'
      '- 未做：触发距离、作息、生成点与配音（见[[特殊地点阶段制作与校准规程]]）。\n\n'
      '[[地区闲谈池]] · [[野外NPC口吻与闲谈参照]] · [[城镇声望与信任系统]] · [[城市与聚落设计总索引]] · [[特殊地点与野外NPC对白扩展计划]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S116城镇闲谈池（当前登记）\n\n'
           f"[[城镇闲谈池]]：十五城镇各 4 条Mod原创闲谈（中英对照），条件 any/night/after:<主章台本>；城镇内说行当与街面，与[[地区闲谈池]]分工；不发奖励、不推进任务、不写状态键。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/town-gossip-note-hashes.json'
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
rule = ('\n<!-- TOWN-GOSSIP-S116:BEGIN -->\n2026-10-13 S116：城镇闲谈池（原创，中英对照）。'
        f'research/town-gossip.json 十五城镇各4条共 {len(rows)} 条，条件 any/night/after:<主章台本>；城镇内说行当与街面、城外见地区闲谈池；不发奖励、不推进任务、不写状态键。'
        '入口design/02_世界与地图/特殊地点与野外NPC/城镇闲谈池.md；运行Validate-TownGossip.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。\n<!-- TOWN-GOSSIP-S116:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- TOWN-GOSSIP-S116:BEGIN -->.*?<!-- TOWN-GOSSIP-S116:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- TOWN-GOSSIP-S116:BEGIN -->.*?<!-- TOWN-GOSSIP-S116:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/城镇闲谈池.md', '入口 [城镇闲谈池](design/02_世界与地图/特殊地点与野外NPC/城镇闲谈池.md)'), encoding='utf-8')
print(json.dumps(dict(lines=len(rows), cities=len(CITIES), notes=len(generated)), ensure_ascii=False))
