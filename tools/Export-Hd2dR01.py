"""Scene-only R01 exporter using the requested skill's palette/alpha rules.

Generated artwork supplies materials and objects. Explicit proposed grid geometry
supplies floors/boundaries; neither PNG alpha nor generated geometry defines NPCs.
"""
from pathlib import Path
from functools import lru_cache
import importlib.util, json, hashlib
from PIL import Image, ImageDraw, ImageChops, ImageOps

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v1'
SKILL=ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master'
ASSETS=[]; OPS=[]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name): return json.loads((P/name).read_text(encoding='utf-8'))
def write(name,v): (P/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def raw(name): return Image.open(P/'raw'/name).convert('RGBA')
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sample(name,box,size):
    src=raw(name); assert 0<=box[0]<box[2]<=src.width and 0<=box[1]<box[3]<=src.height
    OPS.append(dict(source='raw/'+name,box=list(box),target_size=list(size),resample='nearest'))
    return src.crop(box).resize(size,Image.Resampling.NEAREST)
def fill(tile,size):
    out=Image.new('RGBA',size)
    for y in range(0,size[1],tile.height):
        for x in range(0,size[0],tile.width):
            part=ImageOps.mirror(tile) if (x//tile.width)%2 else tile
            if (y//tile.height)%2:part=ImageOps.flip(part)
            out.alpha_composite(part,(x,y))
    return out
def water_plate(size):
    # Reuse the full previously generated water painting, never tile a strip.
    source=raw('reuse-n1-water.png'); ratio=size[0]/size[1]
    w=min(source.width,round(source.height*ratio));h=round(w/ratio)
    x=(source.width-w)//2;y=(source.height-h)//2
    return sample('reuse-n1-water.png',(x,y,x+w,y+h),size)
def save(im,name,category='backgrounds',origin=(0,0),**meta):
    rel=f'assets/{category}/{name}.png'; im.save(P/rel)
    ASSETS.append(dict(id=name,path=rel,size=list(im.size),origin=list(origin),**meta));return im
def asset(name,category='backgrounds'):return Image.open(P/f'assets/{category}/{name}.png').convert('RGBA')
def cells(s):
    out={(x,y) for a,b,c,d in s['walkable_rectangles'] for y in range(b,d+1) for x in range(a,c+1)}
    for a,b,c,d in s['blocked_rectangles']:out-={(x,y) for y in range(b,d+1) for x in range(a,c+1)}
    return out
def ranges(vs):
    out=[]
    for v in sorted(vs):
        if not out or v>out[-1][1]+1:out.append([v,v])
        else:out[-1][1]=v
    return out
def sprite(ident,source,box,spec):
    im=raw(source).crop(box); a=im.getchannel('A').point(lambda v:255 if v>=128 else 0);im.putalpha(a)
    bbox=a.getbbox(); assert bbox,ident
    im=im.crop(bbox); w,h=spec['size']; ox,oy=spec['origin']
    # Foot/baseline is aligned to the declared origin, not the canvas bottom.
    scale=min((w-4)/im.width,(oy-2)/im.height)
    size=(max(1,round(im.width*scale)),max(1,round(im.height*scale)))
    fit=im.resize(size,Image.Resampling.NEAREST);out=Image.new('RGBA',(w,h));offset=((w-size[0])//2,oy-size[1])
    out.alpha_composite(fit,offset)
    save(out,ident,'items',spec['origin'],role='independent_environment_sprite',
         foot_anchor=spec['origin'],interaction_hint=[ox-13,oy-13,ox+12,oy+12],
         collision='Explicit grid/occupancy proposal only; alpha is never a collision mask')
    OPS.append(dict(source='raw/'+source,box=list(box),alpha_threshold=128,trim_bbox=list(bbox),
                    target_canvas=[w,h],fitted_size=list(size),offset=list(offset),foot_baseline=oy,resample='nearest'))
    return out

def main():
    scenes=read('layouts.json');brief=read('brief.json');specs={s['id']:s for s in brief['sprites']}
    # Visually inspected source regions: no generated border/water is used as floor.
    materials={
      'r01_camp':('r01-camp-v2.png',(180,335,885,857),(506,376)),
      'r01_canal_pump':('r01-pump-v1.png',(285,83,770,221),(416,118)),
      'r01_canal_tomb':('r01-tomb-v1.png',(185,123,850,229),(442,70))}
    walls={
      'r01_camp':('r01-camp-v2.png',(398,869,840,921)),
      'r01_canal_pump':('r01-pump-v1.png',(304,230,610,296)),
      'r01_canal_tomb':('r01-tomb-v1.png',(344,262,560,326))}
    earth=sample('r01-tomb-v1.png',(260,1054,1150,1102),(598,32))
    for scene in scenes:
        rid=scene['id'];size=tuple(scene['size']);cs=cells(scene);mask=Image.open(P/f'guides/{rid}_walkable.png').convert('L')
        fn,box,sz=materials[rid];floor=fill(sample(fn,box,sz),size)
        if rid=='r01_canal_pump':
            floor.alpha_composite(fill(sample('r01-pump-v1.png',(620,415,945,510),(286,84)),(312,182)),(468,364))
        floor.putalpha(mask);save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        if rid=='r01_camp':
            back=water_plate(size)
            for rect,box in zip(scene['blocked_rectangles'],[(258,154,611,237),(1020,158,1270,213)]):
                a,b,c,d=rect;back.alpha_composite(sample('r01-camp-v2.png',box,((c-a+1)*26,(d-b+1)*26)),(a*26,b*26))
        else:
            back=fill(earth,size)
            # The water is below the paths, restricted to the authored drainage area.
            wm=Image.new('L',size);wd=ImageDraw.Draw(wm)
            if rid=='r01_canal_pump':wd.rectangle((286,286,961,701),fill=255)
            else:wd.rectangle((208,208,727,493),fill=255)
            wm=ImageChops.multiply(wm,ImageChops.invert(mask));back.paste(water_plate(size),(0,0),wm)
        save(back,rid+'__backing',role='blocked_background',scene=rid)
        structure=Image.new('RGBA',size);fore=Image.new('RGBA',size);fn,box=walls[rid]
        wall_h=13 if rid=='r01_camp' else 26
        for y in range(scene['cells'][1]):
            for a,b in ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):
                structure.alpha_composite(fill(sample(fn,box,(156,wall_h)),((b-a+1)*26,wall_h)),(a*26,y*26-wall_h))
            for a,b in ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):
                fore.alpha_composite(fill(sample(fn,box,(156,13)),((b-a+1)*26,13)),(a*26,(y+1)*26))
        for x in range(scene['cells'][0]):
            for side,offset in [(-1,-7),(1,26)]:
                for a,b in ranges([y for cx,y in cs if cx==x and (x+side,y) not in cs]):
                    structure.alpha_composite(fill(sample(fn,box,(7,52)),(7,(b-a+1)*26)),(x*26+offset,a*26))
        # Closed wall footprints of the living side-room remain separate from floor.
        if rid=='r01_canal_pump':
            for a,b,c,d in scene['blocked_rectangles']:
                structure.alpha_composite(fill(sample(fn,box,(52,26)),((c-a+1)*26,(d-b+1)*26)),(a*26,b*26))
        if rid=='r01_canal_tomb':
            # Preserve the master's funerary architecture without baking it into land.
            niche=sample('r01-tomb-v1.png',(269,20,406,107),(78,52))
            for x in [8,14,21,27]:structure.alpha_composite(niche,(x*26,52))
        for im in [structure,fore]:im.putalpha(ImageChops.multiply(im.getchannel('A'),ImageChops.invert(mask)))
        save(structure,rid+'__structure',role='nonwalkable_boundary_architecture',scene=rid)
        save(fore,rid+'__foreground',role='separate_front_edges',scene=rid)
        save(Image.alpha_composite(back,floor),rid+'__plan',role='flat_painted_plan',scene=rid)

    crops={
      'r01_worker_shed':('r01-architecture-v1.png',(18,336,626,750)),
      'r01_winch_shed':('r01-architecture-v1.png',(650,380,1060,750)),
      'r01_canal_entry':('r01-architecture-v1.png',(1096,325,1536,760)),
      'r01_coffin_coat':('r01-props-v1.png',(110,28,448,510)),
      'r01_winch_socket':('r01-props-v1.png',(570,110,1004,500)),
      'r01_sluice_wheel':('r01-props-v1.png',(1060,20,1448,512)),
      'r01_maintenance_ladder':('r01-props-v1.png',(160,533,377,1010)),
      'r01_shelter_bedroll':('r01-props-v1.png',(565,588,977,960)),
      'r01_water_jug':('r01-props-v1.png',(1155,646,1391,950))}
    for ident,(fn,box) in crops.items():sprite(ident,fn,box,specs[ident])
    # Real skill quantizer, cached exact RGB lookup; unchanged metric/palette/alpha.
    finalizer=module('pam_r01_finalize',SKILL/'scripts/finalize_assets.py');orig=finalizer._find_nearest
    @lru_cache(maxsize=250000)
    def nearest(r,g,b,pal):return orig(r,g,b,pal)
    finalizer._find_nearest=lambda r,g,b,pal:nearest(r,g,b,tuple(pal))
    finalizer.cmd_quantize(P);finalizer.cmd_clean(P)

    # Split the three architectural silhouettes into disjoint body/roof PNGs.
    roof_cuts={'r01_worker_shed':116,'r01_winch_shed':96,'r01_canal_entry':115}
    for ident,cut in roof_cuts.items():
        im=asset(ident,'items');roof=im.copy();body=im.copy()
        ra=im.getchannel('A');ba=im.getchannel('A');ImageDraw.Draw(ra).rectangle((0,cut,im.width,im.height),fill=0)
        ImageDraw.Draw(ba).rectangle((0,0,im.width,cut-1),fill=0);roof.putalpha(ra);body.putalpha(ba)
        for part,image in [('roof',roof),('body',body)]:
            save(image,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,split_at_y=cut)
    for scene in scenes:
        rid=scene['id'];size=tuple(scene['size']);props=Image.new('RGBA',size);roofs=Image.new('RGBA',size)
        for obj in sorted(scene['objects'],key=lambda o:o['cell'][1]):
            ident=obj['id'];ox,oy=specs[ident]['origin'];x,y=obj['cell'];pos=(x*26+13-ox,y*26+13-oy)
            props.alpha_composite(asset(ident+('__body' if ident in roof_cuts else ''),'items'),pos)
            if ident in roof_cuts:roofs.alpha_composite(asset(ident+'__roof','items'),pos)
        save(props,rid+'__props_preview',role='placement_preview_only_use_individual_sprites_for_game',scene=rid)
        if roofs.getchannel('A').getbbox():save(roofs,rid+'__roof',role='independent_toggleable_roofs',scene=rid)
        env=asset(rid+'__backing')
        for part in ['floor','structure','props_preview','foreground']:env.alpha_composite(asset(rid+'__'+part))
        if roofs.getchannel('A').getbbox():
            save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid)
            env.alpha_composite(roofs)
        save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid)
        env.save(P/f'previews/{rid}.png')
    for part in ['plan','environment']:
        im=Image.new('RGBA',(1352,1638),'#0F1218');im.alpha_composite(asset('r01_canal_pump__'+part),(0,0));im.alpha_composite(asset('r01_canal_tomb__'+part),(208,910))
        save(im,'r01_canal__'+part+'_overview',role='two_floor_contact_sheet_not_single_room')
    # A uniform-cell atlas is optional; individual sprites remain authoritative.
    atlas=Image.new('RGBA',(936,780));atlas_records=[]
    for i,ident in enumerate(specs):
        im=asset(ident,'items');tx=(i%3)*312+(312-im.width)//2;ty=(i//3)*260+(260-im.height)//2
        atlas.alpha_composite(im,(tx,ty));atlas_records.append(dict(id=ident,rect=[tx,ty,*im.size],sprite_origin=specs[ident]['origin'],atlas_origin=[tx+specs[ident]['origin'][0],ty+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/r01_architecture_props.png');write('sheets/manifest.json',dict(type='nine separate static environment sprites, not animation',size=[936,780],frames=atlas_records))
    for a in ASSETS:a.update(sha256=sha(P/a['path']),palette='BRY-R01-128',runtime_verified=False)
    manifest=dict(schema=1,batch='R01-camp-canal-v1',status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,
        assets=ASSETS,scenes=scenes,source_sha256=brief['source_sha256'],raw_sources={f.name:sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=OPS,
        import_contract=dict(sampling='nearest',mipmaps=False,scale='1 image pixel = 1 room pixel',room_origin=[0,0],
            draw_order=['backing','floor','structure','independent body/props and native actors at foot depth','foreground','roof (toggleable)'],
            collision='layouts.json proposed cells; adopt through native engine grid after testing, never from art alpha',
            npc='Only unoccupied spatial reservations. NPC art, dialogue and behavior belong to the other model.',
            lighting='Unlit base materials. Native light sources must be installed/tested independently.'),
        inventory_requests={'R01-camp__plan':'assets/backgrounds/r01_camp__plan.png',
          'R01-camp__exterior_or_site':'assets/backgrounds/r01_camp__environment.png',
          'R01-canal__plan':'assets/backgrounds/r01_canal__plan_overview.png',
          'R01-canal__exterior_or_site':'assets/items/r01_canal_entry.png',
          'R01-canal__interior_or_working_space':'assets/backgrounds/r01_canal__environment_overview.png'},
        limitations=['Art geometry proposal, not an implemented native room.',
          'Generated masters had approximate geometry; exported floors/boundaries use authored cell masks and painted material crops.',
          'Standalone canal entry has no exterior terrain location assigned.',
          'Camera, native collisions, doorway interaction and dynamic lighting require game integration testing.',
          'N1 art registration is separate; this batch does not claim all remaining maps complete.'])
    write('manifest.json',manifest)
    prefix='src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v1/'
    refs=[dict(id='r01-camp-v1',inputs=[prefix+'guides/r01_camp_geometry.png','design/12_美术参考/城市概念/BRY-概念-v1.png','src/Art/hd2d_26x26_20261013/previews/r_eao_n1_yard__preview.png'],selected=False),
          dict(id='r01-camp-v2',inputs=[prefix+'raw/r01-camp-v1.png',prefix+'guides/r01_camp_geometry.png'],selected=True),
          dict(id='r01-pump-v1',inputs=[prefix+'guides/r01_canal_pump_generation_v1.png','design/12_美术参考/城市概念/BRY-概念-v1.png'],selected=True),
          dict(id='r01-tomb-v1',inputs=[prefix+'guides/r01_canal_tomb_geometry.png',prefix+'raw/r01-pump-v1.png'],selected=True),
          dict(id='r01-architecture-v1',inputs=[],selected=True),dict(id='r01-props-v1',inputs=[],selected=True)]
    for rec in refs:
        ident=rec['id'];fp=P/f'raw/{ident}.png';prompt=P/f'notes/prompt-{ident}.txt'
        rec.update(method='built-in image_gen',prompt=f'notes/prompt-{ident}.txt',prompt_sha256=sha(prompt),
          inputs=[dict(path=p,sha256=sha(ROOT/p)) for p in rec['inputs']],output=f'raw/{ident}.png',output_sha256=sha(fp),
          original_size=list(Image.open(fp).size),spec_lock_sha256=sha(P/'spec_lock.md'),postprocess='manifest.json crop_operations; real skill palette quantizer, binary alpha and nearest-neighbor geometry assembly')
    write('generation-log.json',dict(skill_commit=brief['skill_commit'],generation_count=len(refs),records=refs,
          reuse_sources=[dict(path='src/Art/hd2d_26x26_20261013/raw/n1-water-v1.png',sha256=sha(P/'raw/reuse-n1-water.png'),batch_copy='raw/reuse-n1-water.png',method='existing project AI water master reused as nonrepeating backing')],
          input_note='Pump v1 guide is archived before the separate living-room wall proposal was added during export.'))
    write('preview-index.json',[dict(id=s['id'],name=s['name_zh'],size=s['size'],layers=[a for a in ASSETS if a.get('scene')==s['id']]) for s in scenes])
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(ASSETS),independent_sprites=len(specs),inventory_slots=5),ensure_ascii=False))

if __name__=='__main__':main()
