"""Normalize48new sprites/reuse11 core sprites and46 material patches; not scene delivery."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,shutil,importlib.util,contextlib,io
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];BASE=ROOT/'src/Art/hd2d_26x26_20261013';P=BASE/'batches/BRY-outskirts-v1';CORE=BASE/'batches/BRY-core-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    b=read('brief.json');specs={s['id']:s for s in b['sprites']};log=read('generation-log.json');assert log['generation_count']==7 and all(r.get('output_sha256') for r in log['records']);assert all(sha(ROOT/n)==h for n,h in b['source_sha256'].items());records={r['id']:r for r in log['records']};rgb=[tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/bry_outskirts_128.json')['colors']]
    @lru_cache(None)
    def nearest(c):return min(rgb,key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    recipes=[
      ('bryo-architecture-v1',list(specs)[:8],[(0,0,426,512),(427,0,764,512),(765,0,1151,512),(1152,0,1536,512),(0,512,421,1024),(423,512,762,1024),(764,512,1133,1024),(1135,512,1536,1024)]),
      ('bryo-props-a-v1',list(specs)[8:16],[(0,0,400,512),(410,0,756,512),(765,0,1160,512),(1180,0,1536,512),(0,512,420,1024),(425,512,760,1024),(770,512,1150,1024),(1170,512,1536,1024)]),
      ('bryo-props-b-v1',list(specs)[16:24],[(0,0,415,512),(420,0,815,512),(820,0,1250,512),(1260,0,1536,512),(0,512,390,1024),(400,512,790,1024),(800,512,1170,1024),(1180,512,1536,1024)]),
      ('bryo-props-c-v1',list(specs)[24:32],[(0,0,390,512),(395,0,807,512),(815,0,1175,512),(1185,0,1536,512),(0,512,380,1024),(385,512,786,1024),(790,512,1200,1024),(1205,512,1536,1024)]),
      ('bryo-props-d-v1',list(specs)[32:40],[(0,0,400,512),(410,0,795,512),(810,0,1170,512),(1180,0,1536,512),(0,512,370,1024),(375,512,754,1024),(760,512,1170,1024),(1180,512,1536,1024)]),
      ('bryo-props-e-v1',list(specs)[40:48],[(0,0,390,512),(395,0,770,512),(775,0,1080,512),(1085,0,1536,512),(0,512,400,1024),(405,512,770,1024),(775,512,1140,1024),(1145,512,1536,1024)])]
    assets=[];ops=[]
    for master,ids,boxes in recipes:
        r=records[master];assert sha(P/r['output'])==r['output_sha256'] and sha(P/r['prompt'])==r['prompt_sha256'] and sha(P/r.get('spec_lock_path','spec_lock.md'))==r['spec_lock_sha256'];raw=Image.open(P/r['output']).convert('RGBA')
        for ident,box in zip(ids,boxes):
            s=specs[ident];q=raw.crop(box);alpha=q.getchannel('A').point(lambda a:255 if a>=128 else 0);q.putalpha(alpha);trim=alpha.getbbox();assert trim,ident;q=q.crop(trim);w,h=s['size'];ox,oy=s['origin'];factor=min((w-4)/q.width,(oy-2)/q.height);size=[max(1,round(q.width*factor)),max(1,round(q.height*factor))];offset=[(w-size[0])//2,oy-size[1]];fitted=q.resize(size,Image.Resampling.NEAREST);comp=size[1]-fitted.getchannel('A').getbbox()[3];offset[1]+=comp;out=Image.new('RGBA',(w,h));out.alpha_composite(fitted,offset);out.putdata([(*nearest(c[:3]),255) if c[3] else (0,0,0,0) for c in out.get_flattened_data()]);rel=f'assets/items/{ident}.png';out.save(P/rel)
            assets.append(dict(id=ident,path=rel,size=s['size'],origin=s['origin'],foot_anchor=s['origin'],role='independent_environment_sprite',architecture=s['architecture'],roof_variants_pending=s['architecture'],palette='BRY-CORE-128',sha256=sha(P/rel),collision='Proposed geometry separate; PNG alpha never collision',runtime_verified=False));ops.append(dict(id=ident,source=r['output'],box=list(box),trim_bbox=list(trim),target_canvas=s['size'],fitted_size=size,offset=offset,alpha_threshold=128,foot_blank_row_compensation=comp,resample='nearest',foot_baseline=oy,quantizer='Nearest RGB squared distance, first palette entry on tie',source_slot_note='Actualrawspacing reviewed; isolated crop keeps complete silhouette, normalized production canvas/origin exact'))
    reuse_sources=[]
    core_manifest=json.loads((CORE/'manifest.json').read_text(encoding='utf-8'))
    for a in b['reused_sprites']:
        assert sha(ROOT/a['source_path'])==a['source_asset_sha256'];shutil.copyfile(ROOT/a['source_path'],P/a['path']);assets.append(dict(a));reuse_sources.append(dict(id=a['id'],source=a['source_path'],sha256=a['sha256'],method='Exact owncore productionPNG copy, not raw/regeneration',runtime_verified=False))
    for a in b['reused_sprites']:
        if not a.get('architecture'):continue
        for part in [v for v in core_manifest['assets'] if v.get('source_sprite')==a['id']]:
            assert sha(CORE/part['path'])==part['sha256'];shutil.copyfile(CORE/part['path'],P/part['path']);assets.append(dict(part,source_batch='BRY-core-v1',source_path=(CORE/part['path']).relative_to(ROOT).as_posix()));reuse_sources.append(dict(id=part['id'],source=(CORE/part['path']).relative_to(ROOT).as_posix(),sha256=part['sha256'],method='Exact verified coreawning roof/body copy',runtime_verified=False))
    core=json.loads((CORE/'manifest.json').read_text(encoding='utf-8'));mat_ids={a['id'] for a in json.loads((CORE/'materials-manifest.json').read_text(encoding='utf-8'))['assets']};materials=[]
    for a in core['assets']:
        if a['id'] not in mat_ids and a['role'] not in ['unlit_vertical_wall_not_floor','unlit_window_patch_not_door']:continue
        assert sha(CORE/a['path'])==a['sha256'];shutil.copyfile(CORE/a['path'],P/a['path']);materials.append(dict(a,source_batch='BRY-core-v1',source_path=(CORE/a['path']).relative_to(ROOT).as_posix()));reuse_sources.append(dict(id=a['id'],source=(CORE/a['path']).relative_to(ROOT).as_posix(),sha256=a['sha256'],method='Exact owncore surface/window/wall copy',runtime_verified=False))
    write('sprite-manifest.json',dict(batch=b['batch'],status='exported_pending_quality',assets=assets,crop_operations=ops,source_sha256=b['source_sha256'],view_slots_fulfilled=0,runtime_verified=False));write('materials-manifest.json',dict(batch=b['batch'],status='exported_pending_quality',assets=materials,source_sha256=b['source_sha256'],view_slots_fulfilled=0,runtime_verified=False));log['reuse_sources']=reuse_sources;write('generation-log.json',log)
    spec=importlib.util.spec_from_file_location('bryo_sprite_validator',ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py');pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/sprites-skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');assert passed,buf.getvalue()
    for a in assets+materials:
        q=Image.open(P/a['path']);assert q.mode=='RGBA' and list(q.size)==a['size'];assert all(c[3] in [0,255] and (not c[3] or c[:3] in rgb) for c in q.get_flattened_data()),a['id']
        if a.get('foot_anchor'):assert q.getchannel('A').getbbox()[3]==a['origin'][1],a['id']
    for filename in ['sprite-manifest.json','materials-manifest.json']:
        m=read(filename);m['status']='partial_assets_verified_scene_assembly_pending';write(filename,m)
    write('sprites-validation.json',dict(passed=True,new_independent_sprites=48,reused_independent_sprites=len(b['reused_sprites']),material_patches=len(materials),production_pngs=len(assets)+len(materials),requested_skill_validator=True,view_slots_fulfilled=0,scene_assembly_pending=True,runtime_verified=False))
    for a in assets+materials:(P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n{a["size"]} RGBA静态图，原点{a["origin"]}；BRY-CORE-128、二值alpha、nearest采样。{a["role"]}；SHA {a["sha256"]}。\n\n场景合成/屋顶和原生装配仍待验收，不计完成视图。裁切与复用来源见相应manifest。\n',encoding='utf-8')
    print(json.dumps(read('sprites-validation.json'),ensure_ascii=False))
if __name__=='__main__':main()
