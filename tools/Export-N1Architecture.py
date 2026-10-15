"""Assemble original wall panels outside the unchanged N1 floor masks.

Run after Export-N1SurfaceRepair.py. This pass changes two boundary layers and
the drain's flat blocked backing only. Floor pixels and all actor/door anchors
are untouched. Generated source pixels, prompts and the previous pass survive.
"""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'src/Art/hd2d_26x26_20261013'
BATCH = ROOT / 'src/Art/scene-style-repairs-20261015/n1-architecture-v1'
SIZE = (1040, 780)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    layout = json.loads((BATCH / 'layout.json').read_text(encoding='utf8'))
    manifest_path = PACK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf8'))
    inputs = {}
    for path in [BATCH / 'layout.json', Path(__file__),
                 ROOT / 'src/EmbersAndOaths/NightRooms.cs',
                 PACK / 'palettes/den_n1_128.json']:
        inputs[path.relative_to(ROOT).as_posix()] = sha(path)
    colors = [tuple(bytes.fromhex(c.lstrip('#'))) for c in
              json.loads((PACK / 'palettes/den_n1_128.json').read_text())['colors']]
    palette = Image.new('P', (1, 1))
    palette.putpalette([v for c in colors for v in c] + list(colors[-1]) * (256-len(colors)))

    def clean(im):
        alpha = im.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
        rgb = im.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        result = Image.new('RGBA', im.size)
        result.paste(rgb, (0, 0), alpha)
        return result

    panels = {}
    for name, material in layout['materials'].items():
        path = BATCH / material['raw']
        inputs[path.relative_to(ROOT).as_posix()] = sha(path)
        raw = Image.open(path).convert('RGBA')
        panels[name] = clean(raw.crop(material['crop']).resize(tuple(layout['panel_size']), Image.Resampling.NEAREST))

    def save(im, ident):
        path = PACK / 'assets/backgrounds' / (ident+'.png')
        im = clean(im)
        im.save(path)
        entry = next(a for a in manifest['assets'] if a['id'] == ident)
        entry.update(sha256=sha(path), architecture_repair='0.3.14')
        return im

    untouched_floors = {}
    for room in manifest['rooms']:
        path = PACK / 'assets/backgrounds' / (room['id']+'__floor.png')
        untouched_floors[room['id']] = sha(path)
    for spec in layout['scenes']:
        rid = spec['room']
        record = next(r for r in manifest['rooms'] if r['id'] == rid)
        cells = {(x, y) for a,b,c,d in record['walkable_rectangles']
                 for y in range(b,d+1) for x in range(a,c+1)}
        floor = Image.open(PACK / 'assets/backgrounds' / (rid+'__floor.png')).convert('RGBA')
        mask = floor.getchannel('A')
        outside = ImageChops.invert(mask)
        structure, foreground = Image.new('RGBA', SIZE), Image.new('RGBA', SIZE)

        def material_at(x):
            return 'stone' if x >= spec.get('stone_from_column', 1000) else spec['material']

        for x,y in sorted(cells):
            name = material_at(x)
            panel = panels[name]
            offset = (x % (panel.width//26))*26
            if (x,y-1) not in cells:
                # A two-tile wall face at north-facing boundaries. Cropping
                # after placement also protects adjacent concave walk cells.
                structure.alpha_composite(panel.crop((offset,0,offset+26,spec['north_height'])),
                                          (x*26,y*26-spec['north_height']))
            if (x,y+1) not in cells:
                foreground.alpha_composite(panel.crop((offset,0,offset+26,spec['front_height'])),
                                           (x*26,(y+1)*26))
            width = layout['materials'][name]['side_width']
            post = panel.crop((0,0,width,panel.height))
            for sx,px in ((x-1,x*26-width),(x+1,(x+1)*26)):
                if (sx,y) in cells:
                    continue
                sy = (y % 2)*26
                structure.alpha_composite(post.crop((0,sy,width,sy+26)), (px,y*26))
                if (x,y-1) not in cells:
                    structure.alpha_composite(post,(px,y*26-panel.height))
        for layer in (structure, foreground):
            layer.putalpha(ImageChops.multiply(layer.getchannel('A'), outside))
        structure = save(structure, rid+'__structure')
        foreground = save(foreground, rid+'__foreground')
        backing_path = PACK / 'assets/backgrounds' / (rid+'__backing.png')
        backing = Image.open(backing_path).convert('RGBA')
        if 'backing_color' in spec:
            backing = save(Image.new('RGBA', SIZE, spec['backing_color']),rid+'__backing')
        plan = save(Image.alpha_composite(backing, floor), rid+'__plan')
        environment = save(Image.alpha_composite(Image.alpha_composite(plan, structure), foreground),rid+'__environment')
        preview = environment.copy()
        if rid.endswith('bellhouse'):
            entry = next(a for a in manifest['assets'] if a['id'] == 'n1_bedding')
            sprite = Image.open(PACK / entry['path']).convert('RGBA')
            ox,oy = entry['sprite_origin']
            preview.alpha_composite(sprite,(17*26+13-ox,20*26+13-oy))
        doors = json.loads((ROOT / 'src/Art/native-n1-doorways-v1/manifest.json').read_text(encoding='utf8'))
        for door in doors['doors']:
            if door['room'] != rid:
                continue
            entry = next(a for a in doors['assets'] if a['id'] == door['art'])
            sprite = Image.open(ROOT / 'src/Art/native-n1-doorways-v1' / entry['path']).convert('RGBA')
            x,y = door['cell']; ox,oy = entry['origin']
            preview.alpha_composite(sprite,(x*26+13-ox,y*26+13-oy))
        preview.save(PACK / 'previews' / (rid+'__preview.png'))
    for rid,expected in untouched_floors.items():
        assert sha(PACK / 'assets/backgrounds' / (rid+'__floor.png')) == expected, 'Floor changed: '+rid
    manifest['n1_architecture_repair'] = dict(version='0.3.14', source_sha256=inputs,
        layout=layout, floor_sha256=untouched_floors,
        scope='Original walls in blocked space only; unchanged floors, collision and actors; drain backing flat; runtime sampling separate')
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf8',newline='\n')
    print(json.dumps(dict(rooms=2,replaced_layers=9,source_files=len(inputs),floor_pixels_unchanged=True)))


if __name__ == '__main__':
    main()
