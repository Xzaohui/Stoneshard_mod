"""S86 scoped rendering: change the final eight tasks, preserve the other 65."""
from pathlib import Path
import json,hashlib,re
from AdditionalCityDrama import apply_city
from CityDrama import render_scenes,render_method,render_exceptions
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';AUDIT='寒凉盆地与修院山地人物演出审查'
MARK='CITY-DRAMA-S86';hp=ROOT/'research/care-highland-generated-note-hashes.json'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def wl(p):return '[['+Path(p).stem+']]'
def front(t,i,k):return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, S86, dialogue]\naliases: []\n---\n\n# {t}\n\n'
manifests={}
for p in (ROOT/'research').glob('*note-hashes.json'):
 h=read(p)
 if not isinstance(h,dict) or not all(isinstance(x,str) for x in h.values()):continue
 for rel,expected in h.items():
  if sha(ROOT/rel)!=expected:raise SystemExit('Preserve/reconcile prior note: '+rel)
 manifests[p]=h
model=read(ROOT/'research/city-campaign.json');existing={}
for c in model['cities']:
 for name,role,arc,pid in c['people']:existing[pid]=f'04_人物/城市人物/人物_{pid}_{name}.md'
 for s in c['satellites']:existing[s['resident']['id']]=s['resident']['file']
for cast in model['dramatic_casts'].values():
 for a in cast.values():existing[a['id']]=a['file']
for cid,slug in [('ASH','ashcare'),('HIG','highland')]:apply_city(ROOT,model,existing,cid,slug,'S86')
model['dramatic_scope']='Active authored cities: '+', '.join(model['dramatic_casts'])+'; all 73 baseline quests have current authored scenes; six Brynn continuation quests remain in their registered supplement.'
cs={c['id']:c for c in model['cities']};qs=[q for q in model['quests'] if q['city'] in ['ASH','HIG']]
casts={c:model['dramatic_casts'][c] for c in ['ASH','HIG']};changed=set();generated={}
def put(rel,t,own=False):
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8');k='design/'+rel
 changed.add(k)
 if own:generated[k]=sha(p)
def block(t,b):
 a=f'<!-- {MARK}:BEGIN -->';z=f'<!-- {MARK}:END -->';n=a+'\n'+b.rstrip()+'\n'+z
 return re.sub(re.escape(a)+'.*?'+re.escape(z),lambda _:n,t,flags=re.S) if a in t else t.rstrip()+'\n\n'+n+'\n'
def attach(rel,b):put(rel,block((V/rel).read_text(encoding='utf-8-sig'),b))
for q in qs:
 t=(V/q['file']).read_text(encoding='utf-8-sig')
 t,n=re.subn(r'## 场次与对白[^\n]*\n.*?(?=## 可执行方案与回访)',lambda _:render_scenes(q,model),t,flags=re.S)
 assert n==1,q['id']+' scenes section'
 b='## 可执行方案与回访\n\n'
 for r in q['routes']:
  b+=f"### {r['key']}：{r['label']}\n\n**实际行动**：{r['action']}\n\n**代价**：{r['cost']}\n\n**地方结果**：{r['result']}\n\n"+render_method(q,r,model)
 t,n=re.subn(r'## 可执行方案与回访\n.*?(?=## 状态、资源与奖励)',lambda _:b,t,flags=re.S);assert n==1
 t=re.sub(r'## 本案中断与到达顺序（S86）\n.*?(?=## 交叉影响)',lambda _:'',t,flags=re.S)
 t=t.replace('## 交叉影响\n',render_exceptions(q,model)+'## 交叉影响\n',1)
 if q['id']=='CS-HIG-03':
  t=t.replace('到本地入口得知实际事件；接受、旁观、拒绝均可。拒绝只暂停本案，原生服务/晶石主线保持。无跨城硬前置；现场固定基础线索足够进入。',
   '正式一次事件只在N17真实威胁后安全桌冻结后触发；此前可查旧工资/工约，不能演离任结算或井关句。拒绝本案不影响原主线；本案不是N17前置。')
 b='## 当前R/X与地域所有权\n\nR：'+ ' / '.join(r['key'] for r in q['routes'])+'；实际动作/交接之后确认，预览不写。X：'+ ' · '.join(f['effect'] for f in q['dramatic_feedback'])+'。\n\n'
 b+='此处S86逐角色稿为当前稿，原stages仅地理骨架。'+('地域主章只编排原任务结果，不第二授NE/救济/结局。' if q['kind']=='regional-main' else '这是一次人物事件，非普通运输/维修/清运的重复委托。')
 b+=f' [[{AUDIT}]] · [[文书_ASH-HIG_钥匙与班次短记]]。\n'
 # Top-of-screenplay R/X supersedes the sketch and preserves existing space links.
 a=f'<!-- {MARK}:BEGIN -->';z=f'<!-- {MARK}:END -->'
 t=re.sub(re.escape(a)+'.*?'+re.escape(z)+r'\s*','',t,flags=re.S)
 t=re.sub(r'(?m)^(# [^\n]+\n)',lambda m:m.group(1)+'\n'+a+'\n'+b+z+'\n',t,count=1)
 put(q['file'],t)
