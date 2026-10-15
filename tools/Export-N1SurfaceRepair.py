"""Assemble continuous imagegen floor panels on unchanged N1 native geometry.

Only palette conversion, nearest sampling, crops and alpha masks are performed.
No repeated/mirrored floor crops, no painted geometry, no game-directory writes.
Run after Export-Hd2dN1.py; raw source pixels and previous audit history survive.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'src/Art/hd2d_26x26_20261013'
BATCH = ROOT / 'src/Art/scene-style-repairs-20261015/n1-surfaces-v1'
R01 = PACK / 'batches/R01-camp-canal-v2'
SIZE = (1040, 780)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    layout_path = BATCH / 'layout.json'
    layout = json.loads(layout_path.read_text(encoding='utf8'))
    manifest_path = PACK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    inputs = {}

    def source(path):
        inputs[path.relative_to(ROOT).as_posix()] = sha(path)
        return Image.open(path).convert('RGBA')

    palette_path = PACK / 'palettes/den_n1_128.json'
    inputs[palette_path.relative_to(ROOT).as_posix()] = sha(palette_path)
    colors = [tuple(bytes.fromhex(c.lstrip('#'))) for c in json.loads(palette_path.read_text())['colors']]
    palette = Image.new('P', (1, 1))
    palette.putpalette([v for c in colors for v in c] + list(colors[-1]) * (256-len(colors)))

    def clean(im):
        alpha = im.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
        rgb = im.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        result = Image.new('RGBA', im.size)
        result.paste(rgb, (0, 0), alpha)
        return result

    materials = {name: clean(source(BATCH / 'raw' / path).resize(SIZE, Image.Resampling.NEAREST))
                 for name, path in layout['materials'].items()}
    wall_sheet = source(R01 / 'assets/backgrounds/r01_canal_tomb__structure.png')
    wall = wall_sheet.crop((104, 78, 208, 104))
    side = wall_sheet.crop((97, 104, 104, 156))
    inputs[layout_path.relative_to(ROOT).as_posix()] = sha(layout_path)
    inputs['tools/Export-N1SurfaceRepair.py'] = sha(Path(__file__))
    inputs['src/EmbersAndOaths/NightRooms.cs'] = sha(ROOT / 'src/EmbersAndOaths/NightRooms.cs')

    def save(im, ident):
        path = PACK / 'assets/backgrounds' / (ident+'.png')
        im = clean(im)
        im.save(path)
        entry = next(a for a in manifest['assets'] if a['id'] == ident)
        entry.update(sha256=sha(path), style_repair='0.3.13')
        return im

    for spec in layout['scenes']:
        rid = spec['room']
        record = next(r for r in manifest['rooms'] if r['id'] == rid)
        cells = {(x, y) for a,b,c,d in record['walkable_rectangles']
                 for y in range(b,d+1) for x in range(a,c+1)}
        mask = Image.new('L', SIZE)
        draw = ImageDraw.Draw(mask)
        for x,y in cells:
            draw.rectangle((x*26,y*26,(x+1)*26-1,(y+1)*26-1),fill=255)
        old_alpha = Image.open(PACK/'assets/backgrounds'/(rid+'__floor.png')).getchannel('A')
        assert ImageChops.difference(old_alpha, mask).getbbox() is None, 'Existing floor geometry changed: '+rid
        floor = materials[spec['material']].copy()
        # One continuous stone panel under the bellhouse access corridor, with
        # the old exact wooden hall edge retained. No new blocking furniture.
        if spec.get('stone_corridor'):
            a,b,c,d = spec['stone_corridor']
            box = (a*26,b*26,(c+1)*26,(d+1)*26)
            floor.paste(materials['stone'].crop(box), box[:2])
        floor.putalpha(mask)
        structure = Image.new('RGBA', SIZE)
        foreground = Image.new('RGBA', SIZE)
        nh,sh = spec['north_wall_height'],spec['south_wall_height']
        for x,y in sorted(cells):
            offset = (x%4)*26
            if (x,y-1) not in cells:
                structure.alpha_composite(wall.crop((offset,26-nh,offset+26,26)),(x*26,y*26-nh))
            if (x,y+1) not in cells:
                foreground.alpha_composite(wall.crop((offset,0,offset+26,sh)),(x*26,(y+1)*26))
            for sx,px in ((x-1,x*26-7),(x+1,(x+1)*26)):
                if (sx,y) not in cells:
                    structure.alpha_composite(side.crop((0,(y%2)*26,7,(y%2+1)*26)),(px,y*26))
        outside = ImageChops.invert(mask)
        for layer in (structure,foreground):
            layer.putalpha(ImageChops.multiply(layer.getchannel('A'),outside))
        floor=save(floor,rid+'__floor')
        structure=save(structure,rid+'__structure')
        foreground=save(foreground,rid+'__foreground')
        backing=Image.open(PACK/'assets/backgrounds'/(rid+'__backing.png')).convert('RGBA')
        plan=save(Image.alpha_composite(backing,floor),rid+'__plan')
        environment=save(Image.alpha_composite(Image.alpha_composite(plan,structure),foreground),rid+'__environment')
        # Previews include the same independent props and doorway stamps used
        # in-engine, without baking them into the production floor layers.
        preview=environment.copy()
        placements = ([('n1_bell',31,16),('n1_cut_rope',31,19)] if rid.endswith('yard') else
                      [('n1_bedding',17,20)] if rid.endswith('bellhouse') else [])
        for ident,x,y in placements:
            entry=next(a for a in manifest['assets'] if a['id']==ident)
            sprite=Image.open(PACK/entry['path']).convert('RGBA')
            ox,oy=entry['sprite_origin']
            preview.alpha_composite(sprite,(x*26+13-ox,y*26+13-oy))
        doors=json.loads((ROOT/'src/Art/native-n1-doorways-v1/manifest.json').read_text(encoding='utf8'))
        for door in doors['doors']:
            if door['room'] != rid: continue
            entry=next(a for a in doors['assets'] if a['id']==door['art'])
            sprite=Image.open(ROOT/'src/Art/native-n1-doorways-v1'/entry['path']).convert('RGBA')
            x,y=door['cell'];ox,oy=entry['origin']
            preview.alpha_composite(sprite,(x*26+13-ox,y*26+13-oy))
        preview.save(PACK/'previews'/(rid+'__preview.png'))
    manifest['n1_surface_repair'] = dict(version='0.3.13',sampling='one complete panel per material; nearest; no repeat or mirror',
                                         source_sha256=inputs,layout=layout,
                                         scope='Floor/boundary pixels only; native cells, actors and routes unchanged; runtime acceptance separate')
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(rooms=3,replaced_layers=15,source_files=len(inputs),floor_mask_unchanged=True)))


if __name__ == '__main__':
    main()
