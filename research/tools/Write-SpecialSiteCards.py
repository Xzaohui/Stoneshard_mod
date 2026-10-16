"""Author S95 special-site design cards (six regions) tying S92 sites to S94 NPCs.

Per-site rows carry use, observables, dangers and links; region sections carry
terrain/use, entry and safe return, services, original-content avoidance and
task/person links. Design intent only: no proportional maps or runtime rooms.
"""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'SITE-CARDS-S95'
IDX = '02_世界与地图/特殊地点与野外NPC/特殊地点设计卡总表.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
inv = json.loads((ROOT / 'research/special-location-inventory.json').read_text(encoding='utf-8'))
SITE_NAME = {r['key']: r['name_zh'] for r in inv['rumor_sites']}
SITE_EN = {r['key']: r.get('name_en', '') for r in inv['rumor_sites']}
REGIONS = [
 dict(id='R01', name='布林外港与旧渠', note='区域_R01_布林外港与旧渠',
      terrain='港区外沿的旧渠、碎石坡与围城后留下的营地。白天地面湿滑、盐锈味重，夜里风从渠口灌进来，声大得盖过脚步。',
      use='拾荒、走私卸货、围城遗民临时过夜；旧渠是布林排水的老路，也是不登记的人走的路。',
      entry='主入口沿港区外沿的排水口石阶；安全回程是渠口外的拴船桩——从桩位能看见港灯，逆着灯走即可回城。',
      observables='渠壁上的旧水位线、被锯断的闸栅、营地焦土里的锅底与钉鞋印。',
      dangers='涨潮时渠内水位骤升；渠顶碎石松动；围城营地埋着断铁与未清的钉子。',
      service='无固定服务；临时交换只发生在熟人之间，不设柜台。',
      avoid='不重写布林围城的官方叙述，也不把旧渠写成主线必经；原作港区商店与守卫照旧。',
      links=['聚落_BRY_布林', '空间_BRY-X11_低潮侧泊棚', '人物_FX-BUR_库奇', '人物_FX-SGE_瓦顿', '人物_FX-QRY_德茹']),
 dict(id='R02', name='布林东侧河口与渡口', note='区域_R02_布林东侧河口与渡口',
      terrain='布林东侧河口沿河两岸的土路、水磨渠、零散农宅与一处旧旅店。春天路面翻浆，秋天渡口雾重。',
      use='运粮、磨面、过路住店；荒宅与空磨坊是路人歇脚处，也是小偷踩点的目标。',
      entry='沿官道里程碑走；安全回程是渡口摆渡棚——棚下能看见对岸灯，按灯位等下一班渡船。',
      observables='磨渠里的浮草与断闸、荒宅灶台里的旧灰、旅店门口被换过两次的招牌钉孔。',
      dangers='涨水漫过磨渠小桥；荒宅地板塌陷；夜路劫道与假路标。',
      service='旅店提供过夜与热灶（不赊账）；磨坊不代垫粮。不新增柜台与服务。',
      avoid='不动原作的渡口与旅店店主身份；不改官方商路走向。',
      links=['聚落_DEN_丹布里', '人物_FX-MIL_霍珥', '人物_FX-HOM_苇珥', '人物_FX-INK_韦珥']),
 dict(id='R03', name='曼恩边地', note='区域_R03_曼恩边地',
      terrain='缓坡草场、田界石与零散林地；边界一带的田今年有一半没种。',
      use='放牧、设陷、养蜂与拾穗；猎场按季节换人用，谁先到谁下陷。',
      entry='沿田界石走，猎径在第二块界石后分岔；安全回程是草场北侧的看羊棚，棚顶有旗杆可认。',
      observables='翻起的草皮（新陷）、蜂箱上的烟熏痕、被啃过的田界木桩。',
      dangers='未撤的兽夹与陷坑；蜂群受惊；狼群在入冬前后靠近棚圈。',
      service='无固定服务；蜂蜜与皮毛只在收获季临时交易。',
      avoid='不替原作牧场主与猎人NPC改写身份；不动官方狩猎任务点。',
      links=['聚落_OSB_奥斯布鲁克', '聚落_MNS_曼郡', '人物_FX-HNY_忒曼', '人物_FX-HNT_珥兰']),
 dict(id='R04', name='王廷关隘与边城', note='区域_R04_王廷关隘与边城',
      terrain='关隘两侧的采石坡、崖壁与老城堡残墙；风大、石屑多，夜里崖上落石。',
      use='采石供边城修缮、设绳捕鸟、残兵守堡。',
      entry='沿关道石阶上到采石台，再分岔去崖壁与老堡；安全回程是关道第一座里程碑——回到碑位就能看见关楼旗。',
      observables='崖壁上的旧绳扣、老堡门栓上被摸亮的铜环。',
      dangers='塌方线与落石；哈比俯冲；老堡东墙根有塌角。',
      service='无固定服务；残兵只给口信，不发放通行。',
      avoid='不写王廷调令与军务，不动原作关隘守军编制。',
      links=['聚落_PAS_柏石关与关外聚落', '空间_PAS_柏石关与关外聚落', '人物_FX-HRP_妲兰', '人物_FX-BST_恩岱']),
 dict(id='R05', name='灰烬湿地与疫村', note='区域_R05_灰烬湿地与疫村',
      terrain='烧过的田埂、浅水湿地与废弃病院；雾天能见度低，地面踩下去会冒水。',
      use='护理、送药、避居与拾荒；湿地边有人替病人跑腿，也有人替自己藏身。',
      entry='沿湿地木栈道走，岔口挂草绳为记；安全回程是栈道起点的旧风车基座，基座朝向能定方向。',
      observables='栈道新换的木条、病院篱笆上的药罐、湿地边圈地的红果丛。',
      dangers='湿地暗坑与瘴气；病院里的病人不可被围观；夜里有野狗与游荡者。',
      service='护理者收放台阶上的物资，不设交易；不给药品配方。不新增柜台与服务。',
      avoid='不把疫病写成可治愈的奖励线，不动原作病村叙事与医护NPC身份。',
      links=['台本_DT16_愿意继续治疗的人', '人物_FX-LEP_米洛珥', '人物_FX-WCH_索妲', '人物_FX-CAT_洛珉']),
 dict(id='R06', name='无名修院山地', note='区域_R06_无名修院山地',
      terrain='山道、旧矿洞与修院废墟；坡陡林密，雾从谷底上来得很快。',
      use='采药、旧矿捡拾、避难与守墓；修院停用后，钟楼成了过夜处。',
      entry='沿山道石堆标记走，矿洞与修院各有一处岔口；安全回程是山道口的药棚——棚柱上刻着回程箭号。',
      observables='药棚晾草的分层、矿洞口的旧轨道、修院后墙的豁口与钟楼空阶。',
      dangers='矿洞塌方与迷路；修院地窖不可擅入；山雨来时石阶湿滑。',
      service='学徒记账不抓药；避难者只交换口信。不新增柜台与服务。',
      avoid='不揭原作修院与地窖内容，不动官方山道任务点。',
      links=['空间_HIG_无名修院山地', '人物_FX-HUT_珂琳', '人物_FX-ABY_缇菈', '人物_FX-CRP_瑟珥']),
]
SITES = {
 'R01': [
  ('rumor_crawlerBurrow1', '蛛丝拾取与旧渠探路；拾荒人以此为生', '洞口起风的时段、新旧丝网的层次', '新丝网粘手、洞里不止一窝', '人物_FX-BUR_库奇'),
  ('rumor_siegeCamp1', '围城后遗弃的营地，逃兵在此埋锅', '焦土、半截甲片、埋在地里的钉子', '埋铁崴脚、夜里气味引野兽', '人物_FX-SGE_瓦顿'),
  ('rumor_camp3', '过路者临时扎营点，锅灶还在', '火塘三石、被压平的草', '夜里有人借宿不打招呼', ''),
  ('rumor_camp5', '空地营帐，收容不愿进城的流民', '晾绳、补过的帐布', '账布受潮发霉、地钉伤脚', '人物_FX-CP5_缶珥'),
  ('rumor_banditRuins1', '废弃庄园，匪帮换过几拨人', '门廊的刻痕、翻倒的酒架', '残留的埋伏与塌顶', '人物_FX-MAN_岱珥'),
  ('rumor_abandonedQuarry1', '布林以东废弃石场（坡道Q1规划本地格41,33、坑区Q2 42,32）；采石场停工，看守仍在坑边', '塌方线白痕、渗水的岩壁', '塌方线与夜间落石，坑边不许靠近', '人物_FX-QRY_德茹'),
 ],
 'R02': [
  ('rumor_abandonedWatermill1', '停转的磨坊，守磨人仍在看闸', '浮草、断闸、磨盘上的旧粉痕', '开闸放水的连带责任、水口滑石', '人物_FX-MIL_霍珥'),
  ('rumor_homestead1', '安静的农宅，仍有人住', '烟囱的新烟、院里的菜畦', '夜间敲门者身份不明', '人物_FX-FRM_蓟珥'),
  ('rumor_homesteadAbandoned1', '荒宅，拾荒者翻拣遗物', '塌陷的地板、烟道里的窝', '地板塌陷、拾荒者不愿分享里屋', '人物_FX-HOM_苇珥'),
  ('rumor_ralphSons1', '路边旅店，三兄弟各管一摊', '被换过的招牌钉孔、漏雨的客房', '赊账纠纷、夜里冷灶', '人物_FX-INK_韦珥'),
  ('rumor_camp2', '荒废营地，被后来者当成中继点', '压平的草、旧灰坑', '旧灰坑未熄透、周边踩点者', '人物_FX-RLY_珥薇'),
 ],
 'R03': [
  ('rumor_grazingHG1', '猎场：设陷与放牧轮流使用', '翻起的草皮、界石后的分岔', '未撤的兽夹与陷坑，走熟路也可能踩空', '人物_FX-HNT_珥兰'),
  ('rumor_grazingHG2', '猎场东段，野物饮水处', '水边的蹄印、被啃的树皮', '清晨饮水时最危险', ''),
  ('rumor_grazingHG3', '猎场南段，收草季人多', '晾草架、割过的茬口', '收草时的械斗与误伤', ''),
  ('rumor_wolfHG1', '狼迹：入冬前靠近棚圈', '拖痕、被啃的田界木桩', '狼群护食、夜间围猎', ''),
  ('rumor_wolfHG2', '狼迹：旧猎径上的新爪印', '爪印深浅、风向', '独狼也会扑人', ''),
  ('rumor_mooseHG1', '驼鹿踪迹：灌木被折出新茬', '折枝高度、泥地蹄印', '发情期驼鹿主动冲撞', ''),
  ('rumor_bearHG1', '熊的领地：倒木与抓痕', '树皮抓痕、蜂巢残片', '护崽母熊，正面撞上最危险', ''),
  ('rumor_bearHG2', '熊的领地：山脚果园边', '压塌的篱笆、果核堆', '夜里进园、白天装死无效', ''),
  ('rumor_hornetHive1', '亡蜂巢：蜂群弃巢后无人清理', '烟熏痕、空巢格', '残蜂与新来的野蜂', '人物_FX-HNY_忒曼'),
  ('rumor_homesteadLooted1', '裁缝宅子：被抢空后留下半院布头', '撕开的布匹、翻倒的染缸', '染缸结壳滑倒、原主亲属可能回来', '人物_FX-LOT_绥珥'),
 ],
 'R04': [
  ('rumor_harpyNest1', '哈比巢：崖壁换羽期最凶', '崖缝旧绳扣、巢下白骨与羽毛', '俯冲扑击、记脸追踪', '人物_FX-HRP_妲兰'),
  ('rumor_remoteBastion1', '老城堡：残兵守着一道旧命令', '被摸亮的门栓铜环、后补的墙石', '东墙根塌角、不给通行', '人物_FX-BST_恩岱'),
  ('rumor_remoteBastion2', '固若金汤的堡垒：传言多于实情', '崖下堆积的滚石', '传闻引来的寻宝者', '人物_FX-TRS_谟珥'),
  ('rumor_camp1', '土匪营地：换人频繁', '壕沟、哨位草垫', '哨位伏击与绊索，进营前先看草垫', '人物_FX-CP1_燧珥'),
  ('rumor_camp4', '兵营：关隘换防后的空营', '军旗杆座、被拆的床架', '军械残件与禁令', '人物_FX-CMP_珥泰'),
 ],
 'R05': [
  ('rumor_remoteCatacombs1', '神圣的废墟：守墓教士在祭坛止步', '新挖的土、祭坛下的名单', '塌方道与盗掘痕迹', '人物_FX-CAT_洛珉'),
  ('rumor_leprosy1', '老麻风院：护理者维持最后一间药房', '篱笆上的药罐、井绳的封布', '院内井水不可用、病人不可围观', '人物_FX-LEP_米洛珥'),
  ('rumor_plagueVillage1', '疫村：封门未拆，旧屋尚存', '门上的封条、晒过的药草捆', '疫源未清、游荡者', '人物_FX-PLG_蔻珥'),
  ('rumor_witchHut1', '女巫的住处：村里人夜里绕行', '门口放物石、圈地红果丛', '村民敌意与林中陷阱', '人物_FX-WCH_索妲'),
  ('rumor_ghoulDen1', '食尸鬼巢穴：近坟地', '拖痕、被翻的坟土', '夜行食尸鬼、坟地气味', '人物_FX-GHL_达珥'),
  ('rumor_ghoulDen2', '食尸鬼巢穴：废弃窖口', '窖口结网、散落骨片', '窖内缺氧、出入口狭窄', '人物_FX-GH2_埕珥'),
  ('rumor_rottenWillow1', '烂柳酒馆：据点式酒馆，人来人往', '门口的拴马桩、后院的旧账板', '赌债与帮派换人', '人物_FX-WIL_摩珥'),
 ],
 'R06': [
  ('rumor_abbey1', '亵渎的修院：停用后成为避难处', '钟楼空阶、后墙豁口', '地窖不可擅入、夜里不点灯', '人物_FX-ABY_缇菈'),
  ('rumor_hermitHut1', '药师家：学徒守规矩记账', '晾草分层、门槛外的鞋位', '配药须师父点头', '人物_FX-HUT_珂琳'),
  ('rumor_remoteCrypt1', '英雄陵墓：盗掘者同伴未归', '第二道门的方向、墙上白灰', '墓道回声误导、塌方', '人物_FX-CRP_瑟珥'),
  ('rumor_cave1', '洞穴：山道旁的浅洞', '洞口风、地面苔线', '浅洞也有野兽', '人物_FX-CV1_珞珥'),
  ('rumor_cave2', '洞穴：采药人歇脚处', '药篓残片、熄过的火', '浅洞易被当成近路，雨后洞内积水', '人物_FX-CV2_芩珥'),
  ('rumor_cave3', '三刀会窝点：旧洞被帮派用过', '洞口警戒石、洞内挂钩', '帮派残留的埋伏与挂钩，别碰洞内绳索', '人物_FX-CV3_俉珥'),
  ('rumor_cave4', '野兽洞穴：兽道明显', '爪印、骨堆与蹭秃的树皮', '护崽野兽守在兽道口，退比跑安全', '人物_FX-CV4_佴珥'),
  ('rumor_cave5', '老梣树：树根间的空洞', '树皮刻痕、根系空腔', '根洞积水、蛇', '人物_FX-CV5_栎珥'),
  ('rumor_cave6', '暴雨谷地：雨后成泽', '冲沟、漂来的木片', '暴雨时谷地骤涨，水线比人快', '人物_FX-CV6_洄珥'),
  ('rumor_mine1', '矿洞：旧轨道与塌方段', '轨道锈迹、支撑木', '塌方与岔道迷路，支撑木朽的别进', '人物_FX-MIN_珥德'),
  ('rumor_mine2', '矿洞：停产后的捡拾点', '矿车残件、捡拾者的记号', '支撑木朽坏，矿车轨下沉会崴脚', '人物_FX-MN2_锉珥'),
 ],
}
all_sites = [k for rows in SITES.values() for k, *_ in rows]
inv_sites = [r['key'] for r in inv['rumor_sites']]
assert sorted(all_sites) == sorted(inv_sites), (len(all_sites), len(inv_sites),
                                               set(inv_sites) - set(all_sites), set(all_sites) - set(inv_sites))
