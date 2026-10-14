"""R04 per-asset notes, offline preview and browser-gated package."""
from pathlib import Path
import argparse,json,hashlib,zipfile,importlib.util,re
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R04-pass-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
LABELS={'neutral_inn':'关外中立驿馆','store_house':'军需库门房','mason_shed':'石匠修理棚','windbreak':'退役营地避风棚','drug_pavilion':'卸药亭','seal_shelter':'短封印复核棚','beam_scale':'关前粮秤','comparison_board':'双栏对照板','mason_bench':'石匠工作台','cut_stones':'切砖石料','broken_cart':'冬粮断车','cargo_sacks':'粮袋','empty_drug_crate':'空药箱与空签','public_table':'公共监督桌','drug_rack':'普通药架','drug_cabinet':'药柜','case_cabinet':'病例柜','stop_cabinet':'停机日志柜','return_mail_cabinet':'退信柜','empty_bed':'单张空护理床','two_medicine_bowls':'两只药碗','sealed_pair':'停机治疗床与载体槽','oil_casks':'油桶','oil_spill':'油迹','seal_comparison_table':'封印对照桌','drag_rope':'拖索痕','blank_notice':'空白告示牌','rolled_bedding':'卷铺盖','broken_rack':'废损药架'}
def preview(m,v):
    spec=importlib.util.spec_from_file_location('r04_preview_base',ROOT/'tools/Package-Hd2dR02.py');base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base);html=base.HTML
    html=html.replace('丹布里西路与渡口','柏石关与退役驿道').replace('R02 / N5 / N9 / D03 / SQ04 / SQ05 / DT13','R04 / N7 / N11 / D06 / SQ02 / SQ08 / DT05 / DT14')
    html=html.replace('干燥地面','可走地面').replace('background:#2e454d','background:#5F4939').replace('河面','场地外缘')
    html=html.replace('<label><input type="checkbox" id="repaired">桥面修复示意</label>','').replace("$('repaired').disabled=special||!(s.repaired_add_cells||[]).length;",'').replace("const repair=$('repaired').checked&&!$('repaired').disabled,hasRoof=","const repair=false,hasRoof=").replace("'roof','repaired','grid'","'roof','grid'")
    html=re.sub(r'function canWalk\(s,x,y\)\{.*?\}',"function canWalk(s,x,y){return contains(s.walkable_rectangles,x,y)&&!contains(s.blocked_rectangles,x,y);}",html)
    specials=[dict(id='r04_region',name_zh='柏石关 · 区域连接图',size=[1664,1248],plan='r04_region__plan',scene='r04_region__plan',note='10节点 / 11双向边 · 原创连接示意，非原生世界格'),dict(id='r04_cellar_overview',name_zh='军需地窖 · 四空间拼版',size=[1664,1326],plan='r04_cellar__plan_overview',scene='r04_cellar__working_overview',note='主段 / 废损库 / 油库 / 通行沟 · 1:1拼版，不能作为单间房')]
    html=re.sub(r'const specials=.*?;',lambda _: 'const specials='+json.dumps(specials,ensure_ascii=False)+';',html);html=html.replace("$('scene').value='r02_tax_main'","$('scene').value='r04_cellar_main'").replace("s.id==='r02_region'","s.id==='r04_region'")
    labels={'r04_'+k:n for k,n in LABELS.items()};html=re.sub(r'const labels=.*?;',lambda _: 'const labels='+json.dumps(labels,ensure_ascii=False)+';',html)
    source=next(s for s in read(ROOT/'research/story-regions.json') if s['id']=='R04');names={'R04-'+n[0]:n[1] for n in source['nodes']}
    html=html.replace("ctx.fillText(n.name_zh,x,y+75)","ctx.fillText(DATA.region.labels_zh[n.id]||n.name_zh,x,y+75)")
    html=html.replace('独立建筑与环境物件 · 18件','独立建筑与环境物件 · 29件').replace('五个建筑另含body与roof','六座建筑另含body与roof').replace('修复切换仅展示候选桥面。','').replace('公共桌、取样水口与返程均按空间约束绘制。人物、授权及任务结果由引擎处理。','官署入口、废损库和通行沟分别绘制。治疗床与载体槽为空，装置已停机；文字和人物由引擎处理。').replace('旧渡口复用N1，区域图和多室拼版另标比例','十处场地与六个室内 · 区域图与四室拼版另标比例')
    region=dict(m['region'],labels_zh=names);data=dict(scenes=m['scenes'],assets=m['assets'],region=region,validation=v);(P/'preview.html').write_text(html.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    rows='\n'.join(f'| `{s["id"]}` {s["name_zh"]} | {s["size"][0]}×{s["size"][1]} | {s["cells"][0]}×{s["cells"][1]} |' for s in m['scenes'])
    text=f'''# 柏石关与退役驿道 · R04场景美术v1

本批{len(m['assets'])}张生产PNG：十处地表场地、六个独立室内、29个独立建筑/道具、36块26×26材质瓦片，另含墙窗材质、屋顶分层及检查合成图；对应原清单22项视图。{v['checks_passed']}项静态检查通过。原生房间、世界坐标、门、碰撞、存档与天气尚待装配测试。
NPC形象、对白与事件由另一模型负责，本批不修改游戏包或存档。

preview.html可离线切换平面/空间、屋顶、环境物件、26格网、通行掩码与门点。床、槽、药碗与柜上的文字保持中性，不画已同意、治愈、监督签约、赦免或任务结果。

| 场景 | 像素尺寸 | 格数 |
|---|---|---|
{rows}

## 生产导入

使用assets/内PNG；raw/是原始母图，guides/是制作格图与屋顶掩码，sheets/是可选精灵合集。路径全部相对本目录，nearest采样、关闭平滑与mipmap，保留画布，不自动裁边。
场景1像素=1房间像素，原点(0,0)。物件左上角=(cellX×26+13,cellY×26+13)-sprite.origin；独立PNG的可见底沿对准originY。
绘制顺序：backing→floor→structure→按脚底Y排序的独立物件、建筑body和原生人物→foreground→可关闭roof。full/body/roof同尺寸同原点，不重叠且精确重组；full的roof_variants字段给出直接可读的两个PNG路径。
props_preview、environment、working_space与overview仅供检查；交互对象使用items/内独立PNG，避免重复烘焙物件。单张素材只提供画面，原生对象父项、碰撞、交互盒、门板与落点需要引擎装配。
layouts.json明确候选格、阻挡、门口、调查点及物件位置。PNGalpha不能作为碰撞。室内的窗和后侧墙在structure，低前沿在foreground；关闭屋顶展示外立面前部，进入建筑使用独立室内场景。

## 空间与状态边界

D06主段40×32格，长装卸轴与垂直药柜短廊分开；废损药库、油库、旧通行沟为三张独立场景。关闭官方入口、配对区域和油库后，废库到通行沟仍有候选可走路，病例、药柜与固定日志不靠再次试验取得。
油迹和空白警示牌可见，火险与文字由引擎处理；油库不是核心证据必经路。本图不要求消灭驻军或强试病人。
驿馆普通护理间仅提案一张空床和两只药碗，不保证床位库存或护理效果；地窖另有空治疗床、载体槽与关闭管路，不生成第二个军医身体。
关外粮秤、卸药亭、断车点、封印复核棚、交换场分别有布局。固定箱签、秤数、印章、日期、家信地址和监督结果不烘焙进图；药柜12抽屉是图形分格，不能当成实际库存格承诺。
石匠绕行道保留R02/R03/R05的候选接口；本批只校验格图连通，原生敌对/犯罪/保存与进出仍待运行测试。

## 连接图、拼版与来源

r04_region__plan是1664×1248原创连接示意，10节点/11双向边，图标另缩小；名称由预览页面叠字，不是原作官方地理或原生世界格。
军需地窖plan_overview与working_overview均1664×1326，四室1:1拼版，不能当一间房。36瓦片是四种材质各九个平面变体，非47态边界自动瓦片；312×312大材质供铺面使用。
generation-log.json保留11张生成原稿，包括药柜/地面两次定向修订。v1药柜、v1粗材质原稿保留，旧40张材质PNG及当时清单/校验保留在versions/materials-v1。
原始母图尺寸与布局可能偏离请求；original_size、crop_operations记录实际返回尺寸、完整裁区、NN缩放、128色量化和二值alpha。生产PNG尺寸和原点精确符合锁定规范。色板来自本项目AI生成PAS概念图，未复制商业图集。
validation.json只证明静态文件/色板/原点、屋顶重组、接缝、提案通达和来源；preview-validation.json另记录浏览器画面，均不代表原生游戏运行验收。
复现：准备规范→逐图生成与Record-Hd2dArtGeneration→Export-Hd2dR04Materials→Export-Hd2dR04Sprites→Export-Hd2dR04→Validate-Hd2dR04→Package-Hd2dR04 --preview-only→浏览器检查→Package-Hd2dR04。
'''
    (P/'IMPORT.md').write_text(text,encoding='utf-8')
    for a in m['assets']:(P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n类别：{a["path"].split("/")[1]}。尺寸：{a["size"]}；原点：{a["origin"]}；PAS-R04-128、二值alpha、静态单帧。\n\n用途：{a["role"]}。nearest采样、保留完整画布；碰撞由显式候选格/对象另定，不读取alpha。SHA：{a["sha256"]}。\n\n完整场景与比例见IMPORT.md；原生装配/运行尚未验收。\n',encoding='utf-8')
    print(json.dumps(dict(preview=str(P/'preview.html'),pngs=len(m['assets']),views=len(m['inventory_requests'])),ensure_ascii=False))
def package(m,v):
    pv=read(P/'preview-validation.json');assert pv['passed'] and pv['browser_verified'] and not pv['runtime_verified'];assert sha(P/'manifest.json')==pv['asset_manifest_sha256']==v['asset_manifest_sha256'];assert sha(P/'preview.html')==pv['preview_html_sha256'];assert len(pv['render_cases'])>=40
    for c in pv['render_cases']:assert len(c['gallery'])==29 and all(i['loaded'] for i in c['gallery'])
    for n,h in pv['proof_sha256'].items():assert sha(P/'previews'/n)==h,n
    out=P/'exports/HD2D-R04-Pass-v1.zip';files=[f for f in P.rglob('*') if f.is_file() and 'exports' not in f.relative_to(P).parts]
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
