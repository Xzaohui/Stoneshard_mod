"""Export R03 artwork on explicit authored grids; no game or NPC writes."""
from pathlib import Path
from functools import lru_cache
import importlib.util,json
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R03-maen-v1'
def module(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
H=module('r03_asset_helpers',ROOT/'tools/Export-Hd2dR01.py');H.P=P
G=module('r03_geometry',ROOT/'tools/Prepare-Hd2dR03.py')
def repeat(t,size):
    q=Image.new('RGBA',size)
    for y in range(0,size[1],t.height):
        for x in range(0,size[0],t.width):q.alpha_composite(t,(x,y))
    return q
def mask(size,cs):
    q=Image.new('L',size);d=ImageDraw.Draw(q)
    for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
    return q
def paintrect(q,paint,r):
    a,b,c,d=r;ms=Image.new('L',q.size);ImageDraw.Draw(ms).rectangle((a*26,b*26,(c+1)*26-1,(d+1)*26-1),fill=255);q.paste(paint,(0,0),ms)
def main():
    H.ASSETS.clear();H.OPS.clear();b=H.read('brief.json');scenes=H.read('layouts.json');region=H.read('region-layout.json');specs={s['id']:s for s in b['sprites']};surfaces={}
    ms=H.raw('r03-materials-v1.png');w,h=ms.width//2,ms.height//2
    for i,key in enumerate(['earth','slate','boards','charred']):
        x=i%2*w;y=i//2*h;plate=H.sample('r03-materials-v1.png',(x+24,y+24,x+w-24,y+h-24),(312,312));ts=[plate.crop((104+(j%3)*26,104+(j//3)*26,130+(j%3)*26,130+(j//3)*26)) for j in range(9)]
        horizontal=[ts[0].getpixel((v,0)) for v in range(26)];vertical=[ts[0].getpixel((0,v)) for v in range(26)];horizontal[-1]=vertical[0]=vertical[-1]=horizontal[0]
        for j,t in enumerate(ts):
            for v in range(26):t.putpixel((v,0),horizontal[v]);t.putpixel((v,25),horizontal[v]);t.putpixel((0,v),vertical[v]);t.putpixel((25,v),vertical[v])
            H.save(t,f'r03_{key}_v{j}','tiles',role='flat_edge_matched_material_variant',material=key,variant=j)
        for v in range(312):plate.putpixel((v,311),plate.getpixel((v,0)));plate.putpixel((311,v),plate.getpixel((0,v)))
        surfaces[key]=plate;H.OPS.append(dict(operation='shared_tile_edge_profiles_and312pxmacro_wrap',material=key,tiles=9,border=1,orientation='no flips/rotation',note='Flat material variants, not boundary autotiles'))
    surfaces['boards']=H.sample('r03-interiors-v1.png',(610,640,940,945),(312,312))
    for v in range(312):surfaces['boards'].putpixel((v,311),surfaces['boards'].getpixel((v,0)));surfaces['boards'].putpixel((311,v),surfaces['boards'].getpixel((0,v)))
    arch_boxes=[(0,0,500,540),(510,0,986,540),(1000,0,1536,540),(0,542,500,1024),(510,542,1010,1024),(1030,542,1536,1024)]
    a_boxes=[(0,0,395,535),(430,0,730,535),(820,0,1110,535),(1210,0,1495,535),(0,540,510,1024),(520,540,812,1024),(830,540,1185,1024),(1210,535,1536,1024)]
    b_boxes=[(0,0,403,515),(430,0,711,515),(735,0,1093,515),(1097,0,1536,515),(0,530,355,1024),(410,530,739,1024),(785,520,1085,1024),(1100,530,1536,1024)]
    ids=list(specs)
    for keys,boxes,raw in [(ids[:6],arch_boxes,'r03-architecture-v1.png'),(ids[6:14],a_boxes,'r03-props-a-v1.png'),(ids[14:],b_boxes,'r03-props-b-v1.png')]:
        for ident,box in zip(keys,boxes):H.sprite(ident,raw,box,specs[ident])
    land=H.raw('r03-landscape-v1.png');lw,lh=land.width//2,land.height//2
    landscapes=[H.sample('r03-landscape-v1.png',(i%2*lw,i//2*lh,(i%2+1)*lw,(i//2+1)*lh),(1040,780)) for i in range(4)]
    crop_paint=H.sample('r03-landscape-v1.png',(198,lh+40,lw-24,lh+350),(312,312))
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);cs=G.cells(s);cm=mask(size,cs);indoor=s in scenes[12:];floor=repeat(surfaces[s['material']],size)
        if not indoor and rid!='r03_court':
            lines=s.get('road_lines') or [[e['cell'],[s['cells'][0]//2,s['cells'][1]//2]] for e in s['exits'] if not any(k in e['id'] for k in ['room','common','hall','store'])]
            road=Image.new('L',size);rd=ImageDraw.Draw(road)
            for line in lines:rd.line([tuple(v*26+13 for v in p) for p in line],fill=255,width=52)
            floor.paste(repeat(surfaces['slate'],size),(0,0),road)
        for a in s.get('annexes',[]):paintrect(floor,repeat(surfaces[a['material']],size),a['rect'])
        if rid=='r03_court':paintrect(floor,repeat(surfaces['slate'],size),[12,9,31,26])
        for r in s.get('field_rectangles',[]):paintrect(floor,repeat(crop_paint,size),r)
        floor.putalpha(cm);H.save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        raw={'r03_mill':'r03-mill-ground-v1.png','r03_library':'r03-library-ground-v1.png','r03_court':'r03-court-ground-v1.png'}.get(rid)
        if raw:
            q=H.raw(raw);back=H.sample(raw,(0,0,q.width,q.height),size)
        elif indoor:back=Image.new('RGBA',size,'#090C14')
        else:
            index=1 if rid in ['r03_burnt','r03_depot'] else 3 if rid in ['r03_field','r03_ration'] else 0;back=landscapes[index].resize(size,Image.Resampling.NEAREST)
        H.save(back,rid+'__backing',role='nonwalkable_background',scene=rid);structure=Image.new('RGBA',size);front=Image.new('RGBA',size)
        wall=H.sample('r03-interiors-v1.png',(195,36,299,168),(78,39 if indoor or rid=='r03_court' else 9));height=wall.height
        for y in range(s['cells'][1]):
            for a,z in H.ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):structure.alpha_composite(repeat(wall,((z-a+1)*26,height)),(a*26,y*26-height))
            for a,z in H.ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):front.alpha_composite(repeat(wall.resize((78,8),Image.Resampling.NEAREST),((z-a+1)*26,8)),(a*26,(y+1)*26))
        if indoor or rid=='r03_court':
            side=wall.resize((7,52),Image.Resampling.NEAREST)
            for x in range(s['cells'][0]):
                for step,offset in [(-1,-7),(1,26)]:
                    for a,z in H.ranges([y for cx,y in cs if cx==x and (x+step,y) not in cs]):structure.alpha_composite(repeat(side,(7,(z-a+1)*26)),(x*26+offset,a*26))
            if indoor:
                window=H.sample('r03-interiors-v1.png',(83,48,188,144),(52,52));wx=6 if s['material']=='boards' else 10;structure.alpha_composite(window,(wx*26,3*26-26))
            else:
                west=H.sample('r03-interiors-v1.png',(533,152,572,310),(26,78));north=H.sample('r03-interiors-v1.png',(1390,35,1500,153),(52,26))
                for key,q,pos in [('burnt',west,(5*26,8*26)),('shell',west,(5*26,19*26)),('print',north,(34*26,6*26)),('maintenance',west.transpose(Image.Transpose.FLIP_LEFT_RIGHT),(38*26,22*26))]:
                    structure.alpha_composite(q,pos);next(a for a in s['annexes'] if a['id']==key)['window_rect']=[*pos,*q.size]
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
        H.save(structure,rid+'__structure',role='nonwalkable_boundary_and_window_architecture',scene=rid);H.save(front,rid+'__foreground',role='separate_front_edges',scene=rid);H.save(Image.alpha_composite(back,floor),rid+'__plan',role='flat_painted_plan',scene=rid)
    finalize=H.module('pam_r03_finalize',H.SKILL/'scripts/finalize_assets.py');orig=finalize._find_nearest
    @lru_cache(maxsize=None)
    def palette_rgb(pal):return [tuple(int(h[i:i+2],16) for i in [1,3,5]) for h in pal]
    @lru_cache(maxsize=None)
    def nearest(r,g,b,pal):
        # Exact skill metric and first-entry tie rule; avoid re-parsing HEX on each pixel.
        return min(palette_rgb(pal),key=lambda p:(r-p[0])**2+(g-p[1])**2+(b-p[2])**2)
    declared=tuple(finalize._load_palette(P))
    for rgb in [(0,0,0),(255,255,255),(80,100,120),(142,145,146),(137,123,109)]:assert nearest(*rgb,declared)==orig(*rgb,declared)
    finalize._find_nearest=lambda r,g,b,pal:nearest(r,g,b,tuple(pal));finalize.cmd_quantize(P);finalize.cmd_clean(P)
    # Split after palette/alpha processing, so the variants exactly reconstruct full.
    cuts={'r03_mill_house':202,'r03_granary':101,'r03_low_library':115,'r03_scribe_shed':78,'r03_watch_shelter':71}
    for ident,cut in cuts.items():
        im=H.asset(ident,'items');roof=im.copy();body=im.copy();ra=im.getchannel('A');ba=im.getchannel('A');ImageDraw.Draw(ra).rectangle((0,cut,im.width,im.height),fill=0);ImageDraw.Draw(ba).rectangle((0,0,im.width,cut-1),fill=0);roof.putalpha(ra);body.putalpha(ba)
        for part,q in [('roof',roof),('body',body)]:H.save(q,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,split_at_y=cut)
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);props=Image.new('RGBA',size);roof=Image.new('RGBA',size);conditional=Image.new('RGBA',size)
        for o in sorted(s['objects']+s.get('conditional_objects',[]),key=lambda o:o['cell'][1]):
            ident=o['id'];x,y=o['cell'];ox,oy=specs[ident]['origin'];pos=(x*26+13-ox,y*26+13-oy);target=conditional if 'condition' in o else props;target.alpha_composite(H.asset(ident+('__body' if ident in cuts else ''),'items'),pos)
            if ident in cuts:roof.alpha_composite(H.asset(ident+'__roof','items'),pos)
        H.save(props,rid+'__props_preview',role='placement_preview_only_use_independent_sprites_in_game',scene=rid)
        if conditional.getchannel('A').getbbox():H.save(conditional,rid+'__conditional_props',role='optional_care_chair_example_off_by_default_no_story_commit',scene=rid)
        if roof.getchannel('A').getbbox():H.save(roof,rid+'__roof',role='toggleable_roofs',scene=rid)
        env=H.asset(rid+'__backing')
        for part in ['floor','structure','props_preview','foreground']:env.alpha_composite(H.asset(rid+'__'+part))
        H.save(env.copy(),rid+'__working_space',role='roof_hidden_working_space_composite',scene=rid)
        if roof.getchannel('A').getbbox():env.alpha_composite(roof)
        H.save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
    overview=Image.new('RGBA',(1040,1586),'#090C14');overview.alpha_composite(H.asset('r03_library__plan'),(0,0));overview.alpha_composite(H.asset('r03_library_store__plan'),(52,806));H.save(overview,'r03_library__plan_overview',role='two_scene_contact_sheet_1_to_1_not_single_room')
    overview=Image.new('RGBA',(1300,598),'#090C14');overview.alpha_composite(H.asset('r03_court_print_room__environment'),(0,65));overview.alpha_composite(H.asset('r03_court_shell_room__environment'),(624,13));H.save(overview,'r03_court__working_overview',role='two_scene_contact_sheet_1_to_1_not_single_room')
    anchors=[('border',123,165),('road',406,165),('depot',709,165),('watch',169,375),('field',236,581),('ration',495,531),('mill',759,467),('hide',953,466),('library',1275,306),('burnt',1148,676),('court',1207,883),('scribe',811,865)];region['art_anchor_pixels']={'R03-'+k:[round(x*1664/1448),round(y*1248/1086)] for k,x,y in anchors}
    q=H.raw('r03-region-v1.png');terrain=H.sample('r03-region-v1.png',(0,0,q.width,q.height),(1664,1248));icons=Image.new('RGBA',terrain.size)
    iconmap={'border':'blank_waypost','road':'blank_waypost','depot':'grain_sacks','mill':'mill_house','ration':'granary','hide':'book_grain_stack','library':'low_library','burnt':'burned_frame','court':'empty_shell','scribe':'scribe_shed','field':'grain_sacks','watch':'watch_shelter'}
    for key,short in iconmap.items():
        ident='r03_'+short;im=H.asset(ident,'items');scale=min(156/im.width,130/im.height);part=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);x,y=region['art_anchor_pixels']['R03-'+key];icons.alpha_composite(part,(x-part.width//2,y+40-round(specs[ident]['origin'][1]*scale)))
    # Quantize only this new raw region layer; never requantize all composed assets.
    pal=finalize._load_palette(P)
    for y in range(terrain.height):
        for x in range(terrain.width):
            r,g,b1,a=terrain.getpixel((x,y));terrain.putpixel((x,y),(*finalize._find_nearest(r,g,b1,pal),255))
    H.save(terrain,'r03_region__terrain',role='regional_topology_terrain_not_native_world_grid');H.save(icons,'r03_region__nodes',role='schematic_icons_not_room_scale');terrain.alpha_composite(icons);H.save(terrain,'r03_region__plan',role='regional_connectivity_schematic_not_official_geography');terrain.save(P/'previews/r03_region.png');H.write('region-layout.json',region)
    atlas=Image.new('RGBA',(1248,2028));frames=[]
    for i,ident in enumerate(specs):
        im=H.asset(ident,'items');x=(i%4)*312+(312-im.width)//2;y=(i//4)*338+(338-im.height)//2;atlas.alpha_composite(im,(x,y));frames.append(dict(id=ident,rect=[x,y,*im.size],origin=specs[ident]['origin'],atlas_origin=[x+specs[ident]['origin'][0],y+specs[ident]['origin'][1]]))
    atlas.save(P/'sheets/r03_buildings_props.png');H.write('sheets/manifest.json',dict(size=list(atlas.size),frames=frames,type='22 static sprites, not animation'))
    atlas=Image.new('RGBA',(234,104));frames=[]
    for row,key in enumerate(surfaces):
        for j in range(9):atlas.alpha_composite(H.asset(f'r03_{key}_v{j}','tiles'),(j*26,row*26));frames.append(dict(id=f'r03_{key}_v{j}',rect=[j*26,row*26,26,26]))
    atlas.save(P/'sheets/r03_flat_materials.png');H.write('sheets/tiles.json',dict(size=list(atlas.size),frames=frames,cell_pixels=26))
    for a in H.ASSETS:a.update(sha256=H.sha(P/a['path']),palette='MAE-R03-128',runtime_verified=False)
    H.write('layouts.json',scenes);H.write('manifest.json',dict(schema=1,batch=b['batch'],status='exported_pending_validation',format='RGBA PNG',native_cell_size=26,assets=H.ASSETS,scenes=scenes,region=region,source_sha256=b['source_sha256'],raw_sources={f.name:H.sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=H.OPS,inventory_requests=b['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,room_origin=[0,0],scale='1 pixel=1room pixel; region and contact sheets explicitly separate',collision='Explicit proposed cells, never PNG alpha',draw_order=['backing','floor','structure','foot-sorted independent bodies/props/actors','foreground','toggleable roofs'],states='Care chair optional/off by default; no quest/permission/consent/fire state baked'),limitations=['Proposed geometry, native rooms/portals/weather/save/collision not tested.','Mill two bedrolls are a finite capacity proposal, not an implemented lodging service.','Input generation guides immutable; northeast/west annex dividers refined in production layouts after court master generation.','No NPC art/dialogue/logic in this batch.']))
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(H.ASSETS),sprites=len(specs),tiles=36,view_slots=len(b['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