changed = set(); generated = {}
def put(rel, t):
    p = V / rel; p.parent.mkdir(parents=True, exist_ok=True)
    t = preserve_foreign(V, rel, t)
    p.write_text(t, encoding='utf-8'); changed.add('design/' + rel); generated['design/' + rel] = sha(p)
def card_id(link):
    m = re.match(r'人物_(FX-[A-Z]+)_', link)
    return m.group(1) if m else ''
for R in REGIONS:
    rel = f"02_世界与地图/特殊地点与野外NPC/地点设计卡_{R['id']}_{R['name']}.md"
    b = (f"---\ntitle: \"地点设计卡_{R['id']}_{R['name']}\"\nid: SITE-{R['id']}\ntype: location-design\nstatus: draft\ncanon: mixed\n"
         f"baseline: \"0.9.4.25-modbranch\"\nupdated: 2026-10-13\ntags: [stoneshard, S95, location]\naliases: []\n---\n\n"
         f"# 地点设计卡_{R['id']}_{R['name']}\n\n所属：[[{R['note']}]]；清点见[[特殊地点与野外NPC清点]]；对白见[[台本_FX_野外人物对白]]。\n\n"
         f"**地貌与生活用途**：{R['terrain']}{R['use']}\n\n"
         f"**入口与安全回程**：{R['entry']}\n\n**固定可观察物**：{R['observables']}\n\n**特殊危险**：{R['dangers']}\n\n"
         f"**服务**：{R['service']}\n\n**原作避让**：{R['avoid']}\n\n"
         '**关联任务与人物**：' + ' · '.join('[[' + l + ']]' for l in R['links']) + '。\n\n'
         '## 逐地点\n\n| 地点 | 用途与生活 | 固定可观察物 | 特殊危险 | 关联 |\n|---|---|---|---|---|\n')
    if R['id']=='R01':
        heading=f"# 地点设计卡_{R['id']}_{R['name']}\n\n"
        b=b.replace(heading,heading+'现地理：灰堤外院 G1（43,37）／塌堤滩 G2（44,38）。\n\n',1)
    if R['id']=='R02':
        heading=f"# 地点设计卡_{R['id']}_{R['name']}\n\n"
        b=b.replace(heading,heading+'现地理：布林东侧河口渡口，F1（本地45,36），河道x45，布林东缘盐车道沿y36通达。曾用名「丹布里西路与渡口」；现文件名与链接已改为「布林东侧河口与渡口」；丹布里仍在布林西南。\n\n',1)
        b=b.replace('aliases: []', 'aliases: [地点设计卡_R02_丹布里西路与渡口]', 1)
    for key, use, obs, danger, link in SITES[R['id']]:
        b += f"| `{key}` {SITE_NAME[key]}（{SITE_EN[key]}） | {use} | {obs} | {danger} | " + (f"[[{link}]]" if link else "—") + " |\n"
    b += ('\n## 边界\n\n- 本卡是设计意图：未定瓦片比例、像素原点、碰撞与运行房间；服务栏为“无”的地点不得新增柜台或奖励。\n'
          '- 逐地点对白由 [[台本_FX_野外人物对白]] 的对应人物承担；同名地点可能多处，具体位置以实地核对为准。\n\n'
          '[[特殊地点设计卡总表]] · [[特殊地点与野外NPC对白扩展计划]] · [[野外NPC口吻与闲谈参照]]\n')
    put(rel, b)
