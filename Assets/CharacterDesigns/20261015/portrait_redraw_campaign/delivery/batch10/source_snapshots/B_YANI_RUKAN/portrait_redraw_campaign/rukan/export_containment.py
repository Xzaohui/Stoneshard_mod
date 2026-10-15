from pathlib import Path
from PIL import Image, ImageDraw
from collections import Counter
import json,hashlib,sys
r=Path(__file__).resolve().parent
v=sys.argv[1] if len(sys.argv)>1 else 'portrait_v2'
method=sys.argv[2] if len(sys.argv)>2 else 'MAXCOVERAGE'
assert method in ['MAXCOVERAGE','MEDIANCUT']
raw=r/'raw'/f'{v}_raw_imagegen.png';source=Image.open(raw).convert('RGBA')
scale=min(72/source.width,98/source.height)
size=(round(source.width*scale),round(source.height*scale));offset=((74-size[0])//2,(100-size[1])//2)
im=source.resize(size,Image.Resampling.NEAREST)
a=im.getchannel('A').point(lambda x:255 if x>=128 else 0)
visible=[p[:3] for p,x in zip(im.getdata(),a.getdata()) if x]
strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
pal=strip.quantize(colors=32,method=getattr(Image.Quantize,method),dither=Image.Dither.NONE)
q=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');q.putalpha(a);q.putdata([p if p[3] else (0,0,0,0) for p in q.getdata()])
canvas=Image.new('RGBA',(74,100),(0,0,0,0));canvas.paste(q,offset)
name=v+'_containment'+('_mediancut' if method=='MEDIANCUT' else '');out=r/'candidates'/f'{name}_74x100_candidate.png';canvas.save(out)
big=canvas.resize((592,800),Image.Resampling.NEAREST);big.save(r/'previews'/f'{name}_8x.png')
board=Image.new('RGB',(1030,1050),(105,105,105));d=ImageDraw.Draw(board)
d.text((16,14),f'{r.name.upper()} / {name} / FULL RAW ASPECT FIT {size} ON 74x100 AT {offset}',fill='white')
d.text((16,38),'1x black, gray, light | 8x below | DERIVATIVE, NO RECOVERY OF RAW EDGE DETAIL',fill='white')
for i,bg in enumerate([(12,12,15),(105,105,105),(235,235,229)]):
 t=Image.new('RGBA',(74,100),bg+(255,));t.alpha_composite(canvas);board.paste(t.convert('RGB'),(16+100*i,65))
board.paste(big,(16,200),big)
for i,(f,label) in enumerate([('mara_style_reference.png','Mara v2'),('iwo_style_reference.png','Iwo v1'),('leiya_style_reference.png','Leiya v2'),('tore_style_reference.png','Tore v1')]):
 x=650+(i%2)*180;y=200+(i//2)*280;ref=Image.open(r/'sources'/f).convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(ref,(x,y),ref);d.text((x,y+210),label,fill='white')
board.save(r/'previews'/f'{name}_1x_8x.png')
colors=Counter(p[:3] for p in canvas.getdata() if p[3]);alpha=Counter(canvas.getchannel('A').getdata())
base=json.loads((r/'qa'/f'{v}_maxcoverage_metrics.json').read_text())
base['target']={'path':str(out.relative_to(r)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'size':list(canvas.size),'mode':canvas.mode,'visible_rgb_colors':len(colors),'alpha_values':sorted(alpha),'binary_alpha':set(alpha)<={0,255},'alpha_bbox':canvas.getchannel('A').getbbox(),'visible_pixels':sum(colors.values()),'partial_alpha_pixels':0,'palette_by_frequency':[{'rgb':rgb,'pixels':n} for rgb,n in colors.most_common()]}
base['derivation']={'resize':'Pillow NEAREST entire raw canvas, aspect-preserving fit within 72x98 with integer dimensions rounded','raw_dimensions':list(source.size),'fit_box':[72,98],'scale':scale,'actual_resize':list(size),'crop':None,'alpha_threshold':128,'quantization':f'Pillow {method} from opaque sampled RGB, 32 colors, no dithering','transparent_rgb':'zeroed for alpha 0','canvas':[74,100],'paste_at':list(offset),'centering':'integer floor offset; any odd spare pixel remains on bottom/right','character_geometry_redrawn_by_script':False,'detail_recovered_or_painted':False,'limitation':'Raw opaque alpha>=128 does not touch the outermost columns, but its side margins are less than one target logical pixel and NN sampling makes the 74x100 version touch the border. Whole silhouette completeness is not independently proven. Containment adds a transparent margin only; no content is painted or restored.'}
raw_alpha=source.getchannel('A'); raw_mask=raw_alpha.point(lambda x:255 if x>=128 else 0)
base['raw_margin_analysis']={'alpha128_bbox':raw_mask.getbbox(),'outer_left_max_alpha':raw_alpha.crop((0,0,1,source.height)).getextrema()[1],'outer_right_max_alpha':raw_alpha.crop((source.width-1,0,source.width,source.height)).getextrema()[1],'meaning':'Sub-logical-pixel margins; not proof of missing hair tips.'}
base['same_raw_technical_variant']=True;base['additional_imagegen_call']=False
base['checks']={'dimensions':canvas.size==(74,100),'binary_alpha':set(alpha)<={0,255},'visible_color_budget':len(colors)<=32,'all_four_canvas_borders_fully_transparent':all(canvas.getpixel((x,y))[3]==0 for x in range(74) for y in [0,99]) and all(canvas.getpixel((x,y))[3]==0 for y in range(100) for x in [0,73])}
(r/'qa'/f'{name}_metrics.json').write_text(json.dumps(base,ensure_ascii=False,indent=2)+'\n')
(r/'prompts'/f'{name}_export_parameters.json').write_text(json.dumps(base['derivation'],ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'candidate':str(out),'sha256':base['target']['sha256'],'actual_resize':size,'offset':offset,'alpha_bbox':base['target']['alpha_bbox'],'colors':len(colors),'checks':base['checks']}))
