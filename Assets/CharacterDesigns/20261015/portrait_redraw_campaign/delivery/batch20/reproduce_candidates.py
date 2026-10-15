#!/usr/bin/env python3
"""Reproduce every packaged historical candidate from complete raw/tool returns."""
from pathlib import Path
from PIL import Image, __version__ as pillow_version
import argparse,base64,hashlib,json
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
base=Path(__file__).resolve().parent;campaign=base/'portrait_redraw_campaign';out=Path(args.output).resolve()
assert not out.exists(),'Choose a new output folder; frozen files remain unchanged';out.mkdir(parents=True)
records=[]
for actor in ['luling','noda','sailuo','naya']:
 root=campaign/actor
 if not root.exists():continue
 for target in sorted((root/'candidates').glob('portrait_v*_74x100_candidate.png')):
  tag=target.name.split('_74x100')[0];version=tag.removesuffix('_inset').removesuffix('_safe')
  raw=root/'raw'/f'{version}_raw_imagegen.png';ret=json.loads((root/'tool_returns'/f'{version}.json').read_text())
  assert raw.read_bytes()==base64.b64decode(ret['image_url'].split(',',1)[1]),raw
  image=Image.open(raw).convert('RGBA');box=(70,96) if tag.endswith('_safe') else ((72,98) if tag.endswith('_inset') else (74,100))
  scale=min(box[0]/image.width,box[1]/image.height);size=(round(image.width*scale),round(image.height*scale));offset=((74-size[0])//2,(100-size[1])//2)
  small=image.resize(size,Image.Resampling.NEAREST);canvas=Image.new('RGBA',(74,100),(0,0,0,0));canvas.paste(small,offset)
  alpha=canvas.getchannel('A').point(lambda a:255 if a>=128 else 0)
  visible=[px[:3] for px,a in zip(canvas.getdata(),alpha.getdata()) if a];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
  palette=strip.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
  rgb=canvas.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGB')
  reproduced=Image.new('RGBA',(74,100));reproduced.putdata([(*px,a) if a else (0,0,0,0) for px,a in zip(rgb.getdata(),alpha.getdata())])
  dest=out/f'{actor}_{target.name}';reproduced.save(dest)
  pixels_equal=reproduced.tobytes()==Image.open(target).convert('RGBA').tobytes();bytes_equal=dest.read_bytes()==target.read_bytes()
  records.append({'actor':actor,'version':tag,'held_actor':actor=='naya','quantization':'MAXCOVERAGE','fit_box':list(box),'sampling':{'method':'Pillow NEAREST full-canvas proportional contain with integer dimension rounding','resized_dimensions':list(size),'paste_offset':list(offset)},'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'raw_tool_return_identical':True,'pixels_equal':pixels_equal,'png_bytes_equal':bytes_equal})
  assert pixels_equal and bytes_equal,records[-1]
assert records,'No production character folders found next to this script'
result={'pillow_version':pillow_version,'all_pass':True,'held_reproduction_is_not_visual_approval':True,'candidates':records};(out/'reproduction_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
