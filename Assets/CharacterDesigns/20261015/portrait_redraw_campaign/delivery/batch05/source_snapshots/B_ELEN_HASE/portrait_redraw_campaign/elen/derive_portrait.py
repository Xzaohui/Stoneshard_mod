from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter
import json,hashlib,base64,sys,re
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA');px=list(im.getdata());colors=Counter(x[:3] for x in px if x[3]);alpha=Counter(x[3] for x in px)
 return {'path':str(p.relative_to(root)),'sha256':sha(p),'size':list(im.size),'mode':Image.open(p).mode,'visible_rgb_colors':len(colors),'alpha_values':sorted(alpha),'binary_alpha':set(alpha)<={0,255},'alpha_bbox':list(im.getchannel('A').getbbox()),'visible_pixels':sum(colors.values()),'partial_alpha_pixels':sum(n for a,n in alpha.items() if a not in (0,255)),'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in colors.most_common()] if len(colors)<=32 else None}
results=[]
for ret in sorted((root/'tool_returns').glob('portrait_v*.json')):
 version=ret.stem;r=json.loads(ret.read_text());data=base64.b64decode(r['image_url'].split(',',1)[1]);raw=root/'raw'/f'{version}_raw_imagegen.png'
 if raw.exists() and raw.read_bytes()!=data:raise ValueError('Raw differs from tool result')
 raw.write_bytes(data)
 im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
 alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
 visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a]
 strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
 palette=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 q=im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha)
 q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
 out=root/'candidates'/f'{version}_74x100_candidate.png';q.save(out)
 zoom=q.resize((592,800),Image.Resampling.NEAREST);zoom.save(root/'previews'/f'{version}_8x.png')
 board=Image.new('RGB',(1030,1030),(91,91,91));draw=ImageDraw.Draw(board)
 draw.text((20,10),f'{root.name.upper()} {version} / 74x100 / NN + 32-color derivative; NOT native authoring',fill='white')
 draw.text((20,32),'1x on dark / gray / light. Below: 8x NEAREST.',fill='white')
 for i,bg in enumerate([(16,16,19),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+i*100,55))
 board.paste(zoom,(20,190),zoom)
 for i,slug in enumerate(['mara','iwo','leiya','tore']):
  ref=Image.open(root/'sources'/f'{slug}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST)
  x=640+(i%2)*180;y=240+(i//2)*265
  draw.text((x,y-20),slug+' approved style 2x',fill='white');board.paste(ref,(x,y),ref)
 board.save(root/'previews'/f'{version}_1x_8x.png')
 original=re.search(r'as (/[^\n]+?\.png) by default',r.get('output_hint',''))
 original_path=Path(original.group(1)) if original else None
 m={'raw':metrics(raw),'target':metrics(out),'raw_equals_full_tool_return':data==raw.read_bytes(),'original_generated_path':str(original_path) if original_path else None,'raw_matches_original_generated_file':sha(original_path)==sha(raw) if original_path and original_path.exists() else None,'derivation':{'resize':'Pillow NEAREST entire image canvas to 74x100','crop':None,'alpha_threshold':128,'quantization':'32-color MEDIANCUT palette extracted from visible sampled RGB; Dither.NONE','transparent_rgb':'set fully transparent samples to 0,0,0','geometry_repaint':False,'native_authored':False},'checks':{'dimensions':q.size==(74,100),'max32':len(set(p[:3] for p in q.getdata() if p[3]))<=32,'binary_alpha':set(q.getchannel('A').getdata())<={0,255}}}
 (root/'qa'/f'{version}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));results.append(m)
row=json.loads((root/'sources/roster_entry.json').read_text())
selection_path=root/'qa/selection.json'
selection=json.loads(selection_path.read_text()) if selection_path.exists() else {}
selected=sys.argv[1] if len(sys.argv)>1 else selection.get('selected_version','portrait_v1')
if selection.get('selected_sha256') and sha(root/'candidates'/f'{selected}_74x100_candidate.png')!=selection['selected_sha256']:raise ValueError('Selected reviewed target hash mismatch')
files=[{'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS.txt']]
manifest={'canonical_id':row['canonical_id'],'name':row['name'],'date':'2026-10-15','selected_portrait':f'candidates/{selected}_74x100_candidate.png','selected_version':selected,'status':selection.get('status','candidate_pending_independent_qa'),'generation_tool':'built-in image_gen.imagegen','generation_calls':len(results),'max_generation_calls':2,'method':'Imagegen substantive redraw followed by explicitly non-native nearest-neighbor + 32-color quantized 74x100 derivative. No pixel repaint or invented details in export.','native_authored':False,'runtime_integrated':False,'runtime_verified':False,'user_approved':False,'independent_qa':selection.get('independent_qa','pending; reviewer writes independent_qa/batch05'),'palette_note':'32 visible colors is a temporary ceiling for this batch only; quantization is not proof of designed native palette ramps.','source_manifest':'sources/source_manifest.json','assets':results,'files':files}
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(root)}\n' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'))
print(json.dumps({'slug':root.name,'selected':manifest['selected_portrait'],'assets':[{k:m['target'][k] for k in ['sha256','size','visible_rgb_colors','alpha_values']} for m in results]},ensure_ascii=False))
