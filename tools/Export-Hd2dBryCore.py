"""Assemble all BRY scene views from painted sources and explicit proposed grids."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,copy,math,importlib.util
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-core-v1'
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
    materials=read('materials-manifest.json');sprites=read('sprite-manifest.json');assert len(sprites['assets'])==40;assets=copy.deepcopy(materials['assets']+sprites['assets']);ops=copy.deepcopy(materials['crop_operations']+sprites['crop_operations']);specs={s['id']:s for s in brief['sprites']};scenes=read('layouts.json');region=read('region-layout.json')
    colors=read('palettes/bry_core_128.json')['colors'];rgb=[tuple(int(c[i:i+2],16) for i in (1,3,5)) for c in colors]
    @lru_cache(None)
    def nearest(c):return min(rgb,key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    def quant(q):
        im=Image.new('RGBA',q.size);im.putdata([(*nearest(c[:3]),255) if c[3]>=128 else (0,0,0,0) for c in q.convert('RGBA').get_flattened_data()]);return im
    def save(q,ident,category='backgrounds',origin=(0,0),**meta):
        rel=f'assets/{category}/{ident}.png';q.save(P/rel);a=dict(id=ident,path=rel,size=list(q.size),origin=list(origin),palette='BRY-CORE-128',sha256=sha(P/rel),runtime_verified=False,**meta);assets.append(a);return q
    def asset(ident,category='backgrounds'):return Image.open(P/f'assets/{category}/{ident}.png').convert('RGBA')
    def rawcrop(name,box,size):
        src=Image.open(P/'raw'/name).convert('RGBA');assert 0<=box[0]<box[2]<=src.width and 0<=box[1]<box[3]<=src.height
        ops.append(dict(source='raw/'+name,box=list(box),target_size=list(size),resample='nearest'));return quant(src.crop(box).resize(size,Image.Resampling.NEAREST))
    surfaces={k:asset(f'bry_{k}__material') for k in ['paving','stone','boards','earth']}
    walls={k:save(rawcrop('bry-interiors-v1.png',box,(78,39)),f'bry_{k}__wall','items',role='unlit_vertical_wall_not_floor') for k,box in [('stone',(25,430,490,650)),('wood',(540,440,992,650)),('plaster',(1050,400,1510,600))]}
    windows={k:save(rawcrop('bry-interiors-v1.png',box,(52,52)),f'bry_{k}__window','items',role='unlit_window_patch_not_door') for k,box in [('stone',(160,110,351,348)),('wood',(682,100,857,340)),('plaster',(1190,103,1380,340))]}
    roofpolys={
      'bry_print_arcade':dict(polygons=[[(33,326),(83,264),(399,264),(452,347),(106,350)],[(84,245),(115,245),(115,280),(84,280)]],holes=[[(38,326),(82,281),(119,326)]]),
      'bry_rental_block':dict(polygons=[[(514,235),(563,173),(615,220),(551,276)],[(582,241),(600,212),(747,212),(753,264)],[(720,238),(759,172),(851,258),(790,277)],[(477,330),(527,286),(547,308),(496,349)]],holes=[[(551,260),(588,222),(632,268)],[(760,230),(800,197),(838,268)]]),
      'bry_rope_shed':dict(polygons=[[(898,334),(940,259),(1128,260),(1192,347),(1000,359)]],holes=[[(903,331),(940,277),(988,337)]]),
      'bry_berth_canopy':dict(polygons=[[(1260,303),(1435,292),(1501,337),(1323,367)]],holes=[]),
      'bry_workshop_house':dict(polygons=[[(22,724),(79,653),(380,654),(440,740),(113,746)],[(112,623),(146,623),(146,662),(112,662)]],holes=[[(25,720),(76,668),(116,729)]]),
      'bry_water_observation_house':dict(polygons=[[(471,728),(513,665),(699,668),(751,753),(557,759)],[(532,648),(566,648),(566,685),(532,685)]],holes=[[(476,728),(516,683),(552,731)]]),
      'bry_gate_house':dict(polygons=[[(779,746),(834,681),(1028,687),(1080,750),(833,756)]],holes=[]),
      'bry_neutral_meeting_hall':dict(polygons=[[(1104,720),(1150,646),(1458,638),(1522,731),(1190,750)],[(1158,591),(1197,591),(1197,660),(1158,660)]],holes=[[(1107,715),(1148,667),(1190,730)]])}
    archraw=Image.open(P/'raw/bry-architecture-v1.png');spriteops={o['id']:o for o in sprites['crop_operations']};(P/'guides/roofs').mkdir(exist_ok=True)
    for ident,shapes in roofpolys.items():
        op=spriteops[ident];full=asset(ident,'items');rm=Image.new('L',archraw.size);d=ImageDraw.Draw(rm)
        for poly in shapes['polygons']:d.polygon(poly,fill=255)
        for poly in shapes['holes']:d.polygon(poly,fill=0)
        fit=rm.crop(op['box']).crop(op['trim_bbox']).resize(tuple(op['fitted_size']),Image.Resampling.NEAREST);m=Image.new('L',full.size);m.paste(fit,tuple(op['offset']));m=ImageChops.multiply(m,full.getchannel('A'));m.save(P/f'guides/roofs/{ident}_mask.png')
        body=full.copy();roof=full.copy();body.putalpha(ImageChops.subtract(full.getchannel('A'),m));roof.putalpha(m)
        for part,q in [('body',body),('roof',roof)]:save(q,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,mask='guides/roofs/'+ident+'_mask.png')
        ops.append(dict(id=ident,operation='visually_selected_roof_polygons_with_front_gable_exclusions',source='raw/bry-architecture-v1.png',**shapes,mask='guides/roofs/'+ident+'_mask.png',source_crop_operation=op))
    for a in assets:
        if a.get('architecture'):a.update(roof_variants_pending=False,roof_variants={part:f'assets/items/{a["id"]}__{part}.png' for part in ['body','roof']})
    land=Image.open(P/'raw/bry-landscape-v1.png');lw,lh=land.width//2,land.height//2;landscapes=[rawcrop('bry-landscape-v1.png',(i%2*lw,i//2*lh,(i%2+1)*lw,(i//2+1)*lh),(1040,780)) for i in range(4)]
    def boundaries(scene,cs,cm,indoor):
        rid=scene['id'];size=tuple(scene['size']);structure=Image.new('RGBA',size);front=Image.new('RGBA',size);kind='plaster' if rid in ['bry_d04_b','bry_d06_b'] else 'wood' if scene['material']=='boards' else 'stone';height=78 if rid=='bry_d02_b' else 39 if indoor else 9;wall=walls[kind].resize((78,height),Image.Resampling.NEAREST)
        for y in range(scene['cells'][1]):
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):structure.alpha_composite(repeat(wall,((z-a+1)*26,height)),(a*26,y*26-height))
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):front.alpha_composite(repeat(wall.resize((78,8),Image.Resampling.NEAREST),((z-a+1)*26,8)),(a*26,(y+1)*26))
        if indoor:
            side=wall.resize((7,52),Image.Resampling.NEAREST)
            for x in range(scene['cells'][0]):
                for step,off in [(-1,-7),(1,26)]:
                    for a,z in ranges([y for cx,y in cs if cx==x and (x+step,y) not in cs]):structure.alpha_composite(repeat(side,(7,(z-a+1)*26)),(x*26+off,a*26))
            wx=14 if rid=='bry_d02_b' else 6 if kind=='wood' else 8;top=min(y for x,y in cs if x==wx);pos=(wx*26,top*26-52);structure.alpha_composite(windows[kind],pos);scene['window_wall_rect']=[*pos,52,52]
        scene['wall_decal_rects']=[]
        for decal in scene.get('wall_decals',[]):
            x,y=decal['cell'];q=asset(decal['id'],'items');ox=specs[decal['id']]['origin'][0];pos=(x*26+13-ox,y*26-q.height);structure.alpha_composite(q,pos);scene['wall_decal_rects'].append(dict(id=decal['id'],rect=[*pos,*q.size]))
        for a,b,c,d in scene.get('waterline_wall_rects',[]):
            pts=[(x*26+2,b*26-13+((x-a)%2)*2) for x in range(a,c+2)];ImageDraw.Draw(structure).line(pts,fill=(*rgb[48],255),width=2)
        scene['door_clear_boxes']=[]
        for e in scene['exits']:
            x,y=e['cell'];boxes=[]
            if (x-1,y) not in cs:boxes.append([x*26-13,y*26,x*26-1,y*26+25])
            if (x+1,y) not in cs:boxes.append([(x+1)*26,y*26,(x+1)*26+12,y*26+25])
            if (x,y-1) not in cs:boxes.append([x*26,y*26-height,x*26+25,y*26-1])
            if (x,y+1) not in cs:boxes.append([x*26,(y+1)*26,x*26+25,(y+1)*26+height-1])
            for r in boxes:
                for q in [structure,front]:ImageDraw.Draw(q).rectangle(r,fill=(0,0,0,0))
                scene['door_clear_boxes'].append(dict(exit=e['id'],rect=r))
        for q in [structure,front]:q.putalpha(ImageChops.multiply(q.getchannel('A'),ImageChops.invert(cm)))
        return structure,front
    pathreport=[]
    for scene in scenes:
        rid=scene['id'];size=tuple(scene['size']);cs=cells(scene);cm=mask(size,cs);cm.save(P/f'guides/{rid}_walkable.png');indoor=scene.get('interior',False);floor=repeat(surfaces[scene['material']],size);floor.putalpha(cm);save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        back=Image.new('RGBA',size,(*rgb[-1],255)) if indoor else landscapes[1 if rid in ['bry_d03','bry_d05','bry_d03_b'] else 0 if rid in ['bry_d01','bry_d02','bry_d04'] else 2].resize(size,Image.Resampling.NEAREST);save(back,rid+'__backing',role='nonwalkable_background',scene=rid)
        wc={(x,y) for a,b,c,d in scene.get('water_rectangles',[]) for y in range(b,d+1) for x in range(a,c+1)}-cs;wm=mask(size,wc);water=repeat(landscapes[3].resize((312,312),Image.Resampling.NEAREST),size);water.putalpha(wm)
        if wc:save(water,rid+'__water',role='nonwalkable_calm_water_layer',scene=rid)
        structure,front=boundaries(scene,cs,cm,indoor);save(structure,rid+'__structure',role='nonwalkable_boundary_and_window_architecture',scene=rid);save(front,rid+'__foreground',role='separate_front_edges',scene=rid)
        blueprint=Image.new('RGBA',size);bd=ImageDraw.Draw(blueprint)
        if not indoor:
            for a,b,c,d in scene['blocked_rectangles']:bd.rectangle((a*26,b*26,(c+1)*26-1,(d+1)*26-1),fill=(*rgb[59],255),outline=(*rgb[31],255),width=2)
        if blueprint.getchannel('A').getbbox():save(blueprint,rid+'__plan_structure',role='flat_block_footprint_diagram_only',scene=rid)
        markings=Image.new('RGBA',size);md=ImageDraw.Draw(markings)
        for a,b,c,d in scene.get('public_stair_rectangles',[]):
            for y in range(b*26,(d+1)*26,8):md.line([(a*26,y),((c+1)*26-1,y)],fill=(*rgb[27],255),width=2)
        if markings.getchannel('A').getbbox():save(markings,rid+'__stair_markings',role='public_stair_ground_illustration_no_upper_room_claim',scene=rid)
        plan=back.copy()
        for q in [water,floor,blueprint,markings]:plan.alpha_composite(q)
        save(plan,rid+'__plan',role='flat_painted_plan',scene=rid)
        props=Image.new('RGBA',size);roofs=Image.new('RGBA',size)
        base_objects=sorted([o for o in scene['objects'] if not o.get('surface_attachment')],key=lambda o:o['cell'][1]);ordered=[]
        for host in base_objects:
            ordered.append(host);ordered.extend(o for o in scene['objects'] if o.get('draw_after_instance')==host['instance_id'])
        assert len(ordered)==len(scene['objects']),rid+' attachment target'
        for o in ordered:
            ident=o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];pos=(x*26+13-ox,y*26+13-oy);props.alpha_composite(asset(ident+('__body' if ident in roofpolys else ''),'items'),pos)
            if ident in roofpolys:roofs.alpha_composite(asset(ident+'__roof','items'),pos)
        save(props,rid+'__props_preview',role='placement_preview_only_use_independent_sprites_in_game',scene=rid)
        if roofs.getchannel('A').getbbox():save(roofs,rid+'__roof',role='toggleable_roofs',scene=rid)
        env=back.copy()
        for q in [water,floor,markings,structure,props,front]:env.alpha_composite(q)
        save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid);env.alpha_composite(roofs);save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
        scene['illustration_variants']={}
        if scene.get('high_tide_illustration'):
            low={(x,y) for a,b,c,d in scene['low_walk_closed_rectangles'] for y in range(b,d+1) for x in range(a,c+1)};hc=cs-low;hm=mask(size,hc);hf=repeat(surfaces[scene['material']],size);hf.putalpha(hm);hw=water.copy();hw.putalpha(mask(size,wc|low));hs=copy.deepcopy(scene);hst,hfront=boundaries(hs,hc,hm,indoor)
            for suffix,q,role in [('high_tide_floor',hf,'illustrative_high_tide_candidate_floor'),('high_tide_water',hw,'illustrative_high_tide_water'),('high_tide_structure',hst,'illustrative_high_tide_matching_boundaries'),('high_tide_foreground',hfront,'illustrative_high_tide_matching_front_edges')]:save(q,rid+'__'+suffix,role=role,scene=rid)
            he=back.copy()
            for q in [hw,hf,markings,hst,props,hfront,roofs]:he.alpha_composite(q)
            save(he,rid+'__environment_high_tide',role='illustrative_high_tide_no_game_commit',scene=rid);hp=back.copy()
            for q in [hw,hf,blueprint,markings]:hp.alpha_composite(q)
            save(hp,rid+'__plan_high_tide',role='illustrative_high_tide_candidate_plan',scene=rid);scene['high_tide_walkable_cells']=[list(v) for v in sorted(hc)];scene['high_tide_door_clear_boxes']=hs['door_clear_boxes'];scene['illustration_variants']['tide']=dict(default=False,game_state_commit=False,candidate_walkable_cells='high_tide_walkable_cells',native_collision_unverified=True)
        if scene.get('model_demo_only'):
            demo=Image.new('RGBA',size);dd=ImageDraw.Draw(demo);o=next(o for o in scene['objects'] if o['id']=='bry_drain_sand_model');ox,oy=specs[o['id']]['origin'];x,y=o['cell'];px,py=x*26+13-ox,y*26+13-oy
            for bx,by in [(45,36),(88,49)]:dd.rectangle((px+bx,py+by,px+bx+9,py+by+5),fill=(*rgb[37],255),outline=(*rgb[18],255),width=1)
            save(demo,rid+'__model_demo',role='separate_dry_model_stop_piece_diagram_no_real_water',scene=rid);scene['illustration_variants']['model']=dict(default=False,game_state_commit=False,floor_unchanged=True,real_water_unchanged=True)
        pathreport.append(dict(scene=rid,walkable_cells=len(cs)))
    write('layout-validation.json',dict(passed=True,post_crop_geometry_calibrated=True,paths=pathreport,scope='Authored terrain grids only; native object collisions,doors/stair elevation not measured',runtime_verified=False))
    src=Image.open(P/'raw/bry-city-v1.png');terrain=rawcrop('bry-city-v1.png',(0,0,src.width,src.height),tuple(region['size']));icons=Image.new('RGBA',terrain.size);iconmap={'D01':'print_arcade','D02':'rental_block','D03':'rope_shed','D04':'workshop_house','D05':'gate_house','D06':'neutral_meeting_hall'}
    for k,short in iconmap.items():
        ident='bry_'+short;q=asset(ident,'items');factor=min(156/q.width,130/q.height);fit=q.resize((round(q.width*factor),round(q.height*factor)),Image.Resampling.NEAREST);x,y=region['art_anchor_pixels']['BRY-'+k];icons.alpha_composite(fit,(x-fit.width//2,y+35-round(specs[ident]['origin'][1]*factor)))
    save(terrain,'bry_city__terrain',role='regional_topology_terrain_not_native_world_grid');save(icons,'bry_city__nodes',role='schematic_icons_not_room_scale');terrain.alpha_composite(icons);save(terrain,'bry_city__plan',role='regional_connectivity_schematic_not_official_geography');terrain.save(P/'previews/bry_city.png')
    atlas=Image.new('RGBA',(1560,math.ceil(len(specs)/4)*338));frames=[]
    for i,ident in enumerate(specs):
        q=asset(ident,'items');x=(i%4)*390+(390-q.width)//2;y=(i//4)*338+(338-q.height)//2;atlas.alpha_composite(q,(x,y));frames.append(dict(id=ident,rect=[x,y,*q.size],origin=specs[ident]['origin'],atlas_origin=[x+specs[ident]['origin'][0],y+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/bry_buildings_props.png');write('sheets/manifest.json',dict(size=list(atlas.size),frames=frames,type='40static environment sprites, not animation'))
    write('layouts.json',scenes);write('manifest.json',dict(schema=1,batch=brief['batch'],status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,assets=assets,scenes=scenes,region=region,source_sha256=brief['source_sha256'],raw_sources={f.name:sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=ops,inventory_requests=brief['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,room_origin=[0,0],scale='1pixel=1room pixel; region icons/contact sheets explicitly separate',collision='Explicit proposed grids/occupancy, never PNG alpha',draw_order=['backing', 'nonwalkable water', 'floor', 'public stair ground markings', 'structure and wall decals', 'foot-sorted independent bodies/props/actors; surface attachments immediately after host', 'foreground', 'toggleable roofs', 'optional model diagram overlay'],states='Unlit apparatus, blank labels, no quest/permission/cure/fire outcome baked; illustrative tides/model are default-off and do not commit game state'),limitations=['All18scaled art grids are authored proposals; native rooms,door indices,object collision,stair elevation/save/weather/lighting untested.','Six task-space nodes reference four original areas,not six official quarters; no bank/nationalaccess claim.','Each A/Broom has separate candidate street returns; privacy,account denial and refusal do not lock publicroute.','High-tide illustration changes candidate lowwalk floor/water/boundaries only; highreturn remains; no nativephysics/time/quest/save commit.','Sandmodel is dry with neutral gray tray lining; diagram pieces only,no real sluice opening/waterdamage/consent.','Three shorttables/emptycenter and three separately controlled unlitlamps; no emptyseat as agreement.','Two abstract soot trace decals on rear masonry are environmentmarks,not NPC/body images or ownership/death verdicts.','Rawactual spacing/dimensions recorded; productioncanvases/origins exact bycrop/NN/palette/binaryalpha.','Blueprint block shapes and publicstair lines are art diagrams,never derived native collision from alpha.','No NPC/dialogue/GML/game data modified.','Satellites and sixcontinuation spaces remain pending in745view scope.']))
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(assets),sprites=len(specs),view_slots=len(brief['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
