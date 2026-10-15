"""Generate art catalogue and limited sprite references, never original atlas copies."""
from pathlib import Path
import json,os,hashlib,re
ROOT=Path(__file__).resolve().parents[2];V=ROOT/'design'
m=json.loads((ROOT/'research/city-campaign.json').read_text(encoding='utf-8'));art=json.loads((ROOT/'research/city-art-manifest.json').read_text(encoding='utf-8'))
briefs=json.loads((ROOT/'research/city-art-briefs.json').read_text(encoding='utf-8'));bm={b['id']:b for b in briefs['briefs']};rs={r['id']:r for r in art['reference_based_boards']}
qs={q['id']:q for q in m['quests']}
def wl(path):return '[['+Path(path).stem+']]'
def ql(qid):return wl(qs[qid]['file'])
specific={
'BRY':'码头、水门与富裕市集的相邻关系可作为构图依据；租屋巷仍须增加私下会面退路。水门的实际数量与高低水位要按CS-BRY-09另作机制平面，不能逐像素照搬画面。',
'DEN':'渔屋、破屋与驻点分别表现；三户两房争议只用两个已验住所，画面中的其余屋不计作免费床。海浪与浅滩是视觉提案，通路需重新核碰撞。',
'OSB':'留种粮棚与生活粮分开，家门距离短；磨坊轮与农田仅作新侧场参考，不替换原作磨坊/啤酒作坊布局，原村仍非战毁村。',
'MNS':'葡架断层、新苗与旧封酒桶支持新酒来源争议；酒窖需新增独立通风出口，不能复用原工具铺锁梯反转。',
'ALD':'使用v2干燥料场与工艺街区，v1意外水岸仅留历史对照。甲外展示与衬布/工伤核验是不同空间，宗教侧院不等于王宫或全城官署。',
'SKO':'炉火、有限炭堆、冷却沟与晾衣并置；赎回者会面处不能锁在作坊后间。概念未确定冶炼产能，不能从满料堆推无限库存。',
'YOS':'羊毛、织机、晒布与分开的工位表现师徒来源；冷风为视觉氛围。羊群数量与布色不作真实可收割奖励。',
'KOR':'此寄存院、门牌与住棚均明确原创，不能据此推断考德官方产业、规模与地形。相似门牌可服务身份误认，但取物/住门不可共享全权钥匙。',
'EED':'旧梁料场在公共空间、住户门留在林缘内侧，强调物料核验不等于搜家。河岸是Mod局部提案，原作出口贸易限制仍有效。',
'FOR':'支井、通风与家属院分别构图；画面小轨道、矿车和称场是原创器材提案，需对照可用资源/时代感再选，不作为已核原矿设备。金矿不是北疆犯人石场。',
'RAT':'旧兽只在纪念浮雕中出现，雕刻是地方纪念者诠释，不代表原作怪物官方造型。新足迹/响绳需单独可观察物证，不能做复活旧兽首领。',
'PAS':'卸货中轴与民用旁路分别服务军需核对、普通回程；关口只处理本地个案，视觉规模不授王廷全国代理权。',
'ASH':'护理、公共厨房与观察桌分离，病人可留村或离开；不同桶色是原创标记，不能读图判所有病因/治愈。栈道应有防滑与返回陆路。',
'HIG':'山地冷石、旧钟、停用危险段与可回走台体现维护责任。紫光仅作少量封存介质氛围，不扩成第二处官方晶石真相；修院与序章保持独立。',
'MAE':'使用去旗帜v2；寒地雪景是美术选择，不宣称全年降雪。档案残庭、根菜厨房与护理房有人使用，但不代表恢复正常学院；名册与病史柜需分钥。'}
names=['s_brynn_03_house22','s_brynn_03_grocerypart01','s_brynn_04blacksmith_part06','s_vinery01','s_Denbrie_FisherHouse_pt01','s_AppleTree_03','s_drytree_1','s_oldforge01','s_millinteriorbgpart01','s_millbarninteriorbg']
sprites=json.loads((ROOT/'stoneshard-assets-sample/sprites.json').read_text(encoding='utf-8-sig'));sm={s['name']:s for s in sprites};catalog=[]
for name in names:
 s=sm[name];catalog.append(dict(name=name,width=s['width'],height=s['height'],originX=s['originX'],originY=s['originY'],first_frame=s['frames'][0],use='style/scale candidate only; current installation indices and reuse fit not verified'))
