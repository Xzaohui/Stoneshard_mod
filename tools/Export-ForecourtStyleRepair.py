"""Export painted fine-grain earth using the authored exterior collision mask."""
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'src/Art/scene-style-repairs-20261015'
PACK = ROOT / 'src/Art/native-n2-built-v1'
RAW = BATCH / 'raw/forecourt-earth-v2.png'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    layout = json.loads((PACK / 'layout.json').read_text(encoding='utf-8'))
    tile = layout['tile']
    size = (layout['columns'] * tile, layout['rows'] * tile)
    mask = Image.new('L', size)
    draw = ImageDraw.Draw(mask)
    for x0, y0, x1, y1 in layout['walkable_rectangles']:
        draw.rectangle((x0 * tile, y0 * tile, (x1 + 1) * tile - 1, (y1 + 1) * tile - 1), fill=255)
    for building in layout['buildings']:
        x0, y0, x1, y1 = building['blocked']
        draw.rectangle((x0 * tile, y0 * tile, (x1 + 1) * tile - 1, (y1 + 1) * tile - 1), fill=0)
    output = PACK / 'assets/n2site__floor.png'
    assert ImageChops.difference(mask, Image.open(output).getchannel('A')).getbbox() is None
    lock = (ROOT / 'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v2/spec_lock.md').read_text(encoding='utf-8')
    colors = [tuple(bytes.fromhex(c)) for c in re.findall(r'^  - #([0-9A-F]{6})$', lock, re.M)]
    assert len(colors) == 128
    palette = Image.new('P', (1, 1))
    palette.putpalette([v for c in colors for v in c] + list(colors[-1]) * 128)
    source = Image.open(RAW).convert('RGB')
    ground = source.resize(size, Image.Resampling.NEAREST)
    ground = ground.quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    clean = Image.new('RGBA', size)
    clean.paste(ground, (0, 0), mask)
    clean.save(output)
    manifest_path = PACK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['source_sha256'][RAW.relative_to(ROOT).as_posix()] = sha(RAW)
    entry = next(a for a in manifest['assets'] if a['id'] == 'n2site__floor')
    entry['sha256'] = sha(output)
    entry['repair_source'] = RAW.relative_to(ROOT).as_posix()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    record = dict(source=RAW.relative_to(ROOT).as_posix(), source_sha256=sha(RAW), source_size=list(source.size),
                  output=output.relative_to(ROOT).as_posix(), output_sha256=sha(output),
                  output_size=list(size), resample='nearest', palette='R01-camp-canal-v2/spec_lock.md',
                  alpha='unchanged native walkable mask and three blocked building footprints', runtimeVerified=False)
    (BATCH / 'forecourt-export.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
