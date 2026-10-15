from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import hashlib,json,sys
root=Path(sys.argv[1]);raw=root/'raw/portrait_v2_raw_imagegen.png';stem='portrait_v2_mediancut'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
a=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
vis=[p[:3] for p,x in zip(im.getdata(),a.getdata()) if x]
s=Image.new('RGB',(len(vis),1));s.putdata(vis)
pal=s.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(a);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
out=root/'candidates'/f'{stem}_74x100_candidate.png';q.save(out)
q.resize((592,800),Image.Resampling.NEAREST).save(root/'previews'/f'{stem}_8x.png')
board=Image.new('RGB',(980,1030),(108,108,108));d=ImageDraw.Draw(board)
d.text((20,12),'SEL / v2 MEDIANCUT / 74x100 / NN QUANTIZED DERIVATIVE',fill='white')
d.text((20,36),'1x: dark, gray, light | BELOW: 8x nearest neighbor',fill='white')
for k,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
 tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+k*100,60))
q8=q.resize((592,800),Image.Resampling.NEAREST);board.paste(q8,(20,195),q8)
d.text((642,215),'V2 MAXCOVERAGE / MEDIANCUT at 2x',fill='white')
for file,y in [('portrait_v2_74x100_candidate.png',255),(f'{stem}_74x100_candidate.png',495)]:
 r=Image.open(root/'candidates'/file).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(r,(660,y),r)
board.save(root/'previews'/f'{stem}_1x_8x.png')
c=Counter(p[:3] for p in q.getdata() if p[3]);prior=Image.open(root/'candidates/portrait_v2_74x100_candidate.png').convert('RGBA')
m={'raw':{'path':str(raw.relative_to(root)),'sha256':sha(raw)},'target':{'path':str(out.relative_to(root)),'sha256':sha(out),'size':list(q.size),'visible_rgb_colors':len(c),'alpha_values':sorted(set(a.getdata())),'alpha_bbox':a.getbbox(),'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in c.most_common()]},'derivation':{'resize':'Whole-canvas Pillow NEAREST to 74x100','crop':None,'alpha_threshold':128,'palette':'Pillow MEDIANCUT from visible sampled RGB, no dithering','budget':32,'painting_recoloring_geometry_edits':False,'alpha_identical_to_maxcoverage':list(a.getdata())==list(prior.getchannel('A').getdata())},'reason':'Independent QA found MAXCOVERAGE caused salt-like light flecks on skin. One mechanical export comparison only; raw and original MAXCOVERAGE exports preserved.','native_authored':False,'runtime_verified':False}
(root/'qa'/f'{stem}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));print(json.dumps({'target':m['target']['path'],'sha256':m['target']['sha256'],'colors':len(c),'same_alpha':m['derivation']['alpha_identical_to_maxcoverage']},ensure_ascii=False))
