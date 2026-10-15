"""Render S75 architecture intent and explicit task location review in the Obsidian vault."""
from pathlib import Path
import json,hashlib,re
from NotePreserve import preserve_foreign
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design';DATE='2026-10-12'
m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));qs={q['id']:q for q in m['quests']}
old=json.loads((ROOT/'backups/city-spaces-20261012-s75/research/city-campaign.json').read_text(encoding='utf-8'));oq={q['id']:q for q in old['quests']}
hp=ROOT/'research/city-space-note-hashes.json';hashes={}
if hp.exists():
 for rel,h in json.loads(hp.read_text(encoding='utf-8')).items():
  if hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()!=h:raise SystemExit('Preserve/reconcile edited S75 note: '+rel)
def wl(file):return '[['+Path(file).stem+']]'
def front(title,ident,kind):
 return f'---\ntitle: "{title}"\nid: {ident}\ntype: {kind}\nstatus: draft\ncanon: mod-original\nbaseline: "0.9.4.25-modbranch"\nupdated: {DATE}\ntags: [stoneshard, city-space, S75]\naliases: []\n---\n\n# {title}\n\n'
def write(rel,body):
 if m.get('dramatic_casts',{}).get('KOR') and m.get('dramatic_casts',{}).get('PAS') and rel in ['02_世界与地图/任务空间/空间_KOR_考德.md','02_世界与地图/任务空间/空间_PAS_柏石关与关外聚落.md','11_管理/任务空间与地点关联审查.md']:
  body+='\n寄存／关口两地八篇当前对白见[[考德与柏石关人物演出审查]]；埃文、赛洛、兰衍分人，床／柜／画分项；雷奥莫伦沿原身体，一人单床、原技术资格独立，缺席不造新签。\n'
 if m.get('dramatic_casts',{}).get('OSB') and m.get('dramatic_casts',{}).get('RAT') and rel in ['02_世界与地图/任务空间/空间_OSB_奥斯布鲁克.md','02_世界与地图/任务空间/空间_RAT_拉滕.md','11_管理/任务空间与地点关联审查.md']:
  body+='\n粮村／纪念地域八篇当前对白见[[奥斯布鲁克与拉滕人物演出审查]]；芙朵学艺与蔻芙婚约分户，普通水路与牲口回路独立；伪响撤后仍真护新风险，退款／赔付／护费不复用。\n'
 if m.get('dramatic_casts',{}).get('EED') and m.get('dramatic_casts',{}).get('FOR') and rel in ['02_世界与地图/任务空间/空间_EED_伊德斯.md','02_世界与地图/任务空间/空间_FOR_佛尔霍特.md','11_管理/任务空间与地点关联审查.md']:
  body+='\n林地／矿区八篇当前对白见[[伊德斯与佛尔霍特人物演出审查]]；住梁未准不拆，救援不等选停班制度，矿份非金币，已占料／款／班单记。\n'
 if m.get('dramatic_casts',{}).get('DEN') and m.get('dramatic_casts',{}).get('MNS') and rel in ['02_世界与地图/任务空间/空间_DEN_丹布里.md','02_世界与地图/任务空间/空间_MNS_曼郡.md','11_管理/任务空间与地点关联审查.md']:
  body+='\n丹布里／曼郡八篇当前对白与住处、转运、来源及有限产业交叉见[[丹布里与曼郡人物演出审查]]；修屋未验不造床，酒工与桶工分别署记。\n'
 if m.get('dramatic_casts',{}).get('SKO') and m.get('dramatic_casts',{}).get('YOS') and rel in ['02_世界与地图/任务空间/空间_SKO_斯孔弗特.md','02_世界与地图/任务空间/空间_YOS_约斯特文.md','11_管理/任务空间与地点关联审查.md']:
  body+='\n冶炼／羊毛两地八篇当前对白、同一采购人及有限交易交叉见[[斯孔弗特与约斯特文人物演出审查]]，不增加全访前置或重复奖。\n'
 from TaskArtLinks import add_task_art
 body=add_task_art(ROOT,rel,body)
 if m.get('dramatic_casts',{}).get('MAE') and rel in ['02_世界与地图/任务空间/空间_MAE_曼恩.md','11_管理/任务空间与地点关联审查.md']:
  body+='\n曼恩七篇当前对白、共用主线人物及去留交叉见[[曼恩人物对白与去留交叉审查]]；S79沿现有五场主章与卫星现场，不增加必访或重复奖。\n'
 body=body.replace('其它62篇城市台本',f"其它{sum('dramatic_scenes' not in q for q in m['quests'])}篇城市台本")
 if m.get('dramatic_casts',{}).get('ALD') and rel in ['02_世界与地图/任务空间/空间_ALD_奥尔德文.md','11_管理/任务空间与地点关联审查.md']:
  body+='\n奥尔德文七篇逐角色对白与条件回访见[[奥尔德文人物对白与交叉演出审查]]；当前场次沿此卡空间，不增加必访或新奖励。\n'
 body=preserve_foreign(V,rel,body)
 p=V/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(body,encoding='utf-8');hashes['design/'+rel]=hashlib.sha256(p.read_bytes()).hexdigest()
