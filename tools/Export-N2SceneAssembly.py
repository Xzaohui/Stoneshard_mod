"""Assemble frozen R01 pixels on explicit native geometry; no AI generation."""
import hashlib
import json
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'src/Art/hd2d_26x26_20261013/batches/R01-camp-canal-v2'
OUT = ROOT / 'src/Art/native-n2-built-v1'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    layout = json.loads((OUT/'layout.json').read_text(encoding='utf8'))
    source = json.loads((SOURCE/'manifest.json').read_text(encoding='utf8'))
    specs = {a['id']: a for a in source['assets']}
    inputs = {str((OUT/'layout.json').relative_to(ROOT)).replace('\\','/'):sha(OUT/'layout.json')}
    def load(ident):
        p = SOURCE/specs[ident]['path']
        assert sha(p) == specs[ident]['sha256'], ident
        inputs[str(p.relative_to(ROOT)).replace('\\','/')] = sha(p)
        return Image.open(p).convert('RGBA')
    def lock():
        # Re-read the existing approved execution contract for each export.
        assert 'binary-alpha' in (SOURCE/'spec_lock.md').read_text(encoding='utf8')
    (OUT/'assets').mkdir(exist_ok=True)
    assets=[]
    def save(im, ident, origin=(0,0), **meta):
        p=OUT/'assets'/(ident+'.png');im.save(p)
        assets.append(dict(id=ident,path='assets/'+p.name,size=list(im.size),origin=list(origin),sha256=sha(p),**meta))
    tile=layout['tile'];size=(layout['columns']*tile,layout['rows']*tile)
    cells={(x,y) for a,b,c,d in layout['walkable_rectangles'] for x in range(a,c+1) for y in range(b,d+1)}
    for item in layout['buildings']:
        a,b,c,d=item['blocked'];cells-={(x,y) for x in range(a,c+1) for y in range(b,d+1)}
    mask=Image.new('L',size);md=ImageDraw.Draw(mask)
    for x,y in cells:md.rectangle((x*tile,y*tile,x*tile+25,y*tile+25),fill=255)
    for layer in ['backing','floor','structure','foreground']:
        lock()
        im=Image.new('RGBA',size)
        if layer=='backing':
            im=load('r01_camp__backing').resize(size,Image.Resampling.NEAREST);im.putalpha(255)
            # Blocked building cells still rest on stone, not on the water
            # background. Rendering the foundation never makes it walkable.
            pattern=load('r01_camp__floor').crop((5*tile,10*tile,17*tile,18*tile))
            ground=Image.new('RGBA',size)
            for y in range(0,size[1],pattern.height):
                for x in range(0,size[0],pattern.width):ground.alpha_composite(pattern,(x,y))
            for b in layout['buildings']:
                a,c,d,e=b['blocked'];box=(a*tile,c*tile,(d+1)*tile,(e+1)*tile)
                im.alpha_composite(ground.crop(box),(box[0],box[1]))
        elif layer=='floor':
            pattern=load('r01_camp__floor').crop((5*tile,10*tile,17*tile,18*tile))
            assert pattern.getchannel('A').getextrema()==(255,255)
            for y in range(0,size[1],pattern.height):
                for x in range(0,size[0],pattern.width):im.alpha_composite(pattern,(x,y))
            im.putalpha(mask)
        save(im,'n2site__'+layer,role=layer)
    for ident in dict.fromkeys([b['source'] for b in layout['buildings']]+[p['source'] for p in layout['props']]):
        lock();save(load(ident),'n2site_'+ident,tuple(specs[ident]['origin']),role='released_sprite_reuse',source_id=ident)
    report=dict(schema=1,version='native-n2-built-v1',native_cell_size=tile,source_sha256=inputs,assets=assets,
                walkable_cells=len(cells),runtime_verified=False,scope='Native exterior buildings, collision footprint and doors; interior nonblocking scenery')
    (OUT/'manifest.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps(dict(assets=len(assets),walkable_cells=len(cells)),ensure_ascii=False))

if __name__=='__main__':main()
