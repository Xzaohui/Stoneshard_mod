"""Scene-only R02 production contract; explicit proposed grids, no NPC implementation."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];PARENT=ROOT/'src/Art/hd2d_26x26_20261013';P=PARENT/'batches/R02-river-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rectcells(rects):return {(x,y) for a,b,c,d in rects for y in range(b,d+1) for x in range(a,c+1)}
def cells(s):return rectcells(s['walkable_rectangles'])-rectcells(s['blocked_rectangles'])-rectcells(s.get('cutout_rectangles',[]))
def obj(k,x,y,**kw):return dict(id=k,cell=[x,y],**kw)
def point(k,x,y):return dict(id=k,cell=[x,y])
def main():
    for n in ['raw','images','animations','sheets','assets/backgrounds','assets/items','assets/tiles','assets/ui','guides','palettes','notes','previews','exports']:(P/n).mkdir(parents=True,exist_ok=True)
    ref=ROOT/'design/12_美术参考/城市概念/DEN-概念-v1.png';im=Image.open(ref).convert('RGB').quantize(colors=128,method=Image.Quantize.MEDIANCUT)
    pal=im.getpalette();colors=['#%02X%02X%02X'%tuple(pal[i*3:i*3+3]) for i in range(128)]
    write('palettes/den_r02_128.json',dict(name='DEN-R02-128',colors=colors,source=ref.relative_to(ROOT).as_posix(),source_sha256=sha(ref),method='Pillow median cut128 from existing project AI concept, no commercial atlas copy'))
    (P/'palettes/den_r02_128.gpl').write_text('GIMP Palette\nName: DEN-R02-128\nColumns: 8\n#\n'+''.join('%d %d %d\t%s\n'%(*tuple(int(c[i:i+2],16) for i in [1,3,5]),c) for c in colors),encoding='utf-8')
    scenes=[
      dict(id='r02_inn_exterior',location='R02-inn',name_zh='渡口客店岸院',cells=[40,30],material='gravel',walkable_rectangles=[[3,4,36,26]],blocked_rectangles=[[7,5,18,10]],exits=[point('fork',3,9),point('well',11,26),point('tracks',36,9),point('ford',36,24),point('common_room',13,11)],reserved=[point('public_entry',13,13),point('ordinary_supply',25,16)],objects=[obj('r02_ferry_inn',13,11,roof=True),obj('r02_road_sign',24,15),obj('r02_mooring_post',20,25)]),
      dict(id='r02_inn_common',location='R02-inn',name_zh='渡口客店公共桌与分柜',cells=[32,26],material='boards',walkable_rectangles=[[3,4,28,22]],blocked_rectangles=[[22,5,27,7],[20,8,20,12],[20,15,20,18]],exits=[point('inn_return',3,20)],reserved=[point('public_table',12,13),point('case_ledger',24,17),point('private_name_cabinet',25,13),point('soup_service',25,10)],objects=[obj('r02_public_table',12,11),obj('r02_privacy_screen',21,13),obj('r02_case_cabinet',24,15),obj('r02_name_cabinet',25,11),obj('r02_soup_stove',25,8)],private_zone=[21,8,28,18]),
      dict(id='r02_well',location='R02-well',name_zh='渡民岸井与过滤架',cells=[40,30],material='grass',walkable_rectangles=[[3,4,36,26],[17,27,21,28]],blocked_rectangles=[[14,5,20,7],[30,7,33,10]],exits=[point('inn',3,9),point('ferryold',19,28)],reserved=[point('filter_inspection',17,12),point('sample_A',9,24),point('sample_B',19,22),point('sample_C',28,25),point('anonymous_case',31,16),point('private_name',33,13)],objects=[obj('r02_filter_shelter',17,10,roof=True),obj('r02_filter_rack',17,10),obj('r02_sample_bucket',9,22),obj('r02_sample_bucket',19,20),obj('r02_sample_bucket',28,23),obj('r02_case_cabinet',31,14),obj('r02_name_cabinet',33,11)]),
      dict(id='r02_tracks',location='R02-tracks',name_zh='河岸轮印带',cells=[42,30],material='grass',walkable_rectangles=[[2,3,39,26]],blocked_rectangles=[[4,5,10,7],[31,20,35,22]],exits=[point('inn',2,9),point('tax',39,23)],reserved=[point('wheel_tracks',20,14),point('clamp_traces',28,21),point('mooring',12,26)],objects=[obj('r02_crate_corner',28,19),obj('r02_mooring_post',12,24)]),
      dict(id='r02_repair',location='R02-repair',name_zh='护路维修坡与步行回路',cells=[42,30],material='grass',walkable_rectangles=[[2,3,16,26],[28,3,39,26],[17,20,27,22],[17,9,21,11],[25,9,27,11]],blocked_rectangles=[[5,4,12,8]],exits=[point('tax',39,6),point('ford',2,24)],reserved=[point('bridge_inspect',16,12),point('ordinary_repair',12,17),point('permanent_return',21,21)],objects=[obj('r02_repair_canopy',9,9,roof=True),obj('r02_repair_timbers',11,15),obj('r02_road_sign',28,24)],water_rectangles=[[17,3,27,26]],bridge_rectangles=[[17,20,27,22],[17,9,21,11],[25,9,27,11]],repair_add_rectangles=[[22,9,24,11]]),
      dict(id='r02_ford',location='R02-ford',name_zh='浅滩路标带',cells=[42,30],material='grass',walkable_rectangles=[[2,3,13,26],[29,3,39,26],[14,19,20,21],[19,13,23,21],[23,13,28,15]],blocked_rectangles=[],exits=[point('repair',39,7),point('inn',2,7),point('fork',2,23)],reserved=[point('fixed_ford',21,17),point('waymark',12,21)],objects=[obj('r02_road_sign',12,19)],water_rectangles=[[14,3,28,26]],ford_rectangles=[[14,19,20,21],[19,13,23,21],[23,13,28,15]]),
      dict(id='r02_fork',location='R02-fork',name_zh='西路分岔',cells=[40,30],material='grass',walkable_rectangles=[[1,2,38,27]],blocked_rectangles=[[1,2,8,5],[31,21,38,27]],exits=[point('R01_interface_pending',1,18),point('R03_interface_pending',19,2),point('R04_interface_pending',38,8),point('inn',38,18),point('ford',19,27)],reserved=[point('blank_sign',19,16)],objects=[obj('r02_road_sign',19,14)]),
      dict(id='r02_tax_main',location='R02-tax',name_zh='断桥税栈主段',cells=[42,32],material='gravel',walkable_rectangles=[[2,2,39,10],[2,25,39,29],[5,10,7,25]],blocked_rectangles=[[18,4,27,9]],exits=[point('tracks',2,7),point('repair',39,27),point('yard_permit',23,10),point('yard_ford',7,25),point('tax_office',23,10)],reserved=[point('ford_inspection',6,17),point('bridge_trace',25,15),point('safe_entry',4,7)],objects=[obj('r02_tax_house',23,10,roof=True),obj('r02_mooring_post',10,27)],water_rectangles=[[2,11,39,24]],ford_rectangles=[[5,10,7,25]],bridge_rectangles=[],repair_add_rectangles=[]),
      dict(id='r02_tax_yard',location='R02-tax',name_zh='税栈暂存院与卸货台',cells=[30,22],material='gravel',walkable_rectangles=[[2,3,27,19]],blocked_rectangles=[[6,4,13,6],[21,4,25,7]],exits=[point('main_permit',2,8),point('main_ford',2,16),point('lower_embankment_return',27,17)],reserved=[point('limited_inspection',10,12),point('clamp_corner',22,13),point('unoccupied_actor_zone',16,12)],objects=[obj('r02_inspection_shed',10,7,roof=True),obj('r02_inspection_table',10,10),obj('r02_crate_corner',22,11),obj('r02_case_cabinet',24,8)]),
      dict(id='r02_tax_office',location='R02-tax',name_zh='税房有限查验工作间',cells=[24,18],material='boards',walkable_rectangles=[[3,4,20,14]],blocked_rectangles=[[16,5,19,6]],exits=[point('main_return',3,12)],reserved=[point('permit_desk',12,10),point('limited_case_cabinet',18,9)],objects=[obj('r02_inspection_table',12,8),obj('r02_case_cabinet',18,7)])]
    scenes[2]['cutout_rectangles']=[[7,24,8,26],[18,24,18,26],[28,25,29,26]]
    next(e for e in scenes[2]['reserved'] if e['id']=='sample_B')['cell']=[19,24]
    next(e for e in scenes[2]['reserved'] if e['id']=='sample_C')['cell']=[27,25]
    scenes[2]['blocked_rectangles'] += [[16,8,18,9]]
    next(o for o in scenes[1]['objects'] if o['id']=='r02_case_cabinet')['cell']=[18,17]
    next(e for e in scenes[1]['reserved'] if e['id']=='case_ledger')['cell']=[18,19]
    next(o for o in scenes[1]['objects'] if o['id']=='r02_soup_stove')['cell']=[8,8]
    next(e for e in scenes[1]['reserved'] if e['id']=='soup_service')['cell']=[8,10]
    tax=scenes[7]
    next(e for e in tax['exits'] if e['id']=='yard_permit')['cell']=[32,8]
    next(e for e in tax['exits'] if e['id']=='tax_office')['cell']=[22,10]
    for x in range(22,36):
        y=10+round((x-22)*15/13);r=[x,y-1,x,y+1];tax['walkable_rectangles'].append(r);tax['bridge_rectangles'].append(r)
    tax['blocked_rectangles'] += [[28,16,30,20]]
    tax['repair_add_rectangles']=[[28,16,28,18],[29,17,29,19],[30,18,30,20]]
    # The observation cell is on the existing upper broken bridge section.
    tax['reserved'][1]['cell']=[26,15]
    sprites=[dict(id=k,size=z,origin=o) for k,z,o in [
      ('r02_ferry_inn',[312,260],[156,242]),('r02_tax_house',[260,234],[130,216]),('r02_filter_shelter',[156,156],[78,140]),('r02_repair_canopy',[208,156],[104,140]),('r02_inspection_shed',[208,182],[104,166]),('r02_bridge_pier',[78,130],[39,117]),
      ('r02_public_table',[130,78],[65,65]),('r02_privacy_screen',[78,104],[39,91]),('r02_case_cabinet',[52,78],[26,65]),('r02_name_cabinet',[52,78],[26,65]),('r02_filter_rack',[104,104],[52,91]),('r02_sample_bucket',[26,26],[13,23]),('r02_mooring_post',[52,78],[26,65]),('r02_crate_corner',[52,52],[26,43]),('r02_repair_timbers',[104,52],[52,43]),('r02_soup_stove',[78,104],[39,91]),('r02_road_sign',[52,78],[26,65]),('r02_inspection_table',[78,52],[39,45])]]
    for s in scenes:
        s.update(size=[v*26 for v in s['cells']],cell_pixels=26,origin=[0,0],geometry_authority='Authored art grid proposal under R02 screenplay constraints, not a native room',runtime_verified=False)
        cs=cells(s);mask=Image.new('L',tuple(s['size']));d=ImageDraw.Draw(mask)
        for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
        mask.save(P/f'guides/{s["id"]}_walkable.png');g=Image.new('RGB',tuple(s['size']),'#20363A');g.paste('#A29474',(0,0),mask);gd=ImageDraw.Draw(g)
        for a,b,c,e in s['blocked_rectangles']:
            colour='#20363A' if s['id']=='r02_tax_main' and [a,b,c,e]==[28,16,30,20] else '#4C3C2F'
            gd.rectangle((a*26,b*26,(c+1)*26-1,(e+1)*26-1),fill=colour)
        g.save(P/f'guides/{s["id"]}_geometry.png')
        for e in s['exits']:
            x,y=e['cell'];gd.rectangle((x*26+4,y*26+4,x*26+21,y*26+21),fill='#E7AF52')
        for e in s['reserved']:
            x,y=e['cell'];gd.ellipse((x*26+6,y*26+6,x*26+20,y*26+20),fill='#9DE0B4')
        g.save(P/f'guides/{s["id"]}_technical_plan.png')
        for i,o in enumerate(s['objects']):o['instance_id']=s['id']+'__'+o['id']+'__'+str(i)
    write('layouts.json',scenes)
    region=dict(id='r02_region',size=[1664,1248],display_cells=[64,48],authority='Original R02 topology schematic; display coordinates are not native world coordinates',runtime_verified=False,
      nodes=[dict(id=k,cell=c,name_zh=n) for k,c,n in [('R02-fork',[8,16],'西路分岔'),('R02-inn',[27,20],'渡口客店'),('R02-well',[26,8],'渡民岸井'),('R02-ferryold',[9,6],'旧渡口'),('R02-tracks',[39,14],'河岸轮印带'),('R02-tax',[52,20],'断桥税栈'),('R02-repair',[49,34],'护路维修坡'),('R02-ford',[25,34],'浅滩路标带')]],
      edges=[['R02-fork','R02-inn'],['R02-inn','R02-well'],['R02-well','R02-ferryold'],['R02-inn','R02-tracks'],['R02-tracks','R02-tax'],['R02-tax','R02-repair'],['R02-repair','R02-ford'],['R02-ford','R02-inn'],['R02-ford','R02-fork']])
    write('region-layout.json',region);g=Image.new('RGB',(1664,1248),'#20363A');d=ImageDraw.Draw(g);d.rectangle((0,0,1663,1040),fill='#6F6153');lookup={n['id']:[v*26+13 for v in n['cell']] for n in region['nodes']}
    for a,b in region['edges']:d.line([tuple(lookup[a]),tuple(lookup[b])],fill='#A39277',width=52)
    for x,y in lookup.values():d.rectangle((x-65,y-52,x+65,y+52),fill='#4C3C2F')
    g.save(P/'guides/r02_region_geometry.png')
    sources=['research/story-regions.json','design/02_世界与地图/区域_R02_丹布里西路与渡口.md','design/08_副本/台本/台本_D03_断桥税栈.md','design/05_主线/台本/台本_N5_渡口的三种说法.md','design/05_主线/台本/台本_N9_把证据摆上桌.md','design/05_主线/台本/台本_N18_誓约之后.md','design/06_支线/台本/台本_SQ04_一条不卖人的路.md','design/06_支线/台本/台本_SQ05_渡口与姓名.md','design/12_美术参考/城市概念/DEN-概念-v1.png']
    requests={'R02__plan':'assets/backgrounds/r02_region__plan.png'}
    for s in [scenes[i] for i in [0,2,3,4,5,6]]:
        for view,suffix in [('plan','plan'),('exterior_or_site','environment')]:requests[s['location']+'__'+view]=f'assets/backgrounds/{s["id"]}__{suffix}.png'
    requests.update({'R02-tax__plan':'assets/backgrounds/r02_tax__plan_overview.png','R02-tax__exterior_or_site':'assets/backgrounds/r02_tax_main__environment.png','R02-tax__interior_or_working_space':'assets/backgrounds/r02_tax__working_overview.png','R02-ferryold__plan':'assets/backgrounds/r02_ferryold__plan_overview.png','R02-ferryold__exterior_or_site':'assets/backgrounds/r02_ferryold__site.png'})
    write('brief.json',dict(schema=1,batch='R02-river-v1',palette='DEN-R02-128',scope='Only scene art; NPC model owns people/dialogue/state events',skill_commit='33d891c421a9ad3608f5a09af97271388ca923af',source_sha256={n:sha(ROOT/n) for n in sources},sprites=sprites,inventory_requests=requests,runtime_verified=False))
    lock='# Execution Lock — R02 River\n\n## authorization\nContinued by user2026-10-13; approved26-cell static HD2D workflow and reference-derived128 regional colors continue. NPC work belongs to another model.\n\n## canvas\n- base_size: 26x26\n- tile_size: 26x26\n- format: RGBA PNG\n'
    for s in scenes:lock+=f'- {s["id"]}: {s["size"][0]}x{s["size"][1]}\n'
    lock+='- materials_master: 1536x1536, four768x768texture panels\n- architecture_master: 1536x1024, six512x512slots\n- props_master: 2048x1536, twelve512x512slots\n- interiors_master: 1536x1024, two768x1024panels\n- r02_region: 1664x1248 schematic, not a native world map\n- r02_crate_corner_detail: 208x208, inspection artwork only\n'
    for s in sprites:lock+=f'- {s["id"]}: {s["size"][0]}x{s["size"][1]}, origin {s["origin"]}, transparent static frame\n'
    lock+='\n## palette\n- name: DEN-R02-128\n- colors:\n'+''.join('  - '+c+'\n' for c in colors)
    lock+='\n## style\n- sub_style: textured HD-2D, square-grid orthographic oblique\n- materials: pale limestone, damp green grass, muddy ruts, brown timber, dark blue/teal river\n- light_direction: top-left\n- lighting: static unlit base, dynamic sources separate\n\n## per_sprite_budget\n- max_colors: 128\n\n## invariants\n- D03 main42x32 and yard30x22 cells; diagonal bridge with broken span, persistent fixed ford and return route. Repair adds bridge cells and never removes ford.\n- Basic pedestrian paths stay open independently of toll or story outcome; no native world coordinates are claimed.\n- Inn public table and private names/case cabinets separated; no personal details or invented hotel bed capacity.\n- Well has three fixed sample points and separate anonymous-case/name cabinets. Filtering does not depict completed cure or consent.\n- Ruts/clamp traces indicate inspectable shapes only, not certified evidence or a selected narrative route.\n- No NPCs, people, dialogue, monsters, corpses, readable text, labels, UI, flames, glow or story completion baked into scenery.\n- Floor masks and occupancy explicit; alpha is never collision. Roofs and foreground separate.\n- Raw masters immutable; documented crops, nearest-neighbor normalization, exact palette, binary alpha and tile-edge copying are authorized production postprocessing.\n'
    (P/'spec_lock.md').write_text(lock,encoding='utf-8')
    sections=['I. Project Information','II. Canvas Specification','III. Color Palette','IV. Art Style Definition','V. Asset List','VI. Animation Specification','VII. Technical Constraints','VIII. Platform Export Notes']
    values=['R02丹布里西路与渡口，场景绘制，不接NPC逻辑。','十张局部场景与区域图；26格规格见spec_lock。','DEN-R02-128从既有Mod概念提取，固定后逐像素核验。','正交斜俯视HD2D，左上基础光。','河岸、分岔、客店室内外、岸井、断桥两岸、暂存院及税房。','静态单帧。','D03尺寸与永久浅滩保留；私密柜隔断、三取样点和修复对比。','相对PNG路径、独立精灵和原点、分层/显式格方案；原生装配未验证。']
    (P/'design_spec.md').write_text('# Purple Crystal HD-2D — R02 River\n\n'+'\n\n'.join('## '+a+'\n\n'+b for a,b in zip(sections,values))+'\n',encoding='utf-8')
    print(json.dumps(dict(batch=str(P.relative_to(ROOT)),scenes=len(scenes),sprites=len(sprites),view_slots=len(requests)),ensure_ascii=False))
if __name__=='__main__':main()
