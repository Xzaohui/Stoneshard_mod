"""S84 scoped character cards, letter text and Korde/pass narrative review."""
from pathlib import Path
import json,hashlib,re
from NotePreserve import preserve_foreign
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));hp=ROOT/'research/names-pass-generated-note-hashes.json';hashes={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if sha(ROOT/rel)!=h:raise SystemExit('Preserve/reconcile edited S84 note: '+rel)
casts={cid:m['dramatic_casts'][cid] for cid in ['KOR','PAS']};qs=[q for q in m['quests'] if q['city'] in casts];cs={c['id']:c for c in m['cities']}
def wl(p):return '[['+Path(p).stem+']]'
def front(t,i,k):return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, dialogue, S84]\naliases: []\n---\n\n# {t}\n\n'
def write(rel,b):
 b=preserve_foreign(V,rel,b)
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(b,encoding='utf-8');hashes['design/'+rel]=sha(p)
def uses(q,key):return any(who==key for s in q['dramatic_scenes'] for who,_ in s['lines']) or any(who==key for pairs in q['dramatic_followups'].values() for who,_ in pairs) or any(f['speaker']==key for f in q['dramatic_feedback'])
for cid,cast in casts.items():
 for key,a in cast.items():
  if a['existing']:continue
  b=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
  for label,field in [('稳定ID','id'),('工作','role'),('所求','desire'),('所怕','fear'),('口吻','voice'),('可能弧线','arc')]:b+=f'**{label}**：{a[field]}\n\n'
  b+='所属'+wl(cs[cid]['file'])+'，本案关系与人物皆Mod原创。关联：'+' · '.join(wl(q['file']) for q in qs if q['city']==cid and uses(q,key))+'\n\n'
  b+='一身份一身体沿真实工作、去向与自愿约见移场，不为另一任务克隆。只说亲历、受准本段事实与实际有限回执；死亡、拒绝、缺席与私密优先，双链不授全城知情。实际交还、入住、托款、护理交班与接收后才确认，钱床柜工班先单记；晚到仅未来，不抹旧史、重发奖或改N17。\n\n[[考德与柏石关人物演出审查]] · '+wl(cs[cid]['space_file'])+' · [[城市篇章与跨区域任务网]]\n'
  write(a['file'],b)
