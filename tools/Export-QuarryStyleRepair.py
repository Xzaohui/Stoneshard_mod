"""Production export of the imagegen quarry repair; native geometry stays authoritative.

Only crop/resample/palette/alpha normalization is deterministic. The painted
ground comes from the retained imagegen source, not a procedural substitute.
"""
import hashlib
import json
import re
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / 'src/Art/scene-style-repairs-20261015'
PACK = ROOT / 'src/Art/hd2d_26x26_20261013'
RAW = BATCH / 'raw/quarry-floor-v2.png'
OUTPUT = PACK / 'assets/backgrounds/r_eao_fx_quarry__floor.png'
# Inward crops exclude model-generated fringes. They correspond, in order,
# to the three native rectangles, never to a new inferred collision map.
CROPS = [(128, 164, 530, 452), (499, 465, 1009, 888), (1019, 282, 1316, 809)]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    source = Image.open(RAW).convert('RGB')
    assert source.size == (1448, 1086), 'Repair source canvas changed'
    code = (ROOT / 'src/EmbersAndOaths/FieldQuest.cs').read_text(encoding='utf-8-sig')
    shapes = re.search(r'\[Quarry\] = new\[\] \{([^}]+)\}', code)[1]
    rectangles = [tuple(map(int, match.split(','))) for match in re.findall(r'\(([^)]+)\)', shapes)]
    assert len(rectangles) == len(CROPS) == 3
    result = Image.new('RGB', (1040, 780))
    mask = Image.new('L', result.size)
    painter = ImageDraw.Draw(mask)
    for crop, (x0, y0, x1, y1) in zip(CROPS, rectangles):
        width, height = (x1 - x0 + 1) * 26, (y1 - y0 + 1) * 26
        part = source.crop(crop).resize((width, height), Image.Resampling.NEAREST)
        result.paste(part, (x0 * 26, y0 * 26))
        painter.rectangle((x0 * 26, y0 * 26, (x1 + 1) * 26 - 1, (y1 + 1) * 26 - 1), fill=255)
    colors = json.loads((PACK / 'palettes/den_n1_128.json').read_text())['colors']
    rgb = [tuple(bytes.fromhex(color.lstrip('#'))) for color in colors]
    palette = Image.new('P', (1, 1))
    palette.putpalette([component for color in rgb for component in color] + list(rgb[-1]) * (256 - len(rgb)))
    result = result.quantize(palette=palette, dither=Image.Dither.NONE).convert('RGBA')
    result.putalpha(mask)
    clean = Image.new('RGBA', result.size)
    clean.paste(result, (0, 0), mask)
    # Compare with the installed export mask before writing, independently
    # of model transparency and crop geometry.
    old_mask = Image.open(OUTPUT).getchannel('A')
    assert ImageChops.difference(old_mask, mask).getbbox() is None
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    clean.save(OUTPUT)
    manifest_path = PACK / 'manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    asset = next(a for a in manifest['assets'] if a['id'] == 'r_eao_fx_quarry__floor')
    asset['sha256'] = sha(OUTPUT)
    asset['repair_source'] = RAW.relative_to(ROOT).as_posix()
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    record = dict(source=RAW.relative_to(ROOT).as_posix(), source_sha256=sha(RAW),
                  source_size=list(source.size), crops=CROPS, native_rectangles=rectangles,
                  output=OUTPUT.relative_to(ROOT).as_posix(), output_sha256=sha(OUTPUT),
                  palette='DEN-N1-128', alpha='unchanged exact native walkable mask',
                  resample='nearest', dither=False, runtimeVerified=False)
    (BATCH / 'quarry-export.json').write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(json.dumps(record, ensure_ascii=False))


if __name__ == '__main__':
    main()
