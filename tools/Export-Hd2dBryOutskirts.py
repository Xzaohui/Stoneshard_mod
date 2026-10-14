"""Assemble21 authored zones and27 complete satellite/continuation view slots."""
from pathlib import Path
from functools import lru_cache
import json,hashlib,copy,math
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/BRY-outskirts-v1'
def read(n):return json.loads((P/n).read_text(encoding='utf-8'))
def write(n,d):(P/n).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rc(rs):return {(x,y) for a,b,c,d in rs for y in range(b,d+1) for x in range(a,c+1)}
def cells(s):return rc(s['walkable_rectangles'])-rc(s['blocked_rectangles'])
def mask(size,cs):
    q=Image.new('L',tuple(size));d=ImageDraw.Draw(q)
    for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
    return q
def repeat(t,size):
    q=Image.new('RGBA',size)
    for y in range(0,size[1],t.height):
        for x in range(0,size[0],t.width):q.alpha_composite(t,(x,y))
    return q
def ranges(vs):
    result=[]
    for x in sorted(vs):
        if not result or x>result[-1][1]+1:result.append([x,x])
        else:result[-1][1]=x
    return result
def main():
    b=read('brief.json');assert read('sprites-validation.json')['passed'];assert all(sha(ROOT/n)==h for n,h in b['source_sha256'].items());sm=read('sprite-manifest.json');mm=read('materials-manifest.json');assets=copy.deepcopy(mm['assets']+sm['assets']);ops=copy.deepcopy(sm['crop_operations']);specs={s['id']:s for s in b['sprites']+b['reused_sprites']};scenes=read('layouts.json');rgb=[tuple(int(c[i:i+2],16) for i in [1,3,5]) for c in read('palettes/bry_outskirts_128.json')['colors']]
    @lru_cache(None)
    def nearest(c):return min(rgb,key=lambda q:sum((q[i]-c[i])**2 for i in range(3)))
    def quant(q):
        out=Image.new('RGBA',q.size);out.putdata([(*nearest(c[:3]),255) if c[3]>=128 else (0,0,0,0) for c in q.convert('RGBA').get_flattened_data()]);return out
    def asset(ident,category='backgrounds'):return Image.open(P/f'assets/{category}/{ident}.png').convert('RGBA')
    def save(q,ident,category='backgrounds',origin=(0,0),**meta):
        rel=f'assets/{category}/{ident}.png';assert ident not in {a['id'] for a in assets},ident;q.save(P/rel);assets.append(dict(id=ident,path=rel,size=list(q.size),origin=list(origin),palette='BRY-CORE-128',sha256=sha(P/rel),runtime_verified=False,**meta));return q
    roofpolys={
      'bryo_embankment_commons':dict(polygons=[[(22,343),(84,247),(358,249),(421,354),(124,366)],[(79,212),(120,212),(120,257),(79,257)]],holes=[[(26,342),(81,272),(123,347)]]),
      'bryo_raised_seed_store':dict(polygons=[[(435,252),(491,176),(700,177),(760,266),(532,279)]],holes=[[(440,249),(491,196),(531,256)]]),
      'bryo_sail_commons':dict(polygons=[[(767,344),(820,259),(1095,263),(1149,355),(856,365)],[(820,232),(859,232),(859,276),(820,276)]],holes=[[(772,340),(820,284),(851,348)]]),
      'bryo_side_berth_shed':dict(polygons=[[(1151,336),(1208,265),(1469,254),(1518,338),(1247,350)]],holes=[[(1158,331),(1207,284),(1243,335)]]),
      'bryo_binding_shop':dict(polygons=[[(25,733),(83,653),(363,651),(419,735),(117,754)]],holes=[[(30,728),(82,675),(114,739)]]),
      'bryo_sealed_outer_shed':dict(polygons=[[(426,735),(480,653),(704,654),(757,745),(524,755)]],holes=[[(431,731),(480,674),(520,739)]]),
      'bryo_public_tower_portico':dict(polygons=[[(765,730),(805,649),(1081,647),(1128,738),(805,743)]],holes=[]),
      'bryo_small_hearing_pavilion':dict(polygons=[[(1140,718),(1313,622),(1511,716),(1374,772),(1229,770)]],holes=[])}
    roof_ids=set(roofpolys)|{s['id'] for s in b['reused_sprites'] if s.get('architecture')}
    raw=Image.open(P/'raw/bryo-architecture-v1.png');spriteops={o['id']:o for o in sm['crop_operations']};(P/'guides/roofs').mkdir(exist_ok=True)
    for ident,shapes in roofpolys.items():
        op=spriteops[ident];full=asset(ident,'items');rm=Image.new('L',raw.size);d=ImageDraw.Draw(rm)
        for poly in shapes['polygons']:d.polygon(poly,fill=255)
        for poly in shapes['holes']:d.polygon(poly,fill=0)
        fitted=rm.crop(op['box']).crop(op['trim_bbox']).resize(tuple(op['fitted_size']),Image.Resampling.NEAREST);m=Image.new('L',full.size);m.paste(fitted,tuple(op['offset']));m=ImageChops.multiply(m,full.getchannel('A'));m.save(P/f'guides/roofs/{ident}_mask.png');body=full.copy();roof=full.copy();body.putalpha(ImageChops.subtract(full.getchannel('A'),m));roof.putalpha(m)
        for part,q in [('body',body),('roof',roof)]:save(q,ident+'__'+part,'items',specs[ident]['origin'],role='architectural_'+part,source_sprite=ident,mask=f'guides/roofs/{ident}_mask.png')
        ops.append(dict(id=ident,operation='reviewed_roof_polygons_with_gable_exclusions',source='raw/bryo-architecture-v1.png',**shapes,source_crop_operation=op,mask=f'guides/roofs/{ident}_mask.png'))
    for a in assets:
        if a.get('architecture'):a.update(roof_variants_pending=False,roof_variants={part:f'assets/items/{a["id"]}__{part}.png' for part in ['body','roof']})
    land=Image.open(P/'raw/bryo-landscape-v1.png').convert('RGBA');lw,lh=land.width//2,land.height//2;landscapes=[quant(land.crop((i%2*lw,i//2*lh,(i%2+1)*lw,(i//2+1)*lh)).resize((312,312),Image.Resampling.NEAREST)) for i in range(4)];ops.append(dict(source='raw/bryo-landscape-v1.png',actual_size=list(land.size),quadrants=[[(i%2)*lw,(i//2)*lh,(i%2+1)*lw,(i//2+1)*lh] for i in range(4)],target_size=[312,312],resample='nearest',palette='BRY-CORE-128'))
    surfaces={k:asset('bry_'+k+'__material') for k in ['paving','stone','boards','earth']};walls={k:asset('bry_'+k+'__wall','items') for k in ['stone','wood','plaster']};windows={k:asset('bry_'+k+'__window','items') for k in walls}
    for s in scenes:
        rid=s['id'];size=tuple(s['size']);cs=cells(s);cm=mask(size,cs);cm.save(P/f'guides/{rid}_walkable.png');indoor=s.get('interior',False);floor=repeat(surfaces[s['material']],size);floor.putalpha(cm);save(floor,rid+'__floor',role='exact_proposed_walkable_floor',scene=rid)
        back=Image.new('RGBA',size,(*rgb[-1],255)) if indoor else repeat(landscapes[0 if rid.startswith('bryo_s01') else 1 if rid.startswith('bryo_s02') else 2],size);save(back,rid+'__backing',role='nonwalkable_background',scene=rid)
        water=repeat(landscapes[3],size);wc=rc(s.get('water_rectangles',[]))-cs;water.putalpha(mask(size,wc))
        if wc:save(water,rid+'__water',role='nonwalkable_calm_water_layer',scene=rid)
        field=repeat(landscapes[1],size);fc=rc(s.get('salt_field_rectangles',[]))-cs;field.putalpha(mask(size,fc))
        if fc:save(field,rid+'__salt_field',role='nonwalkable_low_salt_field_not_deep_water',scene=rid)
        structure=Image.new('RGBA',size);front=Image.new('RGBA',size);kind='wood' if s['material']=='boards' else 'stone';height=39 if indoor else 9;wall=walls[kind].resize((78,height),Image.Resampling.NEAREST)
        for y in range(s['cells'][1]):
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y-1) not in cs]):structure.alpha_composite(repeat(wall,((z-a+1)*26,height)),(a*26,y*26-height))
            for a,z in ranges([x for x,cy in cs if cy==y and (x,y+1) not in cs]):front.alpha_composite(repeat(wall.resize((78,8),Image.Resampling.NEAREST),((z-a+1)*26,8)),(a*26,(y+1)*26))
        if indoor:
            side=wall.resize((7,52),Image.Resampling.NEAREST)
            for x in range(s['cells'][0]):
                for step,off in [(-1,-7),(1,26)]:
                    for a,z in ranges([y for cx,y in cs if cx==x and (x+step,y) not in cs]):structure.alpha_composite(repeat(side,(7,(z-a+1)*26)),(x*26+off,a*26))
            wx=5;top=min(y for x,y in cs if x==wx);pos=(wx*26,top*26-52);structure.alpha_composite(windows[kind],pos);s['window_wall_rect']=[*pos,52,52]
        s['door_clear_boxes']=[]
        for e in s['exits']:
            x,y=e['cell'];boxes=[]
            if (x-1,y) not in cs:boxes.append([x*26-13,y*26,x*26-1,y*26+25])
            if (x+1,y) not in cs:boxes.append([(x+1)*26,y*26,(x+1)*26+12,y*26+25])
            if (x,y-1) not in cs:boxes.append([x*26,y*26-height,x*26+25,y*26-1])
            if (x,y+1) not in cs:boxes.append([x*26,(y+1)*26,x*26+25,(y+1)*26+height-1])
            for box in boxes:
                for q in [structure,front]:ImageDraw.Draw(q).rectangle(box,fill=(0,0,0,0))
                s['door_clear_boxes'].append(dict(exit=e['id'],rect=box))
        for q in [structure,front]:q.putalpha(ImageChops.multiply(q.getchannel('A'),ImageChops.invert(cm)))
        save(structure,rid+'__structure',role='boundary_architecture_not_floor',scene=rid);save(front,rid+'__foreground',role='separate_front_edges',scene=rid)
        blueprint=Image.new('RGBA',size);d=ImageDraw.Draw(blueprint)
        for a,y,c,z in s['blocked_rectangles']:d.rectangle((a*26,y*26,(c+1)*26-1,(z+1)*26-1),fill=(*rgb[59],255),outline=(*rgb[31],255),width=2)
        if blueprint.getchannel('A').getbbox():save(blueprint,rid+'__plan_structure',role='flat_block_footprint_diagram_only',scene=rid)
        plan=back.copy()
        for q in [water,field,floor,blueprint]:plan.alpha_composite(q)
        save(plan,rid+'__plan',role='flat_painted_plan',scene=rid)
        props=Image.new('RGBA',size);roofs=Image.new('RGBA',size);ordered=[]
        for host in sorted([o for o in s['objects'] if not o.get('surface_attachment')],key=lambda o:o['cell'][1]):ordered.append(host);ordered.extend(o for o in s['objects'] if o.get('draw_after_instance')==host['instance_id'])
        assert len(ordered)==len(s['objects']),rid+' attachment host missing';s['object_canvas_rects']=[]
        for o in ordered:
            ident=o['id'];x,y=o['cell'];ox,oy=specs[ident]['origin'];pos=(x*26+13-ox,y*26+13-oy);q=asset(ident+('__body' if ident in roof_ids else ''),'items');assert pos[0]>=0 and pos[1]>=0 and pos[0]+q.width<=size[0] and pos[1]+q.height<=size[1],(rid,ident,'clipped');props.alpha_composite(q,pos)
            s['object_canvas_rects'].append(dict(instance_id=o['instance_id'],rect=[*pos,*q.size]))
            if ident in roof_ids:roofs.alpha_composite(asset(ident+'__roof','items'),pos)
        save(props,rid+'__props_preview',role='placement_preview_use_independent_sprites_in_game',scene=rid)
        if roofs.getchannel('A').getbbox():save(roofs,rid+'__roof',role='toggleable_roofs',scene=rid)
        env=back.copy()
        for q in [water,field,floor,structure,props,front]:env.alpha_composite(q)
        save(env.copy(),rid+'__working_space',role='roof_hidden_working_composite',scene=rid);env.alpha_composite(roofs);save(env,rid+'__environment',role='scene_composite_preview_not_game_backdrop',scene=rid);env.save(P/f'previews/{rid}.png')
        if s.get('hazard_rectangles'):
            h=Image.new('RGBA',size);hd=ImageDraw.Draw(h)
            for a,y,c,z in s['hazard_rectangles']:
                box=(a*26,y*26,(c+1)*26-1,(z+1)*26-1);hd.rectangle(box,outline=(*rgb[31],255),width=2)
                for dx in range(a*26+5,(c+1)*26,13):hd.line([(dx,y*26+4),(dx-4,y*26+12)],fill=(*rgb[31],255),width=1)
            save(h,rid+'__hazard_markings',role='default_off_proposed_unsafe_outline_not_damage_or_game_state',scene=rid);s['illustration_variants']=dict(hazard=dict(default=False,game_state_commit=False,floor_unchanged=True))
    for loc in ['s01','s02','s03','x11','x12','x13','x14','x15','x16']:
        ids=[s['id'] for s in scenes if s['id'].startswith('bryo_'+loc+'_')];ss={s['id']:s for s in scenes};ext=ids[0];others=ids[1:];gap=26;y=ss[ext]['size'][1]+gap;x=0;parts=[(ext,0,0)]
        for rid in others:parts.append((rid,x,y));x+=ss[rid]['size'][0]+gap
        size=[max(ss[ext]['size'][0],x-gap),y+max(ss[rid]['size'][1] for rid in others)]
        for suffix,layer in [('plan_overview','plan'),('working_overview','environment')]:
            q=Image.new('RGBA',tuple(size),(*rgb[-1],255))
            for rid,x,y in parts:q.alpha_composite(asset(rid+'__'+layer),(x,y))
            save(q,'bryo_'+loc+'__'+suffix,role='multizone_1to1_overview_not_single_room',sheet_layout=dict(size=size,parts=parts),location='BRY-'+loc.upper());q.save(P/f'previews/bryo_{loc}_{suffix}.png')
    atlas=Image.new('RGBA',(1794,math.ceil(len(specs)/4)*338));frames=[]
    for i,(ident,spec) in enumerate(specs.items()):
        q=asset(ident,'items');x=(i%4)*448+(448-q.width)//2;y=(i//4)*338+(338-q.height)//2;atlas.alpha_composite(q,(x,y));frames.append(dict(id=ident,rect=[x,y,*q.size],origin=spec['origin'],atlas_origin=[x+spec['origin'][0],y+spec['origin'][1]]))
    atlas.save(P/'sheets/bryo_buildings_props.png');write('sheets/manifest.json',dict(size=list(atlas.size),frames=frames,type='60static environment sprites, no animations'))
    write('layouts.json',scenes);write('manifest.json',dict(schema=1,batch=b['batch'],status='exported_pending_validation',native_cell_size=26,format='RGBA PNG',assets=assets,scenes=scenes,region=read('region-layout.json'),source_sha256=b['source_sha256'],raw_sources={f.name:sha(f) for f in sorted((P/'raw').glob('*.png'))},crop_operations=ops,inventory_requests=b['inventory_requests'],import_contract=dict(sampling='nearest',mipmaps=False,room_origin=[0,0],scale='1pixel=1room pixel; overview preserves exact zone pixels, not one room',collision='Terrain plus separate proposed fixture rectangles; never PNGalpha; native unmeasured',draw_order=['backing','nonwalkable water/saltfield','floor','structure','foot-sorted independent bodies/props/actors; surface attachments after host','foreground','toggleable roofs','optional hazard outline'],states='Blanklabels/unlitbase; no permissions/consent/payment/harvest/repair/departure/health or story outcome baked'),limitations=['21authored grid proposals, not native doors,stairs,collision,saves/weather/lighting.','S01is R01camp backliving extension, original N2yard unchanged. Three satellites each2bed designcapacity, not actual assigned beds/stock.','X11one shore entrance and one physical rentalboat represented in exterior/detail views, no secondboat/trip/supportset.','Saltfield is low damp soil, not deepwater; seed/scale highroute remains independent.','X12two finitebatches and three testtypes; publicroute bypasses fence.','X13separate historic/added trays,covered familylabels and single restorationseat.','X14unsafearea closed, fixed outer inspection independent; no original cellar/ladder/enemies reproduced.','X15privateclaim/batchpurse/fee separate, no military authority or wholebatchpaid.','X16one ringtable/fiveemptychairs and separate sidetable; emptychair isnotconsent.','Original generationlock preserved byte-for-byte; current lock fixes only validator heading/explicit approved128budget; raw/prompt hashes unchanged.','No NPC/dialogue/GML/game package modified.']))
    print(json.dumps(dict(scenes=len(scenes),production_pngs=len(assets),independent_sprites=len(specs),view_slots=len(b['inventory_requests'])),ensure_ascii=False))
if __name__=='__main__':main()
