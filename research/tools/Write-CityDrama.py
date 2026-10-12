"""S76 cast and auditable coverage, without overwriting unrelated generated cards."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';DATE='2026-10-12'
model=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));cast=model['dramatic_cast'];covered=[q for q in model['quests'] if q['city']=='BRY' and 'dramatic_scenes' in q]
hp=ROOT/'research/brynn-generated-note-hashes.json';hashes={}
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=h:raise SystemExit('Preserve/reconcile edited S76 note: '+rel)
def wl(file):return '[['+Path(file).stem+']]'
def front(title,ident,kind):return f'---\ntitle: "{title}"\nid: {ident}\ntype: {kind}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: {DATE}\ntags: [stoneshard, brynn, dialogue, S76]\naliases: []\n---\n\n# {title}\n\n'
def write(rel,body):
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8');hashes['design/'+rel]=hashlib.sha256(p.read_bytes()).hexdigest()
def uses(q,key):
 return any(key==who for s in q['dramatic_scenes'] for who,_ in s['lines']) or any(key==who for pairs in q['dramatic_followups'].values() for who,_ in pairs) or any(f['speaker']==key for f in q['dramatic_feedback'])
for key,a in cast.items():
 if a['existing']:continue
 b=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
 b+='**稳定演员ID**：`'+a['id']+'`。**工作**：'+a['role']+'。\n\n**所求**：'+a['desire']+'\n\n**所怕**：'+a['fear']+'\n\n**说话方式**：'+a['voice']+'\n\n**可能弧线**：'+a['arc']+'\n\n'
 b+='所属 [[聚落_BRY_布林]]。关联当前台本：'+' · '.join(wl(q['file']) for q in covered if uses(q,key))+'。\n\n'
 b+='姓名、经历、关系均Mod原创，不替原NPC或原作统治者。台词只在本人存活/在场且有来源时演；不知的案不因和玩家熟就知，现时位置不能自动传所有同城人物。缺席仅用事前有效有限陈述，代理不能新造本人去留/和解/续作同意。\n\n'
 b+='同一演员只有一个身体和真实位置：私人住处／本职岗位为默认，当前协商的有限会面才可排剧情位置。共享多个任务时，先问本次谈哪件，未谈案不自动结。已结方法只回访，不搬回危险处重演，不用人物死亡后替身台词凑完整演出。\n\n[[布林人物对白与网状演出审查]] · [[空间_BRY_布林]] · [[城市篇章与跨区域任务网]]\n'
 write(a['file'],b)

b=front('布林人物对白与网状演出审查','QA-BRYNN-DRAMA-S76','narrative-audit')
b+='本轮为布林主章与十支线逐角色对白、选择询问、方法门槛和回访细稿。更新前备份backups/city-drama-20261012-s76；当前数据research/brynn-drama.json与brynn-feedback.json，导入纸面模型city-campaign.json。本轮未修改游戏包与存档。\n\n'
b+='## 实际改了什么\n\nS63部分患者/租客/学徒台词标在米罗或蕾娜名下，且每场复用三句询问。S76对11篇改用显式演员台词与现场选项，不再输出旧模板；模型stages留作原地理骨架，S76 dramatic_scenes才是这些任务当前对白。赫林在第二场只留空椅与离开痕，第三场才本人在旧帆村出现，避免原稿两处同时躲藏的矛盾。\n\n'
b+='## 覆盖与人物\n\n|任务|当前场次|方法|有限回执回应|\n|---|---:|---:|---:|\n'
for q in covered:b+='|'+wl(q['file'])+f"|{len(q['dramatic_scenes'])}|{len(q['routes'])}|{len(q['dramatic_feedback'])}|\n"
b+='\n下表含原已有4名城市人物、3名周边住户与13名补充演员。新增配角为多任务共用人物，不每任务塞一位万能委托员。\n\n|演员|本职与口吻|涉及本案|\n|---|---|---|\n'
for key,a in cast.items():b+='|'+wl(a['file'])+'|'+a['role']+'；'+a['voice']+'|'+' · '.join(wl(q['file']) for q in covered if uses(q,key))+'|\n'
b+='\n## 会话选择与真正行动\n\nask只读本人此时肯说的内容；inspect需真完成对应安全观察，私密权限另问；preview展开既有方法，不写resolve/paid；pause关闭。每场都有退出。实际费用、材料与工班分别到位，代价单独预览、玩家二次确认后由真实交接/处置提交，才有方法回执。取消不清掉已经发生的伤害和欠款。\n\n各方法沿用原23种方案与唯一奖所有者，增加的是实际门槛、角色回应与不体面后果。普通修路、搬粮、印送、护理与施工由约定工班完成；玩家调查、问责、选授权范围与接受代价，不收十件东西当另类解法。费用与库存数值仍待下一步，不虚写到位。\n\n'
b+='## 不同顺序怎样回应\n\n56条已存在回执边有分别写的台词：20条支线→城市章、30条城市章→支线、6条外城→布林。原314条边、来源方法、有限事实与所有权保持。先完成来源且本次准传，接收者才知本段；目标已结时仅未来会面/新一班安排，不重选方法、不改既有paid、不重新开闸领费、不回滚货损或N17。未接任何回执也能用原本地独立证据，不要求全城巡礼。\n\n'
b+='## 演员位置与可复入时序\n\n赫林的安全落脚是旧帆村船骨棚干角，米蕾未归弟弟不是赫林。第二场工场只见空椅/样扣；未接本人许可不向阿薇、工头、药商转现时住址。本人愿见谁，才安排后面的分开会面。\n\n佩兰默认租屋巷，安菈/沃伦默认副工场，乔彤默认校版廊，陶芮默认普通护理侧间，奥德默认靠泊亭，洛妲默认安全水门廊。维松只在同意本次见面时出现，没来领奖仍可使用事前有限许可；不在结案场强行生成其人。鲁坎/芮莎/米蕾只按本村亲历和本人事项说话，不用同城链接赋予全案秘密。\n\n同一NPC多案并存时以当前约定会面/本人日常地点为准，不克隆身体。到达某房间可先看固定物；人不在只显示问讯/等下一班/离开，不顺读全部台词。公开授权和事实核验分别记；不因玩家关菜单视为拒绝全案，也无未告知倒计时强杀或强结。\n\n'
b+='## 手工逐案审查焦点\n\n|场景|当前设计结果|\n|---|---|\n|赫林拒登台|civic暂停，不等于放弃住处；有限分案须实际同意；拒全部代理保基本安全与未结记录|\n|阿薇借名领款|错误留下，她只认自己的那笔，不代丈夫认全部工伤/去留|\n|安菈留坊或走|留可仍怨师傅，走真损工具/工期；旧教养费不买未来人身|\n|伊芙双灯或私存|两路均不强原谅奥辛，不改原围城胜败|\n|维松不领奖|补地方事实与仪式拆开；死亡不补新愿意，薇特可独立退自己多领份|\n|陶芮拒商用|失高现金而保有限普通护理；有限交易也不保证痊愈|\n|水门先做或后做|同次安全、料与工资不重复；已稳居民不为另一任务重回危险|\n|单方赞助之后办夜会|新公共席必须真撤当前控制，旧控制历史仍在；CM方法不重选|\n|米蕾放船|仅本案位/存物/款项，不确认弟弟生死，不买全村政治代理|\n|芮莎未来预购|只一季有限份，底种不抵押，未到粮不充当前库存|\n\n'
b+='## 完成口径与剩余工作\n\n本轮11篇已有逐角色对白与演出逻辑初稿，不是文学终审、游戏对话树或已玩过任务。其它62篇城市任务仍有S63询问模板，需要同样精修；有限经济数字、全区域时间轴与比例地图仍待定。因此不能以此宣称用户完整城市设计目标已经全部达成。\n\n工具校验只验数据/双链/场景归属/方法覆盖/已知回执，不证明对白艺术质量或真实游戏运行。报告research/brynn-drama-validation.json；新卡哈希research/brynn-generated-note-hashes.json，原任务哈希仍city-generated-note-hashes.json。[[城市与聚落设计总索引]] · [[任务空间与地点关联审查]] · [[城市扩展验收记录]] · [[网状叙事与条件对话规范]]\n'
remaining=sum('dramatic_scenes' not in q for q in model['quests'])
b=b.replace('其它62篇城市任务',f'其它{remaining}篇城市任务')
if model.get('dramatic_casts',{}).get('ALD'):b+='\nS78接续：奥尔德文七篇当前对白与回执见[[奥尔德文人物对白与交叉演出审查]]。\n'
if model.get('dramatic_casts',{}).get('MAE'):b+='\nS79接续：曼恩七篇当前对白与回执见[[曼恩人物对白与去留交叉审查]]。\n'
write('11_管理/布林人物对白与网状演出审查.md',b)
hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule='\n<!-- CITY-DRAMA-S76:BEGIN -->\n2026-10-12 S76：布林主章＋10支线当前对白由research/brynn-drama.json、brynn-feedback.json驱动；stages只保S63地理骨架，dramatic_scenes是当前文本，不再输出三问模板或把患者/学徒话标在商户名下。20名演员包含13新增配角，56条旧回执分别写早到/晚到回应。入口design/11_管理/布林人物对白与网状演出审查.md。只增剧情细稿，不增新奖励、全巡前置、原作事实或游戏实现；实际签约/交接才提交，已结不改选，不克隆NPC。运行Validate-CityDrama.py及既有设计检查，尚余62篇城市对白与经济数值未终审。\n<!-- CITY-DRAMA-S76:END -->\n'
rule=rule.replace('尚余62篇',f'尚余{remaining}篇')
for p in [ROOT/'AGENTS.md',V/'AGENTS.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S76:BEGIN -->.*?<!-- CITY-DRAMA-S76:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
p=ROOT/'README.md';t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S76:BEGIN -->.*?<!-- CITY-DRAMA-S76:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule.replace('入口design/11_管理/布林人物对白与网状演出审查.md','入口 [布林人物对白与网状演出审查](design/11_管理/布林人物对白与网状演出审查.md)'),encoding='utf-8')
print(json.dumps(dict(quests=len(covered),scenes=sum(len(q['dramatic_scenes']) for q in covered),actors=len(cast),new_actors=sum(not a['existing'] for a in cast.values()),feedbacks=sum(len(q['dramatic_feedback']) for q in covered)),ensure_ascii=False))
