"""Author and render the S93 original field-NPC reading: per-slot coverage,
voice summaries and short examples. Design vault only; no dialogue stored."""
from pathlib import Path
import json, hashlib, re
from NotePreserve import preserve_foreign
ROOT = Path(__file__).resolve().parents[2]; V = ROOT / 'design'
MARK = 'NPC-READING-S93'
CARD = '01_原作基线/野外NPC口吻与闲谈参照.md'
PLAN = '11_管理/特殊地点与野外NPC对白扩展计划.md'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads((ROOT / p).read_text(encoding='utf-8-sig'))
inv = read('research/original-dialogue-inventory.json')
rows = {}
for fam in ('greeting', 'chat'):
    for e in inv['families'][fam]['entries']:
        spk = e.get('speaker')
        if not spk: continue
        rows.setdefault(spk, {'greeting': [], 'chat': []})[fam].append(e['index'])
slots = sorted(rows)

GROUPS = [
 dict(id='gossip', title='通用乡谈池（无角色槽）', tokens=[''], extra_slots=['(无槽位)'],
      summary='乡民闲谈池：同一条由城镇条件（Osbrook/Mannshire/Denbrie/Brynn）筛用，主题是战时日常——瘟疫、饥荒、征兵、路匪、休战不可信、外迁尼斯特拉/斯卡迪亚、矮人与精灵来客、雇佣兵变多、物价与旧集市回忆。'
              '讲述结构固定为「听说一件事 → 补充细节 → 感慨」，文本用 # 分段，可整条替换；恐怖与迷信（半夜马蹄、墓穴、火女巫、中冬不祥）常作结尾。',
      patterns=['长句叙事，# 分三段：引子／细节／感慨', '城镇限定决定可播条目，不改文本',
                '每条约 40–90 字，多用第一人称与“我听说/我有个朋友”', '迷信与传闻收尾，不给结论'],
      examples=[dict(index=29958, zh='我听人说再过一阵子，所有男的，只要身强力壮、没有残疾，就都得入伍、上战场打仗。'),
                dict(index=30010, zh='这些日子是真苦……我印象里是从来没见过。')]),
 dict(id='guard', title='守卫与军官', tokens=['guard', 'guard_SI', 'guard_sergeant', 'officer', 'captain', 'soldier'],
      summary='守城人的实际恐惧：夜巡城墙外最怕（黑、安静、怀疑有土匪或哈比）、装备先给前锋、执法快而粗（偷窃即坐牢）、对矮人与法师不信任、墓穴与不死生物的恐惧远超土匪。'
              '军官短促命令式；布林卫兵会提迪·贝罗与围城旧事；奥斯布鲁克军官先盘问来意。',
      patterns=['挑战式短句问候（“看什么呢？”“干什么的？”）', '长句只在独白式闲聊，语气粗直、少修饰',
                '把城市名与官署（城联/王廷/前锋）挂在嘴边', '对玩家雇佣兵身份既鄙视又羡慕'],
      examples=[dict(index=30002, zh='我不怕土匪，他们是恶人，但起码还是人，那些不死的玩意儿就不是这回事了。'),
                dict(index=30240, zh='阿诺·迪·贝罗万岁！')]),
 dict(id='traders', title='商贩与钱庄', tokens=['merchant', 'merchant_denbrie', 'merchant_fair', 'food_trader', 'food_trader_m', 'food_trader_fair', 'vegetable_trader', 'vegetable_trader_m', 'fruit_trader', 'fruit_trader_m', 'cheese_trader', 'wine_trader', 'grocer', 'dealer', 'trader_fjall', 'trader_jibey', 'trader_nistra', 'trader_skadia', 'fence', 'loanshark', 'ragpicker', 'ragpicker_tott', 'npc_banker01', 'npc_banker02', 'npc_jeweller01gq', 'npc_jeweller02gq'],
      summary='生意经与提防：假冒金币要咬一口、先收钱再雇护卫、亏本也要卖、大城市诱惑多但乡下相亲、想搬去布林、女儿婚事、看人下菜（滑头过得更好）。'
              '吆喝式问候占多数；收赃人（ragpicker/fence）在烂柳语境下戒备更重；尼斯特拉与弗约商贩夹外语短句。',
      patterns=['吆喝短句做问候（“新鲜奶酪！”“卖水果了！”）', '闲聊夹算计与自嘲，常以“这年头”开头',
                '带一句生活常识（咬金币、雇车、防蘑菇）', '外语商贩保留音译短语再切奥尔多语'],
      examples=[dict(index=30028, zh='不论谁给你钱，第一件事，先咬一下，这年头假币泛滥。'),
                dict(index=30027, zh='我现在干的都是亏本买卖。这年头，没几个有钱的。')]),
 dict(id='craftsmen', title='匠人与作坊', tokens=['smith', 'carpenter', 'tailor', 'butcher', 'baker', 'tanner', 'miller', 'stableman', 'printer', 'ralph_brother01', 'ralph_brother02', 'ralph_brother03'],
      summary='手上活与抱怨：好铁贵、只够糊口；军械订单挤掉定制活（“别想我给你单做”）；木匠骂奥达霸道、念伊德斯木材、羡慕布鲁克酒馆生意；屠户听曼郡亲戚讲城联与摄政王妃的传言；马夫吹自己的母马。'
              '作坊问候一律问“要买还是要修”。',
      patterns=['问候即业务（修东西吗／要肥一点的）', '闲聊=行业视角的政治与价格', '对雇佣兵摆脸色但给折扣口风',
                '短句为主，偶尔一段手艺自述'],
      examples=[dict(index=30017, zh='我们村长，奥达，器量不大，还霸道。跟他打交道，机灵一点。'),
                dict(index=30023, zh='这年头好铁可不便宜，就算这样，我也才算勉强能挣够吃的。')]),
 dict(id='tavern', title='旅店与仆人', tokens=['innkeeper', 'innkeeper_TP', 'innkeeper_GS', 'innkeeper_CH', 'innkeeper_DW', 'innkeeper_SI', 'hostess', 'hostess_GS', 'hostess_SI', 'hostess_CH', 'hostess_TP', 'brewer', 'servant', 'servant_CH', 'maid', 'maid_SI', 'maid_GS', 'apprentice_inn'],
      summary='围着吧台的生活：老板催点单、抱怨人手不够；仆人知道城里的享乐地（忘忧坊）与贵族习惯，但只能远远看着；精灵绸缎是稀罕物，半夜替太太找精灵青柠。'
              '问候先问“喝啤酒还是住店”。',
      patterns=['服务性问候，先问需求', '闲聊=内部人视角的阶层差（老爷吃剩的救了我）', '对奢侈品的羡慕与距离感'],
      examples=[dict(index=29909, zh='管他的呢，我这都忙不过来，哪有工夫管那些事儿。'),
                dict(index=30285, zh='干什么？没看见我做菜呢吗？')]),
 dict(id='sailor', title='水手与渔民', tokens=['sailor', 'fisherman'],
      summary='海员的世界：青铜群岛老王驾崩、港口要重开、迪·贝罗捞好处；接舷战与海防；回港先去忘忧坊剪头泡澡；远航地名（尼斯特拉、斯卡迪亚、尤哈拉、诺尔海姆）；海盗点火诱船撞礁的传说。'
              '渔民说今年海太静、鱼多得反常。',
      patterns=['地名清单是海员标志（一串异国名）', '把海上规矩与陆地对比', '对陆地人语气带优越与怜悯'],
      examples=[dict(index=29923, zh='船上这碗饭吃起来可不容易。船跟船要是打起来了，谁强谁弱一眼就能看出来。'),
                dict(index=30206, zh='我跟你说啊，今年海里太平静了，平静得不大对劲。')]),
 dict(id='worker', title='码头工与杂役', tokens=['worker', 'delivery'],
      summary='城市底层经验：白天睡觉会被抓、走路打盹会栽进海里；父亲喝醉与否决定挨不挨揍；围城后全城重建的自豪；旱港听海员吹牛到想出海；琢磨自己也去当雇佣兵（“搞破坏还有钱拿”）。',
      patterns=['生活规矩式建议（别在码头打盹）', '自述式家史与酒馆名（三口锅）', '对雇佣兵又羡又酸'],
      examples=[dict(index=29932, zh='雇佣兵，感觉我们布林这个自由城邦怎么样？是不是根本看不出来这地方半年前刚被王廷围过城？'),
                dict(index=29930, zh='大白天睡觉，谁看见都不会喜欢，到处瞎溜达还有可能坐牢。')]),
 dict(id='townsfolk', title='市民、乡民与市井', tokens=['townsman', 'townswoman', 'peasant', 'elder', 'old_woman', 'newsboy', 'herald', 'jester', 'minstrel', 'mourner', 'undertaker_RC', 'daughter', 'kenricks_son', 'seeker', 'limper', 'lowcrey'],
      summary='城里人讲三件事：钱（通胀、宝石保值、佛·诺姆斯放贷人）、雕像（埃特伯特无头像）、排外（精灵占城、“登瓦尔说得对”）。'
              '乡民问“你觉得我们熬得过去吗”；报童与传令官吆喝；小丑、吟游诗人、哭坟人各有固定动作描写。',
      patterns=['市民闲聊=城市八卦＋物价＋排外', '哭坟/旁观类问候用动作星号描写（*她定定地盯着那个坟墓*）',
                '乡民更短更直（“你觉得我们熬得过去吗？”）', '布林排外句与精灵组对读，不能照抄进Mod'],
      examples=[dict(index=29941, zh='铸币广场的雕像看见没有？是不是纳闷头怎么没了？'),
                dict(index=30316, zh='你觉得我们熬得过去吗？')]),
 dict(id='patrician', title='贵族与官面', tokens=['patrician', 'damsel', 'emissar', 'intendant', 'official', 'landwaiter'],
      summary='居高临下：先要求摘帽整衣；不谈闲话；抱怨治安（“连老楼角角落落都有当兵的看着”）；把玩家当无赖直接喊卫兵。'
              '官面（intendant/official/emissar）短促公事化，先问“什么事”。',
      patterns=['命令式礼仪要求', '拒绝闲聊并指明“去别处问”', '把玩家身份直接判成可疑（“是不是密探？”）'],
      examples=[dict(index=29937, zh='跟我这种身份的人说话之前，先把头上戴的东西摘了，再整理整理你的衣服。'),
                dict(index=29938, zh='我可没工夫聊闲天，要是想听人闲扯，不如去骚扰市场上那些卖东西的。')]),
 dict(id='guild', title='新会匠人与学徒', tokens=['master', 'apprentice'],
      summary='布林新会（行会）之争：手艺好坏不再决定收入、按件计酬抹平差距；有人说方便有活有钱，有人嫌规矩多；学徒累到只想下班去三口锅；督工会罚钱。'
              '还夹着对精灵首饰的工艺比较（“给我材料我也能做”）。',
      patterns=['师徒两人合写一条，立场不同', '把制度争论落在一日三餐与罚款上', '问候短促（“别干扰我了，行不行？”）'],
      examples=[dict(index=30183, zh='别干扰我了，行不行？要是让督工看见了，肯定说我偷奸耍滑、罚我钱，那我这一天就白干了。'),
                dict(index=30184, zh='我告诉你，今天下了班我就去三口锅，喝他个一醉方休。')]),
 dict(id='drunkard', title='酒鬼', tokens=['drunkard'],
      summary='酒鬼自成一格：问候用动作描写（“*老酒鬼身上臭气熏天，熏得你下意识地退了一步*”），台词用连字符做口齿不清（“有缘千-里来相见”），主题只有酒与胡话。'
              '布林酒鬼只剩嘿嘿笑；曼郡酒鬼还在纠结“你现在……知道了，对吧？”。',
      patterns=['口吃用连字符切字，不写整句错字', '问候先给气味/神态动作描写', '闲谈只有酒、天气与胡话'],
      examples=[dict(index=30250, zh='有缘千-里来相见，咱们赫-喝点啥庆-应祝一下，咋样？'),
                dict(index=28299, zh='*老酒鬼身上臭气熏天，熏得你下意识地退了一步*')]),
 dict(id='care', title='药师、治疗师与巫医', tokens=['herbalist', 'healer', 'alchemist', 'witch', 'occultist', 'occultist2', 'theologist', 'surgeon'],
      summary='草药变多（“土里浸透了血”）、蘑菇警告（有一家人夏天下了葬）、捕兽夹与蝮蛇提醒；治疗师想收学徒传本事；炼金术被卫兵当笑话；女巫与神秘学者说谜语式短句。',
      patterns=['专业建议夹在问候里（“用车前草没有？”）', '警告用具体案例（谁家死了人）', '神秘系用箴言短句（“循此苦旅，以达星辰”）'],
      examples=[dict(index=30020, zh='在这个地方摘蘑菇千万小心……我认识一家人，特别爱采蘑菇，吃蘑菇……夏天刚下了葬。'),
                dict(index=30021, zh='我快干不动了……得收个徒弟，把我的本事传下去了。')]),
 dict(id='military', title='雇佣兵、匪帮与囚徒', tokens=['mercenary', 'merc_SI', 'merc_comp', 'brigand', 'brigand_leader', 'raider', 'convict', 'bodyguard', 'bouncer'],
      summary='同行的冷淡与敌意：井水不犯河水、祝你好运、撞上同行真倒霉；匪帮与看守短句驱逐（“滚蛋。”“让开！”）；囚徒自嘲（“来看幸灾乐祸的吗？”）。'
              '雇佣兵之间不结盟，各接各的契据。',
      patterns=['问候即拒人（滚蛋／让开／在这儿寻摸什么呢）', '同行识别句（“也是来找活干的？”）', '匪帮按据点（烂柳）给口风'],
      examples=[dict(index=30136, zh='看什么看？'),
                dict(index=30193, zh='我得站岗，想聊天去那边找科隆去。')]),
 dict(id='church', title='教会与学院', tokens=['priest_RC', 'hierodidact', 'monk', 'pilgrim', 'scribe', 'jurist', 'student'],
      summary='信仰与学问：教士问候带祝福（“导引圣手令你我重逢”）；朝圣者给具体忠告（进旧修院先祷告、别下地窖）；教授自报家门（“我是法学系的厄尔富特·佛·勒柯里”）；'
              '学生讲神学难、法学是女王（“凡人皆狼”）、围城后医学院缺尸体、大学文凭保衣食、曼恩与布林谁更开化。',
      patterns=['祝福式问候，主语是圣主/圣手', '学者自报姓名与院系', '把学问争论落到职业前途与尸体供给'],
      examples=[dict(index=30235, zh='旅人，愿圣主保佑你。'),
                dict(index=29946, zh='法学是各个学科的女王，无法无以立国……“凡人皆狼”。')]),
 dict(id='elves', title='精灵组（原始复合槽）', tokens=['elf_barker', 'elf_guard', 'elf_woman', 'elf_merchant', 'elf_noble'],
      extra_slots=['elf_noble', 'elf_noble, elf_guard', 'elf_noble, elf_guard, elf_woman', 'elf_guard, elf_woman', 'elf_barker', 'elf_merchant'],
      summary='碧罗商馆的封闭感：贵族直接挡人（“这里是碧罗商馆，你不得入内”“走，我不说奥尔多”），守卫用音译精灵语短句再切奥尔多语，商人招呼“阿巴依\'阿迈德”；'
              '也有乡愁句（“要是能回哈尊就好了”）。',
      patterns=['精灵语音译短句 + 奥尔多语', '贵族以门第挡人，仆人阶层才肯闲聊', '乡愁与看人下菜并存'],
      examples=[dict(index=30213, zh='陌生人，这里是碧罗商馆，你不得入内。'),
                dict(index=30209, zh='唉……要是能回哈尊就好了……')]),
 dict(id='field', title='野外行当', tokens=['hunter', 'hunter_rut', 'gatherer', 'forager', 'forager_f', 'trapper', 'shepherd', 'huntress'],
      summary='靠山吃山：猎人说这一带野物变多、希望每趟都有收获；采集者报草药浆果丰收；牧羊人无聊（“天天赶这些羊，快无聊死了”）。'
              '野外问候短，多在据点（烂柳）出现。',
      patterns=['收获量是话题（今年多／少）', '对陌生人短句（“什么事儿？”“你好。”）', '把安全提醒当闲聊（捕兽夹、蝮蛇）'],
      examples=[dict(index=30287, zh='天天赶这些羊，快无聊死了……'),
                dict(index=27357, zh='这个是维伦说的那个修道院吗？那个钟楼上看这片林子，景致肯定差不了……')]),
 dict(id='special', title='有名字的常驻人物', tokens=['darrel', 'fogt', 'wigmar', 'idet', 'kenrick', 'ralph_brother', 'npc_', 'seeker'],
      summary='原著常驻角色（达雷尔、福格特、维格玛、伊黛特、肯里克父子等）在问候层已带完整性格：达雷尔给新会干活但话里留旧事；福格特是催货督工（“天黑之前赶不完，耶昂非得扒了我的皮”）；'
              '伊黛特用动作描写拒绝交谈；肯里克之子骂城联并护着父亲。逐场景台词属 scene 条目，未在本页展开。',
      patterns=['常驻人物问候即人设（督工催货／老太婆不说话）', '剧情线索只给半句（“外边见过什么……算了”）', '护卫家人的短句带刺'],
      examples=[dict(index=30139, zh='给新会干活儿，苦是苦了点儿，不过这城里起码不用担心嗝屁。'),
                dict(index=28532, zh='天黑之前要是赶不完这些，耶昂非得扒了我的皮不可。别闲扯了，抓紧干活儿！')]),
]
# ---- assign every slot ----
def assign(slot):
    toks = [t.strip() for t in slot.split(',')] if slot else ['']
    for g in GROUPS:
        if any(t in g['tokens'] for t in toks): return g['id']
    return 'other'
