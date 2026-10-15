from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import json,hashlib,base64,sys
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA'); c=Counter(p[:3] for p in im.getdata() if p[3]); a=Counter(im.getchannel('A').getdata())
 return {'path':str(p.relative_to(root)),'sha256':sha(p),'size':list(im.size),'mode':im.mode,'visible_rgb_colors':len(c),'alpha_values':sorted(a),'binary_alpha':set(a)<={0,255},'alpha_bbox':im.getchannel('A').getbbox(),'visible_pixels':sum(c.values()),'partial_alpha_pixels':sum(n for v,n in a.items() if v not in [0,255]),'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in c.most_common()] if len(c)<=32 else None}
results=[]
jobs=[(ret, ret.stem, Image.Quantize.MEDIANCUT) for ret in sorted((root/'tool_returns').glob('portrait_v*.json'))]
if (root/'tool_returns/portrait_v2.json').exists():jobs.append((root/'tool_returns/portrait_v2.json','portrait_v2_maxcoverage',Image.Quantize.MAXCOVERAGE))
for ret,v,quant_method in jobs:
 raw=root/'raw'/f'{ret.stem}_raw_imagegen.png'; data=base64.b64decode(json.loads(ret.read_text())['image_url'].split(',',1)[1]); assert raw.read_bytes()==data
 im=Image.open(raw).convert('RGBA'); scale=min(72/im.width,98/im.height); size=(round(im.width*scale),round(im.height*scale)); im=im.resize(size,Image.Resampling.NEAREST)
 out=Image.new('RGBA',(74,100),(0,0,0,0)); offset=((74-size[0])//2,(100-size[1])//2); out.paste(im,offset)
 alpha=out.getchannel('A').point(lambda a:255 if a>=128 else 0); visible=[p[:3] for p,a in zip(out.getdata(),alpha.getdata()) if a]
 strip=Image.new('RGB',(len(visible),1));strip.putdata(visible);pal=strip.quantize(colors=32,method=quant_method,dither=Image.Dither.NONE)
 q=out.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA'); q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
 target=root/'candidates'/f'{v}_74x100_candidate.png';q.save(target); zoom=q.resize((592,800),Image.Resampling.NEAREST);zoom.save(root/'previews'/f'{v}_8x.png')
 board=Image.new('RGB',(1010,1030),(89,89,89));draw=ImageDraw.Draw(board);draw.text((16,10),f'EMO {v} | 74x100 | 32-color NN derivative, not native authorship',fill='white');draw.text((16,32),'1x dark / gray / light; below 8x nearest',fill='white')
 for i,bg in enumerate([(16,16,19),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(16+i*100,55))
 board.paste(zoom,(16,190),zoom)
 for i,s in enumerate(['mara','iwo','leiya','tore']):
  ref=Image.open(root/'sources'/f'{s}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST);x=640+(i%2)*180;y=240+(i//2)*265;draw.text((x,y-20),s+' reference 2x',fill='white');board.paste(ref,(x,y),ref)
 board.save(root/'previews'/f'{v}_1x_8x.png')
 m={'raw':metrics(raw),'target':metrics(target),'raw_equals_full_tool_return':True,'derivation':{'method':'Proportional full-canvas NEAREST containment into 72x98 safe area then transparent 74x100 padding, threshold alpha, declared no-dither palette quantization, transparent RGB zero.','resize':size,'offset':offset,'alpha_threshold':128,'palette_cap':32,'palette_method':('MEDIANCUT' if quant_method==Image.Quantize.MEDIANCUT else 'MAXCOVERAGE'),'cropping':False,'repainting':False,'native_authored':False},'checks':{'dimensions':q.size==(74,100),'max32':len(set(p[:3] for p in q.getdata() if p[3]))<=32,'binary_alpha':set(q.getchannel('A').getdata())<={0,255}}}
 (root/'qa'/f'{v}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));results.append(m)
selected=sys.argv[1] if len(sys.argv)>1 else results[-1]['target']['path'].split('/')[-1].split('_74x')[0]
row=json.loads((root/'sources/campaign_roster_entry.json').read_text()); selection=json.loads((root/'qa/selection.json').read_text()) if (root/'qa/selection.json').exists() else {}; assert not selection.get('selected_sha256') or selection['selected_sha256']==sha(root/'candidates'/f'{selected}_74x100_candidate.png'); manifest={'canonical_id':row['canonical_id'],'name':row['name'],'status':selection.get('status','candidate_pending_independent_qa'),'selected_portrait':f'candidates/{selected}_74x100_candidate.png','selected_version':selected,'selected_portrait_sha256':sha(root/'candidates'/f'{selected}_74x100_candidate.png'),'generation_tool':'built-in image_gen.imagegen','generation_calls':len(list((root/'tool_returns').glob('portrait_v*.json'))),'max_generation_calls':2,'method':'Imagegen actual redraw followed by proportional NEAREST, binary alpha, temporary 32-color quantization. Derived non-native candidate.','native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'user_approved':False,'independent_qa':selection.get('independent_qa','pending'),'old_assets_preserved':True,'source_manifest':'sources/source_manifest.json','assets':results,'files':[{'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS.txt']]};(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));(root/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(root)}\n' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'));print(json.dumps({'selected':selected,'sha256':manifest['selected_portrait_sha256'],'metrics':results[-1]['target']},ensure_ascii=False))
