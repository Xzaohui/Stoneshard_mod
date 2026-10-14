"""R05 import notes, offline layered preview and browser-gated immutable package."""
from pathlib import Path
import argparse,json,hashlib,zipfile,importlib.util,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R05-basin-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
LABELS=dict(zip(['care_lodge','ward_house','well_drain_shed','filter_well','voluntary_hut','high_archive_shed','water_bucket_pair','warning_board','public_table','water_gauge','reed_cluster','sample_bucket','herb_bundle','filter_rack','medicine_cabinet','case_cabinet','name_cabinet','inspection_table','closed_sample_tray','empty_care_bed','privacy_curtain','schedule_board','old_living_pipe','new_waste_pipe','new_waste_pipe_capped','valve_closed','clamp_pair','low_gate','bypass_wheel','lift_platform','high_record_cabinet','optional_parameter_shelf','research_refuge_door','workers_refuge_door','maintenance_ladder','empty_crate','sitting_bench','waste_casks','foam_decal','inactive_basin'],['隔离营护理棚','疫所与后建翼','档案井排水棚','过滤村井','自愿安置棚','高位副件棚','双桶与区分图形','双栏取水警示','公共桌','水位刻尺','寒地芦苇','取样桶','普通草束','过滤架','药柜','匿名病例柜','私密姓名柜','查验桌','封口样本托盘','单张空护理床','双柱隔帘','空白排班板','旧生活水管','新废液管·连接','新废液管·封帽断开','关闭阀','新旧管夹','低闸','旁通轮','空货物升降台','固定副件柜','可选参数架','研究者避险门','工人避险门','维修梯','空货箱','等候凳','废液桶','泡沫贴花','小型停用盆']))
def preview(m,v):
    spec=importlib.util.spec_from_file_location('r05_preview_base',ROOT/'tools/Package-Hd2dR02.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);html=base.HTML
    html=html.replace('丹布里西路与渡口','灰烬湿地与疫村').replace('R02 / N5 / N9 / D03 / SQ04 / SQ05 / DT13','R05 / N8 / N12 / N13 / D07 / D08 / SQ05 / SQ07')
    html=html.replace('干燥地面','候选可走地面').replace('河面','非通行水面').replace('<label><input type="checkbox" id="repaired">桥面修复示意</label>','<label><input type="checkbox" id="pipe">新管断开示意</label><label><input type="checkbox" id="tide">低水位示意</label>')
    html=re.sub(r'function canWalk\(s,x,y\)\{.*?\}',"function canWalk(s,x,y){const land=s.walkable_cells?s.walkable_cells.some(([a,b])=>a===x&&b===y):contains(s.walkable_rectangles,x,y);return land&&!contains(s.blocked_rectangles,x,y);}",html)
    html=html.replace("$('repaired').disabled=special||!(s.repaired_add_cells||[]).length;","$('pipe').disabled=special||plan||!s.illustration_variants?.pipe;$('tide').disabled=special||!s.illustration_variants?.water;")
    a=html.index('const repair=');z=html.index('try{const images=',a)
    html=html[:a]+"""const pipe=$('pipe').checked&&!$('pipe').disabled,tide=$('tide').checked&&!$('tide').disabled,hasRoof=$('roof').checked&&!$('roof').disabled;
const water=s.id+'__'+(tide?'water_lowered':'water');
const parts=special?[plan?s.plan:s.scene]:[s.id+'__backing',...(assets.has(water)?[water]:[]),s.id+'__floor',...(plan?[]:[s.id+'__structure',...($('props').checked?[s.id+'__'+(pipe?'props_disconnected':'props_preview')]:[]),s.id+'__foreground',...(hasRoof?[s.id+'__roof']:[])])];
"""+html[z:]
    html=html.replace('images.forEach(im=>ctx.drawImage(im,0,0));',"images.forEach(im=>ctx.drawImage(im,0,0));canvas.dataset.renderedLayers=parts.join(',');")
    html=html.replace("+(repair?' · 修复桥面示意':'')","+(pipe?' · 新管断开示意':'')+(tide?' · 低水位示意':'')")
    html=html.replace("'roof','repaired','grid'","'roof','pipe','tide','grid'")
    specials=[dict(id='r05_region',name_zh='灰烬湿地 · 区域连接图',size=[1664,1248],plan='r05_region__plan',scene='r05_region__plan',note='8节点 / 9双向边 · 原创连接示意，非原生世界格'),dict(id='r05_ward_overview',name_zh='灰烬疫所 · 四段总览',size=[1742,1482],plan='r05_ward__plan_overview',scene='r05_ward__working_overview',note='主廊 / 废液翼 / 旧侧房 / 接应坡 · 1:1拼版，非单间房'),dict(id='r05_well_overview',name_zh='沉水档案井 · 总览1/2 三层井环',size=[2002,2002],plan='r05_well__plan_overview',scene='r05_well__working_overview',note='上环 / 中环 / 下环 · 三间独立38×38格房，1:1拼版；附室见总览2/2'),dict(id='r05_well_annex_overview',name_zh='沉水档案井 · 总览2/2 避险与维修',size=[2002,2002],plan='r05_well_annex__plan_overview',scene='r05_well_annex__working_overview',note='研究者避险室 / 工人避险室 / 维修通道 · 1:1拼版，非单间房')]
    html=re.sub(r'const specials=.*?;',lambda _:'const specials='+json.dumps(specials,ensure_ascii=False)+';',html)
    html=html.replace("$('scene').value='r02_tax_main'","$('scene').value='r05_ward_main'").replace("s.id==='r02_region'","s.id==='r05_region'")
    html=re.sub(r'const labels=.*?;',lambda _:'const labels='+json.dumps({'r05_'+k:n for k,n in LABELS.items()},ensure_ascii=False)+';',html)
    html=html.replace('独立建筑与环境物件 · 18件','独立建筑与环境物件 · 40件').replace('五个建筑另含body与roof','六座建筑另含body与roof')
    html=html.replace('修复切换仅展示候选桥面。','两项状态切换仅改变图形，不提交任务或改变通行格。').replace('公共桌、取样水口与返程均按空间约束绘制。人物、授权及任务结果由引擎处理。','三个井环与两扇避险门分别绘制。人物、授权、水质、救援与机关时序由引擎处理。').replace('旧渡口复用N1，区域图和多室拼版另标比例','21个独立场景 · 双页井环总览保持1:1原始比例')
    data=dict(scenes=m['scenes'],assets=m['assets'],region=m['region'],validation=v);(P/'preview.html').write_text(html.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    rows='\n'.join(f'| `{s["id"]}` {s["name_zh"]} | {s["size"][0]}×{s["size"][1]} | {s["cells"][0]}×{s["cells"][1]} |' for s in m['scenes'])
    doc=f'''# 灰烬湿地与疫村 · R05场景美术v1

本批{len(m['assets'])}张生产PNG、21个独立场景、40个独立建筑/物件、36块26×26平面材质瓦片，对应原清单19项视图。{v['checks_passed']}项静态检查通过。原生房间、门、碰撞、世界坐标、保存、水位机关和天气光照仍待实际装配测试；本批不修改游戏或NPC内容。

preview.html可离线检查平面/空间、屋顶、独立物件、26格网、通行掩码和门点。新管断开/低水位示意默认关闭，只换图层，不提交任务、救援挑战、时序、死亡、奖励或碰撞。

| 场景 | 像素尺寸 | 格数 |
|---|---|---|
{rows}

## 导入约定

assets/是生产目录；raw/保留原稿，guides/为候选格图与屋顶掩码，sheets/为40精灵与36瓦片合集。全为相对路径；nearest采样、关闭平滑和mipmap，保留透明画布。
1像素=1房间像素，场景原点(0,0)。物件左上角=(cellX×26+13,cellY×26+13)−sprite.origin，独立物件可见底沿对准originY。
绘制顺序：backing→非通行water→floor→structure→按脚底Y排序的独立物件、建筑body与原生人物→foreground→roof。full/body/roof同尺寸同原点，不重叠且精确重组，full.roof_variants为两个直接可读路径。
environment、props_preview、working_space和overview仅供检查；交互物件使用items/内独立PNG，避免重复烘焙。layouts.json明确候选通行格、阻挡、门口与预留交互格；三个井环用walkable_cells显式格表。PNGalpha不作碰撞。
水面分层限于非通行格。低水位替换water_lowered，mask与基础水面完全相同，不添加可走路。新管断开用props_disconnected替换整个props_preview，不能叠加到仍连通的管线上；只替换标有pipe_variant的新废液管，旧生活水管保持不变。两状态可同时展示。
三种管线都用156×52画布、原点(78,43)、152×41共同可见拟合范围，以端点和脚底对齐；NN缩放/底沿补偿见crop_operations。
独立警示双桶、不同形状的桶牌和泡沫用于视觉区分；图上棕红/白色不独自证明水质，文字与实际危害由引擎实现。样本托盘不接人，柜中文字不烘焙。

## 场景约束

D07前段46×34格，短横廊、三处空床和隔帘，后建废液翼、小型停用盆侧房、排液坡分别是独立场景。封闭废液翼和旧侧房后，前门到接应坡仍连通。基本护理、普通取水和回程在外部隔离营；图不要求接受试验或迁居。
D08上/中/下为三间独立38×38环房，中央水坑非通行，研究者与工人有不同的门口、门图和附室目标。固定安全副件在上环高棚，可选参数在中环另架；三层维修回程保留。预览没有自动死亡计时、实时水位物理或进入即触发挑战。
护理空床提案为营内2、疫所3、安置棚1，不承诺实际床位、人数、同意或护理效果。病例柜与姓名柜分开，有限账目、身份与住址由引擎授权后显示。

## 比例与制作来源

区域图1664×1248、8节点/9边，仅为Mod原创连接图，图标缩小，不代表官方地理或原生世界格。
疫所总览1742×1482，四段1:1拼版，26px重叠仅在相同空白非通行边框，逐房所有像素保留。
井环总览两页各2002×2002：第一页三层井环，第二页两间独立避险室及维修通道。两页一起覆盖六空间，各房不缩小、不复制为游戏房；不能把总览当一间可走房。notes/assembly-supplement.json解释复数总览的分页装配，原spec_lock哈希和单房尺寸不变。
四种材质各九个瓦片是平面变体，非47态边界自动瓦片；312×312材质供整面铺设，全部边缘匹配。{v["new_generated_masters"]}份生成原稿保留完整提示词、输入/输出哈希及original_size。v1大地砖原稿和40张当时材质输出存于versions/materials-v1，v2细化后用于最终场景。
ASH-R05-128源本项目既有AI寒凉盆地概念，未复制商业图集。raw母图返回尺寸/间距可能偏离请求，裁切、NN缩放、二值alpha、区域128色和屋顶掩码均记录；生产PNG尺寸/原点严格锁定。
validation.json与preview-validation.json分别是静态与浏览器证据，不能证明游戏运行。复现：逐图Record-Hd2dArtGeneration→Export-Hd2dR05Materials→Export-Hd2dR05Sprites→Export-Hd2dR05→Validate-Hd2dR05→Package-Hd2dR05 --preview-only→浏览器检查→Package-Hd2dR05。不要重跑Prepare覆盖已锁定原稿记录。
'''
    (P/'IMPORT.md').write_text(doc,encoding='utf-8')
    for a in m['assets']:(P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n类别{a["path"].split("/")[1]}；尺寸{a["size"]}；原点{a["origin"]}；ASH-R05-128、二值alpha、静态单帧。\n\n用途：{a["role"]}。nearest采样、保留完整画布；候选格和对象另定碰撞，不读alpha。SHA {a["sha256"]}。\n\n见IMPORT.md；原生装配/运行尚未验收。\n',encoding='utf-8')
    print(json.dumps(dict(preview=str(P/'preview.html'),pngs=len(m['assets']),views=len(m['inventory_requests'])),ensure_ascii=False))
def package(m,v):
    pv=read(P/'preview-validation.json');assert pv['passed'] and pv['browser_verified'] and not pv['runtime_verified'];assert sha(P/'manifest.json')==pv['asset_manifest_sha256']==v['asset_manifest_sha256'];assert sha(P/'preview.html')==pv['preview_html_sha256'];assert len(pv['render_cases'])>=57
    for c in pv['render_cases']:assert len(c['gallery'])==40 and all(i['loaded'] for i in c['gallery'])
    for n,h in pv['proof_sha256'].items():assert sha(P/'previews'/n)==h
    out=P/'exports/HD2D-R05-Basin-v1.zip';assert not out.exists(),'Released packages are immutable'
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
