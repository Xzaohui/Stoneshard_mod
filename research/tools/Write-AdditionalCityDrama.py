"""Render S78 cast cards and review of the authored Aldwynn scenes."""
from pathlib import Path
import json,hashlib,re
from NotePreserve import preserve_foreign
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));cast=m['dramatic_casts']['ALD'];qs=[q for q in m['quests'] if q['city']=='ALD']
hp=ROOT/'research/aldwynn-generated-note-hashes.json';hashes={}
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=h:raise SystemExit('Preserve/reconcile edited S78 note: '+rel)
def wl(p):return '[['+Path(p).stem+']]'
def front(title,ident,kind):return f'---\ntitle: "{title}"\nid: {ident}\ntype: {kind}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, aldwynn, dialogue, S78]\naliases: []\n---\n\n# {title}\n\n'
def write(rel,b):
 b=preserve_foreign(V,rel,b)
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(b,encoding='utf-8');hashes['design/'+rel]=hashlib.sha256(p.read_bytes()).hexdigest()
def uses(q,key):return any(key==who for s in q['dramatic_scenes'] for who,_ in s['lines']) or any(key==who for pairs in q['dramatic_followups'].values() for who,_ in pairs) or any(f['speaker']==key for f in q['dramatic_feedback'])
for key,a in cast.items():
 if a['existing']:continue
 b=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
 for label,field in [('稳定ID','id'),('工作','role'),('所求','desire'),('所怕','fear'),('口吻','voice'),('可能弧线','arc')]:b+=f'**{label}**：{a[field]}\n\n'
 b+='身份与经历全部Mod原创；所属[[聚落_ALD_奥尔德文]]。关联：'+' · '.join(wl(q['file']) for q in qs if uses(q,key))+'\n\n'
 b+='同一身体按本人日常位置和实际约见移场，不在每个任务各生一个。只讲亲历、准用本案材料或已收有限回执，不从关联链接得知全部剧情。拒绝、死亡、保密与缺席优先；未结案不自动表态，已结案不重选或反复领同项款。\n\n[[奥尔德文人物对白与交叉演出审查]] · [[空间_ALD_奥尔德文]] · [[城市篇章与跨区域任务网]]\n'
 write(a['file'],b)