changes=[]
for c in m['cities']:
 nodes={n['id']:n for n in c['nodes']};rel=c['space_file']
 b=front('空间_'+c['id']+'_'+c['name'],'SPACE-'+c['id'],'architectural-design')
 b+='所属 '+wl(c['file'])+'；地域主章 '+wl(qs[c['main_id']]['file'])+'。\n\n'
 b+='> [!info] 制作口径\n> 本卡把原来的工作间／侧室替换为逐街区独立空间方案。仅定义相对布局、观察与行动，未定瓦片比例、像素原点、碰撞和原资源索引；不是可导入房间。没有要求玩家走遍所有室内。私密信息按具体任务的授权守卫处理，观察不自动写解决方案。\n\n'
 b+='**地域区别**：'+c['theme']+'。'+c['visual']+'\n\n[[原素材参考与城市概念图]]给出风貌；下列布局优先于画面中偶然生成的门数、床数、轨道和水岸。图中人物只是占位，实际人物弧线和方法以各台本为准。\n\n'
 for plan in c['space_plans']:
  did=plan['district'];a,bn=[nodes[x] for x in plan['rooms']]
  b+=f"## {did} {nodes[did]['name']}\n\n**相对布局**：{plan['layout']}\n\n"
  b+=f"入口／返街节点 `{did}`，A `{a['id']}` 与B `{bn['id']}` 各自有返街门。两间不能共用一把剧情钥锁住普通回程；路径不穿私卧房或危险作业区。这里只表示出口意图，实际宽度、碰撞和高度待制作核。\n\n"
  for n in [a,bn]:
   b+=f"### {n['id']} {n['name']}\n\n**可观察物**：{n['space']['observable']}。\n\n**实际交互**：{n['space']['interaction']}\n\n"
  b+='**入场权限与证据替代**：'+plan['access']+'\n\n'
  b+='**相关任务**：'+' · '.join(wl(qs[x]['file']) for x in plan['quests'])+'。地域主章的街区用途是按现选方案查对应责任，不是多加必访进度；支线只读本案范围。\n\n'
 b+='## 周边现场与逐任务出入点\n\n调查聚落不再按支线序号轮换。每条CS的触发街区、现场聚落、处置／回访街区都显式指定；现场有原固定回城环路。城内A/B为可选交互处，不能因列了两间就要求全访。\n\n|任务|触发→调查→处置／回访|地方关联|\n|---|---|---|\n'
 for qid in c['side_ids']:
  q=qs[qid];sat=next(s for s in c['satellites'] if s['id']==q['satellite'])
  b+='|'+wl(q['file'])+'|'+' → '.join('`'+x+'` '+nodes[x]['name'] for x in q['locations'])+'|'+wl(sat['file'])+'；'+sat['function']+'；'+q['need']+'|\n'
  if q['locations']!=oq[qid]['locations']:changes.append(dict(quest=qid,old=oq[qid]['locations'],current=q['locations'],satellite=sat['id']))
 b+='\n## 周边住户与独立生活场景\n\n'
 for sat in c['satellites']:
  r=sat['resident'];b+='- '+wl(sat['file'])+'：'+sat['space']['layout']+' 当地住户 '+wl(r['file'])+'；'+sat['space']['interaction']+'\n'
 b+='\n## 信息、行动、资源分别提交\n\n先见物只记录本案可知的观察；开柜、入私屋、公布信息另核当事人授权；实际付费、移料、交还或停止危险段之后才提交对应方法。关菜单、拒绝或退出不写resolve。固定脱体样／公共痕／事前有限记录支持独立核验，不能凭替代证据伪造本人同意。\n\n维修、磨谷、搬粮和普通运输交给实际工班；玩家参与的是归属、调查、监督、真实代价与人物选择，不以收十件材料当多解。各项付钱与库存由现有任务记账，本卡不增加paid、NE或N17资格。\n\n[[任务空间与地点关联审查]] · [[城市篇章与跨区域任务网]] · [[城市与聚落设计总索引]]\n'
 if c['id']=='BRY' and (V/'12_美术参考/布林任务场所概念与台本映射.md').exists():
  b+='\n六处场所的材质、物件与剧情用途参看[[布林任务场所概念与台本映射]]；出口意图仍以本卡为准。\n'
 write(rel,b)
 for sat in c['satellites']:
  r=sat['resident'];nb=front(Path(r['file']).stem,r['id'],'character')
  nb+='居住 '+wl(sat['file'])+'；所属 '+wl(c['file'])+'。身份、经历与口吻全部Mod原创。\n\n**日常工作**：'+r['role']+'。\n\n**动机、缺点与可能转折**：'+r['arc']+'\n\n**生活台词**：「'+r['line']+'」\n\n'
  nb+='关联台本：'+' · '.join(wl(qs[q]['file']) for q in sat['quests'])+'；地域章 '+wl(qs[c['main_id']]['file'])+'。\n\n'
  nb+='此人负责本地生活现场与有限观察，不替代台本原当事人的新同意、旧证据所有权和奖励。未亲历的案不能因同在本镇就知；须有具体公开事实或经本人允许的有限回执。已结案只有未来回应，不重开方法。\n\n死亡/缺席时停本人新台词，基础安全可走现有固定痕和事前有限记录；不能让别的住户代该人和解、迁居或签未来劳动。上面的转折是可能弧线，具体发生须满足已执行方法和实际代价，并非走进聚落自动触发。\n\n[[任务空间与地点关联审查]] · '+wl(c['space_file'])+'\n'
  write(r['file'],nb)

