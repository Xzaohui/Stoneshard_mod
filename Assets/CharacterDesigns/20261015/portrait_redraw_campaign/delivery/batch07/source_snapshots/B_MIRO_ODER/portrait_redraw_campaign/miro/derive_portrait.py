from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import json, hashlib, base64
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA');rgb=Counter(p[:3] for p in im.getdata() if p[3]);a=Counter(im.getchannel('A').getdata())
 return {'path':str(p.relative_to(root)),'size':list(im.size),'mode':Image.open(p).mode,'sha256':sha(p),'visible_rgb_colors':len(rgb),'alpha_levels':sorted(a),'binary_alpha':set(a)<={0,255},'alpha_bbox':im.getchannel('A').getbbox(),'visible_pixels':sum(rgb.values()),'partial_alpha_pixels':sum(n for k,n in a.items() if k not in (0,255)),'palette_by_frequency':[{'rgb':list(c),'pixels':n} for c,n in rgb.most_common()] if len(rgb)<=32 else None}
for ret in sorted((root/'tool_returns').glob('portrait_v*.json')):
 key=ret.stem;data=json.loads(ret.read_text())
 if 'image_url' not in data: continue
 raw_data=base64.b64decode(data['image_url'].split(',',1)[1]);raw=root/'raw'/f'{key}_raw_imagegen.png';raw.write_bytes(raw_data)
 im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST);alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
 visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
 pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()]);out=root/'candidates'/f'{key}_74x100_candidate.png';q.save(out)
 enlarged=q.resize((592,800),Image.Resampling.NEAREST);enlarged.save(root/'previews'/f'{key}_8x.png')
 board=Image.new('RGB',(1000,1020),(108,108,108));draw=ImageDraw.Draw(board);draw.text((20,10),f'{root.name.upper()} / {key} / 74x100 NN + QUANTIZED DERIVATIVE',fill='white');draw.text((20,32),'1x: dark / gray / light; bottom: 8x NEAREST',fill='white')
 for i,c in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),c+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+i*100,55))
 board.paste(enlarged,(20,190),enlarged)
 draw.text((640,10),'APPROVED STYLE ANCHORS 2x',fill='white')
 for filename,x,y in [('mara_style_reference.png',640,55),('iwo_style_reference.png',820,55),('leiya_style_reference.png',640,290),('tore_style_reference.png',820,290)]:
  r=Image.open(root/'sources'/filename).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(r,(x,y),r)
 board.save(root/'previews'/f'{key}_1x_8x.png')
 report={'raw':metrics(raw),'target':metrics(out),'raw_equals_full_tool_return':raw.read_bytes()==raw_data,'derivation':{'resize':'whole canvas Pillow NEAREST to 74x100','crop':None,'quantization':'Pillow MEDIANCUT opaque sampled RGB palette','max_colors':32,'dither':False,'alpha_threshold':128,'transparent_rgb':'0,0,0','drawn_geometry':False},'native_target_generation':False,'checks':{'exact_dimensions':q.size==(74,100),'visible_color_budget_pass':len(set(p[:3] for p in q.getdata() if p[3]))<=32,'binary_alpha':set(q.getchannel('A').getdata())<={0,255}}}
 (root/'qa'/f'{key}_metrics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(root.name,key,report['target'])
