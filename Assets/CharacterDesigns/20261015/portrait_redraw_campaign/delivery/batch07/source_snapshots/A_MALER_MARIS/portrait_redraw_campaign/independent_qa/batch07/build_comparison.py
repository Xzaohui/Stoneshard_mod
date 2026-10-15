#!/usr/bin/env python3
"""QA display only. Does not alter production art or supply edited art for selection."""
from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json
OUT = Path(__file__).resolve().parent
CAMP = OUT.parent.parent
selection = json.loads((OUT / 'FINAL_SELECTION.json').read_text())
board = Image.new('RGB', (1280, 860), (102, 102, 102))
draw = ImageDraw.Draw(board)
draw.text((20, 12), 'BATCH 07 / Independent selection / 1x + 4x NN / DERIVED CANDIDATES, NOT NATIVE FINALS', fill='white')
inputs = []
for col, (slug, actor) in enumerate(selection['actors'].items()):
    path = CAMP / slug / actor['selected_candidate']
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == actor['selected_sha256']
    image = Image.open(path).convert('RGBA')
    x = 20 + 315 * col
    draw.text((x, 38), slug.upper() + ' / ' + actor['selected_version'], fill='white')
    for i, bg in enumerate([(12, 12, 15), (102, 102, 102), (235, 235, 229)]):
        tile = Image.new('RGBA', (74, 100), bg + (255,))
        tile.alpha_composite(image)
        board.paste(tile.convert('RGB'), (x + i * 95, 62))
    large = image.resize((296, 400), Image.Resampling.NEAREST)
    board.paste(large, (x, 185), large)
    draw.text((x, 594), digest[:16], fill='white')
    inputs.append(dict(path=str(path.relative_to(CAMP)), sha256=digest))
draw.text((20, 625), 'CORE STYLE REFERENCES 2x / style only, not identity transfer', fill='white')
for i, slug in enumerate(('mara', 'iwo', 'leiya', 'tore')):
    path = CAMP / 'maler/sources' / (slug + '_style_reference.png')
    image = Image.open(path).convert('RGBA').resize((148, 200), Image.Resampling.NEAREST)
    x = 320 + i * 220
    board.paste(image, (x, 650), image)
    draw.text((x - 50, 650), slug, fill='white')
    inputs.append(dict(path=str(path.relative_to(CAMP)), sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
target = OUT / 'selected_candidates_1x_4x.png'
board.save(target)
(OUT / 'comparison_manifest.json').write_text(json.dumps(dict(board=target.name, sha256=hashlib.sha256(target.read_bytes()).hexdigest(), inputs=inputs, purpose='Independent QA display. Exact target PNGs composited on backgrounds and integer-nearest-neighbor enlarged without content edits.'), ensure_ascii=False, indent=2) + '\n')
print(target)