def uses(q,key):return any(w==key for s in q['dramatic_scenes'] for w,_ in s['lines']) or any(w==key for pairs in q['dramatic_followups'].values() for w,_ in pairs) or any(f['speaker']==key for f in q['dramatic_feedback'])
for cid,cast in casts.items():
 for key,a in cast.items():
  related=' · '.join(wl(q['file']) for q in qs if q['city']==cid and uses(q,key))
  if a['existing']:
   attach(a['file'],f'## S86同一人物的地域事件\n\n[[{AUDIT}]] · {related or wl(cs[cid]["file"])}。同一ID/身体按真实位置、愿见与受准记录演出；旧伤/控制/拒绝保留。赫斯若原死亡/敌对/不可约见不生新会面，米娅只替自己答，不代表全营。')
   continue
  t=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
  for label,k in [('稳定ID','id'),('身份','role'),('所求','desire'),('所怕','fear'),('口吻','voice'),('跨案弧线','arc')]:t+=f'**{label}**：{a[k]}\n\n'
  t+='原创人物；所属'+wl(cs[cid]['file'])+'。本人的当前台本：'+related+f'。\n\n[[{AUDIT}]] · '+wl(cs[cid]['space_file'])+'\n\n一身体按真实班次/去向移场，已到这一班不同时到另一处。本人存活/在场/愿谈并具该句来源才发言；死亡、缺席、拒绝、用途授权优先。实际款、物、班、职责交接再确认；更正不删旧过，新的愿意只管未来。\n'
  put(a['file'],t,True)

world='文书_ASH-HIG_钥匙与班次短记'
t=front(world,'DOC-CARE-HIGHLAND-S86','world-text')
t+='这些为Mod原创可选背包短件；不是原作物品/现已实现功能。长材料分存，不塞对白，也不要求收齐这些纸。实际现场见证/原有限柜核是替代入口。读过只获准文本，不提交方法、发奖、假交接。\n\n'
docs=[('S86-KEY','妮蔻取物范围','CS-ASH-01','只准毯子和锅。私柜不准翻；屋的共住争议未判，取物不放弃旧权。'),
 ('S86-SHIFT','枯恩本次交班','CS-ASH-02','先写真实到班人和这一段时间。护理所需只本用途；奥娅休息不等以后每班已签。'),
 ('S86-BOWL','普通柜与观察柜','CS-ASH-03','本批普通给量按实际需要与库存记；观察另问，拒绝不扣普通水。未到物/未停工时留空。'),
 ('S86-STOP','本段停牌范围','CS-HIG-01','停的是本段捷径，绕行另标。只有实际验修后的核范围可填开放；钱不是梁没裂的证明。'),
 ('S86-MARK','司榆原数与补笔','CS-HIG-02','原数、补笔和实测版分栏。复测不稳留不稳，支架一件不变全山安全；必要公开纠错不抹旧错。'),
 ('S86-KEYBACK','一班工约与交钥','CS-HIG-03','旧已做薪与新工约分。未续不是自愿永久留下；必要职责真接才记已交，非必需停用不回滚N17。')]