assignment = {s: assign(s) for s in slots}
unassigned = sorted(s for s, g in assignment.items() if g == 'other')
def idx_list(slot):
    r = rows[slot]; return dict(greet=r['greeting'], chat=r['chat'])
# ---- S98: npc functional/behavior tag groups and scene-structure finding ----
npc_entries = inv['families']['npc']['entries']
unique_keys = sorted({e['key'] for e in npc_entries})
NPC_TAGS = [
 dict(id='utility', title='工具句', rx=r'^npc(?:Trade|Talk|Found|_lowhp)$',
      note='占位句用 $1/$2 代换说话人，如“$1和$2做起了买卖。”；是系统播报，不是角色台词。'),
 dict(id='bands', title='声望档行为集（守卫/乡民）', rx=r'^npc_(?:guard|peasant)_(?:respect|amity|admiration|trueneutral|neutral|dislike|hatred)$',
      note='原作为守卫与乡民各设 7 档（respect/amity/admiration/trueneutral/neutral/dislike/hatred）行为集；文本为空，行为在引擎侧。Mod 的[[城镇声望与信任系统]]用 −2..+2 五档，不照搬 7 档，但保留“档位改变行为而非只改价格”的原则。'),
 dict(id='crime', title='治安反应', rx=r'^npc_crime[A-Za-z0-9_]*$',
      note='盗窃、斗殴、杀人、报警等治安事件反应槽；说明原作把犯罪反馈也挂成标签而不是写死在每个NPC里。'),
 dict(id='state', title='状态与天气', rx=r'^npc_rain\d$|^npc_(?:ambush|nightmares|pest)$',
      note='天气（rain1–3）与状态（遇袭、噩梦、疫病）触发不同闲话；Mod 的野外人物条件回访沿用同一思路，但只按台本条件，不新做天气系统。'),
 dict(id='variants', title='收尾与转译变体', rx=r'^npc_.*_(?:translated|end)$',
      note='多数角色与商贩都带“收尾（_end）/转译（_translated）”变体，说明原作对结束语与异国商贩双语准备了独立槽位。'),
 dict(id='role_idle', title='角色闲话标签', rx=r'^npc_[a-z][a-z_]*$',
      note='按角色或场所命名的闲话槽（工人、卫兵、商人、酒馆、讲学者、市民、军士、乡民等）；文本在引擎侧，说明原作把“谁说闲话”做成可挂标签的槽位。'),
]
for g in NPC_TAGS: g['keys'] = []
for k in unique_keys:
    for g in NPC_TAGS:
        if re.match(g['rx'], k): g['keys'].append(k); break
