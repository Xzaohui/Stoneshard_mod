"""Brynn core layered preview/import notes; package only after browser evidence."""
from pathlib import Path
import argparse,json,hashlib,zipfile,importlib.util,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-core-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
LABELS=['公告试印长廊','老楼租屋块','船工绳棚','岸上空泊亭','副工场','水尺观测屋','双闸维护屋','中立夜会馆','试印台','活字分类盘','空白试样纸','分账见证桌','封口钱袋','三方空白赞助筹','修补租牌','封闭旧门','左组旧烟灰手印','右组旧烟灰手印','未点亮纪念灯','分名绳筹架','独立货押挂钩','空泊位系缆钉','解除绳结','旧席留空牌','未点亮锻炉','空夹具试铆台','两件制作者标记样片','断铆钉','离体衬垫样本','封口药瓶','空白指导签','高低双水尺','水闸杆','分节止塞','干砂排放模型','短议桌','三枚空白提名筹','空租户凳','隐私屏风','空白邀函']
def preview(m,v):
    spec=importlib.util.spec_from_file_location('bry_preview_base',ROOT/'tools/Package-Hd2dR02.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);h=base.HTML
    h=h.replace('丹布里西路与渡口','布林 · 六处任务场所').replace('R02 / N5 / N9 / D03 / SQ04 / SQ05 / DT13','BRY / 公告廊 / 租屋巷 / 船工街 / 副工场 / 水门 / 夜会馆')
    h=h.replace('干燥地面','候选可走地面').replace('河面','非通行水面').replace('<label><input type="checkbox" id="repaired">桥面修复示意</label>','<label><input type="checkbox" id="tide">码头涨水示意</label><label><input type="checkbox" id="model">干砂模型止塞示意</label>')
    h=re.sub(r'function canWalk\(s,x,y\)\{.*?\}',"function canWalk(s,x,y){if($('tide').checked&&!$('tide').disabled)return s.high_tide_walkable_cells.some(([a,b])=>a===x&&b===y);return contains(s.walkable_rectangles,x,y)&&!contains(s.blocked_rectangles,x,y);}",h)
    h=h.replace("$('repaired').disabled=special||!(s.repaired_add_cells||[]).length;","$('tide').disabled=special||!s.illustration_variants?.tide;$('model').disabled=special||plan||!s.illustration_variants?.model;")
    a=h.index('const repair=');z=h.index('try{const images=',a)
    h=h[:a]+"""const tide=$('tide').checked&&!$('tide').disabled,model=$('model').checked&&!$('model').disabled,hasRoof=$('roof').checked&&!$('roof').disabled;
const water=s.id+'__'+(tide?'high_tide_water':'water'),mark=s.id+'__stair_markings',blue=s.id+'__plan_structure';
const parts=special?[plan?s.plan:s.scene]:[s.id+'__backing',...(assets.has(water)?[water]:[]),s.id+'__'+(tide?'high_tide_floor':'floor'),...(plan&&assets.has(blue)?[blue]:[]),...(assets.has(mark)?[mark]:[]),...(plan?[]:[s.id+'__'+(tide?'high_tide_structure':'structure'),...($('props').checked?[s.id+'__props_preview']:[]),s.id+'__'+(tide?'high_tide_foreground':'foreground'),...(hasRoof?[s.id+'__roof']:[]),...(model&&$('props').checked?[s.id+'__model_demo']:[])])];
"""+h[z:]
    h=h.replace('images.forEach(im=>ctx.drawImage(im,0,0));',"images.forEach(im=>ctx.drawImage(im,0,0));canvas.dataset.renderedLayers=parts.join(',');")
    h=h.replace("+(repair?' · 修复桥面示意':'')","+(tide?' · 涨水候选步道示意':'')+(model?' · 干砂模型止塞示意':'')").replace("'roof','repaired','grid'","'roof','tide','model','grid'")
    special=[dict(id='bry_city',name_zh='布林 · 六处任务场所连接图',size=[1664,1248],plan='bry_city__plan',scene='bry_city__plan',note='六处Mod场所参照原作四区 · 连接示意，非官方地理或原生世界格')]
    h=re.sub(r'const specials=.*?;',lambda _:'const specials='+json.dumps(special,ensure_ascii=False)+';',h).replace("$('scene').value='r02_tax_main'","$('scene').value='bry_d01'").replace("s.id==='r02_region'","s.id==='bry_city'")
    h=re.sub(r'const labels=.*?;',lambda _:'const labels='+json.dumps({a['id']:n for a,n in zip(read(P/'brief.json')['sprites'],LABELS)},ensure_ascii=False)+';',h)
    h=h.replace('独立建筑与环境物件 · 18件','独立建筑与环境物件 · 40件').replace('五个建筑另含body与roof','八座建筑另含body与roof')
    h=h.replace('修复切换仅展示候选桥面。','涨水切换只展示低步道的候选图形；模型切换只展示干砂台上的止塞图形，均不改变游戏状态。').replace('公共桌、取样水口与返程均按空间约束绘制。人物、授权及任务结果由引擎处理。','公共回程、私密授权和实际处置分别处理。名字、读数、人物与任务结果由引擎绘制。').replace('旧渡口复用N1，区域图和多室拼版另标比例','18个独立场景 · 六处任务场所参照原作四区 · 涨水和模型默认关闭')
    data=dict(scenes=m['scenes'],assets=m['assets'],region=m['region'],validation=v);(P/'preview.html').write_text(h.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    rows='\n'.join(f'| `{s["id"]}` {s["name_zh"]} | {s["size"][0]}×{s["size"][1]} | {s["cells"][0]}×{s["cells"][1]} |' for s in m['scenes'])
    doc=f'''# 布林核心任务场所 · HD-2D v1

本批{len(m['assets'])}张生产PNG、18个独立场景（六处街区＋十二处A/B工作空间）、40个独立建筑/环境精灵、36块26×26材质瓦片，完成37项原清单视图。{v['checks_passed']}项静态检查通过；原生房间、门索引、世界坐标、物件碰撞、保存、天气和灯光仍待游戏装配。本批不改NPC、对白、GML或游戏包。

preview.html可离线查看平面地图、空间、屋顶、物件、26格网、候选通行掩码和门点。码头涨水、干砂模型止塞示意默认关闭；前者只切换候选低步道图形，后者只加模型台上的图形，均不提交游戏时序、闸位、授权、任务、奖励或保存。

| 场景 | 像素尺寸 | 格数 |
|---|---|---|
{rows}

## 生产导入

assets/为生产素材，raw/为九份完整原稿，guides/为候选可走格与屋顶掩码，sheets/为40精灵和36瓦片合集。所有路径相对本目录，nearest采样，关闭平滑/mipmap；保留完整透明画布，不自动裁边。
1像素=1房间像素，场景原点(0,0)。物件左上角=(cellX×26+13,cellY×26+13)−sprite.origin，脚底底沿对齐originY。未测量的原生门、楼梯高差和碰撞不能从这些提案坐标推定。
空间绘制顺序：backing→非通行water→floor→stair_markings→structure（包括后墙印迹）→按脚底Y排序的独立建筑body/物件及原生人物→foreground→可关闭roof→可选model_demo。
封口钱袋附着于分账桌、制作者样片附着于试铆台，按draw_after_instance紧接宿主绘制，不应在普通脚底排序时被桌面遮挡；独立PNG与宿主关系保留在layouts.json。
八座建筑full/body/roof共画布共原点，body与roof不重叠且精确重组full；roof_variants给出两个相对PNG路径。environment、working_space、props_preview是检查合成图；原生可交互物件用items/独立PNG，避免重复烘焙。
平面图顺序：backing→water→floor→plan_structure→stair_markings。plan_structure为阻挡区域的平面示意；PNGalpha不是碰撞，地面格仍以布局提案单独登记。
涨水须同时替换floor/water/structure/foreground为high_tide_*，不能只加水而保留旧步道墙；预览通行掩码同步用high_tide_walkable_cells。这仍是美术候选图，不证明原生水位、寻路或存档功能。
两组烟灰手印是独立墙面贴图，不按物件脚底放置：左上角=(cellX×26+13−originX,cellY×26−PNG高度)，本房后墙78像素高，手印上方不裁切、不与地面重叠。78×39竖墙样片非整格地砖，PAM的三条尺寸警告已按此用途复核。

## 各场所约束

D01公告廊有开敞通廊与浅院；公开试印、账额范围和三方赞助分别保留，不以赞助换普通阅读。账额台在视线外区，封口钱袋和三枚空白筹独立，不画姓名、数值或授权结果。
D02老楼保留公共楼梯与两翼中间通巷，不借私人卧房通行、不增加床位。封闭旧门不是出口；两组旧手印各自作为观察印迹，不代替物主、死亡或原谅判断。
D03高栈与低侧步道并列；涨水只关闭[12,24]—[31,29]低段，所有门、调查预留格和高位回程保持可达。岸上空泊亭、系缆钉、旧席牌和分名绳筹分开，不画船、尸体或失踪者归来。B空间是岸上工作亭，不能当作新船舱。
D04公共访客绕行避开员工炉区；炉子是未点亮基础图，不表示剧情已停工。空夹具、制作者样片、断铆钉、离体衬垫、封口药瓶和指导签分别制作，不画人体试验、治愈或同意。
D05观测廊的高低双尺和旧水线无数字，不当水位裁决。维护间两根闸杆、分节止塞和干砂模型独立；模型灰色线是槽内衬，台面保持砂，不表示真实进水。model_demo只加两枚止塞示意，真实floor/water不换。
D06议事厅恰好三张短桌、中央空地和空租户凳；提名筹留空，空席不是同意。候谈廊恰好三盏独立未点亮灯，两端街道退场门不受屏风与私密拒绝关闭。
十二处A/B空间均有两处候选街道回程，授权、拒绝和账目封闭不锁公共道路。物件碰撞、门锁条件、NPC位置和实际互动由原生装配另行验证。

## 比例、色板与来源

城市连接图1664×1248、六节点六环边及18条核心空间边，参照原作四区来组织Mod任务场所，不是六个官方城区，不确定官方地理、银行或全国权限。城市图标明确缩小，不能作为房间物件尺寸导入。
四种312×312材料面与各九块26×26平面瓦片使用BRY-CORE-128（来自本项目AI布林概念图）；36瓦片逐边匹配，非47态边界自动瓦片。不复制原作商业图集。
九份母图的实际尺寸、完整提示词与输入/输出SHA见generation-log.json；实际尺寸/间距偏离请求时，裁切、NN、128色量化、二值alpha、脚底补偿与屋顶掩码保留在清单中，生产尺寸/原点精确。
validation.json为静态证据；preview-validation.json为浏览器展示证据，两者均不代替游戏运行。37项只计布林核心，三处卫星与六处续篇的27项仍在原745视图范围中待制作，不缩减范围。
复现顺序：逐图Record-Hd2dArtGeneration→Export-Hd2dBryMaterials→Export-Hd2dBrySprites→Export-Hd2dBryCore→Validate-Hd2dBryCore→Package-Hd2dBryCore --preview-only→浏览器检查→Package-Hd2dBryCore。不要重跑Prepare覆盖已锁定母图记录。
'''
    (P/'IMPORT.md').write_text(doc,encoding='utf-8')
    for a in m['assets']:(P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n类别{a["path"].split("/")[1]}；尺寸{a["size"]}；原点{a["origin"]}；BRY-CORE-128、二值alpha、静态单帧。\n\n用途：{a["role"]}。nearest采样、保留完整画布；格图和物件碰撞另定，不读alpha。SHA {a["sha256"]}。\n\n见IMPORT.md；原生装配与运行尚未验收。\n',encoding='utf-8')
    print(json.dumps(dict(preview=str(P/'preview.html'),pngs=len(m['assets']),views=len(m['inventory_requests'])),ensure_ascii=False))
def package(m,v):
    pv=read(P/'preview-validation.json');assert pv['passed'] and pv['browser_verified'] and not pv['runtime_verified'];assert sha(P/'manifest.json')==pv['asset_manifest_sha256']==v['asset_manifest_sha256'];assert sha(P/'preview.html')==pv['preview_html_sha256'];assert len(pv['render_cases'])>=46
    for c in pv['render_cases']:assert len(c['gallery'])==40 and all(i['loaded'] for i in c['gallery'])
    for n,h in pv['proof_sha256'].items():assert sha(P/'previews'/n)==h
    out=P/'exports/HD2D-BRY-Core-v1.zip';assert not out.exists(),'Released packages are immutable'
    files=[f for f in P.rglob('*') if f.is_file() and 'exports' not in f.relative_to(P).parts]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):z.write(f,f.relative_to(P).as_posix())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for a in m['assets']:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256']
    report=dict(path=out.relative_to(ROOT).as_posix(),bytes=out.stat().st_size,sha256=sha(out),files=len(files),production_pngs=len(m['assets']),zip_crc_and_asset_sha_verified=True,runtime_verified=False);(P/'exports/package-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args();m=read(P/'manifest.json');v=read(P/'validation.json');assert v['passed'] and v['asset_manifest_sha256']==sha(P/'manifest.json');assert all(sha(P/a['path'])==a['sha256'] for a in m['assets']);assert all(sha(ROOT/n)==h for n,h in m['source_sha256'].items())
    if args.preview_only:preview(m,v)
    else:package(m,v)
