"""Normalize the reviewed R06 masters; keep incomplete batch outside delivered-view counts."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,importlib.util,contextlib,io
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R06-highland-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    b=read('brief.json');specs={s['id']:s for s in b['sprites']};assert all(sha(ROOT/n)==h for n,h in b['source_sha256'].items());log=read('generation-log.json');records={r['id']:r for r in log['records'] if r.get('output_sha256')}
    recipes=[
      ('r06-architecture-v1',list(specs)[:6],[(0,0,520,512),(520,0,1015,512),(1016,0,1536,512),(0,520,515,1024),(520,520,1015,1024),(1016,520,1536,1024)]),
      ('r06-props-a-v1',list(specs)[6:14],[(0,0,395,560),(410,0,725,560),(755,0,1140,560),(1160,0,1536,560),(0,595,580,1024),(585,595,885,1024),(890,595,1220,1024),(1230,595,1536,1024)]),
      ('r06-props-b-v1',list(specs)[14:17]+list(specs)[18:22],[(0,0,390,535),(400,0,755,535),(770,0,1110,535),(0,570,405,1024),(425,570,740,1024),(750,570,1120,1024),(1125,570,1536,1024)]),
      ('r06-medium-niche-v2',['r06_medium_niche'],[(0,0,1536,1024)]),
      ('r06-props-c-v1',list(specs)[22:25]+list(specs)[26:30],[(0,0,435,512),(440,0,805,512),(810,0,1155,512),(0,540,480,1024),(495,540,785,1024),(815,540,1170,1024),(1180,540,1536,1024)]),
      ('r06-coupling-capped-v2',['r06_aux_coupling_capped'],[(0,0,1536,1024)]),
      ('r06-props-d-v1',list(specs)[30:38],[(0,0,430,512),(450,0,775,512),(785,0,1160,512),(1180,0,1536,512),(0,520,370,1024),(395,520,780,1024),(795,520,1160,1024),(1180,520,1536,1024)])]
    pal=read('palettes/hig_r06_128.json');rgb=[tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in pal['colors']]
    @lru_cache(None)
    def nearest(c,violet=False):return min(rgb if violet else rgb[:120],key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    assets=[];ops=[]
    for master,ids,boxes in recipes:
        if master not in records:continue
        r=records[master];assert sha(P/r['output'])==r['output_sha256'] and sha(P/r['prompt'])==r['prompt_sha256'];assert sha(P/'spec_lock.md')==r['spec_lock_sha256'];raw=Image.open(P/r['output']).convert('RGBA')
        for ident,box in zip(ids,boxes):
            s=specs[ident];im=raw.crop(box);alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0);im.putalpha(alpha);component_quantization=None
            if ident=='r06_medium_niche':
                component_quantization=dict(source_face_polygon=[[670,510],[741,468],[861,510],[861,646],[809,675],[675,639]],iron_latch_exclusion=[727,542,778,621],hue_filter='B-R>=3,B-G>=9,R>=G',palette_subset='8locked HIG violet colors; rest uses full/regional palette',operation='Per-component nearest-palette quantization; no silhouette or source rewrite')
                cm=Image.new('L',im.size);cd=ImageDraw.Draw(cm);cd.polygon(component_quantization['source_face_polygon'],fill=255);cd.rectangle(component_quantization['iron_latch_exclusion'],fill=0)
                for yy in range(468,676):
                    for xx in range(670,862):
                        c=im.getpixel((xx,yy))
                        if cm.getpixel((xx,yy)) and c[3] and c[2]-c[0]>=3 and c[2]-c[1]>=9 and c[0]>=c[1]:im.putpixel((xx,yy),(*min(rgb[120:],key=lambda v:sum((v[j]-c[j])**2 for j in range(3))),c[3]))
            trim=alpha.getbbox();assert trim,ident;im=im.crop(trim);w,h=s['size'];ox,oy=s['origin'];scale=min((w-4)/im.width,(oy-2)/im.height);size=[max(1,round(im.width*scale)),max(1,round(im.height*scale))];size=[100,63] if ident in ['r06_aux_coupling','r06_aux_coupling_capped'] else size;offset=[(w-size[0])//2,oy-size[1]];fitted=im.resize(size,Image.Resampling.NEAREST);foot_adjust=size[1]-fitted.getchannel('A').getbbox()[3];offset[1]+=foot_adjust;out=Image.new('RGBA',(w,h));out.alpha_composite(fitted,offset)
            out.putdata([(*nearest(c[:3],ident=='r06_medium_niche'),255) if c[3] else (0,0,0,0) for c in out.get_flattened_data()]);rel=f'assets/items/{ident}.png';out.save(P/rel)
            assets.append(dict(id=ident,path=rel,size=s['size'],origin=s['origin'],foot_anchor=s['origin'],role='independent_environment_sprite',architecture=s['architecture'],roof_variants_pending=s['architecture'],palette='HIG-R06-128',sha256=sha(P/rel),collision='No collision supplied; proposed grids separate; alpha is never collision',runtime_verified=False))
            ops.append(dict(id=ident,source=r['output'],box=list(box),trim_bbox=list(trim),target_canvas=s['size'],component_quantization=component_quantization,fitted_size=size,offset=offset,alpha_threshold=128,foot_blank_row_compensation=foot_adjust,resample='nearest',foot_baseline=oy,coupling_alignment=('shared100x63visible canvas, fixed end/foot positions' if 'coupling' in ident else None),source_slot_note='AI raw spacing deviates from nominal uniform slot guides; visually inspected isolated crop keeps complete silhouette; production dimensions/origins exact',quantizer='Nearest RGB squared distance, first palette color on ties'))
    write('sprite-manifest.json',dict(batch=b['batch'],status='exported_pending_quality_scene_generation_pending',assets=assets,crop_operations=ops,source_sha256=b['source_sha256'],view_slots_fulfilled=0,runtime_verified=False))
    validator=ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py';spec=importlib.util.spec_from_file_location('r06_sprite_skill',validator);pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/sprites-skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');assert passed,buf.getvalue()
    for a in assets:
        q=Image.open(P/a['path']);box=q.getchannel('A').getbbox();assert list(q.size)==a['size'] and box and box[3]==a['origin'][1],a['id'];assert all(c[3] in [0,255] and (not c[3] or c[:3] in rgb) for c in q.get_flattened_data())
    m=read('sprite-manifest.json');m['status']='sprite_assets_verified_roof_and_scene_assembly_pending';write('sprite-manifest.json',m);write('sprites-validation.json',dict(passed=True,requested_skill_validator=True,independent_sprites=len(assets),source_current=True,view_slots_fulfilled=0,roof_and_scene_assembly_pending=True,runtime_verified=False))
    for a in assets:
        (P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n{a["size"]}静态RGBA、二值alpha、HIG-R06-128。脚底原点{a["origin"]}；像素归一化/母图裁切见sprite-manifest.json。\n\nSHA {a["sha256"]}。建筑屋顶分层与完整场景仍待装配，本文件不证明原生门/碰撞/交互/运行，不计已完成视图。\n',encoding='utf-8')
    print(json.dumps(dict(batch=P.name,independent_sprites=len(assets),architectures=sum(a['architecture'] for a in assets),passed=True,view_slots_fulfilled=0),ensure_ascii=False))
if __name__=='__main__':main()
