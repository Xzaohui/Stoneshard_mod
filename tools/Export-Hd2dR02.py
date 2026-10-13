"""R02 scene compositor: authored cell masks, AI-painted components, exact skill palette."""
from pathlib import Path
from functools import lru_cache
import importlib.util,json
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R02-river-v1'
def module(n,p):
    spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
H=module('r02_paint_helpers',ROOT/'tools/Export-Hd2dR01.py');H.P=P
G=module('r02_cell_geometry',ROOT/'tools/Prepare-Hd2dR02.py')
MACROS={}
def repeat(tile,size):
    q=Image.new('RGBA',size)
    for y in range(0,size[1],tile.height):
        for x in range(0,size[0],tile.width):q.alpha_composite(tile,(x,y))
    return q
H.fill=repeat
def gridmask(size,cs):
    q=Image.new('L',size);d=ImageDraw.Draw(q)
    for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
    return q
def paste_rect(q,paint,rect):
    a,b,c,d=rect;m=Image.new('L',q.size);ImageDraw.Draw(m).rectangle((a*26,b*26,(c+1)*26-1,(d+1)*26-1),fill=255);q.paste(paint,(0,0),m)
def terrain(cs,size,tiles):
    if id(tiles) in MACROS:
        q=repeat(MACROS[id(tiles)],size);q.putalpha(gridmask(size,cs));return q
    q=Image.new('RGBA',size)
    for x,y in sorted(cs):q.alpha_composite(tiles[(x%3)+(y%3)*3],(x*26,y*26))
    return q