idx = ('---\ntitle: "特殊地点设计卡总表"\nid: SITE-INDEX-S95\ntype: index\nstatus: draft\ncanon: mixed\n'
       'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S95, location]\naliases: []\n---\n\n'
       '# 特殊地点设计卡总表\n\n'
       f"按地域拆分 [[特殊地点与野外NPC清点]] 的 {len(inv_sites)} 个传闻地点：每卡含地域级地貌/用途/入口与安全回程/观察物/危险/服务/原作避让/关联，以及逐地点用途、观察物、危险与人物。"
       '设计意图，不是比例平面或运行房间。\n\n| 地域 | 地点数 | 卡 |\n|---|---:|---|\n')
for R in REGIONS:
    idx += f"| {R['name']} | {len(SITES[R['id']])} | [[地点设计卡_{R['id']}_{R['name']}]] |\n"
idx += ('\n## 口径\n\n- 服务一律不新增：标“无固定服务”的地点只提供观察、口信与去路指引。\n'
        '- 安全回程均给出可认的锚点（灯、旗、基座、药棚），不是自制传送；实际通达待制作核对。\n'
        '- 关联人物为 S94 野外人物；关联任务与聚落沿用既有台本与地域卡，不新增前置。\n\n'
        '[[特殊地点与野外NPC对白扩展计划]] · [[特殊地点与野外NPC清点]] · [[台本_FX_野外人物对白]]\n')
