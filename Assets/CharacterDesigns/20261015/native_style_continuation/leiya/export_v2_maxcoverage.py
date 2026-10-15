"""One deterministic palette-only export correction; no character drawing or geometry changes."""
from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import json,hashlib
root=Path(__file__).resolve().parent
raw=root/'raw/portrait_v2_raw_imagegen.png'
im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
a=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
visible=[p[:3] for p,v in zip(im.getdata(),a.getdata()) if v]
strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
pal=strip.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(a);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
name='portrait_v2_maxcoverage'
out=root/'candidates'/f'{name}_74x100_candidate.png';q.save(out)
q.resize((592,800),Image.Resampling.NEAREST).save(root/'previews'/f'{name}_8x.png')
board=Image.new('RGB',(980,1030),(108,108,108));d=ImageDraw.Draw(board)
d.text((20,12),'LEIYA / v2 / 74x100 / NN MAXCOVERAGE QUANTIZED DERIVATIVE',fill='white')
d.text((20,36),'1x: dark, gray, light | BELOW: 8x nearest neighbor',fill='white')
for k,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
 t=Image.new('RGBA',(74,100),bg+(255,));t.alpha_composite(q);board.paste(t.convert('RGB'),(20+k*100,60))
large=q.resize((592,800),Image.Resampling.NEAREST);board.paste(large,(20,195),large)
d.text((642,215),'Approved style anchors at 2x',fill='white')
for file,y in [('mara_style_reference.png',255),('iwo_style_reference.png',495)]:
 ref=Image.open(root/'sources'/file).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(660,y),ref)
board.save(root/'previews'/f'{name}_1x_8x.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
blue=lambda img:sum(1 for r,g,b,a in img.getdata() if a and b>r+5 and b>=g)
old=root/'candidates/portrait_v2_74x100_candidate.png'
record={'reason':'Independent QA found that frequency-weighted MEDIANCUT removed the small-area blue shawl already present in raw. One mechanical quantization alternative only.','old_export_preserved':{'path':str(old.relative_to(root)),'sha256':sha(old),'blue_diagnostic_pixels':blue(Image.open(old).convert('RGBA'))},'source':{'path':str(raw.relative_to(root)),'sha256':sha(raw)},'output':{'path':str(out.relative_to(root)),'sha256':sha(out),'size':list(q.size),'visible_rgb_colors':len(set(p[:3] for p in q.getdata() if p[3])),'alpha_values':sorted(set(q.getchannel('A').getdata())),'blue_diagnostic_pixels':blue(q)},'method':{'resize':'NEAREST whole canvas, same sampling and geometry as original v2 export','alpha_threshold':128,'palette':'Pillow MAXCOVERAGE from visible sampled RGB, 32 colors','dither':False,'painting_or_recoloring_or_geometry_edits':False},'blue_criterion':'B > R + 5 and B >= G, alpha > 0; diagnostic only','pixel_alpha_identical_to_prior':q.getchannel('A').tobytes()==Image.open(old).getchannel('A').tobytes(),'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in Counter(p[:3] for p in q.getdata() if p[3]).most_common()]}
(root/'qa/portrait_v2_maxcoverage_metrics.json').write_text(json.dumps(record,ensure_ascii=False,indent=2));print(json.dumps(record,ensure_ascii=False,indent=2))
