"""Lock the confirmed art specification and derive N1 technical guides.

The diagrams and masks are code-native layout assets, not generated artwork.
"""
from pathlib import Path
import importlib.util
import json
import hashlib
import re
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/hd2d_26x26_20261013'
SKILL=ROOT/'tools/vendor/pixel-asset-master-skills/skills/pixel-asset-master'

def load_module(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    palette_tool=load_module('pixel_palette',SKILL/'scripts/palette_analyzer.py')
    ref=ROOT/'design/12_美术参考/城市概念/DEN-概念-v1.png'
    # Upstream frequency sampling was audited, but its coarse 16-step bins
    # miss neutral stone ramps. Median-cut provides actual reference colors
    # without inventing saturated mauve/blue intermediates.
    analyzed_palette=palette_tool.extract_palette(ref,64)
    pimg=Image.open(ref).convert('RGB').quantize(colors=128,method=Image.Quantize.MEDIANCUT)
    rgb=pimg.getpalette()[:384]
    palette=['#%02X%02X%02X'%tuple(rgb[i:i+3]) for i in range(0,len(rgb),3)]
    inv=json.loads((P/'inventory.json').read_text(encoding='utf-8'))
    n1=[r for r in inv['records'] if r['family']=='existing_n1_room']
    specs=[dict(id=r['id']+'__ground',size=[1040,780],category='backgrounds',transparent=False) for r in n1]
    specs += [dict(id='n1_bellhouse_exterior',size=[312,260],category='items',transparent=True),
              dict(id='n1_story_props',size=[624,416],category='items',transparent=True)]
    # Guide colors are technical-only and are not art palette additions.
    anchors={
      'r_eao_n1_yard': dict(doors=[['home',7,24],['bellhouse',32,9]],
                            spawns=[['in',7,22],['back',32,11]],
                            story=[['tor',11,13],['rope',31,19],['bell',31,16]],
                            lights=[[10,7],[30,13]]),
      'r_eao_n1_bellhouse': dict(doors=[['yard',7,22],['underpass',34,17]],
                                 spawns=[['in',7,20],['back',32,17]],
                                 story=[['ivo',20,10],['cots',17,20]],
                                 lights=[[10,10],[22,18]]),
      'r_eao_n1_underpass': dict(doors=[['house',6,22]],
                                 spawns=[['in',6,20]],story=[['rhea',30,8]],
                                 lights=[[15,15],[25,8]])}
    (P/'guides').mkdir(exist_ok=True);(P/'palettes').mkdir(exist_ok=True)
    rooms=[]
    for r in n1:
        mask=Image.new('L',(1040,780),0);d=ImageDraw.Draw(mask)
        for x0,y0,x1,y1 in r['walkable_rectangles']:
            d.rectangle((x0*26,y0*26,(x1+1)*26-1,(y1+1)*26-1),fill=255)
        mask.save(P/'guides'/f'{r["id"]}_walkable.png')
        guide=Image.new('RGB',(1040,780),'#16262E')
        guide.paste('#ADA58A',(0,0),mask)
        guide.save(P/'guides'/f'{r["id"]}_geometry.png')
        marker=guide.copy();draw=ImageDraw.Draw(marker)
        for x in range(0,1040,26):draw.line((x,0,x,779),fill='#4E5555')
        for y in range(0,780,26):draw.line((0,y,1039,y),fill='#4E5555')
        for name,x,y in anchors[r['id']]['doors']:
            draw.rectangle((x*26+2,y*26+2,x*26+23,y*26+23),fill='#E0AF62')
        for name,x,y in anchors[r['id']]['spawns']:
            draw.ellipse((x*26+7,y*26+7,x*26+19,y*26+19),fill='#9BCDAB')
        marker.save(P/'guides'/f'{r["id"]}_plan.png')
        rooms.append(dict(id=r['id'],name_zh=r['name_zh'],size=r['pixels'],
                          cell_size=26,origin=[0,0],walkable_rectangles=r['walkable_rectangles'],
                          anchors=anchors[r['id']],
                          authority='src/EmbersAndOaths/NightRooms.cs',
                          evidence='source-code coordinates; not a runtime test',runtime_verified=False))
    (P/'native_layouts.json').write_text(json.dumps(rooms,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (P/'palettes/den_n1_128.json').write_text(json.dumps(dict(name='DEN-N1-128',colors=palette,method='Pillow median-cut of existing DEN reference, 128 actual RGB colors',upstream_analyzer_64=analyzed_palette,source=ref.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(ref.read_bytes()).hexdigest()),indent=2)+'\n',encoding='utf-8')
    gpl='GIMP Palette\nName: DEN-N1-128\nColumns: 8\n# Reference-derived median-cut; see JSON for upstream palette audit\n'
    for c in palette:
        rgb=[int(c[i:i+2],16) for i in [1,3,5]];gpl+=' '.join(map(str,rgb))+' '+c+'\n'
    (P/'palettes/den_n1_128.gpl').write_text(gpl,encoding='utf-8')
    lock='# Execution Lock\n\nConfirmed by user: 2026-10-13, 继续 after the six-parameter proposal.\n'
    lock+='Scope: full inventory retained; the active production batch is N1. No other region is marked complete.\n\n'
    lock+='## canvas\n- base_size: 26x26\n- tile_size: 26x26\n- format: RGBA PNG\n- room_size: 1040x780\n- generation_master: 4:3 scene, ideally 1040x780; preserve original output and document any nearest-neighbor size normalization\n\n'
    lock+='## palette\n- name: DEN-N1-128\n- colors:\n'+''.join('  - '+c+'\n' for c in palette)
    lock+='\n## style\n- sub_style: textured HD-2D, square-grid orthographic oblique\n- shading: restrained hard clusters\n- light_direction: top-left\n- atmosphere: muted coastal stone, weathered wood, grey teal water, cold night\n- lighting: no baked movable lamps; light effects are separate\n- no_purple: N1 has no visible crystal or supernatural glow\n\n'
    lock+='## per_sprite_budget\n- max_colors: 128\n\n## assets\n'
    for a in specs:
        lock+=f'- {a["id"]}: {a["size"][0]}x{a["size"][1]}, {a["category"]}, transparent={a["transparent"]}, single frame\n'
    lock+='- n1_water_base: 1040x780, opaque nonrepeating room backing\n- derived room floor/structure/foreground/plan/composite: 1040x780\n- derived props: bell78x104, bedding104x78, rope26x26, portal52x78, jug26x26, lantern26x52\n'
    lock+='\n## invariants\n- Every N1 floor shape comes from native_layouts.json. Artwork must not change walkable cells.\n- Doors and actor anchors are reserved, no new blockers or invented doors.\n- No baked characters, text, interface, clues that imply a selected quest result.\n- Existing bell remains hanging; only rope is cut. Bedrolls plus small shoes, no new occupied beds.\n- Raw generated pictures remain untouched in raw/; only explicitly recorded skill post-processing and asset export may normalize palette, alpha and canvas.\n- HD-2D depth uses independent structure/foreground/light passes; technical masks are never sold as painted assets.\n\n'
    lock+='## forbidden\n- Diamond isometric grid\n- Perspective camera\n- Anti-aliasing in production sprites\n- Unregistered colors\n- Partial alpha in base art\n- Glowing purple decorations in N1\n- Invented safe land in blocked water/void\n- Claiming export is deployment or runtime verification\n'
    (P/'spec_lock.md').write_text(lock,encoding='utf-8')
    spec='# Purple Crystal HD-2D - Design Spec\n\n'
    spec+='## I. Project Information\n\nFull inventory: 745 initial view slots. Active batch: N1 three rooms and separate architectural/story assets. Status: production in progress.\n\n'
    spec+='## II. Canvas Specification\n\n26×26 game cells; three 1040×780 local scenes. Building export 312×260; prop sheet 624×416. Camera: orthographic oblique over square grid.\n\n'
    spec+='## III. Color Palette\n\nDEN-N1-128; all HEX values in spec_lock.md and palettes/den_n1_128.json. Existing DEN concept image supplies the material colors. Revised after visual QA found coarse neutral ramps in the first 64-color sampling.\n\n'
    spec+='## IV. Art Style Definition\n\nCrisp textured medieval HD-2D, worn timber, limestone and dark tidal water; restrained top-left light. Independent art depth passes; no crystal effects in this chapter.\n\n'
    spec+='## V. Asset List\n\nProduction geometry: native_layouts.json. Full requirements: inventory.json. Generation records: generation-log.json. Unfinished requirements remain open.\n\n'
    spec+='## VI. Animation Specification\n\nSingle static frame per export. Existing in-engine NPC and candle behavior is not baked into art.\n\n'
    spec+='## VII. Technical Constraints\n\nNative source geometry is authoritative. Preserve door/arrival/story coordinates. Validate dimensions, alpha, palette, source hashes, connectivity, and actual visual fit independently.\n\n'
    spec+='## VIII. Platform Export Notes\n\nGameMaker-compatible RGBA PNG with relative paths, origin and draw-layer metadata. Exports are not a modified data.win or an accepted in-game test.\n'
    (P/'design_spec.md').write_text(spec,encoding='utf-8')
    prop=json.loads((P/'proposal.json').read_text(encoding='utf-8'))
    prop['status']='confirmed_production_started';prop['confirmation']={'date':'2026-10-13','message':'继续'}
    (P/'proposal.json').write_text(json.dumps(prop,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'rooms':len(rooms),'palette':len(palette),'batch_assets':len(specs)},ensure_ascii=False))

if __name__=='__main__': main()
