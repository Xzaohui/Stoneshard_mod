#!/usr/bin/env python3
"""Reproduce all packaged v1/v2 candidates independently without changing frozen files."""
from pathlib import Path
from PIL import Image, __version__ as pillow_version
import argparse, base64, hashlib, json
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
base=Path(__file__).resolve().parent;campaign=base/'portrait_redraw_campaign';out=Path(args.output).resolve()
assert not out.exists(),'Choose a new output folder; frozen files remain unchanged';out.mkdir(parents=True)
records=[]
for actor in ['vila','hepo','siyu','buxi']:
 root=campaign/actor
 if not root.exists():continue
 for target in sorted((root/'candidates').glob('portrait_v*_74x100_candidate.png')):
  version=target.name.split('_74x100')[0]
  raw_version=version.removesuffix('_inset');raw=root/'raw'/f'{raw_version}_raw_imagegen.png';ret=json.loads((root/'tool_returns'/f'{raw_version}.json').read_text())
  assert raw.read_bytes()==base64.b64decode(ret['image_url'].split(',',1)[1]),raw
  image=Image.open(raw).convert('RGBA');sample=Image.new('RGBA',(74,100),(0,0,0,0))
  box=(72,98) if version.endswith('_inset') else (74,100);scale=min(box[0]/image.width,box[1]/image.height);size=(round(image.width*scale),round(image.height*scale));offset=((74-size[0])//2,(100-size[1])//2)
  sample.paste(image.resize(size,Image.Resampling.NEAREST),offset)
  sampling={'method':'Pillow NEAREST full-canvas proportional contain with integer dimension rounding','scale':scale,'resized_dimensions':list(size),'paste_offset':list(offset)};method='MAXCOVERAGE'
  alpha=sample.getchannel('A').point(lambda a:255 if a>=128 else 0)
  visible=[px[:3] for px,a in zip(sample.getdata(),alpha.getdata()) if a];strip=Image.new('RGB',(len(visible),1));strip.putdata(visible)
  palette=strip.quantize(colors=32,method=getattr(Image.Quantize,method),dither=Image.Dither.NONE)
  reproduced=sample.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA');reproduced.putalpha(alpha)
  reproduced.putdata([px if px[3] else (0,0,0,0) for px in reproduced.getdata()])
  dest=out/f'{actor}_{target.name}';reproduced.save(dest)
  pixels_equal=reproduced.tobytes()==Image.open(target).convert('RGBA').tobytes();bytes_equal=dest.read_bytes()==target.read_bytes()
  records.append({'actor':actor,'version':version,'quantization':method,'fit_box':list(box),'sampling':sampling,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'raw_tool_return_identical':True,'pixels_equal':pixels_equal,'png_bytes_equal':bytes_equal})
  assert pixels_equal and bytes_equal,records[-1]
assert records,'No production character folders found next to this script'
result={'pillow_version':pillow_version,'all_pass':True,'reproduction_does_not_imply_native_pixel_approval':True,'candidates':records};(out/'reproduction_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
