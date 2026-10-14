"""Assemble all R04 scene views from painted sources and explicit proposed grids."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,copy,math,importlib.util
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R04-pass-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def repeat(t,size):
    q=Image.new('RGBA',size)
    for y in range(0,size[1],t.height):
        for x in range(0,size[0],t.width):q.alpha_composite(t,(x,y))
    return q
def cells(s):
    def rc(rs):return {(x,y) for a,b,c,d in rs for y in range(b,d+1) for x in range(a,c+1)}
    return rc(s['walkable_rectangles'])-rc(s['blocked_rectangles'])
def mask(size,cs):
    q=Image.new('L',size);d=ImageDraw.Draw(q)
    for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
    return q
def ranges(values):
    rs=[]
    for x in sorted(values):
        if not rs or x>rs[-1][1]+1:rs.append([x,x])
        else:rs[-1][1]=x
    return rs
def main():
    brief=read('brief.json');assert all(sha(ROOT/n)==h for n,h in brief['source_sha256'].items());assert read('materials-validation.json')['passed'] and read('sprites-validation.json')['passed']
    materials=read('materials-manifest.json');sprites=read('sprite-manifest.json');assert len(sprites['assets'])==29;assets=copy.deepcopy(materials['assets']+sprites['assets']);ops=copy.deepcopy(materials['crop_operations']+sprites['crop_operations']);specs={s['id']:s for s in brief['sprites']};scenes=read('layouts.json');region=read('region-layout.json')
    colors=read('palettes/pas_r04_128.json')['colors'];rgb=[tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in colors]
    @lru_cache(None)
    def nearest(c):return min(rgb,key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    def quant(q):
        im=Image.new('RGBA',q.size);im.putdata([(*nearest(c[:3]),255) if c[3]>=128 else (0,0,0,0) for c in q.convert('RGBA').get_flattened_data()]);return im
    def save(q,ident,category='backgrounds',origin=(0,0),**meta):
        rel=f'assets/{category}/{ident}.png';q.save(P/rel);a=dict(id=ident,path=rel,size=list(q.size),origin=list(origin),palette='PAS-R04-128',sha256=sha(P/rel),runtime_verified=False,**meta);assets.append(a);return q
    def asset(ident,category='backgrounds'):return Image.open(P/f'assets/{category}/{ident}.png').convert('RGBA')
    def rawcrop(name,box,size):
        src=Image.open(P/'raw'/name).convert('RGBA');assert 0<=box[0]<box[2]<=src.width and 0<=box[1]<box[3]<=src.height
        ops.append(dict(source='raw/'+name,box=list(box),target_size=list(size),resample='nearest'));return quant(src.crop(box).resize(size,Image.Resampling.NEAREST))
    surfaces={k:asset(f'r04_{k}__material') for k in ['cobble','brick','boards','earth']}
    walls={k:save(rawcrop('r04-interiors-v1.png',box,(78,39)),f'r04_{k}__wall','items',role='unlit_vertical_wall_material_not_floor') for k,box in [('stone',(30,420,430,550)),('wood',(560,420,960,550)),('brick',(1045,420,1490,550))]}
    windows={k:save(rawcrop('r04-interiors-v1.png',box,(52,52)),f'r04_{k}__window','items',role='unlit_window_wall_patch_not_door') for k,box in [('stone',(110,65,305,275)),('wood',(630,65,810,275)),('brick',(1120,65,1305,275))]}
    # Roof masks are selected against the unchanged raw architecture, including the inn porch.
    roofpolys={
      'r04_neutral_inn':dict(polygons=[[(48,240),(100,112),(382,112),(451,237),(397,247),(65,247)],[(150,334),(300,334),(302,368),(160,383)]],holes=[[(115,235),(162,181),(212,235)],[(264,235),(302,181),(352,235)]]),
      'r04_store_house':dict(polygons=[[(552,309),(590,188),(971,188),(1006,308)]],holes=[]),
      'r04_mason_shed':dict(polygons=[[(1074,294),(1166,216),(1484,303),(1400,352),(1097,327)]],holes=[]),
      'r04_windbreak':dict(polygons=[[(77,803),(137,700),(386,700),(446,778),(393,799)]],holes=[]),
      'r04_drug_pavilion':dict(polygons=[[(519,744),(605,647),(958,647),(1012,735),(965,747)]],holes=[]),
      'r04_seal_shelter':dict(polygons=[[(1113,807),(1189,709),(1442,708),(1467,790),(1380,812)]],holes=[])}
    archraw=Image.open(P/'raw/r04-architecture-v1.png');spriteops={o['id']:o for o in sprites['crop_operations']};(P/'guides/roofs').mkdir(exist_ok=True)
    for ident,shapes in roofpolys.items():
        op=spriteops[ident];full=asset(ident,'items');rm=Image.new('L',archraw.size);d=ImageDraw.Draw(rm)
        for poly in shapes['polygons']:d.polygon(poly,fill=255)
        for poly in shapes['holes']:d.polygon(poly,fill=0)
        fit=rm.crop(op['box']).crop(op['trim_bbox']).resize(tuple(op['fitted_size']),Image.Resampling.NEAREST);m=Image.new('L',full.size);m.paste(fit,tuple(op['offset']));m=ImageChops.multiply(m,full.getchannel('A'));m.save(P/f'guides/roofs/{ident}_mask.png')
        body=full.copy();roof=full.copy();body.putalpha(ImageChops.subtract(full.getchannel('A'),m));roof.putalpha(m)
        for part,q in [('body',body),('roof',roof)]:save(q,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,mask='guides/roofs/'+ident+'_mask.png')
        ops.append(dict(id=ident,operation='visually_selected_roof_polygons_with_front_gable_exclusions',source='raw/r04-architecture-v1.png',**shapes,mask='guides/roofs/'+ident+'_mask.png',source_crop_operation=op))
    for a in assets:
        if a.get('architecture'):a.update(roof_variants_pending=False,roof_variants={part:f'assets/items/{a["id"]}__{part}.png' for part in ['body','roof']})
    land=Image.open(P/'raw/r04-landscape-v1.png');lw,lh=land.width//2,land.height//2;landscapes=[rawcrop('r04-landscape-v1.png',(i%2*lw,i//2*lh,(i%2+1)*lw,(i//2+1)*lh),(1040,780)) for i in range(4)]
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);cs=cells(s);cm=mask(size,cs);indoor=s.get('interior',False);floor=repeat(surfaces[s['material']],size)
        if s.get('road_lines'):
            road=Image.new('L',size);d=ImageDraw.Draw(road)
            for line in s['road_lines']:d.line([tuple(v*26+13 for v in p) for p in line],fill=255,width=52)
            floor.paste(repeat(surfaces['cobble'],size),(0,0),road)
        floor.putalpha(cm);save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        if indoor:back=Image.new('RGBA',size,(*rgb[-1],255))
        else:
            index=1 if rid in ['r04_cellar','r04_mason','r04_scale','r04_seal'] else 3 if rid=='r04_camp' else 2 if rid in ['r04_drug','r04_cart'] else 0;back=landscapes[index].resize(size,Image.Resampling.NEAREST)
        save(back,rid+'__backing',role='nonwalkable_background',scene=rid);structure=Image.new('RGBA',size);front=Image.new('RGBA',size);kind='wood' if s['material']=='boards' else 'brick' if indoor else 'stone';wall=walls[kind] if indoor else walls[kind].resize((78,9),Image.Resampling.NEAREST);height=wall.height
        for y in range(s['cells'][1]):
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):structure.alpha_composite(repeat(wall,((z-a+1)*26,height)),(a*26,y*26-height))
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):front.alpha_composite(repeat(wall.resize((78,8),Image.Resampling.NEAREST),((z-a+1)*26,8)),(a*26,(y+1)*26))
        if indoor:
            side=wall.resize((7,52),Image.Resampling.NEAREST)
            for x in range(s['cells'][0]):
                for step,off in [(-1,-7),(1,26)]:
                    for a,z in ranges([y for cx,y in cs if cx==x and (x+step,y) not in cs]):structure.alpha_composite(repeat(side,(7,(z-a+1)*26)),(x*26+off,a*26))
            wx=20 if rid=='r04_cellar_main' else 6 if kind=='wood' else 8;top=min(y for x,y in cs if x==wx);pos=(wx*26,top*26-52);structure.alpha_composite(windows[kind],pos);s['window_wall_rect']=[*pos,52,52]
        s['door_clear_boxes']=[]
        for e in s['exits']:
            x,y=e['cell'];boxes=[]
            if (x-1,y) not in cs:boxes.append([x*26-13,y*26,x*26-1,y*26+25])
            if (x+1,y) not in cs:boxes.append([(x+1)*26,y*26,(x+1)*26+12,y*26+25])
            if (x,y-1) not in cs:boxes.append([x*26,y*26-height,x*26+25,y*26-1])
            if (x,y+1) not in cs:boxes.append([x*26,(y+1)*26,x*26+25,(y+1)*26+height-1])
            for r in boxes:
                for q in [structure,front]:ImageDraw.Draw(q).rectangle(r,fill=(0,0,0,0))
                s['door_clear_boxes'].append(dict(exit=e['id'],rect=r))
        for q in [structure,front]:q.putalpha(ImageChops.multiply(q.getchannel('A'),ImageChops.invert(cm)))
        save(structure,rid+'__structure',role='nonwalkable_boundary_and_window_architecture',scene=rid);save(front,rid+'__foreground',role='separate_front_edges',scene=rid);save(Image.alpha_composite(back,floor),rid+'__plan',role='flat_painted_plan',scene=rid)
        props=Image.new('RGBA',size);roofs=Image.new('RGBA',size)
        for o in sorted(s['objects'],key=lambda o:o['cell'][1]):
            ident=o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];pos=(x*26+13-ox,y*26+13-oy);props.alpha_composite(asset(ident+('__body' if ident in roofpolys else ''),'items'),pos)
            if ident in roofpolys:roofs.alpha_composite(asset(ident+'__roof','items'),pos)
        save(props,rid+'__props_preview',role='placement_preview_only_use_independent_sprites_in_game',scene=rid)
        if roofs.getchannel('A').getbbox():save(roofs,rid+'__roof',role='toggleable_roofs',scene=rid)
        env=back.copy()
        for q in [floor,structure,props,front]:env.alpha_composite(q)
        save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid);env.alpha_composite(roofs);save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
    # Multi-space dungeon sheets retain1:1scale and are not a single walkable room.
    plans=Image.new('RGBA',(1664,1326),(*rgb[-1],255));plans.alpha_composite(asset('r04_cellar_main__plan'),(0,0));plans.alpha_composite(asset('r04_cellar_damaged__plan'),(1066,0));plans.alpha_composite(asset('r04_cellar_oil__plan'),(1066,494));plans.alpha_composite(asset('r04_cellar_ditch__plan'),(0,858));save(plans,'r04_cellar__plan_overview',role='four_scene_contact_sheet_1_to_1_not_single_room')
    work=Image.new('RGBA',(1664,1326),(*rgb[-1],255));work.alpha_composite(asset('r04_cellar_main__environment'),(0,0));work.alpha_composite(asset('r04_cellar_damaged__environment'),(1066,0));work.alpha_composite(asset('r04_cellar_oil__environment'),(1066,494));work.alpha_composite(asset('r04_cellar_ditch__environment'),(0,858));save(work,'r04_cellar__working_overview',role='four_scene_contact_sheet_1_to_1_not_single_room')
    src=Image.open(P/'raw/r04-region-v1.png');terrain=rawcrop('r04-region-v1.png',(0,0,src.width,src.height),tuple(region['size']));icons=Image.new('RGBA',terrain.size);iconmap={'inn':'neutral_inn','cellar':'store_house','scale':'beam_scale','mason':'mason_shed','cart':'broken_cart','camp':'windbreak','drug':'drug_pavilion','market':'public_table','seal':'seal_shelter','bypass':'blank_notice'}
    for k,short in iconmap.items():
        ident='r04_'+short;q=asset(ident,'items');factor=min(156/q.width,130/q.height);fit=q.resize((round(q.width*factor),round(q.height*factor)),Image.Resampling.NEAREST);x,y=region['art_anchor_pixels']['R04-'+k];icons.alpha_composite(fit,(x-fit.width//2,y+35-round(specs[ident]['origin'][1]*factor)))
    save(terrain,'r04_region__terrain',role='regional_topology_terrain_not_native_world_grid');save(icons,'r04_region__nodes',role='schematic_icons_not_room_scale');terrain.alpha_composite(icons);save(terrain,'r04_region__plan',role='regional_connectivity_schematic_not_official_geography');terrain.save(P/'previews/r04_region.png')
    atlas=Image.new('RGBA',(1248,math.ceil(len(specs)/4)*286));frames=[]
    for i,ident in enumerate(specs):
        q=asset(ident,'items');x=(i%4)*312+(312-q.width)//2;y=(i//4)*286+(286-q.height)//2;atlas.alpha_composite(q,(x,y));frames.append(dict(id=ident,rect=[x,y,*q.size],origin=specs[ident]['origin'],atlas_origin=[x+specs[ident]['origin'][0],y+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/r04_buildings_props.png');write('sheets/manifest.json',dict(size=list(atlas.size),frames=frames,type='29static environment sprites, not animation'))
    write('layouts.json',scenes);write('manifest.json',dict(schema=1,batch=brief['batch'],status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,assets=assets,scenes=scenes,region=region,source_sha256=brief['source_sha256'],raw_sources={f.name:sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=ops,inventory_requests=brief['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,room_origin=[0,0],scale='1pixel=1room pixel; region icons/contact sheets explicitly separate',collision='Explicit proposed grids/occupancy, never PNG alpha',draw_order=['backing','floor','structure','foot-sorted independent bodies/props/actors','foreground','toggleable roofs'],states='Stopped historical apparatus, blank labels, no quest/permission/cure/fire outcome baked'),limitations=['All16scene grids are authored proposals; native rooms,doors,collision,weather,lighting and save not tested.','Inn care proposes one empty bed and two bowls, not confirmed lodging capacity or new patient entitlement.','Oil hazard is independent and optional; literal warning text/native fire simulation are not embedded.','Raw AI dimensions/spacing may differ from request; documented crops/NN normalization deliver exact production canvases and origins.','R04topology is Mod-original schematic geography only.','No NPC art/dialogue/logic or game data modified.']))
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(assets),sprites=len(specs),view_slots=len(brief['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