b=front('奥尔德文人物对白与交叉演出审查','QA-ALDWYNN-DRAMA-S78','narrative-audit')
b+='本轮将奥尔德文主章与六条支线从S63三问素材深化为逐人对白。源research/aldwynn-drama.json与aldwynn-feedback.json；更新前备份backups/city-drama-20261012-s78。设计阶段，未改游戏包与存档。\n\n'
b+='## 地域特色和原作避让\n\n奥尔德文以金工护甲和宗教分歧的地方生活为基础：明亮外壳、被藏起的衬层与人的功劳；仪式秩序、真出资与真正许可并不等同。这里不写现代全城陷落、王宫布局、继承人、神迹判决或进口限制已废止。既有来源范围见[[城市设计与原作避让审查]]，全部新增事件和人物仍是原创。\n\n'
b+='本案广告均为手绘招贴，伤像为受准的手绘摹图，不引入摄影或现代镜头。S63旧方法文字中的伤照仅作历史术语保留，当前演出按此口径。\n\n'
b+='## 当前七案\n\n|任务|场次|原方法|早／晚回执对|\n|---|---:|---:|---:|\n'
for q in qs:b+='|'+wl(q['file'])+f"|{len(q['dramatic_scenes'])}|{len(q['routes'])}|{len(q['dramatic_feedback'])}|\n"
b+='\n合计21场、15种原方法、32条既有回执。原314条关系、NE/N17、奖励所有者、任务地点和地理stages均保留；S78 dramatic_scenes才是奥尔德文当前对白。effects旧receiver是S63示意人物，当前演出说话者以本案dramatic_feedback.speaker为准，不能拿旧摘要配新头像。\n\n'
b+='## 人物互相改变什么\n\n|关系|选择与真实代价|不会自动发生的和解|\n|---|---|---|\n|赫莲／埃墨／索芮|壳真有技术，补针真救过工艺，但旧印、遮掩及赶工分别认责；开放失独认证，分散核验慢，赞助封存留下监督缺口|好作品不证明好人，索芮拒露手也不等于她放弃救济|\n|芬珂／科纳|代号公开保来源，家门各自准；私存少订单是本人选择，不是家属替她说没有野心|科纳仍可不接她的新公开单，不能因此撤她署记|\n|司诺／伊榕／穆柯|分开仪式真多一班费用，简葬保死者未知意愿，亲属可另留纪念|不把同款、简葬或空椅解释为全家同信|\n|奈汀／索芮|纯赠须实际撤免责广告与真交付；奈汀可撤赠，索芮可选有限普通替代|受助不替赞助者洗责任，拒礼也不成为普通服务惩罚|\n|齐勒／布娅／泊恩|限定历史会少票，退款会少现钱；布娅自己转述的假消息也需更正|退款不抹掉已经受恐惧影响的人，不证明远路安全|\n|奇恩／萝铎／维安|如实申报可能拒收，旧件有限性能和校验费；驿主不借名真失生意|图纸许可不是货物准入，空箱不变成库存|\n\n'
b+='## 同一人的位置和知情\n\n赫莲默认修院或工场，埃墨默认白缝工艺现场，司诺默认礼仪外庭；芬珂、泊恩、萝铎默认各自聚落。索芮默认缓息屋／普通护理地点，只在自愿约见时进试装场或会馆；CS05白缝场不生成她，核脱体样，不靠再现伤害取证。她是成人试装学徒，本案死者是另一位原创家属，不用同一个身体同时死亡、受礼和索赔。\n\n科纳默认白缝联络檐，伊榕与穆柯在约定送别时段会面；齐勒默认旧墙停歇亭，布娅随本次游约自选去留；奈汀默认有限会馆，奇恩默认验箱廊，维安默认空试架。移动按一个实际会面表，不克隆演员；人不在时可看固定物、问下一班、独立有限代理或离开。每句必须有该人的亲历／授权来源，先看样不会自动获名字或伤像许可。\n\n'
b+='## 任务顺序如何影响后续\n\n12条支线→主章回应分别承认署记、送别、有限赠与、旧墙范围、工伤与真实物流；18条主章→支线回应按open／distributed／seal分别写，不能把旧封存用一场新对话抹掉。另有CX11缩产料量与IN-ALD旧案先例两条传入；主章往布林学徒支线的既有接货回应沿S76稿，接收者只知回执限定事实。\n\n未收到任何回执也可本地独立核验。前后任务同项已付、已占样件和工时不可再发一份；新班次另外核预算。已结案只改未来许可、报价、见面与展示，不重选resolve、不回滚伤害或paid、不解冻N17。取消菜单不作拒全案，预览不写完成；实际处置＋确认后才结本案。\n\n'
b+='## 逐案审查与仍待细化\n\n赠与a路线：若奈汀实际撤赠，不能演纯赠交付完成，转回普通替代预览或保pending，不强夺赠具。封存路线：只封各作者本次准用的来源，不拿赞助条款封独立申诉；旧控制仍存，后来开放本案资料须真实可执行。葬务b路线：仍需实际有权者同意，不以NPC死亡制造简葬共识。工伤两路线：同项主章已付扣清，不用拒拍照给患者补一个拒援助的状态。\n\n'
remaining=sum('dramatic_scenes' not in q for q in m['quests'])
b+=f'当前布林11篇与奥尔德文7篇共18篇已有逐角色稿，尚有{remaining}篇城市任务需同等精修。经济数字、全区域情境时间轴、比例房间与最终对白评审仍未完成；不是可运行任务树或用户认可的终稿。静态工具仅核引用、演员、场景归属、分支门槛和现有回执覆盖。\n\n[[布林人物对白与网状演出审查]] · [[任务空间与地点关联审查]] · [[城市与聚落设计总索引]] · [[城市扩展验收记录]]\n'
if m.get('dramatic_casts',{}).get('MAE'):
 b=b.replace('当前布林11篇与奥尔德文7篇共18篇已有逐角色稿','当前布林11篇、奥尔德文7篇与曼恩7篇共25篇已有逐角色稿')
 b+='\n曼恩接续见[[曼恩人物对白与去留交叉审查]]。\n'
if m.get('dramatic_casts',{}).get('SKO') and m.get('dramatic_casts',{}).get('YOS'):
 b=b.replace('当前布林11篇、奥尔德文7篇与曼恩7篇共25篇已有逐角色稿',f'当前已深化的各城共{73-remaining}篇已有逐角色稿')
 b+='\n两地接续见[[斯孔弗特与约斯特文人物演出审查]]。\n'
write('11_管理/奥尔德文人物对白与交叉演出审查.md',b)
hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule='\n<!-- CITY-DRAMA-S78:BEGIN -->\n2026-10-12 S78：奥尔德文主章＋六支线当前文本由research/aldwynn-drama.json与aldwynn-feedback.json驱动，独立dramatic_casts.ALD不混布林演员。21场、15方法、32旧回执；9新增配角卡，入口design/11_管理/奥尔德文人物对白与交叉演出审查.md。当前18篇逐角色稿，尚55篇待同等精修；stages为地理素材，S78 dramatic_scenes才是本城现行对白。保旧314边与NE/N17/奖励，拒伤像、共仪、赞助不取消基本出口，赠与撤回不得冒称交付。修改后运行Validate-AdditionalCityDrama.py和既有设计检查；数字经济、比例地图和游戏实现未经验证。\n<!-- CITY-DRAMA-S78:END -->\n'
rule=rule.replace('当前18篇逐角色稿，尚55篇',f"当前{73-remaining}篇逐角色稿，尚{remaining}篇")
for p in [ROOT/'AGENTS.md',V/'AGENTS.md',ROOT/'README.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S78:BEGIN -->.*?<!-- CITY-DRAMA-S78:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(quests=len(qs),scenes=sum(len(q['dramatic_scenes']) for q in qs),actors=len(cast),notes=len(hashes),feedback=sum(len(q['dramatic_feedback']) for q in qs)),ensure_ascii=False))
