from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import json,hashlib,base64,sys
r=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA');px=list(im.getdata());c=Counter(x[:3] for x in px if x[3]);a=Counter(x[3] for x in px);bb=im.getchannel('A').getbbox()
 return {'path':str(p.relative_to(r)),'size':list(im.size),'mode':Image.open(p).mode,'sha256':sha(p),'visible_rgb_colors':len(c),'alpha_levels':len(a),'binary_alpha':set(a)<={0,255},'alpha_bbox':bb,'edge_margins':None if bb is None else [bb[0],bb[1],im.width-bb[2],im.height-bb[3]],'visible_pixels':sum(c.values()),'partial_alpha_pixels':sum(n for v,n in a.items() if v not in (0,255)),'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in c.most_common()] if len(c)<=32 else None}
assets=[]
for ret in sorted((r/'tool_returns').glob('portrait_v*.json')):
 name=ret.stem;result=json.loads(ret.read_text());raw=r/'raw'/f'{name}_raw_imagegen.png';data=base64.b64decode(result['image_url'].split(',',1)[1]);raw.write_bytes(data)
 source=Image.open(raw).convert('RGBA');fitbox=(72,98) if name=='portrait_v2' else (74,100);scale=min(fitbox[0]/source.width,fitbox[1]/source.height);scaled=(round(source.width*scale),round(source.height*scale));offset=((74-scaled[0])//2,(100-scaled[1])//2)
 im=Image.new('RGBA',(74,100));im.paste(source.resize(scaled,Image.Resampling.NEAREST),offset);a=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
 visible=[p[:3] for p,v in zip(im.getdata(),a.getdata()) if v];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
 pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE);q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(a);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
 out=r/'candidates'/f'{name}_74x100_candidate.png';q.save(out);up=q.resize((592,800),Image.Resampling.NEAREST);up.save(r/'previews'/f'{name}_8x.png')
 board=Image.new('RGB',(980,1030),(108,108,108));d=ImageDraw.Draw(board);d.text((20,12),f'{r.name.upper()} / {name} / 74x100 / NN QUANTIZED DERIVATIVE',fill='white');d.text((20,36),'1x on dark / gray / light; below 8x NEAREST. No hand pixel painting.',fill='white')
 for k,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+k*100,60))
 board.paste(up,(20,195),up);d.text((640,205),'Core style at 2x',fill='white')
 for file,xy in [('mara',(640,240)),('iwo',(810,240)),('leiya',(640,480)),('tore',(810,480))]:
  ref=Image.open(r/'sources'/f'{file}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,xy,ref)
 board.save(r/'previews'/f'{name}_1x_8x.png')
 m={'raw':metrics(raw),'target':metrics(out),'raw_equals_full_tool_return':raw.read_bytes()==data,'method':{'resize':'whole canvas single-scalar NN fit; v2 safe fit within 72x98 before centered padding on 74x100, preserving complete source silhouette; v1 fit within 74x100','fit_box':fitbox,'scale':scale,'scaled_dimensions':scaled,'offset':offset,'crop':None,'alpha_threshold':128,'quantization':'MEDIANCUT 32-color palette from opaque sampled RGB; no dither','manual_geometry_drawing':False},'native_target_generation':False};(r/'qa'/f'{name}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));assets.append(m)
selected=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'
manifest={'actor_id':'ALD-NPC-'+r.name.upper(),'name':'奇恩' if r.name=='kien' else '科纳','date':'2026-10-15','selected_portrait':f'candidates/{selected}_74x100_candidate.png','generation_calls':len(assets),'max_attempts':2,'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'independent_qa':'pending','method':'Built-in imagegen substantive redraw. Raw preserved, scalar fit NN/alpha/MEDIANCUT derivative, not native-authored final.','color_budget_note':'At most 32 visible RGB colors is temporary candidate ceiling, not a global locked palette.','assets':assets,'files':[{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(r.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]}
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(r/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(r)}' for p in sorted(r.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n');print(json.dumps([{'raw':x['raw']['size'],'target':{k:v for k,v in x['target'].items() if k!='palette_by_frequency'}} for x in assets],ensure_ascii=False))
