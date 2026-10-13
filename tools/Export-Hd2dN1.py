"""Pack AI-painted materials on the existing N1 geometry; no game writes.

User-approved Pixel Asset Master post-processing: exact palette quantization,
binary alpha, non-destructive crops, native-canvas layout and sprite export.
Raw source images are retained, hashes and every crop are recorded.
"""
from pathlib import Path
from functools import lru_cache
import importlib.util
import hashlib
import json
import re
import zipfile
from PIL import Image, ImageDraw, ImageChops, ImageOps, ImageFilter, ImageEnhance

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013'
SKILL=ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master'
SIZE=(1040,780);TILE=26
RAW=P/'raw'
OUT=P/'assets';PRE=P/'previews'
MAN=[];CROPS=[]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def module(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def image(name): return Image.open(RAW/name).convert('RGBA')
def blank(): return Image.new('RGBA',SIZE)
def sample(name,box,size):
    CROPS.append(dict(source='raw/'+name,box=list(box),target_size=list(size),resample='nearest'))
    return image(name).crop(box).resize(size,Image.Resampling.NEAREST)
def fill_material(tile,size):
    """Mirrored architecture material fill, not a claimed seamless terrain tile."""
    out=Image.new('RGBA',size)
    for y in range(0,size[1],tile.height):
        for x in range(0,size[0],tile.width):
            part=tile
            if (x//tile.width)%2:part=ImageOps.mirror(part)
            if (y//tile.height)%2:part=ImageOps.flip(part)
            out.alpha_composite(part,(x,y))
    return out
def save(im,category,name,**meta):
    d=OUT/category;d.mkdir(parents=True,exist_ok=True)
    p=d/(name+'.png');im.save(p)
    MAN.append(dict(id=name,path=p.relative_to(P).as_posix(),size=list(im.size),origin=[0,0],**meta))
    return im
def cells(room):
    return {(x,y) for a,b,c,d in room['walkable_rectangles'] for y in range(b,d+1) for x in range(a,c+1)}
def ranges(values):
    values=sorted(values);out=[]
    for v in values:
        if not out or v>out[-1][-1]+1:out.append([v,v])
        else:out[-1][1]=v
    return out
def normalize_sprite(name,box,canvas,ident,origin):
    src=image(name).crop(box)
    alpha=src.getchannel('A').point(lambda a:255 if a>=128 else 0)
    src.putalpha(alpha);bbox=alpha.getbbox()
    if bbox is None: raise ValueError(ident+' is empty')
    src=src.crop(bbox)
    # Preserve object proportions, fit to a native cell-multiple canvas.
    scale=min((canvas[0]-4)/src.width,(canvas[1]-4)/src.height)
    size=(max(1,round(src.width*scale)),max(1,round(src.height*scale)))
    fitted=src.resize(size,Image.Resampling.NEAREST)
    result=Image.new('RGBA',canvas)
    result.alpha_composite(fitted,((canvas[0]-size[0])//2,canvas[1]-size[1]-2))
    save(result,'items',ident,sprite_origin=origin,role='independent_sprite',collision='native object only, never derive from full artwork alpha')
    CROPS.append(dict(source='raw/'+name,box=list(box),alpha_threshold=128,trim_bbox=list(bbox),target_canvas=list(canvas),fitted_size=list(size),resample='nearest'))
    return result

def main():
    PRE.mkdir(exist_ok=True)
    rooms=json.loads((P/'native_layouts.json').read_text(encoding='utf-8'))
    water=sample('n1-water-v1.png',(0,0,1448,1086),SIZE)
    save(water,'backgrounds','n1_water_base',role='nonrepeating_water_backing')
    # Rectangles below are visually inspected material regions, not guessed
    # geometry. Shape geometry comes only from native_layouts.json.
    floor_crops={
      'r_eao_n1_yard': [('n1-yard-v1.png',(144,144,575,749)),
                        ('n1-yard-v1.png',(612,553,999,625)),
                        ('n1-yard-v1.png',(1060,278,1284,712))],
      'r_eao_n1_bellhouse': [('n1-bellhouse-v1.png',(249,280,887,713)),
                             ('n1-bellhouse-v1.png',(945,549,1269,617))],
      'r_eao_n1_underpass': [('n1-underpass-v1.png',(154,714,575,832)),
                             ('n1-underpass-v1.png',(548,358,644,674)),
                             ('n1-underpass-v1.png',(715,221,1300,319))]}
    walls={
      'r_eao_n1_yard':('n1-yard-v1.png',(208,787,330,823)),
      'r_eao_n1_bellhouse':('n1-bellhouse-v1.png',(402,186,514,249)),
      'r_eao_n1_underpass':('n1-underpass-v1.png',(1090,119,1198,171))}
    for room in rooms:
        rid=room['id'];cs=cells(room)
        materials={
          'r_eao_n1_yard':('n1-yard-v1.png',(160,190,560,590),(260,260)),
          'r_eao_n1_bellhouse':('n1-bellhouse-v1.png',(260,300,780,560),(338,169)),
          'r_eao_n1_underpass':('n1-underpass-v1.png',(744,225,1264,315),(338,59))}
        fn,box,sz=materials[rid]
        floor=fill_material(sample(fn,box,sz),SIZE)
        mask=Image.open(P/'guides'/f'{rid}_walkable.png').convert('L')
        if rid.endswith('yard'):
            # One flat repair patch; edges are coplanar and carry no collision.
            floor.alpha_composite(sample('n1-yard-v1.png',(754,554,867,624),(104,78)),(546,481))
        if rid.endswith('bellhouse'):
            corridor=fill_material(sample('n1-yard-v1.png',(160,190,560,590),(260,260)),(260,104))
            floor.alpha_composite(corridor,(676,416))
        floor.putalpha(mask)
        assert ImageChops.difference(floor.getchannel('A'),mask).getbbox() is None
        save(floor,'backgrounds',rid+'__floor',role='exact_native_walkable_floor',room=rid)
        backing=water.copy() if rid.endswith('yard') else Image.new('RGBA',SIZE,'#101010')
        if rid.endswith('underpass'):
            # Code-native underground ambient shading, with a one-cell channel
            # outside the exact floor. No invented walkable water or new rooms.
            channel=mask.filter(ImageFilter.MaxFilter(53))
            backing.paste(ImageEnhance.Brightness(water).enhance(0.34),(0,0),channel)
        save(backing,'backgrounds',rid+'__backing',role='blocked_background',room=rid)
        structure=blank();foreground=blank()
        wall_name,wall_box=walls[rid]
        top_height=13 if rid.endswith('yard') else 39
        bottom_height=26 if rid.endswith('yard') else 13
        # Continuous runs prevent per-cell seams. All geometry lies outside
        # actual walkable pixels; foreground can be toggled separately.
        for y in range(30):
            top=[x for x,cy in cs if cy==y and (x,y-1) not in cs]
            bottom=[x for x,cy in cs if cy==y and (x,y+1) not in cs]
            for start,end in ranges(top):
                structure.alpha_composite(fill_material(sample(wall_name,wall_box,(104,top_height)),((end-start+1)*26,top_height)),(start*26,y*26-top_height))
            for start,end in ranges(bottom):
                foreground.alpha_composite(fill_material(sample(wall_name,wall_box,(104,bottom_height)),((end-start+1)*26,bottom_height)),(start*26,(y+1)*26))
        for x in range(40):
            for side,offset in [(-1,-7),(1,26)]:
                ys=[y for cx,y in cs if cx==x and (x+side,y) not in cs]
                for start,end in ranges(ys):
                    structure.alpha_composite(fill_material(sample(wall_name,wall_box,(7,52)),(7,(end-start+1)*26)),(x*26+offset,start*26))
        inv=ImageChops.invert(mask)
        for layer in [structure,foreground]:layer.putalpha(ImageChops.multiply(layer.getchannel('A'),inv))
        save(structure,'backgrounds',rid+'__structure',role='outside_floor_walls',room=rid)
        save(foreground,'backgrounds',rid+'__foreground',role='toggleable_front_walls',room=rid)
        for layer in [structure,foreground]:assert ImageChops.multiply(layer.getchannel('A'),mask).getbbox() is None
        # A flat plan is painted floor + backing, with no false 3D collision.
        plan=Image.alpha_composite(backing,floor)
        save(plan,'backgrounds',rid+'__plan',role='painted_flat_plan',room=rid)
    objects={
      'n1_bell':((30,30,492,494),(78,104),(39,95)),
      'n1_bedding':((542,106,1061,473),(104,78),(52,60)),
      'n1_cut_rope':((1093,175,1505,466),(26,26),(13,20)),
      'n1_portal':((37,535,485,973),(52,78),(26,70)),
      'n1_water_jug':((590,615,981,932),(26,26),(13,23)),
      'n1_unlit_lantern':((1138,546,1432,943),(26,52),(13,48))}
    for ident,(box,canvas,origin) in objects.items():
        normalize_sprite('n1-props-v2.png',box,canvas,ident,origin)
    normalize_sprite('n1-exterior-v1.png',(0,0,1374,1145),(312,260),'n1_bellhouse_exterior',(167,249))

    # Invoke the user's requested skill's actual quantizer, caching exact RGB
    # queries only. No change to its distance metric, palette or alpha rule.
    finalizer=module('pam_finalize',SKILL/'scripts/finalize_assets.py')
    original_nearest=finalizer._find_nearest
    @lru_cache(maxsize=250000)
    def nearest(r,g,b,palette):return original_nearest(r,g,b,palette)
    finalizer._find_nearest=lambda r,g,b,palette:nearest(r,g,b,tuple(palette))
    finalizer.cmd_quantize(P)
    finalizer.cmd_clean(P)
    # Composites are made after normalization, without RGB/alpha interpolation.
    def read_asset(name,cat='backgrounds'):return Image.open(OUT/cat/(name+'.png')).convert('RGBA')
    scene_previews=[]
    for room in rooms:
        rid=room['id'];composite=read_asset(rid+'__backing')
        for part in ['floor','structure','foreground']:composite=Image.alpha_composite(composite,read_asset(rid+'__'+part))
        save(composite,'backgrounds',rid+'__environment',role='static_environment_composite',room=rid)
        # Interactive objects stay individual sprites; this preview shows their
        # existing anchor positions, and is never baked into the room layers.
        placements=[]
        if rid.endswith('yard'):placements=[('n1_bell',31,16),('n1_cut_rope',31,19)]
        elif rid.endswith('bellhouse'):placements=[('n1_bedding',17,20)]
        preview=composite.copy()
        for ident,x,y in placements:
            sprite=read_asset(ident,'items');origin=next(a['sprite_origin'] for a in MAN if a['id']==ident)
            preview.alpha_composite(sprite,(x*26+13-origin[0],y*26+13-origin[1]))
        preview.save(PRE/(rid+'__preview.png'))
        scene_previews.append(dict(id=rid,name=room['name_zh'],image='previews/'+rid+'__preview.png'))
    exterior=read_asset('n1_bellhouse_exterior','items')
    ext_preview=Image.new('RGBA',(624,520),'#302020');ext_preview.alpha_composite(exterior.resize((624,520),Image.Resampling.NEAREST));ext_preview.save(PRE/'n1_bellhouse_exterior_2x.png')
    # Final metadata hashes are computed after all post-processing.
    for a in MAN:a['sha256']=sha(P/a['path']);a['palette']='DEN-N1-128';a['runtime_verified']=False
    manifest=dict(schema=1,batch='N1',status='exported_pending_visual_and_static_checks',
                  skill_commit='33d891c421a9ad3608f5a09af97271388ca923af',
                  format='RGBA PNG',native_cell_size=26,assets=MAN,rooms=rooms,
                  lighting=dict(mode='existing_native_dynamic_lights',baked=False,positions_source='native_layouts.json'),
                  import_contract=dict(room_origin=[0,0],sampling='nearest',mipmaps=False,draw_order=['backing','floor','structure','native actors and independent props sorted by feet y','foreground'],
                    collision='Use native_layouts walkable cells and the original object masks. PNG alpha is not collision.',
                    doors='Keep existing native door instances, transfer and save lifecycle. Do not infer extra entries from drawing.',
                    exterior='Independent architectural sprite. Door alignment and placement must be checked before enabling in N1; it is not baked into the yard preview.',
                    scale='1 image pixel = 1 room pixel; never auto-crop origin-bearing canvases'),
                  source_code_sha256=sha(ROOT/'src/EmbersAndOaths/NightRooms.cs'),
                  raw_sources={p.name:sha(p) for p in RAW.glob('*.png')},
                  crop_operations=CROPS,
                  limitations=['No game package changed.','Full inventory is not complete.','Generation master geometry was approximate; production floor and boundary layers are rebuilt from native rectangles.','Architecture placement and native dynamic lights require in-engine testing.'])
    (P/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (P/'preview-index.json').write_text(json.dumps(scene_previews,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'exported_pngs':len(MAN),'room_previews':len(scene_previews),'status':manifest['status']}))

if __name__=='__main__':main()
