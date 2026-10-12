"""Save reviewed DEN/MNS art, provenance and Obsidian links; no game changes."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil,re
from TaskArtLinks import add_task_art
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads((ROOT/p).read_text(encoding='utf-8-sig'))
def wl(p):return '[['+Path(p).stem+']]'
cache=Path('C:/Users/83912/.codex/generated_images/01a128a4-4af2-7493-b41e-9b162279a019')
specs=[dict(id='DEN',name='丹布里',slug='denbrie',atlas='088',
 first='exec-1597ea9c-f2d9-44e4-a7fa-40e9fc290244.png',selected='exec-6f486892-c6fe-4bbe-b9cd-4c958536d9a4.png',
 theme='回迁不是回到从前；修屋、捕鱼、接收和信仰不能互相变成服从条件。',
 review='已目视查看v1/v2六面板：A有两处可用隔间与未修后段，B人物留干岸，C网架与旁路、D结线檐与陆路、E礼桌侧院和F两床可区分。v2在F入口增加侧边带扶手坡面，原台阶仍可见；坡宽、坡度、门槛和担架转弯需比例图独立核验，不能由画面宣称无障碍验收。A三户旧门痕、C新割与旧磨毛细节仍不够可读，需另制近景。',
 panels=[
 ('A','DEN-D01-A',['CM-DEN'],'两处安全空间与三户旧居经历不能自然合成第三床。','后段封闭，暂住由真实接收点承担；门痕只是近景待绘提示，不证明任何一户资格。'),
 ('B','DEN-D04-A',['CS-DEN-01'],'家船第三位家人有自己的去留；帮助第四人不等于忘记他的旧告密。','车船分装棚外侧干岸与接船地点；图中船型和站位不定载重，三位成人逐人许可，伤者出发前留原岸。'),
 ('C','DEN-D03-A',['CS-DEN-02'],'擅借渔网与割网救人同时成立，迁来身份不能代替责任。','旧磨毛和新割口需独立近景；烟灶靠石墙离网，保绕网陆路，不用危险重演或收集材料推进。'),
 ('D','DEN-S02-3',['CS-DEN-02'],'熟悉自己的结法不等于能指认所有陌生补法为破坏。','结线比样檐在桥边干地；普通住宿朝陆路，不以过危险桥、搜旅人包袱或强制归返为前置。'),
 ('E','DEN-S01-3',['CS-DEN-01','CS-DEN-03'],'户主的失亲仪式对她有意义，住户也能拒绝参加。','两种生活院把侧院礼桌、取水、患者独立门和村路分开；伤者未移交时不在此出现，伊蕾只知已授权范围。'),
 ('F','DEN-D02-B',['CM-DEN','CS-DEN-03'],'短宿与照护各有有限位置；不参加仪式不取消已签基本居住。','两张床单账占用，侧坡回普通村路；实际移住须接收、费用和照护交接，不能凭切图结算。')]),
 dict(id='MNS',name='曼郡',slug='mannshire',atlas='083',
 first='exec-f75e0509-4406-4c0b-a198-625fb1a13db5.png',selected='exec-4fe7e053-f9f3-406a-b99a-5284e4beb023.png',
 theme='旧名可以留下来，年份、技术来源、容器用途与本季收成却要说清。',
 review='已目视查看v1/v2：六面板用途与街区有区别，B/F均有枯枝而非全坡丰收；E空架试箍与独立侧棚门可见。v2在A/D两端画平缓坡面，D前排原桶上增加并列红黄签，未凭编辑新加第二批桶。具体用途隔离、样酒出处、工具归属、标记近景与真实容量仍须制作核验；人物只作匿名比例，不据相似脸像合并两对师徒。',
 panels=[
 ('A','MNS-D02-A',['CM-MNS'],'瓶外旧名、家族旧杯与瓶中新酒不是同一项证据。','封桶通风廊两端地面坡门，旧封与新批分位；年份要真实确认，图中杯与蜡不证明酒龄或失亲真相。'),
 ('B','MNS-D01-A',['CM-MNS','CS-MNS-03'],'一条活芽不能证明整坡恢复，季工投入也不是永久土地所有权。','旧枝辨芽棚留采果通路；观察原位与公共样枝，不采走指定数量、不拔枝试移植，不保证下季成活。'),
 ('C','MNS-D04-A',['CM-MNS','CS-MNS-03'],'商誉里既有真实劳动也有虚报年份，退款不买下一次合作。','新酒小售廊两类样位与侧院纪念分开；有限批量，来源和新酿标记需另做UI/物品；缺席者不因此归来。'),
 ('D','MNS-D02-B',['CS-MNS-01'],'同一批桶收过两笔订金，养工的理由不能把债变没。','双名保桶室同桶双签，替代容器分放；护理用途须合用且买方接受，洗一次不等于适用，不派玩家搬桶。'),
 ('E','MNS-D03-A',['CS-MNS-02'],'师傅教过基础，学徒的改法仍需真实承认来源。','刻线试箍屋用空载安全架；侧门通学徒临作棚，提奥酿酒／贝洛箍桶分人，本案师傅凯诺为原创不替原NPC。'),
 ('F','MNS-S01-3',['CS-MNS-03'],'种枝来处、三季劳动和有限田界有不同的权利与代价。','两期葡架台有限成活与枯枝并存；移枝需专业可行、本人生效许可与真实补偿，季约不改全国土地制度。')])]
model=load('research/city-campaign.json');cs={c['id']:c for c in model['cities']};qs={q['id']:q for q in model['quests']}
records=[]
for s in specs:
 cid=s['id'];c=cs[cid];nodes={n['id']:n for n in c['nodes']}
 outputs=[]
 for version,key in [(1,'first'),(2,'selected')]:
  src=cache/s[key];dest=V/f'12_美术参考/城市概念/{cid}-任务场所-v{version}.png'
  if dest.exists():
   if sha(dest)!=sha(src):raise SystemExit('Refusing overwrite: '+str(dest))
  else:shutil.copy2(src,dest)
  outputs.append(dict(path=dest.relative_to(ROOT).as_posix(),sha256=sha(dest),source_path=str(src)))
 dest=ROOT/outputs[1]['path'];note=f"design/12_美术参考/{s['name']}任务场所概念与台本映射.md"
 refs=[f'design/12_美术参考/城市概念/{cid}-概念-v1.png',f"stoneshard-assets-sample/atlas-{s['atlas']}.png",'stoneshard-assets-sample/atlas-099.png']
 prompts=[f"research/{s['slug']}-task-art-{action}-s81-20261012.txt" for action in ['prompt','edit']]
 linked=['design/'+c['file']]+['design/'+t['file'] for t in c['satellites']]+['design/'+q['file'] for q in model['quests'] if q['city']==cid]+['design/'+c['space_file']]
 rec=dict(id=cid,name=s['name'],selected=outputs[1]['path'],sha256=sha(dest),dimensions=list(Image.open(dest).size),source_path=outputs[1]['source_path'],previous=outputs[0],actual_edit_reference=dict(path=outputs[0]['path'],sha256=outputs[0]['sha256']),
  references=[dict(path=p,sha256=sha(ROOT/p),role='style and material reference only') for p in refs],actual_generation_references=refs,prompts=[dict(path=p,sha256=sha(ROOT/p)) for p in prompts],
  generation_baseline=dict(city_model_sha256=sha(ROOT/'research/city-campaign.json'),dialogue_draft_source=f"research/{s['slug']}-drama.json",dialogue_draft_sha256=sha(ROOT/f"research/{s['slug']}-drama.json")),
  panels=[dict(label=a,space=n,name=nodes[n]['name'],quests=qids) for a,n,qids,_,_ in s['panels']],note=note,linked_notes=linked,review=s['review'],link_marker='SHORE-VINE-TASK-ART-20261012')
 records.append(rec)
 b=f'''---
title: "{s['name']}任务场所概念与台本映射"
id: ART-{cid}-TASK-S81
type: art-reference
status: draft
canon: mod-original
baseline: "0.9.4.25-modbranch"
updated: 2026-10-12
tags: [stoneshard, art, task-spaces, {cid}]
aliases: []
---

# {s['name']}任务场所概念与台本映射

所属 {wl(c['file'])}，空间依据 {wl(c['space_file'])}，逐角色对白见 [[丹布里与曼郡人物演出审查]]，总览见 [[原素材参考与城市概念图]]。

主题：{s['theme']}

![{s['name']}任务场所六面板](城市概念/{dest.name})

> [!info] 当前美术草稿
> A—F是画板位置，不是实际相邻关系、游历顺序或必须访问清单。参考已查看的城市总览与用户原素材；图集只读，未复制入库。床、桶、船、工班和款项仍按台本真实单账，画中数量不是库存或奖励。人物只是匿名比例，不据脸像替任务分配身份。

## 图文映射

|面板|稳定空间ID／地点|关联任务|矛盾与人物弧线|互动边界与制作要求|
|---|---|---|---|---|
'''
 for a,n,qids,dilemma,boundary in s['panels']:
  b+=f"|{a}|`{n}` {nodes[n]['name']}|"+' · '.join(wl(qs[q]['file']) for q in qids)+f'|{dilemma}|{boundary}|\n'
 b+='\n## 周边与回程\n\n'+' · '.join(wl(t['file']) for t in c['satellites'])+'。周边接收和工坊会面以当地具名住户真实在场或有限授权回执为准；出入普通村路不能依附某个任务选项。图中桥、水和装卸区域不直接决定世界坐标。\n'
 b+='''
## 多解与后果

实际退款、交还、接收、有限签约或专业处置执行后，才按对应台本确认分支；观察、问话和图片预览不结案。拒绝同船、合住、共署或仪式各保独立出口，不强迫和解。缺席、死亡、拒绝与私密范围优先于跨城回访，不能由买方订单得知他人的病史。晚到只改变未来可做的事，旧伤害、欠款和损失保留；不追加奖励、不回滚N17。

## 目视核对与下一步制作

'''+s['review']+'\n\n后续须另制比例平面、近景可观察物、原点、遮挡与安全距离，按原生地图保存和出入口生命周期实现。此图不是逐格地表、室内碰撞、可直接打包的精灵或游戏运行证据。\n'
 b+='\n## 来源与版本\n\n使用内置 image_gen 生成并作一次定向编辑，保留v1/v2及原缓存。完整生成／编辑提示词：'+'、'.join('`'+p+'`' for p in prompts)+'。输入参考、输出SHA256、尺寸、生成时台本指纹与候选版本登记于 `research/shore-vine-task-art-20261012.json`。\n\n[[任务空间与地点关联审查]] · [[城市美术与图片目录]] · [[城市与聚落设计总索引]]\n'
 (ROOT/note).write_text(b,encoding='utf-8')
manifest=dict(date='2026-10-12',status='draft',canon='mod-original',tool='built-in image_gen',boards=records,runtimeVerified=False,scope='DEN and MNS companion task-location boards: 12 panels, 8 existing tasks; no game changes')
(ROOT/'research/shore-vine-task-art-20261012.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
hashfiles=['research/city-generated-note-hashes.json','research/city-space-note-hashes.json'];hashes={p:load(p) for p in hashfiles};changed=[]
for rec in records:
 for rel in rec['linked_notes']:
  p=ROOT/rel
  for h in hashes.values():
   if rel in h and sha(p)!=h[rel]:raise SystemExit('Untracked edit: '+rel)
  old=p.read_text(encoding='utf-8-sig');new=add_task_art(ROOT,rel.removeprefix('design/'),old)
  if new!=old:p.write_text(new,encoding='utf-8');changed.append(rel)
  for h in hashes.values():
   if rel in h:h[rel]=sha(p)
for p,h in hashes.items():(ROOT/p).write_text(json.dumps(h,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
marker='SHORE-VINE-TASK-ART-20261012'
body='2026-10-12：丹布里／曼郡各新增六面板任务场所概念，逐项映射见design/12_美术参考/丹布里任务场所概念与台本映射.md与曼郡对应卡。完整提示词、原参考、v1/v2和输入输出哈希见research/shore-vine-task-art-20261012.json；不替十五总览或旧选稿。短宿两床、双名同桶、两对师徒及实际回程遵台本，坡面、容量和近景仍须制作；图不代表游戏交互。TaskArtLinks.py维持本批双链，运行Validate-ShoreVineTaskArt.py及既有设计检查。'
for p in [ROOT/'AGENTS.md',V/'AGENTS.md',ROOT/'README.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- '+marker+r':BEGIN -->.*?<!-- '+marker+r':END -->\n','',t,flags=re.S)
 p.write_text(t.rstrip()+f'\n\n<!-- {marker}:BEGIN -->\n{body}\n<!-- {marker}:END -->\n',encoding='utf-8')
print(json.dumps(dict(boards=2,panels=12,associated_tasks=8,linked_notes=16,changed_notes=len(changed),runtimeVerified=False),ensure_ascii=False))
