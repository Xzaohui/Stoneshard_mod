from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import base64, hashlib, json, sys
root=Path(__file__).resolve().parent
version=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def metrics(p):
 im=Image.open(p).convert('RGBA');px=list(im.getdata());colors=Counter(p[:3] for p in px if p[3]);a=Counter(p[3] for p in px)
 return {'path':str(p.relative_to(root)),'sha256':sha(p),'size':list(im.size),'mode':Image.open(p).mode,'visible_rgb_colors':len(colors),'alpha_values':sorted(a),'binary_alpha':set(a)<={0,255},'alpha_bbox':list(im.getchannel('A').getbbox()),'visible_pixels':sum(colors.values()),'partial_alpha_pixels':sum(n for v,n in a.items() if v not in (0,255)),'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in colors.most_common()] if len(colors)<=32 else None}
ret=root/'tool_returns'/f'{version}.json'; result=json.loads(ret.read_text());data=base64.b64decode(result['image_url'].split(',',1)[1]);raw=root/'raw'/f'{version}_raw_imagegen.png';raw.write_bytes(data)
im=Image.open(raw).convert('RGBA'); raw_size=im.size;scale=min(72/im.width,98/im.height);fit=(round(im.width*scale),round(im.height*scale));im=im.resize(fit,Image.Resampling.NEAREST);offset=((74-fit[0])//2,(100-fit[1])//2)
alpha=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
visible=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
pal=strip.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(alpha);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()]);target=Image.new('RGBA',(74,100));target.paste(q,offset)
out=root/'candidates'/f'{version}_74x100_candidate.png';target.save(out)
big=target.resize((592,800),Image.Resampling.NEAREST);big.save(root/'previews'/f'{version}_8x.png')
board=Image.new('RGB',(1030,1050),(105,105,105));d=ImageDraw.Draw(board);d.text((16,14),f'{root.name.upper()} / {version} / 74x100 / NN + QUANTIZED DERIVATIVE',fill='white');d.text((16,38),'1x on black, gray, light | 8x below | NOT native-pixel final',fill='white')
for i,bg in enumerate([(12,12,15),(105,105,105),(235,235,229)]):
 tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(target);board.paste(tile.convert('RGB'),(16+100*i,65))
board.paste(big,(16,200),big)
for i,(f,label) in enumerate([('mara_style_reference.png','Mara v2'),('iwo_style_reference.png','Ivo v1'),('leiya_style_reference.png','Leiya v2'),('tore_style_reference.png','Tor v1')]):
 x=650+(i%2)*180;y=200+(i//2)*280;ref=Image.open(root/'sources'/f).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(x,y),ref);d.text((x,y+210),label,fill='white')
board.save(root/'previews'/f'{version}_1x_8x.png')
edge=[target.getpixel((x,0))[3] for x in range(74)]+[target.getpixel((x,99))[3] for x in range(74)]+[target.getpixel((0,y))[3] for y in range(100)]+[target.getpixel((73,y))[3] for y in range(100)]
m={'raw':metrics(raw),'target':metrics(out),'raw_equals_decoded_tool_return':raw.read_bytes()==data,'native_target_generation':False,'derivation':{'resize':'Pillow NEAREST entire raw canvas aspect-preserving fit within 72x98, integer-rounded dimensions','raw_dimensions':raw_size,'scale':scale,'actual_resize':fit,'offset':offset,'crop':None,'alpha_threshold':128,'quantization':'Pillow MAXCOVERAGE from opaque sampled RGB, 32 colors, no dithering','transparent_rgb':'zeroed for alpha 0','character_geometry_redrawn_by_script':False,'detail_restored':False},'checks':{'dimensions':target.size==(74,100),'binary_alpha':set(target.getchannel('A').getdata())<={0,255},'visible_color_budget':len(set(p[:3] for p in target.getdata() if p[3]))<=32,'all_four_canvas_borders_fully_transparent':max(edge)==0}}
(root/'qa'/f'{version}_metrics.json').write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'candidate':str(out),'size':m['target']['size'],'colors':m['target']['visible_rgb_colors'],'raw_size':raw_size,'bbox':m['target']['alpha_bbox'],'sha256':sha(out)}))
