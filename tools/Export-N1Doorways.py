"""Package imagegen-painted N1 thresholds at native scale; no new painted pixels."""
import hashlib
import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / 'src/Art/native-n1-doorways-v1'
PALETTE = ROOT / 'src/Art/hd2d_26x26_20261013/palettes/den_n1_128.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    colors = [tuple(bytes.fromhex(c.lstrip('#'))) for c in json.loads(PALETTE.read_text(encoding='utf8'))['colors']]
    palette = Image.new('P', (1, 1))
    palette.putpalette([v for c in colors for v in c] + list(colors[-1]) * (256-len(colors)))
    manifest = dict(schema=1, batch='N1-doorways-v1', status='exported-runtime-unverified', native_cell_size=26,
                    source_sha256={PALETTE.relative_to(ROOT).as_posix(): sha(PALETTE)}, assets=[], doors=[])
    (PACK / 'assets').mkdir(exist_ok=True)
    preview = Image.new('RGBA', (312, 78), (35, 35, 32, 255))
    for index, (name, raw) in enumerate((('causeway_steps', 'causeway-steps-v1'),
                                         ('bell_threshold', 'bell-threshold-v1'), ('drain_steps', 'drain-steps-v1'))):
        source = PACK / 'raw' / (raw + '.png')
        manifest['source_sha256'][source.relative_to(ROOT).as_posix()] = sha(source)
        image = Image.open(source).convert('RGBA')
        alpha = image.getchannel('A').point(lambda v: 255 if v >= 128 else 0)
        image.putalpha(alpha)
        image = image.crop(alpha.getbbox())
        image.thumbnail((52, 39), Image.Resampling.NEAREST)
        alpha = image.getchannel('A')
        image = image.convert('RGB').quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
        image.putalpha(alpha)
        sprite = Image.new('RGBA', (52, 39))
        sprite.alpha_composite(image, ((52-image.width)//2, 39-image.height))
        ident = 'n1_' + name
        path = PACK / 'assets' / (ident + '.png')
        sprite.save(path)
        manifest['assets'].append(dict(id=ident, path='assets/'+path.name, size=[52, 39], origin=[26, 26],
                                       alpha_bbox=list(sprite.getchannel('A').getbbox()), role='doorway_floor_stamp',
                                       palette='DEN-N1-128', sha256=sha(path)))
        preview.alpha_composite(sprite.resize((104, 78), Image.Resampling.NEAREST), (index*104, 0))
    for room, obj, x, y, art in (
        ('r_eao_n1_yard', 'home', 7, 24, 'causeway_steps'),
        ('r_eao_n1_yard', 'to_bell', 32, 9, 'bell_threshold'),
        ('r_eao_n1_bellhouse', 'to_yard', 7, 22, 'bell_threshold'),
        ('r_eao_n1_bellhouse', 'to_drain', 34, 17, 'drain_steps'),
        ('r_eao_n1_underpass', 'to_house', 6, 22, 'drain_steps')):
        manifest['doors'].append(dict(room=room, object='o_eao_n1_'+obj, cell=[x, y], art='n1_'+art))
    (PACK / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+'\n', encoding='utf8')
    preview.save(PACK / 'preview.png')
    print(json.dumps(dict(assets=len(manifest['assets']), doors=len(manifest['doors']),
                          bounds={a['id']: a['alpha_bbox'] for a in manifest['assets']})))


if __name__ == '__main__':
    main()