for g in NPC_TAGS: g['count'] = len(g['keys'])
assigned = sum(g['count'] for g in NPC_TAGS)
assert assigned == len(unique_keys), (assigned, len(unique_keys),
                                      [k for k in unique_keys if not any(k in g['keys'] for g in NPC_TAGS)])
SCENE_FINDING = ('场景族 326 条的键可枚举（scene_<角色>_<题材>，如 scene_darrel_oldcaravan），但条目槽位只含数字标记（如 20、25），'
                 '文本、选项与显示条件不在字符串表内，而在引擎脚本侧。按本库边界（只做只读接口核对、不保存反编译源码），场景级逐条对读到此为止：'
                 '本页给键与计数，分支与跳转需在制作阶段按实际场景核对。')
out = dict(date='2026-10-13', source='research/original-dialogue-inventory.json',
           scope='S93/S98 field-NPC reading: slot coverage, per-group voice summaries, short examples with locators, npc behavior tags and scene-structure finding; scene text and npc tag text live engine-side and are not read here',
           slots=len(slots), groups=[dict(id=g['id'], title=g['title'], slots=sorted(s for s, gid in assignment.items() if gid == g['id']),
                                          summary=g['summary'], patterns=g['patterns'], examples=g['examples']) for g in GROUPS],
           npc_tags=[dict(id=g['id'], title=g['title'], note=g['note'], count=g['count'], keys=g['keys']) for g in NPC_TAGS],
           scene_finding=SCENE_FINDING,
           unassigned=unassigned)
