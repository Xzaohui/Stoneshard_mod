"""Render authored S80 characters and review; one shared trader, no game writes."""
from pathlib import Path
import json,hashlib,re
from NotePreserve import preserve_foreign
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));hp=ROOT/'research/forge-wool-generated-note-hashes.json';hashes={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if sha(ROOT/rel)!=h:raise SystemExit('Preserve/reconcile edited S80 note: '+rel)
casts={c:m['dramatic_casts'][c] for c in ['SKO','YOS']};qs=[q for q in m['quests'] if q['city'] in casts];cities={c['id']:c for c in m['cities']}
def wl(p):return '[['+Path(p).stem+']]'
def front(title,ident,kind):return f'---\ntitle: "{title}"\nid: {ident}\ntype: {kind}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, dialogue, S80]\naliases: []\n---\n\n# {title}\n\n'
def write(rel,body):
 body=preserve_foreign(V,rel,body)
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8');hashes['design/'+rel]=sha(p)
def uses(q,ident):
 cast=casts[q['city']]
 keys={k for k,a in cast.items() if a['id']==ident}
 return any(who in keys for s in q['dramatic_scenes'] for who,_ in s['lines']) or any(who in keys for pairs in q['dramatic_followups'].values() for who,_ in pairs) or any(f['speaker'] in keys for f in q['dramatic_feedback'])
actors={a['id']:a for cast in casts.values() for a in cast.values() if not a['existing']}
for ident,a in actors.items():
 body=front(Path(a['file']).stem,'CITY-NPC-'+ident,'character')
 for label,field in [('稳定ID','id'),('工作','role'),('所求','desire'),('所怕','fear'),('口吻','voice'),('可能弧线','arc')]:body+=f'**{label}**：{a[field]}\n\n'
 home=[cid for cid,cast in casts.items() if any(x['id']==ident for x in cast.values())]
 body+='所属／实际活动范围：'+' · '.join(wl(cities[c]['file']) for c in home)+'。身份、经历与关系均Mod原创，设计ID不是运行资源索引。\n\n关联：'+' · '.join(wl(q['file']) for q in qs if uses(q,ident))+'\n\n'
 if ident=='TRADE-NPC-LIQUI':
  body+='## 共用人物与有限交易\n\nSKO和YOS的莉葵是同一身体、同一笔周转和同一批在手货。城间实际行程期间两市都不能同时点到她；已有有效本单记录可核，缺席不补新的本人交易同意。只知道她亲自成交的物、款与质量，不带妮莎的家事或呼蕾的病史换价格。\n\n报价预览不占款；双方实订才占本单尚未占用款／货，到款与交物逐项确认后记已执行。撤单只释放未执行段，已经花掉的钱不自动退回，旧坯未卖出不能当收益。冬衣已给一户不能仍在第二案库里。利润与周转不无限刷新，往另一城前按实余量更新报价。\n\n'
 body+='角色按本职或真实约见移场；死亡、缺席、拒绝、保密优先。只讲亲历、已受准本段或已收有限回执；关联双链不等于知道全部城案。预览、沉默和取消不代许可，完成一案不买未来续作。旧伤害、旧欠、已用物与钱保留。\n\n[[斯孔弗特与约斯特文人物演出审查]] · [[城市篇章与跨区域任务网]]\n'
 write(a['file'],body)
body=front('斯孔弗特与约斯特文人物演出审查','QA-FORGE-WOOL-DRAMA-S80','narrative-audit')
body+='斯孔弗特与约斯特文各一主章、三支线的逐角色初稿。作者源research/skonfert-drama.json、skonfert-feedback.json、yostwayne-drama.json与yostwayne-feedback.json。S80原备份与本轮含概念图的备份分别在backups/city-drama-20261012-s80、backups/city-drama-20261012-s80-art-followup。设计阶段，不修改游戏、MSL或玩家数据。\n\n'
body+='## 两地各自的问题\n\n斯孔弗特把少烧一炉的产值、等待未归者的亲情与已做工钱放在一起。会计的等待真实，中介的兑筹也真，却不表示未归者已到；归乡者的感谢不出售未来劳力。冷沟把信仰与安全分开，护符不替厂里卸责，也不作为患者失去护理的条件。\n\n约斯特文以羊毛、织机、染色来源与预收订单承载矛盾。家纹确有工序与信用，不能吞徒弟后来的颜色；冬料是之前认过的一份，不是出口卖剩。下游怕用水有理由，迁居身份却不能代具体管序；本地经手者只认自己开过的那段。新增格局、现代工班与事件均为Mod原创，不推城主去向、全年天气、全国工商业或N8全部病因。\n\n[[城市设计与原作避让审查]] · [[空间_SKO_斯孔弗特]] · [[空间_YOS_约斯特文]]\n\n'
body+='## 八案覆盖\n\n|任务|场次|原方法|早／晚回执对|\n|---|---:|---:|---:|\n'
for q in qs:body+='|'+wl(q['file'])+f"|{len(q['dramatic_scenes'])}|{len(q['routes'])}|{len(q['dramatic_feedback'])}|\n"
body+='\n共24场、16种原方法、48组现场选择答复、30条既有传入回执（SKO14，YOS16）。没有添加新奖励或第315条任务边；stages保原地理素材，S80 dramatic_scenes为现行文本。314条原关系、方法、地图地点、奖励归属、NE与N17保持。早晚回应由当前dramatic_feedback.speaker演出，不拿旧receiver摘要配新头像。\n\n'
body+='## 人物跨案的变化与仍有的矛盾\n\n|关系|选择怎样影响另一案|不会被结案抹掉的部分|\n|---|---|---|\n|妮莎／桑勒／古烈／布岚|封拆预款后新炉缺钱；退单后少产；主章缩产或售坯又决定下一笔真正可用的款|妮莎挪过的钱仍由她认，桑勒兑筹不代表归人已到，炭工拒续作不取消旧工资|\n|博赫／雷哈／妮莎|限权见证让主章只认准句；安静归乡仍可接普通班；还款不买另一次仪式|博赫是雷哈的儿子，不是妮莎未归弟弟。父亲失体面、儿子仍有怨，不强英雄化或再出征|\n|古烈／温诺／妮莎|分流减产、停沟替水都改变主章炉期；主章已偿的钱不能借回来写维护已付|护符仍可留，身体损伤不因水班完成消失，原因及源责任未核继续待查|\n|塔雅／缇娜／梅蓓|归包与一单延期限制主章续作范围；分署或独立反过来不自动清掉路费及真实旧债|缇娜是同一个成人徒弟兼迁居染工，过去借标欠款是真的，扣包和不和也是真的|\n|尤尔／呼蕾／昂朵|留冬或合用换衣决定出口余料；主章已签帘与帐段不能在冬料案再签一份|尤尔少体面大单仍想赚；呼蕾可拒衣而不露病史，昂朵专业验尺寸不代同意或生新衣|\n|溪悠／阿洛／缇娜|具体班分流或先停新管决定真实洗料能力与订单延期|安全改善不抹溪悠旧排斥；阿洛是本地具体经手者，不替全部迁户赔罪，未知源责任不随暂停全清|\n|莉葵／两地交易者|一地已实买坯、交衣和占款减少另一地后续报价；货若未实际卖出不产生周转|她不是无限慈善出口，亏与收益须真实兑现；不靠知道两地私史作万能调停|\n\n'
body+='## 共用身体、地点与有限知情\n\nSKO八个演员槽与YOS九个槽共16个唯一身份；重复的只有莉葵。一份补充角色卡在SKO建，YOS沿同ID与同路径引用，不另起第二人。八名新角色卡中四位属SKO（含莉葵）、四位属YOS；每地另用已有两城市人物与两聚落住户。\n\n妮莎默认寄柜／工款会计点，桑勒在兑筹柜；古烈普通工班或脱离热工护理处，温诺在安全维护岗位。布岚默认炭背预付台，博赫与雷哈在归火普通生活点，返街会面须本人真愿。归乡与未归两户保持不同；缺人不意味着死亡。\n\n塔雅默认织屋工作点，缇娜依本人当时选择在本坊或实际安全去处，梅蓓默认缓梭本班。尤尔在羊坡称捆台，呼蕾在实际取冬份约见处，昂朵在当班验料点，溪悠在生活水岸，阿洛在排管岗位。有人先离坊，后场由本次真约见／有效有限材料回答，不能为主章强回屋；未验远城接应不填BRY或MNS已到。\n\n玩家先安全观察再问亲历，私密许可另问；居住、姓名、病史、技术来源、商标、物件、工班与公开见证不互相包办。缺席或拒某句，可看固定物、等实际一班、用有效限权材料或走独立方法；代理不能新造本人归乡、延期或交换意愿。\n\n'
body+='## 莉葵交易账的设计约束\n\n以下是待实现的设计概念，不是现有游戏变量。两地任务只读取本人亲历的有限交易段，不读取另一城全部任务状态。\n\n|记账段|何时改变|对下一案的影响|\n|---|---|---|\n|可用现金／本单占款|只有真实订立且尚未支付部分占款，预览不占；实际付款转已付|下一地可用=真在手款减尚占款；已付不仍作余额，未卖旧坯不能预生收入|\n|旧坯在途／在手|实际交物才改变归属；不合性能可拒收，撤单只释放未执行段|已售坯不回SKO库存；尚未实售所得不补YOS预算，基本修理料先独立留|\n|普通衣料在手／已交|实际交给获准家庭并验合用才记已交，返还也须实际发生|同衣不能重复换第二捆；拒不合用保留底量方法，不能因热心索隐私|\n|有限工班与行程|采购、检查、改衣和城间移动占实际时间；一身体按真实位置出现|不同时两城出场，不与已占班重复交付；缺席可核本单旧记录但不能替本人答新约|\n\n每份款与物以单一交易项对应所有者和已执行量；一地结案只登记真实完成部分，不凭状态名生成资产。维持旧314边不妨碍同一当事人知道自己亲历付款，但这不是第31条外城全知回执。确切数量、报价、工期与零余额出口仍待经济和情境时间轴细化。\n\n'
body+='## 顺序、行动与替代\n\nSKO有6条支线→主章、6条主章→支线，加CX12分批接工和IN-SKO旧案有限公开先例。YOS同样6＋6，再有CX06新批标、CX10分署不抵赊款、CX28逐人限班与IN-YOS旧案公开段。每条写不同早到／晚到说话者及可执行的未来安排。没有这些外来回执，也可固定兑筹、原袋、旧样、料份及管序独立进案，不要求跨城全巡或三个支线全成。\n\nask只问本次愿说；inspect核安全可达的固定物或受准材料；preview只看方案代价；每场可退出。钱、物、专业班与许可真到位并二次确认才提交方法。已结目标的晚到回执只改下次有限报价、会面与工作，不重选resolve、不重付同项、不回滚旧欠／排斥／损伤、不解冻N17。\n\n普通搬炭、换水、洗料、修理与运衣由真实工班做，玩家面对的是原授权、实际责任、有限预算与人物选择。拒公开仍能归乡，拒延期可归包离坊，拒不合用旧衣可留冬毛；买家缺席或拒报价，SKO保缩产方法，YOS保底量及独立普通出口。护理不要求扔护符或露整户病史。\n\n'
body+='## 图片与制作范围\n\n[[斯孔弗特任务场所概念与台本映射]]与[[约斯特文任务场所概念与台本映射]]各六场所，A—F不是必访顺序；图片不证库存、授权、门锁、管道隔离或碰撞。文学口吻和方言仍需终审，源稿没有摄影合影、强制全体道歉或把战争未知补成官方结局。\n\n'
remaining=sum('dramatic_scenes' not in q for q in m['quests'])
body+=f'## 覆盖与剩余\n\n全部73篇城市任务中，{73-remaining}篇已有逐角色细稿，{remaining}篇仍待同等深化；十五地域总览与三十三卫星构图不代表所有对白或地图完成。全区域情境时间轴、数值经济、比例平面、原素材映射与最终对白评审仍有工作。工具检查仅核作者源／渲染、演员和空间、原方法／回执覆盖及明确分支回归，不是艺术质量或游戏运行证明。报告research/forge-wool-drama-validation.json；新增九份笔记哈希research/forge-wool-generated-note-hashes.json。\n\n[[布林人物对白与网状演出审查]] · [[奥尔德文人物对白与交叉演出审查]] · [[曼恩人物对白与去留交叉审查]] · [[城市与聚落设计总索引]] · [[城市扩展验收记录]]\n'
write('11_管理/斯孔弗特与约斯特文人物演出审查.md',body)
hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule=f'\n<!-- CITY-DRAMA-S80:BEGIN -->\n2026-10-12 S80：冶炼／羊毛两地八案作者源为research/skonfert-drama.json、yostwayne-drama.json及各feedback.json，入口design/11_管理/斯孔弗特与约斯特文人物演出审查.md。24场、16原方法、30旧回执；莉葵共一ID、卡、身体和有限款货，博赫不替妮莎未归弟弟归家，缇娜跨两案同人。当前{73-remaining}篇逐角色稿、{remaining}篇待深化。开门归包、信仰与护理、工钱／预款、冬料／外售分别核，拒未来不抹旧欠；晚到只改未来，不重奖／改N17。运行Validate-ForgeAndWoolDrama.py及既有设计检查；数值经济、时间轴、比例地图和游戏实现尚未验收。\n<!-- CITY-DRAMA-S80:END -->\n'
for p in [ROOT/'AGENTS.md',V/'AGENTS.md',ROOT/'README.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S80:BEGIN -->.*?<!-- CITY-DRAMA-S80:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(quests=8,scenes=24,methods=16,choices=48,incoming_pairs=30,unique_actors=16,new_cards=8,notes=len(hashes),covered=73-remaining,remaining=remaining),ensure_ascii=False))
