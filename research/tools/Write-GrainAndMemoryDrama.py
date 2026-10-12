"""S83 distinct family cards and grain/memory cross-task review, design only."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));hp=ROOT/'research/grain-memory-generated-note-hashes.json';hashes={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if sha(ROOT/rel)!=h:raise SystemExit('Preserve/reconcile edited S83 note: '+rel)
casts={cid:m['dramatic_casts'][cid] for cid in ['OSB','RAT']};qs=[q for q in m['quests'] if q['city'] in casts];cs={c['id']:c for c in m['cities']}
def wl(p):return '[['+Path(p).stem+']]'
def front(t,i,k):return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, dialogue, S83]\naliases: []\n---\n\n# {t}\n\n'
def write(rel,b):
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(b,encoding='utf-8');hashes['design/'+rel]=sha(p)
def uses(q,key):return any(who==key for s in q['dramatic_scenes'] for who,_ in s['lines']) or any(who==key for pairs in q['dramatic_followups'].values() for who,_ in pairs) or any(f['speaker']==key for f in q['dramatic_feedback'])
for cid,cast in casts.items():
 for key,a in cast.items():
  if a['existing']:continue
  b=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
  for label,field in [('稳定ID','id'),('工作','role'),('所求','desire'),('所怕','fear'),('口吻','voice'),('可能弧线','arc')]:b+=f'**{label}**：{a[field]}\n\n'
  b+='所属'+wl(cs[cid]['file'])+'，人物、关系与本案行为为Mod原创。关联：'+' · '.join(wl(q['file']) for q in qs if q['city']==cid and uses(q,key))+'\n\n'
  b+='一个身份和身体按工作、去向及受准约见移场，不在每个任务另生同名人。只说亲历、受准本段材料与实际收到的有限回执；死亡、缺席、拒绝与私密优先，双链不授全城知情。钱、种、饭、礼、章、护班与门料真实先占，实际交接／处置才确认；晚到仅未来，不抹伤害旧债、复制奖励或改N17。\n\n[[奥斯布鲁克与拉滕人物演出审查]] · '+wl(cs[cid]['space_file'])+' · [[城市篇章与跨区域任务网]]\n'
  write(a['file'],b)
b=front('奥斯布鲁克与拉滕人物演出审查','QA-GRAIN-MEMORY-DRAMA-S83','narrative-audit')
b+='两地主章＋六支线逐角色初稿。源为Author-GrainAndMemoryDrama.py、Author-GrainMemoryFeedback.py与osbrook／ratten的drama.json及feedback.json。更新前备份backups/city-drama-20261012-s83，本轮只写设计、未更新游戏或存档。\n\n'
b+='''## 两地的生活与原作边界

奥斯布鲁克以可播种样、卖过的一袋、旧磨耗、牲铃、门钥和井边菜篮呈现地方生计。主章不是给城里供无限粮，村户能拒预购，有限过渡口粮与明年订单各有真实代价。家中帮过、借过都可以是真，强替人签劳动、婚事或土地也可以同时是真的错；人物不用否定过去全部好处才能脱离当前控制。新增磨租、田户、母女婚约与私人份额皆原创，原村领主、店铺、酒馆、原生任务和服务不替换，不定全国土地／继承制度。

拉滕以新痕、响绳、旧副件、附碑、仿章模和不同孔筹呈现公共记忆。旧狂兽仍死，揭穿伪响不让当前风险也消失；专业有限驱护实际执行，玩家可选白昼观察或现场掩护，夜访不是硬前置，也不是击杀数任务。旧英雄事迹只到原作已核范围，爵士现时生死不补新结论，雕刻不当官方兽形。护栏工瑟铎为本地原创退班普通人，不推出原作军团退役身份或新的兵役系统。

上述新增人、亲属、旧件和私款为Mod原创，事实与unknown仍见[[城市设计与原作避让审查]]。[[空间_OSB_奥斯布鲁克]] · [[空间_RAT_拉滕]] · [[原素材参考与城市概念图]]。

## 八案覆盖

|任务|场次|原方法|早／晚回访对|
|---|---:|---:|---:|
'''
for q in qs:b+='|'+wl(q['file'])+f"|{len(q['dramatic_scenes'])}|{len(q['routes'])}|{len(q['dramatic_feedback'])}|\n"
b+='\n24场、16原方法、48组现场答复、29条旧传入回执（OSB15／RAT14）。19名演员，11新增配角卡；原73任务、314边、地理stages、方法、NE、奖励和N17保持。S83 dramatic_scenes是当前对白，旧三句模板不再配人物头像。\n\n'
b+='''## 人物跨案弧线

|人物关系|具体变化|留在历史里的代价|
|---|---|---|
|芙朵／多恩／瓦森／洛珊|卖粮救弟弟真认，底种释押和饭有限分；父债与女儿路费／限工独立，外作或洛珊真教有限修筐皆能成立|芙朵瞒过实售、多恩暗替签、瓦森强磨条件留史；释种不清全部旧债，留村不再给父亲代签|
|德娅／蔻芙／雅铎|一季预款旧经验解释母亲急收礼；女儿可愿婚而保地，也可暂停清礼，公共井照用|德娅替许土地、雅铎把不安听成移地仍留；退礼少体面与现金，不保证两家马上和好|
|沃达／雷玛／芮茵|开侧门退出保旧互助，或先有钥再续一季；余料实退、维护贵，各不强无限补料|堵门、独钥和剩余户担心留；主章不能默认退户出共粮，来吃一餐不续共田|
|阿莉／妮耶／伊默|旧救人与漏下家庭分记，限权附记或私家副件；伊默认把今损叫旧兽，仍有旧损请求|阿莉删过见证、赚过完整故事钱；后人不强公开、不必握手，英雄也不因补碑被抹掉|
|托斐／瑟铎／芬罗|伪响与当前普通痕分因，撤绳不撤护；有限专业班实到，新户真姓可核当前损|托斐造响拖欠不因有真兽变好，芬罗未做冒领不写已犯罪；新旧赔都可能缺额|
|佩菈／米菈|本枚新铸、假旧价与真实旧事分清；真准明标仿退差价，或停未准样限存退款|改标不当退已付，未售新件不当退款收入；米菈可收回全史皆假的怒话，不必再采购|
|阿莉／妮耶／伊默／佩菈|给付与出席分，或各家私下纪念；真想参加与真不想重复痛苦并存|少声势、少摊客、分散维护费真少；拒礼不取消基础份，参加一次不买未来见证|

## 两户女儿与原模板纠正

芙朵与父亲多恩属一家庭，救弟弟的实售和学艺是同一成年人的跨案生活。蔻芙为德娅的成年女儿，与雅铎为另一对；婚事不转给芙朵。德娅在芙朵案只以自己的借季经验与有限牵线说话，不冒充她的母亲。原stages中把父母、修工或领助者台词放在通用主角名下的情况保留作历史地理素材，当前逐句由dramatic_casts与speaker指定，不继续沿用。

## 有限粮、门、礼与护赔账

OSB可播底量、口粮、实售、实押、糠耗、旧磨租、父债、女儿路费、教作工时、篱料与礼款分别记。同一袋售掉不能再播／吃，同笔定金不能付三家。预购限一季数量，薄收风险双方真准，不拿样芽保证整田收成；拒预售者的中立过渡份也要真有来源。余额欠则认欠，不因主章结案把路费、礼退款全部写到账。固定种样无需盗仓，普通分粮、开门、教作执行不变玩家搬十袋／收十木的循环。

RAT旧池、当前护赔源、争议柜段、实付临时份、专业护班、碑／柜维护、仿章差价与原型许可各单记。现损不冒领旧兽赔款，旧漏不因新住户领新份消失。给付池缺额照留，明标不等退款，未售新章不预生收入。当前安全临护先行；实际专业驱护完成后才收束其范围，未续班不假永驻。旧争可真存柜，不能让不知道旧那笔给谁使今夜完全不做。

## 拒绝、死亡和顺序

|情形|出口与边界|
|---|---|
|拒病例／私仓／家史|固定种样、公共痕、受准实付与有限凭可核；不给额外病例或卧房换基本申请|
|拒外作、拒婚、拒续围|真实本地学作、暂停有限清礼或独立侧门；普通路水和已核旧权不作惩罚|
|拒预售／分期|真实有限中立过渡源另核；款粮不足保待办，不把口头愿意当到账|
|拒夜访／战斗|白昼无伤绳样与当前固定痕可查，真实专业有限驱护出口；不全歼野兽、不放活畜重演|
|拒仪式、公开家名或原型商用|基础核赔照需，未准副件分柜，停售限存；拒绝不是忘旧救人或无新损|
|任人物死亡／缺席|本人句停，只固定受准事实与合法限权接续；不生新签约／展示／和解，不造第二同名角色|
|支线先到／主章先到|各本案款料工时先真实占用，后案查余量；早到仅未来方案与报价，晚到仅下一次，不回滚旧resolve、奖励或N17|

传入先例为CX05布林限粮实际支付、CX30曼郡有限旧名不购未来归属、DT04公开护种，以及CX18布林双见证未和解、DT03普通护栏范围。回执不传全部城状态，不授新婚、地、家名或永久机构权；每条边有独立早到／晚到台词与具体下一行动，无旧案亦有本地固定替代，不设全城全支线硬前置。
'''
remaining=sum('dramatic_scenes' not in q for q in m['quests'])
b+=f'\n## 阶段与检查\n\n当前{73-remaining}/73篇城市任务有逐角色初稿，尚{remaining}篇待同等深化。Validate-GrainAndMemoryDrama.py核准确源／渲染、两户身份、旧边和有限实际门槛；三项原检查核双链／依赖／网络。数值经济、详细时间轴、比例地图、最终文学评审与游戏运行仍未验收，不能据静态通过称整体完成。\n\n[[城市与聚落设计总索引]] · [[城市篇章与跨区域任务网]] · [[任务空间与地点关联审查]] · [[城市扩展验收记录]]\n'
write('11_管理/奥斯布鲁克与拉滕人物演出审查.md',b);hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule=f'\n<!-- CITY-DRAMA-S83:BEGIN -->\n2026-10-12 S83：奥斯布鲁克／拉滕八案源为osbrook／ratten的drama.json与feedback.json，入口design/11_管理/奥斯布鲁克与拉滕人物演出审查.md。24场、16方法、29旧回执、11新卡；芙朵学艺／蔻芙婚事分户，种／饭、父债／路费、门钥／互助、婚／地各准；伪响不盖真风险，旧兽仍死，假章不判全部旧史，基本给付不买出席。当前{73-remaining}篇逐角色稿、{remaining}篇待深化，旧314边／NE／奖励／N17保，运行Validate-GrainAndMemoryDrama.py与既有检查；数值、比例地图和游戏未验收。\n<!-- CITY-DRAMA-S83:END -->\n'
for p in [ROOT/'AGENTS.md',V/'AGENTS.md',ROOT/'README.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S83:BEGIN -->.*?<!-- CITY-DRAMA-S83:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(quests=8,scenes=24,methods=16,choices=48,incoming_pairs=29,actors=19,new_cards=11,notes=len(hashes),covered=73-remaining,remaining=remaining),ensure_ascii=False))
