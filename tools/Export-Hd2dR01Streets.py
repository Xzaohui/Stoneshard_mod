"""Generate scene import layers from AI masters under the Pixel Asset Master lock."""
from pathlib import Path
from functools import lru_cache
import importlib.util,json
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-streets-v1'
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
H=module('r01_painted_helpers',ROOT/'tools/Export-Hd2dR01.py');H.P=P
def repeat_paint(tile,size):
    # Do not mirror textured material: reflected weeds and cobbles can form
    # false object/face silhouettes. Keep the painter's original orientation.
    out=Image.new('RGBA',size)
    for row,y in enumerate(range(0,size[1],tile.height)):
        shift=(row%3)*tile.width//3
        for x in range(-shift,size[0],tile.width):out.alpha_composite(tile,(x,y))
    return out
H.fill=repeat_paint
def main():
    H.ASSETS.clear();H.OPS.clear()
    scenes=H.read('layouts.json');brief=H.read('brief.json');region=H.read('region-layout.json')
    specs={s['id']:s for s in brief['sprites']}
    mats={
      'r01_port':('r01-port-v1.png',(180,348,1210,725),(780,286)),
      'r01_hearing':('r01-hearing-v1.png',(203,408,1196,705),(702,210)),
      'r01_workshop':('r01-workshop-v1.png',(508,321,1120,524),(624,208)),
      'r01_salt':('r01-salt-v1.png',(670,546,1195,842),(520,293)),
      'r01_rental':('r01-rental-v1.png',(248,388,1110,826),(468,238))}
    wall=('r01-hearing-v1.png',(426,53,640,80))
    earth=H.sample('r01-salt-v1.png',(570,500,900,710),(312,198))
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);mask=Image.open(P/f'guides/{rid}_walkable.png').convert('L');cs=H.cells(s)
        floor=H.fill(H.sample(*mats[rid]),size)
        if rid=='r01_salt':
            rm=Image.new('L',size);ImageDraw.Draw(rm).line([(39,481),(338,481),(520,390),(760,265),(1001,221)],fill=255,width=78)
            road=H.fill(H.sample('r01-salt-v1.png',(305,364,665,494),(286,103)),size)
            floor.paste(road,(0,0),rm)
            H.OPS.append(dict(operation='authored_dry_road_material_mask',points=[[39,481],[338,481],[520,390],[760,265],[1001,221]],width=78))
        floor.putalpha(mask);H.save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        back=H.fill(earth,size) if rid!='r01_rental' else Image.new('RGBA',size,'#0F1218')
        wm=Image.new('L',size);wd=ImageDraw.Draw(wm)
        if rid in ['r01_port','r01_hearing','r01_workshop']:wd.rectangle((0,676,size[0],size[1]),fill=255)
        if rid=='r01_salt':wd.rectangle((0,572,234,780),fill=255)
        wm=ImageChops.multiply(wm,ImageChops.invert(mask))
        if wm.getbbox():back.paste(H.water_plate(size),(0,0),wm)
        # Every foundation is dry; generated guide pools are discarded.
        for a,b,c,d in s['blocked_rectangles']:
            if rid!='r01_salt':back.alpha_composite(H.fill(earth,((c-a+1)*26,(d-b+1)*26)),(a*26,b*26))
        H.save(back,rid+'__backing',role='blocked_background',scene=rid)
        structure=Image.new('RGBA',size);fore=Image.new('RGBA',size)
        wall_h=39 if rid=='r01_rental' else 13
        if rid=='r01_rental':fn,box='r01-rental-v1.png',(276,185,455,277)
        else:fn,box=wall
        if rid!='r01_salt':
            for y in range(s['cells'][1]):
                for a,b in H.ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):
                    structure.alpha_composite(H.fill(H.sample(fn,box,(156,wall_h)),((b-a+1)*26,wall_h)),(a*26,y*26-wall_h))
                for a,b in H.ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):
                    fore.alpha_composite(H.fill(H.sample(fn,box,(156,13)),((b-a+1)*26,13)),(a*26,(y+1)*26))
            for x in range(s['cells'][0]):
                for side,offset in [(-1,-7),(1,26)]:
                    for a,b in H.ranges([y for cx,y in cs if cx==x and (x+side,y) not in cs]):
                        structure.alpha_composite(H.fill(H.sample(fn,box,(7,52)),(7,(b-a+1)*26)),(x*26+offset,a*26))
        else:
            rock=H.sample('r01-salt-v1.png',(1111,0,1408,132),(208,78));structure.alpha_composite(rock,(806,26))
        s['door_clear_boxes']=[]
        for e in s['exits']:
            x,y=e['cell'];boxes=[]
            if (x-1,y) not in cs:boxes.append([x*26-13,y*26,x*26-1,(y+1)*26-1])
            if (x+1,y) not in cs:boxes.append([(x+1)*26,y*26,(x+1)*26+12,(y+1)*26-1])
            if (x,y-1) not in cs:boxes.append([x*26,y*26-wall_h,(x+1)*26-1,y*26-1])
            if (x,y+1) not in cs:boxes.append([x*26,(y+1)*26,(x+1)*26-1,(y+1)*26+wall_h-1])
            for box in boxes:
                for im in [structure,fore]:ImageDraw.Draw(im).rectangle(box,fill=(0,0,0,0))
                s['door_clear_boxes'].append(dict(exit=e['id'],rect=box))
        for im in [structure,fore]:im.putalpha(ImageChops.multiply(im.getchannel('A'),ImageChops.invert(mask)))
        H.save(structure,rid+'__structure',role='nonwalkable_boundary_architecture',scene=rid)
        H.save(fore,rid+'__foreground',role='separate_front_edges',scene=rid)
        H.save(Image.alpha_composite(back,floor),rid+'__plan',role='flat_painted_plan',scene=rid)
    arch=[('r01_port_kiosk',(0,0,512,512)),('r01_hearing_canopy',(512,0,1024,512)),('r01_rental_house',(1024,0,1536,512)),('r01_forge_building',(0,512,512,1024)),('r01_abandoned_post',(512,512,1024,1024))]
    for ident,box in arch:H.sprite(ident,'r01-architecture-v1.png',box,specs[ident])
    prop_ids=['r01_notice_board','r01_twin_ledger_table','r01_stamp_bench','r01_basic_repair_bench','r01_storage_chest','r01_drying_rack','r01_ash_stove','r01_water_basin']
    ps=H.raw('r01-props-v1.png');xs=[round(i*ps.width/3) for i in range(4)];ys=[round(i*ps.height/3) for i in range(4)]
    for i,ident in enumerate(prop_ids):
        x=i%3;y=i//3;H.sprite(ident,'r01-props-v1.png',(xs[x],ys[y],xs[x+1],ys[y+1]),specs[ident])
    # The regional master is a map diagram. Its actual painted pads define
    # display anchors only, never player/world positions.
    region['art_anchor_pixels']={k:[round(x*1664/1448),round(y*1248/1086)] for k,x,y in [
      ('R01-salt',180,675),('R01-port',450,675),('R01-camp',454,245),('R01-canal',857,164),('R01-workshop',1180,255),('R01-hearing',954,496)]}
    region['display_anchor_authority']='Visually reviewed painted master pads; no native world grid coordinates'
    terrain=H.sample('r01-region-v1.png',(0,0,1448,1086),(1664,1248))
    H.save(terrain,'r01_region__terrain',role='regional_schematic_terrain_not_walkable_room')
    finalizer=H.module('pam_streets_finalize',H.SKILL/'scripts/finalize_assets.py');orig=finalizer._find_nearest
    @lru_cache(maxsize=250000)
    def nearest(r,g,b,pal):return orig(r,g,b,pal)
    finalizer._find_nearest=lambda r,g,b,pal:nearest(r,g,b,tuple(pal))
    finalizer.cmd_quantize(P);finalizer.cmd_clean(P)
    cuts={'r01_port_kiosk':91,'r01_hearing_canopy':104,'r01_rental_house':127,'r01_forge_building':131,'r01_abandoned_post':66}
    for ident,cut in cuts.items():
        im=H.asset(ident,'items');roof=im.copy();body=im.copy();ra=im.getchannel('A');ba=im.getchannel('A')
        ImageDraw.Draw(ra).rectangle((0,cut,im.width,im.height),fill=0);ImageDraw.Draw(ba).rectangle((0,0,im.width,cut-1),fill=0)
        roof.putalpha(ra);body.putalpha(ba)
        for part,q in [('roof',roof),('body',body)]:H.save(q,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,split_at_y=cut)
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);props=Image.new('RGBA',size);roofs=Image.new('RGBA',size)
        for o in sorted(s['objects'],key=lambda o:o['cell'][1]):
            ident=o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];pos=(x*26+13-ox,y*26+13-oy)
            props.alpha_composite(H.asset(ident+('__body' if ident in cuts else ''),'items'),pos)
            if ident in cuts:roofs.alpha_composite(H.asset(ident+'__roof','items'),pos)
        H.save(props,rid+'__props_preview',role='placement_preview_only_use_individual_sprites_for_game',scene=rid)
        env=H.asset(rid+'__backing')
        for part in ['floor','structure','props_preview','foreground']:env.alpha_composite(H.asset(rid+'__'+part))
        if roofs.getchannel('A').getbbox():
            H.save(roofs,rid+'__roof',role='independent_toggleable_roofs',scene=rid)
            H.save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid);env.alpha_composite(roofs)
        elif rid=='r01_rental':H.save(env.copy(),rid+'__working_space',role='private_working_space_composite',scene=rid)
        H.save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
    icons=Image.new('RGBA',(1664,1248))
    map_sprites={'R01-port':'r01_port_kiosk','R01-hearing':'r01_hearing_canopy','R01-workshop':'r01_forge_building'}
    for key,ident in map_sprites.items():
        im=H.asset(ident,'items');q=im.resize((im.width//2,im.height//2),Image.Resampling.NEAREST);x,y=region['art_anchor_pixels'][key]
        icons.alpha_composite(q,(x-q.width//2,y+45-specs[ident]['origin'][1]//2))
    for key,fn in [('R01-camp','reuse-r01-worker-shed.png'),('R01-canal','reuse-r01-canal-entry.png')]:
        im=H.raw(fn);q=H.sample(fn,(0,0,im.width,im.height),(im.width//2,im.height//2));x,y=region['art_anchor_pixels'][key]
        icons.alpha_composite(q,(x-q.width//2,y+45-q.height+9))
    # Salt road remains an unbuilt road node. Its dry site pad is visual context.
    H.save(icons,'r01_region__nodes',role='regional_schematic_building_icons_not_room_scale')
    regional=H.asset('r01_region__terrain');regional.alpha_composite(icons);H.save(regional,'r01_region__plan',role='regional_topology_schematic_not_native_world_map');regional.save(P/'previews/r01_region.png')
    H.write('region-layout.json',region)
    atlas=Image.new('RGBA',(936,1300));frames=[]
    for i,ident in enumerate(specs):
        im=H.asset(ident,'items');tx=(i%3)*312+(312-im.width)//2;ty=(i//3)*260+(260-im.height)//2;atlas.alpha_composite(im,(tx,ty))
        frames.append(dict(id=ident,rect=[tx,ty,*im.size],sprite_origin=specs[ident]['origin'],atlas_origin=[tx+specs[ident]['origin'][0],ty+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/r01_streets_architecture_props.png');H.write('sheets/manifest.json',dict(type='13 individual static environment sprites, not animation',size=list(atlas.size),frames=frames))
    for a in H.ASSETS:a.update(sha256=H.sha(P/a['path']),palette='BRY-R01-128',runtime_verified=False)
    manifest=dict(schema=1,batch='R01-streets-v1',status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,
      assets=H.ASSETS,scenes=scenes,region=region,source_sha256=brief['source_sha256'],raw_sources={f.name:H.sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=H.OPS,
      inventory_requests=brief['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,scale='1 image pixel = 1 room pixel except regional schematic icons',room_origin=[0,0],
      draw_order=['backing','floor','structure','independent body/props and native actors at foot depth','foreground','roof (toggleable)'],
      collision='layouts.json explicit proposed cells; use native engine collision after integration testing, never art alpha',npc='Only empty reservations; NPC work belongs to other model',lighting='Unlit materials, sources handled independently'),
      limitations=['Scene geometry proposal, not implemented native rooms.','Public working spaces and rental are visual/collision proposals, native portals and authorization pending.',
      'Regional artwork is schematic; it does not register world cells or claim official geography.','No narrative outcome, text, inventory, NPC or light state baked into art.'])
    H.write('manifest.json',manifest)
    prefix='src/Art/hd2d_26x26_20261013/batches/R01-streets-v1/'
    records=[]
    for ident,guide in [('r01-port-v1','r01_port_generation_v1'),('r01-hearing-v1','r01_hearing_generation_v1'),('r01-workshop-v1','r01_workshop_generation_v1'),('r01-salt-v1','r01_salt_geometry'),('r01-rental-v1','r01_rental_generation_v1'),('r01-architecture-v1',None),('r01-props-v1',None),('r01-region-v1','r01_region_geometry')]:
        inputs=[prefix+'guides/'+guide+'.png','design/12_美术参考/城市概念/BRY-概念-v1.png'] if guide else []
        prompt=f'notes/prompt-{ident}.txt';output=f'raw/{ident}.png'
        records.append(dict(id=ident,method='built-in image_gen',selected=True,prompt=prompt,prompt_sha256=H.sha(P/prompt),inputs=[dict(path=p,sha256=H.sha(ROOT/p)) for p in inputs],output=output,output_sha256=H.sha(P/output),original_size=list(Image.open(P/output).size),spec_lock_sha256=H.sha(P/'spec_lock.md'),postprocess='manifest crop_operations; requested skill quantize/clean; binary alpha and nearest sampling'))
    reuses=[dict(path=src,batch_copy='raw/'+dst,sha256=H.sha(P/'raw'/dst)) for src,dst in [
      ('src/Art/hd2d_26x26_20261013/raw/n1-water-v1.png','reuse-n1-water.png'),
      ('src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v1/assets/items/r01_worker_shed.png','reuse-r01-worker-shed.png'),
      ('src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v1/assets/items/r01_canal_entry.png','reuse-r01-canal-entry.png')]]
    H.write('generation-log.json',dict(skill_commit='33d891c421a9ad3608f5a09af97271388ca923af',generation_count=len(records),records=records,reuse_sources=reuses,
      input_note='Original generation guides archived before production body occupancy refinements. Port original guide had teal footprints; export replaces both with dry ground. Raw props master1254x1254 normalized into specified independent canvases. Material crops repeat in their original orientation with staggered rows; no mirrored grass/cobble silhouettes.'))
    H.write('preview-index.json',[dict(id=s['id'],name=s['name_zh'],size=s['size'],layers=[a for a in H.ASSETS if a.get('scene')==s['id']]) for s in scenes])
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(H.ASSETS),independent_sprites=len(specs),inventory_slots=len(brief['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
