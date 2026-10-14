"""R03 art handoff/preview/ZIP, gated on current candidate quality evidence."""
from pathlib import Path
import argparse,json,hashlib,zipfile,importlib.util
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R03-maen-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main(preview_only=False):
    m=read(P/'manifest.json');v=read(P/'validation.json');assert v['passed'] and not v['errors'] and v['asset_manifest_sha256']==sha(P/'manifest.json')
    for a in m['assets']:assert sha(P/a['path'])==a['sha256'],a['path']
    for path,h in m['source_sha256'].items():assert sha(ROOT/path)==h,path
    for a in m['assets']:
        im=Image.open(P/a['path']).convert('RGBA');colors={px[:3] for px in im.get_flattened_data() if px[3]}
        (P/f"notes/{a['id']}.md").write_text(f"# {a['id']}\n\n- Category: {a['path'].split('/')[1]}\n- Size: {im.width}x{im.height}\n- Origin: {a['origin']}\n- Colors used: {len(colors)} from MAE-R03-128\n- Animation: none\n- Design notes: {a['role']}\n- Sampling: nearest, no mipmaps, keep full canvas.\n- Variants: architectural full/body/roof use identical canvas and origin.\n- Collision: proposed cell geometry only, never alpha.\n- Runtime: native integration pending; NPC work belongs to the other model.\n",encoding='utf-8')
    s=importlib.util.spec_from_file_location('r03_preview_style',ROOT/'tools/Package-Hd2dR02.py');base=importlib.util.module_from_spec(s);s.loader.exec_module(base);css=base.HTML.split('<style>',1)[1].split('</style>',1)[0]
    data=dict(scenes=m['scenes'],assets=m['assets'],region=m['region'],validation=v)
    (P/'preview.html').write_text(HTML.replace('__CSS__',css).replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/')),encoding='utf-8')
    rows='\n'.join(f"| `{s['id']}` {s['name_zh']} | {'×'.join(map(str,s['size']))} | {'×'.join(map(str,s['cells']))} |" for s in m['scenes'])
    text=f'''# 曼恩边地 · R03 场景美术 v1

{len(m['assets'])}张生产PNG、18个场景、22个独立建筑/物件、36块26×26平面材料瓦片，完成27项原清单视图。{v['checks_passed']}项静态检查通过。
全十二节点及六个工作室内均已制作；这批为可导入美术，原生房间、世界坐标、门、碰撞、保存生命周期与天气尚待装配测试。
人物区域与文字保持空白，NPC图像、对白和事件由另一模型接入。

打开preview.html可离线切换空间/平面、屋顶、独立物件、格网、通行掩码和门点。护理椅示意默认关闭，只在民粮公议室有一个位置；页面切换不提交剧情结果。
生产导入用assets/；raw/保留十张原稿，guides/保留生成前输入和制作格图，sheets/可按配套manifest提取精灵。路径均相对本目录。

| 场景 | 像素尺寸 | 格数 |
|---|---|---|
{rows}

## 导入接口

场景1像素＝1房间像素；nearest采样，关闭平滑/mipmap，原点(0,0)，保留透明画布，禁止自动裁边。
draw order：backing → floor → structure → 按脚底Y排序的独立建筑body/环境物件与原生人物 → foreground → 可关闭roof。
物件左上角=(cellX×26+13,cellY×26+13)−sprite.origin；独立精灵的底沿对准originY。body/roof使用同一画布和原点，不重叠并精确重组full。
props_preview、environment、working_space及overview为检查合成图；交互对象使用items/中的独立PNG，避免重复烘焙。
门点为制作候选格，实际门对象与点击/接近盒须按门板及脚底原点在引擎中校准；不能把图像透明度当碰撞。
layouts.json是显式候选通行和占位接口。静态连通检查不包含尚未接入的原生物件碰撞、敌人、犯罪或保存行为。
窗与侧墙在structure，低前沿在foreground；屋顶关闭用于观察前部，完整室内使用各自独立场景。

## 叙事空间约束

D04书库36×30：前廊、粮袋干区、侧封柜和低檐废库分区。病例/技术、姓名和停用请求使用三个不同柜；它们不是要求收齐三件文书的新任务。正式门不可用时，废库副件和装卸坡返程保留。
D05庭院44×34：开阔中央和四个尺寸不同的附室，灰烬/石板/木板/泥地分别绘制，窗位分别朝北/西/东。关闭中央可选演示且断供杆不可用时，外围仍能到印模间、试验壳房和维护返程。
断供杆与试验壳房入口格分别放置。装置为惰性旧壳与手动支架，不是魔法军队。封蜡、墨和回执图只提供比对桌面，具体认证和后果不写进图。
磨坊放两个铺位，属于有限容量的美术提案，尚未变成付费住宿服务。磨坊和民粮站各有中立技术副本柜，身份柜独立。
护理椅只在公议室conditional_props层，默认不画；室外旧候选已退役到previews/retired，不作为生产PNG或第二把椅子。
夜岗排水槽保持空的基底图；弃血、狼、护理和焚烧等事件按游戏状态添加。冷火盆没有火焰、烟或被烧毁的关键记录。
田块用普通土垄与作物图样，路上不烘焙大灌木；产量、租契、居民去留不由图片判定。霜雪仅为非通行边缘的美术表现，不代表原生天气已验证。

## 总览、比例与来源

区域图1664×1248：12节点/13双向边，功能拓扑原创，图中display_cells及art_anchor_pixels都不是原生世界格；R02/R04/R05接口待接入。
书库plan_overview为1040×1586，两张1:1平面图上下拼版；庭院working_overview为1300×598，印模间/试验壳房两张1:1室内横向拼版，均不是单间房。
36块瓦片为四类材料各九个平面变体，逐像素接缝匹配；不是边界自动瓦片。场景地面另用312像素母图纹理。
色板MAE-R03-128来自本项目既有AI概念图MAE-概念-v2；未复制商业原作图集，也不宣称官方学院已经开放。
generation-log.json保留每次生成之前的完整提示词、规格SHA、输入SHA及十张输出SHA；所有输入导图保留原样，制作阶段补的东西以layouts/manifest为准。
manifest.json记录实际裁切和输出SHA；调色沿用指定skill的RGB平方距离及首项平局规则，缓存颜色、预解析HEX以加速，未用近似距离。
validation.json绑定当前manifest SHA；浏览器记录（若存在）另在preview-validation.json。两者都不证明真实游戏运行。
项目内重建顺序：Prepare-Hd2dR03.py → Export-Hd2dR03.py → Validate-Hd2dR03.py → Package-Hd2dR03.py。
本轮未修改游戏包或玩家存档。
'''
    (P/'IMPORT.md').write_text(text,encoding='utf-8')
    if (P/'preview-validation.json').exists():
        pv=read(P/'preview-validation.json');assert pv['passed'] and pv['browser_verified'] and not pv['runtime_verified'];assert len(pv['render_cases'])==42
        pv.update(asset_manifest_sha256=sha(P/'manifest.json'),preview_html_sha256=sha(P/'preview.html'),proof_sha256={n:sha(P/'previews'/n) for n in pv['proofs']});(P/'preview-validation.json').write_text(json.dumps(pv,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if preview_only:print(json.dumps(dict(preview=str(P/'preview.html'),production_pngs=len(m['assets'])),ensure_ascii=False));return
    out=P/'exports/HD2D-R03-Maen-v1.zip';files=[f for f in P.rglob('*') if f.is_file() and 'exports' not in f.relative_to(P).parts]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):z.write(f,f.relative_to(P).as_posix())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for a in m['assets']:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256']
    report=dict(path=out.relative_to(ROOT).as_posix(),bytes=out.stat().st_size,sha256=sha(out),files=len(files),production_pngs=len(m['assets']),zip_crc_and_asset_sha_verified=True,runtime_verified=False);(P/'exports/package-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))

HTML=r'''<!doctype html><html lang="zh-CN"><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>曼恩边地 · HD-2D场景预览</title><style>__CSS__</style>
<header><h1>曼恩边地 · 迁藏与藏身</h1><p>HD-2D场景素材 · R03 / N6 / N10 / D04 / D05 / SQ03 / SQ06 / DT04 / DT10 / DT11</p><span id="status">正在载入分层素材…</span></header>
<main><aside><label for="scene">查看场景<select id="scene"></select></label><label for="mode">视图<select id="mode"><option value="scene">空间展示</option><option value="plan">平面地图</option></select></label><label for="zoom">缩放<select id="zoom"><option value="fit" selected>适合窗口</option><option value="0.5">50%</option><option value="1">100% 原尺寸</option><option value="2">200% 像素检查</option></select></label><label><input type="checkbox" id="props" checked>环境物件与建筑前部</label><label><input type="checkbox" id="roof" checked>建筑屋顶</label><label><input type="checkbox" id="conditional">护理椅结果示意</label><label><input type="checkbox" id="grid">26×26格网</label><label><input type="checkbox" id="mask">通行掩码</label><label><input type="checkbox" id="doors">出口与预留交互点</label><div id="info"></div><p>绿色为可走格，红色为阻挡；橙色为出口，浅绿色为预留交互格。护理椅示意只显示一个候选物件，不提交任务。</p><p>正式门之外保留废库通路；试验庭另有外围返程。人物、许可、火光和天气由引擎处理。</p><a href="IMPORT.md">导入说明</a> · <a href="manifest.json">资源清单</a> · <a href="../../index.html">场景素材库</a></aside>
<section><div class="legend"><span><i class="dot" style="background:#8e9192"></i>冷灰石</span><span><i class="dot" style="background:#463630"></i>旧木与灰烬</span><span id="coords">移动鼠标查看格坐标</span></div><div id="board"><canvas id="canvas"></canvas></div><h2 style="font-size:18px;margin-top:26px">独立建筑与环境物件 · 22件</h2><p>单帧透明PNG；五个建筑另有body/roof，三柜分别保留。</p><div id="gallery" class="gallery"></div></section></main><footer>可导入场景素材 · 原生房间与天气待装配测试 · 不烘焙人物、姓名或任务结果</footer>
<script>
const DATA=__DATA__,$=id=>document.getElementById(id),canvas=$('canvas'),ctx=canvas.getContext('2d'),cache=new Map(),assets=new Set(DATA.assets.map(a=>a.id));let revision=0;
const specials=[{id:'r03_region',name_zh:'曼恩边地 · 区域连接图',size:[1664,1248],scene:'r03_region__plan',plan:'r03_region__plan',note:'12节点 / 13双向边 · 功能拓扑，非原生世界格'},{id:'r03_library_overview',name_zh:'迁藏书库 · 室内与平面拼版',size:[936,780],planSize:[1040,1586],scene:'r03_library_store__environment',plan:'r03_library__plan_overview',note:'室内1:1；外围/库房平面上下1:1拼版，非单间房'},{id:'r03_court_overview',name_zh:'弃置庭院 · 附室与平面',size:[1300,598],planSize:[1144,884],scene:'r03_court__working_overview',plan:'r03_court__plan',note:'两附室横向1:1拼版；庭院平面44×34，非合并原生房间'}];
for(const s of [...DATA.scenes,...specials]){const o=document.createElement('option');o.value=s.id;o.textContent=s.name_zh;$('scene').append(o);}$('scene').value='r03_library_store';
function load(id){const path=`assets/backgrounds/${id}.png`;if(!cache.has(path))cache.set(path,new Promise((resolve,reject)=>{const im=new Image();im.onload=()=>resolve(im);im.onerror=()=>reject(new Error('无法载入 '+path));im.src=path;}));return cache.get(path);}
const contains=(rs,x,y)=>(rs||[]).some(([a,b,c,d])=>x>=a&&x<=c&&y>=b&&y<=d);
function canWalk(s,x,y){return contains(s.walkable_rectangles,x,y)&&!contains(s.blocked_rectangles,x,y);}
async function draw(){const rev=++revision,s=DATA.scenes.find(s=>s.id===$('scene').value)||specials.find(s=>s.id===$('scene').value),special=!s.cells,plan=$('mode').value==='plan';for(const id of ['grid','mask','doors'])$(id).disabled=special;$('props').disabled=special||plan;$('roof').disabled=special||plan||!assets.has(s.id+'__roof');$('conditional').disabled=special||plan||!assets.has(s.id+'__conditional_props');
const roof=$('roof').checked&&!$('roof').disabled,conditional=$('conditional').checked&&!$('conditional').disabled;
const parts=special?[plan?s.plan:s.scene]:plan?[s.id+'__plan']:['backing','floor','structure',...($('props').checked?['props_preview']:[]),...(conditional?['conditional_props']:[]),'foreground',...(roof?['roof']:[])].map(p=>s.id+'__'+p);
try{const images=await Promise.all(parts.map(load));if(rev!==revision)return;const size=special&&plan&&s.planSize?s.planSize:s.size;canvas.width=size[0];canvas.height=size[1];ctx.imageSmoothingEnabled=false;ctx.clearRect(0,0,...size);images.forEach(im=>ctx.drawImage(im,0,0));const zoom=$('zoom').value==='fit'?Math.min(1,Math.max(.2,($('board').clientWidth-12)/size[0]),Math.max(350,innerHeight-220)/size[1]):+$('zoom').value;canvas.style.width=size[0]*zoom+'px';canvas.style.height=size[1]*zoom+'px';
if(!special&&$('mask').checked)for(let y=0;y<s.cells[1];y++)for(let x=0;x<s.cells[0];x++){ctx.fillStyle=canWalk(s,x,y)?'rgba(53,196,113,.22)':'rgba(211,73,65,.24)';ctx.fillRect(x*26,y*26,26,26);}
if(!special&&$('grid').checked){ctx.strokeStyle='rgba(218,225,217,.35)';ctx.lineWidth=1;ctx.beginPath();for(let x=0;x<=size[0];x+=26){ctx.moveTo(x+.5,0);ctx.lineTo(x+.5,size[1]);}for(let y=0;y<=size[1];y+=26){ctx.moveTo(0,y+.5);ctx.lineTo(size[0],y+.5);}ctx.stroke();}
if(!special&&$('doors').checked)for(const[items,color]of[[s.exits,'#e7af52'],[s.reserved,'#9de0b4']])for(const e of items){const[x,y]=e.cell;ctx.strokeStyle=color;ctx.lineWidth=2;ctx.strokeRect(x*26+3,y*26+3,20,20);}
if(s.id==='r03_region'){const labels={'R03-mill':'旧磨坊站','R03-ration':'民粮站','R03-library':'迁藏封存书库','R03-court':'弃置试验庭','R03-road':'风雪驿道','R03-depot':'受损集散点','R03-hide':'迁藏小路','R03-burnt':'烧毁旧屋','R03-field':'民田围栏','R03-watch':'夜岗林缘','R03-scribe':'抄写工棚','R03-border':'争议支路'};ctx.font='24px Microsoft YaHei';ctx.textAlign='center';for(const n of DATA.region.nodes){const[x,y]=DATA.region.art_anchor_pixels[n.id];ctx.fillStyle='#141a1e';ctx.fillRect(x-88,y+48,176,36);ctx.fillStyle='#ded0ad';ctx.fillText(labels[n.id]||n.name_zh,x,y+75,168);}}
$('info').textContent=`${s.name_zh} · ${size.join(' × ')} 像素`+(special?' · '+s.note:` · ${s.cells.join(' × ')} 格`)+(conditional?' · 护理椅结果示意':'');$('status').textContent=`${DATA.assets.length}张生产PNG · ${DATA.validation.checks_passed}项静态检查通过 · 原生房间待装配`;$('coords').textContent=special?'示意 / 拼版：不可当作房间坐标':'移动鼠标查看格坐标';}catch(e){$('status').textContent=e.message;}}
for(const id of ['scene','mode','zoom','props','roof','conditional','grid','mask','doors'])$(id).addEventListener('change',draw);window.addEventListener('resize',draw);canvas.addEventListener('mousemove',e=>{const s=DATA.scenes.find(s=>s.id===$('scene').value);if(!s)return;const r=canvas.getBoundingClientRect(),x=Math.floor((e.clientX-r.left)*canvas.width/r.width/26),y=Math.floor((e.clientY-r.top)*canvas.height/r.height/26);$('coords').textContent=`格 ${x},${y} · ${canWalk(s,x,y)?'可走':'阻挡'}`;});
const labels={r03_mill_house:'旧磨坊',r03_granary:'民粮站粮棚',r03_low_library:'低檐迁藏库',r03_scribe_shed:'抄写工棚',r03_burned_frame:'烧损门框',r03_watch_shelter:'夜岗与雨棚',r03_book_grain_stack:'包书粮袋',r03_technical_cabinet:'病例与技术柜',r03_name_cabinet:'姓名柜',r03_stop_cabinet:'停用请求柜',r03_copy_table:'副本对照桌',r03_seal_press:'手动印台',r03_empty_shell:'惰性试验壳',r03_feed_lever:'徒手断供杆',r03_grain_sacks:'有限粮袋',r03_water_barrel:'水桶',r03_bedroll:'单个铺位',r03_public_table:'公议桌',r03_care_chair:'护理者椅子',r03_cold_brazier:'未点燃火盆',r03_blank_waypost:'空白路标',r03_drain_trough:'空排水槽'};
for(const a of DATA.assets.filter(a=>a.role==='independent_environment_sprite')){const card=document.createElement('div');card.className='card';const box=document.createElement('div');box.className='sprite';const im=document.createElement('img');im.src=a.path;im.alt=labels[a.id];box.append(im);card.append(box);const t=document.createElement('small');t.textContent=`${labels[a.id]} · ${a.size.join('×')} · 原点(${a.origin.join(',')})`;card.append(t);$('gallery').append(card);}draw();
</script></html>'''
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');args=ap.parse_args();main(args.preview_only)
