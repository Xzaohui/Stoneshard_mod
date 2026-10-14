"""Adapt released R01 artwork to the existing N2 native collision cells.

No generation, NPC edits, or released image changes. Masks come from N2Quest.cs,
never from painted floor alpha. All source bytes are pinned in the manifest.
"""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageChops

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v2'
OUT = ROOT / 'src/Art/native-n2-hd2d-v1'
ROOMS = {'Camp': ('r_eao_n2_camp', 'r01_camp', (5, 10, 17, 18)),
         'Winch': ('r_eao_n2_winch', 'r01_canal_pump', (4, 4, 16, 10)),
         'Side': ('r_eao_n2_side', 'r01_canal_tomb', (12, 10, 24, 18))}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    OUT.mkdir(exist_ok=True)
    (OUT / 'assets').mkdir(exist_ok=True)
    inputs = {}
    def load(rel):
        path = SOURCE / rel
        inputs[str(path.relative_to(ROOT)).replace('\\', '/')] = sha(path)
        return Image.open(path).convert('RGBA')
    code = (ROOT / 'src/EmbersAndOaths/N2Quest.cs').read_text(encoding='utf8')
    inputs['src/EmbersAndOaths/N2Quest.cs'] = sha(ROOT / 'src/EmbersAndOaths/N2Quest.cs')
    assets, scenes = [], []
    def save(im, ident, origin=(0, 0), **meta):
        path = OUT / 'assets' / (ident + '.png')
        im.save(path)
        assets.append(dict(id=ident, path='assets/' + path.name, size=list(im.size),
                           origin=list(origin), sha256=sha(path), **meta))
    for key, (room, src, crop) in ROOMS.items():
        text = re.search(r'\[' + key + r'\]\s*=\s*new\[\]\s*\{([^}]+)\}', code).group(1)
        rects = [list(map(int, r.split(','))) for r in re.findall(r'\(([^)]+)\)', text)]
        cells = {(x,y) for a,b,c,d in rects for x in range(a,c+1) for y in range(b,d+1)}
        mask = Image.new('L', (1040,780)); md = ImageDraw.Draw(mask)
        for x,y in cells: md.rectangle((x*26,y*26,x*26+25,y*26+25), fill=255)
        pattern = load('assets/backgrounds/' + src + '__floor.png').crop(tuple(v*26 for v in crop))
        assert pattern.getchannel('A').getextrema() == (255,255), src
        floor = Image.new('RGBA', mask.size)
        for y in range(0,780,pattern.height):
            for x in range(0,1040,pattern.width): floor.alpha_composite(pattern,(x,y))
        floor.putalpha(mask)
        backing = load('assets/backgrounds/' + src + '__backing.png').resize(mask.size,Image.Resampling.NEAREST)
        backing.putalpha(255)
        # Architectural strips remain outside authored floor cells.
        old_structure = load('assets/backgrounds/' + src + '__structure.png')
        old_fore = load('assets/backgrounds/' + src + '__foreground.png')
        wall = old_structure.crop((4*26,4*26-13,5*26,4*26))
        edge = old_fore.crop((4*26,8*26,5*26,8*26+6))
        structure = Image.new('RGBA',mask.size); foreground = Image.new('RGBA',mask.size)
        for x,y in sorted(cells):
            if (x,y-1) not in cells: structure.alpha_composite(wall,(x*26,y*26-13))
            if (x,y+1) not in cells: foreground.alpha_composite(edge,(x*26,(y+1)*26))
        outside = ImageChops.invert(mask)
        for layer in (structure,foreground): layer.putalpha(ImageChops.multiply(layer.getchannel('A'),outside))
        for layer,im in [('backing',backing),('floor',floor),('structure',structure),('foreground',foreground)]:
            save(im,room+'__'+layer, role=layer,room=room)
        scenes.append(dict(room=room,walkable_rectangles=rects,cells=len(cells),
                           material_source=src,material_crop_cells=list(crop)))
    manifest = json.loads((SOURCE/'manifest.json').read_text(encoding='utf8'))
    for ident in ['r01_coffin_coat','r01_winch_socket','r01_worker_shed','r01_winch_shed','r01_canal_entry']:
        spec = next(a for a in manifest['assets'] if a['id']==ident)
        save(load(spec['path']),ident,tuple(spec['origin']),role='released_sprite_reuse')
    report = dict(schema=1,version='native-n2-hd2d-v1',native_cell_size=26,
                  scope='Developer F10 visual overlay; existing N2 geometry, NPCs and interaction unchanged',
                  source_sha256=inputs,scenes=scenes,assets=assets,runtime_verified=False)
    (OUT/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(assets=len(assets),scenes=len(scenes),output=str(OUT)),ensure_ascii=False))

if __name__=='__main__': main()
