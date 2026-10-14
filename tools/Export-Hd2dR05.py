"""Assemble all R05 scene views from painted sources and explicit proposed grids."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,copy,math,importlib.util
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R05-basin-v1'
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
    return (set(map(tuple,s['walkable_cells'])) if 'walkable_cells' in s else rc(s['walkable_rectangles']))-rc(s['blocked_rectangles'])
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
    materials=read('materials-manifest.json');sprites=read('sprite-manifest.json');assert len(sprites['assets'])==40;assets=copy.deepcopy(materials['assets']+sprites['assets']);ops=copy.deepcopy(materials['crop_operations']+sprites['crop_operations']);specs={s['id']:s for s in brief['sprites']};scenes=read('layouts.json');region=read('region-layout.json')
    colors=read('palettes/ash_r05_128.json')['colors'];rgb=[tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in colors]
    @lru_cache(None)
    def nearest(c):return min(rgb,key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    def quant(q):
        im=Image.new('RGBA',q.size);im.putdata([(*nearest(c[:3]),255) if c[3]>=128 else (0,0,0,0) for c in q.convert('RGBA').get_flattened_data()]);return im
    def save(q,ident,category='backgrounds',origin=(0,0),**meta):
        rel=f'assets/{category}/{ident}.png';q.save(P/rel);a=dict(id=ident,path=rel,size=list(q.size),origin=list(origin),palette='ASH-R05-128',sha256=sha(P/rel),runtime_verified=False,**meta);assets.append(a);return q
    def asset(ident,category='backgrounds'):return Image.open(P/f'assets/{category}/{ident}.png').convert('RGBA')
    def rawcrop(name,box,size):
        src=Image.open(P/'raw'/name).convert('RGBA');assert 0<=box[0]<box[2]<=src.width and 0<=box[1]<box[3]<=src.height
        ops.append(dict(source='raw/'+name,box=list(box),target_size=list(size),resample='nearest'));return quant(src.crop(box).resize(size,Image.Resampling.NEAREST))
    surfaces={k:asset(f'r05_{k}__material') for k in ['gravel','wetstone','boards','earth']}
    walls={k:save(rawcrop('r05-interiors-v1.png',box,(78,39)),f'r05_{k}__wall','items',role='unlit_vertical_wall_material_not_floor') for k,box in [('upper',(28,440,484,660)),('middle',(540,440,995,660)),('lower',(1050,440,1510,660))]}
    windows={k:save(rawcrop('r05-interiors-v1.png',box,(52,52)),f'r05_{k}__window','items',role='unlit_window_wall_patch_not_door') for k,box in [('upper',(179,78,329,273)),('middle',(680,78,844,273)),('lower',(1220,78,1377,225))]}
    walls['wood']=save(rawcrop('r05-architecture-v1.png',(268,336,447,388),(78,39)),'r05_wood__wall','items',role='unlit_vertical_wood_wall_from_own_care_lodge')
    windows['wood']=save(rawcrop('r05-architecture-v1.png',(184,331,260,403),(52,52)),'r05_wood__window','items',role='unlit_wood_window_from_own_care_lodge_not_door')
    water_surfaces={k:save(rawcrop('r05-water-v1.png',(i*512+12,12,(i+1)*512-12,1012),(312,312)),f'r05_{k}__water_material',role='nonwalkable_static_water_illustration_no_physics') for i,k in enumerate(['ordinary','foam','lowered'])}
    roofpolys={
      'r05_care_lodge':dict(polygons=[[(26,318),(73,171),(501,171),(541,315)],[(80,138),(118,138),(118,207),(80,207)]],holes=[]),
      'r05_ward_house':dict(polygons=[[(564,310),(603,171),(929,171),(924,321)],[(922,220),(1038,266),(1028,319),(923,287)],[(610,137),(652,137),(652,207),(610,207)]],holes=[]),
      'r05_well_drain_shed':dict(polygons=[[(1095,279),(1130,157),(1474,156),(1500,278),(1466,297),(1105,299)]],holes=[]),
      'r05_filter_well':dict(polygons=[[(79,717),(125,605),(325,605),(368,717)]],holes=[]),
      'r05_voluntary_hut':dict(polygons=[[(487,758),(577,593),(953,596),(1047,758)]],holes=[]),
      'r05_high_archive_shed':dict(polygons=[[(1148,718),(1192,616),(1428,617),(1467,716)]],holes=[])}
    archraw=Image.open(P/'raw/r05-architecture-v1.png');spriteops={o['id']:o for o in sprites['crop_operations']};(P/'guides/roofs').mkdir(exist_ok=True)
    for ident,shapes in roofpolys.items():
        op=spriteops[ident];full=asset(ident,'items');rm=Image.new('L',archraw.size);d=ImageDraw.Draw(rm)
        for poly in shapes['polygons']:d.polygon(poly,fill=255)
        for poly in shapes['holes']:d.polygon(poly,fill=0)
        fit=rm.crop(op['box']).crop(op['trim_bbox']).resize(tuple(op['fitted_size']),Image.Resampling.NEAREST);m=Image.new('L',full.size);m.paste(fit,tuple(op['offset']));m=ImageChops.multiply(m,full.getchannel('A'));m.save(P/f'guides/roofs/{ident}_mask.png')
        body=full.copy();roof=full.copy();body.putalpha(ImageChops.subtract(full.getchannel('A'),m));roof.putalpha(m)
        for part,q in [('body',body),('roof',roof)]:save(q,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,mask='guides/roofs/'+ident+'_mask.png')
        ops.append(dict(id=ident,operation='visually_selected_roof_polygons_with_front_gable_exclusions',source='raw/r05-architecture-v1.png',**shapes,mask='guides/roofs/'+ident+'_mask.png',source_crop_operation=op))
    for a in assets:
        if a.get('architecture'):a.update(roof_variants_pending=False,roof_variants={part:f'assets/items/{a["id"]}__{part}.png' for part in ['body','roof']})
    land=Image.open(P/'raw/r05-landscape-v1.png');lw,lh=land.width//2,land.height//2;landscapes=[rawcrop('r05-landscape-v1.png',(i%2*lw,i//2*lh,(i%2+1)*lw,(i//2+1)*lh),(1040,780)) for i in range(4)]
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);cs=cells(s);cm=mask(size,cs);indoor=s.get('interior',False);floor=repeat(surfaces['earth' if s['material']=='mud' else s['material']],size)
        if s.get('road_lines'):
            road=Image.new('L',size);d=ImageDraw.Draw(road)
            for line in s['road_lines']:d.line([tuple(v*26+13 for v in p) for p in line],fill=255,width=52)
            floor.paste(repeat(surfaces['gravel'],size),(0,0),road)
        floor.putalpha(cm);save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        if indoor:back=Image.new('RGBA',size,(*rgb[-1],255))
        else:
            index=0 if rid=='r05_reeds' else 2 if rid in ['r05_drain','r05_well','r05_ward'] else 1 if rid in ['r05_care','r05_road','r05_ward_exit'] else 3;back=landscapes[index].resize(size,Image.Resampling.NEAREST)
        save(back,rid+'__backing',role='nonwalkable_background',scene=rid);structure=Image.new('RGBA',size);front=Image.new('RGBA',size);kind='wood' if s['material']=='boards' else s.get('level','middle' if rid=='r05_ward_waste' else 'lower' if rid=='r05_ward_ritual' else 'upper');wall=walls[kind] if indoor else walls[kind].resize((78,9),Image.Resampling.NEAREST);height=wall.height
        for y in range(s['cells'][1]):
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):structure.alpha_composite(repeat(wall,((z-a+1)*26,height)),(a*26,y*26-height))
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):front.alpha_composite(repeat(wall.resize((78,8),Image.Resampling.NEAREST),((z-a+1)*26,8)),(a*26,(y+1)*26))
        if indoor:
            side=wall.resize((7,52),Image.Resampling.NEAREST)
            for x in range(s['cells'][0]):
                for step,off in [(-1,-7),(1,26)]:
                    for a,z in ranges([y for cx,y in cs if cx==x and (x+step,y) not in cs]):structure.alpha_composite(repeat(side,(7,(z-a+1)*26)),(x*26+off,a*26))
            wx=18 if 'walkable_cells' in s else 20 if rid=='r05_ward_main' else 6 if kind=='wood' else 8;wx=wx if any(x==wx for x,y in cs) else min(x for x,y in cs);top=min(y for x,y in cs if x==wx);pos=(wx*26,top*26-52);structure.alpha_composite(windows[kind],pos);s['window_wall_rect']=[*pos,52,52]
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
        save(structure,rid+'__structure',role='nonwalkable_boundary_and_window_architecture',scene=rid);save(front,rid+'__foreground',role='separate_front_edges',scene=rid);
        wc=set(map(tuple,s.get('water_cells',[])))|{(x,y) for a,b,c,d in s.get('water_rectangles',[]) for y in range(b,d+1) for x in range(a,c+1)};wc-=cs;wm=mask(size,wc);wkind='foam' if rid in ['r05_drain','r05_ward','r05_ward_exit','r05_well_lower'] else 'ordinary';water=repeat(water_surfaces[wkind],size);water.putalpha(wm);
        if wc:save(water,rid+'__water',role='nonwalkable_water_layer',scene=rid)
        plan=back.copy();plan.alpha_composite(water);plan.alpha_composite(floor);save(plan,rid+'__plan',role='flat_painted_plan',scene=rid)
        props=Image.new('RGBA',size);roofs=Image.new('RGBA',size)
        for o in sorted(s['objects'],key=lambda o:o['cell'][1]):
            ident=o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];pos=(x*26+13-ox,y*26+13-oy);props.alpha_composite(asset(ident+('__body' if ident in roofpolys else ''),'items'),pos)
            if ident in roofpolys:roofs.alpha_composite(asset(ident+'__roof','items'),pos)
        save(props,rid+'__props_preview',role='placement_preview_only_use_independent_sprites_in_game',scene=rid)
        if roofs.getchannel('A').getbbox():save(roofs,rid+'__roof',role='toggleable_roofs',scene=rid)
        env=back.copy()
        for q in [water,floor,structure,props,front]:env.alpha_composite(q)
        save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid);env.alpha_composite(roofs);save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
        s['illustration_variants']={}
        if s.get('illustrative_pipe_disconnect'):
            dp=Image.new('RGBA',size)
            for o in sorted(s['objects'],key=lambda o:o['cell'][1]):
                ident='r05_new_waste_pipe_capped' if o.get('pipe_variant') else o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];dp.alpha_composite(asset(ident+('__body' if ident in roofpolys else ''),'items'),(x*26+13-ox,y*26+13-oy))
            save(dp,rid+'__props_disconnected',role='graphics_only_new_pipe_disconnected_props_keep_living_pipe',scene=rid)
            de=back.copy()
            for q in [water,floor,structure,dp,front]:de.alpha_composite(q)
            save(de.copy(),rid+'__working_disconnected',role='graphics_only_pipe_variant_no_game_commit',scene=rid);de.alpha_composite(roofs);save(de,rid+'__environment_disconnected',role='graphics_only_pipe_variant_no_game_commit',scene=rid)
            s['illustration_variants']['pipe']=dict(props='assets/backgrounds/'+rid+'__props_disconnected.png',default=False,game_state_commit=False,floor_unchanged=True,living_water_unchanged=True)
        if 'walkable_cells' in s:
            lowwater=repeat(water_surfaces['lowered'],size);lowwater.putalpha(wm);save(lowwater,rid+'__water_lowered',role='graphics_only_lowered_water_same_nonwalkable_mask',scene=rid)
            lp=back.copy();lp.alpha_composite(lowwater);lp.alpha_composite(floor);save(lp,rid+'__plan_lowered',role='graphics_only_low_water_plan_no_added_path',scene=rid)
            le=back.copy()
            for q in [lowwater,floor,structure,props,front,roofs]:le.alpha_composite(q)
            save(le,rid+'__environment_lowered',role='graphics_only_low_water_composite_no_added_path',scene=rid)
            s['illustration_variants']['water']=dict(water='assets/backgrounds/'+rid+'__water_lowered.png',default=False,game_state_commit=False,floor_unchanged=True,automatic_timer=False)
    sheets={
      'r05_ward':dict(size=[1742,1482],parts=[['r05_ward_main',0,0],['r05_ward_waste',1170,0],['r05_ward_ritual',1170,546],['r05_ward_exit',0,910]],note='26pxoverlap only identical nonwalkable blank borders; all floor/props retained; 1:1segments'),
      'r05_well':dict(size=[2002,2002],parts=[['r05_well_upper',0,0],['r05_well_middle',1014,0],['r05_well_lower',0,1014]],note='Page1of2:three independent38x38rings,1:1; refuge/maintenance on annex_overview'),
      'r05_well_annex':dict(size=[2002,2002],parts=[['r05_well_research_refuge',130,182],['r05_well_workers_refuge',754,182],['r05_well_maintenance',507,780]],note='Page2of2:two distinct refuge rooms plus always-available maintenance,1:1; not merged into ring rooms')}
    for ident,sh in sheets.items():
        for suffix,source in [('plan_overview','plan'),('working_overview','environment')]:
            q=Image.new('RGBA',tuple(sh['size']),(*rgb[-1],255))
            for rid,x,y in sh['parts']:q.alpha_composite(asset(rid+'__'+source),(x,y))
            save(q,ident+'__'+suffix,role='multi_scene_contact_sheet_1_to_1_not_single_room',sheet_layout=sh)
    write('notes/assembly-supplement.json',dict(execution_lock_sha256=sha(P/'spec_lock.md'),room_dimensions_unchanged=True,overview_layouts=sheets,well_pages=2,reason='Six rooms cannot fit one2002square at1:1. Plural locked overviews resolved as2pages; no source lock or original canvas changed.'))
    src=Image.open(P/'raw/r05-region-v1.png');terrain=rawcrop('r05-region-v1.png',(0,0,src.width,src.height),tuple(region['size']));icons=Image.new('RGBA',terrain.size);iconmap={'care':'care_lodge','ward':'ward_house','well':'well_drain_shed','village':'filter_well','reeds':'reed_cluster','shelter':'voluntary_hut','drain':'low_gate','road':'warning_board'}
    for k,short in iconmap.items():
        ident='r05_'+short;q=asset(ident,'items');factor=min(156/q.width,130/q.height);fit=q.resize((round(q.width*factor),round(q.height*factor)),Image.Resampling.NEAREST);x,y=region['art_anchor_pixels']['R05-'+k];icons.alpha_composite(fit,(x-fit.width//2,y+35-round(specs[ident]['origin'][1]*factor)))
    save(terrain,'r05_region__terrain',role='regional_topology_terrain_not_native_world_grid');save(icons,'r05_region__nodes',role='schematic_icons_not_room_scale');terrain.alpha_composite(icons);save(terrain,'r05_region__plan',role='regional_connectivity_schematic_not_official_geography');terrain.save(P/'previews/r05_region.png')
    atlas=Image.new('RGBA',(1248,math.ceil(len(specs)/4)*286));frames=[]
    for i,ident in enumerate(specs):
        q=asset(ident,'items');x=(i%4)*312+(312-q.width)//2;y=(i//4)*286+(286-q.height)//2;atlas.alpha_composite(q,(x,y));frames.append(dict(id=ident,rect=[x,y,*q.size],origin=specs[ident]['origin'],atlas_origin=[x+specs[ident]['origin'][0],y+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/r05_buildings_props.png');write('sheets/manifest.json',dict(size=list(atlas.size),frames=frames,type='40static environment sprites, not animation'))
    write('layouts.json',scenes);write('manifest.json',dict(schema=1,batch=brief['batch'],status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,assets=assets,scenes=scenes,region=region,source_sha256=brief['source_sha256'],raw_sources={f.name:sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=ops,inventory_requests=brief['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,room_origin=[0,0],scale='1pixel=1room pixel; region icons/contact sheets explicitly separate',collision='Explicit proposed grids/occupancy, never PNG alpha',draw_order=['backing','nonwalkable water','floor','structure','foot-sorted independent bodies/props/actors','foreground','toggleable roofs'],states='Stopped historical apparatus, blank labels, no quest/permission/cure/fire outcome baked'),limitations=['All21scene grids are art proposals; native rooms,doors,collision,weather,lighting/save not tested.','Camp2/ward3/shelter1empty beds are finite visual placements, not actual occupancy/capacity/consent.','Pipe and water toggles are illustrative static art only; no challenge,time,quest,result,water purity or rescue state changes.','Water hazard also requires engine text and interaction; muted glyphs/foam never substitute causality.','Raw AI spacing/dimensions differ; documented crop/NN/palette normalization delivers exactproduction dimensions and origins.','Two2002square well overview pages retain1:1three levels,distinct refuge rooms and maintenance; never one walkable room.','R05topology is Mod-original schematic only.','No NPC art/dialogue/logic or game data modified.']))
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(assets),sprites=len(specs),view_slots=len(brief['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
