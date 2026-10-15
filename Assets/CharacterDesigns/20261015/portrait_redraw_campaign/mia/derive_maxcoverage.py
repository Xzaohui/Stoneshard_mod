from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import hashlib,json
root=Path(__file__).resolve().parent
raw=root/'raw/portrait_v2_raw_imagegen.png'
im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a]
strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
pal=strip.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha)
q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
out=root/'candidates/portrait_v2_maxcoverage_74x100_candidate.png';q.save(out)
large=q.resize((592,800),Image.Resampling.NEAREST);large.save(root/'previews/portrait_v2_maxcoverage_8x.png')
board=Image.new('RGB',(980,1030),(108,108,108));d=ImageDraw.Draw(board)
d.text((20,12),'MIA / v2 MAXCOVERAGE / 74x100 / NN + QUANTIZED DERIVATIVE',fill='white')
d.text((20,36),'1x: dark, gray, light | BELOW: 8x nearest neighbor',fill='white')
for k,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
 tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+k*100,60))
board.paste(large,(20,195),large)
d.text((642,215),'Approved style anchors at 2x',fill='white')
for name,y in [('mara_style_reference.png',255),('leiya_style_reference.png',495)]:
 ref=Image.open(root/'sources'/name).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(660,y),ref)
board.save(root/'previews/portrait_v2_maxcoverage_1x_8x.png')
old=Image.open(root/'candidates/portrait_v2_74x100_candidate.png').convert('RGBA')
colors=Counter(p[:3] for p in q.getdata() if p[3])
teal=lambda x:sum(1 for p in x.getdata() if p[3] and p[1]>p[0]+10 and p[2]>p[0]+10)
report={'reason':'MEDIANCUT v2 compressed original blue-teal shawl to one near-gray teal. Mechanically test MAXCOVERAGE without geometry edits or paint.','source':str(raw.relative_to(root)),'source_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'output':str(out.relative_to(root)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'size':list(q.size),'visible_rgb_colors':len(colors),'alpha_values':sorted(set(q.getchannel('A').getdata())),'alpha_identical_to_mediancut':q.getchannel('A').tobytes()==old.getchannel('A').tobytes(),'resize':'whole-canvas NEAREST','palette':'Pillow MAXCOVERAGE 32 visible colors, no dither','alpha_threshold':128,'native_pixel_authorship_claim':False,'painting_geometry_edit_or_recoloring':False,'teal_diagnostic_criterion':'G>R+10 and B>R+10; alpha>0; diagnostic only','teal_diagnostic_pixels_before':teal(old),'teal_diagnostic_pixels_after':teal(q),'palette_by_frequency':[{'rgb':c,'pixels':n} for c,n in colors.most_common()]}
(root/'qa/portrait_v2_maxcoverage_metrics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='palette_by_frequency'},ensure_ascii=False))

