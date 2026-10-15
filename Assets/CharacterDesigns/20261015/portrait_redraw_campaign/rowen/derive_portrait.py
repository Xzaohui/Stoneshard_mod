from pathlib import Path
from PIL import Image, ImageDraw, __version__ as pillow_version
from collections import Counter
import json,hashlib,base64,sys
root=Path(sys.argv[1]); variant=sys.argv[2] if len(sys.argv)>2 else 'portrait_v1'
maxcoverage=len(sys.argv)>3 and sys.argv[3]=='maxcoverage'
method=Image.Quantize.MAXCOVERAGE if maxcoverage else Image.Quantize.MEDIANCUT
export_tag=variant+'_maxcoverage' if maxcoverage else variant
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA');px=list(im.getdata());c=Counter(p[:3] for p in px if p[3]);a=Counter(p[3] for p in px)
 return {'path':str(p.relative_to(root)),'size':list(im.size),'mode':Image.open(p).mode,'sha256':sha(p),'visible_rgb_colors':len(c),'alpha_levels':len(a),'binary_alpha':set(a)<={0,255},'alpha_bbox':im.getchannel('A').getbbox(),'visible_pixels':sum(c.values()),'partial_alpha_pixels':sum(n for v,n in a.items() if v not in (0,255)),'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in c.most_common()] if len(c)<=32 else None}
ret=json.loads((root/'tool_returns'/f'{variant}.json').read_text());raw=root/'raw'/f'{variant}_raw_imagegen.png'
encoded=base64.b64decode(ret['image_url'].split(',',1)[1]);assert raw.read_bytes()==encoded
im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
alpha=im.getchannel('A').point(lambda a:255 if a>=128 else 0)
visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a]
strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
pal=strip.quantize(colors=32,method=method,dither=Image.Dither.NONE)
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
out=root/'candidates'/f'{export_tag}_74x100_candidate.png';q.save(out)
q.resize((592,800),Image.Resampling.NEAREST).save(root/'previews'/f'{export_tag}_8x.png')
board=Image.new('RGB',(1150,1020),(94,94,94));d=ImageDraw.Draw(board)
d.text((20,12),f'{root.name.upper()} / {export_tag} / 74x100 / NN + 32-color derivative',fill='white')
d.text((20,35),'1x on dark / gray / light; 8x below. Not native pixel-authored.',fill='white')
for k,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
 tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+k*100,60))
large=q.resize((592,800),Image.Resampling.NEAREST);board.paste(large,(20,195),large)
d.text((650,195),'Style anchors 2x',fill='white')
for file,(x,y) in zip(['mara_style_reference.png','iwo_style_reference.png','leiya_style_reference.png','tore_style_reference.png'],[(660,230),(850,230),(660,480),(850,480)]):
 ref=Image.open(root/'sources'/file).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(x,y),ref);d.text((x,y+205),file.split('_')[0],fill='white')
board.save(root/'previews'/f'{export_tag}_1x_8x.png')
m={'raw':metrics(raw),'target':metrics(out),'derivation':{'pillow_version':pillow_version,'resize':'Pillow NEAREST entire canvas','crop':None,'alpha_threshold':128,'quantization':('MAXCOVERAGE' if maxcoverage else 'MEDIANCUT')+' 32 palette from post-NN pixels whose thresholded alpha is 255, then quantize full RGB to that palette; no dithering','transparent_rgb_normalized':[0,0,0],'drawn_character_geometry':False},'raw_equals_full_tool_return':True,'native_target_generation':False,'checks':{'exact_dimensions':q.size==(74,100),'visible_color_budget_pass':len(set(p[:3] for p in q.getdata() if p[3]))<=32,'alpha_binary':set(q.getchannel('A').getdata())<={0,255}}}
(root/'qa'/f'{export_tag}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2));
record=json.loads((root/'sources/roster_record.json').read_text())
manifest={'canonical_id':record['canonical_id'],'name':record['name'],'slug':root.name,'date':'2026-10-15','selected_portrait':str(out.relative_to(root)),'selected_raw':str(raw.relative_to(root)),'generation_calls':len(list((root/'tool_returns').glob('portrait_v*.json'))),'max_attempts':2,'status':'draft_ready_for_independent_QA','native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'independent_qa':'pending','color_budget_note':'32 visible RGB colors is a temporary campaign ceiling; numerical quantization does not prove palette design quality','method':'Built-in imagegen redraw with complete raw/tool return; explicit full-canvas nearest-neighbor resize and palette-quantized 74x100 derivative. Not native one-pixel-at-a-time artwork.','source_manifest':'sources/source_manifest.json','selected_metrics':m,'source_priority':'current card governs age and identity; historic art only where consistent','files':[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['manifest.json','SHA256SUMS.txt']]}
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(root/'SHA256SUMS.txt').write_text('\n'.join(f'{sha(p)}  {p.relative_to(root)}' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt')+'\n')
print(json.dumps({'slug':root.name,'target':m['target'],'pillow':pillow_version},ensure_ascii=False))
