from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import base64, hashlib, json, sys
root=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA'); px=list(im.getdata()); colors=Counter(p[:3] for p in px if p[3]); a=Counter(p[3] for p in px)
 return {'path':str(p.relative_to(root)),'sha256':sha(p),'size':list(im.size),'mode':'RGBA','visible_rgb_colors':len(colors),'alpha_values':sorted(a),'binary_alpha':set(a)<={0,255},'alpha_bbox':im.getchannel('A').getbbox(),'visible_pixels':sum(colors.values()),'partial_alpha_pixels':sum(n for v,n in a.items() if v not in (0,255))}
versions=sys.argv[1:] or [p.stem for p in sorted((root/'tool_returns').glob('portrait_v*.json'))]
for name in versions:
 ret=root/'tool_returns'/f'{name}.json';result=json.loads(ret.read_text());data=base64.b64decode(result['image_url'].split(',',1)[1]);raw=root/'raw'/f'{name}_raw_imagegen.png';raw.write_bytes(data)
 source=Image.open(raw).convert('RGBA'); scale=min(72/source.width,98/source.height); dims=tuple(round(v*scale) for v in source.size); small=source.resize(dims,Image.Resampling.NEAREST)
 im=Image.new('RGBA',(74,100),(0,0,0,0));paste=((74-dims[0])//2,(100-dims[1])//2);im.paste(small,paste)
 alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0);visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible);pal=strip.quantize(colors=32,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.NONE)
 q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()]);out=root/'candidates'/f'{name}_74x100_candidate.png';q.save(out)
 big=q.resize((592,800),Image.Resampling.NEAREST);big.save(root/'previews'/f'{name}_8x.png')
 board=Image.new('RGB',(1010,1020),(105,105,105));d=ImageDraw.Draw(board);d.text((16,14),f'{root.name.upper()} / {name} / 74x100 / NN + 32-COLOR DERIVATIVE',fill='white');d.text((16,35),'1x on three backgrounds | 8x below | Not native-pixel final',fill='white')
 for i,bg in enumerate([(12,12,15),(105,105,105),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(q);board.paste(tile.convert('RGB'),(16+100*i,65))
 board.paste(big,(16,200),big)
 for i,char in enumerate(['mara','iwo','leiya','tore']):
  x=650+(i%2)*170;y=200+(i//2)*280;ref=Image.open(root/'sources'/f'{char}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(x,y),ref);d.text((x,y+210),char,fill='white')
 board.save(root/'previews'/f'{name}_1x_8x.png')
 m={'raw':metrics(raw),'target':metrics(out),'raw_equals_decoded_tool_return':raw.read_bytes()==data,'tool_return_sha256':sha(ret),'native_target_generation':False,'derivation':{'resize':'Pillow NEAREST entire raw canvas, aspect-preserving fit within 72x98; integer dimensions rounded','fit_box':[72,98],'scale':scale,'actual_resize':dims,'crop':None,'canvas':[74,100],'paste_at':paste,'alpha_threshold':128,'quantization':'Pillow MEDIANCUT from opaque sampled RGB, 32 colors, no dithering','transparent_rgb':'zeroed at alpha 0','character_geometry_redrawn_by_script':False,'detail_recovered_or_painted':False},'checks':{'dimensions':q.size==(74,100),'binary_alpha':set(q.getchannel('A').getdata())<={0,255},'visible_color_budget':len(set(p[:3] for p in q.getdata() if p[3]))<=32}}
 (root/'qa'/f'{name}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'candidate':str(out),'size':m['target']['size'],'colors':m['target']['visible_rgb_colors'],'sha256':sha(out)}))
