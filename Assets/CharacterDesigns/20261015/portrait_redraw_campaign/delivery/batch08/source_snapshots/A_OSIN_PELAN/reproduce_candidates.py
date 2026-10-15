#!/usr/bin/env python3
"""Read the extracted package, reproduce into a separate folder, compare PNG bytes."""
from pathlib import Path
from PIL import Image, __version__ as pillow_version
import argparse, base64, hashlib, json

p=argparse.ArgumentParser()
p.add_argument('--output', required=True, help='New empty folder for reproduced files')
args=p.parse_args()
base=Path(__file__).resolve().parent
campaign=base/'portrait_redraw_campaign'
out=Path(args.output).resolve()
assert not out.exists(), 'Use a new output folder; no frozen files are overwritten'
out.mkdir(parents=True)
records=[]
for actor in ['osin','pelan','rena','roan']:
    root=campaign/actor
    if not root.exists(): continue
    for target in sorted((root/'candidates').glob('portrait_v*_74x100_candidate.png')):
        export_tag=target.name.split('_74x100')[0]
        version=export_tag.removesuffix('_maxcoverage').removesuffix('_mediancut')
        method='MAXCOVERAGE' if actor in ('osin','pelan') or export_tag.endswith('_maxcoverage') else 'MEDIANCUT'
        raw=root/'raw'/f'{version}_raw_imagegen.png'
        ret=json.loads((root/'tool_returns'/f'{version}.json').read_text())
        assert raw.read_bytes()==base64.b64decode(ret['image_url'].split(',',1)[1]), raw
        image=Image.open(raw).convert('RGBA')
        sampled=image.resize((74,100),Image.Resampling.NEAREST)
        alpha=sampled.getchannel('A').point(lambda a:255 if a>=128 else 0)
        visible=[px[:3] for px,a in zip(sampled.getdata(),alpha.getdata()) if a]
        strip=Image.new('RGB',(len(visible),1)); strip.putdata(visible)
        palette=strip.quantize(colors=32,method=getattr(Image.Quantize,method),dither=Image.Dither.NONE)
        reproduced=sampled.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
        reproduced.putalpha(alpha)
        reproduced.putdata([px if px[3] else (0,0,0,0) for px in reproduced.getdata()])
        dest=out/f'{actor}_{target.name}'; reproduced.save(dest)
        pixels_equal=reproduced.tobytes()==Image.open(target).convert('RGBA').tobytes()
        bytes_equal=dest.read_bytes()==target.read_bytes()
        records.append({'actor':actor,'version':export_tag,'quantization':method,'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'raw_tool_return_identical':True,'pixels_equal':pixels_equal,'png_bytes_equal':bytes_equal})
        assert pixels_equal and bytes_equal, records[-1]
assert records, 'No character source folders found beside this script'
result={'pillow_version':pillow_version,'all_pass':True,'candidates':records}
(out/'reproduction_report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
