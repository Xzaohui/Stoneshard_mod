"""Build the R02 scene-art handoff only after asset quality validation passes."""
from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R02-river-v1'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    m=read(P/'manifest.json');v=read(P/'validation.json')
    assert v['passed'] and not v['errors'],'Complete quality validation before packaging'
    for a in m['assets']:assert sha(P/a['path'])==a['sha256'],a['path']
    for path,h in m['source_sha256'].items():assert sha(ROOT/path)==h,'Source changed: '+path
    for a in m['assets']:
        im=Image.open(P/a['path']).convert('RGBA')
        colors=set(px[:3] for px in im.get_flattened_data() if px[3])
        text=f'''# {a['id']}

- Category: {a['path'].split('/')[1]}
- Size: {im.width}x{im.height}
- Origin: {a['origin']}
- Colors used: {len(colors)} from DEN-R02-128
- Animation: none
- Design notes: {a['role']}
- Sampling: nearest; no mipmaps; keep the full canvas.
- Collision: proposed cell geometry in layouts.json, never alpha.
- Variants: architectural full/body/roof share their canvas and origin; repaired layers do not commit story state.
- Runtime: pending native integration. NPC content belongs to the other model.
'''
        (P/f"notes/{a['id']}.md").write_text(text,encoding='utf-8')
    data=dict(scenes=m['scenes'],assets=m['assets'],region=m['region'],validation=v)
    (P/'preview.html').write_text(HTML.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    table='\n'.join(f"| {s['name_zh']} `{s['id']}` | {'×'.join(map(str,s['size']))} | {'×'.join(map(str,s['cells']))} |" for s in m['scenes'])
    handoff=f'''# 丹布里西路与渡口 · R02 场景美术 v1

本批输出{len(m['assets'])}张生产PNG、18个独立建筑/环境精灵、36块26×26平面材料瓦片、10处场景，完成18项原清单视图。{v['checks_passed']}项静态检查通过。
它们是可导入的美术素材；原生游戏房间、世界坐标、门对象、保存生命周期和动态灯光仍待装配测试。
人物区域保持空白，NPC图像、对白及事件由另一模型负责。

打开preview.html可离线查看分层场景、平面地图、屋顶、物件、26格网、通行掩码、出口和修复桥面示意。
assets/是生产导入目录；raw/保留生成母图和复用源，不导入母图。相对路径可整体搬移。

| 场景 | 像素尺寸 | 格数 |
|---|---|---|
{table}

## 导入方式

1像素＝1房间像素，使用nearest采样，关闭平滑和mipmap。场景原点(0,0)，透明画布不能自动裁边。
绘制顺序：backing → floor → structure → 按脚底Y排序的独立物件/建筑body与原生人物 → foreground → 可关闭roof。
独立物件位置：左上角=(cellX×26+13, cellY×26+13)−sprite.origin。foot_anchor供放置校准。
建筑full/body/roof共用画布和原点，body与roof不重叠并精确重组full。door_anchor相对于精灵画布，与interaction_hint分别登记；税房门口偏离中线，接入原生门时须按door_anchor校准。
props_preview、environment、working_space和repaired_preview为检查合成图，交互物件须使用items/中的独立PNG，避免重复画出物件。
layouts.json逐场登记可走矩形、阻挡、cutout_rectangles水口、门点和预留交互格；不能以PNG透明度代替碰撞。

## 桥面、空间与剧情接口

D03主段42×32、院落30×22。税栈斜桥缺口和护路维修坡均另有repaired_floor/repaired_structure/repaired_foreground及repair_overlay。
完整修复示意使用三张repaired层替换对应base层，不能只加桥面而保留旧缺口边墙。固定浅滩和普通步行回路始终保留；图片切换不提交修桥、许可或任务状态。
客店公共桌能看见河面，公共汤灶与匿名病例柜在公开侧；姓名柜位于隔断内。没有擅自设定收费客房床数或绘制专用客房。
岸井三个取样水口分别保留，过滤架、匿名病例柜和姓名柜分开；图像不表示治愈或已获姓名公开同意。
轮印及三处木夹痕为可检查形状，放大图仅作观察，不证明物主、授权或调查结论。火焰、姓名、库存、许可和人物由引擎独立绘制。
region-layout.json为8节点、9双向边的区域拓扑提案；图上位置不是原生世界格。R01/R03/R04接口和门对象尚未接入游戏。

## 比例和复用

r02_region__plan为1664×1248连接示意，文字只由预览页面叠加。
r02_tax__plan_overview为1092×1430主段/院落1:1拼版；r02_tax__working_overview为780×1066院落/税房1:1拼版，均不是一间可走房间。
旧渡口沿用N1已有三个场景：r02_ferryold__plan_overview为1040×806、三张平面图各50%比例；site沿用1040×780岸院图并量化到本批色板，没有新增重复原生房间。
r02_crate_corner_detail为208×208放大观察图；r02_ferry_map_icon为156×130地图图标，均不能按房间物件比例放置。
36块材料瓦片为四种材料各九个平面变体，边缘逐像素匹配，不是47态边界自动瓦片。场景地面另用312×312母图纹理避免26格重复过密。

## 来源与验收

色板DEN-R02-128来自本项目既有AI生成的丹布里概念图，未复制原作商业图集。
generation-log.json保留9次新增生成的完整提示词、参考、输入/输出哈希及8份复用源。manifest.json保留裁切、原点、输出SHA和来源文档SHA。
岸井初始生成几何归档是在制作阶段按原约束恢复的图，哈希也是恢复后测量；日志明确区分，未冒称生成前即时采样证据。后续三水口及棚体边墙校准属于制作几何。
validation.json只证明静态色板、二值alpha、尺寸/原点、屋顶重组、瓦片接缝、候选通达、分柜与区域拓扑检查；preview-validation.json（若存在）为浏览器展示证据，均不代表游戏运行验收。
重建顺序：Prepare-Hd2dR02.py → Export-Hd2dR02.py → Validate-Hd2dR02.py → Package-Hd2dR02.py。
原稿和旧批次保留；本轮不更新游戏包。
'''
    (P/'IMPORT.md').write_text(handoff,encoding='utf-8')
    if (P/'preview-validation.json').is_file():
        preview=read(P/'preview-validation.json')
        assert preview['passed'] and preview['browser_verified'] and not preview['runtime_verified']
        assert len(preview['render_cases'])==26
        for case in preview['render_cases']:
            assert len(case['gallery'])==18 and all(im['loaded'] for im in case['gallery'])
        preview['proof_sha256']={n:sha(P/'previews'/n) for n in preview['proofs']}
        preview.update(asset_manifest_sha256=sha(P/'manifest.json'),preview_html_sha256=sha(P/'preview.html'))
        (P/'preview-validation.json').write_text(json.dumps(preview,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    out=P/'exports/HD2D-R02-River-v1.zip'
    files=[f for f in P.rglob('*') if f.is_file() and 'exports' not in f.relative_to(P).parts]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):z.write(f,f.relative_to(P).as_posix())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for a in m['assets']:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256']
    report=dict(path=out.relative_to(ROOT).as_posix(),bytes=out.stat().st_size,sha256=sha(out),files=len(files),production_pngs=len(m['assets']),zip_crc_and_asset_sha_verified=True,runtime_verified=False)
    (P/'exports/package-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

HTML=r'''<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>丹布里西路与渡口 · HD-2D场景预览</title>
<style>*{box-sizing:border-box}body{margin:0;background:#151a1c;color:#e4ded1;font:15px "Microsoft YaHei","Segoe UI",sans-serif}header{padding:22px 30px;border-bottom:1px solid #48504d;background:#202728}h1{margin:0 0 7px;font-size:25px}p{line-height:1.65;margin:7px 0;color:#bcb7aa}main{display:grid;grid-template-columns:280px 1fr}aside{padding:22px;background:#202728;border-right:1px solid #48504d}label{display:block;margin:14px 0;line-height:1.5}select{font:inherit;color:#e4ded1;background:#333d3d;border:1px solid #70766d;border-radius:4px;padding:7px;width:100%}input{accent-color:#c3a16b;margin-right:9px}label:has(input:disabled){opacity:.45}section{padding:20px;overflow:auto}#board{background:#11171a;overflow:auto;max-width:100%;min-height:350px}canvas{display:block;image-rendering:pixelated}#info{margin:17px 0;padding:12px;border:1px solid #48504d;color:#d2c8b3}#status{color:#d6b879}.legend{display:flex;gap:15px;padding:10px 0;font-size:13px}.dot{display:inline-block;width:11px;height:11px;margin-right:5px}.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(175px,1fr));gap:15px;margin:24px 0}.card{padding:12px;border:1px solid #515751;background:#252d2e;border-radius:4px}.sprite{height:155px;display:flex;align-items:center;justify-content:center;background:repeating-conic-gradient(#353c3b 0% 25%,#2a3132 0% 50%) 50%/20px 20px}.sprite img{image-rendering:pixelated;max-height:145px;max-width:100%;object-fit:contain}.card small{display:block;color:#bcb7aa;padding-top:8px}a{color:#d6b879}footer{padding:14px 30px;color:#aab2ad;border-top:1px solid #48504d}@media(max-width:850px){main{grid-template-columns:1fr}aside{border-right:0}}</style>
<header><h1>丹布里西路与渡口</h1><p>HD-2D场景素材 · R02 / N5 / N9 / D03 / SQ04 / SQ05 / DT13</p><span id="status">正在载入分层素材…</span></header>
<main><aside><label for="scene">查看场景<select id="scene"></select></label><label for="mode">视图<select id="mode"><option value="scene">空间展示</option><option value="plan">平面地图</option></select></label><label for="zoom">缩放<select id="zoom"><option value="fit" selected>适合窗口</option><option value="0.5">50%</option><option value="1">100% 原尺寸</option><option value="2">200% 像素检查</option></select></label><label><input type="checkbox" id="props" checked>环境物件与建筑前部</label><label><input type="checkbox" id="roof" checked>建筑屋顶</label><label><input type="checkbox" id="repaired">桥面修复示意</label><label><input type="checkbox" id="grid">26×26格网</label><label><input type="checkbox" id="mask">通行掩码</label><label><input type="checkbox" id="doors">出口与预留交互点</label><div id="info"></div><p>绿色为可走格，红色为阻挡；橙色为出口，浅绿色为预留交互格。修复切换仅展示候选桥面。</p><p>公共桌、取样水口与返程均按空间约束绘制。人物、授权及任务结果由引擎处理。</p><a href="IMPORT.md">导入说明</a> · <a href="manifest.json">资源清单</a> · <a href="../../index.html">场景素材库</a></aside>
<section><div class="legend"><span><i class="dot" style="background:#a39277"></i>干燥地面</span><span><i class="dot" style="background:#2e454d"></i>河面</span><span id="coords">移动鼠标查看格坐标</span></div><div id="board"><canvas id="canvas"></canvas></div><h2 style="font-size:18px;margin-top:26px">独立建筑与环境物件 · 18件</h2><p>单帧透明PNG，脚底原点统一；五个建筑另含body与roof。</p><div id="gallery" class="gallery"></div></section></main><footer>静态素材已验收 · 原生游戏房间待装配测试 · 旧渡口复用N1，区域图和多室拼版另标比例</footer>
<script>
const DATA=__DATA__, $=id=>document.getElementById(id),canvas=$('canvas'),ctx=canvas.getContext('2d'),cache=new Map(),assets=new Set(DATA.assets.map(a=>a.id));let revision=0;
const specials=[{id:'r02_region',name_zh:'西路与渡口 · 区域连接图',size:[1664,1248],plan:'r02_region__plan',scene:'r02_region__plan',note:'8节点 / 9双向边 · 连接示意，非原生世界格'}, {id:'r02_ferryold',name_zh:'旧渡口 · N1现有场景',size:[1040,780],planSize:[1040,806],plan:'r02_ferryold__plan_overview',scene:'r02_ferryold__site',note:'岸院1:1；平面图三室各50%拼版 · 无新增重复房间'}, {id:'r02_tax_overview',name_zh:'断桥税栈 · 多空间拼版',size:[780,1066],planSize:[1092,1430],plan:'r02_tax__plan_overview',scene:'r02_tax__working_overview',note:'主段/院落平面及院落/税房工作空间 · 1:1拼版，非单间房'}];
for(const s of [...DATA.scenes,...specials]){const opt=document.createElement('option');opt.value=s.id;opt.textContent=s.name_zh;$('scene').append(opt);}$('scene').value='r02_tax_main';
function load(id){const path=`assets/backgrounds/${id}.png`;if(!cache.has(path))cache.set(path,new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(new Error('无法载入 '+path));im.src=path;}));return cache.get(path);}
const contains=(rs,x,y)=>(rs||[]).some(([a,b,c,d])=>x>=a&&x<=c&&y>=b&&y<=d);
function canWalk(s,x,y){const repaired=$('repaired').checked&&!$('repaired').disabled;return repaired&&(s.repaired_add_cells||[]).some(([a,b])=>a===x&&b===y)||(contains(s.walkable_rectangles,x,y)&&!contains(s.blocked_rectangles,x,y)&&!contains(s.cutout_rectangles,x,y));}
async function draw(){const rev=++revision,s=DATA.scenes.find(s=>s.id===$('scene').value)||specials.find(s=>s.id===$('scene').value),special=!s.cells,plan=$('mode').value==='plan';
for(const id of ['grid','mask','doors'])$(id).disabled=special;$('props').disabled=special||plan;$('roof').disabled=special||plan||!assets.has(s.id+'__roof');$('repaired').disabled=special||!(s.repaired_add_cells||[]).length;
const repair=$('repaired').checked&&!$('repaired').disabled,hasRoof=$('roof').checked&&!$('roof').disabled;
const parts=special?[plan?s.plan:s.scene]:plan?['backing',repair?'repaired_floor':'floor'].map(p=>s.id+'__'+p):['backing',repair?'repaired_floor':'floor',repair?'repaired_structure':'structure',...($('props').checked?['props_preview']:[]),repair?'repaired_foreground':'foreground',...(hasRoof?['roof']:[])].map(p=>s.id+'__'+p);
try{const images=await Promise.all(parts.map(load));if(rev!==revision)return;const size=special&&plan&&s.planSize?s.planSize:s.size;canvas.width=size[0];canvas.height=size[1];ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,...size);images.forEach(im=>ctx.drawImage(im,0,0));
const zoom=$('zoom').value==='fit'?Math.min(1,Math.max(.2,($('board').clientWidth-12)/size[0]),Math.max(350,innerHeight-220)/size[1]):+$('zoom').value;canvas.style.width=size[0]*zoom+'px';canvas.style.height=size[1]*zoom+'px';
if(!special&&$('mask').checked)for(let y=0;y<s.cells[1];y++)for(let x=0;x<s.cells[0];x++){ctx.fillStyle=canWalk(s,x,y)?'rgba(53,196,113,.22)':'rgba(211,73,65,.24)';ctx.fillRect(x*26,y*26,26,26);}
if(!special&&$('grid').checked){ctx.strokeStyle='rgba(218,225,217,.35)';ctx.lineWidth=1;ctx.beginPath();for(let x=0;x<=size[0];x+=26){ctx.moveTo(x+.5,0);ctx.lineTo(x+.5,size[1]);}for(let y=0;y<=size[1];y+=26){ctx.moveTo(0,y+.5);ctx.lineTo(size[0],y+.5);}ctx.stroke();}
if(!special&&$('doors').checked)for(const[items,color]of[[s.exits,'#e7af52'],[s.reserved,'#9de0b4']])for(const e of items){const[x,y]=e.cell;ctx.strokeStyle=color;ctx.lineWidth=2;ctx.strokeRect(x*26+3,y*26+3,20,20);}
if(s.id==='r02_region'){ctx.font='24px Microsoft YaHei';ctx.textAlign='center';for(const n of DATA.region.nodes){const[x,y]=DATA.region.art_anchor_pixels[n.id];ctx.fillStyle='#141a1e';ctx.fillRect(x-105,y+48,210,36);ctx.fillStyle='#ded0ad';ctx.fillText(n.name_zh,x,y+75);}}
$('info').textContent=`${s.name_zh} · ${size.join(' × ')} 像素`+(special?' · '+s.note:` · ${s.cells.join(' × ')} 格`)+(repair?' · 修复桥面示意':'');$('status').textContent=`${DATA.assets.length}张生产PNG · ${DATA.validation.checks_passed}项静态检查通过 · 原生房间待装配`;$('coords').textContent=special?'示意 / 拼版：不可当作房间坐标':'移动鼠标查看格坐标';
}catch(e){$('status').textContent=e.message;}}
for(const id of ['scene','mode','zoom','props','roof','repaired','grid','mask','doors'])$(id).addEventListener('change',draw);window.addEventListener('resize',draw);
canvas.addEventListener('mousemove',e=>{const s=DATA.scenes.find(s=>s.id===$('scene').value);if(!s)return;const r=canvas.getBoundingClientRect(),x=Math.floor((e.clientX-r.left)*canvas.width/r.width/26),y=Math.floor((e.clientY-r.top)*canvas.height/r.height/26);$('coords').textContent=`格 ${x},${y} · ${canWalk(s,x,y)?'可走':'阻挡'}`;});
const labels={r02_ferry_inn:'渡口客店',r02_tax_house:'税房',r02_filter_shelter:'岸井过滤棚',r02_repair_canopy:'维修棚',r02_inspection_shed:'有限查验棚',r02_bridge_pier:'斜桥桥墩',r02_public_table:'公共桌',r02_privacy_screen:'私密隔断',r02_case_cabinet:'匿名病例柜',r02_name_cabinet:'姓名柜',r02_filter_rack:'过滤架',r02_sample_bucket:'取样桶',r02_mooring_post:'系船桩',r02_crate_corner:'木夹痕箱角',r02_repair_timbers:'维修木料',r02_soup_stove:'公共汤灶',r02_road_sign:'空白路标',r02_inspection_table:'有限查验桌'};
for(const a of DATA.assets.filter(a=>a.role==='independent_environment_sprite')){const card=document.createElement('div');card.className='card';const box=document.createElement('div');box.className='sprite';const im=document.createElement('img');im.src=a.path;im.alt=labels[a.id];box.append(im);card.append(box);const text=document.createElement('small');text.textContent=`${labels[a.id]} · ${a.size.join('×')} · 原点(${a.origin.join(',')})`;card.append(text);$('gallery').append(card);}draw();
</script></html>'''
if __name__=='__main__':main()
