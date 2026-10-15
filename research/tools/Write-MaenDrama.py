"""Render S79 Maen cast additions, shared identity notes and scene review."""
from pathlib import Path
import json,hashlib,re
from NotePreserve import preserve_foreign
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));cast=m['dramatic_casts']['MAE'];qs=[q for q in m['quests'] if q['city']=='MAE'];hp=ROOT/'research/maen-generated-note-hashes.json';hashes={}
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=h:raise SystemExit('Preserve/reconcile edited S79 note: '+rel)
def wl(p):return '[['+Path(p).stem+']]'
def front(title,ident,kind):return f'---\ntitle: "{title}"\nid: {ident}\ntype: {kind}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, maen, dialogue, S79]\naliases: []\n---\n\n# {title}\n\n'
def write(rel,b):
 b=preserve_foreign(V,rel,b)
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(b,encoding='utf-8');hashes['design/'+rel]=hashlib.sha256(p.read_bytes()).hexdigest()
def uses(q,key):return any(key==who for s in q['dramatic_scenes'] for who,_ in s['lines']) or any(key==who for pairs in q['dramatic_followups'].values() for who,_ in pairs) or any(f['speaker']==key for f in q['dramatic_feedback'])
for key,a in cast.items():
 if a['existing']:continue
 b=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
 if a.get('legacy_shared'):b+='> [!info] 共用人物\n> 这就是[[台本_N10_没有写下的见证]]里的凯姆，本轮补卡而非新增另一个凯姆。存活、失印、旧责任与已结方法共用，城市任务不重奖或重新洗清；设计ID用于引用，不是运行资源索引。\n\n'
 for label,field in [('稳定ID','id'),('工作','role'),('所求','desire'),('所怕','fear'),('口吻','voice'),('可能弧线','arc')]:b+=f'**{label}**：{a[field]}\n\n'
 b+='所属[[聚落_MAE_曼恩]]，身份／经历Mod原创。关联：'+' · '.join(wl(q['file']) for q in qs if uses(q,key))+'\n\n'
 b+='共用一身体，按实际日常位置和本人约见移场；没来、死亡、拒绝、保密优先，不为了串任务各生成一人。只讲亲历、准用本段或已收有限回执，关联双链不等于知道全案。当前愿意只管本次范围，取消不结案；旧伤害、已用资源和欠项保留。\n\n[[曼恩人物对白与去留交叉审查]] · [[空间_MAE_曼恩]] · [[城市篇章与跨区域任务网]]\n'
 write(a['file'],b)
