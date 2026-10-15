from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import json, hashlib, base64, sys

root = Path(sys.argv[1]); version = sys.argv[2]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def metrics(p):
    im = Image.open(p).convert('RGBA'); px = list(im.getdata())
    c = Counter(x[:3] for x in px if x[3]); a = Counter(x[3] for x in px)
    return {'path': str(p.relative_to(root)), 'size': list(im.size), 'sha256': sha(p), 'visible_rgb_colors': len(c), 'alpha_values': sorted(a), 'binary_alpha': set(a) <= {0,255}, 'alpha_bbox': im.getchannel('A').getbbox(), 'visible_pixels': sum(c.values()), 'partial_alpha_pixels': sum(n for v,n in a.items() if v not in (0,255)), 'palette_by_frequency': [{'rgb': rgb, 'pixels': n} for rgb,n in c.most_common()] if len(c) <= 32 else None}

raw = root/'raw'/f'{version}_raw_imagegen.png'
ret = json.loads((root/'tool_returns'/f'{version}.json').read_text())
assert base64.b64decode(ret['image_url'].split(',',1)[1]) == raw.read_bytes()
source = Image.open(raw).convert('RGBA')
# One scalar fit, inverse-mapped pixel centers; no per-axis stretch, crop, or painting.
scale = min(74/source.width, 100/source.height)
dx = (74-source.width*scale)/2; dy = (100-source.height*scale)/2
im = Image.new('RGBA',(74,100),(0,0,0,0))
sp = source.load(); tp = im.load()
for y in range(100):
    sy = int((y+.5-dy)/scale)
    for x in range(74):
        sx = int((x+.5-dx)/scale)
        if 0 <= sx < source.width and 0 <= sy < source.height:
            tp[x,y]=sp[sx,sy]
alpha = im.getchannel('A').point(lambda a: 255 if a >= 128 else 0)
visible = [p[:3] for p,a in zip(im.getdata(), alpha.getdata()) if a]
strip = Image.new('RGB', (len(visible), 1)); strip.putdata(visible)
pal = strip.quantize(colors=32, method=Image.Quantize.MAXCOVERAGE, dither=Image.Dither.NONE)
out = im.convert('RGB').quantize(palette=pal, dither=Image.Dither.NONE).convert('RGBA')
out.putalpha(alpha); out.putdata([p if p[3] else (0,0,0,0) for p in out.getdata()])
target = root/'candidates'/f'{version}_74x100_candidate.png'; out.save(target)
large = out.resize((592,800), Image.Resampling.NEAREST)
large.save(root/'previews'/f'{version}_8x.png')
board = Image.new('RGB', (1000,1000), (100,100,100)); d = ImageDraw.Draw(board)
d.text((20,14), f'{root.name.upper()} / {version} / 74x100 NN QUANTIZED DERIVATIVE', fill='white')
d.text((20,38), '1x on dark / gray / light; below: 8x nearest neighbor', fill='white')
for i,bg in enumerate([(15,15,18),(100,100,100),(238,235,229)]):
    tile=Image.new('RGBA',(74,100), bg+(255,)); tile.alpha_composite(out); board.paste(tile.convert('RGB'),(20+i*100,62))
board.paste(large,(20,190),large)
d.text((650,210), 'Approved anchors at 2x', fill='white')
for label,y in [('mara',250),('leiya',490)]:
    ref=Image.open(root/'sources'/f'{label}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST); board.paste(ref,(680,y),ref)
board.save(root/'previews'/f'{version}_1x_8x.png')
m={'raw':metrics(raw),'target':metrics(target),'derivation':{'resize':'single-scale nearest-neighbor inverse pixel-center mapping to contain whole canvas','isotropic_scale':scale,'offset_xy':[dx,dy],'crop':None,'alpha_threshold':128,'quantization':'Pillow MAXCOVERAGE from visible sampled RGB','color_budget':32,'dither':False,'manual_painting_or_geometry_edits':False},'native_authored':False,'runtime_integrated':False,'raw_equals_stored_full_tool_return':True}
(root/'qa'/f'{version}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
print(json.dumps({'root':str(root),'target':m['target']},ensure_ascii=False))
