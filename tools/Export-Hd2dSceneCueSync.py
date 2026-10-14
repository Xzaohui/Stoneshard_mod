"""Export six reviewed cues and version the affected art without rewriting story files."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,shutil,copy,argparse
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013';C=P/'batches/Scene-cues-20261014-v1'
def read(p):return json.loads(p.read_text(encoding='utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def quant(im,colors):
    rgb=[tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in colors]
    @lru_cache(None)
    def nearest(p):return min(rgb,key=lambda q:sum((p[i]-q[i])**2 for i in range(3)))
    q=Image.new('RGBA',im.size);q.putdata([(*nearest(v[:3]),255) if v[3] else (0,0,0,0) for v in im.get_flattened_data()]);return q
def export_cues():
    brief=read(C/'brief.json');palette=read(C/'palettes/shared.json')['regional_palettes'];raw=Image.open(C/'raw/scene-cues-v1.png').convert('RGBA');assets=[];ops=[]
    for i,s in enumerate(brief['sprites']):
        box=[(i%3)*512,(i//3)*512,(i%3+1)*512,(i//3+1)*512];im=raw.crop(box)
        a=im.getchannel('A').point(lambda v:255 if v>=128 else 0);im.putalpha(a);bbox=a.getbbox();assert bbox,s['id'];im=im.crop(bbox)
        w,h=s['size'];ox,oy=s['origin'];scale=min((w-4)/im.width,(oy-2)/im.height)
        # A small paper overlays the existing sign boards, rather than covering the whole post.
        if s['id']=='r02_bridge_note':scale=min(20/im.width,24/im.height)
        size=[max(1,round(im.width*scale)),max(1,round(im.height*scale))];off=[(w-size[0])//2,oy-size[1]]
        out=Image.new('RGBA',(w,h));out.alpha_composite(im.resize(size,Image.Resampling.NEAREST),off)
        pk='BRY-R01-128' if s['id'].startswith('r01') else 'DEN-R02-128';out=quant(out,palette[pk]);rel=f'assets/items/{s["id"]}.png';out.save(C/rel)
        assets.append(dict(id=s['id'],path=rel,size=s['size'],origin=s['origin'],role='independent_environment_sprite',scene_cue_role=s['role'],foot_anchor=s['origin'],interaction_hint=[ox-13,oy-13,ox+12,oy+12],collision='None supplied; visual cue only, alpha is never collision',sha256=sha(C/rel),palette=pk,runtime_verified=False))
        ops.append(dict(id=s['id'],source='raw/scene-cues-v1.png',box=box,alpha_threshold=128,trim_bbox=list(bbox),target_canvas=[w,h],fitted_size=size,offset=off,resample='nearest',palette=pk,quantizer='Exact nearest RGB squared distance, first palette color on ties; same as skill finalizer'))
    write(C/'manifest.json',dict(batch=brief['batch'],status='exported_pending_validation',assets=assets,source_sha256=brief['source_sha256'],crop_operations=ops,runtime_verified=False))
    return assets,ops
def save_asset(folder,m,im,ident,**meta):
    previous=next((a for a in m['assets'] if a['id']==ident),None);rel=previous['path'] if previous else f'assets/backgrounds/{ident}.png';im.save(folder/rel)
    a=copy.deepcopy(previous) if previous else dict(id=ident,path=rel,size=list(im.size),origin=[0,0],palette=m['assets'][0]['palette'],runtime_verified=False)
    a.update(meta,sha256=sha(folder/rel));m['assets']=[v for v in m['assets'] if v['id']!=ident]+[a]
def layer(folder,m,scene,cues):
    byid={a['id']:a for a in m['assets']};out=Image.new('RGBA',tuple(scene['size']))
    for c in cues:
        a=byid[c['id']];im=Image.open(folder/a['path']).convert('RGBA');point=c['pixel_anchor'];out.alpha_composite(im,(point[0]-a['origin'][0],point[1]-a['origin'][1]))
    return out
def compose(folder,m,scene,repair=False,conditional=False,roof=True):
    rid=scene['id'];parts=['backing','repaired_floor' if repair else 'floor','repaired_structure' if repair else 'structure','story_underlay','props_preview','story_details']
    if conditional:parts+=['conditional_cues']
    parts+=['repaired_foreground' if repair else 'foreground']
    if roof:parts+=['roof']
    out=Image.new('RGBA',tuple(scene['size']));ids={a['id']:a for a in m['assets']}
    for part in parts:
        a=ids.get(rid+'__'+part)
        if a:out.alpha_composite(Image.open(folder/a['path']).convert('RGBA'))
    return out
def sync(base,assets,ops):
    old=P/'batches'/base;new=P/'batches'/base.replace('-v1','-v2');assert old!=new
    if not new.exists():
        shutil.copytree(old,new,ignore=shutil.ignore_patterns('exports','previews','validation.json','preview-validation.json','preview.html','IMPORT.md'))
        (new/'previews').mkdir();(new/'exports').mkdir()
    original=read(old/'manifest.json');m=copy.deepcopy(original);m['batch']=new.name;m['status']='exported_pending_validation';by_scene={s['id']:s for s in m['scenes']}
    m['supersedes']=dict(batch=base,manifest_sha256=sha(old/'manifest.json'),inventory_requests=sorted(original['inventory_requests']),reason='2026-10-14 reviewed scene-source drift; immutable v1 retained')
    m['inherited_assets']={a['path']:a['sha256'] for a in original['assets']};m['source_sha256']={n:sha(ROOT/n) for n in original['source_sha256']}
    chosen=[a for a in assets if a['id'].startswith('r01' if base.startswith('R01') else 'r02')]
    for a in chosen:shutil.copy2(C/a['path'],new/a['path']);m['assets'].append(copy.deepcopy(a))
    # Own contract preserves the combined master lock; inherited generation locks stay byte-identical.
    contract=new/'cue-source';contract.mkdir(exist_ok=True)
    for rel in ['spec_lock.md','design_spec.md','brief.json','generation-log.json','manifest.json','palettes/shared.json','notes/prompt-scene-cues-v1.txt','raw/scene-cues-v1.png']:
        dst=contract/rel;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/rel,dst)
    for a in assets:
        dst=contract/a['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(C/a['path'],dst)
    log=read(old/'generation-log.json');external=copy.deepcopy(read(C/'generation-log.json')['records'][0]);external.update(contract='cue-source',prompt='cue-source/'+external['prompt'],output='cue-source/'+external['output'],spec_lock='cue-source/spec_lock.md');log['external_generation_records']=[external];log['generation_count']=len(log['records'])+1
    write(new/'generation-log.json',log);m['cue_contract']=dict(path='cue-source',master_sha256=external['output_sha256'],selected_sprite_ids=[a['id'] for a in chosen],operations=[o for o in ops if o['id'] in {a['id'] for a in chosen}])
    def cue(rid,ident,cell,offset=(0,0),render='story_details',condition=None,**extra):
        c=dict(id=ident,instance_id=rid+'__'+ident,cell=cell,pixel_offset=list(offset),pixel_anchor=[cell[0]*26+13+offset[0],cell[1]*26+13+offset[1]],render_layer=render,collision=None,default_visible=condition is None,condition=condition,runtime_verified=False,**extra)
        by_scene[rid].setdefault('scene_cues',[]).append(c)
    if base.startswith('R01'):
        cue('r01_camp','r01_ash_threshold',[12,11],offset=[0,26],render='story_underlay',source_locator='N2-S01',meaning='Ordinary ash immediately outside threshold; no ghost/rune/collision')
        cue('r01_camp','r01_tool_stub',[30,17],offset=[12,15],render='story_underlay',source_locator='N2-S02',meaning='Exposed stub below existing empty shaft socket; observation only')
    else:
        cue('r02_tax_main','r02_well_notice',[28,10],offset=[0,-14],source_locator='N5-S02',meaning='Fresh paint and blank well notice; text rendered by engine')
        cue('r02_tax_main','r02_red_water_buckets',[29,10],offset=[-8,0],source_locator='N5-S02',bucket_count=2,meaning='Exactly two stacked red buckets and water-carrier knot; no inventory or verdict')
        cue('r02_inn_exterior','r02_rope_shoe_stall',[25,19],render='conditional_cues',condition=dict(id='N18_return_visit',description='Only the matching N18-S01 return-visit scene; ownership, consent and shoes state handled by engine',default=False),source_locator='N18-S01',meaning='One pair of small half-woven rope shoes; no child or owner image')
        cue('r02_repair','r02_bridge_note',[28,24],offset=[0,-42],render='conditional_cues',condition=dict(id='SQ04_refusal_return_visit',description='Refused coerced transport AND corresponding SQ04-S03 return visit; never clears transport_harm',default=False),source_locator='SQ04-S03',parent_instance='r02_repair__r02_road_sign__2',meaning='Blank paper and nail on existing sign boards; no new signpost')
    changed=[]
    for s in m['scenes']:
        if not s.get('scene_cues'):continue
        rid=s['id'];changed.append(rid)
        for name in sorted({c['render_layer'] for c in s['scene_cues']}):save_asset(new,m,layer(new,m,s,[c for c in s['scene_cues'] if c['render_layer']==name]),rid+'__'+name,role='conditional_return_visit_layer_off_by_default' if name=='conditional_cues' else 'independent_scene_observation_layer',scene=rid,default_visible=name!='conditional_cues',collision=None)
        if any(c['default_visible'] for c in s['scene_cues']):
            for suffix,roof in [('environment',True),('working_space',False),('repaired_preview',True)]:
                ident=rid+'__'+suffix
                if any(a['id']==ident for a in m['assets']):save_asset(new,m,compose(new,m,s,repair=suffix=='repaired_preview',roof=roof),ident)
        if any(not c['default_visible'] for c in s['scene_cues']):
            save_asset(new,m,compose(new,m,s,conditional=True),rid+'__conditional_environment',role='conditional_scene_preview_off_by_default',scene=rid,default_visible=False,collision=None)
            if s.get('repaired_add_cells'):save_asset(new,m,compose(new,m,s,repair=True,conditional=True),rid+'__conditional_repaired_environment',role='conditional_repaired_preview_off_by_default',scene=rid,default_visible=False,collision=None)
    m['changed_scenes']=changed;m['replaced_asset_paths']=[a['path'] for a in m['assets'] if a['path'] in m['inherited_assets'] and a['sha256']!=m['inherited_assets'][a['path']]]
    m['source_review']=dict(date='2026-10-14',changed_source_files=[n for n in m['source_sha256'] if m['source_sha256'][n]!=original['source_sha256'][n]],no_raster_change_needed=['N9-S03 / X75 / X76: existing public table, river windows and separate cabinets remain suitable; engine owns text and knowledge'],geometry_unchanged=True,NPC_files_edited=False,runtime_verified=False)
    write(new/'manifest.json',m);write(new/'layouts.json',m['scenes']);brief=read(old/'brief.json');brief.update(batch=m['batch'],source_sha256=m['source_sha256'],scene_cue_contract=m['cue_contract']);write(new/'brief.json',brief)
    print(json.dumps(dict(batch=new.name,production_pngs=len(m['assets']),cues=len(chosen),replaced_previews=m['replaced_asset_paths'],conditional_default=False),ensure_ascii=False))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--batch',choices=['R01-camp-canal-v1','R02-river-v1']);args=ap.parse_args()
    assets,ops=export_cues()
    for b in [args.batch] if args.batch else ['R01-camp-canal-v1','R02-river-v1']:sync(b,assets,ops)
if __name__=='__main__':main()
