#!/usr/bin/env python3
"""Deterministic technical export; full canvas proportional NEAREST; no native pixel claim."""
from pathlib import Path
from PIL import Image,ImageDraw,__version__ as pillow_version
from collections import Counter
import hashlib,json,base64,sys
root=Path(__file__).resolve().parent;version=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p in ['candidates','previews','qa']: (root/p).mkdir(exist_ok=True)
raw=root/'raw'/f'{version}_raw_imagegen.png';im=Image.open(raw).convert('RGBA');scale=min(72/im.width,98/im.height);size=(round(im.width*scale),round(im.height*scale));offset=((74-size[0])//2,(100-size[1])//2)
sample=Image.new('RGBA',(74,100));sample.paste(im.resize(size,Image.Resampling.NEAREST),offset);alpha=sample.getchannel('A').point(lambda a:255 if a>=128 else 0)
visible=[p[:3] for p,a in zip(sample.getdata(),alpha.getdata()) if a];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible);pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
q=sample.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()]);out=root/'candidates'/f'{version}_74x100_candidate.png';q.save(out)
q.save(root/'previews'/f'{version}_1x.png');q8=q.resize((592,800),Image.Resampling.NEAREST);q8.save(root/'previews'/f'{version}_8x.png')
board=Image.new('RGB',(1110,1060),(104,104,104));d=ImageDraw.Draw(board);d.text((20,14),f'{root.name.upper()} | {version} | 74x100 NN / QUANTIZED DERIVATIVE',fill='white');d.text((20,38),'Top: 1x dark, gray, light | Bottom: exact 8x NN | full canvas contain, 72x98 interior',fill='white')
for i,bg in enumerate(((15,15,18),(104,104,104),(235,235,229))):
 tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+i*100,62))
board.paste(q8,(20,210),q8)
for i,s in enumerate(('mara','iwo','leiya','tore')):
 ref=Image.open(root/'sources'/f'{s}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST);x=650+(i%2)*190;y=245+(i//2)*255;d.text((x,y-22),f'{s}: 2x style only',fill='white');board.paste(ref,(x,y),ref)
board.save(root/'previews'/f'{version}_1x_8x.png')
colors=Counter(p[:3] for p in q.getdata() if p[3]);av=sorted(set(q.getchannel('A').getdata()));bbox=q.getchannel('A').getbbox();rawbytes=base64.b64decode(json.loads((root/'tool_returns'/f'{version}.json').read_text())['image_url'].split(',',1)[1])
m={'version':version,'source_raw':str(raw.relative_to(root)),'source_raw_sha256':sha(raw),'source_dimensions':im.size,'source_raw_matches_full_tool_return':raw.read_bytes()==rawbytes,'target':{'path':str(out.relative_to(root)),'dimensions':[74,100],'sha256':sha(out),'visible_rgb_colors':len(colors),'alpha_values':av,'alpha_bbox':bbox,'visible_pixels':sum(colors.values()),'palette_by_frequency':[{'rgb':list(c),'count':n} for c,n in colors.most_common()]},'derivation':{'pillow_version':pillow_version,'interior_bounds':[72,98],'nominal_uniform_scale':scale,'resized_dimensions':size,'center_padding_offset':offset,'resampling':'Pillow NEAREST proportional contain; raster size round()','crop':None,'local_geometry_edits':False,'painting_or_pixel_cleanup':False,'alpha_threshold':128,'quantization':'MEDIANCUT 32 colors from visible target pixels; Dither.NONE','intent':'Full original raw silhouette preserved, with transparent border at 74x100','additional_generation':False},'checks':{'dimensions':q.size==(74,100),'color_ceiling':len(colors)<=32,'binary_alpha':set(av)<=set([0,255]),'complete_transparent_border':bool(bbox and bbox[0]>0 and bbox[1]>0 and bbox[2]<74 and bbox[3]<100)},'native_pixel_authored':False,'native_pixel_approved':False}
(root/'qa'/f'{version}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
entry=json.loads((root/'sources/roster_entry.json').read_text()); manifest=json.loads((root/'manifest.json').read_text()) if (root/'manifest.json').exists() else {}
versions=sorted(p.stem for p in (root/'prompts').glob('portrait_v*.json'))
manifest.update({'character_id':entry['canonical_id'],'name':entry['name'],'slug':root.name,'date':'2026-10-15','status':'candidate_pending_independent_visual_QA','selected_version':version,'selected_portrait':str(out.relative_to(root)),'selected_portrait_sha256':sha(out),'selected_preview':f'previews/{version}_1x_8x.png','generated_image_count':len(list((root/'raw').glob('*_raw_imagegen.png'))),'method':'Built-in imagegen substantive redraw; full original returns retained; full-canvas proportional nearest-neighbor and nondithered quantization technical derivative, NOT native 74x100 pixel authorship.','native_pixel_approved':False,'native_pixel_authored':False,'runtime_integrated':False,'runtime_verified':False,'old_assets_modified':False,'character_cards_modified':False,'code_modified':False,'commit_or_push_performed':False,'source_provenance':'sources/source_manifest.json','full_tool_parameters':[f'prompts/{v}.json' for v in versions],'full_tool_returns':[f'tool_returns/{v}.json' for v in versions],'selected_export':m,'reproduction':f'python derive_portrait.py {version}','qa_metrics':[str(p.relative_to(root)) for p in sorted((root/'qa').glob('*_metrics.json'))]})
(root/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'slug':root.name,'sha256':sha(out),'colors':len(colors),'bbox':bbox,'checks':m['checks']},ensure_ascii=False))