def main():
    H.ASSETS.clear();H.OPS.clear();MACROS.clear();scenes=H.read('layouts.json');b=H.read('brief.json');r=H.read('region-layout.json');specs={s['id']:s for s in b['sprites']}
    # Input geometry for well generation predates the normalized well-body block.
    well=next(s for s in scenes if s['id']=='r02_well');old=dict(well);old['blocked_rectangles']=[v for v in well['blocked_rectangles'] if v!=[16,8,18,9]]
    gm=gridmask(tuple(old['size']),G.cells(old));guide=Image.new('RGB',tuple(old['size']),'#20363A');guide.paste('#A29474',(0,0),gm);d=ImageDraw.Draw(guide)
    for a1,b1,c1,d1 in old['blocked_rectangles']:d.rectangle((a1*26,b1*26,(c1+1)*26-1,(d1+1)*26-1),fill='#4C3C2F')
    guide.save(P/'guides/r02_well_generation_v1.png')
    tile_sets={};ms=H.raw('r02-materials-v1.png');cw=ms.width//2;ch=ms.height//2
    for i,key in enumerate(['gravel','grass','boards','wetstone']):
        x=(i%2)*cw;y=(i//2)*ch;plate=H.sample('r02-materials-v1.png',(x+24,y+24,x+cw-24,y+ch-24),(312,312))
        ts=[plate.crop((j%3*26+104,j//3*26+104,j%3*26+130,j//3*26+130)) for j in range(9)]
        horizontal=[ts[0].getpixel((v,0)) for v in range(26)];vertical=[ts[0].getpixel((0,v)) for v in range(26)];corner=horizontal[0];horizontal[-1]=corner;vertical[0]=vertical[-1]=corner
        for j,t in enumerate(ts):
            for v in range(26):t.putpixel((v,0),horizontal[v]);t.putpixel((v,25),horizontal[v]);t.putpixel((0,v),vertical[v]);t.putpixel((25,v),vertical[v])
            H.save(t,f'r02_{key}_v{j}','tiles',role='flat_edge_matched_material_variant',material=key,variant=j)
        tile_sets[key]=ts
        macro=plate.copy()
        for v in range(312):macro.putpixel((v,311),macro.getpixel((v,0)));macro.putpixel((311,v),macro.getpixel((0,v)))
        MACROS[id(ts)]=macro
        H.OPS.append(dict(operation='macro_surface_wrap_border_copy',material=key,size=[312,312],border=1,role='Scene PNG surface paint; optional26pxvariation tiles exported separately'))
        H.OPS.append(dict(operation='tile_border_copy_before_quantization',material=key,tiles=9,size=[26,26],border=1,orientation='no mirrors or rotations',contract='Shared top/bottom profile and shared left/right profile across all9variants; not a boundary autotile'))
    arch=[('r02_ferry_inn',(0,0,700,560)),('r02_tax_house',(704,0,1136,560)),('r02_filter_shelter',(1148,0,1536,560)),('r02_repair_canopy',(0,562,634,1024)),('r02_inspection_shed',(650,562,1130,1024)),('r02_bridge_pier',(1180,562,1536,1024))]
    for ident,box in arch:H.sprite(ident,'r02-architecture-v1.png',box,specs[ident])
    props=['r02_public_table','r02_privacy_screen','r02_case_cabinet','r02_name_cabinet','r02_filter_rack','r02_sample_bucket','r02_mooring_post','r02_crate_corner','r02_repair_timbers','r02_soup_stove','r02_road_sign','r02_inspection_table']
    raw=H.raw('r02-props-v1.png')
    boxes=[(0,0,432,362),(435,0,754,362),(780,0,1126,362),(1155,0,1448,362),
           (0,365,425,730),(490,365,720,730),(805,365,1095,730),(1110,365,1448,730),
           (0,732,432,1086),(446,732,765,1086),(790,732,1082,1086),(1095,732,1448,1086)]
    for i,ident in enumerate(props):
        box=boxes[i];H.sprite(ident,'r02-props-v1.png',box,specs[ident])
        if ident=='r02_crate_corner':
            q=raw.crop(box);q.putalpha(q.getchannel('A').point(lambda v:255 if v>=128 else 0));q=q.crop(q.getchannel('A').getbbox());out=Image.new('RGBA',(208,208));scale=min(200/q.width,200/q.height);q=q.resize((round(q.width*scale),round(q.height*scale)),Image.Resampling.NEAREST);out.alpha_composite(q,((208-q.width)//2,(208-q.height)//2));H.save(out,'r02_crate_corner_detail','ui',role='inspection_detail_only_not_room_scale_or_verified_evidence')
    backgrounds={'r02_inn_exterior':'r02-inn-ground-v1.png','r02_well':'r02-well-ground-v1.png','r02_tax_yard':'r02-tax-yard-v1.png'}
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);cs=G.cells(s);mask=gridmask(size,cs);floor=terrain(cs,size,tile_sets[s['material']]);allcells=G.rectcells([[0,0,s['cells'][0]-1,s['cells'][1]-1]])
        for rect in s.get('bridge_rectangles',[]):paste_rect(floor,terrain(cs,size,tile_sets['boards']),rect)
        for rect in s.get('ford_rectangles',[]):paste_rect(floor,terrain(cs,size,tile_sets['wetstone']),rect)
        if rid in ['r02_fork','r02_tracks','r02_inn_exterior','r02_well']:
            rm=Image.new('L',size);rd=ImageDraw.Draw(rm)
            lines=([[(39,481),(507,377),(1001,221)],[(507,65),(507,377),(1001,481)],[(507,377),(507,715)]] if rid=='r02_fork' else [[(65,247),(455,325),(1027,611)]] if rid=='r02_tracks' else [[(91,247),(455,325),(247,637)],[(455,325),(507,637),(507,741)],[(455,325),(715,663)]] if rid=='r02_well' else [[(91,247),(663,429),(949,637)]])
            for line in lines:rd.line(line,fill=255,width=78)
            floor.paste(terrain(allcells,size,tile_sets['gravel']),(0,0),ImageChops.multiply(rm,mask))
            if rid=='r02_tracks':
                rd=ImageDraw.Draw(floor)
                for dy in [-17,17]:rd.line([(65,247+dy),(455,325+dy),(1027,611+dy)],fill='#5E4F36',width=5)
                H.OPS.append(dict(operation='authored_static_wheel_rut_masks',scene=rid,width=5,separation=34,meaning='Visible traces only; no evidence certification'))
        floor.putalpha(mask);H.save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        if rid in backgrounds:
            fn=backgrounds[rid];im=H.raw(fn);back=H.sample(fn,(0,0,im.width,im.height),size)
        elif s['material']=='boards':back=Image.new('RGBA',size,'#050408')
        else:back=terrain(allcells,size,tile_sets['grass'])
        wm=Image.new('L',size);wd=ImageDraw.Draw(wm)
        for a1,b1,c1,d1 in s.get('water_rectangles',[])+s.get('cutout_rectangles',[]):wd.rectangle((a1*26,b1*26,(c1+1)*26-1,(d1+1)*26-1),fill=255)
        if rid in ['r02_inn_exterior','r02_well','r02_tracks']:wd.rectangle((0,702,size[0],size[1]),fill=255)
        if rid=='r02_tax_yard':wd.rectangle((0,520,size[0],size[1]),fill=255)
        wm=ImageChops.multiply(wm,ImageChops.invert(mask))
        if wm.getbbox():back.paste(H.water_plate(size),(0,0),wm)
        for rect in s['blocked_rectangles']:
            if rid=='r02_tax_main' and rect==[28,16,30,20]:continue
            paste_rect(back,terrain(allcells,size,tile_sets['gravel']),rect)
        H.save(back,rid+'__backing',role='nonwalkable_background',scene=rid)
        structure=Image.new('RGBA',size);fore=Image.new('RGBA',size)
        if rid=='r02_tax_main':
            s['structural_objects']=[dict(id='r02_bridge_pier',cell=list(v),role='Noninteractive lower bridge support, clipped outside walking plane') for v in [(23,16),(27,20),(31,24)]]
            for o in s['structural_objects']:
                x,y=o['cell'];ox,oy=specs[o['id']]['origin'];structure.alpha_composite(H.asset(o['id'],'items'),(x*26+13-ox,y*26+13-oy))
        indoor=s['material']=='boards';fn,box=('r02-interiors-v1.png',(86,185,156,276)) if indoor else ('r02-tax-main-v1.png',(657,91,695,232));wh=39 if indoor else 8
        for y in range(s['cells'][1]):
            for a1,b1 in H.ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):structure.alpha_composite(repeat(H.sample(fn,box,(78,wh)),((b1-a1+1)*26,wh)),(a1*26,y*26-wh))
            for a1,b1 in H.ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):fore.alpha_composite(repeat(H.sample(fn,box,(78,8)),((b1-a1+1)*26,8)),(a1*26,(y+1)*26))
        if indoor:
            for x in range(s['cells'][0]):
                for side,offset in [(-1,-7),(1,26)]:
                    for a1,b1 in H.ranges([y for cx,y in cs if cx==x and (x+side,y) not in cs]):structure.alpha_composite(repeat(H.sample(fn,box,(7,52)),(7,(b1-a1+1)*26)),(x*26+offset,a1*26))
            window=H.sample('r02-interiors-v1.png',(169,166,269,278),(78,65)) if rid=='r02_inn_common' else H.sample('r02-interiors-v1.png',(1152,267,1252,340),(78,52))
            for x in ([6,12,17] if rid=='r02_inn_common' else [10]):structure.alpha_composite(window,(x*26,39))
        s['door_clear_boxes']=[]
        for e in s['exits']:
            x,y=e['cell'];boxes=[]
            if (x-1,y) not in cs:boxes.append([x*26-13,y*26,x*26-1,y*26+25])
            if (x+1,y) not in cs:boxes.append([(x+1)*26,y*26,(x+1)*26+12,y*26+25])
            if (x,y-1) not in cs:boxes.append([x*26,y*26-wh,x*26+25,y*26-1])
            if (x,y+1) not in cs:boxes.append([x*26,(y+1)*26,x*26+25,(y+1)*26+wh-1])
            for rect in boxes:
                for im in [structure,fore]:ImageDraw.Draw(im).rectangle(rect,fill=(0,0,0,0))
                s['door_clear_boxes'].append(dict(exit=e['id'],rect=rect))
        for im in [structure,fore]:im.putalpha(ImageChops.multiply(im.getchannel('A'),ImageChops.invert(mask)))
        H.save(structure,rid+'__structure',role='nonwalkable_boundary_and_window_architecture',scene=rid);H.save(fore,rid+'__foreground',role='separate_front_edges',scene=rid)
        H.save(Image.alpha_composite(back,floor),rid+'__plan',role='flat_painted_plan',scene=rid)
        if s.get('repair_add_rectangles'):
            add=G.rectcells(s['repair_add_rectangles'])-cs;overlay=terrain(add,size,tile_sets['boards']);repaired=floor.copy();repaired.alpha_composite(overlay)
            H.save(overlay,rid+'__repair_overlay',role='optional_repaired_bridge_overlay_does_not_commit_story',scene=rid)
            H.save(repaired,rid+'__repaired_floor',role='proposed_floor_with_bridge_repaired_ford_kept',scene=rid)
            s['repaired_add_cells']=[list(v) for v in sorted(add)]
            repaired_mask=gridmask(size,cs|add)
            for part,layer in [('structure',structure),('foreground',fore)]:
                variant=layer.copy();variant.putalpha(ImageChops.multiply(variant.getchannel('A'),ImageChops.invert(repaired_mask)))
                H.save(variant,rid+'__repaired_'+part,role='boundary_variant_clipped_outside_repaired_walking_plane',scene=rid)
    # Reused N1 displays are art contact sheets, not a new duplicate playable room.
    over=Image.new('RGBA',(1040,806),'#050408')
    for room,pos in [('yard',(0,0)),('bellhouse',(520,0)),('underpass',(260,416))]:
        q=H.sample(f'reuse-n1-{room}-plan.png',(0,0,1040,780),(520,390));over.alpha_composite(q,pos)
    H.save(over,'r02_ferryold__plan_overview',role='existing_N1_three_room_contact_sheet_half_scale_not_room')
    H.save(H.raw('reuse-n1-yard-environment.png'),'r02_ferryold__site',role='existing_N1_yard_art_requantized_no_new_native_room')
    # Region pads measured from the generated master, display anchors only.
    r['art_anchor_pixels']={k:[round(x*1664/1448),round(y*1248/1086)] for k,x,y in [('R02-fork',164,354),('R02-inn',628,451),('R02-well',597,166),('R02-ferryold',201,129),('R02-tracks',915,318),('R02-tax',1233,457),('R02-repair',1166,768),('R02-ford',565,765)]}
    H.save(H.sample('r02-region-v1.png',(0,0,1448,1086),(1664,1248)),'r02_region__terrain',role='regional_topology_terrain_not_native_world_grid')
    q=H.raw('reuse-n1-bellhouse-exterior.png');H.save(q.resize((156,130),Image.Resampling.NEAREST),'r02_ferry_map_icon','ui',role='reused_N1_architecture_map_icon_half_scale')
    # Requested skill implementation, unchanged RGB nearest metric, cached exactly.
    finalize=H.module('pam_r02_finalize',H.SKILL/'scripts/finalize_assets.py');orig=finalize._find_nearest
    @lru_cache(maxsize=None)
    def nearest(r1,g,b1,pal):return orig(r1,g,b1,pal)
    finalize._find_nearest=lambda r1,g,b1,pal:nearest(r1,g,b1,tuple(pal));finalize.cmd_quantize(P);finalize.cmd_clean(P)
    # Quantized tiles are authoritative for all further rebuild/rendering.
    for key in tile_sets:tile_sets[key]=[H.asset(f'r02_{key}_v{j}','tiles') for j in range(9)]
    cuts={'r02_ferry_inn':159,'r02_tax_house':115,'r02_filter_shelter':61,'r02_repair_canopy':83,'r02_inspection_shed':76}
    for ident,cut in cuts.items():
        full=H.asset(ident,'items');roof=full.copy();body=full.copy();ra=full.getchannel('A');ba=full.getchannel('A');ImageDraw.Draw(ra).rectangle((0,cut,full.width,full.height),fill=0);ImageDraw.Draw(ba).rectangle((0,0,full.width,cut-1),fill=0);roof.putalpha(ra);body.putalpha(ba)
        for part,im in [('roof',roof),('body',body)]:H.save(im,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,split_at_y=cut)
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);props_layer=Image.new('RGBA',size);roof_layer=Image.new('RGBA',size)
        for o in sorted(s['objects'],key=lambda v:v['cell'][1]):
            ident=o['id'];ox,oy=specs[ident]['origin'];x,y=o['cell'];pos=(x*26+13-ox,y*26+13-oy);props_layer.alpha_composite(H.asset(ident+('__body' if ident in cuts else ''),'items'),pos)
            if ident in cuts:roof_layer.alpha_composite(H.asset(ident+'__roof','items'),pos)
        H.save(props_layer,rid+'__props_preview',role='placement_preview_only_use_independent_sprites_in_game',scene=rid)
        env=H.asset(rid+'__backing')
        for part in ['floor','structure','props_preview','foreground']:env.alpha_composite(H.asset(rid+'__'+part))
        if roof_layer.getchannel('A').getbbox():H.save(roof_layer,rid+'__roof',role='toggleable_roofs',scene=rid);H.save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid);env.alpha_composite(roof_layer)
        elif s['material']=='boards':H.save(env.copy(),rid+'__working_space',role='interior_working_space_composite',scene=rid)
        H.save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
        if s.get('repaired_add_cells'):
            repaired=H.asset(rid+'__backing')
            for part in ['repaired_floor','repaired_structure','props_preview','repaired_foreground']:repaired.alpha_composite(H.asset(rid+'__'+part))
            if roof_layer.getchannel('A').getbbox():repaired.alpha_composite(roof_layer)
            H.save(repaired,rid+'__repaired_preview',role='bridge_repair_visual_example_no_state_commit',scene=rid)
    for ident,parts in [('r02_tax__plan_overview',[('r02_tax_main__plan',(0,0)),('r02_tax_yard__plan',(156,858))]),('r02_tax__working_overview',[('r02_tax_yard__working_space',(0,0)),('r02_tax_office__working_space',(78,598))])]:
        size=(1092,1430) if 'plan' in ident else (780,1066);q=Image.new('RGBA',size,'#050408')
        for src,pos in parts:q.alpha_composite(H.asset(src),pos)
        H.save(q,ident,role='two_scene_contact_sheet_1_to_1_not_single_room')
    icons=Image.new('RGBA',(1664,1248));mapping={'R02-inn':'r02_ferry_inn','R02-well':'r02_filter_shelter','R02-tax':'r02_tax_house','R02-repair':'r02_repair_canopy','R02-ford':'r02_road_sign','R02-fork':'r02_road_sign','R02-tracks':'r02_crate_corner'}
    for key,ident in mapping.items():
        im=H.asset(ident,'items');q=im.resize((im.width//2,im.height//2),Image.Resampling.NEAREST);x,y=r['art_anchor_pixels'][key];icons.alpha_composite(q,(x-q.width//2,y+40-specs[ident]['origin'][1]//2))
    x,y=r['art_anchor_pixels']['R02-ferryold'];q=H.asset('r02_ferry_map_icon','ui');icons.alpha_composite(q,(x-q.width//2,y+40-121))
    H.save(icons,'r02_region__nodes',role='schematic_icons_not_room_scale');q=H.asset('r02_region__terrain');q.alpha_composite(icons);H.save(q,'r02_region__plan',role='regional_connectivity_schematic_not_official_geography');q.save(P/'previews/r02_region.png');H.write('region-layout.json',r)
    atlas=Image.new('RGBA',(936,1560));frames=[]
    for i,ident in enumerate(specs):
        im=H.asset(ident,'items');x=(i%3)*312+(312-im.width)//2;y=(i//3)*260+(260-im.height)//2;atlas.alpha_composite(im,(x,y));frames.append(dict(id=ident,rect=[x,y,*im.size],origin=specs[ident]['origin'],atlas_origin=[x+specs[ident]['origin'][0],y+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/r02_buildings_props.png');H.write('sheets/manifest.json',dict(type='18 static sprites, not animation',size=list(atlas.size),frames=frames))
    tile_atlas=Image.new('RGBA',(234,104));tile_frames=[]
    for row,key in enumerate(tile_sets):
        for j,q in enumerate(tile_sets[key]):tile_atlas.alpha_composite(q,(j*26,row*26));tile_frames.append(dict(id=f'r02_{key}_v{j}',rect=[j*26,row*26,26,26]))
    tile_atlas.save(P/'sheets/r02_flat_materials.png');H.write('sheets/tiles.json',dict(size=list(tile_atlas.size),cell_pixels=26,format='4materials x9edge-matched flat variants; not boundary autotiles',frames=tile_frames))
    for a in H.ASSETS:
        a.update(sha256=H.sha(P/a['path']),palette='DEN-R02-128',runtime_verified=False)
        if a['id']=='r02_tax_house':a['door_anchor']=[106,216]
        if a['id']=='r02_ferry_inn':a['door_anchor']=[155,242]
    H.write('manifest.json',dict(schema=1,batch=b['batch'],status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,assets=H.ASSETS,scenes=scenes,region=r,source_sha256=b['source_sha256'],raw_sources={f.name:H.sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=H.OPS,inventory_requests=b['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,scale='1 pixel =1 room pixel except map icons/detail/contact sheets explicitly marked',room_origin=[0,0],draw_order=['backing','floor','structure','foot-sorted independent bodies/props and native actors','foreground','toggleable roofs'],collision='Explicit proposed cell sets including cutout rectangles; never PNG alpha',npc='All actor zones empty; NPC model owns art/dialogue/logic',states='Repair overlays illustrative only; no story/permission/stock/light state is committed'),limitations=['Proposed scene geometry, not native game rooms.','Inn public common room drawn; paid lodging capacity and dedicated guest room not specified or invented.','World positions/portals/native save lifecycle/dynamic lights require integration testing.','N1 contact sheet reuses existing project art; no new duplicate rooms or story events.']))
    prefix='src/Art/hd2d_26x26_20261013/batches/R02-river-v1/';records=[]
    refs={'r02-inn-ground-v1':'r02_inn_exterior_generation_v1','r02-well-ground-v1':'r02_well_generation_v1','r02-tax-main-v1':'r02_tax_main_generation_v1','r02-tax-yard-v1':'r02_tax_yard_generation_v1','r02-region-v1':'r02_region_geometry'}
    for ident in ['r02-materials-v1','r02-inn-ground-v1','r02-well-ground-v1','r02-tax-main-v1','r02-tax-yard-v1','r02-interiors-v1','r02-architecture-v1','r02-props-v1','r02-region-v1']:
        prompt=f'notes/prompt-{ident}.txt';output=f'raw/{ident}.png';inputs=[prefix+'guides/'+refs[ident]+'.png','design/12_美术参考/城市概念/DEN-概念-v1.png'] if ident in refs else []
        records.append(dict(id=ident,method='built-in image_gen',selected=True,prompt=prompt,prompt_sha256=H.sha(P/prompt),output=output,output_sha256=H.sha(P/output),original_size=list(Image.open(P/output).size),inputs=[dict(path=n,sha256=H.sha(ROOT/n)) for n in inputs],spec_lock_sha256=H.sha(P/'spec_lock.md')))
    reuses=[]
    for f in sorted((P/'raw').glob('reuse-*.png')):
        if f.name=='reuse-n1-water.png':src='src/Art/hd2d_26x26_20261013/raw/n1-water-v1.png'
        elif f.name=='reuse-n1-bellhouse-exterior.png':src='src/Art/hd2d_26x26_20261013/assets/items/n1_bellhouse_exterior.png'
        else:
            room=f.name.split('-')[2];view=f.name.split('-')[3].split('.')[0];src=f'src/Art/hd2d_26x26_20261013/'+(f'previews/r_eao_n1_{room}__preview.png' if view=='environment' else f'assets/backgrounds/r_eao_n1_{room}__plan.png')
        reuses.append(dict(path=src,batch_copy='raw/'+f.name,sha256=H.sha(f)))
    H.write('generation-log.json',dict(skill_commit=b['skill_commit'],generation_count=len(records),records=records,reuse_sources=reuses,input_note='Well v1 guide restored from recorded pre-body-occupancy generation geometry after production refinement; archive hash is measured on the restored file, not a contemporaneous pre-call fingerprint. Other geometry input guides retained before refinements. Raw atlas panel widths approximate; actual inspected crop boxes and NN normalization recorded.'))
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(H.ASSETS),sprites=len(specs),tiles=36,view_slots=len(b['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
