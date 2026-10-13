"""Prepare the scene-only R01 art batch from the confirmed Pixel Asset Master spec.

Writes original art geometry proposals and technical guides, never game/NPC files.
"""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / 'src/Art/hd2d_26x26_20261013'
P = PARENT / 'batches/R01-camp-canal-v1'
TILE = 26

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name, value):
    path = P / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def main():
    for name in ['raw', 'images', 'animations', 'sheets', 'assets/backgrounds', 'assets/items', 'guides', 'palettes', 'notes', 'previews', 'exports']:
        (P / name).mkdir(parents=True, exist_ok=True)
    sources = ['design/02_世界与地图/区域_R01_布林外港与旧渠.md',
               'design/05_主线/台本/台本_N2_灰堤没有墓碑.md',
               'design/08_副本/台本/台本_D02_旧渠检修墓室.md',
               'design/12_美术参考/城市概念/BRY-概念-v1.png']
    reference = ROOT / sources[-1]
    pal = Image.open(reference).convert('RGB').quantize(colors=128, method=Image.Quantize.MEDIANCUT).getpalette()[:384]
    colors = ['#%02X%02X%02X' % tuple(pal[i:i+3]) for i in range(0, len(pal), 3)]
    write('palettes/bry_r01_128.json', dict(name='BRY-R01-128', colors=colors,
          method='median-cut of existing BRY Mod concept reference', source=sources[-1], sha256=sha(reference)))
    gpl = 'GIMP Palette\nName: BRY-R01-128\nColumns: 8\n# Existing reference-derived colors\n'
    for c in colors: gpl += ' '.join(str(int(c[i:i+2],16)) for i in (1,3,5))+' '+c+'\n'
    (P/'palettes/bry_r01_128.gpl').write_text(gpl, encoding='utf-8')
    scenes = [
      dict(id='r01_camp', location='R01-camp', name_zh='灰堤工营', size=[1040,780], cells=[40,30],
           walkable_rectangles=[[4,4,35,9],[5,10,22,24],[23,14,35,24],[22,10,25,13]],
           blocked_rectangles=[[7,5,16,7],[28,5,34,6]],
           exits=[dict(id='port',cell=[8,24]),dict(id='hearing',cell=[5,15]),dict(id='canal',cell=[35,20])],
           reserved=[dict(id='coffin_inspect',cell=[12,17]),dict(id='winch_inspect',cell=[30,19]),
                     dict(id='shed_front',cell=[12,11]),dict(id='repair_front',cell=[31,9])],
           objects=[dict(id='r01_worker_shed',cell=[12,11],plane_bounds=[7,5,16,10],roof=True),
                    dict(id='r01_winch_shed',cell=[31,9],plane_bounds=[28,5,34,8],roof=True),
                    dict(id='r01_coffin_coat',cell=[12,15]),dict(id='r01_winch_socket',cell=[30,17])],
           rationale='High embankment, communal shed court, broken lower bank and separate winch court. Open shed front is working space; no additional NPC or grave proof.'),
      dict(id='r01_canal_pump', location='R01-canal', name_zh='旧渠高位泵房与检修侧间', size=[1352,884], cells=[52,34],
           walkable_rectangles=[[4,4,47,10],[4,11,10,29],[18,14,29,20],[37,11,47,28],
                                [11,16,17,18],[30,16,36,18],[4,27,47,29]],
           blocked_rectangles=[[39,18,39,20],[39,23,39,24],[40,18,46,18],[40,24,46,24]],
           exits=[dict(id='camp_entry',cell=[7,5]),dict(id='maintenance_return',cell=[44,6]),dict(id='tomb',cell=[26,29])],
           reserved=[dict(id='sluice_control',cell=[24,8]),dict(id='side_room_front',cell=[38,21]),dict(id='inspection_plate',cell=[9,10])],
           objects=[dict(id='r01_sluice_wheel',cell=[24,7]),dict(id='r01_maintenance_ladder',cell=[44,5]),
                    dict(id='r01_shelter_bedroll',cell=[44,21]),dict(id='r01_water_jug',cell=[45,22])],
           water_rectangles=[[11,11,17,26],[30,11,36,26]],
           rationale='Two longitudinal channels, high pump hall, dry perimeter loop and bridges. Living side room stays on the east dry bank, separated from the lower tomb.'),
      dict(id='r01_canal_tomb', location='R01-canal', name_zh='旧渠下层墓龛环道', size=[936,728], cells=[36,28],
           walkable_rectangles=[[4,4,31,7],[4,8,7,22],[28,8,31,22],[8,19,27,22],
                                [12,10,23,17],[8,12,11,14],[24,12,27,14]],
           blocked_rectangles=[],
           exits=[dict(id='pump_entry',cell=[6,5]),dict(id='maintenance_return',cell=[6,20])],
           reserved=[dict(id='history_inspection',cell=[18,13])],
           objects=[dict(id='r01_maintenance_ladder',cell=[5,20])],
           rationale='Dry central platform inside an annular maintenance route; low wall niches face the ring. No resident or occupied bed in the tomb, no automatic loot ownership.')]
    for scene in scenes:
        scene.update(cell_pixels=TILE, origin=[0,0], geometry_authority='Mod art geometry proposal, not an implemented game room',
                     implementation_verified=False, runtime_verified=False)
        mask=Image.new('L', tuple(scene['size']), 0); draw=ImageDraw.Draw(mask)
        for a,b,c,d in scene['walkable_rectangles']: draw.rectangle((a*TILE,b*TILE,(c+1)*TILE-1,(d+1)*TILE-1),fill=255)
        for a,b,c,d in scene['blocked_rectangles']: draw.rectangle((a*TILE,b*TILE,(c+1)*TILE-1,(d+1)*TILE-1),fill=0)
        mask.save(P/'guides'/f'{scene["id"]}_walkable.png')
        guide=Image.new('RGB', tuple(scene['size']), '#20363A'); guide.paste('#A29474', (0,0), mask)
        guide.save(P/'guides'/f'{scene["id"]}_geometry.png')
        plan=guide.copy(); d=ImageDraw.Draw(plan)
        for x in range(0,scene['size'][0],26): d.line((x,0,x,scene['size'][1]-1),fill='#555D58')
        for y in range(0,scene['size'][1],26): d.line((0,y,scene['size'][0]-1,y),fill='#555D58')
        for e in scene['exits']:
            x,y=e['cell']; d.rectangle((x*26+4,y*26+4,x*26+21,y*26+21),fill='#E7AF52')
        for e in scene['reserved']:
            x,y=e['cell']; d.ellipse((x*26+6,y*26+6,x*26+20,y*26+20),fill='#9DE0B4')
        plan.save(P/'guides'/f'{scene["id"]}_technical_plan.png')
    write('layouts.json', scenes)
    asset_specs=[dict(id=s['id'],size=s['size'],role='room master with floor, blocked backing and independently exported architecture') for s in scenes]
    sprite_specs = [dict(id='r01_worker_shed',size=[260,208],origin=[130,190]),
                    dict(id='r01_winch_shed',size=[208,182],origin=[104,165]),
                    dict(id='r01_canal_entry',size=[260,234],origin=[130,216]),
                    dict(id='r01_coffin_coat',size=[52,78],origin=[26,65]),
                    dict(id='r01_winch_socket',size=[52,52],origin=[26,43]),
                    dict(id='r01_sluice_wheel',size=[52,78],origin=[26,65]),
                    dict(id='r01_maintenance_ladder',size=[26,78],origin=[13,65]),
                    dict(id='r01_shelter_bedroll',size=[52,52],origin=[26,43]),
                    dict(id='r01_water_jug',size=[26,26],origin=[13,23])]
    write('brief.json', dict(schema=1,batch='R01-camp-canal-v1',scope='Scene art only; NPC work is owned by the other model per user 2026-10-13',
          source_sha256={p:sha(ROOT/p) for p in sources},parent_confirmation='Existing HD2D six-parameter proposal confirmed by user 继续 on 2026-10-13; current user continues scene work',
          inventory_requests=['R01-camp__plan','R01-camp__exterior_or_site','R01-canal__plan','R01-canal__exterior_or_site','R01-canal__interior_or_working_space'],
          scenes=asset_specs,sprites=sprite_specs,skill='tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master/SKILL.md',
          skill_commit='33d891c421a9ad3608f5a09af97271388ca923af',runtime_verified=False))
    lock='# Execution Lock — R01 Scene Art\n\n## authorization\n'
    lock+='Existing HD2D style/six-parameter confirmation remains in force. Current user assigns scene drawing only; NPC files and behavior are outside this batch.\n\n'
    lock+='## canvas\n- base_size: 26x26\n- tile_size: 26x26\n- format: RGBA PNG\n- generation_master: preserve original image, then nearest-neighbor normalization to the following declared production canvases\n'
    for s in asset_specs: lock+=f'- {s["id"]}: {s["size"][0]}x{s["size"][1]}\n'
    lock+='- architecture_master: 1536x1024, 3 isolated structures in a row on transparent background; no scene floor\n- props_master: 1536x1024, 3x2 isolated objects on transparent background\n- utility_master: 1024x1024, isolated ladder and jug on transparent background\n'
    for s in sprite_specs: lock+=f'- {s["id"]}: {s["size"][0]}x{s["size"][1]}, origin {s["origin"]}, transparent, single frame\n'
    lock+='\n## palette\n- name: BRY-R01-128\n- colors:\n'+''.join('  - '+c+'\n' for c in colors)
    lock+='\n## style\n- sub_style: textured HD-2D, square-grid orthographic oblique, consistent with previous Stoneshard Mod concept\n- materials: salt-grey limestone, brown timber, dull russet shingles, wet brick, desaturated teal water\n- light_direction: top-left\n- pixel_edges: hard readable clusters, no blurred gradients or antialiasing after export\n- no_purple: no visible crystal or purple glow in N2/D02\n- lighting: no baked moving flame or screen-space bloom; engine lights separately\n\n'
    lock+='## per_sprite_budget\n- max_colors: 128\n\n## invariants\n'
    lock+='- layouts.json is a new art geometry proposal; D02 canvas cell counts follow the current screenplay. It is not native collision proof.\n- Every production floor alpha must equal its explicit walkable mask. Buildings have independent occupancy metadata; no collision inferred from sprite alpha.\n- Keep the high pump hall, two channels, dry route, initial retreat and return ladder. Never paint the sole return as flooded.\n- Empty coffin contains only an old coat, no body; winch socket shows removed axle. No selected N2/D02 outcome baked in.\n- Living side room stays separate from the tomb. No characters, faces, dialogue, handwriting, readable notices, logos or UI.\n- No copied commercial texture atlas. References are existing Mod concepts.\n- Single-frame assets; no unspecified animation.\n- Raw generated masters are immutable; palette quantization, binary-alpha, documented crops, nearest-neighbor export and code-native geometry masks are authorized post-processing.\n'
    (P/'spec_lock.md').write_text(lock, encoding='utf-8')
    sections=[('I. Project Information','布林外围Mod原创场景：灰堤工营、旧渠泵房与下层墓龛。角色仅预留空间。'),
      ('II. Canvas Specification','26×26格；工营40×30，旧渠52×34，墓室36×28。尺寸与独立精灵见spec_lock.md。'),
      ('III. Color Palette','BRY-R01-128，从既有布林Mod概念图提取128色，全HEX保存在spec_lock与palette JSON。'),
      ('IV. Art Style Definition','原作方向的正交斜俯视HD-2D，盐灰石、湿砖、褐木、低饱和水；左上基础光。'),
      ('V. Asset List','三幅场景母图、独立建筑与环境物件；地图、场景、结构、屋顶/前景分层导出。'),
      ('VI. Animation Specification','单帧静态；移动灯光与水/门动画不在本批。'),
      ('VII. Technical Constraints','几何为制作提案，源自台本约束；不改NPC、任务状态或安装包。固定门点与干地回程分别验收。'),
      ('VIII. Platform Export Notes','GameMaker RGBA PNG、原点、相对路径、占地和通路掩码；导入后仍需原生转场/相机/碰撞测试。')]
    (P/'design_spec.md').write_text('# Purple Crystal HD-2D — R01 Design Spec\n\n'+ '\n\n'.join('## '+a+'\n\n'+b for a,b in sections)+'\n',encoding='utf-8')
    print(json.dumps(dict(batch=P.relative_to(ROOT).as_posix(),scenes=len(scenes),sprites=len(sprite_specs),palette=len(colors)),ensure_ascii=False))

if __name__=='__main__': main()
