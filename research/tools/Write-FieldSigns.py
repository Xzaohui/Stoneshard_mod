"""Author S101 field signs/observations for the remaining 16 sites.

Signs are observations (tracks, marks, residue) with a judgement hint and a
danger note; reading a sign grants knowledge only: no reward, no task progress,
no substitute for any person's consent.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'FIELD-SIGNS-S101'
CARD = '02_世界与地图/特殊地点与野外NPC/野外迹象与观察.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inv = json.loads((ROOT / 'research/special-location-inventory.json').read_text(encoding='utf-8'))
SITES = {r['key']: r['name_zh'] for r in inv['rumor_sites']}
SIGNS = [
 dict(id='SGN-BR1', site='rumor_bearHG1', title='倒木上的抓痕', obs='离地一人高的抓痕，三道并排，树皮向外翻；下方落着碎蜂巢。',
      judge='是护崽母熊的领地标记：抓痕越高，熊越大。', danger='别顺着抓痕方向走；退的时候别跑。', link='人物_FX-HNY_忒曼'),
 dict(id='SGN-BR2', site='rumor_bearHG2', title='果园篱笆的塌口', obs='篱笆压塌一段，果核堆在缺口内侧，脚印往返都走同一个口。',
      judge='熊把这里当固定觅食路；缺口是新近踩塌的。', danger='夜里别进园；装死无效，退到开阔处。', link='人物_FX-HNT_珥兰'),
 dict(id='SGN-CP1', site='rumor_camp1', title='哨位草垫', obs='壕沟内侧草垫压得很实，旁边插着削尖的木桩，灰烬是新的。',
      judge='营里有人换班；草垫朝向说明哨位盯着来路。', danger='别从正坡上；绊索就挂在草垫前两步。', link=''),
 dict(id='SGN-CP3', site='rumor_camp3', title='火塘三石', obs='三块石头围成的火塘，灰是冷的；旁边草被压平，像睡过两三夜。',
      judge='过路人临时营地，规矩是走前把火压灭。', danger='冷灰里可能还埋着炭；夜里有人借宿不打招呼。', link='人物_FX-RLY_珥薇'),
 dict(id='SGN-CP5', site='rumor_camp5', title='补过的帐布', obs='帐布补丁叠补丁，晾绳上还挂着没收走的布条；地钉斜插，扎得很浅。',
      judge='流民过夜处：帐子不锁，收帐才走。', danger='地钉伤脚；帐布受潮，别在里面生火。', link=''),
 dict(id='SGN-CV2', site='rumor_cave2', title='洞口熄过的火', obs='洞内三步处有熄火堆，药篓残片压在石下；地面苔线被踩断。',
      judge='采药人歇脚点；歇脚不进深段。', danger='浅洞也有野兽借宿；进前先听。', link='人物_FX-CV1_珞珥'),
 dict(id='SGN-CV4', site='rumor_cave4', title='蹭秃的树皮', obs='洞口两侧树皮蹭得发亮，地面爪印同向，骨堆在兽道口。',
      judge='兽道明显，走的是同一头；骨堆是进食处。', danger='护崽野兽守在兽道口；退比跑安全。', link=''),
 dict(id='SGN-CV5', site='rumor_cave5', title='根洞与刻痕', obs='老梣树根系间有空洞，树皮上刻着旧记号；洞底积水反光。',
      judge='记号是早年的路标，指的不是洞，是绕行的方向。', danger='根洞积水，蛇会借凉；别把手伸进空腔。', link=''),
 dict(id='SGN-CV6', site='rumor_cave6', title='冲沟与漂来的木片', obs='谷地中央一道新冲沟，沟沿挂着上游漂来的木片与草根。',
      judge='雨来得快，水线比人快；冲沟是上一场雨的线。', danger='暴雨时别下谷；退到高处等水落。', link=''),
 dict(id='SGN-GH2', site='rumor_ghoulDen2', title='窖口结网', obs='废弃窖口结着灰网，网后散着骨片；窖口窄，只容侧身。',
      judge='窖内缺氧，出入只有这一个口。', danger='别独自侧身进；点火会把氧耗得更快。', link='人物_FX-GHL_达珥'),
 dict(id='SGN-GR2', site='rumor_grazingHG2', title='水边蹄印', obs='水边泥地上蹄印杂乱，深浅不一；树皮被啃到齐腰高。',
      judge='清晨是饮水时段，野物成群；蹄印说明这几天来过。', danger='清晨饮水时最危险；别在下风处蹲守。', link='人物_FX-HNT_珥兰'),
 dict(id='SGN-GR3', site='rumor_grazingHG3', title='晾草架与茬口', obs='晾草架还立着，茬口整齐；架下散着断绳与两把旧镰。',
      judge='收草季人多，械斗与误伤都出在这几天。', danger='别在收草时穿场；镰比人快。', link=''),
 dict(id='SGN-MN2', site='rumor_mine2', title='矿车残件与记号', obs='矿车残件堆在轨旁，木撑上刻着捡拾人的记号；轨面下沉一段。',
      judge='记号标出下沉段；捡拾人只走轨枕。', danger='木撑朽坏，别靠；轨下沉会崴脚。', link='人物_FX-MIN_珥德'),
 dict(id='SGN-MO1', site='rumor_mooseHG1', title='折枝的新茬', obs='灌木折口是新的，高度到胸口；泥地蹄印比牛蹄还大。',
      judge='驼鹿刚过，折枝高度说明体型。', danger='发情期驼鹿主动冲撞；绕到它上风处。', link=''),
 dict(id='SGN-WF1', site='rumor_wolfHG1', title='拖痕与界桩', obs='田界木桩被啃出缺口，草上拖着一条浅痕通向棚圈方向。',
      judge='狼群入冬前靠近棚圈；拖痕是叼走猎物的路。', danger='狼群护食；别追拖痕，护好牲畜先。', link='人物_FX-HNT_珥兰'),
 dict(id='SGN-WF2', site='rumor_wolfHG2', title='旧猎径上的爪印', obs='旧猎径上爪印深浅不一，前爪比后爪深；风向标草朝同一侧倒。',
      judge='独狼也走这条径；爪印深浅说明它跑过。', danger='独狼也会扑人；沿倒草的反方向退。', link=''),
]
SIGNS_EN = {'SGN-BR1': {'title_en': 'Claw Marks on a Fallen Trunk', 'obs_en': 'Three parallel scores at shoulder height, bark curling outward; a crushed honeycomb below.', 'judge_en': 'A sow bear boundary mark: the higher the scores, the bigger the bear.', 'danger_en': 'Do not follow the line of the marks; back off without running.'}, 'SGN-BR2': {'title_en': 'A Breach in the Orchard Fence', 'obs_en': 'A fence section pressed flat, pits piled inside the gap, prints entering and leaving by the same hole.', 'judge_en': 'The bear uses this as a feeding route; the breach is freshly trampled.', 'danger_en': 'Stay out of the orchard at night; playing dead fails, retreat to open ground.'}, 'SGN-CP1': {'title_en': 'A Sentry Grass Pad', 'obs_en': 'A pad pressed hard inside the ditch, sharpened stakes beside it, ash still fresh.', 'judge_en': 'The camp runs shifts; the pad faces the approach, so the sentry watches the path up.', 'danger_en': 'Do not come up the main slope; trip cords run two paces before the pad.'}, 'SGN-CP3': {'title_en': 'Three Stones of a Fire Ring', 'obs_en': 'A ring of three stones, ash cold, grass nearby flattened as if slept on for two or three nights.', 'judge_en': 'A travellers camp; the rule is to smother the fire before leaving.', 'danger_en': 'Cold ash can hide embers; strangers may share the spot without a word.'}, 'SGN-CP5': {'title_en': 'Patched Tent Canvas', 'obs_en': 'Patch over patch, a cloth strip still on the line, pegs set shallow and crooked.', 'judge_en': 'A shelter for displaced folk: the tent is not locked, it leaves when they do.', 'danger_en': 'Pegs catch feet; damp canvas and a fire inside do not mix.'}, 'SGN-CV2': {'title_en': 'A Dead Fire at the Cave Mouth', 'obs_en': 'Three paces in, a smothered fire, herb-basket shards under a stone, moss line broken by boots.', 'judge_en': 'A herbalist rest stop; rest stops do not go deep.', 'danger_en': 'Even shallow caves shelter animals; listen before entering.'}, 'SGN-CV4': {'title_en': 'Rubbed-Bare Bark', 'obs_en': 'Bark polished on both sides of the mouth, prints heading one way, bones piled at the trail head.', 'judge_en': 'A clear animal trail used by one beast; the bone pile is where it feeds.', 'danger_en': 'A guarding animal holds the trail head; backing away beats running.'}, 'SGN-CV5': {'title_en': 'Root Hollow and Cut Marks', 'obs_en': 'A hollow between ash roots, old marks cut in the bark, water glinting at the bottom.', 'judge_en': 'The marks are an old road sign; they point away from the hollow, not into it.', 'danger_en': 'Hollows hold water and snakes; keep hands out of the cavity.'}, 'SGN-CV6': {'title_en': 'Gully and Driftwood', 'obs_en': 'A fresh gully down the valley floor, wood chips and roots snagged on its lip.', 'judge_en': 'Rain arrives fast; the water line runs quicker than a person; the gully is last storm line.', 'danger_en': 'Stay out of the valley in a downpour; wait on high ground until it drops.'}, 'SGN-GH2': {'title_en': 'Webbing over a Cellar Mouth', 'obs_en': 'Grey web over an abandoned cellar mouth, bone fragments behind it; the opening fits one person sideways.', 'judge_en': 'Air inside runs thin, and there is only this one way in.', 'danger_en': 'Do not squeeze in alone; a flame burns the air faster.'}, 'SGN-GR2': {'title_en': 'Hoofprints at the Water', 'obs_en': 'Mud churned by prints of differing depth; bark gnawed to waist height.', 'judge_en': 'Dawn is the drinking hour and the herd comes together; the prints say they came these days.', 'danger_en': 'Dawn at the water is the worst hour; do not wait downwind.'}, 'SGN-GR3': {'title_en': 'Hay Rack and Stubble', 'obs_en': 'The rack still stands, stubble cut even; snapped cord and two old sickles beneath.', 'judge_en': 'The haying season draws crowds; brawls and cuts happen in these days.', 'danger_en': 'Do not cross the field while haying; a sickle is quicker than a person.'}, 'SGN-MN2': {'title_en': 'Cart Parts and Marks', 'obs_en': 'Cart parts piled by the rails, the salvager marks cut into the props, a stretch of rail sunk.', 'judge_en': 'The marks flag the sunken stretch; the salvager walks sleepers only.', 'danger_en': 'Rotten props, and sunken rail turns ankles; do not lean on either.'}, 'SGN-MO1': {'title_en': 'Fresh Break on a Bush', 'obs_en': 'Breaks are fresh, chest-high; prints in the mud larger than an ox hoof.', 'judge_en': 'A moose just passed; break height tells the size.', 'danger_en': 'In rut a moose charges; circle to its upwind side.'}, 'SGN-WF1': {'title_en': 'Drag Marks and a Boundary Post', 'obs_en': 'A post gnawed at the notch, a shallow drag line running toward the pens.', 'judge_en': 'Wolves close in on pens before winter; the drag is how prey is carried off.', 'danger_en': 'Wolves guard their kill; do not follow the drag, see to the stock first.'}, 'SGN-WF2': {'title_en': 'Prints on an Old Hunting Path', 'obs_en': 'Prints of uneven depth on the old path, front deeper than rear; grass laid one way.', 'judge_en': 'A lone wolf uses this path too; print depth says it ran.', 'danger_en': 'A lone wolf will still charge; retreat against the laid grass.'}}
for s in SIGNS: s.update(SIGNS_EN[s['id']])
assert len({s['id'] for s in SIGNS}) == len(SIGNS) == 16
for s in SIGNS:
    assert s['site'] in SITES, s['id'] + ' site'
    for k in ('title', 'obs', 'judge', 'danger'): assert s[k].strip(), s['id'] + ' ' + k
    assert re.search(r'[\u4e00-\u9fff]', s['obs']) and not re.search(r'[A-Za-z]', s['obs'] + s['judge'] + s['danger']), s['id'] + ' purity'
    for k in ('title_en', 'obs_en', 'judge_en', 'danger_en'):
        s3 = s[k]
        assert s3.strip() and not re.search(r'[\u4e00-\u9fff]', s3) and len(s3) <= 220, s['id'] + ' en ' + k
out = dict(date='2026-10-13', scope='S101 field signs for the remaining 16 sites: observation, judgement hint and danger note; reading grants knowledge only, no reward and no task progress',
           rules=['迹象是观察：只给信息与判定提示，不发奖励、不完成任务、不替代当事人同意',
                  '判定提示写“看得出什么”，不写数值与掉落', '危险提示给退路，不给解法；不新增道具',
                  '与人物、文书互链；同一地点若有人物，迹象只说现场，不替人物说话'],
           signs=SIGNS)
(ROOT / 'research/field-signs.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
n = ('---\ntitle: "野外迹象与观察"\nid: FX-FIELD-SIGNS\ntype: script\nstatus: draft\ncanon: mod-original\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S101, field-npc, signs]\naliases: []\n---\n\n'
     '# 野外迹象与观察\n\n'
     f"本页补足[[特殊地点与野外NPC清点]]中尚未有人物的 16 处地点：以「迹象」形式给出观察、判定提示与危险退路。"
     '迹象只给信息，不发奖励、不完成任务、不替代当事人同意；中英对照（英文为Mod原创新稿）。与[[台本_FX_野外人物对白]]、[[文书_FX_野外地点短稿]]互链。人物与迹象合计覆盖 44 处传闻地点；部分地点两者并存，人物在场不撤现场观察。\n\n'
     '| 迹象 | 地点 | 关联 |\n|---|---|---|\n')
for s in SIGNS:
    link = f"[[{s['link']}]]" if s['link'] else '—'
    n += f"| {s['title']}（`{s['id']}`） | `{s['site']}` {SITES[s['site']]} | {link} |\n"
for s in SIGNS:
    n += f"\n## {s['title']} / {s['title_en']}\n\n**地点**：`{s['site']}` {SITES[s['site']]}。**观察**：{s['obs']}\n\n**Observation (EN)**：{s['obs_en']}\n\n**判定提示**：{s['judge']}\n\n**Judgement (EN)**：{s['judge_en']}\n\n**危险与退路**：{s['danger']}\n\n**Danger and retreat (EN)**：{s['danger_en']}\n"
n += ('\n## 边界\n\n- 迹象为Mod原创；判定提示只写“看得出什么”，不含数值、掉落与概率。\n'
      '- 观察不改变实际判定与生成；真正的地表排布、生成点与触发范围待制作阶段核对。\n'
      '- 未做：比例位置、生成权重、英文稿。\n\n'
      '[[特殊地点与野外NPC对白扩展计划]] · [[特殊地点与野外NPC清点]] · [[特殊地点设计卡总表]] · [[台本_FX_野外人物对白]] · [[文书_FX_野外地点短稿]]\n')
put(CARD, n)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S101野外迹象与观察（当前登记）\n\n'
           f"[[野外迹象与观察]]：16 处地点以迹象形式补齐（抓痕、塌口、哨位草垫、火塘、帐布、兽道、根洞、冲沟、窖口、蹄印、晾草架、矿车记号、折枝、拖痕、爪印），含判定提示与危险退路；44 处传闻地点全部有内容落点（28 人物＋16 迹象）。迹象只给信息，不发奖励。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/field-signs-note-hashes.json'
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
rule = ('\n<!-- FIELD-SIGNS-S101:BEGIN -->\n2026-10-13 S101：用户要求扩充各特殊地点。'
        'research/field-signs.json 为剩余16处地点补“迹象与观察”（观察/判定提示/危险退路），入口design/02_世界与地图/特殊地点与野外NPC/野外迹象与观察.md；44处传闻地点至此全部有落点（28人物＋16迹象）。'
        '迹象只给信息：不发奖励、不完成任务、不替代同意；判定不含数值掉落。运行Validate-FieldSigns.py及既有检查；生成点与比例仍待制作，不部署游戏包。\n<!-- FIELD-SIGNS-S101:END -->\n')
for p in [ROOT / 'AGENTS.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- FIELD-SIGNS-S101:BEGIN -->.*?<!-- FIELD-SIGNS-S101:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'README.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- FIELD-SIGNS-S101:BEGIN -->.*?<!-- FIELD-SIGNS-S101:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/野外迹象与观察.md', '入口 [野外迹象与观察](design/02_世界与地图/特殊地点与野外NPC/野外迹象与观察.md)'), encoding='utf-8')
print(json.dumps(dict(signs=len(SIGNS), notes=len(generated)), ensure_ascii=False))
