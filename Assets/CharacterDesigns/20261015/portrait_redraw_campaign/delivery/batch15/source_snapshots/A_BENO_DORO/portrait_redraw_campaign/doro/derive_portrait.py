#!/usr/bin/env python3
"""Reproduce technical portrait derivatives from full saved built-in imagegen returns.
No pixel painting: full-canvas proportional NEAREST fit, binary alpha and nondithered palette.
"""
from pathlib import Path
from PIL import Image,ImageDraw
from collections import Counter,deque
import json,base64,hashlib,sys,math
root=Path(__file__).resolve().parent
selected=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def jsonwrite(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def measure(p):
 im=Image.open(p).convert('RGBA');px=list(im.getdata());colors=Counter(x[:3] for x in px if x[3]);a=Counter(x[3] for x in px)
 return {'path':str(p.relative_to(root)),'dimensions':list(im.size),'mode':Image.open(p).mode,'sha256':sha(p),'visible_rgb_colors':len(colors),'alpha_values':sorted(a),'binary_alpha':set(a)<=set([0,255]),'visible_pixels':sum(colors.values()),'partial_alpha_pixels':sum(n for x,n in a.items() if x not in (0,255)),'alpha_bbox':im.getchannel('A').getbbox(),'palette_by_frequency':[{'rgb':list(c),'count':n} for c,n in colors.most_common()] if len(colors)<=32 else None}
def components(im):
 w,h=im.size;a=im.getchannel('A');live={(x,y) for y in range(h) for x in range(w) if a.getpixel((x,y))};groups=[]
 while live:
  first=next(iter(live));live.remove(first);stack=[first];group=[]
  while stack:
   x,y=stack.pop();group.append((x,y))
   for dx,dy in ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)):
    n=(x+dx,y+dy)
    if n in live:live.remove(n);stack.append(n)
  groups.append({'pixels':len(group),'bbox':[min(x for x,y in group),min(y for x,y in group),max(x for x,y in group)+1,max(y for x,y in group)+1],'coordinates':group if len(group)<=8 else None})
 return sorted(groups,key=lambda d:-d['pixels'])
assets=[]
for ret in sorted((root/'tool_returns').glob('portrait_v*.json')):
 name=ret.stem;r=json.loads(ret.read_text());data=base64.b64decode(r['image_url'].split(',',1)[1]);raw=root/'raw'/f'{name}_raw_imagegen.png';raw.write_bytes(data)
 im=Image.open(raw).convert('RGBA');scale=min(74/im.width,100/im.height);size=(max(1,round(im.width*scale)),max(1,round(im.height*scale)))
 scaled=im.resize(size,Image.Resampling.NEAREST);sample=Image.new('RGBA',(74,100));offset=((74-size[0])//2,(100-size[1])//2);sample.paste(scaled,offset)
 alpha=sample.getchannel('A').point(lambda a:255 if a>=128 else 0)
 visible=[p[:3] for p,a in zip(sample.getdata(),alpha.getdata()) if a];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible);pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 q=sample.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()]);out=root/'candidates'/f'{name}_74x100_candidate.png';q.save(out)
 q.save(root/'previews'/f'{name}_1x.png');q8=q.resize((592,800),Image.Resampling.NEAREST);q8.save(root/'previews'/f'{name}_8x.png')
 board=Image.new('RGB',(1040,1040),(104,104,104));d=ImageDraw.Draw(board);d.text((20,14),f'{root.name.upper()} | {name} | 74x100 NN / QUANTIZED DERIVATIVE',fill='white');d.text((20,38),'Top: 1x on dark, gray, light | Bottom: exact 8x nearest',fill='white')
 for i,bg in enumerate(((15,15,18),(104,104,104),(235,235,229))):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(20+i*100,62))
 board.paste(q8,(20,200),q8)
 for i,s in enumerate(('mara','iwo','leiya','tore')):
  ref=Image.open(root/'sources'/f'{s}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST);x=650+(i%2)*180;y=225+(i//2)*245;d.text((x,y-22),f'{s}: 2x style only',fill='white');board.paste(ref,(x,y),ref)
 board.save(root/'previews'/f'{name}_1x_8x.png')
 m={'raw':measure(raw),'target':measure(out),'derivation':{'full_canvas':True,'crop':None,'geometry_edits':False,'resampling':'Pillow NEAREST proportional contain','nominal_uniform_scale':scale,'resized_dimensions':size,'center_padding_offset':offset,'subpixel_rounding_only':True,'alpha_threshold':128,'quantization':'Pillow MEDIANCUT, palette sampled from visible target pixels','color_ceiling':32,'dithering':False},'raw_matches_full_tool_return':raw.read_bytes()==data,'connected_components_8':components(q),'checks':{'dimensions':q.size==(74,100),'color_ceiling':len(set(p[:3] for p in q.getdata() if p[3]))<=32,'binary_alpha':set(q.getchannel('A').getdata())<=set([0,255])},'native_pixel_authorship':False}
 jsonwrite(root/'qa'/f'{name}_metrics.json',m);assets.append(m)
old=json.loads((root/'manifest.json').read_text()) if (root/'manifest.json').exists() else {}
entry=json.loads((root/'sources/roster_entry.json').read_text());out=root/'candidates'/f'{selected}_74x100_candidate.png'
manifest={**old,'character_id':entry['canonical_id'],'name':entry['name'],'date':'2026-10-15','selected_version':selected,'selected_portrait':str(out.relative_to(root)),'selected_portrait_sha256':sha(out),'selected_preview':f'previews/{selected}_1x_8x.png','generated_image_count':len(assets),'max_generation_calls':2,'method':'Built-in imagegen substantive redraw; full original returns retained; proportional full-canvas nearest-neighbor and nondithered quantization derived export, not native 74x100 pixel authorship.','native_pixel_approved':False,'native_pixel_authored':False,'runtime_integrated':False,'runtime_verified':False,'old_assets_modified':False,'character_cards_modified':False,'code_modified':False,'commit_or_push_performed':False,'source_provenance':'sources/source_manifest.json','full_tool_parameters':[f'prompts/{r.stem}.json' for r in sorted((root/'tool_returns').glob('portrait_v*.json'))],'full_tool_returns':[str(r.relative_to(root)) for r in sorted((root/'tool_returns').glob('portrait_v*.json'))],'derivations':assets,'color_ceiling_note':'32 visible RGB is a temporary batch ceiling, not a project-wide palette lock; color count does not establish authored ramp quality.'}
manifest['files']=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ('manifest.json','SHA256SUMS.txt')]
jsonwrite(root/'manifest.json',manifest)
(root/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(root)}\n' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'))
print(json.dumps({'name':entry['name'],'selected':manifest['selected_portrait'],'sha256':sha(out),'versions':[{'raw_size':m['raw']['dimensions'],'colors':m['target']['visible_rgb_colors'],'bbox':m['target']['alpha_bbox'],'components':len(m['connected_components_8'])} for m in assets]},ensure_ascii=False))
