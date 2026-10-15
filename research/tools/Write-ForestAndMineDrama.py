"""S82 character cards and authored cross-region review for the design vault."""
from pathlib import Path
import json,hashlib,re
from NotePreserve import preserve_foreign
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));hp=ROOT/'research/forest-mine-generated-note-hashes.json';hashes={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if sha(ROOT/rel)!=h:raise SystemExit('Preserve/reconcile edited S82 note: '+rel)
casts={cid:m['dramatic_casts'][cid] for cid in ['EED','FOR']};qs=[q for q in m['quests'] if q['city'] in casts];cs={c['id']:c for c in m['cities']}
def wl(p):return '[['+Path(p).stem+']]'
def front(t,i,k):return f'---\ntitle: "{t}"\nid: {i}\ntype: {k}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: 2026-10-12\ntags: [stoneshard, dialogue, S82]\naliases: []\n---\n\n# {t}\n\n'
def write(rel,b):
 b=preserve_foreign(V,rel,b)
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(b,encoding='utf-8');hashes['design/'+rel]=sha(p)
def uses(q,key):return any(who==key for s in q['dramatic_scenes'] for who,_ in s['lines']) or any(who==key for pairs in q['dramatic_followups'].values() for who,_ in pairs) or any(f['speaker']==key for f in q['dramatic_feedback'])
for cid,cast in casts.items():
 for key,a in cast.items():
  if a['existing']:continue
  b=front(Path(a['file']).stem,'CITY-NPC-'+a['id'],'character')
  for label,field in [('稳定ID','id'),('工作','role'),('所求','desire'),('所怕','fear'),('口吻','voice'),('可能弧线','arc')]:b+=f'**{label}**：{a[field]}\n\n'
  b+='所属'+wl(cs[cid]['file'])+'，身份与家庭经历为Mod原创。关联：'+' · '.join(wl(q['file']) for q in qs if q['city']==cid and uses(q,key))+'\n\n'
  b+='同一身体按真实去向、工作与本人许可约见，不在每案复制一次。死亡、缺席、拒绝与隐私优先；只说亲历、受准本段材料或已收到的有限回执。双链不授全城知情。余料、钱、份、床与工班单账，实际支付／交还／安置／专业处置后才确认；晚到改未来，不改旧史、奖励或N17。\n\n[[伊德斯与佛尔霍特人物演出审查]] · '+wl(cs[cid]['space_file'])+' · [[城市篇章与跨区域任务网]]\n'
  write(a['file'],b)
b=front('伊德斯与佛尔霍特人物演出审查','QA-FOREST-MINE-DRAMA-S82','narrative-audit')
b+='两地主章＋六支线的逐角色初稿，作者源为Author-ForestAndMineDrama.py、Author-ForestMineFeedback.py及eeders／forholt各drama.json与feedback.json。更新前备份backups/city-drama-20261012-s82，本轮未修改游戏或存档。\n\n'
b+='''## 地域与原作边界

伊德斯用木纹、旧梁、弯试片和林段哨声承载冲突。出口减少是实损，住户仍有屋顶也是实需；藏申诉的锯工、想退款又缺现钱的买方、借过屋也逼迁的屋主各有自己的责任。地方料棚与巡点不代表全国民兵总部，不解除全线贸易限制。传统弓料、住屋梁与本批已付木材分别核，不能用改一项方法便得到其它全部许可。

佛尔霍特用班签、风带、少量粗矿、停班饭钱和家杯承载冲突。困人先救、制度后谈，伤者真出井后才说自己的去留；历史纹杯只核物源与受准记忆，现役骑卫存续继续待核。矿份不是黄金现金，地方资金缺口要实际认；旧工资、底薪、检费、水款与继份不是同一项可以反复付款的奖励。

新增人物、私契、家庭经历和支井事件全部Mod原创。既有事实与unknown见[[城市设计与原作避让审查]]；总览参考[[原素材参考与城市概念图]]，空间见[[空间_EED_伊德斯]]与[[空间_FOR_佛尔霍特]]，已有概念图不因此完成比例地图与可走房间。

## 八案覆盖

|任务|场次|原方法|早／晚回访对|
|---|---:|---:|---:|
'''
for q in qs:b+='|'+wl(q['file'])+f"|{len(q['dramatic_scenes'])}|{len(q['routes'])}|{len(q['dramatic_feedback'])}|\n"
b+='\n共24场、16原方法、48组现场选项答复、29条旧传入边（伊德斯14、佛尔霍特15），两城18名人物含10新增卡。保73任务地理骨架、314边、原方法、NE、奖励和N17；dramatic_scenes为S82当前对白，stages为地理素材。\n\n'
b+='''## 人物弧线与交叉影响

|关系|实际改变|不会被结案抹掉的事|
|---|---|---|
|奥菈／芦雅／黎恩|旧材交一部分与退对应款各损信誉和工期；工人独立报价、地方料量与搜家权限分开|藏申诉、误指外城盗材和先搜家仍留；一次交好木不能恢复无限信任|
|苏槿／葛黎／欧莎|有限病伐不补健康树；旧料改法慢、长料少，先扣试件再看主章余量|假病签和照签失查留史；葛黎可留学而非被迫离乡证明成长；改法不等工艺全公开|
|布泽／岱里／芦雅|逐户真实安置才拆梁，卖款先付迁居；保屋换旧料则桥贵且晚|旧借住有真实善意，早收款与逼快也真有责任；岱里曾想走不使拒搬变虚伪|
|朔娅／佛兰／欧莎／黎恩|限原岗读取或独立巡点各有限人手；真实旧债与安全告警另谈|旧地址已泄露不靠删下一页恢复秘密，债也不靠匿名清零；不再找母亲仍要认旧威吓|
|玛诺／艾珀／科蔚／西婕|维护真停权或外检托柜各付实际费用，普通救援不等制度确认|先报矿后报人的误报、挪维护钱与照开责任留；外检不授病例、工资或整矿终身安全|
|艾钦／祁铎／科蔚|杯限历史展示或家内存；继份与工班拆开或售受准份，每项分授权|祖父杯、父亲不停班、哥哥本次伤不是一个人一段事；不复井／不展示不叫背叛，卖份少未来收入|
|蓓娜／洛芙／科蔚|赔付与持续隔流，或临停与真外水；水款先占使底薪需余款|不强她留村做英雄，迁走不替全村买沉默；未知病因留未知，不让患者试喝取证|

## 真实有限账与时序

EED同一梁分别记来源、权利、现住用途、专业可拆段、已有承诺和实装航次。住户真安置与路费先到，住梁才可拆；其它旧料先按主章／弓样／桥工占用去重，涨水停装保高堤。退款若受款者准明确分期，未退仍欠；普通拆运由专业班执行，不做十梁、十屋收集任务。主章不要求先巡三支线，支线可先做但不替后续本人签其它权利。

FOR矿份先分合法权利、本案已冻段、真可兑余量与未来未知收益，不能把纸上价格当金币。救援立即停危险段且专业执行；工资制度可后谈，未确认者保待查不靠失声报全死全活。已付底薪、外检、水处理、继份售款各是一次真实支出；出售本金不自动捐回池。恢复井段需要实际公开复验与本人新劳动许可，伤者不因救助欠复井。技术检只本段、有限时效与费用，生活水不凭风检认证。

## 身体、权限与多解出口

|情形|实际处理|
|---|---|
|祁铎未真出井|只用公开固定班签与受准有限账询问，不演其新同意；救援仍先进行。已出／未出／专业确认分别记|
|多人住旧屋|岱里不是全家代理，每位实际住者各许可、各真实接收；拒者保屋，住梁未安置不拆|
|拒家名、私图、病史、宣传|公开林段／固定木样／班签／受准账可限核，拒公开不取消普通服务，不抢读家中柜|
|拒退款分期、拒空地迁居|没现金或接收则待办，不能把预览当到账；可用真实独立购料或保守停段出口|
|拒复井、拒售份|旧薪与继份请求按本笔独立核；可留收益不下井，不强离乡来证明自主|
|专业样证据不全|树段围护、井段保守停、已核支流临停与实有替水；未知保留，不再置人危险验证|
|人物死亡／不在|本人句停止，只允许固定事实与合法受准有限接续；不生死者新同意，不复制同名演员|

已有跨城边分别传CX03布林工人席位、SQ04旧桥有限核验、CX16危险段停检、CX21分柜问责与N14公开先例。回执不搬来原人物、不授全国代理，不带未准病例地址；每边分别写早到改变实际报价／权限与晚到只谈未来。晚到不改旧resolve、已付项、伤害、库存、奖励或N17。
'''
remaining=sum('dramatic_scenes' not in q for q in m['quests'])
b+=f'\n## 阶段与检查\n\n当前{73-remaining}/73篇城市任务有逐角色初稿，尚{remaining}篇待同等深化。Validate-ForestAndMineDrama.py核源／渲染、旧边与领域门槛，原设计检查核双链、依赖及地图通路意图；数值经济、全局时间轴、比例图、最终文学评审与游戏运行仍未验收，不据静态通过称全稿完成。\n\n[[城市与聚落设计总索引]] · [[城市篇章与跨区域任务网]] · [[任务空间与地点关联审查]] · [[城市扩展验收记录]]\n'
write('11_管理/伊德斯与佛尔霍特人物演出审查.md',b);hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule=f'\n<!-- CITY-DRAMA-S82:BEGIN -->\n2026-10-12 S82：伊德斯／佛尔霍特八案逐角色源为eeders／forholt的drama.json、feedback.json；入口design/11_管理/伊德斯与佛尔霍特人物演出审查.md。24场、16方法、29旧回执，10新卡；住梁未安置不拆，索名撤权不清旧泄露，救援立即执行、伤者真出井才演新句；矿份非金币，底薪／水款／检费／售款各真实占一次。当前{73-remaining}篇逐角色初稿、{remaining}篇待深化；旧314边、NE／奖励／N17保留，运行Validate-ForestAndMineDrama.py与既有检查，数值、比例地图和游戏未验收。\n<!-- CITY-DRAMA-S82:END -->\n'
for p in [ROOT/'CHANGELOG.md',V/'AGENTS.md',ROOT/'CHANGELOG.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-DRAMA-S82:BEGIN -->.*?<!-- CITY-DRAMA-S82:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(quests=8,scenes=24,methods=16,choices=48,incoming_pairs=29,actors=18,new_cards=10,notes=len(hashes),covered=73-remaining,remaining=remaining),ensure_ascii=False))
