"""Prepare reviewed v2 previews, then package only after browser QA."""
from pathlib import Path
import json,re,hashlib,zipfile,importlib.util,argparse,shutil
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def module(path):
    s=importlib.util.spec_from_file_location('cue_package_base',path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
LABELS={'r01_ash_threshold':'雇工棚门槛灰圈','r01_tool_stub':'轴座下的借据存根','r02_well_notice':'新漆井牌','r02_red_water_buckets':'两只红桶与运水绳结','r02_rope_shoe_stall':'回访：半编小绳鞋摊','r02_bridge_note':'拒绝强运回访：桥牌钉纸'}
def preview(folder):
    m=read(folder/'manifest.json');v=read(folder/'validation.json');assert v['passed'] and sha(folder/'manifest.json')==v['asset_manifest_sha256'];isr01=m['batch'].startswith('R01');old=folder.parent/m['supersedes']['batch']
    base=module(ROOT/'tools/Package-Hd2dR02.py');html=base.HTML
    if isr01:
        r01=module(ROOT/'tools/Package-Hd2dR01.py');labels=re.search(r'const labels=(.*?);',r01.HTML).group(1)
        html=re.sub(r'const labels=.*?;',lambda _:f'const labels={labels};',html)
        html=re.sub(r'const specials=.*?;',"const specials=[{id:'r01_canal_overview',name_zh:'旧渠双层拼版',size:[1352,1638],plan:'r01_canal__plan_overview',scene:'r01_canal__environment_overview',note:'两层1:1比例拼版，不能作为一间原生房间'}];",html)
        html=html.replace("$('scene').value='r02_tax_main'","$('scene').value='r01_camp'")
        html=html.replace('丹布里西路与渡口','灰堤工营与旧渠').replace('R02 / N5 / N9 / D03 / SQ04 / SQ05 / DT13','R01 / N2 / D02')
        html=html.replace('旧渡口复用N1，区域图和多室拼版另标比例','旧渠双层拼版保持1:1，不能作为单间房')
    html=html.replace('HD-2D场景素材 ·','HD-2D场景素材 v2 ·')
    html=html.replace('<label><input type="checkbox" id="grid">','<label><input type="checkbox" id="return_cues">对应回访道具（默认关闭）</label><label><input type="checkbox" id="grid">')
    html=html.replace("const repair=$('repaired')", "$('return_cues').disabled=special||plan||!$('props').checked||!assets.has(s.id+'__conditional_cues');\nconst repair=$('repaired')")
    oldparts="['backing',repair?'repaired_floor':'floor',repair?'repaired_structure':'structure',...($('props').checked?['props_preview']:[]),repair?'repaired_foreground':'foreground',...(hasRoof?['roof']:[])].map(p=>s.id+'__'+p)"
    newparts="['backing',repair?'repaired_floor':'floor',repair?'repaired_structure':'structure',...($('props').checked?['story_underlay','props_preview','story_details']:[]),...($('return_cues').checked&&!$('return_cues').disabled?['conditional_cues']:[]),repair?'repaired_foreground':'foreground',...(hasRoof?['roof']:[])].map(p=>s.id+'__'+p).filter(p=>assets.has(p))"
    assert oldparts in html;html=html.replace(oldparts,newparts).replace("'repaired','grid','mask','doors'","'repaired','return_cues','grid','mask','doors'")
    html=html.replace("for(const a of DATA.assets.filter",'Object.assign(labels,'+json.dumps(LABELS,ensure_ascii=False)+');\nfor(const a of DATA.assets.filter')
    html=html.replace('独立建筑与环境物件 · 18件',f'独立建筑与环境物件 · {v["independent_sprites"]}件').replace('五个建筑另含body与roof','建筑另含body与roof')
    html=html.replace('公共桌、取样水口与返程均按空间约束绘制。人物、授权及任务结果由引擎处理。','观察物件独立绘制。回访绳鞋与桥牌钉纸默认关闭；具体条件及文字由游戏引擎处理。')
    data=dict(scenes=m['scenes'],assets=m['assets'],validation=v,region=m.get('region',{}));html=html.replace('__DATA__',json.dumps(data,ensure_ascii=False).replace('</','<\\/'))
    (folder/'preview.html').write_text(html,encoding='utf-8');shutil.copy2(old/'IMPORT.md',folder/'BASE_IMPORT-v1.md')
    notes=['# 场景补画与导入说明 v2','',f'本批包含{len(m["assets"])}张生产PNG，对应原清单{len(m["inventory_requests"])}项视图。{v["checks_passed"]}项静态检查通过；原生游戏装配和运行未验收。','',f'基于{m["supersedes"]["batch"]}补画观察物件。旧版本完整保留；地面、阻挡、门口、屋顶及浅滩/回程提案逐字节保持。基础空间导入详见BASE_IMPORT-v1.md。','', '打开preview.html切换平面地图、建筑外观、屋顶下空间和有条件回访道具。所有生产路径相对本目录，导入assets/，不要导入raw/。关闭平滑和mipmap，比例1像素=1房间像素。','', '绘制顺序：backing → floor → structure → story_underlay → 按脚底Y排序的原独立物件/body与原生人物 → story_details → 对应条件的conditional_cues → foreground → roof。预览合成图仅供检查，不能和独立物件重复绘制。','', 'scene_cues在manifest.json及layouts.json中登记。pixel_anchor=(cell*26+13)+pixel_offset；PNG左上角=pixel_anchor-origin。灰圈为地面观察贴花，借据位于轴座下；这两个锚点是贴图基准，不是角色脚底。所有新增PNG均不提供碰撞，alpha不能作为碰撞。','', 'scene_cues不是已实现游戏事件，condition为接入契约。N18绳鞋摊只在对应回访显示；SQ04字条须拒绝强运并进入对应回访，不抹除transport_harm。两者默认隐藏、分别切换，不代表家属同意或伤害结清。','', '井牌留空供引擎绘字，红桶为准确两只且不作库存/饮用性结论；借据小印仅作观察线索，不认证采购链。灰圈没有亡者、符文或魔法效果。人物与对白由另一模型负责。','', '共享新增母图保存在cue-source/raw/，六格拆图和区域128色量化见cue-source/manifest.json；其生成锁、完整提示词与SHA另存cue-source/。继承母图的原锁不改，generation-log.json区分records与external_generation_records。两批共享同一新增母图，全项目按输出SHA去重。','', '本次更新复核N2/N5/N9/N18/SQ04；N9变化为文字与知识交叉条件，现有公共桌、河窗、分柜仍适用，没有新增栅格物件。源文件从未被本工具修改。','', '复现：Export-Hd2dSceneCueSync.py → Validate-Hd2dSceneCueSync.py → Package-Hd2dSceneCueSync.py --preview-only → 浏览器检查 → Package-Hd2dSceneCueSync.py。复制的旧原稿、基础提示词与v1包不覆盖。','']
    (folder/'IMPORT.md').write_text('\n'.join(notes),encoding='utf-8')
    for a in m['assets']:
        if 'scene_cue_role' in a:
            (folder/'notes'/f'{a["id"]}.md').write_text(f'# {LABELS[a["id"]]}\n\n{a["size"]}，原点{a["origin"]}，静态二值alpha区域128色PNG。\n\n用途：{a["scene_cue_role"]}。实例/锚点/条件见manifest.json的scene_cues。不是物品认证、NPC或碰撞。\n\n生产SHA：{a["sha256"]}。新增共享母图SHA：{m["cue_contract"]["master_sha256"]}。\n',encoding='utf-8')
    print(json.dumps(dict(batch=m['batch'],preview=str(folder/'preview.html'),pngs=len(m['assets'])),ensure_ascii=False))
def package(folder):
    m=read(folder/'manifest.json');v=read(folder/'validation.json');pv=read(folder/'preview-validation.json')
    assert v['passed'] and pv['passed'] and pv['browser_verified'] and not pv['runtime_verified'];assert sha(folder/'manifest.json')==pv['asset_manifest_sha256']==v['asset_manifest_sha256'];assert sha(folder/'preview.html')==pv['preview_html_sha256']
    assert all(sha(folder/a['path'])==a['sha256'] for a in m['assets'])
    contract=folder/'cue-source';cm=read(contract/'manifest.json')
    assert all(sha(contract/a['path'])==a['sha256'] for a in cm['assets']),'All relative cue-source sprite paths must resolve'
    assert all(sha(folder/'previews'/n)==h for n,h in pv['proof_sha256'].items())
    name='HD2D-R01-Camp-Canal-v2.zip' if m['batch'].startswith('R01') else 'HD2D-R02-River-v2.zip';out=folder/'exports'/name
    files=[f for f in folder.rglob('*') if f.is_file() and 'exports' not in f.relative_to(folder).parts]
    with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(files):z.write(f,f.relative_to(folder).as_posix())
    with zipfile.ZipFile(out) as z:
        assert z.testzip() is None
        for a in m['assets']:assert hashlib.sha256(z.read(a['path'])).hexdigest()==a['sha256']
    report=dict(path=out.relative_to(ROOT).as_posix(),bytes=out.stat().st_size,sha256=sha(out),files=len(files),production_pngs=len(m['assets']),zip_crc_and_asset_sha_verified=True,runtime_verified=False);write(folder/'exports/package-report.json',report);print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--preview-only',action='store_true');ap.add_argument('--batch',choices=['R01-camp-canal-v2','R02-river-v2']);a=ap.parse_args()
    for b in ['R01-camp-canal-v2','R02-river-v2']:
        if a.batch and a.batch!=b:continue
        folder=P/'batches'/b
        if a.preview_only:preview(folder)
        else:package(folder)
