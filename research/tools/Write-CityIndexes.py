"""S63 navigation and evidence notes. Preserve earlier screenplay models."""
from pathlib import Path
import json,re,hashlib
from NotePreserve import preserve_foreign
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';DATE='2026-10-12'
m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));cs=m['cities'];qs={q['id']:q for q in m['quests']}
def front(title,ident,kind='navigation',canon='mod-original'):
 return f'---\ntitle: "{title}"\nid: {ident}\ntype: {kind}\nstatus: draft\ncanon: {canon}\nbaseline: "0.9.4.25-modbranch"\nupdated: {DATE}\ntags: [stoneshard, S63, cities]\naliases: []\n---\n\n# {title}\n\n'
def wl(file):return '[['+Path(file).stem+']]'
changed=set()
def write(rel,body):
 body=preserve_foreign(V,rel,body)
 changed.add('design/'+rel)
 if rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md'] and (V/'11_管理/特殊地点与野外NPC对白扩展计划.md').exists():
  body+='\n用户2026-10-12追加阶段见[[特殊地点与野外NPC对白扩展计划]]：先收尾城市与全局逻辑，再逐NPC只读核对原版中英文并扩特殊地点／野外对白；该追加阶段尚未开展，不计本页当前完成数。\n'
 if m.get('dramatic_casts',{}).get('KOR') and m.get('dramatic_casts',{}).get('PAS') and rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S84寄存与关口演出\n\n[[考德与柏石关人物演出审查]]覆盖两地主章＋六支线、24场、16方法与28组早／晚回访。考德镇史unknown保留，物／亲属／房／画分项；柏石关同一雷奥莫伦沿N7／SQ02真实结果，床／病例／工资／家书各准，不二发资格奖励。单件文本见[[文书_PAS_列梵的家书与口信]]。\n'
 if m.get('dramatic_casts',{}).get('OSB') and m.get('dramatic_casts',{}).get('RAT') and rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S83粮村与纪念地域演出\n\n[[奥斯布鲁克与拉滕人物演出审查]]覆盖两地主章＋六支线、24场、16方法及29组早／晚回访。种／饭、路费／父债、门钥／旧互助、婚／地分开；旧损／现损、假价／真旧事、出席／基本给付分别限核，不复活旧兽或移原NPC家事。\n'
 if m.get('dramatic_casts',{}).get('EED') and m.get('dramatic_casts',{}).get('FOR') and rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S82林地与矿区演出\n\n[[伊德斯与佛尔霍特人物演出审查]]覆盖两地主章＋六支线、24场、16方法及29组早／晚回访。有限旧材、真实安置、巡段隐私与停班、排水、矿份分别落到具名人物；救援先执行，伤者真出井才出场。图像总览保留，经济数字、比例图与游戏仍未验收。\n'
 if m.get('dramatic_casts',{}).get('DEN') and m.get('dramatic_casts',{}).get('MNS') and rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S81丹布里与曼郡演出\n\n[[丹布里与曼郡人物演出审查]]覆盖两地主章＋六支线、24场、16原方法及30组早／晚回访。三户两空间保真实接收，三成年人同船逐人问；酿酒与箍桶师徒分人，旧名、桶与种枝收益各有真实损失。\n'
 if m.get('dramatic_casts',{}).get('SKO') and m.get('dramatic_casts',{}).get('YOS'):
  pending=sum('dramatic_scenes' not in q for q in m['quests'])
  body=body.replace('逐角色深化稿仍在整理','逐角色初稿见演出审查')
  body=body.replace('25篇当前逐角色稿，48篇待同等深化',f'{73-pending}篇当前逐角色稿，{pending}篇待同等深化')
  if rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
   body+=f'\n## S80冶炼与羊毛两地演出\n\n[[斯孔弗特与约斯特文人物演出审查]]覆盖两地主章＋六支线、24场、16原方法与30组早／晚回执；莉葵同一身体与有限款货，两户归人不混、缇娜两案不克隆。当前共{73-pending}篇城市逐角色初稿，{pending}篇待同等深化。\n'
 if rel in ['00_导航/城市与聚落设计总索引.md','12_美术参考/城市美术与图片目录.md','11_管理/城市扩展验收记录.md'] and (ROOT/'research/city-task-art-20261012.json').exists():
  body+='\n## 任务场所新概念（2026-10-12）\n\n[[斯孔弗特任务场所概念与台本映射]]与[[约斯特文任务场所概念与台本映射]]各新增六处独立构图，链接八篇任务和四个周边聚落。原素材只作材质／尺度参考，逐角色深化稿仍在整理；图片不代表对白已批准或游戏房间已实现。\n'
 if rel in ['00_导航/城市与聚落设计总索引.md','12_美术参考/城市美术与图片目录.md','11_管理/城市扩展验收记录.md'] and (ROOT/'research/shore-vine-task-art-20261012.json').exists():
  body+='\n## 丹布里与曼郡任务场所概念\n\n[[丹布里任务场所概念与台本映射]]与[[曼郡任务场所概念与台本映射]]补十二处场所，关联八篇现行台本及四处周边聚落；保留v1/v2，逐图来源见research/shore-vine-task-art-20261012.json。两床、同桶双签、回程与两对师徒按文字核；坡面、载重、容量和近景仍需制作，尚未生成运行地图。\n'
 body=body.replace('给建筑设计差异化室内平面','将现有逐街区空间方案细化为比例室内平面')
 if rel in ['00_导航/城市与聚落设计总索引.md','12_美术参考/城市美术与图片目录.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S75任务空间（当前细化）\n\n[[任务空间与地点关联审查]]汇总15份地域空间卡、66街区和132个独立室内方案；33个卫星各有独立生活场景和具名住户。58条城市支线已按内容显式指定触发街区、调查聚落与处置／回访街区。布局包含可观察物、实际行动、拒入替代与独立回程，尚需比例平面、碰撞、预算和逐角色对白细稿；静态通过不代表游戏实现。\n'
 if rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S76布林对白（当前细化）\n\n[[布林人物对白与网状演出审查]]覆盖布林主章与十支线、35场逐角色对白、23种原方法的实际门槛和56条既有回执的早到／晚到回应。20名演员中13名新增配角；其余62篇城市台本仍需同等精修。经济数字与游戏对话树未经制作，不能因此称所有区域终稿已完成。\n'
 body=body.replace('大城共用概念板只供风貌，不用于碰撞。','当前十五张参考式像素概念板含三十三个卫星构图，见[[原素材参考与城市概念图]]；旧三联画只留早期对照，均不用于碰撞。')
 body=body.replace('并为其他聚落补独立概念画及游戏资源映射','并补逐格制作图及游戏资源映射')
 body=body.replace('三大城概念板为一张三联画，不计三张独立制作素材；其余十二地域没有独立风貌概念画。','S74已增加十五张参考式像素概念板，覆盖全部地域和三十三个周边构图；卫星面板不是独立像素资产。旧三联画保留历史。')
 body=body.replace('48通路SVG、一张三大城概念板；其余风貌图与比例平面未完成','48通路SVG＋15张参考式概念板（33个周边构图）；比例平面、碰撞与资产拆层未完成')
 body=body.replace('概念板已目视确认三大城风貌差异，不作为比例和碰撞证据。','S74十五张选稿均已逐张目视检查；ALD已定向去水岸、MAE已去未核阵营旗帜。当前图片、提示词和来源见[[原素材参考与城市概念图]]；不作为比例和碰撞证据。文档与图片更新前备份在backups/city-art-20261012-015928。')
 body=body.replace('116条同城路线边，30条旧任务双向接入边','116条CS→CM路线边、138条CM→CS回流边、30条旧任务双向接入边')
 body=body.replace('每条CS路线分别回到本地CM，影响的是实际已执行的结果','每条CS路线分别回到本地CM，CM已执行的方法也回流CS：现存安排与独立方法可用，已占资源不重复承诺、额外费用另记；影响的是实际已执行的结果')
 body=body.replace('73篇初稿，逐路线行动/代价/结果/回访','73篇初稿、223场、149种方法，逐路线行动/代价/结果/回访')
 body=body.replace('66街区、33卫星各有任务入口/现场/回访','66街区有主章核验用途、33卫星有支线现场/回访')
 remaining=sum('dramatic_scenes' not in q for q in m['quests'])
 body=body.replace('其余62篇城市台本',f'其余{remaining}篇城市台本')
 if m.get('dramatic_casts',{}).get('ALD') and rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S78奥尔德文对白接续\n\n[[奥尔德文人物对白与交叉演出审查]]覆盖主章与六支线、21场、15种原方法及32条旧回执的早到／晚到回应。15名演员含9名新增配角；拒伤照、拒共仪、拒赞助均有实际出口，有限资金和工具不因对话生成。\n'
 if m.get('dramatic_casts',{}).get('MAE') and rel in ['00_导航/城市与聚落设计总索引.md','11_管理/城市扩展验收记录.md']:
  body+='\n## S79曼恩对白接续\n\n[[曼恩人物对白与去留交叉审查]]覆盖主章与六支线、23场、15种原方法和33条有限回执的早／晚回应。凯姆沿N10原身份与责任，护理、来源、地址与政治授权分开，焚毁和控制留史；人可自愿留城。三大城市共25篇有逐角色初稿，其余48篇待同等精修。\n'
 if m.get('dramatic_casts',{}).get('SKO') and m.get('dramatic_casts',{}).get('YOS'):
  remaining=sum('dramatic_scenes' not in q for q in m['quests'])
  body=body.replace('逐角色深化稿仍在整理','逐角色初稿见[[斯孔弗特与约斯特文人物演出审查]]')
  body=body.replace('三大城市共25篇有逐角色初稿，其余48篇待同等精修',f'当前共{73-remaining}篇有逐角色初稿（其中三大城市25篇），尚余{remaining}篇待同等精修')
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8')
legacy=[]
for x in ['main','main-late','side','daily','dungeon']:legacy+=json.loads((ROOT/f'research/story-{x}.json').read_text(encoding='utf-8-sig'))
ln={q['id']:f"台本_{q['id']}_{q['name']}" for q in legacy}
def ql(q):return wl(qs[q]['file']) if q in qs else '[['+ln[q]+']]'
cl={c['id']:wl(c['file']) for c in cs}

b=front('城市与聚落设计总索引','NAV-CITIES-S63')
b+='当前城市设计入口：[[城市篇章与跨区域任务网]]、[[城市设计与原作避让审查]]、[[城市美术与图片目录]]、[[城市扩展验收记录]]。\n\nS63扩展覆盖十二个原作命名聚落和三个原创地域；布局、卫星、人员及新任务均为Mod原创。现有六区54节点保留为早期连接场景，不能再当完整世界范围。新增模型另计297个规划功能节点，包含66个街区、132个室内、99个卫星节点；街区名不是全部独立世界格或已做房间。两组预算存在接入重叠，不能相加称351个已定房间。\n\n'
b+='十五个地域章、五十八条城市支线，共七十三篇新台本；原51篇晶石主线/支链/地方事件/副本不删除。布林10条、奥尔德文与曼恩各6条新支线，其他地域各3条。任务数量与纸面覆盖不代表人物、经济、战斗和对白细稿已经终审。\n\n|城市／地域|主题与主章|新支线|卫星聚落|图片|\n|---|---|---:|---|---|\n'
for c in cs:
 b+=f"|{cl[c['id']]}|{c['theme']}；{ql(c['main_id'])}|{len(c['side_ids'])}|"+' · '.join(wl(s['file']) for s in c['satellites'])+'|通路SVG＋参考式像素概念板（含周边构图）|\n'
b+='\n## 当前可用深度与尚缺部分\n\n每城有基线边界、空间气质、街区功能、周边争议、人物弧线、地域主线及支线初稿、两种以上行动路线、费用与回访、跨任务影响和回程规划。每卫星有自己的争议与相关任务，入口/服务/现场三节点及示意。大城共用概念板只供风貌，不用于碰撞。\n\n仍需逐城精修支线场次和配角口吻、确定有限库存与调查费数值、给建筑设计差异化室内平面，并为其他聚落补独立概念画及游戏资源映射。本稿没有逐格地图、完整像素资产或游戏运行验证，因此不能称所有城市都已达到可直接制作/投放的完整终稿。\n\n[[设计总览]] · [[任务台本总索引]] · [[新区域设计与任务总表]]\n'
write('00_导航/城市与聚落设计总索引.md',b)

b=front('城市篇章与跨区域任务网','SYS-CITY-NET-S63','narrative-system')
b+='晶石主线保持N1—N18。城市CM是地方篇章；支线CS可提前、随后、拒做。PAS/ASH/HIG的CM是现有任务的地域编排，不新增第二次晶石证据、奖励或终局。没有“完成全部73任务”前置。\n\n## 交通和叙事分别计账\n\n下面仅为Mod拟定双向交通接入，具体全球方向、里程、种子与原生房间映射均待验证。交通可达不代表双方互知秘密；所有剧情交叉另走有限回执。\n\n```mermaid\ngraph LR\n'
for c in cs:b+=f"  {c['id']}[\"{c['name']}\"]\n"
for a,z in m['travel']:b+=f'  {a} --- {z}\n'
b+='```\n\n## 回执规则\n\n实际选择并完成行动后，来源任务记唯一resolve与receipt事实；玩家可拒传。接收者存活/在场、本人允许传达且有这条有限事实，才作具体回应。死亡优先、再拒绝/保密、再到场、最后才选回应；代理只能传已有记录，不能替当事人新授权。晚到只能改未来安排或回访报价，不能回滚已完成方法。控制与伤害历史不可被新服务或高声望抹平。\n\n## 跨地域实质影响\n\n|ID|来源与方案→目标|实际变化|限定回应|\n|---|---|---|---|\n'
for e in m['effects']:
 if e['id'].startswith('CX'):
  b+=f"|{e['id']}|{ql(e['source'])}（{e['route']}）→{ql(e['target'])}|{e['change']}|{e['receiver']}：「{e['line']}」；只知{e['receipt']}|\n"
b+='\n## 同城支线与主章\n\n每条CS路线分别回到本地CM，影响的是实际已执行的结果，而非“完成计数”。例如布林工艺分署与学徒离坊为不同地方事实；同主章都能继续，但来源、工具、发言人不同。未做时保本地独立固定核验。每个同城边的回访台词及传达范围见两端台本的交叉影响节。\n\n## 原51篇的归属映射\n\n|旧任务|接入城市／地域|原所有者保留|\n|---|---|---|\n'
for qid,h in m['legacy_home'].items():b+=f"|{ql(qid)}|"+' · '.join(cl[x] for x in h)+'|NE、唯一物件、paid和结局资格仍由该旧任务记账|\n'
b+='\n## 冻结与预算边界\n\nN17终局安全快照独立冻结；回风驿停非必需捷径与维护者拒续约不推翻已验证安全，仍要认地方失约。床位、工班、材料与钱先占用再承诺，实际交接才有接收；口头愿意不解锁archive/托管。新增CM控制路线有便利也有排除与监督缺口，不虚标优选；不同城政治代理不能给全国进口许可、赦免或正式王位。\n\n[[城市与聚落设计总索引]] · [[网状叙事与条件对话规范]] · [[当前任务依赖与状态字典]] · [[当前证据链与结局条件]] · [[叙事交叉影响矩阵]]\n'
write('09_系统逻辑/城市篇章与跨区域任务网.md',b)

sources=[
 ('S64','布林城区与既有任务','https://www.stoneshardwiki.com/zh/towns/brynn/','0.9.4.25','位置与城区；已收录任务；官方背景','四城区和既有任务存在；网页为社区资料，不证明本存档服务已开。'),
 ('S65','Brynn社区背景','https://stoneshard.com/wiki/Brynn','页面未标与本地同版','History/Politics','本轮先前读取成功；再次访问超时，不能称最新重读成功。一年居住习俗只作租约题材，不认引擎公民功能。'),
 ('S66','奥斯布鲁克','https://www.stoneshardwiki.com/zh/towns/osbrook/','0.9.4.25','背景；相关地点；任务','农业村背景保留，新增粮权案不改原领主。'),
 ('S67','曼郡','https://www.stoneshardwiki.com/zh/towns/mannshire/','0.9.4.25','背景；人物与服务','酒业受战争冲击，不混作曼恩。'),
 ('S68','公家办事要“缴费”','https://www.stoneshardwiki.com/zh/quests/vogt-tailor-bribe/','0.9.4.25','流程；服务条件','原付费准入保留，不在新章二次消费相同物品。'),
 ('S69','黄金满地，腐败满地','https://www.stoneshardwiki.com/zh/quests/vogt-smith-bribe/','0.9.4.25','流程；服务条件','原送酒及室内后续保留，新工伤线不替代原商店准入。'),
 ('S70','贿赂督工','https://www.stoneshardwiki.com/zh/quests/vogt-carpenter-bribe/','0.9.4.25','流程；服务条件','原宝石准入保留，新工艺来源不赐全城贸易许可。'),
 ('S71','布林狩猎奇闻','https://www.stoneshardwiki.com/zh/quests/brynn-boar-hunt/','0.9.4.25','工具地窖与真实威胁；分支','新图不重做关门、误认怪物、地下工具店同一反转。')]
b=front('城市设计与原作避让审查','BASE-CITY-AUDIT-S63','research','mixed')
b+='S63是城市篇创作需求；S64—S71为2026-10-12网页调查摘要，只保存有用信息及定位，不复制整页或商业资源。这些网页为社区整理，原作本地文本定位仍优先。版本一致不证明当前存档行为。\n\n|ID|逐页来源|资料版本与定位|避让措施与读取限制|\n|---|---|---|---|\n'
for sid,title,url,ver,loc,note in sources:b+=f'|{sid}|[{title}]({url})|{ver}；{loc}|{note}|\n'
b+='\n## 原作边界逐城核对\n\n布林保留四城区和原任务，新副工场不覆盖督工、海关、印坊老板的既有对白。自由城、旧围城与政治群体是背景；新夜会只代表地方当事人，不能替全城通过新法律。\n\n奥尔德文金工护甲与历史宗教分歧保留，不把古围城当现代废墟；王宫、继承人、现任统治布局未知。斯孔弗特冶炼与战俘题材不挪用原NPC人生。约斯特文按羊毛/帐布传统，不沿用旧亚麻印象。考德仅名称与分类有依据，新寄存院完全原创，不把人名Korde当城主。\n\n曼恩保冷、战乱损伤、迫害风险与学院旧传统，不画已恢复的正常大学城；葛文涅尔去向不因此证实。伊德斯林地和旧木出口不意味着如今自由出货或地方民兵代表全灰军。佛尔霍特金矿不等于北疆犯人石场，不生成无限金库。拉滕旧狂兽已经被杀，不复活同一怪物卖第二次英雄剧情。\n\n十二个命名地点的现行政府布局和确切全球邻接仍未知；城市规模标签只标Mod内容密度。三十三个周边聚落与新街区均原创，不引用为官方地图。\n\n[[王廷与灰色军团聚落清单]] · [[地点设定核对与冲突修订]] · [[既有聚落与原作内容避让]] · [[城市与聚落设计总索引]] · [[来源登记]]\n'
write('01_原作基线/城市设计与原作避让审查.md',b)
(ROOT/'research/city-source-log.json').write_text(json.dumps(dict(date=DATE,sources=[dict(id=sid,title=t,url=u,version=v,locator=l,limit=n) for sid,t,u,v,l,n in sources]),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

b=front('城市美术与图片目录','ART-CITY-S63','art-direction')
b+='## 当前参考式像素概念\n\n[[原素材参考与城市概念图]]汇总十五张独立地域概念板、三十三个卫星构图、各图任务用途和制作修订。图片已接入所有城市和周边聚落笔记，初始及编辑提示词、原参考与输出哈希分别登记。下方旧三联画保留为早期绘画风格对照，当前风格以S74选稿为准。\n\n'
b+='## 已有图片\n\n![三大城原创概念板](城市概念/三大城市概念-v1.png)\n\n上：布林，温暖石市、拥挤租巷、潮水与富裕港口并存；中：奥尔德文，金工护甲的展示与受伤劳动者处于同一工场；下：曼恩，冷色残城与少量暖灯，档案、护理、织工仍有人生活。2026-10-12 imagegen原创生成，未取游戏图集。概念板没有可用于游戏的门坐标、碰撞与图层。\n\n## 各城与周边图纸\n\n'
for c in cs:
 b+=f"- {cl[c['id']]}：[城市通路SVG](城市示意/{c['id']}-layout.svg)；"+'、'.join(f"[{s['name']}通路](城市示意/{s['id']}-layout.svg)" for s in c['satellites'])+'。\n'
b+='\n## 制作前继续细化\n\n现有48张SVG是拓扑示意：节点、两种室内用途与双向回程可核，不是建筑比例图。三大城概念板为一张三联画，不计三张独立制作素材；其余十二地域没有独立风貌概念画。内部分层、独特室内平面、像素尺度、可互动门、光照遮挡及资源复用清单均待后续。不能把“有图片”写成全部地图美术完成。\n\n生成记录在research/city-art-manifest.json；原图复制进本库，未只留工具缓存。[[城市与聚落设计总索引]] · [[城市扩展验收记录]]\n'
write('12_美术参考/城市美术与图片目录.md',b)

b=front('城市扩展验收记录','QA-CITY-S63','validation')
b+='本轮只写设计，不构建、部署或改存档。备份：backups/city-design-20261012-a134943d。新增模型research/city-campaign.json与两份作者脚本可追踪来源；生成笔记哈希在research/city-generated-note-hashes.json。\n\n## 验收口径\n\n|要求|当前状态与证据|\n|---|---|\n|每个命名聚落有地域章|十二聚落＋三原创地域，均见[[城市与聚落设计总索引]]|\n|大城更多任务|布林10、奥尔德文6、曼恩6条新支线；其他地域各3|\n|城内与周边关联|66街区、33卫星各有任务入口/现场/回访；关联在各城卡|\n|各任务多解及后果|73篇初稿，逐路线行动/代价/结果/回访；文学深度与口吻仍待精修|\n|跨城网状影响|30条跨地域条件边，116条同城路线边，30条旧任务双向接入边；[[城市篇章与跨区域任务网]]|\n|原作边界|[[城市设计与原作避让审查]]及既有八城基线卡；现代未知不补成事实|\n|图片|48通路SVG、一张三大城概念板；其余风貌图与比例平面未完成|\n|游戏运行|未实现新城市，未做运行验证|\n\n自动验收为文档/参考条件模型，不证明对白艺术质量、真实床位库存或游戏任务接口。当前仍draft，禁止以任务数量或通过静态检查宣称完整终稿。\n\n[[城市与聚落设计总索引]] · [[城市美术与图片目录]] · [[叙事逻辑校验与修订记录]]\n'
reports=[]
for fn in ['city-validation.json','story-script-validation.json','story-network-validation.json','vault-validation.json','city-art-validation.json','city-task-art-validation.json','shore-vine-task-art-validation.json','city-space-validation.json','brynn-drama-validation.json','aldwynn-drama-validation.json','maen-drama-validation.json','forge-wool-drama-validation.json','shore-vine-drama-validation.json','forest-mine-drama-validation.json','grain-memory-drama-validation.json','names-pass-drama-validation.json']:
 p=ROOT/'research'/fn
 if p.exists():
  report=json.loads(p.read_text(encoding='utf-8-sig'))
  reports.append(f"- `{fn}`：{'通过' if report.get('passed') else '未通过'}，日期{report.get('date')}；{report.get('checks_passed','全库链接与ID检查')}。")
if reports:b+='\n## 已执行检查\n\n'+'\n'.join(reports)+'\n\nBRY通路SVG用独立无界面浏览器渲染并查看：中文标签可读、图片未裁切，截图在artifacts/city-visual-review/BRY-layout.png。其余SVG做XML与路径静态检查，未逐张目视；概念板已目视确认三大城风貌差异，不作为比例和碰撞证据。\n'
write('11_管理/城市扩展验收记录.md',b)

# Promote current scope in existing documents, without erasing historical decisions.
promotions={
'设计总览':'当前城市范围已扩到十二个命名聚落＋三原创地域，入口[[城市与聚落设计总索引]]。六区54节点是保留的早期连接场景，不再代表完整城市稿。N1—N18与S62状态规则继续有效，新CM/CS按[[城市篇章与跨区域任务网]]接入。城市收尾后的追加阶段（特殊地点与野外NPC）入口[[特殊地点与野外NPC阶段验收记录]]：8区域/44地点清点、28名野外人物（中英对照）、44地点卡、16迹象、12文书、条件流与规则审计；剩余经济/比例/运行见[[特殊地点阶段制作与校准规程]]。',
'地图扩张总图':'新增城市/卫星规划见[[城市与聚落设计总索引]]与[[城市美术与图片目录]]。旧六区只作连接场景；新交通是原创拓扑，非原作全球坐标，不能将两组重叠节点预算相加。',
'剧情总纲':'晶石主线N1—N18保持；十五城市篇章与58支线独立收束并互相影响。详见[[城市篇章与跨区域任务网]]。城市全巡不是主线硬前置，地方章不能重新结算NE或N17终局。',
'当前任务依赖与状态字典':'新增resolve_CM/CS与paid是设计命名，详见[[城市篇章与跨区域任务网]]及各台本；本地菜单预览不写，实际确认才写唯一方案，回执范围与费用占用先核。',
'当前证据链与结局条件':'新城市章只产生有限地方回执，不增加NE必收数量、不强制所有城市、不发重复托管资格；N17安全快照仍冻结。[[城市篇章与跨区域任务网]]。',
'势力关系总览':'城市代理的管辖范围各案限定；[[城市与聚落设计总索引]]中的地方班组不能代表全王廷、全灰军或全联盟。城市获救不等于国策改变。',
'人物弧光与关系转折':'新增城市人物卡从[[城市与聚落设计总索引]]进入，实际弧线和有限回应见[[城市篇章与跨区域任务网]]；关系改善不能抹控制、伤害或拒绝。',
'来源登记':'S63为城市扩展创作输入。S64—S71逐页版本、定位与读取限制见[[城市设计与原作避让审查]]；八城本地基线仍保留，三十三卫星全部原创。S74为用户提供原素材参考的概念图制作，逐图引用、提示词、输出版本和限制见[[原素材参考与城市概念图]]。',
'既有聚落与原作内容避让':'下方“奥斯布鲁克/曼郡只作背景”和“新增外港代表布林”为旧范围决策，S63已取代。十二聚落现有独立城市篇章；原生任务服务不覆盖。S64—S71已读相关流程摘要，见[[城市设计与原作避让审查]]。',
'王廷与灰色军团聚落清单':'下方不新增可玩八城是早期限制，现已扩为八城原创纸面篇章，尚未制作。[[城市与聚落设计总索引]]明确各城和卫星设计；原作事实的未知仍有效。'}
for name,body in promotions.items():
 found=list(V.rglob(name+'.md'));assert len(found)==1,name
 p=found[0];t=p.read_text(encoding='utf-8-sig');start='<!-- CITY-S63:BEGIN -->';end='<!-- CITY-S63:END -->'
 block=start+'\n## S63城市扩展（当前范围）\n\n'+body+' 所有新增稿仍draft；本轮未更新游戏包。\n'+end+'\n\n'
 if start in t:t=re.sub(re.escape(start)+'.*?'+re.escape(end)+r'\s*',lambda _:block,t,flags=re.S)
 else:t=re.sub(r'(?m)^(# [^\n]+\n)',lambda x:x.group(1)+'\n'+block,t,count=1)
 p.write_text(t,encoding='utf-8')
for c in cs:
 if c['baseline'].startswith('地点基线_'):
  name=c['baseline'];p=next(V.rglob(name+'.md'));t=p.read_text(encoding='utf-8-sig');start='<!-- CITY-S63:BEGIN -->';end='<!-- CITY-S63:END -->'
  block=start+'\n## S63原创城市规划\n\n'+cl[c['id']]+'包含新的地域章、城内支线与卫星聚落；这些现代布局是Mod原创，并未补成官方事实。旧“暂不新增可玩城市”范围已扩大，游戏实现仍未开始；本卡下方事实和unknown保留。\n'+end+'\n\n'
  if start in t:t=re.sub(re.escape(start)+'.*?'+re.escape(end)+r'\s*',lambda _:block,t,flags=re.S)
  else:t=re.sub(r'(?m)^(# [^\n]+\n)',lambda x:x.group(1)+'\n'+block,t,count=1)
  p.write_text(t,encoding='utf-8')

rule='\n<!-- CITY-S63:BEGIN -->\n2026-10-12 S63：城市范围为十二命名聚落＋三原创地域，设计入口为design/00_导航/城市与聚落设计总索引.md。六区54节点仅早期连接场景，旧限制已被扩展纸面设计取代，不能据此缩回八城。N1—N18、NE与终局保持S62规则；CM地方篇章无全城游历前置，PAS/ASH/HIG为现有任务编排而非第二奖励。新版另用research/city-campaign.json管理城市/卫星/任务/条件回执，运行Validate-CityCampaign.py和原三项检查。通路SVG与概念板只作设计参考，房间美术/经济/运行未经验证不能称完成。\n<!-- CITY-S63:END -->\n'
for p in [ROOT/'CHANGELOG.md',V/'AGENTS.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-S63:BEGIN -->.*?<!-- CITY-S63:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
p=ROOT/'CHANGELOG.md';t=p.read_text(encoding='utf-8-sig');block='\n<!-- CITY-S63:BEGIN -->\n2026-10-12：新增城市/周边设计入口 [城市与聚落设计总索引](design/00_导航/城市与聚落设计总索引.md)，十五地域章与58支线初稿，48通路SVG和三大城概念板。全稿仍draft，具体限制见 [城市扩展验收记录](design/11_管理/城市扩展验收记录.md)。本轮不构建/部署或改存档。\n<!-- CITY-S63:END -->\n';t=re.sub(r'\n<!-- CITY-S63:BEGIN -->.*?<!-- CITY-S63:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+block,encoding='utf-8')
# Reconcile every note-hash manifest for the notes this writer regenerated.
for _hp in sorted((ROOT/'research').glob('*note-hashes.json')):
    try: _h=json.loads(_hp.read_text(encoding='utf-8'))
    except Exception: continue
    if not isinstance(_h,dict) or not all(isinstance(v,str) for v in _h.values()): continue
    _touched=False
    for _rel in list(_h):
        if _rel in changed:
            _new=hashlib.sha256((ROOT/_rel).read_bytes()).hexdigest()
            if _h[_rel]!=_new: _h[_rel]=_new; _touched=True
    if _touched: _hp.write_text(json.dumps(_h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
from CityLinks import add_city_links
hp=ROOT/'research/story-generated-note-hashes.json';hashes=json.loads(hp.read_text(encoding='utf-8'))
for relative,expected in hashes.items():
 p=ROOT/relative
 if hashlib.sha256(p.read_bytes()).hexdigest()!=expected:raise SystemExit('Preserve/reconcile edited earlier note: '+relative)
for relative in hashes:
 p=ROOT/relative;t=p.read_text(encoding='utf-8');p.write_text(add_city_links(ROOT,relative,t),encoding='utf-8');hashes[relative]=hashlib.sha256(p.read_bytes()).hexdigest()
hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('S63 navigation, baseline audit, art directory, rules and legacy backlinks written.')

# Current supplements remain discoverable when older navigation is regenerated.
from BrynnContinuation import apply as apply_brynn_continuation
apply_brynn_continuation(ROOT)
