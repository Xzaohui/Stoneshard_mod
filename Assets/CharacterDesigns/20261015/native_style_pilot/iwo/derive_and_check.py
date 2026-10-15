"""Mechanical derivation/QA only. No character pixels are authored by this script."""
from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import hashlib, json, math

ROOT = Path(__file__).resolve().parent
CONFIG = {
    'portrait_v1': {'canvas': (74, 100), 'colors': 32, 'crop': False},
    'map_v1': {'canvas': (35, 44), 'colors': 20, 'crop': True, 'fit': (33, 42), 'bottom': 43},
    'map_v2': {'canvas': (35, 44), 'colors': 20, 'crop': True, 'fit': (31, 40), 'bottom': 42},
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def info(path):
    im = Image.open(path).convert('RGBA')
    px = list(im.getdata())
    counts = Counter(p[:3] for p in px if p[3])
    alpha = Counter(p[3] for p in px)
    visible = {(x, y) for y in range(im.height) for x in range(im.width) if im.getpixel((x, y))[3]}
    edge = [xy for xy in visible if any((xy[0]+dx, xy[1]+dy) not in visible for dx, dy in ((1,0),(-1,0),(0,1),(0,-1))) ]
    dark = sum(0.2126*im.getpixel(xy)[0]+0.7152*im.getpixel(xy)[1]+0.0722*im.getpixel(xy)[2] < 60 for xy in edge)
    return {
        'file': str(path.relative_to(ROOT)), 'sha256': sha(path), 'mode': Image.open(path).mode,
        'size': list(im.size), 'alpha_bbox': im.getchannel('A').getbbox(),
        'opaque_rgb_colors': len(counts), 'all_rgb_colors': len(set(p[:3] for p in px)),
        'alpha_levels': len(alpha), 'alpha_binary': set(alpha) <= {0,255},
        'partial_alpha_pixels': sum(n for a,n in alpha.items() if a not in (0,255)),
        'visible_pixels': len(visible), 'transparent_nonzero_rgb': sum(1 for p in px if p[3] == 0 and p[:3] != (0,0,0)),
        'boundary_dark_fraction_luma_lt60_4neighbor': round(dark/len(edge),4) if edge else None,
        'palette_by_frequency': [{'rgb': list(c), 'pixels': n} for c,n in counts.most_common()] if len(counts) <= 32 else 'omitted_for_raw',
    }

def derive(name,cfg):
    src = ROOT/'raw'/f'{name}_raw_imagegen.png'
    im = Image.open(src).convert('RGBA')
    box = None
    if cfg['crop']:
        box = im.getchannel('A').point(lambda n: 255 if n >= 128 else 0).getbbox()
        c = im.crop(box)
        scale = min(cfg['fit'][0]/c.width,cfg['fit'][1]/c.height)
        size = tuple(round(n*scale) for n in c.size)
        c = c.resize(size,Image.Resampling.NEAREST)
        x = Image.new('RGBA',cfg['canvas'])
        x.alpha_composite(c,((cfg['canvas'][0]-c.width)//2,cfg['bottom']-c.height))
    else:
        x = im.resize(cfg['canvas'],Image.Resampling.NEAREST)
        size = cfg['canvas']
    alpha = x.getchannel('A').point(lambda n: 255 if n >= 128 else 0)
    q = x.convert('RGB').quantize(colors=cfg['colors'],method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE).convert('RGBA')
    q.putalpha(alpha)
    q.putdata([(r,g,b,a) if a else (0,0,0,0) for r,g,b,a in q.getdata()])
    out = ROOT/'candidates'/f'{name}_{cfg["canvas"][0]}x{cfg["canvas"][1]}_candidate.png'
    q.save(out)
    return {'source':str(src.relative_to(ROOT)), 'output':str(out.relative_to(ROOT)), 'source_crop_bbox_threshold128':box,
            'resample':'Pillow NEAREST', 'resized_size':list(size), 'alpha_threshold':128,
            'quantizer':'Pillow MEDIANCUT, no dithering', 'color_budget':cfg['colors'],
            'geometry_authored_by_script':False, 'native_generation':False}

operations=[derive(k,v) for k,v in CONFIG.items()]
reports=[info(p) for p in sorted((ROOT/'raw').glob('*.png'))]+[info(p) for p in sorted((ROOT/'candidates').glob('*.png'))]
(ROOT/'QA.json').write_text(json.dumps({'operations':operations,'images':reports,
    'technical_gates':'Candidate sizes, binary alpha and numerical color budgets pass. These do not establish native-pixel art quality.',
    'visual_self_review':{
      'portrait_v1':'Keep as style candidate. At 1x, adult identity, cloth cap and nose/cheek planes readable. Warm-brown eye shadows replace purple-black mask. Eye whites are somewhat bright but not isolated glitter pixels. Face occupies less of canvas than native reference.',
      'map_v1':'Fail native-style visual gate: 19x42 visible fit is too tall/thin; face details collapse and legs/coat are noisy.',
      'map_v2':'Fail native-style visual gate after one allowed revision: 21x40 compactness improves but eyes remain large merged dark blocks and lower face becomes a dark column. Material/identity agreement is useful, pixel organization at 1x is insufficient.'},
    'limitations':['Built-in imagegen lacks exact output-size/palette control; all raw outputs are larger than targets with continuous alpha and many colors.',
      'Target-size files are explicitly nearest-neighbor quantized derivatives, not verified native-authored assets.',
      'Automatic quantization contains near-duplicate palette entries; numerical color count is not a hand-designed palette.',
      'No pixel-level manual painting, engine import, runtime test, commit, push or old-asset overwrite performed.'],
    'attempt_budget':{'portrait':{'initial':1,'revision':0},'map':{'initial':1,'revision':1,'further_generation':'stopped'}}},ensure_ascii=False,indent=2),encoding='utf-8')

# Contact sheet contains existing PNGs and labels only, never newly drawn character content.
portrait=Image.open(ROOT/'candidates/portrait_v1_74x100_candidate.png').convert('RGBA')
map_im=Image.open(ROOT/'candidates/map_v2_35x44_candidate.png').convert('RGBA')
board=Image.new('RGB',(1160,1030),(109,109,109));d=ImageDraw.Draw(board)
d.text((20,10),'IVO / PORTRAIT: STYLE CANDIDATE | MAP: VISUAL GATE FAILED',fill='white')
d.text((20,35),'1x on dark / neutral / light backgrounds (native-size files, derived from model images)',fill='white')
for k,bg in enumerate([(15,15,17),(109,109,109),(235,235,225)]):
    for im,x in ((portrait,20+k*140),(map_im,100+k*140)):
        t=Image.new('RGBA',im.size,bg+(255,));t.alpha_composite(im);board.paste(t.convert('RGB'),(x,60))
d.text((20,180),'Portrait 8x nearest neighbor / 74x100 / 31 visible colors',fill='white')
d.text((660,180),'Map v2 12x / 35x44 / 17 visible colors',fill='white')
for im,factor,pos in ((portrait,8,(20,205)),(map_im,12,(650,205))):
    large=im.resize((im.width*factor,im.height*factor),Image.Resampling.NEAREST);board.paste(large,pos,large)
board.save(ROOT/'review/ivo_pair_candidate_1x_8x_12x.png')

files=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name != 'manifest.json']
(ROOT/'manifest.json').write_text(json.dumps({'actor_id':'n1_ivo','design_id':'NPC-N-IVO','date':'2026-10-15',
    'method':'built-in imagegen; independent portrait and map generations; map one targeted imagegen revision; deterministic mechanical nearest-neighbor/quantized derivatives',
    'selected_portrait':'candidates/portrait_v1_74x100_candidate.png','selected_map_for_failure_review':'candidates/map_v2_35x44_candidate.png',
    'native_qualified':False,'runtime_integrated':False,'runtime_verified':False,'parent_qa_required':True,'files':files},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'operations':operations,'candidate_metrics':[x for x in reports if x['file'].startswith('candidates/')]},ensure_ascii=False,indent=2))
