"""Assemble all R06 scene views from painted sources and explicit proposed grids."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,copy,math,importlib.util
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R06-highland-v1'
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
    materials=read('materials-manifest.json');sprites=read('sprite-manifest.json');assert len(sprites['assets'])==38;assets=copy.deepcopy(materials['assets']+sprites['assets']);ops=copy.deepcopy(materials['crop_operations']+sprites['crop_operations']);specs={s['id']:s for s in brief['sprites']};scenes=read('layouts.json');region=read('region-layout.json')
    colors=read('palettes/hig_r06_128.json')['colors'];rgb=[tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in colors]
    @lru_cache(None)
    def nearest(c):return min(rgb[:120],key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    def quant(q):
        im=Image.new('RGBA',q.size);im.putdata([(*nearest(c[:3]),255) if c[3]>=128 else (0,0,0,0) for c in q.convert('RGBA').get_flattened_data()]);return im
    def save(q,ident,category='backgrounds',origin=(0,0),**meta):
        rel=f'assets/{category}/{ident}.png';q.save(P/rel);a=dict(id=ident,path=rel,size=list(q.size),origin=list(origin),palette='HIG-R06-128',sha256=sha(P/rel),runtime_verified=False,**meta);assets.append(a);return q
    def asset(ident,category='backgrounds'):return Image.open(P/f'assets/{category}/{ident}.png').convert('RGBA')
    def rawcrop(name,box,size):
        src=Image.open(P/'raw'/name).convert('RGBA');assert 0<=box[0]<box[2]<=src.width and 0<=box[1]<box[3]<=src.height
        ops.append(dict(source='raw/'+name,box=list(box),target_size=list(size),resample='nearest'));return quant(src.crop(box).resize(size,Image.Resampling.NEAREST))
    surfaces={k:asset(f'r06_{k}__material') for k in ['paving','stone','boards','earth']}
    walls={k:save(rawcrop('r06-interiors-v1.png',box,(78,39)),f'r06_{k}__wall','items',role='unlit_vertical_wall_not_floor') for k,box in [('stone',(28,440,482,660)),('wood',(540,440,993,660)),('rough',(1050,440,1510,660))]}
    windows={k:save(rawcrop('r06-interiors-v1.png',box,(52,52)),f'r06_{k}__window','items',role='unlit_window_patch_not_door') for k,box in [('stone',(160,108,355,325)),('wood',(674,108,869,326)),('rough',(1190,110,1385,297))]}
    roofpolys={
      'r06_bell_station':dict(polygons=[[(30,333),(184,182),(431,182),(510,307),(368,338)],[(48,138),(146,69),(194,117),(143,150),(99,129)]],holes=[[(372,330),(430,202),(493,310)]]),
      'r06_echo_gatehouse':dict(polygons=[[(586,245),(679,135),(802,140),(987,259),(948,272),(809,265),(775,233)]],holes=[[(599,240),(679,153),(789,240)]]),
      'r06_residual_well_house':dict(polygons=[[(1043,310),(1221,177),(1341,177),(1508,286),(1423,320),(1133,315)]],holes=[]),
      'r06_maintenance_shed':dict(polygons=[[(44,735),(134,617),(408,637),(489,730),(432,764),(111,746)]],holes=[[(391,731),(409,650),(470,731)]]),
      'r06_trial_canopy':dict(polygons=[[(578,676),(676,613),(950,655),(879,753),(583,716)]],holes=[]),
      'r06_station_table_canopy':dict(polygons=[[(1038,713),(1153,610),(1344,625),(1492,717),(1247,741),(1040,720)]],holes=[[(1048,698),(1153,627),(1229,698)]])}
    archraw=Image.open(P/'raw/r06-architecture-v1.png');spriteops={o['id']:o for o in sprites['crop_operations']};(P/'guides/roofs').mkdir(exist_ok=True)
    for ident,shapes in roofpolys.items():
        op=spriteops[ident];full=asset(ident,'items');rm=Image.new('L',archraw.size);d=ImageDraw.Draw(rm)
        for poly in shapes['polygons']:d.polygon(poly,fill=255)
        for poly in shapes['holes']:d.polygon(poly,fill=0)
        fit=rm.crop(op['box']).crop(op['trim_bbox']).resize(tuple(op['fitted_size']),Image.Resampling.NEAREST);m=Image.new('L',full.size);m.paste(fit,tuple(op['offset']));m=ImageChops.multiply(m,full.getchannel('A'));m.save(P/f'guides/roofs/{ident}_mask.png')
        body=full.copy();roof=full.copy();body.putalpha(ImageChops.subtract(full.getchannel('A'),m));roof.putalpha(m)
        for part,q in [('body',body),('roof',roof)]:save(q,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,mask='guides/roofs/'+ident+'_mask.png')
        ops.append(dict(id=ident,operation='visually_selected_roof_polygons_with_front_gable_exclusions',source='raw/r06-architecture-v1.png',**shapes,mask='guides/roofs/'+ident+'_mask.png',source_crop_operation=op))
    for a in assets:
        if a.get('architecture'):a.update(roof_variants_pending=False,roof_variants={part:f'assets/items/{a["id"]}__{part}.png' for part in ['body','roof']})
    land=Image.open(P/'raw/r06-landscape-v1.png');lw,lh=land.width//2,land.height//2;landscapes=[rawcrop('r06-landscape-v1.png',(i%2*lw,i//2*lh,(i%2+1)*lw,(i//2+1)*lh),(1040,780)) for i in range(4)]
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);cs=cells(s);cm=mask(size,cs);indoor=s.get('interior',False);floor=repeat(surfaces[s['material']],size)
        if s.get('road_lines'):
            road=Image.new('L',size);d=ImageDraw.Draw(road)
            for line in s['road_lines']:d.line([tuple(v*26+13 for v in p) for p in line],fill=255,width=52)
            floor.paste(repeat(surfaces['paving'],size),(0,0),road)
        floor.putalpha(cm);save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        if indoor:back=Image.new('RGBA',size,(*rgb[119],255))
        else:
            index=0 if rid in ['r06_slope','r06_echo','r06_residual'] else 2 if rid=='r06_seal' else 1;back=landscapes[index].resize(size,Image.Resampling.NEAREST)
        save(back,rid+'__backing',role='nonwalkable_background',scene=rid);structure=Image.new('RGBA',size);front=Image.new('RGBA',size);kind='wood' if s['material']=='boards' else 'rough' if rid in ['r06_residual_main','r06_residual_maintenance'] else 'stone';wall=walls[kind] if indoor else walls[kind].resize((78,9),Image.Resampling.NEAREST);height=wall.height
        for y in range(s['cells'][1]):
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):structure.alpha_composite(repeat(wall,((z-a+1)*26,height)),(a*26,y*26-height))
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):front.alpha_composite(repeat(wall.resize((78,8),Image.Resampling.NEAREST),((z-a+1)*26,8)),(a*26,(y+1)*26))
        if indoor:
            side=wall.resize((7,52),Image.Resampling.NEAREST)
            for x in range(s['cells'][0]):
                for step,off in [(-1,-7),(1,26)]:
                    for a,z in ranges([y for cx,y in cs if cx==x and (x+step,y) not in cs]):structure.alpha_composite(repeat(side,(7,(z-a+1)*26)),(x*26+off,a*26))
            wx=23 if rid=='r06_residual_main' else 6 if kind=='wood' else 8;top=min(y for x,y in cs if x==wx);pos=(wx*26,top*26-52);structure.alpha_composite(windows[kind],pos);s['window_wall_rect']=[*pos,52,52]
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
        wm=mask(size,{(x,y) for a,b,c,d in s.get('water_rectangles',[]) for y in range(b,d+1) for x in range(a,c+1)}-cs);water=repeat(landscapes[3].resize((312,312),Image.Resampling.NEAREST),size);water.putalpha(wm)
        if wm.getbbox():save(water,rid+'__water',role='nonwalkable_calm_water',scene=rid)
        markings=Image.new('RGBA',size);md=ImageDraw.Draw(markings)
        for a,b,c,d in s.get('safety_line_rectangles',[]):md.rectangle((a*26+3,b*26+3,(c+1)*26-4,(d+1)*26-4),outline=(*rgb[0],255),width=2)
        if markings.getchannel('A').getbbox():save(markings,rid+'__safety_markings',role='neutral_safety_white_line_not_verification_result',scene=rid)
        plan=back.copy()
        for q in [water,floor,markings]:plan.alpha_composite(q)
        save(plan,rid+'__plan',role='flat_painted_plan',scene=rid)
        props=Image.new('RGBA',size);roofs=Image.new('RGBA',size)
        for o in sorted(s['objects'],key=lambda o:o['cell'][1]):
            ident=o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];pos=(x*26+13-ox,y*26+13-oy);props.alpha_composite(asset(ident+('__body' if ident in roofpolys else ''),'items'),pos)
            if ident in roofpolys:roofs.alpha_composite(asset(ident+'__roof','items'),pos)
        save(props,rid+'__props_preview',role='placement_preview_only_use_independent_sprites_in_game',scene=rid)
        if roofs.getchannel('A').getbbox():save(roofs,rid+'__roof',role='toggleable_roofs',scene=rid)
        env=back.copy()
        for q in [water,floor,structure,markings,props,front]:env.alpha_composite(q)
        save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid);env.alpha_composite(roofs);save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
        s['illustration_variants']={}
        if s.get('illustrative_coupling_disconnect'):
            alt=Image.new('RGBA',size)
            for o in sorted(s['objects'],key=lambda o:o['cell'][1]):
                ident='r06_aux_coupling_capped' if o.get('coupling_variant') else o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];alt.alpha_composite(asset(ident+('__body' if ident in roofpolys else ''),'items'),(x*26+13-ox,y*26+13-oy))
            save(alt,rid+'__props_disconnected',role='graphics_only_coupling_replacement_keep_other_props',scene=rid);ae=back.copy()
            for q in [water,floor,structure,markings,alt,front]:ae.alpha_composite(q)
            save(ae.copy(),rid+'__working_disconnected',role='graphics_only_coupling_illustration_no_game_commit',scene=rid);ae.alpha_composite(roofs);save(ae,rid+'__environment_disconnected',role='graphics_only_coupling_illustration_no_game_commit',scene=rid)
            s['illustration_variants']['coupling']=dict(props='assets/backgrounds/'+rid+'__props_disconnected.png',default=False,game_state_commit=False,floor_unchanged=True)
        if s.get('pre_warning_rectangles'):
            warning=Image.new('RGBA',size);wd=ImageDraw.Draw(warning)
            for a,b,c,d in s['pre_warning_rectangles']:
                wd.rectangle((a*26+3,b*26+3,(c+1)*26-4,(d+1)*26-4),outline=(*rgb[120],255),width=3)
                for x in range(a*26+4,(c+1)*26-4,26):wd.line([(x,b*26+5),(x+6,b*26+11)],fill=(*rgb[120],255),width=2)
            warning.putalpha(ImageChops.multiply(warning.getchannel('A'),cm));save(warning,rid+'__pre_warning',role='proposed_warning_shape_only_not_active_battle_or_damage',scene=rid);s['illustration_variants']['warning']=dict(overlay='assets/backgrounds/'+rid+'__pre_warning.png',default=False,game_state_commit=False,floor_unchanged=True)
    sheetlayouts={
      'r06_echo':dict(size=[1092,1534],parts=[['r06_echo_front',0,0],['r06_echo_maintenance',0,806]],note='Two1:1rooms; front and exterior maintenance,not one room'),
      'r06_residual':dict(size=[2262,1690],parts=[['r06_residual_main',0,0],['r06_residual_maintenance',1274,0],['r06_residual_safe',0,1066]],note='Three1:1rooms; double-ring,safe table,maintenance,not one room')}
    for ident,sh in sheetlayouts.items():
        for suffix,source in [('plan_overview','plan'),('working_overview','environment')]:
            q=Image.new('RGBA',tuple(sh['size']),(*rgb[-9],255))
            for rid,x,y in sh['parts']:q.alpha_composite(asset(rid+'__'+source),(x,y))
            save(q,ident+'__'+suffix,role='multi_room_contact_sheet_1_to_1',sheet_layout=sh)
    # Neutral hand-authored pixel glyphs are separate engine controls, never quest state.
    for i,key in enumerate(brief['hand_pixel_icons']):
        q=Image.new('RGBA',(26,26));d=ImageDraw.Draw(q);dark=(*rgb[109],255);light=(*rgb[0],255);metal=(*rgb[21],255);d.rectangle((2,2,23,23),fill=dark,outline=metal,width=1)
        if key=='cooling':d.line([(7,6),(7,18),(13,18),(13,8),(18,8),(18,19)],fill=light,width=2)
        elif key=='return_valve':d.ellipse((7,6,19,18),outline=light,width=2);d.line([(13,7),(13,21)],fill=metal,width=2)
        elif key=='residual_response':d.arc((6,6,20,20),180,360,fill=light,width=2);d.line([(13,12),(13,20)],fill=metal,width=2);d.rectangle((11,19,15,21),fill=(*rgb[121],255))
        elif key=='isolation':d.rectangle((6,7,19,19),outline=light,width=2);d.line([(13,5),(13,21)],fill=metal,width=2)
        elif key=='bypass':d.line([(6,18),(6,8),(19,8),(19,18)],fill=light,width=2);d.line([(10,18),(15,18)],fill=metal,width=2)
        elif key=='closed_waste':d.rectangle((6,10,20,20),outline=light,width=2);d.rectangle((5,6,21,9),fill=metal)
        elif key=='coupling':d.rectangle((5,10,10,17),outline=light,width=2);d.rectangle((16,10,21,17),outline=light,width=2)
        else:d.rectangle((7,6,19,20),outline=light,width=2);d.rectangle((10,9,16,16),outline=metal,width=1)
        save(q,'r06_icon_'+key,'ui',(13,13),role='hand_pixel_neutral_engine_control_glyph_no_state',created_by='integer pixel drawing, not AI sprite edit')
    src=Image.open(P/'raw/r06-region-v1.png');terrain=rawcrop('r06-region-v1.png',(0,0,src.width,src.height),tuple(region['size']));icons=Image.new('RGBA',terrain.size);iconmap={'station':'bell_station','echo':'echo_gatehouse','residual':'residual_well_house','sign':'return_board','shed':'maintenance_shed','trial':'trial_canopy','table':'station_table_canopy','seal':'blank_seal_plate','drain':'maintenance_valve','slope':'rope_pulley'}
    for k,short in iconmap.items():
        ident='r06_'+short;q=asset(ident,'items');factor=min(156/q.width,130/q.height);fit=q.resize((round(q.width*factor),round(q.height*factor)),Image.Resampling.NEAREST);x,y=region['art_anchor_pixels']['R06-'+k];icons.alpha_composite(fit,(x-fit.width//2,y+35-round(specs[ident]['origin'][1]*factor)))
    save(terrain,'r06_region__terrain',role='regional_topology_terrain_not_native_world_grid');save(icons,'r06_region__nodes',role='schematic_icons_not_room_scale');terrain.alpha_composite(icons);save(terrain,'r06_region__plan',role='regional_connectivity_schematic_not_official_geography');terrain.save(P/'previews/r06_region.png')
    atlas=Image.new('RGBA',(1248,math.ceil(len(specs)/4)*286));frames=[]
    for i,ident in enumerate(specs):
        q=asset(ident,'items');x=(i%4)*312+(312-q.width)//2;y=(i//4)*286+(286-q.height)//2;atlas.alpha_composite(q,(x,y));frames.append(dict(id=ident,rect=[x,y,*q.size],origin=specs[ident]['origin'],atlas_origin=[x+specs[ident]['origin'][0],y+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/r06_buildings_props.png');write('sheets/manifest.json',dict(size=list(atlas.size),frames=frames,type='38static environment sprites, not animation'))
    write('layouts.json',scenes);write('manifest.json',dict(schema=1,batch=brief['batch'],status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,assets=assets,scenes=scenes,region=region,source_sha256=brief['source_sha256'],raw_sources={f.name:sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=ops,inventory_requests=brief['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,room_origin=[0,0],scale='1pixel=1room pixel; region icons/contact sheets explicitly separate',collision='Explicit proposed grids/occupancy, never PNG alpha',draw_order=['backing','nonwalkable water','floor','structure','foot-sorted independent bodies/props/actors','foreground','toggleable roofs'],states='Stopped historical apparatus, blank labels, no quest/permission/cure/fire outcome baked'),limitations=['All18grids are art proposals; native rooms,doors,collision,save,lights/weather untested.','D09three blank measurements and independent exterior controls/return; no NE5/readings/outcomes baked.','D10empty carrier slot,side ledger,three staggeredcouplings; actor rescue/boss anchors separate; no NPC art or actual combat test.','Coupling and warning toggles illustrate graphics only,not game states/physics/ending freeze.','Safe station supplies/ordinaryreturns not politicalchoice or new restcapacity; inventory/authorization engine-owned.','Eight26pixel hand glyphs separate engine controls; no automatic state machine.','Raw actualspacing/dimensions recorded; exact productiondimensions/origins bycrop/NN/palette/binaryalpha.','HIGregional128palette reserves8violetcolors only for limitedmedium/warning,glyphs; ordinarymaterials use120basecolors.','R06regional topology Mod-original schematic only.','No NPC/dialogue/game data modified.']))
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(assets),sprites=len(specs),view_slots=len(brief['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