b=front('曼恩人物对白与去留交叉审查','QA-MAEN-DRAMA-S79','narrative-audit')
b+='本轮将曼恩主章与六支线写成逐角色演出初稿。更新前备份backups/city-drama-20261012-s79；作者源research/maen-drama.json与maen-feedback.json。游戏与角色存档未改。\n\n'
b+='## 地域命题与原作避让\n\n寒地战损的生活不以空城或大学重新招生收束。根菜灶、旧织物、寒窗夜灯、残庭安全试台与分用途藏柜承担剧情；真实稀缺决定有些班要等，有些原件失去，有些人不愿同坐一桌。知识可能有用，也可能曾压过人，反对某种保存者不自动变成愚昧障碍。原作天气、全城控制与葛文涅尔去向未知，见[[城市设计与原作避让审查]]；新增人物、记录和政治班组均是Mod原创。\n\n'
b+='## 七案覆盖\n\n|任务|当前场次|原方法|早／晚回执对|\n|---|---:|---:|---:|\n'
for q in qs:b+='|'+wl(q['file'])+f"|{len(q['dramatic_scenes'])}|{len(q['routes'])}|{len(q['dramatic_feedback'])}|\n"
b+='\n合计23场、15种原方法、33条已有传入回执。原314边、地图节点、地点、奖励归属及N1—N18／NE／N17保留。stages只是S63地理素材；S79 dramatic_scenes为本城当前对白，dramatic_feedback.speaker为本次实际说话者，不拿旧receiver摘要配新头像。\n\n'
b+='## 人物和生活关系\n\n|关系|如何跨任务改变|保留的损失／不和|\n|---|---|---|\n|塞娜／莉德／凯姆|保书与替熟人解释分开，孔序核来源可独立进入；本段更正不重做N10，塞娜失去代言便利|凯姆旧失印不回授，莉德也可选私存；旧责任不被匿名吞没|\n|玛娅／古岚／缇弗|粮少是真，已做照护也是真；照护份、工资与公议票实际拆开，或自愿转中立班|拆条件少动员，转班使原站少人，不能把缺口再归作护工不关心|\n|维芮／多罗|售料低价保身份范围，或保袍求有限过渡；姐姐做过的照护被认，不用沉默当售物同意|卖了不证明忘过去，保物不抹姐姐负担，也无永久免费粮|\n|欧岚／薇榆／尼芙|姓名对照、护理连续段与改账责任分开，保护人也承认自己护过改账|分箱会毁部分可选原件，迁藏会失一把全柜钥；护理接续不能拿空火盆代完成|\n|菲勒／扎禾|暖过一夜与永久技术归属不同；限批续作有独立署记与退出，另棚真有成本|扎禾可有怨又真愿留，菲勒会失独家，离棚不需否认曾获救|\n|艾娜／尼芙／贝诺|自愿留城与真接收出城均可完成这一班；实际床、水、人手和去向授权分别核|没有整齐的全体获救表，未来位和班不由旧结案生成，拒迁不抹旧救助|\n\n'
b+='## 共用旧人物与有限知情\n\n塞娜与玛娅的城市卡和旧人物卡是同一人的两个设计视角，不能各生一身体：[[人物_塞娜·里德]]与[[人物_NPC-SENA_塞娜·里德]]、[[人物_玛娅·禾]]与[[人物_NPC-MAYA_玛娅·禾]]分别共用责任、存活和已结案历史。莉德沿已有来源角色。凯姆新增的是本轮角色卡，不是新人生；N10已结不再发印、补认罪或复发NE。未做N10也有本地固定孔序，不能用不存在的旧回执抢先念其结果。\n\n'
b+='默认：玛娅／古岚在实际粮站，缇弗在根灯照护班，塞娜／莉德按本次准用核验约见，薇榆在雪页背注桌，艾娜在冷窗接收亭，菲勒／扎禾在旧织街工班；扎禾真离棚后不在新旧两点同时干活。维芮只在自愿私下约见或有效限权代理时说物件范围；多罗在日常照护处。尼芙默认实际护理点，不随全部任务巡游；去外点只有她真选且接收者实接。欧岚在无火分档廊，贝诺在当班中立护理点。凯姆沿旧剧情当时位置和权限，缺席／死亡用固定物证，不为城市听证回生。\n\n'
b+='每句先核说话者亲历和本次允许讲的范围；住址、物件、护理、署记、去向和政治授权分开。链接同城不意味着知全名册；主章五场不是所有居民必到的巡礼。按先到后场看固定物时改询问，不抢先替人认错或讲未准秘密。\n\n'
b+='## 先后次序与资源实际影响\n\n12条支线→主章分别带售物／保物、分箱／迁藏、护工留／转、织工续／离、来源更正／私存、留城／出城的有限事实；18条主章→支线按separate／evacuate／control分别写，尤其控制之后再办拆票、独立更正和中立接手必须真实可执行，不用新台词抹旧排斥。另有CX13限定代理、CX25核心安全、IN-MAE旧案公开范围三条传入。未收任何回执也能本地独立核，外城不会因此给全城权。\n\n'
b+='同一件袍只售一次，同一工资／粮份／床／副件／工时不两案各领一次。新班可另约但须新资源，不让问话生成菜、床和运输。实际保护／交接＋二次确认后才结，取消、预览、拒绝或尸体沉默不选方法。已结只改未来许可、服务和报价，不重选resolve、不回滚paid、火损与控制，不解冻N17。\n\n'
b+='## 人物可以不被说服的出口\n\n维芮可不卖、不公开家门；缇弗可不坐桌而留工，也可真转一班；扎禾可留又怨，或独立慢做；莉德可私存不做全城名人；尼芙可留下且拒政治站，也可只授权下一班迁出。古岚控制的只是有限新增条件站，未同意者不入名单；普通中立保障实际由另一班接，不能同粮两边承诺。欧岚不肯协作仍可固定用途对照，不能焚掉混箱取证。\n\n'
remaining=sum('dramatic_scenes' not in q for q in m['quests'])
b+=f'## 当前范围与剩余工作\n\n三大城市当前共25篇有逐角色演出初稿，其余{remaining}篇城市任务仍待同等深化。全区域情境时间轴、有限经济数字、比例房间和文学终审尚未完成；本轮不称已运行任务树。工具验证只证明数据、引用、演员／空间归属、方法与回执覆盖及明确分支回归，不能证明对白质量或游戏行为。报告research/maen-drama-validation.json；新卡哈希research/maen-generated-note-hashes.json。\n\n[[布林人物对白与网状演出审查]] · [[奥尔德文人物对白与交叉演出审查]] · [[任务空间与地点关联审查]] · [[城市与聚落设计总索引]] · [[城市扩展验收记录]]\n'
b=b.replace('三大城市当前共25篇有逐角色演出初稿',f'全部已深化城市任务共{73-remaining}篇有逐角色演出初稿（其中三大城市25篇）')
if m.get('dramatic_casts',{}).get('SKO') and m.get('dramatic_casts',{}).get('YOS'):b+='\n冶炼／羊毛两地接续见[[斯孔弗特与约斯特文人物演出审查]]。\n'
write('11_管理/曼恩人物对白与去留交叉审查.md',b)
hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule='\n<!-- CITY-DRAMA-S79:BEGIN -->\n2026-10-12 S79：曼恩主章＋六支线逐角色稿由research/maen-drama.json与maen-feedback.json驱动，dramatic_casts.MAE独立。23场、15原方法、33旧回执；8补充角色卡含N10同一凯姆，不新增第二人生或回授旧认证。入口design/11_管理/曼恩人物对白与去留交叉审查.md。三大城市共25篇当前逐角色稿，48篇待同等深化；病例、住址、技术、物件、政治与去向授权分别核，焚毁/排斥/欠款留史，不强空城或正常学院重开。修改后运行Validate-MaenDrama.py及既有设计检查；数字经济、比例地图、最终对白和游戏运行尚未验收。\n<!-- CITY-DRAMA-S79:END -->\n'
rule=rule.replace('三大城市共25篇当前逐角色稿，48篇待同等深化',f'当前共{73-remaining}篇逐角色稿，其中三大城市25篇；{remaining}篇待同等深化')
for p in [ROOT/'CHANGELOG.md',V/'AGENTS.md',ROOT/'CHANGELOG.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S79:BEGIN -->.*?<!-- CITY-DRAMA-S79:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(quests=len(qs),scenes=sum(len(q['dramatic_scenes']) for q in qs),actors=len(cast),cards=sum(not a['existing'] for a in cast.values()),legacy_shared=1,feedback=sum(len(q['dramatic_feedback']) for q in qs)),ensure_ascii=False))
