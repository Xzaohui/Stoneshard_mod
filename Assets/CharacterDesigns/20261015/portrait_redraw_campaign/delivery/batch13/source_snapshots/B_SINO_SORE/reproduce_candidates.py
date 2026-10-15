#!/usr/bin/env python3
"""Reproduce all candidate PNGs from packaged raw data into a new separate directory."""
from pathlib import Path
from PIL import Image, __version__ as pillow_version
import argparse, base64, hashlib, json
p=argparse.ArgumentParser(); p.add_argument('--output',required=True); args=p.parse_args()
base=Path(__file__).resolve().parent; campaign=base/'portrait_redraw_campaign'
out=Path(args.output).resolve(); assert not out.exists(),'Use a new output folder; frozen files stay unchanged'; out.mkdir(parents=True)
records=[]
for actor in ['muko','naetin','sino','sore']:
 root=campaign/actor
 if not root.exists(): continue
 for target in sorted((root/'candidates').glob('portrait_v*_74x100_candidate.png')):
  export_tag=target.name.split('_74x100')[0]; version=export_tag.removesuffix('_inset')
  raw=root/'raw'/f'{version}_raw_imagegen.png';ret=json.loads((root/'tool_returns'/f'{version}.json').read_text())
  assert raw.read_bytes()==base64.b64decode(ret['image_url'].split(',',1)[1]),raw
  image=Image.open(raw).convert('RGBA'); inset=actor in ['sino','sore'] or '_inset' in export_tag
  box=(72,98) if inset else (74,100); scale=min(box[0]/image.width,box[1]/image.height)
  size=(round(image.width*scale),round(image.height*scale));offset=((74-size[0])//2,(100-size[1])//2)
  sampled=image.resize(size,Image.Resampling.NEAREST)
  # Preserve each production pipeline's operation order, including alpha-zero RGB handling.
  if actor in ['muko','naetin']:
   canvas=Image.new('RGBA',(74,100),(0,0,0,0));canvas.paste(sampled,offset);sampled=canvas
  alpha=sampled.getchannel('A').point(lambda a:255 if a>=128 else 0)
  visible=[px[:3] for px,a in zip(sampled.getdata(),alpha.getdata()) if a]
  strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
  palette=strip.quantize(colors=32,method=Image.Quantize.MAXCOVERAGE,dither=Image.Dither.NONE)
  reproduced=sampled.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
  reproduced.putalpha(alpha);reproduced.putdata([px if px[3] else (0,0,0,0) for px in reproduced.getdata()])
  if actor in ['sino','sore']:
   canvas=Image.new('RGBA',(74,100),(0,0,0,0));canvas.paste(reproduced,offset);reproduced=canvas
  dest=out/f'{actor}_{target.name}';reproduced.save(dest)
  pixels_equal=reproduced.tobytes()==Image.open(target).convert('RGBA').tobytes();bytes_equal=dest.read_bytes()==target.read_bytes()
  records.append({'actor':actor,'version':export_tag,'quantization':'MAXCOVERAGE','fit_box':list(box),'resize':list(size),'paste_offset':list(offset),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'raw_tool_return_identical':True,'pixels_equal':pixels_equal,'png_bytes_equal':bytes_equal})
  assert pixels_equal and bytes_equal,records[-1]
assert records,'No character source folders found beside this script'
result={'pillow_version':pillow_version,'all_pass':True,'candidates':records}
(out/'reproduction_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n'); print(json.dumps(result,ensure_ascii=False,indent=2))