byq={q['id']:q for q in qs}
for did,name,qid,body in docs:
 t+=f'## {did}：{name}\n\n所属：{wl(byq[qid]["file"])}。\n\n候选短文：「{body}」\n\n仅本人实际准许范围的副件可留背包；原件交出不仍持有，未做字段不自动填，价格/护理/医疗私料分用途，不卖全户地址。遗失去原有限柜/受准现场复核同一事实，不重新给物/款。\n\n'
t+=f'[[{AUDIT}]] · [[文书与现场文本台本]] · [[城市与聚落设计总索引]]\n'
put('05_主线/城市篇章/'+world+'.md',t,True)

t=front(AUDIT,'QA-CARE-HIGHLAND-DRAMA-S86','narrative-audit')
t+='作者源Author-CareAndHighlandDrama.py、Author-CareHighlandFeedback.py；输出ashcare/highland的drama与feedback.json。前置备份backups/city-drama-20261012-s86，改的是设计和作者工具，游戏/存档/部署包未改。上一轮完成布林六案和原作复核属于实际进展；本轮继续原范围最后八篇，不缩回只写城市总纲。\n\n'
t+='## 两地特色与任务空间\n\n寒凉盆地的生活道、生活水与新管、旧屋钥窗、干堤轮班、拒观察等候屋分别服务“被救之后还要怎样生活”。妮蔻的毯、缇安抓着的钥绳、奥娅没洗的锅、枯恩要的具体一步、苏奈靠柜放的邀请，都是人物关系里的实物线索；不是收三份文书。病源/护理/迁居/研究/救济/问责分账，不写医学奇迹或患者全体同愿。\n\n修院山地的旧钟回程棚、稳定外道、裂梁旁停牌、固定三刻槽、分席议屋、外道付薪亭和离任钥间分别服务“深入之前能否回来、结束之后谁还愿留下”。蕾因的免等广告、司榆补笔、古菈的一班、艾萝夸大铭牌有自己的责任；精确图形不是核心认证，拒听不锁原旁路，少展示不重开井。普通工作由当地人运行，玩家只参与一次真实关系转折。\n\n'
t+='## 八案逐角色稿\n\n|当前台本|场次/方法|传入回执对|\n|---|---|---|\n'
for q in qs:t+=f'|{wl(q["file"])}|{len(q["dramatic_scenes"])}/{len(q["routes"])}|{len(q["dramatic_feedback"])}|\n'
t+='\n24场、16原方法、48组现场问答、31组早/晚回访；16名演员含八新配角卡，另六段独立短文本。原73篇/314单方法回执保持结构和所有者，布林六续篇/15桥组另存，共79篇现在都有逐角色初稿。纸面覆盖不是文学终审/游戏验收。\n\n'
t+='## 人物弧光与互相影响\n\n'
for cid,cast in casts.items():
 for key,a in cast.items():
  if not a['existing']:t+=f'- {wl(a["file"])}：{a["arc"]}\n'
