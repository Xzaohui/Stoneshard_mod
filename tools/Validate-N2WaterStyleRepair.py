"""Verify complete basin pixels stay within the unchanged blocked rectangles."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageChops

ROOT=Path(__file__).resolve().parents[1]
PACK=ROOT/'src/Art/native-n2-hd2d-v1'
manifest_path=PACK/'manifest.json'
manifest=json.loads(manifest_path.read_text(encoding='utf8'))
layout=json.loads((PACK/'interior-style-layout.json').read_text(encoding='utf8'))
scene=next(s for s in manifest['scenes'] if s['room']=='r_eao_n2_winch')
source_path=ROOT/layout['water_source']
source=Image.open(source_path).convert('RGBA')
colors=[tuple(bytes.fromhex(c.lstrip('#'))) for c in json.loads((ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v2/palettes/bry_r01_128.json').read_text(encoding='utf8'))['colors']]
palette=Image.new('P',(1,1))
palette.putpalette([v for c in colors for v in c]+list(colors[-1])*128)
backing=Image.open(PACK/'assets/r_eao_n2_winch__backing.png').convert('RGBA')
floor=Image.open(PACK/'assets/r_eao_n2_winch__floor.png').getchannel('A')
checks=[]
def require(ok,name):
    if not ok:raise AssertionError(name)
    checks.append(name)

require(scene['water_sampling']==layout['water_sampling']=='whole-basin','complete-basin-sampling')
require(hashlib.sha256(source_path.read_bytes()).hexdigest()==manifest['source_sha256'][layout['water_source']],'painted-basin-source-hash')
require(source.getchannel('A').getextrema()==(255,255),'opaque-basin-with-painted-coping')
for index,(x0,y0,x1,y1) in enumerate(scene['water_rectangles']):
    box=(x0*26,y0*26,(x1+1)*26,(y1+1)*26)
    require(floor.crop(box).getextrema()==(0,0),f'basin-{index}-entirely-outside-walkable-cells')
    actual=backing.crop(box)
    expected=source.resize(actual.size,Image.Resampling.NEAREST).convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
    require(ImageChops.difference(actual,expected).convert('RGB').getbbox() is None,f'basin-{index}-whole-source-and-coping-preserved')
    inner=actual.crop((14,14,actual.width-14,actual.height-14)).convert('RGB')
    rows=[inner.crop((0,y,inner.width,y+1)).tobytes() for y in range(inner.height)]
    require(len(set(rows))>len(rows)*0.8,f'basin-{index}-no-repeated-row-strips')

report=dict(passed=True,checks=checks,count=len(checks),manifestSha256=hashlib.sha256(manifest_path.read_bytes()).hexdigest().upper(),runtimeVerified=False)
(ROOT/'artifacts/n2-water-style-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(report))
