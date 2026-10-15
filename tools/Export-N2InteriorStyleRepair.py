"""Compose generated materials around unchanged N2 collision cells.

Run after Export-Hd2dNativeN2.py. Imagegen supplies all new painted pixels;
this exporter only samples, quantizes, masks and assembles existing assets.
"""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'src/Art/native-n2-hd2d-v1'
BATCH = ROOT / 'src/Art/scene-style-repairs-20261015'
RAW = BATCH / 'raw/interiors'
R01 = ROOT / 'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v2'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest_path = PACK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    layout = json.loads((PACK / 'interior-style-layout.json').read_text(encoding='utf8'))
    version = layout['repair_version']
    size, tile = tuple(layout['size']), layout['tile']
    inputs = {}

    def source(path):
        inputs[path.relative_to(ROOT).as_posix()] = sha(path)
        return Image.open(path).convert('RGBA')

    palette_path = R01 / 'palettes/bry_r01_128.json'
    inputs[palette_path.relative_to(ROOT).as_posix()] = sha(palette_path)
    colors = [tuple(bytes.fromhex(c.lstrip('#'))) for c in json.loads(palette_path.read_text(encoding='utf8'))['colors']]
    assert len(colors) == 128
    palette = Image.new('P', (1, 1))
    palette.putpalette([v for c in colors for v in c] + list(colors[-1]) * 128)

    def clean(im):
        alpha = im.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
        rgb = im.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        result = Image.new('RGBA', im.size)
        result.paste(rgb, (0, 0), alpha)
        return result

    materials = {}
    for name in ('wood-floor', 'stone-floor'):
        # Long-period quiet material, never the old small crop with repeated dirt motifs.
        sample = clean(source(RAW / (name + '.png')).resize(tuple(layout['material_period']), Image.Resampling.NEAREST))
        canvas = Image.new('RGBA', size)
        for y in range(0, size[1], sample.height):
            for x in range(0, size[0], sample.width):
                canvas.alpha_composite(sample, (x, y))
        materials[name] = canvas

    wall_sheet = source(R01 / 'assets/backgrounds/r01_canal_tomb__structure.png')
    wall = wall_sheet.crop((104,78,208,104))
    side = wall_sheet.crop((97,104,104,156))
    earth = source(BATCH / 'raw/forecourt-earth-v2.png').resize(size, Image.Resampling.NEAREST)
    # Preserve a complete painted basin, including its coping and end caps.
    # Never repeat the former 128x65 patch down the channel.
    assert layout['water_sampling'] == 'whole-basin'
    water = source(ROOT / layout['water_source'])
    code_path = ROOT / 'src/EmbersAndOaths/N2Quest.cs'
    code = code_path.read_text(encoding='utf8')
    inputs[code_path.relative_to(ROOT).as_posix()] = sha(code_path)
    layout_path = PACK / 'interior-style-layout.json'
    inputs[layout_path.relative_to(ROOT).as_posix()] = sha(layout_path)

    def save(im, ident, **extra):
        path = PACK / 'assets' / (ident + '.png')
        im = clean(im)
        im.save(path)
        entry = next((a for a in manifest['assets'] if a['id'] == ident), None)
        if entry is None:
            entry = dict(id=ident,path='assets/'+path.name,size=list(im.size),origin=[26,52],role='doorway_floor_stamp')
            manifest['assets'].append(entry)
        entry.update(sha256=sha(path),style_repair=version,**extra)
        return im

    for index, spec in enumerate(layout['scenes']):
        key = ('Camp', 'Winch', 'Side')[index]
        text = re.search(r'\['+key+r'\]\s*=\s*new\[\]\s*\{([^}]+)\}',code).group(1)
        rects = [list(map(int,r.split(','))) for r in re.findall(r'\(([^)]+)\)',text)]
        cells = {(x,y) for a,b,c,d in rects for x in range(a,c+1) for y in range(b,d+1)}
        record = next(s for s in manifest['scenes'] if s['room'] == spec['room'])
        assert rects == record['walkable_rectangles']
        mask = Image.new('L',size)
        draw = ImageDraw.Draw(mask)
        for x,y in cells:
            draw.rectangle((x*tile,y*tile,(x+1)*tile-1,(y+1)*tile-1),fill=255)
        floor = materials[spec['material']].copy()
        floor.putalpha(mask)
        previous_alpha = Image.open(PACK/'assets'/(spec['room']+'__floor.png')).getchannel('A')
        assert ImageChops.difference(previous_alpha,mask).getbbox() is None
        backing = Image.new('RGBA',size,(13,14,14,255))
        if spec['backing'] == 'earth-and-drain':
            backing = earth.copy()
            backing.putalpha(255)
            for x0,y0,x1,y1 in spec['water_rectangles']:
                assert not any((x,y) in cells for x in range(x0,x1+1) for y in range(y0,y1+1))
                region = water.resize(((x1-x0+1)*tile,(y1-y0+1)*tile),Image.Resampling.NEAREST)
                backing.alpha_composite(region,(x0*tile,y0*tile))
        structure = Image.new('RGBA',size)
        foreground = Image.new('RGBA',size)
        nh, sh = spec['north_wall_height'],spec['south_wall_height']
        for x,y in sorted(cells):
            if (x,y-1) not in cells:
                offset = (x%4)*tile
                strip = wall.crop((offset,26-nh,offset+tile,26))
                structure.alpha_composite(strip,(x*tile,y*tile-nh))
            if (x-1,y) not in cells:
                structure.alpha_composite(side.crop((0,(y%2)*26,7,(y%2+1)*26)),(x*tile-7,y*tile))
            if (x+1,y) not in cells:
                structure.alpha_composite(side.crop((0,(y%2)*26,7,(y%2+1)*26)),((x+1)*tile,y*tile))
            if (x,y+1) not in cells:
                offset = (x%4)*tile
                foreground.alpha_composite(wall.crop((offset,0,offset+tile,sh)),(x*tile,(y+1)*tile))
        outside = ImageChops.invert(mask)
        for im in (structure,foreground):
            im.putalpha(ImageChops.multiply(im.getchannel('A'),outside))
        for name,im in [('backing',backing),('floor',floor),('structure',structure),('foreground',foreground)]:
            save(im,spec['room']+'__'+name)
        record.update(material_source=spec['material'],material_period=layout['material_period'],backing_style=spec['backing'],door_anchors=spec['doors'])
        if spec['backing'] == 'earth-and-drain':
            record.update(water_source=layout['water_source'],water_sampling=layout['water_sampling'],water_rectangles=spec['water_rectangles'])
        record.pop('material_crop_cells',None)

    doorway = source(RAW/'doorway.png')
    alpha = doorway.getchannel('A').point(lambda v:255 if v>=128 else 0)
    doorway.putalpha(alpha)
    doorway = doorway.crop(alpha.getbbox())
    doorway.thumbnail((52,65),Image.Resampling.NEAREST)
    sprite = Image.new('RGBA',(52,65))
    sprite.alpha_composite(doorway,((52-doorway.width)//2,65-doorway.height))
    sprite=save(sprite,'r01_doorway_open')
    # Existing nonblocking bedrolls retain their IDs, room positions and origin.
    bedroll = source(ROOT/layout['bedroll_source'])
    bedroll.putalpha(bedroll.getchannel('A').point(lambda v:255 if v>=128 else 0))
    bedroll = bedroll.crop(bedroll.getchannel('A').getbbox())
    bedroll.thumbnail((24,44),Image.Resampling.NEAREST)
    cloth = Image.new('RGBA',(52,52))
    cloth.alpha_composite(bedroll,((52-bedroll.width)//2,52-bedroll.height))
    cloth = clean(cloth)
    built_pack=ROOT/'src/Art/native-n2-built-v1'
    built_path=built_pack/'manifest.json'
    built=json.loads(built_path.read_text(encoding='utf8'))
    cloth_spec=next(a for a in built['assets'] if a['id']=='n2site_r01_shelter_bedroll')
    assert cloth_spec['size']==[52,52] and cloth_spec['origin']==[26,43]
    cloth_path=built_pack/cloth_spec['path']
    cloth.save(cloth_path)
    cloth_spec.update(sha256=sha(cloth_path),style_repair=version,role='generated_floor_cloth',body_bbox=list(cloth.getchannel('A').getbbox()))
    for path in (ROOT/layout['bedroll_source'],palette_path):
        built['source_sha256'][path.relative_to(ROOT).as_posix()]=sha(path)
    built['style_repair']=version
    built_path.write_text(json.dumps(built,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')

    preview_dir=ROOT/('artifacts/interior-style-'+version.replace('.','')+'-previews')
    preview_dir.mkdir(exist_ok=True)
    for spec in layout['scenes']:
        preview=Image.new('RGBA',size)
        for layer in ('backing','floor','structure'):
            preview.alpha_composite(Image.open(PACK/'assets'/(spec['room']+'__'+layer+'.png')).convert('RGBA'))
        for door in spec['doors']:
            x,y=door['cell']
            preview.alpha_composite(sprite,(x*26+13-26,y*26+13-52))
        scene_layout=json.loads((built_pack/'layout.json').read_text(encoding='utf8'))
        for prop in scene_layout['props']:
            if prop['room']!=spec['room']:continue
            asset=next(a for a in built['assets'] if a['id']=='n2site_'+prop['source'])
            px,py=prop['cell'];ox,oy=asset['origin']
            preview.alpha_composite(Image.open(built_pack/asset['path']).convert('RGBA'),(px*26+13-ox,py*26+13-oy))
        preview.alpha_composite(Image.open(PACK/'assets'/(spec['room']+'__foreground.png')).convert('RGBA'))
        preview.save(preview_dir/(spec['room']+'.png'))
    manifest['source_sha256'].update(inputs)
    manifest['scope']='Current N2 visual layers; unchanged collision/actor/quest geometry, generated materials and doorway stamps below actors'
    manifest['style_repair']=version
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    report=dict(version=version,source_sha256=inputs,assets={a['id']:a['sha256'] for a in manifest['assets'] if a.get('style_repair')==version},bedroll_sha256=cloth_spec['sha256'],water_sampling=layout['water_sampling'],collision_mask_unchanged=True,runtimeVerified=False)
    (BATCH/'interior-export.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(assets=len(report['assets']),source_files=len(inputs),collision_mask_unchanged=True)))


if __name__ == '__main__':
    main()
