"""Package the reviewed N1 export without changing the game or source designs."""
from pathlib import Path
from PIL import Image
import hashlib
import importlib.util
import json
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013'
SKILL=ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8'))
def write(path,value):path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    # Revalidate current PNGs, rather than trusting an earlier pass.
    subprocess.run([sys.executable,str(ROOT/'tools/Validate-Hd2dN1.py')],check=True)
    upstream=subprocess.run([sys.executable,str(SKILL/'scripts/asset_validator.py'),str(P)],check=True,capture_output=True,text=True,encoding='utf-8')
    (P/'notes/skill-validation.txt').write_text(upstream.stdout,encoding='utf-8')
    manifest=read(P/'manifest.json')
    manifest['status']='static_export_verified_runtime_unverified'
    manifest['validation']='validation.json'
    manifest['visual_review']={
        'date':'2026-10-13','reviewer':'assistant','scope':'Exported scene and facade previews, source sprite sheets and cutouts',
        'findings':['128-color reference palette replaces the purple-grey midtones of the first quantization pass.',
                    'Stone wall blocks preserve their scale rather than stretching over a whole wall.',
                    'Underpass water is restricted to a dark narrow outer channel.',
                    'Floor alpha matches existing room geometry. Bell, cut rope, and two bedrolls remain independent sprites.'],
        'limitations':['Visual review is not user approval or in-game verification.','Facade placement remains independent from the present yard scene.']}
    write(P/'manifest.json',manifest)

    style=ROOT/'design/12_美术参考/城市概念/DEN-概念-v1.png'
    source_names=['yard','bellhouse','underpass','exterior','props','props','water']
    versions=['v1','v1','v1','v1','v1','v2','v1']
    records=[]
    for name,version in zip(source_names,versions):
        basename=f'n1-{name}-{version}'
        raw=P/'raw'/(basename+'.png');prompt=P/'notes'/('prompt-'+basename+'.txt')
        inputs=[]
        if name in ['yard','bellhouse','underpass']:
            inputs.append(P/'guides'/f'r_eao_n1_{name}_geometry.png')
        if name!='water' and not (name=='props' and version=='v2'):inputs.append(style)
        if name=='props' and version=='v2':inputs.append(P/'raw/n1-props-v1.png')
        records.append(dict(id=basename,method='built-in image_gen',
          prompt=prompt.relative_to(P).as_posix(),prompt_sha256=sha(prompt),
          inputs=[dict(path=i.relative_to(ROOT).as_posix(),sha256=sha(i)) for i in inputs],
          output=raw.relative_to(P).as_posix(),output_sha256=sha(raw),original_size=list(Image.open(raw).size),
          role='generation_master_not_direct_import',
          selection='superseded_by_props_v2' if name=='props' and version=='v1' else 'production_source',
          postprocess='See manifest.json crop_operations; nearest-neighbor resize, alpha threshold, skill palette quantization and native geometry assembly.'))
    write(P/'generation-log.json',dict(schema=1,skill_url='https://github.com/424431185/pixel-asset-master-skills',
      skill_commit=manifest['skill_commit'],generation_count=len(records),records=records,
      reference_policy='Existing Mod art and code-native masks only; no original commercial atlas copied into this package.'))

    # Skill packer: six props in 208px cells, reflowed into the locked 3x2;
    # never a huge atlas
    # combining 1040px room layers, and never an implied animation.
    spec=importlib.util.spec_from_file_location('pam_sheet',SKILL/'scripts/sprite_sheet.py')
    sheet_module=importlib.util.module_from_spec(spec);spec.loader.exec_module(sheet_module)
    staged=P/'sheets/frames';staged.mkdir(exist_ok=True,parents=True)
    props=[a for a in manifest['assets'] if a.get('role')=='independent_sprite' and a['id']!='n1_bellhouse_exterior']
    files=[];origins={}
    for i,a in enumerate(props):
        im=Image.open(P/a['path']).convert('RGBA');canvas=Image.new('RGBA',(208,208))
        offset=((208-im.width)//2,(208-im.height)//2)
        canvas.alpha_composite(im,offset);dest=staged/(a['id']+'.png');canvas.save(dest);files.append(dest)
        origins[a['id']]=dict(source=a['path'],source_origin=a['sprite_origin'],
            sheet_origin=[(i%3)*208+offset[0]+a['sprite_origin'][0],(i//3)*208+offset[1]+a['sprite_origin'][1]],
            cell_origin=[offset[0]+a['sprite_origin'][0],offset[1]+a['sprite_origin'][1]],cell_rect=[(i%3)*208,(i//3)*208,208,208])
    sheets={'sheets':[]}
    sheet_module._create_sheet(P/'sheets/n1_props.png',files,208,208,sheets,'props','static_independent_objects')
    strip=Image.open(P/'sheets/n1_props.png').convert('RGBA')
    grid=Image.new('RGBA',(624,416))
    for i in range(6):grid.alpha_composite(strip.crop((i*208,0,(i+1)*208,208)),((i%3)*208,(i//3)*208))
    grid.save(P/'sheets/n1_props.png')
    sheets['sheets'][0].update(columns=3,rows=2)
    sheets.update(note='Six independent static objects. Do not play this sheet as animation.',objects=origins)
    write(P/'sheets/manifest.json',sheets)
    packed=Image.open(P/'sheets/n1_props.png').convert('RGBA')
    assert packed.size==(624,416)
    for a,file in zip(props,files):
        x,y,w,h=origins[a['id']]['cell_rect']
        assert packed.crop((x,y,x+w,y+h)).tobytes()==Image.open(file).convert('RGBA').tobytes()

    progress_path=P/'progress.json';progress=read(progress_path) if progress_path.exists() else dict(schema=1,requests={})
    for room in manifest['rooms']:
        rid=room['id'];views=['plan','exterior_or_site' if rid.endswith('yard') else 'interior_or_working_space']
        related={a['path']:a['sha256'] for a in manifest['assets'] if a.get('room')==rid or a.get('role')=='independent_sprite'}
        for view in views:
            part='plan' if view=='plan' else 'environment';path=f'assets/backgrounds/{rid}__{part}.png'
            progress['requests'][rid+'__'+view]=dict(batch='N1',status='static_export_verified',path=path,outputs=related,
               source_sha256={'src/EmbersAndOaths/NightRooms.cs':manifest['source_code_sha256']},runtime_verified=False)
    progress.update(date='2026-10-13',counting_note='6 fulfilled view slots; 26 PNG files including supporting sprites and layers. These are different counts.')
    write(progress_path,progress)
    subprocess.run([sys.executable,str(ROOT/'tools/Build-Hd2dInventory.py')],check=True)
    proposal=read(P/'proposal.json')
    proposal.update(status='production_in_progress_n1_static_export_verified',generation_started=True,
       finished_new_images=26,generated_master_files=7,production_pngs=26,fulfilled_view_slots=6,remaining_view_slots=739)
    proposal['completed']=['skill下载与版本固定','全范围745视图需求清单','N1逐图生成与提示词留存','N1三场景分层与独立建筑/道具导出','128色量化及244项静态检查','可切换图层的离线预览与导入包']
    write(P/'proposal.json',proposal)
    # Recompute current whole-project counts; later scene batches must survive
    # rebuilding this original N1 package.
    from Hd2dProgress import reconcile
    reconcile()
    (P/'IMPORT.txt').write_text('''紫色晶石 / N1 HD-2D 导入包 v1

范围：旧渡口岸院、钟屋、暗渠。26张生产PNG，另附六物件精灵表。
本N1包覆盖6项视图。全项目进度由artwork-state.json单独统计。
validation.json是本素材导出时的静态证据；当前Mod部署与游戏测试证据另见项目artifacts/。

1. 用浏览器直接打开 preview.html，无需服务器；同目录相对路径必须保留。
2. assets/backgrounds/*__plan.png 是1040×780的平面材质图；guides/*_plan.png 为带点位的技术图。
3. 分层使用顺序：backing → floor → structure → 按脚底Y排序的原生人物与独立物件 → foreground。
   房间层原点(0,0)，比例1:1，最近邻采样，关闭平滑和mipmap。不可自动裁掉画布透明边。
4. objects放置公式：左上角 = (cellX*26+13,cellY*26+13) - sprite_origin。
   原点、尺寸、SHA256见 manifest.json。图集sheet_origin包含图集偏移；cell_origin用于拆分后的208方格。
   图集包含六个独立静态物件，不是动画帧。逐物件原PNG无需使用图集就能导入。
5. 钟、断绳与铺盖仅在preview中按现有锚点合成；它们未烘焙进房间底图。
   两张铺盖与小鞋在一个物件PNG中。其他水壶、门拱、灯尚无新增交互/库存。
6. 原生可走格、门点、落点、灯点及剧情物件锚点见 native_layouts.json。
   mask白=原生可走地面，黑=阻挡。不要从美术透明轮廓推算人物或门的碰撞。
   原生门实例、保存和转场必须保留，D标记仅为技术覆盖层。
7. n1_bellhouse_exterior.png 是312×260独立外观，不能当室内比例图或直接烘焙到岸院。
   原点为门槛参考点；启用前需在引擎中校准遮挡、入口和实际碰撞。
8. 静态图片没有烘焙发光。native_layouts已登记原生灯点，由现有动态光源渲染。
9. raw/是生图原稿，含几何近似和半透明边；应导入assets/中的校正版本。
   完整提示词/输入输出哈希在notes/及generation-log.json，裁切步骤在manifest.json。
10. source_snapshot/NightRooms.cs仅为该导出对应的Mod几何源码快照，不替换当前项目源码。
    validation.json仅证明静态文件/像素/通路检查，不证明游戏运行、对白或用户美术认可。

重建（在项目根目录，用可用Python/Pillow）：
  python tools/Prepare-Hd2dProduction.py
  python tools/Export-Hd2dN1.py
  python tools/Package-Hd2dN1.py
生图原稿须保留；重建命令复用raw/，不会重新调用图像生成。
''',encoding='utf-8')
    (P/'source_snapshot').mkdir(exist_ok=True)
    (P/'source_snapshot/NightRooms.cs').write_bytes((ROOT/'src/EmbersAndOaths/NightRooms.cs').read_bytes())
    exports=P/'exports';exports.mkdir(exist_ok=True)
    archive=exports/'HD2D-N1-v1.zip'
    files=[f for f in P.rglob('*') if f.is_file() and exports not in f.parents and 'frames' not in f.parts and 'batches' not in f.relative_to(P).parts and f.name!='index.html']
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for f in sorted(files):z.write(f,f.relative_to(P).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist())==len(files)
        for f in files:assert hashlib.sha256(z.read(f.relative_to(P).as_posix())).hexdigest()==sha(f)
    report=dict(archive=archive.relative_to(P).as_posix(),sha256=sha(archive),bytes=archive.stat().st_size,
       file_count=len(files),zip_roundtrip_verified=True,atlas_pixels_verified=True,runtime_verified=False)
    write(exports/'package-report.json',report)
    print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':main()
