"""Normalize the reviewed BRY masters; keep incomplete batch outside delivered-view counts."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,importlib.util,contextlib,io
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-core-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    b=read('brief.json');specs={s['id']:s for s in b['sprites']};assert all(sha(ROOT/n)==h for n,h in b['source_sha256'].items());log=read('generation-log.json');records={r['id']:r for r in log['records'] if r.get('output_sha256')}
    recipes=[
      ('bry-architecture-v1',list(specs)[:8],[(0,0,464,512),(466,0,879,512),(880,0,1230,512),(1231,0,1536,512),(0,530,458,1024),(461,530,770,1024),(774,530,1090,1024),(1095,530,1536,1024)]),
      ('bry-props-a-v1',list(specs)[8:16],[(0,0,442,512),(448,0,780,512),(788,0,1105,512),(1110,0,1536,512),(0,530,370,1024),(380,530,785,1024),(800,530,1135,1024),(1150,520,1536,1024)]),
      ('bry-props-b-v1',list(specs)[16:24],[(0,0,390,512),(410,0,750,512),(770,0,1080,512),(1090,0,1536,512),(0,520,385,1024),(410,520,735,1024),(765,520,1110,1024),(1130,520,1536,1024)]),
      ('bry-props-c-v1',list(specs)[24:32],[(0,0,375,512),(385,0,815,512),(835,0,1200,512),(1220,0,1536,512),(0,520,390,1024),(415,520,760,1024),(800,520,1130,1024),(1140,520,1536,1024)]),
      ('bry-props-d-v1',list(specs)[32:40],[(0,0,400,512),(415,0,730,512),(735,0,1160,512),(1170,0,1536,512),(0,520,380,1024),(395,520,790,1024),(800,520,1140,1024),(1150,520,1536,1024)])]
    pal=read('palettes/bry_core_128.json');rgb=[tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in pal['colors']]
    @lru_cache(None)
    def nearest(c):return min(rgb,key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    assets=[];ops=[]
    for master,ids,boxes in recipes:
        if master not in records:continue
        r=records[master];assert sha(P/r['output'])==r['output_sha256'] and sha(P/r['prompt'])==r['prompt_sha256'];assert sha(P/'spec_lock.md')==r['spec_lock_sha256'];raw=Image.open(P/r['output']).convert('RGBA')
        for ident,box in zip(ids,boxes):
            s=specs[ident];im=raw.crop(box);alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0);im.putalpha(alpha);trim=alpha.getbbox();assert trim,ident;im=im.crop(trim);w,h=s['size'];ox,oy=s['origin'];scale=min((w-4)/im.width,(oy-2)/im.height);size=[max(1,round(im.width*scale)),max(1,round(im.height*scale))];offset=[(w-size[0])//2,oy-size[1]];fitted=im.resize(size,Image.Resampling.NEAREST);foot_adjust=size[1]-fitted.getchannel('A').getbbox()[3];offset[1]+=foot_adjust;out=Image.new('RGBA',(w,h));out.alpha_composite(fitted,offset)
            out.putdata([(*nearest(c[:3]),255) if c[3] else (0,0,0,0) for c in out.get_flattened_data()]);rel=f'assets/items/{ident}.png';out.save(P/rel)
            assets.append(dict(id=ident,path=rel,size=s['size'],origin=s['origin'],foot_anchor=s['origin'],role='independent_environment_sprite',architecture=s['architecture'],wall_decal=s.get('wall_decal',False),roof_variants_pending=s['architecture'],palette='BRY-CORE-128',sha256=sha(P/rel),collision='No collision supplied; proposed grids separate; alpha is never collision',runtime_verified=False))
            ops.append(dict(id=ident,source=r['output'],box=list(box),trim_bbox=list(trim),target_canvas=s['size'],fitted_size=size,offset=offset,alpha_threshold=128,foot_blank_row_compensation=foot_adjust,resample='nearest',foot_baseline=oy,source_slot_note='AI raw spacing deviates from nominal uniform slot guides; visually inspected isolated crop keeps complete silhouette; production dimensions/origins exact',quantizer='Nearest RGB squared distance, first palette color on ties'))
    write('sprite-manifest.json',dict(batch=b['batch'],status='exported_pending_quality_scene_generation_pending',assets=assets,crop_operations=ops,source_sha256=b['source_sha256'],view_slots_fulfilled=0,runtime_verified=False))
    validator=ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/scripts/asset_validator.py';spec=importlib.util.spec_from_file_location('bry_sprite_skill',validator);pam=importlib.util.module_from_spec(spec);spec.loader.exec_module(pam);buf=io.StringIO()
    with contextlib.redirect_stdout(buf):passed=pam.validate_project(P)
    (P/'notes/sprites-skill-validation.txt').write_text(buf.getvalue(),encoding='utf-8');assert passed,buf.getvalue()
    for a in assets:
        q=Image.open(P/a['path']);box=q.getchannel('A').getbbox();assert list(q.size)==a['size'] and box and box[3]==a['origin'][1],a['id'];assert all(c[3] in [0,255] and (not c[3] or c[:3] in rgb) for c in q.get_flattened_data())
    m=read('sprite-manifest.json');m['status']='sprite_assets_verified_roof_and_scene_assembly_pending';write('sprite-manifest.json',m);write('sprites-validation.json',dict(passed=True,requested_skill_validator=True,independent_sprites=len(assets),source_current=True,view_slots_fulfilled=0,roof_and_scene_assembly_pending=True,runtime_verified=False))
    for a in assets:
        (P/'notes'/f'{a["id"]}.md').write_text(f'# {a["id"]}\n\n{a["size"]}静态RGBA、二值alpha、BRY-CORE-128。脚底原点{a["origin"]}；像素归一化/母图裁切见sprite-manifest.json。\n\nSHA {a["sha256"]}。建筑屋顶分层与完整场景仍待装配，本文件不证明原生门/碰撞/交互/运行，不计已完成视图。\n',encoding='utf-8')
    print(json.dumps(dict(batch=P.name,independent_sprites=len(assets),architectures=sum(a['architecture'] for a in assets),passed=True,view_slots_fulfilled=0),ensure_ascii=False))
if __name__=='__main__':main()
