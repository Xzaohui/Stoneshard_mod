from pathlib import Path
import json, hashlib, base64, sys, platform
from collections import Counter
from PIL import Image, __version__ as PIL_VERSION
W=Path(__file__).resolve().parent
version=sys.argv[1] if len(sys.argv)>1 else 'portrait_v1'
raw=W/'raw'/f'{version}_raw_imagegen.png'
profile=sys.argv[2] if len(sys.argv)>2 else 'full'
export_tag=version+'_'+profile if profile!='full' else version
fit_box={'full':(74,100),'inset':(72,98),'containment':(70,96)}[profile]
source=Image.open(raw).convert('RGBA')
s= min(fit_box[0]/source.width,fit_box[1]/source.height)
size=(round(source.width*s),round(source.height*s))
small=source.resize(size,Image.Resampling.NEAREST)
canvas=Image.new('RGBA',(74,100),(0,0,0,0)); canvas.paste(small,((74-size[0])//2,(100-size[1])//2))
mask=canvas.getchannel('A').point(lambda x:255 if x>=128 else 0)
visible=[rgb[:3] for rgb,a in zip(canvas.getdata(),mask.getdata()) if a]
samples=Image.new('RGB',(len(visible),1));samples.putdata(visible)
palette=samples.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
q=canvas.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB')
out=Image.new('RGBA',(74,100)); out.putdata([(*rgb,a) if a else (0,0,0,0) for rgb,a in zip(q.getdata(),mask.getdata())])
target=W/'candidates'/f'{export_tag}_74x100_candidate.png';out.save(target)
out.save(W/'previews'/f'{export_tag}_1x.png')
out.resize((592,800),Image.Resampling.NEAREST).save(W/'previews'/f'{export_tag}_8x.png')
board=Image.new('RGB',(74*3+16,100+8),(100,100,100))
for i,bg in enumerate([(20,20,22),(115,115,115),(235,231,220)]):
 tile=Image.new('RGBA',(74,100),(*bg,255));tile.alpha_composite(out);board.paste(tile.convert('RGB'),(4+i*78,4))
board.save(W/'previews'/f'{export_tag}_1x_backgrounds.png')
board.resize((board.width*4,board.height*4),Image.Resampling.NEAREST).save(W/'previews'/f'{export_tag}_4x_backgrounds.png')
return_data=json.loads((W/'tool_returns'/f'{version}.json').read_text()); encoded=return_data['image_url'].split(',',1)[1];same=base64.b64decode(encoded)==raw.read_bytes()
counts=Counter(rgb[:3] for rgb in out.getdata() if rgb[3]); alpha=sorted(set(out.getchannel('A').getdata()))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
metrics={'version':export_tag,'raw':{'path':str(raw.relative_to(W)),'sha256':sha(raw),'dimensions':list(source.size),'byte_identical_to_full_tool_return':same},'candidate':{'path':str(target.relative_to(W)),'sha256':sha(target),'dimensions':list(out.size),'mode':out.mode,'visible_rgb_colors':len(counts),'alpha_values':alpha,'alpha_bbox':out.getchannel('A').getbbox(),'partial_alpha_pixels':sum(0<a<255 for a in out.getchannel('A').getdata()),'palette_by_frequency':[{'rgb':list(c),'count':n} for c,n in counts.most_common()]},'method':{'substantive_imagegen_redraw':True,'native_pixel_authored':False,'resize':'isotropic fit entire canvas with NEAREST, integer-rounded output dimensions; no crop or geometric redrawing','scale':s,'fit_box':fit_box,'same_raw_technical_inset':profile!='full','export_profile':profile,'resized_dimensions':list(size),'alpha_threshold':128,'palette':'MAXCOVERAGE <=32 visible colors, no dithering','transparent_rgb':'zero','technical_export_only':True},'checks':{'dimensions':out.size==(74,100),'color_budget':len(counts)<=32,'binary_alpha':alpha==[0,255],'full_tool_return_matches_raw':same},'environment':{'python':platform.python_version(),'pillow':PIL_VERSION}}
(W/'qa'/f'{export_tag}_metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'version':export_tag,'candidate':metrics['candidate']['path'],'sha':sha(target),'raw_dimensions':source.size,'colors':len(counts),'alpha':alpha,'bbox':metrics['candidate']['alpha_bbox'],'checks':metrics['checks']}))
