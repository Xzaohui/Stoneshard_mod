"""Ship scene PNGs with an offline native-resolution art preview and import notes."""
from pathlib import Path
import json,hashlib,zipfile,importlib.util
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-streets-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def main():
    m=read('manifest.json');v=read('validation.json');assert v['passed'] and not v['errors'],'Successful validation required before packaging'
    for a in m['assets']:
        assert sha(P/a['path'])==a['sha256'],a['id'];im=Image.open(P/a['path']);n=len({p[:3] for p in im.get_flattened_data() if p[3]})
        (P/f'notes/{a["id"]}.md').write_text(f'# {a["id"]}\n\n- Category: {a["path"].split("/")[1]}\n- Size: {im.width}x{im.height}\n- Origin: {a["origin"]}\n- Colors: {n} from BRY-R01-128\n- Animation: none\n- Design: {a["role"]}\n- Sampling: nearest; retain transparent canvas\n- Runtime: pending native integration; scenes only\n',encoding='utf-8')
    s=importlib.util.spec_from_file_location('camp_art_preview',ROOT/'tools/Package-Hd2dR01.py');old=importlib.util.module_from_spec(s);s.loader.exec_module(old)
    html=old.HTML.replace('灰堤与旧渠','布林外港 · 场景绘制').replace('HD-2D场景素材 · 布林外港 · N2 / D02','HD-2D场景素材 · 港街 / 听审棚 / 工坊 / 盐路 / 租屋')
    options=''.join(f'<option value="{s["id"]}">{s["name_zh"]}</option>' for s in m['scenes'])+'<option value="r01_region">R01区域连接总览（示意）</option>'
    start=html.index('<select id="scene">');end=html.index('</select>',start)
    html=html[:start]+'<select id="scene">'+options+html[end:]
    html=html.replace("s.id==='r01_camp'","DATA.assets.some(a=>a.id===s.id+'__roof')")
    html=html.replace("plan=$('mode').value==='plan'","plan=$('mode').value==='plan'||s.schematic")
    for control in ['mask','grid','doors']:html=html.replace(f"if($('{control}').checked)",f"if($('{control}').checked&&!s.schematic)")
    html=html.replace("`${s.name_zh} · ${s.size.join(' × ')} 像素 · ${s.cells.join(' × ')} 格`","`${s.name_zh} · ${s.size.join(' × ')} 像素 · ${s.schematic?'七条连接 · 非世界坐标':s.cells.join(' × ')+' 格'}`")
    html=html.replace("$('coords').textContent=`格 ${x},${y} · ${canWalk(s,x,y)?'可走':'阻挡'}`;","$('coords').textContent=s.schematic?'区域示意 · 非原生世界坐标':`格 ${x},${y} · ${canWalk(s,x,y)?'可走':'阻挡'}`;")
    labels=dict(r01_port_kiosk='港街复核亭',r01_hearing_canopy='半开放听审棚',r01_rental_house='熄灯租屋',r01_forge_building='冷炉工坊',r01_abandoned_post='弃置驿站',r01_notice_board='空白公示栏',r01_twin_ledger_table='双副账工作桌',r01_stamp_bench='压印台',r01_basic_repair_bench='基础修理台',r01_storage_chest='封闭寄存箱',r01_drying_rack='晾纸架',r01_ash_stove='冷灰炉',r01_water_basin='取水石盆')
    start=html.index('const labels=');end=html.index(';',start)
    html=html[:start]+'const labels='+json.dumps(labels,ensure_ascii=False)+html[end:]
    schematic=dict(id='r01_region',name_zh='R01区域连接总览（示意）',size=[1664,1248],cells=[64,48],schematic=True,walkable_rectangles=[],blocked_rectangles=[],exits=[],reserved=[])
    data=dict(scenes=m['scenes']+[schematic],assets=m['assets'],validation=v,region=m['region'])
    html=html.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    # Labels belong to the preview/engine, not the import PNGs.
    html=html.replace("$('info').textContent=", "if(s.schematic){ctx.font='18px Microsoft YaHei';ctx.textAlign='center';for(const n of DATA.region.nodes){const [x,y]=DATA.region.art_anchor_pixels[n.id];ctx.fillStyle='#0F1218';ctx.fillRect(x-114,y+58,228,30);ctx.fillStyle='#DBCAA2';ctx.fillText(n.name_zh,x,y+81);}}$('info').textContent=")
    (P/'preview.html').write_text(html,encoding='utf-8')
    table='\n'.join('| '+s['id']+' | '+s['name_zh']+' | '+'×'.join(map(str,s['size']))+' | '+'×'.join(map(str,s['cells']))+' |' for s in m['scenes'])
    handoff=f'''# 布林外港街区场景素材 v1

本批继续负责场景绘制。{len(m['assets'])}张生产PNG、13个独立建筑与道具、5张局部场景，加1张区域连接总览；对应原清单9项视图。{v['checks_passed']}项静态检查通过。
本批为可导入美术和空间制作提案，尚未安装为原生游戏房间。NPC图像、对白和行为由另一模型负责。

打开preview.html，切换场景、平面图、屋顶、26格、通行掩码及出口点。它在解压目录离线可用。

| ID | 场景 | 像素 | 格数 |
|---|---|---|---|
{table}

区域图r01_region__plan为1664×1248的连接示意图；六个节点、七条双向边与R01设计一致，显示锚点不等于世界格坐标。区域图标缩为1/2，只用于地图显示；不得作为实际房间尺寸或碰撞。

**导入**：使用assets/的RGBA PNG，关闭平滑与mipmap，保持透明画布。场景层1像素＝1房间像素，原点(0,0)。
层次：backing→floor→structure→按脚底Y排序的独立body/道具与原生人物→foreground→可关闭roof。
建筑full/body/roof共用相同画布与原点，body和roof不重叠、可以逐像素重组full。roof隐藏只影响视觉，不替代室内房间或权限。
物件左上角=(cellX×26+13,cellY×26+13)-sprite.origin。脚底已经对齐originY，保留画布，禁止自动裁边。
props_preview、environment、working_space是检查图，实际交互使用items中的单独PNG。NPC不能烘焙进这些层。

**空间接口**：manifest.json登记尺寸、原点、相对路径和SHA；layouts.json登记地面与阻挡提案；manifest.scenes另含门边开口。
各场景所有可走格连通，出口和预留点可达。碰撞采用显式格方案，经原生引擎测试后接入，不能从PNG透明度推测。
听审公共通路与私租屋入口分开。租屋只含工作桌、晾纸架和冷炉，没有新造床位；进入授权、纸张内容及冷炉证据状态由任务逻辑处理。
工坊大炉、普通修理台与压印台为独立对象，停大炉或处分资产时仍可保留基础修理。
公示栏和纸张不含文字；使用引擎字体和对应状态。寄存箱只表示外观，不声明容量或库存。灯光、火焰、处置后变化须独立绘制。

**来源和重建**：原始母图在raw/，完整提示词与输入/输出SHA在generation-log.json，裁切/最近邻组装见manifest.crop_operations；未复制商业图集。
指定Pixel Asset Master skill commit：33d891c421a9ad3608f5a09af97271388ca923af。实际调用其finalize_assets.py量化/清理与asset_validator.py验收。
raw母图保持不变；港街最早输入中的蓝色基础已在导出时换为干地。建筑占地与出口开口在生产几何中校正，生图时输入另存guides/*_generation_v1.png。
重建顺序：Prepare-Hd2dR01Streets.py→Prepare-Hd2dR01Region.py→Export-Hd2dR01Streets.py→Validate-Hd2dR01Streets.py→Package-Hd2dR01Streets.py。
本批不修改游戏包、角色存档或NPC源码。原生门、保存、镜头、碰撞、人物遮挡与动态灯光仍需游戏装配验收。
'''
    (P/'IMPORT.md').write_text(handoff,encoding='utf-8')
    out=P/'exports/HD2D-R01-Streets-v1.zip';files=[f for f in P.rglob('*') if f.is_file() and 'exports' not in f.relative_to(P).parts]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):z.write(f,f.relative_to(P).as_posix())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None,'ZIP CRC failure'
        for a in m['assets']:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256'],a['path']
    report=dict(path=out.relative_to(ROOT).as_posix(),bytes=out.stat().st_size,sha256=sha(out),files=len(files),production_pngs=len(m['assets']),zip_crc_and_asset_sha_verified=True,runtime_verified=False)
    (P/'exports/package-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
