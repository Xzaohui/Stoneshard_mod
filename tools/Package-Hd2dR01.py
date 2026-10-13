"""Create scene preview, import handoff and ZIP after R01 asset validation passes."""
from pathlib import Path
import json,hashlib,zipfile
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PARENT=ROOT/'src/Art/hd2d_26x26_20261013';P=PARENT/'batches/R01-camp-canal-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    m=json.loads((P/'manifest.json').read_text(encoding='utf-8'));validation=json.loads((P/'validation.json').read_text(encoding='utf-8'))
    assert validation['passed'] and not validation['errors'],'Run successful validation before packaging'
    for a in m['assets']:assert sha(P/a['path'])==a['sha256'],a['path']
    for a in m['assets']:
        im=Image.open(P/a['path']);palette=set(px[:3] for px in im.get_flattened_data() if px[3])
        (P/f'notes/{a["id"]}.md').write_text(f'# {a["id"]}\n\n- Category: {a["path"].split("/")[1]}\n- Size: {im.width}x{im.height}\n- Origin: {a["origin"]}\n- Colors used: {len(palette)} from BRY-R01-128\n- Animation: none\n- Design notes: {a["role"]}\n- Variants: full/body/roof architecture parts share the same canvas and origin.\n- Runtime: pending native integration; NPC content belongs to the other model.\n',encoding='utf-8')
    data=dict(scenes=m['scenes'],assets=m['assets'],validation=validation)
    html=HTML.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    (P/'preview.html').write_text(html,encoding='utf-8')
    handoff='''# 灰堤工营与旧渠场景美术 v1

本批负责场景绘制。NPC 图像、对白与任务事件由另一模型负责。
已输出40张生产PNG、9个独立建筑/环境物件、3张局部地图；对应5项原清单视图。381项静态检查通过。
这是一批可导入素材，几何为台本约束下的制作提案，尚未装配或验证为原生游戏房间。

打开 preview.html 可离线切换场景、平面图、物件、屋顶、26格网、通行掩码和门点。
所有路径相对本目录；原图在 raw/，生产导入使用 assets/，不要导入生图原稿。

| 场景 | 画布 | 格数 | 用途 |
|---|---|---|---|
| r01_camp | 1040×780 | 40×30 | N2灰堤工营：空棺、雇工棚、拆轴工地 |
| r01_canal_pump | 1352×884 | 52×34 | D02泵房、双水槽、桥、维护梯与干燥侧间 |
| r01_canal_tomb | 936×728 | 36×28 | D02下层墓龛环道与干燥平台 |

导入比例为1像素＝1房间像素；关闭平滑和mipmap。场景层原点(0,0)，保留透明画布，不能自动裁边。
draw order：backing → floor → structure → 按脚底Y排序的独立物件/建筑body与原生人物 → foreground → 可关闭roof。
建筑full/body/roof三版本使用相同尺寸和原点；body与roof不重叠，可精确重组full。
props_preview、environment、working_space和overview是预览/拼版；实际交互物件使用items中的独立PNG。
两个overview均为1352×1638、保持两层1:1比例的上下拼版，不能当一间可走房间。

物件位置公式：左上角=(cellX*26+13,cellY*26+13)-sprite.origin。
独立物件的实际底沿对准originY；foot_anchor与interaction_hint供后续对象校准，不能直接把alpha当碰撞。
layouts.json中的可走格、阻挡矩形、门点与预留格是本批空间接口；NPC模型按各场景空位接入人物，不需要把人物烘焙进背景。
各房间所有可走格连通；初始入口和维护返程不靠人物授权解锁。原生转场、保存与犯罪/碰撞行为仍须后续安装测试。

工营棺内只放旧外套，不表示确认死亡；轴座为空，不表示本人已经回营。
泵房生活侧间有两格宽维护开口，铺盖和水壶只作独立环境图；下层墓室没有住户床位。
闸轮是中性静态图，没有烘焙所选放水方法；灯光、机关、水位变化与文字由引擎独立绘制。
旧渠入口为独立建筑图，户外地形位置及门洞接入尚待装配。

完整提示词、输入/输出哈希：generation-log.json；裁切与量化：manifest.json；静态证据：validation.json。
材料来自本项目AI生成母图与既有Mod概念图，未复制商业图集。
重建：python tools/Prepare-Hd2dR01.py → python tools/Export-Hd2dR01.py → python tools/Validate-Hd2dR01.py → python tools/Package-Hd2dR01.py。
泵房初始生图输入已归档为guides/r01_canal_pump_generation_v1.png；生活侧间边墙在制作几何中另行补齐。
'''
    handoff=handoff.replace('381项',str(validation['checks_passed'])+'项').replace('40张',str(len(m['assets']))+'张')
    (P/'IMPORT.md').write_text(handoff,encoding='utf-8')
    out=P/'exports/HD2D-R01-Camp-Canal-v1.zip'
    files=[f for f in P.rglob('*') if f.is_file() and 'exports' not in f.relative_to(P).parts]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):z.write(f,f.relative_to(P).as_posix())
    report=dict(path=out.relative_to(ROOT).as_posix(),bytes=out.stat().st_size,sha256=sha(out),files=len(files),production_pngs=len(m['assets']),runtime_verified=False)
    (P/'exports/package-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))

HTML=r'''<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>灰堤与旧渠 · HD-2D场景预览</title>
<style>*{box-sizing:border-box}body{margin:0;background:#151a1c;color:#e4ded1;font:15px "Microsoft YaHei","Segoe UI",sans-serif}header{padding:24px 32px;border-bottom:1px solid #48504d;background:#202728}h1{margin:0 0 7px;font-size:25px;letter-spacing:1px}p{line-height:1.65;margin:7px 0;color:#bcb7aa}main{display:grid;grid-template-columns:275px 1fr;min-height:760px}aside{padding:25px;background:#202728;border-right:1px solid #48504d}label{display:block;margin:16px 0;line-height:1.5}select,button{font:inherit;color:#e4ded1;background:#333d3d;border:1px solid #70766d;border-radius:4px;padding:8px}select{width:100%}input{accent-color:#c3a16b;margin-right:9px}section{padding:22px;overflow:auto}#board{background:#11171a;overflow:auto;max-width:100%;min-height:550px}canvas{display:block;image-rendering:pixelated;image-rendering:crisp-edges}#info{margin:17px 0;padding:12px;border:1px solid #48504d;color:#d2c8b3}#status{color:#d6b879}.legend{display:flex;gap:15px;padding:15px 0;font-size:13px}.dot{display:inline-block;width:11px;height:11px;margin-right:5px}.gallery{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:15px;margin:24px 0}.card{padding:12px;border:1px solid #515751;background:#252d2e;border-radius:4px}.sprite{height:155px;display:flex;align-items:center;justify-content:center;background:repeating-conic-gradient(#353c3b 0% 25%,#2a3132 0% 50%) 50%/20px 20px}.sprite img{image-rendering:pixelated;max-height:145px;max-width:100%;object-fit:contain}.card small{display:block;color:#bcb7aa;padding-top:8px;overflow-wrap:anywhere}a{color:#d6b879}footer{padding:14px 32px;color:#aab2ad;border-top:1px solid #48504d}@media(max-width:850px){main{grid-template-columns:1fr}aside{border-right:0}#board{min-height:300px}}</style>
<header><h1>灰堤与旧渠</h1><p>HD-2D场景素材 · 布林外港 · N2 / D02</p><span id="status">正在载入分层素材…</span></header>
<main><aside><label for="scene">查看场景<select id="scene"><option value="r01_camp">灰堤工营</option><option value="r01_canal_pump">旧渠泵房与生活侧间</option><option value="r01_canal_tomb">下层墓龛环道</option></select></label><label for="mode">视图<select id="mode"><option value="scene">空间展示</option><option value="plan">平面地图</option></select></label><label for="zoom">缩放<select id="zoom"><option value="fit" selected>适合窗口</option><option value="0.5">50%</option><option value="0.75">75%</option><option value="1">100% 原尺寸</option><option value="2">200% 像素检查</option></select></label><label><input type="checkbox" id="props" checked>环境物件与建筑前部</label><label><input type="checkbox" id="roof" checked>建筑屋顶</label><label><input type="checkbox" id="grid">26×26格网</label><label><input type="checkbox" id="mask">通行掩码</label><label><input type="checkbox" id="doors">出口与预留交互点</label><div id="info"></div><p>关闭屋顶可检查工作空间。绿色为可走地面，红色为阻挡；橙色为出口，浅绿色为预留交互点。</p><p>人物由另一模型接入。本批为可导入美术，游戏房间装配与动态灯光待验收。</p><a href="IMPORT.md">导入说明</a> · <a href="manifest.json">资源清单</a></aside>
<section><div class="legend"><span><i class="dot" style="background:#a39277"></i>干燥平台</span><span><i class="dot" style="background:#2e454d"></i>低位水道</span><span id="coords">移动鼠标查看格坐标</span></div><div id="board"><canvas id="canvas"></canvas></div><h2 style="font-size:18px;margin-top:28px">独立建筑与环境物件</h2><p>单帧透明PNG；建筑另含body与roof分层。</p><div id="gallery" class="gallery"></div></section></main><footer>原稿与提示词完整保留 · 每像素与每格分别校验 · 场景中不烘焙人物或剧情结论</footer>
<script>
const DATA=__DATA__;window.SCENE_ART=DATA;const $=id=>document.getElementById(id),canvas=$('canvas'),ctx=canvas.getContext('2d'),cache=new Map();let revision=0;
function load(path){if(!cache.has(path))cache.set(path,new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(new Error('无法载入 '+path));im.src=path;}));return cache.get(path);}
function canWalk(s,x,y){return s.walkable_rectangles.some(([a,b,c,d])=>x>=a&&x<=c&&y>=b&&y<=d)&&!s.blocked_rectangles.some(([a,b,c,d])=>x>=a&&x<=c&&y>=b&&y<=d);}
async function draw(){const rev=++revision,s=DATA.scenes.find(s=>s.id===$('scene').value),plan=$('mode').value==='plan';const parts=plan?['plan']:['backing','floor','structure',...($('props').checked?['props_preview']:[]),'foreground',...($('roof').checked&&s.id==='r01_camp'?['roof']:[])];
try{const images=await Promise.all(parts.map(p=>load(`assets/backgrounds/${s.id}__${p}.png`)));if(rev!==revision)return;canvas.width=s.size[0];canvas.height=s.size[1];ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,...s.size);images.forEach(im=>ctx.drawImage(im,0,0));const zoom=$('zoom').value==='fit'?Math.min(1,Math.max(.25,($('board').clientWidth-12)/s.size[0])):+$('zoom').value;canvas.style.width=s.size[0]*zoom+'px';canvas.style.height=s.size[1]*zoom+'px';
if($('mask').checked){for(let y=0;y<s.cells[1];y++)for(let x=0;x<s.cells[0];x++){ctx.fillStyle=canWalk(s,x,y)?'rgba(53,196,113,.22)':'rgba(211,73,65,.24)';ctx.fillRect(x*26,y*26,26,26);}}
if($('grid').checked){ctx.strokeStyle='rgba(218,225,217,.35)';ctx.lineWidth=1;ctx.beginPath();for(let x=0;x<=s.size[0];x+=26){ctx.moveTo(x+.5,0);ctx.lineTo(x+.5,s.size[1]);}for(let y=0;y<=s.size[1];y+=26){ctx.moveTo(0,y+.5);ctx.lineTo(s.size[0],y+.5);}ctx.stroke();}
if($('doors').checked){for(const [items,color]of [[s.exits,'#e7af52'],[s.reserved,'#9de0b4']])for(const e of items){const[x,y]=e.cell;ctx.strokeStyle=color;ctx.lineWidth=2;ctx.strokeRect(x*26+3,y*26+3,20,20);}}
$('info').textContent=`${s.name_zh} · ${s.size.join(' × ')} 像素 · ${s.cells.join(' × ')} 格`;$('status').textContent=`${DATA.assets.length}张生产PNG · ${DATA.validation.checks_passed}项静态检查通过 · 待游戏装配`;window.__artReady=true;window.__artRender={scene:s.id,mode:plan?'plan':'scene',parts,zoom,width:canvas.width,height:canvas.height};
}catch(e){$('status').textContent=e.message;window.__artError=e.message;}}
for(const id of ['scene','mode','zoom','props','roof','grid','mask','doors'])$(id).addEventListener('change',draw);window.addEventListener('resize',draw);
canvas.addEventListener('mousemove',e=>{const r=canvas.getBoundingClientRect(),x=Math.floor((e.clientX-r.left)*canvas.width/r.width/26),y=Math.floor((e.clientY-r.top)*canvas.height/r.height/26),s=DATA.scenes.find(s=>s.id===$('scene').value);$('coords').textContent=`格 ${x},${y} · ${canWalk(s,x,y)?'可走':'阻挡'}`;});
const labels={r01_worker_shed:'雇工棚',r01_winch_shed:'绞盘修理棚',r01_canal_entry:'旧渠入口',r01_coffin_coat:'空棺与旧外套',r01_winch_socket:'拆轴后的空轴座',r01_sluice_wheel:'旁通闸轮',r01_maintenance_ladder:'检修梯',r01_shelter_bedroll:'侧间铺盖与木夹板',r01_water_jug:'水壶'};
for(const a of DATA.assets.filter(a=>a.role==='independent_environment_sprite')){const card=document.createElement('div');card.className='card';const box=document.createElement('div');box.className='sprite';const im=document.createElement('img');im.src=a.path;im.alt=labels[a.id];box.append(im);card.append(box);const text=document.createElement('small');text.textContent=`${labels[a.id]} · ${a.size.join('×')} · 原点(${a.origin.join(',')})`;card.append(text);$('gallery').append(card);}draw();
</script></html>'''
if __name__=='__main__':main()
