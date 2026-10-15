from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import json,hashlib
r=Path(__file__).resolve().parent; name='portrait_v2_mediancut'
raw=r/'raw/portrait_v2_raw_imagegen.png'; im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
a=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
pixels=[p[:3] for p,v in zip(im.getdata(),a.getdata()) if v]
strip=Image.new('RGB',(len(pixels),1));strip.putdata(pixels)
pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(a);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
out=r/f'candidates/{name}_74x100_candidate.png';q.save(out);up=q.resize((592,800),Image.Resampling.NEAREST);up.save(r/f'previews/{name}_8x.png')
board=Image.new('RGB',(980,1030),(108,108,108));d=ImageDraw.Draw(board);d.text((20,12),'IVE / V2 MEDIANCUT / SAME RAW, NN QUANTIZED DERIVATIVE',fill='white');d.text((20,36),'1x dark / gray / light. 8x nearest below; no painting.',fill='white')
for i,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
 tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+i*100,60))
board.paste(up,(20,195),up);d.text((640,215),'V2 MAXCOVERAGE at 3x',fill='white');old=Image.open(r/'candidates/portrait_v2_74x100_candidate.png').convert('RGBA').resize((222,300),Image.Resampling.NEAREST);board.paste(old,(640,250),old);board.save(r/f'previews/{name}_1x_8x.png')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
metrics={'name':name,'raw':'raw/portrait_v2_raw_imagegen.png','raw_sha256':sha(raw),'target':str(out.relative_to(r)),'target_sha256':sha(out),'target_size':list(q.size),'visible_rgb_colors':len(set(p[:3] for p in q.getdata() if p[3])),'binary_alpha':set(q.getchannel('A').getdata())<={0,255},'method':'whole-canvas NEAREST, alpha threshold 128, MEDIANCUT from visible sampled RGB, no dither','purpose':'Mechanical alternate export to reduce MAXCOVERAGE-induced facial color fragmentation; no imagegen call or painting.','native_authored':False}
(r/f'qa/{name}_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2));print(json.dumps(metrics,ensure_ascii=False))