(ROOT / 'research/original-npc-reading.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
# ---- render card ----
n = ('---\ntitle: "野外NPC口吻与闲谈参照"\nid: SRC-NPC-READING-S93\ntype: source\nstatus: draft\ncanon: mixed\n'
     'baseline: "0.9.4.25-modbranch"\nupdated: 2026-10-13\ntags: [stoneshard, S93, source, dialogue]\naliases: []\n---\n\n'
     '# 野外NPC口吻与闲谈参照\n\n'
     '本页是[[特殊地点与野外NPC对白扩展计划]]第4步的阅读结果：把原版问候／闲谈（greeting 446、chat 125）按说话人槽归组，记录各组的口吻、主题与可复用结构，并给必要短例与 STRG 定位；'
     '另含 npc 227 条行为槽的分组与场景族结构结论（S98）。对白全文不入库，短例均 ≤ 48 字。\n\n'
     f'覆盖：{len(slots)} 个说话人槽全部归组（未归组 {len(unassigned)}）。槽位-索引清单在 `research/original-npc-reading.json`。\n\n'
     '> [!info] 用法\n> 新写野外／闲谈对白时：先定角色槽与城镇条件，再按本页口吻要点写；不复用原句，只沿用结构与题材；同一事实在不同槽位要给不同解释（守卫的版本、商贩的版本、乡民的版本）。\n\n')
for g in GROUPS:
    gslots = sorted(s for s, gid in assignment.items() if gid == g['id'])
    shown = gslots or g.get('extra_slots', [])
    if not shown: continue
    greet = sum(len(rows[s]['greeting']) for s in gslots); chat = sum(len(rows[s]['chat']) for s in gslots)
    tag = '' if gslots else '（原始复合槽，未计入72槽直方图）'
    n += f"## {g['title']}{tag}\n\n**槽位**：" + '、'.join('`' + (s or '(空)') + '`' for s in shown) + (f"（问候 {greet}、闲谈 {chat}）\n\n" if gslots else '\n\n')
    n += g['summary'] + '\n\n**可复用结构**：\n\n' + '\n'.join('- ' + p for p in g['patterns']) + '\n\n**短例**：\n\n'
    for ex in g['examples']:
        n += f"- 「{ex['zh']}」（`{ex['index']}`）\n"
    n += '\n'
if unassigned:
    n += '## 未归组槽位\n\n' + '、'.join('`' + s + '`' for s in unassigned) + '\n\n'
n += ('## 功能与行为条目（npc 227）\n\n'
      '这 227 条不是台词，而是行为槽：工具句、按角色/场所的闲话标签、声望档行为集与状态/天气触发。文本在引擎侧，键名本身说明了原作的挂载方式。\n\n'
      '| 组 | 条数 | 样例键 | 说明 |\n|---|---:|---|---|\n')
for g in NPC_TAGS:
    sample = '、'.join('`' + k + '`' for k in g['keys'][:3]) if g['keys'] else '—'
    n += f"| {g['title']} | {g['count']} | {sample} | {g['note']} |\n"
n += (f"\n## 场景族的结构结论\n\n{SCENE_FINDING}\n\n")
n += ('## 未核与边界\n\n- 本页只读问候／闲谈；scene 326 条与 npc 227 条的文本、选项与条件在引擎侧，字符串表只给键、计数与数字标记（S98 结论）。\n'
      '- 槽位是引擎侧说话人标记，不等于具名NPC；复合槽位（“a, b, c”）表示共用池，不代表人物关系。\n'
      '- 短例只作语气定位，不能整句搬进Mod；Mod新写对白须自证原创并守各台本既有边界。\n\n'
      '[[特殊地点与野外NPC对白扩展计划]] · [[特殊地点与野外NPC清点]] · [[原作剧情与对话系统参照]] · [[台本编写规则与对白口径]] · [[城镇声望与信任系统]]\n')
p = V / CARD; p.parent.mkdir(parents=True, exist_ok=True)
p.write_text(preserve_foreign(V, CARD, n), encoding='utf-8')
changed = {'design/' + CARD}; generated = {'design/' + CARD: sha(p)}
# ---- plan block with incoming link ----
a = f'<!-- {MARK}:BEGIN -->'; z = f'<!-- {MARK}:END -->'
summary = ('## S93野外NPC对白阅读（当前登记）\n\n'
           f"[[野外NPC口吻与闲谈参照]]：原版问候446/闲谈125按 {len(slots)} 个说话人槽归为 {len(GROUPS)} 组，逐组记口吻、主题、可复用结构与短例定位；对白全文不入库，scene与npc功能句留待下一步。")
plan_rel = PLAN
t = (V / plan_rel).read_text(encoding='utf-8-sig')
nb = a + '\n' + summary + '\n' + z
t2 = re.sub(re.escape(a) + '.*?' + re.escape(z), lambda _: nb, t, flags=re.S) if a in t else t.rstrip() + '\n\n' + nb + '\n'
t2 = preserve_foreign(V, plan_rel, t2)
(V / plan_rel).write_text(t2, encoding='utf-8')
changed.add('design/' + plan_rel); generated['design/' + plan_rel] = sha(V / plan_rel)
own = ROOT / 'research/npc-reading-note-hashes.json'
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
rule = ('\n<!-- NPC-READING-S93:BEGIN -->\n2026-10-13 S93/S98：用户要求扩充特殊地点与野外NPC对白。'
        'research/original-npc-reading.json 把原版问候446/闲谈125按说话人槽归组（全槽覆盖）并逐组给口吻/主题/结构/短例定位；'
        'S98 增 npc 227 条行为槽分组（工具句、声望7档行为集、角色闲话标签、状态天气、商人变体）与场景族结论（scene 326 键可枚举、文本与分支在引擎侧）。'
        '入口design/01_原作基线/野外NPC口吻与闲谈参照.md。对白全文不入库、短例≤48字；不部署游戏包。\n<!-- NPC-READING-S93:END -->\n')
for p in [ROOT / 'CHANGELOG.md', V / 'AGENTS.md']:
    t = p.read_text(encoding='utf-8-sig'); t = re.sub(r'\n<!-- NPC-READING-S93:BEGIN -->.*?<!-- NPC-READING-S93:END -->\n', '', t, flags=re.S)
    p.write_text(t.rstrip() + '\n' + rule, encoding='utf-8')
p = ROOT / 'CHANGELOG.md'; t = p.read_text(encoding='utf-8-sig')
t = re.sub(r'\n<!-- NPC-READING-S93:BEGIN -->.*?<!-- NPC-READING-S93:END -->\n', '', t, flags=re.S)
p.write_text(t.rstrip() + '\n' + rule.replace('入口design/01_原作基线/野外NPC口吻与闲谈参照.md', '入口 [野外NPC口吻与闲谈参照](design/01_原作基线/野外NPC口吻与闲谈参照.md)'), encoding='utf-8')
print(json.dumps(dict(slots=len(slots), groups=len(GROUPS), unassigned=unassigned), ensure_ascii=False))
