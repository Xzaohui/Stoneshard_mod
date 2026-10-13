"""Prepare the remaining R01 locations; scene geometry only, no NPC edits."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1];PARENT=ROOT/'src/Art/hd2d_26x26_20261013'
P=PARENT/'batches/R01-streets-v1';OLD=PARENT/'batches/R01-camp-canal-v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,v):(P/n).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    for n in ['raw','images','animations','sheets','assets/backgrounds','assets/items','guides','palettes','notes','previews','exports']:(P/n).mkdir(parents=True,exist_ok=True)
    for n in ['bry_r01_128.json','bry_r01_128.gpl']:(P/'palettes'/n).write_bytes((OLD/'palettes'/n).read_bytes())
    scenes=[
      dict(id='r01_port',location='R01-port',name_zh='港街复核亭',size=[1040,780],cells=[40,30],walkable_rectangles=[[3,4,35,25]],blocked_rectangles=[[8,5,17,7],[27,7,33,10]],exits=[dict(id='salt',cell=[3,22]),dict(id='camp',cell=[35,7]),dict(id='hearing',cell=[35,22])],reserved=[dict(id='public_notice',cell=[8,14]),dict(id='kiosk_front',cell=[13,11]),dict(id='water',cell=[27,20]),dict(id='limited_storage',cell=[31,14])],objects=[dict(id='r01_port_kiosk',cell=[13,11],roof=True),dict(id='r01_notice_board',cell=[7,12]),dict(id='r01_water_basin',cell=[27,18]),dict(id='r01_storage_chest',cell=[31,12])]),
      dict(id='r01_hearing',location='R01-hearing',name_zh='听审棚与熄灯租屋外巷',size=[1040,780],cells=[40,30],walkable_rectangles=[[4,4,35,25]],blocked_rectangles=[[8,5,18,7],[27,6,34,10]],exits=[dict(id='camp',cell=[4,8]),dict(id='workshop',cell=[35,22]),dict(id='port',cell=[4,22]),dict(id='rental_private',cell=[31,13])],reserved=[dict(id='hearing_table',cell=[14,15]),dict(id='public_notice',cell=[8,20]),dict(id='private_route',cell=[26,15])],objects=[dict(id='r01_hearing_canopy',cell=[14,11],roof=True),dict(id='r01_rental_house',cell=[31,13],roof=True),dict(id='r01_twin_ledger_table',cell=[14,13]),dict(id='r01_notice_board',cell=[8,18])]),
      dict(id='r01_workshop',location='R01-workshop',name_zh='堤外器具工坊与弃置驿站',size=[1040,780],cells=[40,30],walkable_rectangles=[[4,4,35,25]],blocked_rectangles=[[7,5,16,8],[28,6,34,8],[9,12,11,13]],exits=[dict(id='canal',cell=[4,22]),dict(id='hearing',cell=[35,8])],reserved=[dict(id='forge_front',cell=[12,14]),dict(id='basic_repair',cell=[29,21]),dict(id='stamp_inspection',cell=[31,14])],objects=[dict(id='r01_forge_building',cell=[12,12],roof=True),dict(id='r01_abandoned_post',cell=[31,11],roof=True),dict(id='r01_stamp_bench',cell=[31,12]),dict(id='r01_basic_repair_bench',cell=[29,19])]),
      dict(id='r01_salt',location='R01-salt',name_zh='盐车道',size=[1040,780],cells=[40,30],walkable_rectangles=[[1,1,38,28]],blocked_rectangles=[[1,22,8,28],[31,1,38,3]],exits=[dict(id='R02_interface_pending',cell=[1,18]),dict(id='port',cell=[38,8])],reserved=[dict(id='road_observation',cell=[19,14])],objects=[]),
      dict(id='r01_rental',location='R01-hearing',name_zh='熄灯租屋工作间',size=[624,520],cells=[24,20],walkable_rectangles=[[3,4,20,16]],blocked_rectangles=[[18,5,19,6]],exits=[dict(id='hearing_private_return',cell=[4,15])],reserved=[dict(id='desk',cell=[12,12]),dict(id='drying_pages',cell=[9,8]),dict(id='stove_inspect',cell=[17,7])],objects=[dict(id='r01_twin_ledger_table',cell=[12,10]),dict(id='r01_drying_rack',cell=[9,6]),dict(id='r01_ash_stove',cell=[18,6])])]
    # Production occupancy follows the normalized building bodies. Generation
    # input guides before these refinements remain archived as *_generation_v1.
    scenes[0]['blocked_rectangles']=[[8,5,17,10],[27,7,33,10]]
    scenes[1]['blocked_rectangles']=[[8,5,18,7],[8,10,8,11],[19,10,19,11],[27,6,34,12]]
    scenes[2]['blocked_rectangles']=[[7,5,16,11],[28,6,34,10],[9,12,11,13]]
    next(o for o in scenes[2]['objects'] if o['id']=='r01_stamp_bench')['cell']=[31,15]
    next(o for o in scenes[2]['reserved'] if o['id']=='stamp_inspection')['cell']=[31,17]
    next(o for o in scenes[4]['objects'] if o['id']=='r01_ash_stove')['cell']=[18,7]
    scenes[4]['exits'][0]['cell']=[4,16]
    for s in scenes:
        s.update(cell_pixels=26,origin=[0,0],geometry_authority='Original art geometry proposal, not native game geometry',implementation_verified=False,runtime_verified=False)
        im=Image.new('L',tuple(s['size']));d=ImageDraw.Draw(im)
        for a,b,c,e in s['walkable_rectangles']:d.rectangle((a*26,b*26,(c+1)*26-1,(e+1)*26-1),fill=255)
        for a,b,c,e in s['blocked_rectangles']:d.rectangle((a*26,b*26,(c+1)*26-1,(e+1)*26-1),fill=0)
        im.save(P/f'guides/{s["id"]}_walkable.png')
        g=Image.new('RGB',tuple(s['size']),'#20363A');g.paste('#A29474',(0,0),im)
        gd=ImageDraw.Draw(g)
        for a,b,c,e in s['blocked_rectangles']:gd.rectangle((a*26,b*26,(c+1)*26-1,(e+1)*26-1),fill='#4C3C2F')
        g.save(P/f'guides/{s["id"]}_geometry.png')
        d=ImageDraw.Draw(g)
        for e in s['exits']:
            x,y=e['cell'];d.rectangle((x*26+4,y*26+4,x*26+21,y*26+21),fill='#E7AF52')
        for e in s['reserved']:
            x,y=e['cell'];d.ellipse((x*26+6,y*26+6,x*26+20,y*26+20),fill='#9DE0B4')
        g.save(P/f'guides/{s["id"]}_technical_plan.png')
    write('layouts.json',scenes)
    sprites=[dict(id=k,size=s,origin=o) for k,s,o in [
      ('r01_port_kiosk',[260,208],[130,190]),('r01_hearing_canopy',[312,208],[156,190]),('r01_rental_house',[260,234],[130,216]),('r01_forge_building',[260,234],[130,216]),('r01_abandoned_post',[182,156],[91,140]),
      ('r01_notice_board',[52,78],[26,65]),('r01_twin_ledger_table',[78,52],[39,45]),('r01_stamp_bench',[52,52],[26,43]),('r01_basic_repair_bench',[78,52],[39,45]),('r01_storage_chest',[52,52],[26,43]),('r01_drying_rack',[78,78],[39,65]),('r01_ash_stove',[52,78],[26,65]),('r01_water_basin',[52,52],[26,43])]]
    sources=['research/story-regions.json','design/02_世界与地图/区域_R01_布林外港与旧渠.md','design/05_主线/台本/台本_N3_听审前的灯.md','design/05_主线/台本/台本_N4_第一张空白债票.md','design/06_支线/台本/台本_SQ01_港税与自由.md','design/12_美术参考/城市概念/BRY-概念-v1.png']
    requests={}
    for s in scenes[:4]:
        requests[s['location']+'__plan']=f'assets/backgrounds/{s["id"]}__plan.png'
        requests[s['location']+'__exterior_or_site']=f'assets/backgrounds/{s["id"]}__environment.png'
    requests['R01__plan']='assets/backgrounds/r01_region__plan.png'
    write('brief.json',dict(schema=1,batch='R01-streets-v1',scope='Scene drawing only; NPC work belongs to the other model',source_sha256={n:sha(ROOT/n) for n in sources},sprites=sprites,inventory_requests=requests,runtime_verified=False))
    colors=json.loads((P/'palettes/bry_r01_128.json').read_text(encoding='utf-8'))['colors']
    lock='# Execution Lock — R01 Streets\n\n## authorization\nPreviously confirmed HD2D style and six parameters, continued by user 2026-10-13; scenes only.\n\n## canvas\n- base_size: 26x26\n- tile_size: 26x26\n- format: RGBA PNG\n'
    for s in scenes:lock+=f'- {s["id"]}: {s["size"][0]}x{s["size"][1]}\n'
    lock+='- r01_region: 1664x1248 regional schematic artwork; not a native walkable room, actual world coordinates pending\n- architecture_master: 1536x1024, 3x2 isolated structures; five populated slots\n- props_master: 1536x1536, 3x3 isolated props; eight populated slots\n'
    for s in sprites:lock+=f'- {s["id"]}: {s["size"][0]}x{s["size"][1]}, origin {s["origin"]}, one static frame, transparent\n'
    lock+='\n## palette\n- name: BRY-R01-128\n- colors:\n'+''.join('  - '+c+'\n' for c in colors)
    lock+='\n## style\n- sub_style: textured HD-2D, square-grid orthographic oblique\n- materials: salt-grey stone, brown timber, wet brick, dull russet shingles, muted earth and teal water\n- light_direction: top-left\n- lighting: static unlit base, dynamic sources separate\n\n## per_sprite_budget\n- max_colors: 128\n\n## invariants\n- Public hearing is a local labor review, not a formal Brynn court. Separate public space and private rental access.\n- Rental includes a desk, drying pages and cold stove, no invented bedroom capacity.\n- Basic repair bench remains distinct from the large furnace and printing bench. No route outcome, sold assets or active flames baked in.\n- Notices/pages are blank shapes; text and states use engine fonts/logic. Storage is appearance only, not inventory/loot quantities.\n- Salt road has a continuous dry walking route; world interface coordinates are pending, never present the diagram as official geography.\n- Region overview follows the seven declared R01 topology edges, not measured global distances.\n- No people/NPCs, dialogue, actors, corpses, readable text, labels, UI, purple glow or arbitrary extra doors baked into art.\n- Explicit floor masks and authored occupancy; no collisions inferred from alpha. Roofs and foreground separate.\n- Raw masters immutable; documented crops, nearest-neighbor normalization, exact palette and binary alpha are authorized post-processing.\n'
    (P/'spec_lock.md').write_text(lock,encoding='utf-8')
    titles=['I. Project Information','II. Canvas Specification','III. Color Palette','IV. Art Style Definition','V. Asset List','VI. Animation Specification','VII. Technical Constraints','VIII. Platform Export Notes']
    texts=['R01余下四节点及租屋工作间；仅场景制作。','26格；画布与各独立精灵规格见spec_lock。','沿用BRY-R01-128固定色板。','原作方向的正交斜俯视HD-2D，左上基础光。','地图、建筑、工作空间、独立环境物件与区域示意图。','单帧静态；灯光和机关后续由引擎处理。','门点、授权边界和普通修理保持；几何为制作提案。','RGBA PNG与相对清单、原点、遮挡分层；实际游戏装配待验证。']
    (P/'design_spec.md').write_text('# Purple Crystal HD-2D — R01 Streets\n\n'+'\n\n'.join('## '+a+'\n\n'+b for a,b in zip(titles,texts))+'\n',encoding='utf-8')
    print(json.dumps(dict(batch=str(P.relative_to(ROOT)),scenes=len(scenes),sprites=len(sprites),inventory_slots=len(requests)),ensure_ascii=False))
if __name__=='__main__':main()