(ROOT/'research/city-art-reference-catalog.json').write_text(json.dumps(dict(date='2026-10-12',source='user stoneshard-assets-sample; README says extracted from vanilla.win',items=catalog,limits='Only selected asset names/frame coordinates; no atlas pixels or commercial asset collection copied here.'),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
b='''---
title: "原素材参考与城市概念图"
id: ART-REF-S74
type: art-reference
status: draft
canon: mixed
baseline: "0.9.4.25-modbranch"
updated: 2026-10-12
tags: [stoneshard, art, concepts, S74]
aliases: []
---

# 原素材参考与城市概念图

本轮按用户要求，使用内置image_gen，以用户提供的原素材为视觉参考；没有绘画CLI/API调用。十五个城市／地域各有独立概念板，下方共三十三个周边聚落构图。每板是代表性片区与卫星面板，不是全城地理图、逐格地图或碰撞数据。全部仍为Mod原创美术提案，未导入.sml或更新游戏。

原参考：stoneshard-assets-sample/atlas-020.png（城市外观）、atlas-083.png（村路/酒业外观）、atlas-088.png（渔村与木屋）、atlas-060.png（林地、枯树/寒地植被）、atlas-099.png（普通工坊/室内）。已逐页目视；atlas-003.png为技术小页，未作生图参考。图集只读，未复制进设计库；输出保留在城市概念/。sprites.json定位只证明样本定义，不能确认当前安装包索引、资源可复用范围或城市原布局。

## 材质与尺度参考

使用石基、木骨架、瓦/草顶的清晰轮廓，泥路/石街和季节植被的低饱和颜色，原素材俯视斜角与小比例人物。数字画板分辨率不是原游戏格尺寸；真正制作需核角色/门原点、瓦片网格、碰撞、遮挡与动画。十项候选名称和首帧坐标登记在research/city-art-reference-catalog.json，不存完整原图集或对白。

|原精灵|样本画布|首帧图集与定位|可参考部分|
|---|---|---|---|
'''
for s in catalog:
 f=s['first_frame'];b+=f"|`{s['name']}`|{s['width']}×{s['height']}，原点{s['originX']},{s['originY']}|atlas-{f['pageIndex']:03}.png；{f['x']},{f['y']}；{f['width']}×{f['height']}|材质、轮廓或局部室内尺度，实际资源接入待核|\n"
b+='\n## 当前概念板\n\n所有图已目视检查主景/卫星区分、标签、地域用途与明显设定冲突。图中人物只作场景占位，不是新NPC最终脸像；所有库存、床数、机关、物证与通路以任务稿及后续制作验证为准。\n\n'
for c in m['cities']:
 r=rs.get(c['id'])
 b+=f"## {c['id']} {c['name']}\n\n{wl(c['file'])} · {ql(c['main_id'])}\n\n"
 if r:
  rel=Path(os.path.relpath(ROOT/r['output'],V/'12_美术参考')).as_posix();b+=f"![{c['name']}与周边概念]({rel})\n\n"
 else:b+='概念板尚未生成／保存。\n\n'
 b+='**画面任务用途与制作修订**：'+specific[c['id']]+'\n\n'
 b+='**周边面板（从左至右）**：\n\n'+ '\n'.join(f"- `{s['id']}` {wl(s['file'])}：{s['dilemma']}；关联"+' · '.join(ql(q) for q in s['quests'])+'。' for s in c['satellites'])+'\n\n'
 b+='**城内支线**：'+' · '.join(ql(q) for q in c['side_ids'])+'\n\n'
b+='''## 生成记录与实施边界

完整初始提示词与输入路径/哈希：research/city-art-briefs.json；追加约束和ALD/MAE定向编辑：research/city-art-prompt-additions.json。选择的输出、SHA256、原缓存路径、相应城市/卫星笔记和目视结论：research/city-art-manifest.json。旧三联画保留为早期绘画风格对照，ALD/MAE v1保留历史，不作当前选稿。

本轮只生成概念与补文档。后续按原生地图生命周期制作，现有资源按名称引用；新绘资产需拆层、定原点/遮挡、配碰撞、核可走格与回程。任何可见房门和病床都未因此具备游戏交互。这里不设置全国阵营新真相、不移动原角色存档、不覆盖data.win。

[[城市美术与图片目录]] · [[城市与聚落设计总索引]] · [[城市设计与原作避让审查]] · [[城市扩展验收记录]]
'''
if (V/'12_美术参考/布林任务场所概念与台本映射.md').exists():
 b+='\n## 布林任务场所细化（S77）\n\n[[布林任务场所概念与台本映射]]补租屋、纪念、工艺、护理、水门与旧帆六处独立场所；沿用原素材风格，不替换本页十五张城市／地域总览。\n'
if (ROOT/'research/city-task-art-20261012.json').exists():
 b+='\n## 斯孔弗特与约斯特文任务场所（2026-10-12）\n\n[[斯孔弗特任务场所概念与台本映射]]：赎款寄柜、归乡棚、旧坯料廊、炭份台、冷沟与暖手屋。\n\n[[约斯特文任务场所概念与台本映射]]：家纹对色、离坊收包、代工排管、留冬称捆、洗毛分流与师徒分署。两板十二处原创构图已保存；原总览和YOS旧稿保留，逐角色初稿以现行台本为准。图片不证明地图通达、实际库存、授权或任务完成。来源与提示词见research/city-task-art-20261012.json。\n'
if (ROOT/'research/shore-vine-task-art-20261012.json').exists():
 b+='\n## 丹布里与曼郡任务场所（S81）\n\n[[丹布里任务场所概念与台本映射]]：旧屋承重、干岸接船、晾网破口、结线比样、两种生活院与短宿安置。\n\n[[曼郡任务场所概念与台本映射]]：封桶通风、旧枝辨芽、新酒小售、双名保桶、刻线试箍与两期葡架。两板十二处已保存，v1/v2与输入输出来源见research/shore-vine-task-art-20261012.json；任务遵当前台本，坡度、容量、近景与运行仍待制作。\n'
p=V/'12_美术参考/原素材参考与城市概念图.md';p.write_text(b,encoding='utf-8')
rule='\n<!-- CITY-ART-S74:BEGIN -->\n2026-10-12 S74：参考用户stoneshard-assets-sample生成城市概念板，每板含城市核心与卫星ID构图；入口design/12_美术参考/原素材参考与城市概念图.md。初始/追加/编辑提示词、输入哈希和输出SHA分别存research/city-art-briefs.json、city-art-prompt-additions.json、city-art-manifest.json。参考原图只读，不复制图集；生成板是美术草稿，不作官方地理、最终精灵、碰撞或运行证据。新候选记录必须保留原提示词与版本，不覆盖旧选稿。\n<!-- CITY-ART-S74:END -->\n'
for p in [ROOT/'CHANGELOG.md',V/'AGENTS.md']:
 t=p.read_text(encoding='utf-8-sig');t=re.sub(r'\n<!-- CITY-ART-S74:BEGIN -->.*?<!-- CITY-ART-S74:END -->\n','',t,flags=re.S);p.write_text(t.rstrip()+'\n'+rule,encoding='utf-8')
print(json.dumps(dict(boards=len(rs),satellite_vignettes=sum(len(c['satellites']) for c in m['cities']),selected_reference_frames=len(catalog)),ensure_ascii=False))
