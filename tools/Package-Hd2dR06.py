"""R06 import notes, offline layered preview and browser-gated immutable package."""
from pathlib import Path
import argparse,json,hashlib,zipfile,importlib.util,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R06-highland-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
LABEL_VALUES=['旧钟站', '回声厅门房', '残光井口', '维护图棚', '空载试样棚', '钟站议桌棚', '独立钟架', '回头路线牌', '固定维护图', '工具架', '公共议桌', '封口取样托盘', '普通材料箱', '未点亮提灯', '冷却量测台', '回流阀位台', '残留响应台', '封闭介质小龛', '旁路刻尺', '远端机械锁', '密闭弃槽', '空载隔离台', '空载体槽', '侧置债簿桌', '辅助耦合·连接', '辅助耦合·封帽断开', '安全确认桌', '中性回执柜', '未装配封条板', '斜纹警示牌', '空长凳', '货运滑轮', '货箱', '两颗磨损对照螺栓', '维护阀', '封闭弃桶', '绕视线石柱', '固定副件柜']
def preview(m,v):
    spec=importlib.util.spec_from_file_location('r06_preview_base',ROOT/'tools/Package-Hd2dR02.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);html=base.HTML
    html=html.replace('丹布里西路与渡口','无名修院山地').replace('R02 / N5 / N9 / D03 / SQ04 / SQ05 / DT13','R06 / N14 / N15 / N16 / N17 / D09 / D10 / DT12 / DT15')
    html=html.replace('干燥地面','候选可走地面').replace('河面','非通行水面').replace('<label><input type="checkbox" id="repaired">桥面修复示意</label>','<label><input type="checkbox" id="coupling">辅助耦合断开示意</label><label><input type="checkbox" id="warning">预警范围示意</label>')
    html=re.sub(r'function canWalk\(s,x,y\)\{.*?\}',"function canWalk(s,x,y){const land=s.walkable_cells?s.walkable_cells.some(([a,b])=>a===x&&b===y):contains(s.walkable_rectangles,x,y);return land&&!contains(s.blocked_rectangles,x,y);}",html)
    html=html.replace("$('repaired').disabled=special||!(s.repaired_add_cells||[]).length;","$('coupling').disabled=special||plan||!s.illustration_variants?.coupling;$('warning').disabled=special||!s.illustration_variants?.warning;")
    a=html.index('const repair=');z=html.index('try{const images=',a)
    html=html[:a]+"""const coupling=$('coupling').checked&&!$('coupling').disabled,warning=$('warning').checked&&!$('warning').disabled,hasRoof=$('roof').checked&&!$('roof').disabled;
const water=s.id+'__water',mark=s.id+'__safety_markings';
const parts=special?[plan?s.plan:s.scene]:[s.id+'__backing',...(assets.has(water)?[water]:[]),s.id+'__floor',...(assets.has(mark)?[mark]:[]),...(plan?[]:[s.id+'__structure',...($('props').checked?[s.id+'__'+(coupling?'props_disconnected':'props_preview')]:[]),s.id+'__foreground',...(hasRoof?[s.id+'__roof']:[])]),...(warning?[s.id+'__pre_warning']:[])];
"""+html[z:]
    html=html.replace('images.forEach(im=>ctx.drawImage(im,0,0));',"images.forEach(im=>ctx.drawImage(im,0,0));canvas.dataset.renderedLayers=parts.join(',');")
    html=html.replace("+(repair?' · 修复桥面示意':'')","+(coupling?' · 辅助耦合断开示意':'')+(warning?' · 预警范围示意':'')")
    html=html.replace("'roof','repaired','grid'","'roof','coupling','warning','grid'")
    specials=[dict(id='r06_region',name_zh='无名修院山地 · 区域连接图',size=[1664,1248],plan='r06_region__plan',scene='r06_region__plan',note='10节点 / 11双向边 · 原创连接示意，非原生世界格'),dict(id='r06_echo_overview',name_zh='无名修院回声厅 · 前室与外廊总览',size=[1092,1534],plan='r06_echo__plan_overview',scene='r06_echo__working_overview',note='非对称前室 / 不进入发声室的维护廊 · 1:1拼版，非单间房'),dict(id='r06_residual_overview',name_zh='残光之井 · 双环与安全附室总览',size=[2262,1690],plan='r06_residual__plan_overview',scene='r06_residual__working_overview',note='48×40双环 / 独立安全台 / 维护接应通路 · 1:1拼版，非单间房')]
    html=re.sub(r'const specials=.*?;',lambda _:'const specials='+json.dumps(specials,ensure_ascii=False)+';',html)
    html=html.replace("$('scene').value='r02_tax_main'","$('scene').value='r06_residual_main'").replace("s.id==='r02_region'","s.id==='r06_region'")
    html=re.sub(r'const labels=.*?;',lambda _:'const labels='+json.dumps({a['id']:n for a,n in zip(read(P/'brief.json')['sprites'],LABEL_VALUES)},ensure_ascii=False)+';',html)
    html=html.replace('独立建筑与环境物件 · 18件','独立建筑与环境物件 · 38件').replace('五个建筑另含body与roof','六座建筑另含body与roof')
    html=html.replace('修复切换仅展示候选桥面。','两项切换是静态图形示意，不表示当前战斗、装置安全或任务结果，不改变通行格。').replace('公共桌、取样水口与返程均按空间约束绘制。人物、授权及任务结果由引擎处理。','非对称三测台、双环绕行与安全台分别绘制。读数、预警时机、人物、授权和终局冻结由引擎处理。').replace('旧渡口复用N1，区域图和多室拼版另标比例','18个独立场景 · 两处副本总览保持1:1原始比例')
    html=html.replace('<div id="gallery" class="gallery"></div>','<div id="gallery" class="gallery"></div><h2>独立机关图标 · 8件</h2><p>26×26手绘中性图标，交互、读数和状态由引擎控制。</p><div id="icons" class="gallery"></div>')
    html=html.replace("$('gallery').append(card);}draw();", "$('gallery').append(card);}for(const a of DATA.assets.filter(a=>a.role==='hand_pixel_neutral_engine_control_glyph_no_state')){const card=document.createElement('div');card.className='card';const im=document.createElement('img');im.src=a.path;im.alt=a.id;im.style.width='52px';im.style.imageRendering='pixelated';card.append(im);const t=document.createElement('small');t.textContent=a.id+' ·26×26';card.append(t);$('icons').append(card);}draw();")
    data=dict(scenes=m['scenes'],assets=m['assets'],region=m['region'],validation=v);(P/'preview.html').write_text(html.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    rows='\n'.join(f'| `{s["id"]}` {s["name_zh"]} | {s["size"][0]}×{s["size"][1]} | {s["cells"][0]}×{s["cells"][1]} |' for s in m['scenes'])
    doc=f'''# 无名修院山地 · R06场景美术v1

本批{len(m['assets'])}张生产PNG，18个独立场景、38个独立建筑/物件、36块26×26材质瓦片、8个独立手绘机关图标，对应23项原清单视图。{v['checks_passed']}项静态检查通过。原生房间、门、世界坐标、碰撞、保存、动态读数、视线、战斗和灯光天气尚待实际装配；本批不修改NPC与游戏包。

preview.html可离线检查平面/空间、屋顶、独立物件、26格网、通行掩码和门点。耦合断开与预警范围示意默认关闭，只换图形，不表示装置已安全、已击败首领或确认结局。

| 场景 | 像素尺寸 | 格数 |
|---|---|---|
{rows}

## 生产导入

assets/为生产目录；raw/为原稿，guides/为候选格图与屋顶掩码，sheets/为38精灵与36瓦片合集。所有路径相对本目录，nearest采样、关闭平滑和mipmap，保持完整透明画布。
1像素=1房间像素，场景原点(0,0)。物件左上角=(cellX×26+13,cellY×26+13)−sprite.origin，脚底底沿对准originY。
绘制顺序：backing→非通行water→floor→safety_markings白线→structure→按脚底Y排序的独立物件、建筑body和原生人物→foreground→可关闭roof。预警图形应由原生战斗预警时机另外绘制，静态预览不能当成伤害范围逻辑。
full/body/roof共画布共原点，不重叠、精确重组；roof_variants给出两个PNG相对路径。environment、working_space、props_preview、overview是检查合成图；交互物件使用items/独立PNG，避免重复烘焙。
layouts.json明确候选可走矩形、阻挡、门口、预留调查格与物件脚底。PNGalpha不是碰撞。机理、父对象、入口位置、实例创建与保存仍需原生装配。
耦合断开用props_disconnected替换props_preview，只换三个coupling_variant，不叠加旧连接图。两张104×78耦合精灵均用100×63可见拟合预算、原点(52,65)；NN和底沿补偿见crop_operations。v2封帽两端为可见实心圆板，旧C母图保留并继续供应另七物件。
八个ui/r06_icon_*.png为26×26、原点(13,13)的整数像素手绘图标，无确认勾、读数、授权或状态机；交互功能由引擎接线，图标可以独立替换。

## 空间约束

D09前室42×30，冷却量、回流阀位、残留响应是三个不同测台，读数面空白，源介质在高墙小龛中的封闭小匣。隔离白线是独立地面标识；维护外廊可单独核三个机械指示与曲线，不以进入发声室为前置。密闭弃槽与远端锁独立，不接人体。
D10主段48×40内外双环，中轴空载体槽、侧置债簿桌、三处错位辅助耦合、两根提案绕视线石柱。石柱不证明原生射线遮挡；待救预留位置和首领提案锚点分开。内环不可用时外环仍连入口、安全台和维护出口。
独立安全确认房不烘焙任何结局类型或冻结资格，确认前可回钟站，确认后普通物资接应不提升冻结资格。钟站议桌、公共厅和货运坡保持普通回程，不新增床位容量、无限库存或自动同意；空席不是本人同意。
预警范围是三段提案矩形的独立二值PNG，仅用于看图，不证明真实伤害、援兵、敌对或操作阶段。耦合/预警切换不写剧情、时序、结算、奖励、保存或碰撞。

## 比例、色板和来源

区域图1664×1248、10节点11边是Mod原创连接示意，图标缩小，名称由预览页叠字，不是官方地理或原生世界格。
回声总览1092×1534含前室/外廊两张1:1房图；残光总览2262×1690含双环/安全台/维护接应三张1:1房图，逐房像素保持，均不能作一间可走房。
36瓦片为四种材质各九个平面变体，边缘逐像素匹配，非47态边界自动瓦片；312×312大材质供铺面。
HIG-R06-128来自本项目AI山地概念：120种普通色＋8种小龛暗紫保留色。普通地面/墙/背景只用前120色，紫色限定封闭介质与预警/响应图标；小匣面另按组件归一化到这8种已锁定暗紫色（面域、色相筛选与铁锁排除见sprite-manifest.crop_operations），保留轮廓；不复制第二颗原作晶石，无烘焙紫光。
{v['new_generated_masters']}份生成原稿、完整提示词、输入/输出SHA与original_size记录在generation-log.json；独立封帽修订保留旧稿。原稿尺寸/间距可能偏离请求，裁切、NN、128色、二值alpha和屋顶掩码均记录，生产尺寸与原点精确锁定。
validation.json为静态证据，preview-validation.json为真实浏览器画面证据，均不代替游戏实机验证。复现：逐图Record-Hd2dArtGeneration→Export-Hd2dR06Materials→Export-Hd2dR06Sprites→Export-Hd2dR06→Validate-Hd2dR06→Package-Hd2dR06 --preview-only→浏览器检查→Package-Hd2dR06。不要重跑Prepare覆盖已锁定生成记录。
'''
    (P/'IMPORT.md').write_text(doc,encoding='utf-8')
    for a in m['assets']:(P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n类别{a["path"].split("/")[1]}；尺寸{a["size"]}；原点{a["origin"]}；HIG-R06-128、二值alpha、静态单帧。\n\n用途：{a["role"]}。nearest采样、保留完整画布；候选格和对象另定碰撞，不读alpha。SHA {a["sha256"]}。\n\n见IMPORT.md；原生装配/运行尚未验收。\n',encoding='utf-8')
    print(json.dumps(dict(preview=str(P/'preview.html'),pngs=len(m['assets']),views=len(m['inventory_requests'])),ensure_ascii=False))
def package(m,v):
    pv=read(P/'preview-validation.json');assert pv['passed'] and pv['browser_verified'] and not pv['runtime_verified'];assert sha(P/'manifest.json')==pv['asset_manifest_sha256']==v['asset_manifest_sha256'];assert sha(P/'preview.html')==pv['preview_html_sha256'];assert len(pv['render_cases'])>=49
    for c in pv['render_cases']:assert len(c['gallery'])==38 and all(i['loaded'] for i in c['gallery'])
    for c in pv['render_cases']:assert len(c['icons'])==8 and all(i['loaded'] for i in c['icons'])
    for n,h in pv['proof_sha256'].items():assert sha(P/'previews'/n)==h
    out=P/'exports/HD2D-R06-Highland-v1.zip';assert not out.exists(),'Released packages are immutable'
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
