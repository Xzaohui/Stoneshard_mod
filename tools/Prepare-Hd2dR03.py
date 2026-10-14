"""Prepare all twelve R03 locations and their working interiors; scene art only."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'src/Art/hd2d_26x26_20261013/batches/R03-maen-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def rectcells(rs):return {(x,y) for a,b,c,d in rs for x in range(a,c+1) for y in range(b,d+1)}
def cells(s):return rectcells(s['walkable_rectangles'])-rectcells(s['blocked_rectangles'])
def point(k,x,y):return dict(id=k,cell=[x,y])
def obj(k,x,y,**kw):return dict(id='r03_'+k,cell=[x,y],**kw)
def scene(k,n,size,walk,block,exits,reserved,objects,**kw):
    return dict(id='r03_'+k,location='R03-'+k.split('_')[0],name_zh=n,cells=size,size=[a*26 for a in size],material=kw.pop('material','earth'),walkable_rectangles=walk,blocked_rectangles=block,exits=[point(*v) for v in exits],reserved=[point(*v) for v in reserved],objects=objects,**kw)
def main():
    for n in ['raw','images','animations','sheets','assets/backgrounds','assets/items','assets/tiles','assets/ui','guides','palettes','notes','previews','exports']:(P/n).mkdir(parents=True,exist_ok=True)
    ref=ROOT/'design/12_美术参考/城市概念/MAE-概念-v2.png';im=Image.open(ref).convert('RGB').quantize(colors=128,method=Image.Quantize.MEDIANCUT);pal=im.getpalette();colors=['#%02X%02X%02X'%tuple(pal[i*3:i*3+3]) for i in range(128)]
    write('palettes/mae_r03_128.json',dict(name='MAE-R03-128',colors=colors,source=ref.relative_to(ROOT).as_posix(),source_sha256=sha(ref),method='Median-cut128 from existing project AI concept, not a commercial atlas'))
    (P/'palettes/mae_r03_128.gpl').write_text('GIMP Palette\nName: MAE-R03-128\nColumns: 8\n#\n'+''.join('%d %d %d\t%s\n'%(*tuple(int(c[i:i+2],16) for i in [1,3,5]),c) for c in colors),encoding='utf-8')
    scenes=[
      scene('mill','旧磨坊站与雨棚',[40,30],[[2,3,37,27]],[[8,3,20,13]], [('depot',2,12),('ration',37,12),('hide',10,27),('scribe',29,27),('common',14,14)], [('neutral_copy',26,15),('rain_table',27,21),('water',25,25)], [obj('mill_house',14,14,roof=True),obj('public_table',26,13),obj('book_grain_stack',23,18),obj('water_barrel',25,23),obj('watch_shelter',27,19,roof=True),obj('copy_table',27,20)]),
      scene('ration','民粮站与公开退路',[38,28],[[2,3,35,25]],[[6,3,16,10]], [('mill',2,12),('field',35,20),('hall',11,11)], [('ordinary_supply',14,18),('public_meeting',26,14)], [obj('granary',11,11,roof=True),obj('grain_sacks',14,16),obj('public_table',26,12),obj('water_barrel',31,21)], conditional_objects=[obj('care_chair',27,14,condition='Actual SQ03 seating result only; preview is not story state')]),
      scene('library','低檐迁藏库与废库缺口',[40,30],[[2,3,37,27]],[[14,5,26,13]], [('hide',2,14),('formal_store',20,14),('waste_store',6,22),('unloading_return',37,24)], [('cold_brazier',10,20),('dry_receipt',30,23)], [obj('low_library',20,14,roof=True),obj('burned_frame',6,20),obj('cold_brazier',10,18),obj('book_grain_stack',29,21)]),
      scene('court','弃置试验庭与四个非对称附室',[44,34],[[2,3,41,5],[2,6,4,28],[39,6,41,28],[2,29,41,31],[12,9,31,26],[3,8,10,16],[33,4,41,17],[3,19,10,27],[33,22,40,30],[11,12,11,14],[32,12,32,15],[11,22,11,24],[32,23,32,25]],[], [('burnt',2,12),('scribe',41,24),('maintenance_return',39,30),('print_room',35,13),('shell_room',7,24)], [('seal_comparison',36,15),('feed_disconnect',7,26),('central_marks',21,18)], [obj('burned_frame',7,12),obj('seal_press',36,13),obj('copy_table',36,9),obj('empty_shell',7,22),obj('feed_lever',7,24),obj('water_barrel',36,27)], annexes=[dict(id='burnt',rect=[3,8,10,16],material='charred',window_direction='west'),dict(id='print',rect=[33,4,41,17],material='slate',window_direction='north'),dict(id='shell',rect=[3,19,10,27],material='boards',window_direction='west'),dict(id='maintenance',rect=[33,22,40,30],material='earth',window_direction='east')], optional_central_zone=[14,11,29,24]),
      scene('road','风雪驿道的常开步行带',[42,30],[[2,3,39,26]],[[4,3,11,8],[31,19,39,26]], [('border',2,20),('depot',39,11),('watch',20,26)], [('clear_road',20,16)], [obj('blank_waypost',20,14)], road_lines=[[[2,20],[18,15],[39,11]],[[18,15],[20,26]]]),
      scene('depot','受损集散点与滞留旧货',[40,30],[[2,3,37,27]],[[6,4,16,8],[29,5,34,10]], [('road',2,20),('mill',37,15)], [('old_stock',13,14),('unloading',25,20)], [obj('grain_sacks',13,12),obj('book_grain_stack',23,17),obj('water_barrel',28,23),obj('burned_frame',10,9)]),
      scene('hide','迁藏小路与书袋痕迹',[40,30],[[2,3,37,27]],[[2,3,10,7],[26,3,37,12],[2,19,10,27]], [('mill',2,14),('library',37,23),('burnt',25,27)], [('book_bag_trace',19,17)], [obj('book_grain_stack',19,15),obj('blank_waypost',25,24)], road_lines=[[[2,14],[18,12],[26,20],[37,23]],[[26,20],[25,27]]]),
      scene('burnt','烧毁旧屋与保留门框',[40,30],[[2,3,37,27]],[[5,5,15,10],[22,7,30,12]], [('hide',2,21),('court',37,22)], [('charred_frame',10,15),('ordinary_trace',26,19)], [obj('burned_frame',10,13),obj('book_grain_stack',26,17)], ruin_rectangles=[[5,5,15,10],[22,7,30,12]]),
      scene('field','民田围栏与开放收割带',[42,30],[[2,3,39,27]],[[7,6,14,8],[27,7,34,9]], [('ration',2,12),('watch',39,23)], [('crop_A',14,17),('crop_B',29,19),('tenant_meeting',22,24)], [obj('grain_sacks',22,22),obj('blank_waypost',5,13)], field_rectangles=[[8,11,18,21],[25,12,35,23]], fence_rectangles=[[6,5,19,23],[23,6,36,25]]),
      scene('watch','夜岗林缘与普通夜路',[40,30],[[2,3,37,27]],[[3,3,11,9],[29,4,37,16]], [('field',2,22),('road',24,3)], [('drain_inspection',26,20),('safe_watch',17,17)], [obj('watch_shelter',17,13,roof=True),obj('drain_trough',26,18),obj('blank_waypost',20,24)], road_lines=[[[2,22],[19,20],[24,3]]]),
      scene('scribe','抄写工棚与外侧会谈点',[38,28],[[2,3,35,25]],[[10,4,19,10]], [('court',2,16),('mill',35,18),('workroom',15,11)], [('outside_witness',27,19),('copy_transfer',24,14)], [obj('scribe_shed',15,11,roof=True),obj('copy_table',24,12),obj('book_grain_stack',28,17)]),
      scene('border','争议支路与三个跨区接口',[42,30],[[1,2,40,27]],[[1,2,9,8],[32,22,40,27]], [('R02_pending',1,20),('R04_pending',40,12),('R05_pending',28,27),('road',20,2)], [('route_notice',20,17)], [obj('blank_waypost',20,15)], road_lines=[[[1,20],[20,16],[40,12]],[[20,2],[20,16],[28,27]]]),
      scene('mill_common','磨坊释读桌与有限铺位',[30,24],[[3,4,26,21]],[[20,4,20,10],[20,14,20,18]], [('mill_return',3,19)], [('copy_table',12,15),('technical',24,9),('private_name',24,17),('bed_1',8,9),('bed_2',13,9)], [obj('bedroll',8,7),obj('bedroll',13,7),obj('copy_table',12,13),obj('technical_cabinet',24,7),obj('name_cabinet',24,15),obj('water_barrel',7,17)], material='boards',private_zone=[21,14,26,19],bed_capacity_proposal=2),
      scene('ration_hall','民粮公议桌与中立保存柜',[28,22],[[3,4,24,19]],[[18,4,18,10],[18,14,18,17]], [('ration_return',3,17)], [('public_table',10,13),('technical',8,9),('private_name',22,9),('care_chair_slot',13,13)], [obj('public_table',10,11),obj('technical_cabinet',8,7),obj('name_cabinet',22,7),obj('grain_sacks',8,16)], material='boards',private_zone=[19,4,24,10],conditional_objects=[obj('care_chair',13,13,condition='Actual SQ03 seating result only')]),
      scene('library_store','D04前廊、干区、侧封柜与低檐废库',[36,30],[[2,4,33,25]],[[10,5,10,11],[10,14,10,24],[20,5,20,11],[20,15,20,23],[3,17,8,17],[11,17,19,17]], [('formal_front',3,6),('waste_annex',3,23),('unloading_return',32,25)], [('technical_pages',29,9),('name_pages',29,20),('stop_request',16,9),('outside_copy',6,23)], [obj('technical_cabinet',29,7),obj('name_cabinet',29,18),obj('stop_cabinet',16,7),obj('copy_table',16,13),obj('book_grain_stack',6,21),obj('grain_sacks',15,22)], material='boards',zones=[dict(id='front',rect=[2,4,9,16]),dict(id='dry',rect=[11,18,19,25]),dict(id='sealed',rect=[21,4,33,24]),dict(id='waste',rect=[2,18,9,25])]),
      scene('court_print_room','D05印模间的封蜡对照桌',[24,18],[[3,4,20,14]],[[15,4,15,8]], [('perimeter_return',3,12)], [('seal',10,9),('copies',17,12),('fixed_cabinet',18,8)], [obj('seal_press',10,7),obj('copy_table',17,10),obj('stop_cabinet',18,6)], material='slate'),
      scene('court_shell_room','D05试验壳与徒手断供端',[26,22],[[3,4,22,18]],[[17,5,21,7]], [('perimeter_return',3,15),('maintenance_return',22,16)], [('empty_shell',11,11),('feed_disconnect',19,13)], [obj('empty_shell',11,9),obj('feed_lever',19,11),obj('water_barrel',8,16)], material='slate'),
      scene('scribe_room','抄写工棚内的双柜工作台',[26,20],[[3,4,22,17]],[[17,4,17,9],[17,13,17,16]], [('scribe_return',3,15)], [('technical',8,9),('name',20,9),('copy_table',12,14)], [obj('technical_cabinet',8,7),obj('name_cabinet',20,7),obj('copy_table',12,12),obj('book_grain_stack',7,15)], material='boards',private_zone=[18,4,22,10])]
    for s in scenes:
        if s['id']=='r03_court':
            s['blocked_rectangles'] += [[38,7,38,11],[38,14,38,17],[33,6,37,6],[38,22,38,24],[38,27,38,28],[34,28,37,28],[5,8,5,10],[5,13,5,16],[5,19,5,21],[5,25,5,27]]
            for a,r in zip(s['annexes'],[[6,8,10,15],[33,7,37,17],[6,19,10,27],[33,22,37,27]]):a['rect']=r
            next(o for o in s['objects'] if o['id']=='r03_feed_lever')['cell']=[8,25]
            next(e for e in s['reserved'] if e['id']=='feed_disconnect')['cell']=[9,26]
        if s['id']=='r03_scribe':next(e for e in s['exits'] if e['id']=='workroom')['cell']=[16,11]
        if s['id']=='r03_ration':s.pop('conditional_objects',None)
        s.update(origin=[0,0],cell_pixels=26,geometry_authority='Mod art grid proposal under R03 scripts, not native game geometry',runtime_verified=False)
        for i,o in enumerate(s['objects']+s.get('conditional_objects',[])):o['instance_id']=s['id']+'__'+o['id']+'__'+str(i)
        cs=cells(s);mask=Image.new('L',tuple(s['size']));d=ImageDraw.Draw(mask)
        for x,y in cs:d.rectangle((x*26,y*26,x*26+25,y*26+25),fill=255)
        mask.save(P/f"guides/{s['id']}_walkable.png")
        g=Image.new('RGB',tuple(s['size']),'#20252C');g.paste('#8C9395',(0,0),mask);gd=ImageDraw.Draw(g)
        for a,b,c,d1 in s['blocked_rectangles']:gd.rectangle((a*26,b*26,(c+1)*26-1,(d1+1)*26-1),fill='#45413E')
        archive=P/f"guides/{s['id']}_generation_v1.png"
        if not archive.exists():g.save(archive)
        for e in s['exits']:
            x,y=e['cell'];gd.rectangle((x*26+4,y*26+4,x*26+21,y*26+21),fill='#D6B879')
        for e in s['reserved']:
            x,y=e['cell'];gd.ellipse((x*26+6,y*26+6,x*26+20,y*26+20),fill='#9DE0B4')
        g.save(P/f"guides/{s['id']}_technical_plan.png")
    write('layouts.json',scenes)
    arch=[('mill_house',[312,338],[156,320]),('granary',[260,234],[130,216]),('low_library',[312,234],[156,216]),('scribe_shed',[208,182],[104,166]),('burned_frame',[156,182],[78,166]),('watch_shelter',[156,156],[78,140])]
    props=[('book_grain_stack',[78,78],[39,65]),('technical_cabinet',[52,104],[26,91]),('name_cabinet',[52,104],[26,91]),('stop_cabinet',[52,104],[26,91]),('copy_table',[130,78],[65,65]),('seal_press',[78,104],[39,91]),('empty_shell',[130,104],[65,91]),('feed_lever',[52,78],[26,65]),('grain_sacks',[78,78],[39,65]),('water_barrel',[52,78],[26,65]),('bedroll',[78,52],[39,43]),('public_table',[130,78],[65,65]),('care_chair',[52,78],[26,65]),('cold_brazier',[52,78],[26,65]),('blank_waypost',[52,78],[26,65]),('drain_trough',[104,52],[52,43])]
    sprites=[dict(id='r03_'+k,size=z,origin=o) for k,z,o in arch+props]
    names={s['location']:s['name_zh'] for s in scenes[:12]};nodecoords={'border':[5,8],'road':[18,8],'depot':[31,8],'mill':[33,21],'ration':[21,24],'field':[10,26],'watch':[7,17],'hide':[41,21],'library':[55,14],'burnt':[49,30],'court':[52,39],'scribe':[35,38]}
    source= json.loads((ROOT/'research/story-regions.json').read_text(encoding='utf-8'));region_source=next(x for x in source if x['id']=='R03')
    region=dict(id='r03_region',size=[1664,1248],display_cells=[64,48],authority='Original R03 topology; schematic display cells are not native world cells',runtime_verified=False,nodes=[dict(id='R03-'+k,cell=v,name_zh=names['R03-'+k]) for k,v in nodecoords.items()],edges=[['R03-'+a,'R03-'+b] for a,b in region_source['edges']],art_anchor_pixels={('R03-'+k):[x*26+13,y*26+13] for k,(x,y) in nodecoords.items()})
    write('region-layout.json',region);g=Image.new('RGB',(1664,1248),'#37433C');gd=ImageDraw.Draw(g)
    for a,b in region['edges']:gd.line([tuple(region['art_anchor_pixels'][a]),tuple(region['art_anchor_pixels'][b])],fill='#999D93',width=52)
    for x,y in region['art_anchor_pixels'].values():gd.rectangle((x-65,y-52,x+65,y+52),fill='#4D514D')
    if not (P/'guides/r03_region_generation_v1.png').exists():g.save(P/'guides/r03_region_generation_v1.png')
    requests={'R03__plan':'assets/backgrounds/r03_region__plan.png'}
    for s in scenes[:12]:
        requests[s['location']+'__plan']=f"assets/backgrounds/{s['id']}__plan.png"
        requests[s['location']+'__exterior_or_site']=f"assets/backgrounds/{s['id']}__environment.png"
    requests['R03-library__plan']='assets/backgrounds/r03_library__plan_overview.png';requests['R03-library__interior_or_working_space']='assets/backgrounds/r03_library_store__environment.png';requests['R03-court__interior_or_working_space']='assets/backgrounds/r03_court__working_overview.png'
    sources=['research/story-regions.json','design/02_世界与地图/区域_R03_曼恩边地.md','design/08_副本/台本/台本_D04_曼恩封存书库.md','design/08_副本/台本/台本_D05_学院弃置试验庭.md','design/05_主线/台本/台本_N6_被封存的页码.md','design/05_主线/台本/台本_N10_没有写下的见证.md','design/06_支线/台本/台本_SQ03_没有王旗的面包.md','design/06_支线/台本/台本_SQ06_抄本的背面.md','design/07_日常任务/台本/台本_DT04_收割前的空地.md','design/07_日常任务/台本/台本_DT10_别让狼靠近夜岗.md','design/07_日常任务/台本/台本_DT11_两份抄本的交接.md',ref.relative_to(ROOT).as_posix()]
    write('brief.json',dict(schema=1,batch='R03-maen-v1',scope='Scene art only; NPC model owns people/dialogue/events',palette='MAE-R03-128',skill_commit='33d891c421a9ad3608f5a09af97271388ca923af',source_sha256={n:sha(ROOT/n) for n in sources},sprites=sprites,inventory_requests=requests,runtime_verified=False))
    lock='# Execution Lock — R03 Maen\n\n## authorization\nUser continues all scene work on2026-10-14. Previously confirmed26-cell static HD2D,128 regional palette, native PNG import and separate roofs continue. No NPC work.\n\n## canvas\n- base_size: 26x26\n- tile_size: 26x26\n- format: RGBA PNG\n'
    for s in scenes:lock+=f"- {s['id']}: {s['size'][0]}x{s['size'][1]}\n"
    lock+='- materials_master: 1536x1536, four768x768panels\n- architecture_master: 1536x1024, six512x512slots\n- props_a_master: 1536x1024, eight384x512slots\n- props_b_master: 1536x1024, eight384x512slots\n- interiors_master: 1536x1024, three512x1024panels\n- landscape_master: 1536x1536, four768x768panels\n- r03_region: 1664x1248, schematic only\n- r03_library__plan_overview: 1040x1586, two1:1scene plans\n- r03_court__working_overview: 1300x598, two1:1interiors\n'
    for s in sprites:lock+=f"- {s['id']}: {s['size'][0]}x{s['size'][1]}, origin {s['origin']}, transparent static sprite\n"
    lock+='\n## palette\n- name: MAE-R03-128\n- colors:\n'+''.join('  - '+c+'\n' for c in colors)
    lock+='\n## style\n- sub_style: textured HD-2D, square-grid orthographic oblique\n- light_direction: top-left\n- lighting: unlit static base; dynamic fire separate\n- materials: cold gray stone, wet dark wood, faded blue cloth, muted earth and sparse frost at nonwalkable edges\n\n## per_sprite_budget\n- max_colors: 128\n\n## invariants\n- D04store36x30 cells with front porch, dry grain zone, three separate cabinets and waste annex. Formal front permission cannot remove the alternate waste entrance or unloading return.\n- D05court44x34, open center and four asymmetric annexes with differing floor/window directions. Outer return stays accessible with central demonstration closed or feed unavailable.\n- Mill limited bedding proposal=2, not a paid service/runtime claim. Two neutral technical copy sites at mill/ration; identity stays in separate cabinets.\n- Extra care chair conditional and off by default. No consent/NE certification, cure, faction control, transport or burned-record outcome baked into images.\n- No people,NPCs,wolves,corpses,readable text,UI,flags,flames,light glows,active spell machines or tropical vegetation. No thriving open academy.\n- Floors/occupancy explicit; alpha is never collision. Roofs/foreground separate. Raw masters immutable. Crop/NN normalization/exact palette/binary alpha/tile edge copy are authorized postprocessing.\n'
    (P/'spec_lock.md').write_text(lock,encoding='utf-8')
    heads=['I. Project Information','II. Canvas Specification','III. Color Palette','IV. Art Style Definition','V. Asset List','VI. Animation Specification','VII. Technical Constraints','VIII. Platform Export Notes'];vals=['R03曼恩边地，全十二节点及工作室内。','18场景；D04=36×30、D05=44×34；26像素格。','MAE-R03-128，源Mod概念图提取。','冷灰石、湿黑木、旧蓝布，左上基础光。','十二场地、六室内、22独立建筑/物件、四类材料瓦片。','静态单帧。','三柜、替代入口、外围回程；追加椅子默认关闭。','PNG、相对路径、脚底原点和显式格方案；游戏接口未验证。']
    (P/'design_spec.md').write_text('# Purple Crystal HD-2D — R03 Maen\n\n'+'\n\n'.join('## '+a+'\n\n'+b for a,b in zip(heads,vals))+'\n',encoding='utf-8')
    print(json.dumps(dict(batch=str(P.relative_to(ROOT)),scenes=len(scenes),sprites=len(sprites),view_slots=len(requests)),ensure_ascii=False))
if __name__=='__main__':main()