letter=front('列梵的家书与口信','DOC-PAS-LEVAN-ONE-S84','world-text')
letter+='''所属[[台本_CS-PAS-03_关外的最后一封]]，作者[[人物_PAS-NPC-LEVAN_列梵]]，受准接收者[[人物_PAS-NPC-QILEN_绮伦]]。本封为Mod原创，内容只本人愿的一段可读，角色不因拿到物件就全知家庭去向。

## 原信正文

> 绮伦：
>
> 夜里卸到最后一辆车，我常想起家里烧水那声。以前嫌灶边太挤，坐远一点也能听见你们说话；现在觉得能听到就很好。
>
> 我想回来喝一碗热的，也怕这边没结的那班拖着。等这班之后，我会再问能不能回一趟，还没有答过哪天到。别先替我许给家里的人，也不用为我这几句去和别人争一份名册。
>
> 你愿回话就说自己的，暂不愿也不用替每个人应一声。我只想让你知道，我还会想家。想家不是我已经决定了全部以后。
>
> 列梵

## 不留纸的默认口信

「只告诉绮伦，我想家。这班之后我会再问能不能回一趟，还没有答过哪天到。别替我许给别人。」

这一段只是本人可选择的默认文本，可更窄，不能由代理加病史、住址、军役或确定返乡日。绮伦真在场亲耳接才有本次口信回执，后续转述须列梵新准；拒口信或不在场不伪收到。

## 设计物件与单次交接

|设计ID|持有和用途|实际变化|
|---|---|---|
|`PAS-LETTER-LEVAN-ONE`|列梵本封原信，只有真准托递才暂交玩家携带；可在准读范围打开|实际投递交出后原信不仍在玩家背包，作者／可信接收范围核后结本次，不因读过即送达|
|`PAS-LETTER-LEVAN-COPY`|列梵真愿留的副件／本封受准接收回执；不是自动复制原信|可在背包留本次凭，来源／范围与隐私另标；重读不推进、再给付或重新寄一次|
|口信路线|原信先真还本人，玩家无需纸物完成|真实可信接收后结有限这句，纸不在背包不阻该方法|

以上是设计ID，尚非已实现物品。承接[[信件物品与阅读驱动任务]]：阅读仅显示受准文本，不提交方法、造到达或赠新授权。原信、本人准副件与可信接收为同一封的不同状态，不三封奖励；原件送出后只有本人准副件可留，不能同时送出原件、又无授权复制一件作售价或任务道具。

## 与后续人物的关联

雷奥收回本案扣信后仍认扣过，未来雇工要再问；列梵未因送出想家而解除／续签原班。绮伦收到一段不代全家答话，也不让辛娅的量粮柜同时获得整信。监督、护理、岗位与亲属许可分别核，旧N7／SQ02及N17不由信物重写。

[[考德与柏石关人物演出审查]] · [[文书与现场文本台本]] · [[城市篇章与跨区域任务网]]
'''
write('05_主线/城市篇章/文书_PAS_列梵的家书与口信.md',letter)
b=front('考德与柏石关人物演出审查','QA-NAMES-PASS-DRAMA-S84','narrative-audit')
b+='''作者源Author-NamesAndPassDrama.py与Author-NamesPassFeedback.py生成korde／passgate各drama.json、feedback.json；更新前备份backups/city-drama-20261012-s84。本轮只写设计与核对，未改游戏、存档或原N7／SQ02。

## 地域与事实边界

考德原镇史、城主、主业与全球方向仍有unknown，本轮只使用已在库内的原创寄存院、短宿小环路与两卫星布局，不把它写成果园、王宫、矿区或柏石关别名。以两处物刻、相近姓、两块门牌、床钥／物钥、空灯和画背表达事件：帮过可以真帮，代一件不能接成一生；未知脸不靠想有来历补成官方家族。

柏石关为原创R04关隘地域编排，主关卸货轴、石匠道、粮秤、民用护理与家书窗分空间。沿已有雷奥NPC-REY与莫伦NPC-MORREN的一身体、去向和旧责任；城市人物卡只是篇章视图，不新增原角色第二实例。N7配对调查与SQ02冬粮三方法仍保持，原前置未达只登记已见、不造认证。共同地方监督和中立分柜不授全国军需／免税，不把军事急需写无限劳役。

新增家庭、同行、原信、患者与画案全部Mod原创。[[城市设计与原作避让审查]]保事实与未核边界；风貌沿[[原素材参考与城市概念图]]，空间见[[空间_KOR_考德]]与[[空间_PAS_柏石关与关外聚落]]。

## 八案覆盖

|任务|场次|原方法|早／晚回访对|
|---|---:|---:|---:|
'''
for q in qs:b+='|'+wl(q['file'])+f"|{len(q['dramatic_scenes'])}|{len(q['routes'])}|{len(q['dramatic_feedback'])}|\n"
b+='\n24场、16原方法、48组现场答复、28旧传入边（两地各14）；20演员含12新增卡及一封独立信文本。73任务、314边、原stages／方法／NE／奖励／N17保持；S84 dramatic_scenes是当前逐句稿，旧示意人物不配新对白。\n\n'
b+='''## 相互影响与人物弧线

|关系|跨案变化|不会自动消掉的事|
|---|---|---|
|诺妲／埃文／塔斐|本件真领或争段限存先住，修款与代理单记；另案单件代理先例不能代埃文取物|拼姓、过说家属与实垫款各真有；认物不认全权，拒全权不免真实旧修款|
|玛迪／娜娅／缺席兰衍|一晚信清租或真封争款，娜娅自选这晚；空灯与画中未知脸都是可等待而非可伪认证|玛迪少月款可能关闲屋，妹妹仍想等或走；退款不买放下，未知消息不判死亡／到达|
|赛洛／尤恩／卢绫／阿霖|本人领或真愿单件代理，同住另选；修门人限见证可能少订单|两家照顾真实，长辈仍可能不习惯新称呼；不同户、埃文与赛洛不合一，成年不展血脉奖|
|碧珞／榭兰／玛迪|未知价真售一幅，或真有限留展；画款与床／柜费先占|虚城主故事认本笔，盼知道脸是谁真实却不是来源；低价／无即期收入、少宣传收益真少|
|雷奥／莫伦／莎帛／礼昂／辛娅|本地自愿共同核或中立分柜，普通床／护理主持真交；实名／编号各本人范围|印真不免多征／漏人，主持不能只改表仍旧权，礼昂不代N7两患者，不回发技术与CO资格|
|乌珀／沃汀／雷奥|旧薪真兑后自愿有限续班，或限旁路、工人真收工；护路费与民粮检费分别扣|乌珀专业自豪可与疲累并存，沃汀催班和雷奥拖薪留；人能走不等大件已验或旧薪已付|
|列梵／绮伦／雷奥|原信实际交还本人后真托递，或真有限口信；作者与接收者都不是全家代理|想家不定逃岗，信真到不保证亲属回话、合同解除；旧扣信留，不重演罗温旧逃兵案|

## 原任务接入而非重新认证

原N7 inspection／parallel／withdraw实际结果与已造成伤害照留。没有完成时仍按真实床旁、固定副联、停机日志等原方法与前置核，不拿礼昂普通连续记录替装置配对的两位。研究与基本护理分问，拒技术新用途不取消受准普通照护；不再危害患者制造新证据。莫伦若不在场只固定受准资料限核，不复制其身体回来主持。

原SQ02 restitution／rationing／military各保。原military留下民粮欠且无assent_CO，CM-PAS joint不能凭同桌把它翻成CO已准；后续补偿要实际给付且走原资格条件。本章只编排真实已有结果与新增本地范围，不重新结N7、SQ02、旧日常或CO奖励。已补粮、旧薪托柜、外检费、护班与床单账；纸上检费不足不装到账。

## 实际身体与分项出口

|情形|具体规则|
|---|---|
|埃文已到、兰衍未到、赛洛成年|三者独立身份；缺席兰衍仅受准旧信署名存在，不生成到场角色；娜娅是妹妹但不新签哥哥整月|
|同姓／两门／画中脸|只受准刻记、旧用痕与画背可核本物，不定全家血缘／官方族史，不逼年轻人先认唯一亲情|
|物权未核与住所需真实|真中立争柜与受准有限保管费，普通独立租住真接；柜暂不动不能把人也扣住，床柜钥分开|
|一晚信／空灯／月租|实住、受准预留和驿主自愿等分别核；未准款真退或真柜封，缺钱留欠，不生无限第三床|
|礼昂两种记名|先真实同人本案连续核，一个身体一床一份实际量；实名可愿、编号可愿，都不接全病史地址或研究|
|停工与旁路|固定无人样段限荷载，专业工班实做；工资兑不绑未来班，停牌不封普通离关路，大件慢照实|
|信与口信|[[文书_PAS_列梵的家书与口信]]保独立私密文本；原件送出不仍在包，只有本人准副件可留，口信可无纸，不重复送／奖|
|死亡／拒绝／缺席|本人句停，只固定受准事实与合法限权接续；不生新亲属／研究／投递／续岗授权，不索全部私史来换基本服务|

早到回执分别改下一次真实范围、价格与费用来源；晚到只未来，已取物、实住床、交画、实薪、送信不重来。CX14曼恩分用途、SQ08传信范围、CX22矿区独立检费及N7公开本案范围只提供有限先例，不传整城状态／病例，不夺本人许可；无旧先例仍有本地固定基础线索。实际涉及原技术或CO的条款必须按原前置和原完成确认，不伪“全城已授权”。
'''
remaining=sum('dramatic_scenes' not in q for q in m['quests'])
b+=f'\n## 当前阶段\n\n{73-remaining}/73篇城市任务有逐角色初稿，尚{remaining}篇待同等深化。Validate-NamesAndPassDrama.py核源／渲染、三位身份、同人单床、原技术／资格与28旧边；原设计检查核双链、依赖与条件回执。数值经济、详细时间轴、比例地图、文学终审及游戏运行仍未验收，静态通过不等整体完成。\n\n[[城市与聚落设计总索引]] · [[城市篇章与跨区域任务网]] · [[任务空间与地点关联审查]] · [[城市扩展验收记录]]\n'
write('11_管理/考德与柏石关人物演出审查.md',b);hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule=f'\n<!-- CITY-DRAMA-S84:BEGIN -->\n2026-10-12 S84：考德／柏石关八案源为korde／passgate各drama.json与feedback.json，入口design/11_管理/考德与柏石关人物演出审查.md；24场、16方法、28回执、12新卡、一封独立家书。考德物／房／代理分，族史unknown；埃文、兰衍、成年赛洛分人。雷奥莫伦同原身体，一床单占，N7／SQ02方法与CO真条件保，不二奖；原信送出不留原件、本人准副件可背包，口信不强纸。当前{73-remaining}篇逐角色稿、{remaining}篇待深化，运行Validate-NamesAndPassDrama.py及既有检查；数值、比例图与游戏未验收。\n<!-- CITY-DRAMA-S84:END -->\n'
for p in [ROOT/'CHANGELOG.md',V/'AGENTS.md',ROOT/'CHANGELOG.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S84:BEGIN -->.*?<!-- CITY-DRAMA-S84:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(quests=8,scenes=24,methods=16,choices=48,incoming_pairs=28,actors=20,new_cards=12,world_texts=1,notes=len(hashes),covered=73-remaining,remaining=remaining),ensure_ascii=False))