put(IDX, idx)
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S95特殊地点设计卡（当前登记）\n\n'
           f"[[特殊地点设计卡总表]]：{len(inv_sites)} 个传闻地点按 6 个地域拆成设计卡，逐地点含用途/观察物/危险/关联；地域级含入口与安全回程、服务、原作避让。设计意图，非比例平面；服务不新增、奖励不新增。")
t = (V / PLAN).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
put(PLAN, t2)
own = ROOT / 'research/site-cards-note-hashes.json'
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
rule = ('\n<!-- SITE-CARDS-S95:BEGIN -->\n2026-10-13 S95：用户要求扩充特殊地点内容。'
        f'44个传闻地点按6个地域拆成地点设计卡（入口/安全回程锚点、观察物、危险、服务=无、原作避让、逐地点关联），入口design/02_世界与地图/特殊地点与野外NPC/特殊地点设计卡总表.md。'
        '设计意图，未定比例/碰撞/运行房间；不新增服务与奖励、不新增前置。运行Validate-SpecialSiteCards.py及既有检查；不部署游戏包。\n<!-- SITE-CARDS-S95:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- SITE-CARDS-S95:BEGIN -->.*?<!-- SITE-CARDS-S95:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- SITE-CARDS-S95:BEGIN -->.*?<!-- SITE-CARDS-S95:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/02_世界与地图/特殊地点与野外NPC/特殊地点设计卡总表.md', '入口 [特殊地点设计卡总表](design/02_世界与地图/特殊地点与野外NPC/特殊地点设计卡总表.md)'), encoding='utf-8')
print(json.dumps(dict(regions=len(REGIONS), sites=len(all_sites), notes=len(generated)), ensure_ascii=False))
