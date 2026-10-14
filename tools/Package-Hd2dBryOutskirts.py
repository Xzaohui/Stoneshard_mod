"""Export verified27view handoff and browser-gated immutable archive."""
from pathlib import Path
import argparse,json,hashlib,zipfile,importlib.util,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-outskirts-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
LABELS=['堤背共灶住棚','高墩留种棚','旧帆共灶屋','单门侧泊租棚','原创临街装帧副坊','封闭危险外棚','旧塔公共外廊','中立外院听席棚','短宿单床','未点亮普通共灶','分列班筹盒','学徒小印','旧堤修补痕','两只有限留种封袋','田边称粮架','空白定金木筹','低位盐湿田垄','干放旧船骨','唯一租用小艇','单套离体支具','空白载重刻尺','横置挡车箱','封存病史袋','回岸标记','低位试载架','两批分格余料','三种有限试件','卸下的断扣','空白批次签','试载围挡','一人装帧台','历史原页托盘','后添页托盘','有限低柜','独立空椅','订线工具','空白方法示例页','缺撑旧框','弯曲封板','封棚边界栏','固定外缘支架','封存家中便条盒','经手费用盘','中空环桌','三栏交接盘','限定陈述盒','四块有限旧料','空支具收纳架']
def preview(m,v):
    spec=importlib.util.spec_from_file_location('bryo_preview_base',ROOT/'tools/Package-Hd2dR02.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);h=base.HTML
    h=h.replace('丹布里西路与渡口','布林周边聚落与续篇场所').replace('R02 / N5 / N9 / D03 / SQ04 / SQ05 / DT13','BRY-S01—S03 / BRY-X11—X16 · 场景美术')
    h=h.replace('干燥地面','候选地面格').replace('河面','非通行水面 / 低田').replace('<label><input type="checkbox" id="repaired">桥面修复示意</label>','<label><input type="checkbox" id="hazard">危险外棚边界示意</label><label><input type="checkbox" id="fixtures">家具占位提案</label>')
    h=re.sub(r'function canWalk\(s,x,y\)\{.*?\}',"function canWalk(s,x,y){return contains(s.walkable_rectangles,x,y)&&!contains(s.blocked_rectangles,x,y)&&!contains(s.fixture_block_rectangles,x,y);}",h)
    h=h.replace("$('repaired').disabled=special||!(s.repaired_add_cells||[]).length;","$('hazard').disabled=special||!s.illustration_variants?.hazard;$('fixtures').disabled=special||!(s.fixture_block_rectangles||[]).length;")
    a=h.index('const repair=');z=h.index('try{const images=',a)
    h=h[:a]+"""const hazard=$('hazard').checked&&!$('hazard').disabled,hasRoof=$('roof').checked&&!$('roof').disabled;
const water=s.id+'__water',field=s.id+'__salt_field',blue=s.id+'__plan_structure';
const parts=special?[plan?s.plan:s.scene]:[s.id+'__backing',...(assets.has(water)?[water]:[]),...(assets.has(field)?[field]:[]),s.id+'__floor',...(plan?(assets.has(blue)?[blue]:[]):[s.id+'__structure',...($('props').checked?[s.id+'__props_preview']:[]),s.id+'__foreground',...(hasRoof?[s.id+'__roof']:[])]),...(hazard?[s.id+'__hazard_markings']:[])];
"""+h[z:]
    h=h.replace('images.forEach(im=>ctx.drawImage(im,0,0));',"images.forEach(im=>ctx.drawImage(im,0,0));canvas.dataset.renderedLayers=parts.join(',');if(!special&&$('fixtures').checked&&!$('fixtures').disabled){ctx.fillStyle='rgba(221,164,72,.28)';for(const [a,b,c,d] of s.fixture_block_rectangles)ctx.fillRect(a*26,b*26,(c-a+1)*26,(d-b+1)*26);}")
    h=h.replace("+(repair?' · 修复桥面示意':'')","+(hazard?' · 封闭危险段示意':'')").replace("'roof','repaired','grid'","'roof','hazard','fixtures','grid'")
    names={'s01':'灰堤工营·堤背生活段','s02':'盐穗小镇','s03':'旧帆村','x11':'低潮侧泊棚','x12':'断扣试载台','x13':'旧书装帧台','x14':'工具巷外的封板','x15':'旧塔支款席','x16':'四区小听席'};special=[]
    for key,name in names.items():
        a=next(a for a in m['assets'] if a['id']=='bryo_'+key+'__plan_overview');special.append(dict(id='bryo_'+key+'_overview',name_zh=name+' · 多区总览',size=a['size'],plan='bryo_'+key+'__plan_overview',scene='bryo_'+key+'__working_overview',note='各区保持1:1原像素 · 分区拼版，不是一间可走房间'))
    h=re.sub(r'const specials=.*?;',lambda _:'const specials='+json.dumps(special,ensure_ascii=False)+';',h).replace("$('scene').value='r02_tax_main'","$('scene').value='bryo_x11_work'")
    core_spec=importlib.util.spec_from_file_location('bryo_core_labels',ROOT/'tools/Package-Hd2dBryCore.py');cp=importlib.util.module_from_spec(core_spec);core_spec.loader.exec_module(cp);corebrief=read(P.parent/'BRY-core-v1/brief.json');labels={a['id']:n for a,n in zip(corebrief['sprites'],cp.LABELS)};labels.update({a['id']:n for a,n in zip(read(P/'brief.json')['sprites'],LABELS)})
    h=re.sub(r'const labels=.*?;',lambda _:'const labels='+json.dumps(labels,ensure_ascii=False)+';',h)
    h=h.replace('独立建筑与环境物件 · 18件','独立建筑与环境物件 · 60件').replace('五个建筑另含body与roof','九类建筑/棚顶另含body与roof')
    h=h.replace('修复切换仅展示候选桥面。','掩码扣除已登记的家具占位提案；尚非原生碰撞。危险边界开关只加观察图形，不开棚、不触发伤害。').replace('公共桌、取样水口与返程均按空间约束绘制。人物、授权及任务结果由引擎处理。','单门回岸、双床容量和独立侧台按文字空间绘制。人物、姓名、权限、金额、检测与实际交接由引擎处理。').replace('旧渡口复用N1，区域图和多室拼版另标比例','三处卫星＋六处续篇 · 21个区段 · 总览保留1:1像素')
    (P/'preview.html').write_text(h.replace('__DATA__',json.dumps(dict(scenes=m['scenes'],assets=m['assets'],region=m['region'],validation=v),ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    rows='\n'.join(f'| `{s["id"]}` {s["name_zh"]} | {s["size"][0]}×{s["size"][1]} | {s["cells"][0]}×{s["cells"][1]} |' for s in m['scenes'])
    overview='\n'.join(f'| {s["name_zh"]} | {s["size"][0]}×{s["size"][1]} |' for s in special)
    text=f'''# 布林卫星与续篇 · HD-2D v1

本批{len(m['assets'])}张生产PNG、21个独立区段、60个独立建筑/环境精灵（48新增、12复用）、36块26×26材质瓦片，完成27项原清单视图。{v['checks_passed']}项静态检查通过；原生门、世界坐标、物件碰撞、楼梯高差、保存、天气和灯光仍待实际装配，本批不修改NPC/对白/GML/游戏包。

三处卫星：灰堤工营堤背生活段、盐穗小镇、旧帆村，各含外部、双床生活区、工作区。六处续篇：低潮侧泊棚、断扣试载台、旧书装帧台、工具巷外的封板、旧塔支款席、四区小听席，各含外部及工作区。工作区可为露天，不能把所有“工作空间”称作室内原生房间。

preview.html离线查看平面地图/空间、屋顶、独立物件、26格网、候选掩码及出口。家具占位和危险边界是开发观察提案，默认不覆盖美术；危险区域始终按封闭提案保留，切换只加图形，不提交开棚、损伤、授权、奖励、时序或保存。

| 区段 | 像素尺寸 | 格数 |
|---|---|---|
{rows}

## 生产导入

assets/为生产PNG，raw/为七份母图，guides/为格图与屋顶掩码，sheets/为60精灵合集。全部路径相对本目录；nearest采样、关闭平滑/mipmap，保留完整透明画布，不能自动裁边。
1像素=1房间像素，场景原点(0,0)。物件左上角=(cellX×26+13,cellY×26+13)−sprite.origin；脚底底沿对齐originY。object_canvas_rects核对画布不出场景边缘，但不提供原生碰撞。
空间顺序：backing→water或salt_field→floor→structure→按脚底Y排序的独立建筑body/物件/原生人物→foreground→可关闭roof→可选hazard_markings。平面顺序：backing→water/salt_field→floor→plan_structure。
surface_attachment物件按draw_after_instance紧接宿主绘制，包括学徒印、试件、订线/样页、款袋和交接盘；按普通Y排序会被桌面遮住。三栏交接盘的栏头空白，不能根据图像推定授权已获。
九类建筑/棚顶full/body/roof共画布共原点，body与roof不重叠、精确重组full。八类新增建筑用母图掩码，路侧/船骨棚顶逐字节复用本项目BRY核心批次；不复制原作商业图集。
environment、working_space、props_preview和各overview为检查合成图，交互物件使用items/独立PNG，不应同时烘焙并再实例化。城市间接点、门锁、房间保存和实体复现仍需原生实现。
layouts.json的walkable/blocked为候选地形，fixture_block_rectangles为少量家具占位提案，privacy_rectangles只供拒绝路线审查，三者均非从alpha提取。预览掩码显示地形扣除已登记家具，PNGalpha不能作为碰撞。未登记家具、原生人物与射线碰撞仍未测量。
water_object只允许小艇脚底在非通行水面，不能供玩家站立；boundary_object是试载栏杆，脚底在明确阻挡区；ground_decoration为低田纹理，不授予通行格。原生对象类型与保存须另接。

## 空间与状态边界

灰堤是R01既有工营的堤背生活扩展提案，保留原N2院与原场景；入口R01_original_yard仅为待绑定接点。薪筹台在路侧棚下，干路绕过生活房，退班不穿私人卧房。三处卫星每处恰好两床、一灶与一班普通服务的设计容量；六个床实例不代表已分配住宿或可无限刷新。
盐穗低处是盐湿田土纹，独立salt_field层不作深水。留种棚高墩、称粮台和高径相连；封袋、定金筹与高低水尺分开，图不确认水门已造成损失或预支买走全部下一季。
旧帆的旧船骨干放棚内浅院，完整小艇只属于X11；空席牌和未拆泊钉分开，不证明失踪者死亡/返回。工作棚村路与船工岸双向回程，床数/可租位及本人授权由引擎单独管理。
X11工作段恰好一个回岸门、一套离体支具、一条租用小艇。小艇在外部与工作细图都出现，physical_entity同为X11_single_rental_boat，属于同一对象的两幅视图；不能解释成两船/两航次。公开等候/运费刻度、屏风与封存病史袋分开，挡车箱保留步行回岸，未确认载重/回岸不表示出航。空收纳架不额外生成支具。
X12两批分格小料、三种试件、低位固定架和断扣独立；三种形状是本批试件而非可刷新矿产。围挡试验区与公共巷道分开，拒绝试验/付费/技能不关闭公共回程。
X13一人修复席，历史原页与后添页分盘，另有空白方法样页；私人姓名盖住，纸纹/订线可在公开侧核。新副坊不声明大学或原印刷坊开放，也不烘焙古人墨迹与真伪结论。
X14危险木板段默认不可通行，缺撑旧框与固定外缘检查架分开。物主外台、专业单班和安全外缘检查有回程，不复制原工具铺地窖、梯子、敌人或死者，不把封棚画成已整改开工。
X15本班款袋、经手费盘、私下领取座分别布置；拒绝实名公示仍可按本人许可领取。空白告示不表示同意受雇，封袋不表示全班清账，不借博恩柜台/军械权限。
X16一张中空环桌、五张独立空椅与外围长凳，侧台可不进听席单独办理。三栏交接盘分到场/授权/实际交接，标题留空由引擎加字；空椅不作赞同、不放克隆NPC，不确立新城政制度。旁听长凳不推定到场人数。

## 总览、色板与可复核来源

| 总览 | 像素尺寸 |
|---|---|
{overview}

九组plan_overview与working_overview各区保持1:1像素，区段间隔26像素、无重叠裁切，不是九间大房间。卫星总览含外部/生活/工作三域；续篇含外部/工作两域。重复展示同一物件不新增真实库存、床数或船数。
BRY-CORE-128沿用核心批次的128色，四种312面材/36瓦片及墙窗逐字节复用；瓦片边缘匹配，非47态边界自动瓦片。78×39竖墙样片的三条PAM尺寸警告按用途保留；它们不是整格地砖。
七次生成的提示词、输入/输出SHA和original_size见generation-log.json。原稿透明图1536×1024；环境母图实际1254×1254，按记录裁切/NN/128色/二值alpha和脚底补偿，不冒称原始尺寸完全服从提示。
生成时spec_lock.generation-v1.md逐字节保留，日志spec_lock_path指向它，原spec_lock_sha256未改。工具只认canvas/per_sprite_budget章节，修正格式及已批准128色预算后的锁留spec_lock.postprocess-v2.md；当前spec_lock另登记复用棚顶。notes/spec-lock-format-repair.json及reused-awning-extension.json列出版本哈希。没有重写母图或提示词掩盖格式错误。
validation.json是静态证据，preview-validation.json是浏览器证据，均不证明原生房间已运行。复现：Export-Hd2dBryOutskirtsSprites→Export-Hd2dBryOutskirts→Validate-Hd2dBryOutskirts→Package-Hd2dBryOutskirts --preview-only→浏览器验收→Package-Hd2dBryOutskirts。保留已锁定layouts与raw，不重跑Prepare覆盖生成记录。
本批27项连同BRY核心37项完成原清单布林64项美术视图；全项目745项范围不缩减，其余城市/聚落/野外继续制作。
'''
    (P/'IMPORT.md').write_text(text,encoding='utf-8')
    for a in m['assets']:(P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n类别{a["path"].split("/")[1]}；尺寸{a["size"]}；原点{a["origin"]}；BRY-CORE-128、静态RGBA、二值alpha。\n\n用途：{a["role"]}。nearest；不裁透明边；布局/家具/物件碰撞另定，alpha不是碰撞。SHA {a["sha256"]}。\n\n见IMPORT.md。静态图已核对，原生装配/运行尚待实测。\n',encoding='utf-8')
    print(json.dumps(dict(preview=str(P/'preview.html'),production_pngs=len(m['assets']),views=len(m['inventory_requests'])),ensure_ascii=False))
def package(m,v):
    pv=read(P/'preview-validation.json');assert pv['passed'] and pv['browser_verified'] and not pv['runtime_verified'];assert sha(P/'manifest.json')==pv['asset_manifest_sha256']==v['asset_manifest_sha256'];assert sha(P/'preview.html')==pv['preview_html_sha256'];assert len(pv['render_cases'])>=70
    for c in pv['render_cases']:assert len(c['gallery'])==60 and all(i['loaded'] for i in c['gallery'])
    for n,h in pv['proof_sha256'].items():assert sha(P/'previews'/n)==h
    out=P/'exports/HD2D-BRY-Outskirts-v1.zip';assert not out.exists(),'Released package immutable';files=[f for f in P.rglob('*') if f.is_file() and 'exports' not in f.relative_to(P).parts]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):z.write(f,f.relative_to(P).as_posix())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for a in m['assets']:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256']
    outreport=dict(path=out.relative_to(ROOT).as_posix(),bytes=out.stat().st_size,sha256=sha(out),files=len(files),production_pngs=len(m['assets']),zip_crc_and_asset_sha_verified=True,runtime_verified=False);(P/'exports/package-report.json').write_text(json.dumps(outreport,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(outreport,ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args();m=read(P/'manifest.json');v=read(P/'validation.json');assert v['passed'] and v['asset_manifest_sha256']==sha(P/'manifest.json');assert all(sha(P/a['path'])==a['sha256'] for a in m['assets']);assert all(sha(ROOT/n)==h for n,h in m['source_sha256'].items())
    if args.preview_only:preview(m,v)
    else:package(m,v)