audit=dict(date=DATE,source='S75 authored spatial profiles; review against pre-update model in backup',
 districts=66,interiors=132,satellite_scenes=33,satellite_residents=33,explicit_side_placements=58,changed_placements=changes,
 limits=['Not scaled floorplans or game room data.','Does not validate literary quality or real inventory.','Consent, resolve, evidence and rewards remain owned by existing tasks.'])
(ROOT/'research/city-space-change-log.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
b=front('任务空间与地点关联审查','QA-CITY-SPACES-S75','design-audit')
b+='本轮接续城市完整设计，修正纸面空间与任务关联，未更新游戏包。更新前保存design、作者工具与模型在backups/city-spaces-20261012-s75。\n\n## 发现与修订\n\n原132个室内仅“工作间／侧室”，缺少地方物件和结构；已替换成逐街区编写的独立方案，含材料场、试架、分流渠、护栏、分柜、普通出口、实际交互与拒入替代。原支线城市街区与卫星有按序号取模分配的情形，出现白缝署名去铜灯、羊毛余量去缓梭、留灯入住去双门等错接；现在58条全部使用显式地点表。不是增加刷次数或全城跑图门槛。\n\n|城市／地域|结构方案|相关任务|\n|---|---|---|\n'
for c in m['cities']:b+='|'+wl(c['file'])+'|'+wl(c['space_file'])+f"；{len(c['space_plans'])}街区、{2*len(c['space_plans'])}室内|"+wl(qs[c['main_id']]['file'])+f"＋{len(c['side_ids'])}支线|\n"
b+='\n## 有变更的任务现场\n\n下表为原S63模型与现S75模型真实差异，详细地点名见对应台本和结构卡。改现场不改变方法本身、先前旧任务所有权或原作地图，不做角色档迁移。\n\n|任务|原节点|当前节点|\n|---|---|---|\n'
for ch in changes:b+='|'+wl(qs[ch['quest']]['file'])+'|'+' → '.join(ch['old'])+'|'+' → '.join(ch['current'])+'|\n'
b+='\n## 卫星聚落的生活与人物\n\n33处小聚落已分别写相对布局、独立服务/现场名、固定观察物、实际交互和33名当地住户。旧统一驻点联络员弧线已被替换；新卡提供工作、缺点、可能分支转折与生活话，不以走入聚落自动和解。台本原当事人和唯一奖励所有者保持。\n\n## 当前尚未终审\n\n独立空间已具功能布局，不是比例平面与碰撞成品。城市台本还有通用问句和收束台词，逐角色对白、实际预算数值、卫星独立室内及情境时间轴需要继续细写。本审查与绿色静态报告不能证明任务已经达到用户要求的文学深度、所有房间可玩或正式终稿。\n\n逐项数据在research/city-space-profiles.json与satellite-space-profiles.json，空间写入city-campaign.json，变更在city-space-change-log.json，生成哈希在city-space-note-hashes.json，校验在city-space-validation.json。[[城市美术与图片目录]] · [[原素材参考与城市概念图]] · [[城市扩展验收记录]]\n'
write('11_管理/任务空间与地点关联审查.md',b)
if model_drama := m.get('dramatic_cast'):
 b+='\n## S76布林对白接续\n\n布林11篇已在[[布林人物对白与网状演出审查]]改逐角色对白和条件回访，旧三问模板不再输出；其它62篇城市台本仍需相同精修。新配角沿已有空间，不增加必访室内、独占证据或第二奖励。\n'
 write('11_管理/任务空间与地点关联审查.md',b)
visual=ROOT/'research/city-space-visual-review.json'
if visual.exists():
 vr=json.loads(visual.read_text(encoding='utf-8'))
 if hashlib.sha256((ROOT/vr['source']).read_bytes()).hexdigest()==vr['source_sha256']:
  b+='\n## 通路图目视记录\n\n布林新版通路图已独立渲染并查看，完整标签可读、图未裁切，A/B与卫星现场各自返路用曲线区分。截图artifacts/city-visual-review/BRY-layout-s75-selected.png；原SVG与截图SHA在research/city-space-visual-review.json。其余SVG只做XML/路径检查，未逐张目视；拓扑图不是比例平面。\n'
  write('11_管理/任务空间与地点关联审查.md',b)
hp.write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
rule='\n<!-- CITY-SPACES-S75:BEGIN -->\n2026-10-12 S75：132室内用research/city-space-profiles.json逐街区空间替换通用工作间/侧室，58条CS触发/调查/回访用显式地点表，禁止重新按序号取模。入口design/11_管理/任务空间与地点关联审查.md。方案仅相对布局与互动，不是比例碰撞或运行房间；观察、私密授权、实际处置与奖励分记，新增室内不是全访前置。作者工具Write-CitySpaces.py保留备份差异与哈希，变更后额外运行Validate-CitySpaces.py及既有设计检查。\n<!-- CITY-SPACES-S75:END -->\n'
for p in [ROOT/'CHANGELOG.md',V/'AGENTS.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-SPACES-S75:BEGIN -->.*?<!-- CITY-SPACES-S75:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
p=ROOT/'CHANGELOG.md';t=p.read_text(encoding='utf-8-sig');block=rule.replace('入口design/11_管理/任务空间与地点关联审查.md','入口 [任务空间与地点关联审查](design/11_管理/任务空间与地点关联审查.md)');t=re.sub(r'\n<!-- CITY-SPACES-S75:BEGIN -->.*?<!-- CITY-SPACES-S75:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+block,encoding='utf-8')
print(json.dumps(dict(architecture_notes=len(m['cities']),interiors=132,satellite_scenes=33,satellite_residents=33,explicit_side_placements=58,changed_placements=len(changes)),ensure_ascii=False))