t+='\n妮蔻同意代取不授住权放弃；奥娅的休息不买枯恩的研究许可；安妮每一真实班只能占一次，停止观察释放的是实际工时。苏奈可丢下一份差事，不能拿害怕逼患者补数据。主章晚到只改未来，已去/已留都不改原迁居历史。\n\n赫珀真停梁不成为整山反对者，蕾因得认自己的免等承诺；图里验段不免费继承下一班。司榆负责自己补笔，不由赫斯代认；赫斯原伤害/控制不因新表洗掉。古菈旧工资不能靠续约领取，艾萝删“永久”仍曾写过；离任的必要交接真有人接才完，不拿缩展示假称所有义务齐。\n\n'
t+='## 跨城与原章边界\n\n丹布里的床/轮住、约斯特文的暖布、矿区的停班底薪、曼恩的有限迁出分别是有限回执，不克隆资源或人员。暖布实际到件才抵料；空床仍需本人/实接，迁出名单不变新劳工。\n\nCM-ASH只编排N8/N12/N13/SQ05/SQ07；普通护理与正式relief不同，SQ07 patron不由地方主章补资格，NE4仍原核。CM-HIG只编排N14—N17；校表非NE5、图非核心安全。CS-HIG-03只在原N17真实冻结后正式触发，DT15/DT16仍原一次事件所有者；玩家不循环维修维持结局。\n\n'
t+='## 后续全局收尾，仍未证明完整设计完成\n\n79篇都有逐角色初稿，尚须全网核实际接收能力、有限金额/材料/时间轴、多人先后顺序与来源知识，抽读各城戏剧质量并细化比例地图/资源映射。原作事实冲突和特殊地点/野外NPC计划继续保留，城市与全局逻辑未收尾不跳阶段。Validate-CareAndHighlandDrama.py及原三项检查只验证已覆盖静态约束，不能由绿色检查宣布终稿已获认可或游戏可运行。\n\n'
t+=f'[[城市与聚落设计总索引]] · [[城市篇章与跨区域任务网]] · [[任务空间与地点关联审查]] · [[{world}]] · [[特殊地点与野外NPC对白扩展计划]]\n'
put('11_管理/'+AUDIT+'.md',t,True)
summary=f'## S86护理与山地人物演出\n\n[[{AUDIT}]] · [[{world}]]。两地八案由当事人说话，24场/16方法/31早晚回访，八新配角。现73篇基线与六布林续篇均有逐角色初稿，共79篇；仍需全网经济/时间/空间/知识与文学审查，不称终稿或已实现。'
for cid in ['ASH','HIG']:
 attach(cs[cid]['file'],summary);attach(cs[cid]['space_file'],summary)
 for s in cs[cid]['satellites']:attach(s['file'],summary)
for name in ['城市与聚落设计总索引','城市扩展验收记录','任务空间与地点关联审查','特殊地点与野外NPC对白扩展计划','任务台本总索引','新区域设计与任务总表','人物弧光与关系转折','城市篇章与跨区域任务网','文书与现场文本台本']:
 p=next(V.rglob(name+'.md'));attach(p.relative_to(V).as_posix(),summary)
(ROOT/'research/city-campaign.json').write_text(json.dumps(model,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p,h in manifests.items():
 if p==hp:continue
 for rel in changed & h.keys():h[rel]=sha(ROOT/rel)
 p.write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
hp.write_text(json.dumps(generated,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule=f'2026-10-12 S86：寒凉盆地/修院山地八案由ashcare/highland的drama.json与feedback.json驱动，入口design/11_管理/{AUDIT}.md。24场/16原方法/31旧回执/八新卡/六短文本；妮蔻与枯恩分别答、奥娅休息非弃人，真实普通护理不买研究/relief；支架非NE5，司榆补笔/赫斯旧控制留史；古菈旧工资独立、新班再问，缺必需交接保待办，N17不改。现73基线+六布林续篇=79逐角色初稿；全网数值/时间/比例/文学与游戏未验收。运行Validate-CareAndHighlandDrama.py及原三项设计检查，本轮不部署。'
for p in [ROOT/'AGENTS.md',V/'AGENTS.md',ROOT/'README.md']:p.write_text(block(p.read_text(encoding='utf-8-sig'),rule),encoding='utf-8')
print(json.dumps(dict(quests=8,scenes=24,methods=16,incoming_pairs=31,new_cards=8,covered_baseline=73,covered_combined=79),ensure_ascii=False))
from BrynnContinuation import apply
apply(ROOT)
