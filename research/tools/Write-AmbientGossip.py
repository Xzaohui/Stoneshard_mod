"""S115: author the Mod-original regional ambient gossip pool (CN/EN).

Region-scoped small talk with a condition vocabulary (any/night/after/band),
tied to existing region and site notes. No rewards, no task progress, no
knowledge leaks; Chinese first with a Mod-original English script.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'AMBIENT-GOSSIP-S115'
CARD = '02_世界与地图/特殊地点与野外NPC/地区闲谈池.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
LINES = [
 # R01 布林外港与旧渠
 dict(id='AG-R01-1', region='R01', speaker='船工', when='any',
      cn='你闻着这股味儿没有？渠水退下去的时候，底下那层旧泥全翻上来。', en="Smell that? When the culvert drops, the old silt turns up from underneath.",
      link='空间_BRY-X11_低潮侧泊棚'),
 dict(id='AG-R01-2', region='R01', speaker='乡民', when='any',
      cn='围城那阵子，我们连渠里的水都省着用。现在说起来像别人的事。', en="During the siege we rationed even the culvert water. It sounds like someone else's story now.",
      link='聚落_BRY_布林'),
 dict(id='AG-R01-3', region='R01', speaker='卫兵', when='night',
      cn='夜里渠口风大。灯要是灭了，别摸黑走，站着等人来。', en='The wind at the culvert mouth is heavy at night. If your lamp dies, stand still and wait for someone.',
      link='区域_R01_布林外港与旧渠'),
 dict(id='AG-R01-4', region='R01', speaker='商贩', when='band:+1',
      cn='码头那几家肯给我留货位，是看我这几年没欠过账。', en='The dock stalls hold space for me because I have never left a debt here.',
      link='人物_FX-BUR_库奇'),
 dict(id='AG-R01-5', region='R01', speaker='乡民', when='after:台本_N1_无钟之夜',
      cn='那晚上的事过去之后，敲钟的人走路都轻了。你听得出。', en='After that night, the bell-ringer walks lighter. You can hear it.',
      link='台本_N1_无钟之夜'),
 # R02 丹布里西路与渡口
 dict(id='AG-R02-1', region='R02', speaker='渡工', when='any',
      cn='水位看桩，别看天。天说下雨，桩说什么时候能过。', en='Watch the post, not the sky. The sky promises rain; the post says when you can cross.',
      link='区域_R02_丹布里西路与渡口'),
 dict(id='AG-R02-2', region='R02', speaker='乡民', when='any',
      cn='磨坊停转以后，村里磨面要走到下一个村。走一趟就是一整天。', en='Since the mill stopped, grinding means walking to the next village. A whole day gone.',
      link='地点设计卡_R02_丹布里西路与渡口'),
 dict(id='AG-R02-3', region='R02', speaker='旅人', when='night',
      cn='夜里别在荒宅过夜。门是开的，里面的响动不是风。', en='Do not sleep in the empty house at night. The door is open, and what creaks inside is not the wind.',
      link='人物_FX-HOM_苇珥'),
 dict(id='AG-R02-4', region='R02', speaker='商贩', when='after:台本_DT08_修好第二块桥板',
      cn='桥板修好以后，我这车能多跑一趟。多跑一趟，孩子就多一双鞋。', en='With the second plank fixed I can make one more run. One more run buys the child another pair of shoes.',
      link='台本_DT08_修好第二块桥板'),
 dict(id='AG-R02-5', region='R02', speaker='乡民', when='band:+1',
      cn='渡口的人认得你的脸了。认脸的地方，价钱好谈一点。', en='The ford men know your face now. Where they know your face, prices bend a little.',
      link='聚落_DEN_丹布里'),
 # R03 曼恩边地
 dict(id='AG-R03-1', region='R03', speaker='农人', when='any',
      cn='今年的田有一半没种。不是懒，是没人手，也没种子。', en='Half the fields went unsown this year. Not laziness - no hands, no seed.',
      link='区域_R03_曼恩边地'),
 dict(id='AG-R03-2', region='R03', speaker='牧人', when='any',
      cn='界石后头那片草场，谁先到谁下陷。规矩是规矩，人是人。', en='The meadow past the boundary stone: first come, first snares. The rule is the rule; people are people.',
      link='人物_FX-HNT_珥兰'),
 dict(id='AG-R03-3', region='R03', speaker='养蜂人', when='any',
      cn='烟一起，蜂就散。田一荒，人也散。道理是一样的。', en='Smoke rises, the bees scatter. Fields go fallow, people scatter. Same lesson.',
      link='人物_FX-HNY_忒曼'),
 dict(id='AG-R03-4', region='R03', speaker='农人', when='after:台本_DT10_别让狼靠近夜岗',
      cn='夜岗安生以后，牲口回圈早了。狼还在，只是不进棚。', en='Since the night watch settled, the stock comes home early. The wolves are still there; they just keep off the pens.',
      link='台本_DT10_别让狼靠近夜岗'),
 dict(id='AG-R03-5', region='R03', speaker='乡民', when='night',
      cn='入冬前别往草场深处走。陷是旧的，狼是新的。', en='Before winter, keep out of the deep meadow. The snares are old; the wolves are new.',
      link='人物_FX-HNT_珥兰'),
 # R04 王廷关隘与边城
 dict(id='AG-R04-1', region='R04', speaker='石工', when='any',
      cn='关楼的石头是从坑里一块块抬上来的。抬石头的人没留下名字。', en='The gate stones were carried up one by one. The carriers left no names.',
      link='地点设计卡_R04_王廷关隘与边城'),
 dict(id='AG-R04-2', region='R04', speaker='卫兵', when='any',
      cn='过关要看文书，看不了的就看人。看得多了，人比纸准。', en='At the pass we read papers, and when papers fail we read people. Read enough and people beat paper.',
      link='区域_R04_王廷关隘与边城'),
 dict(id='AG-R04-3', region='R04', speaker='乡民', when='night',
      cn='夜里崖上落石。听见响别抬头，往墙根靠。', en='Rock falls off the cliff at night. If you hear it, do not look up - get to the wall foot.',
      link='人物_FX-HRP_妲兰'),
 dict(id='AG-R04-4', region='R04', speaker='石工', when='after:台本_N7_军需账上的空名',
      cn='军需账的事传开了以后，坑边来看热闹的人多了。看热闹不出工钱。', en='Since the quartermaster ledger got around, more people come to stare at the pit. Staring pays no wages.',
      link='台本_N7_军需账上的空名'),
 dict(id='AG-R04-5', region='R04', speaker='旅人', when='band:+1',
      cn='守门的肯跟你多说两句，说明你上次没给他们添乱。', en='The gate men talk a while longer with you - that means last time you caused them no trouble.',
      link='聚落_PAS_柏石关与关外聚落'),
 # R05 灰烬湿地与疫村
 dict(id='AG-R05-1', region='R05', speaker='护理者', when='any',
      cn='湿地边上的路要横着走。竖着走，脚下就是坑。', en='Cross the wetland edge sideways. Straight ahead is a hole.',
      link='人物_FX-LEP_米洛珥'),
 dict(id='AG-R05-2', region='R05', speaker='乡民', when='any',
      cn='封条是给外人看的。住在这儿的人，看的是风。', en='The seals are for outsiders. Those who live here watch the wind.',
      link='人物_FX-PLG_蔻珥'),
 dict(id='AG-R05-3', region='R05', speaker='乡民', when='night',
      cn='夜里有狗叫就回屋。狗比人先知道谁在田埂上走。', en='If the dogs bark at night, go inside. Dogs know who walks the dikes before people do.',
      link='区域_R05_灰烬湿地与疫村'),
 dict(id='AG-R05-4', region='R05', speaker='护理者', when='after:台本_DT16_愿意继续治疗的人',
      cn='愿意继续治的人多了一个，药还是那些药。省着用。', en='One more person chose to keep treating, and the medicine is the same medicine. We stretch it.',
      link='台本_DT16_愿意继续治疗的人'),
 dict(id='AG-R05-5', region='R05', speaker='旅人', when='band:+1',
      cn='村里肯给你指近路，是把你当熟人了。别把近路说给外人。', en='The village shows you the short path now; that means you count as a local. Do not pass it on.',
      link='聚落_DEN_丹布里'),
 # R06 无名修院山地
 dict(id='AG-R06-1', region='R06', speaker='药农', when='any',
      cn='山道上的石堆是路标，不是坟。别把路标踢散。', en='The stone piles on the trail are signs, not graves. Do not kick them apart.',
      link='人物_FX-CV1_珞珥'),
 dict(id='AG-R06-2', region='R06', speaker='矿工', when='any',
      cn='进洞先敲木头。木头响得实，你就还能往里走。', en='Knock the timber before you go in. If it rings solid, you may walk further.',
      link='人物_FX-MIN_珥德'),
 dict(id='AG-R06-3', region='R06', speaker='旅人', when='night',
      cn='修院方向夜里不点灯。你要是看见灯，那不是修院。', en='No lamps burn toward the monastery at night. If you see one, it is not the monastery.',
      link='空间_HIG_无名修院山地'),
 dict(id='AG-R06-4', region='R06', speaker='药农', when='after:台本_DT05_驿馆的急用药',
      cn='驿馆的药送到以后，山道上问药的人少了一半。', en='After the inn got its medicine, half the people asking on the trail stopped asking.',
      link='台本_DT05_驿馆的急用药'),
 dict(id='AG-R06-5', region='R06', speaker='乡民', when='band:+1',
      cn='山里人认熟不认官。你多来两趟，比带什么文书都管用。', en='Mountain folk trust habit, not papers. Two more visits beat any letter you carry.',
      link='区域_R06_无名修院山地'),
]
assert len({x['id'] for x in LINES}) == len(LINES) == 30
CJK = re.compile(r'[\u4e00-\u9fff]')
seen_cn, seen_en = {}, {}
for x in LINES:
    assert x['region'] in {'R01', 'R02', 'R03', 'R04', 'R05', 'R06'}, x['id']
    assert re.fullmatch(r'any|night|band:[+-]1|after:.+', x['when']), x['id'] + ' when'
    for k in ('speaker', 'cn', 'en'):
        assert x[k].strip(), x['id'] + ' ' + k
    assert CJK.search(x['cn']) and not re.search(r'[A-Za-z]', x['cn']), x['id'] + ' cn purity'
    assert not CJK.search(x['en']) and len(x['en']) <= 150, x['id'] + ' en purity'
    assert not re.search(r'\b(?:resolve|paid|relief|accountable|exclusive|patron|sponsor|consent)\b|\b(?:SQ|DT|CM|CS|NE)\b|\bN\d{1,2}\b', x['cn'] + ' ' + x['en'], re.I), x['id'] + ' backstage'
    assert x['cn'] not in seen_cn and x['en'] not in seen_en, x['id'] + ' duplicate'
    seen_cn[x['cn']] = x['id']; seen_en[x['en']] = x['id']
    if x['when'].startswith('after:'): assert x['when'][6:] in {p.stem for p in V.rglob('*.md')}, x['id'] + ' after-task'
    assert x['link'] in {p.stem for p in V.rglob('*.md')}, x['id'] + ' link'
out = dict(date='2026-10-13', scope='S115 Mod-original regional ambient gossip: region-scoped lines with condition vocabulary, CN/EN parity, links to existing notes; no rewards, no task progress, no knowledge leaks',
           vocabulary=['any', 'night', 'band:+1', 'band:-1', 'after:<task>'],
           rules=['按地区写：只谈本区生活、景物与旧事，不替台本当事人发言',
                  '不含奖励、不推进任务、不给库存；闲聊不改任何结算',
                  '同一事实不与台本冲突：只作路人视角，可含糊、可错传',
                  '条件词表固定：any/night/band:+1/band:-1/after:<task>；after 只重评未来台词'],
           lines=LINES)
(ROOT / 'research' / 'ambient-gossip.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
REGNAME = {'R01': '布林外港与旧渠', 'R02': '丹布里西路与渡口', 'R03': '曼恩边地', 'R04': '王廷关隘与边城', 'R05': '灰烬湿地与疫村', 'R06': '无名修院山地'}
n = ('---\ntitle: "地区闲谈池"\nid: FX-AMBIENT-GOSSIP\ntype: script\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S115, dialogue, ambient]\naliases: []\n---\n\n'
     '# 地区闲谈池\n\n'
     f"六个地域的原创闲谈，共 {len(LINES)} 条（中英对照；英文为Mod原创新稿）。按[[野外NPC口吻与闲谈参照]]的结构写：先给一句眼前事，再补细节或感慨；只谈本区生活与旧事，不替台本当事人发言，不发奖励、不推进任务。\n\n"
     '**条件词表**：' + '、'.join('`' + w + '`' for w in out['vocabulary']) + '。`after:<台本>` 只改未来台词，不回滚旧结。\n\n')
for rid in ['R01', 'R02', 'R03', 'R04', 'R05', 'R06']:
    sub = [x for x in LINES if x['region'] == rid]
    n += f"## {REGNAME[rid]}（{len(sub)}）\n\n| 说话人 | 条件 | 中文 | English | 关联 |\n|---|---|---|---|---|\n"
    for x in sub:
        n += f"| {x['speaker']} | `{x['when']}` | 「{x['cn']}」 | {x['en']} | [[{x['link']}]] |\n"
    n += '\n'
n += ('## 边界\n\n- 全部为Mod原创，不复用原作文本；同一事实在不同地区有不同说法，允许错传与含糊。\n'
      '- 闲谈不改变任务状态、不写状态键、不发物品；播放条件只读 `encountered/resolve/order/presence` 与时段。\n'
      '- 未做：触发距离、作息与生成点（见[[特殊地点阶段制作与校准规程]]）；逐条配音与本地化终审。\n\n'
      '[[野外NPC口吻与闲谈参照]] · [[特殊地点与野外NPC阶段验收记录]] · [[台本_FX_野外人物对白]] · [[特殊地点设计卡总表]] · [[特殊地点与野外NPC对白扩展计划]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S115地区闲谈池（当前登记）\n\n'
           f"[[地区闲谈池]]：六地域 {len(LINES)} 条Mod原创闲谈（中英对照），条件词表 any/night/band:+1/band:-1/after:<台本>；只谈本区生活与旧事，不发奖励、不推进任务、不改结算。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/ambient-gossip-note-hashes.json'
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
rule = ('\n<!-- AMBIENT-GOSSIP-S115:BEGIN -->\n2026-10-13 S115：地区闲谈池（原创，中英对照）。'
        f'research/ambient-gossip.json 六地域 {len(LINES)} 条，条件词表 any/night/band:+1/band:-1/after:<台本>；只谈本区生活与旧事，不发奖励、不推进任务、不写状态键。'
        '入口design/02_世界与地图/特殊地点与野外NPC/地区闲谈池.md；运行Validate-AmbientGossip.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。\n<!-- AMBIENT-GOSSIP-S115:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- AMBIENT-GOSSIP-S115:BEGIN -->.*?<!-- AMBIENT-GOSSIP-S115:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- AMBIENT-GOSSIP-S115:BEGIN -->.*?<!-- AMBIENT-GOSSIP-S115:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/地区闲谈池.md', '入口 [地区闲谈池](design/02_世界与地图/特殊地点与野外NPC/地区闲谈池.md)'), encoding='utf-8')
print(json.dumps(dict(lines=len(LINES), regions=6, notes=len(generated)), ensure_ascii=False))
