"""Pixel/export validation; serialized native room validation is in GameProbe."""
import hashlib
import json
import re
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'src/Art/native-n2-built-v1'
def main():
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
    layout=json.loads((OUT/'layout.json').read_text(encoding='utf8'))
    lock=(ROOT/'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v2/spec_lock.md').read_text(encoding='utf8')
    palette={tuple(bytes.fromhex(c)) for c in re.findall(r'^  - #([0-9A-F]{6})$',lock,re.M)}
    assert len(palette)==128
    checks=[]
    def require(ok,name):
        assert ok,name
        checks.append(name)
    for name,sha in manifest['source_sha256'].items():
        require(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==sha,'source:'+name)
    for a in manifest['assets']:
        p=OUT/a['path'];im=Image.open(p).convert('RGBA')
        require(hashlib.sha256(p.read_bytes()).hexdigest()==a['sha256'],a['id']+':sha')
        require(list(im.size)==a['size'],a['id']+':size')
        require(set(im.getchannel('A').get_flattened_data())<={0,255},a['id']+':binary-alpha')
        require({tuple(c[:3]) for c in im.get_flattened_data() if c[3]}<=palette,a['id']+':palette')
    cells={(x,y) for a,b,c,d in layout['walkable_rectangles'] for x in range(a,c+1) for y in range(b,d+1)}
    for b in layout['buildings']:
        a,b,c,d=b['blocked'];cells-={(x,y) for x in range(a,c+1) for y in range(b,d+1)}
    floor=Image.open(OUT/'assets/n2site__floor.png').getchannel('A')
    for x in range(layout['columns']):
        for y in range(layout['rows']):
            val=255 if (x,y) in cells else 0
            require(floor.crop((x*26,y*26,(x+1)*26,(y+1)*26)).getextrema()==(val,val),f'floor-alpha:{x},{y}')
    result=dict(checks=checks,count=len(checks),passed=True,runtimeVerified=False)
    (ROOT/'artifacts/n2-scene-art-validation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(passed=True,checks=len(checks),assets=len(manifest['assets']))))
if __name__=='__main__':main()
