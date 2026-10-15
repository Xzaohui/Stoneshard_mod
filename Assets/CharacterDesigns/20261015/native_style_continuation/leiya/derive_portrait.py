from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import json,hashlib,base64,sys
root=Path(sys.argv[1]); selected=sys.argv[2]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA'); px=list(im.getdata()); c=Counter(x[:3] for x in px if x[3]); a=Counter(x[3] for x in px)
 return {'path':str(p.relative_to(root)),'size':list(im.size),'mode':Image.open(p).mode,'sha256':sha(p),'visible_rgb_colors':len(c),'alpha_levels':len(a),'binary_alpha':set(a)<={0,255},'alpha_bbox':im.getchannel('A').getbbox(),'visible_pixels':sum(c.values()),'partial_alpha_pixels':sum(n for v,n in a.items() if v not in (0,255)), 'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in c.most_common()] if len(c)<=32 else None}
assets=[]
for ret in sorted((root/'tool_returns').glob('portrait_v*.json')):
 name=ret.stem; result=json.loads(ret.read_text()); raw=root/'raw'/f'{name}_raw_imagegen.png'
 data=base64.b64decode(result['image_url'].split(',',1)[1]); raw.write_bytes(data)
 im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST); alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
 visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a]
 strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
 pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
 out=root/'candidates'/f'{name}_74x100_candidate.png';q.save(out)
 q.resize((592,800),Image.Resampling.NEAREST).save(root/'previews'/f'{name}_8x.png')
 board=Image.new('RGB',(980,1030),(108,108,108));d=ImageDraw.Draw(board)
 d.text((20,12),f'{root.name.upper()} / {name} / 74x100 / NN QUANTIZED DERIVATIVE',fill='white')
 d.text((20,36),'1x: dark, gray, light | BELOW: 8x nearest neighbor',fill='white')
 for k,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+k*100,60))
 board.paste(q.resize((592,800),Image.Resampling.NEAREST),(20,195),q.resize((592,800),Image.Resampling.NEAREST))
 d.text((642,215),'Approved style anchors at 2x',fill='white')
 for file,y in [('mara_style_reference.png',255),('iwo_style_reference.png',495)]:
  ref=Image.open(root/'sources'/file).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(660,y),ref)
 board.save(root/'previews'/f'{name}_1x_8x.png')
 m={'raw':metrics(raw),'target':metrics(out),'derivation':{'resize':'Pillow NEAREST entire canvas','crop':None,'alpha_threshold':128,'quantization':'Pillow MEDIANCUT palette from opaque sampled RGB; no dithering','color_budget':32,'drawn_character_geometry':False},'raw_equals_full_tool_return':raw.read_bytes()==data,'native_target_generation':False,'checks':{'exact_dimensions':q.size==(74,100),'visible_color_budget_pass':len(set(p[:3] for p in q.getdata() if p[3]))<=32,'alpha_binary':set(q.getchannel('A').getdata())<={0,255}}}
 (root/'qa'/f'{name}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));assets.append(m)
files=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]
manifest={'actor_id':'n1_rhea' if root.name=='leiya' else 'n1_tor','name':'蕾雅 / Rhea' if root.name=='leiya' else '托雷 / Tor','date':'2026-10-15','selected_portrait':f'candidates/{selected}_74x100_candidate.png','generation_calls':len(assets),'max_attempts':2,'native_authored':False,'runtime_integrated':False,'runtime_verified':False,'independent_qa':'pending','color_budget_note':'32 visible RGB colors is this batch temporary ceiling, not a project-wide hard lock; numerical quantization does not prove designed ramp quality','method':'Built-in imagegen raw preserved; explicit nearest-neighbor and quantized 74x100 derivative. No manual pixel painting.','assets':assets,'files':files}
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({'root':str(root),'selected':manifest['selected_portrait'],'assets':[{'raw':a['raw']['size'],'target':a['target']['size'],'colors':a['target']['visible_rgb_colors'],'sha256':a['target']['sha256']} for a in assets]},ensure_ascii=False))
