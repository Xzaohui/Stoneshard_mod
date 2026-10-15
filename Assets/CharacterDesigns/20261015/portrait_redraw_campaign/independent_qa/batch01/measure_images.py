"""Read-only production QA. Writes only alongside this script; never imports/runs production code."""
from pathlib import Path
from collections import Counter, deque
from PIL import Image
import hashlib, json, base64, re, sys
ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
NAMES=['mia','ena','nara','nell','sel']
sha=lambda data:hashlib.sha256(data).hexdigest()
def components(im, diagonals=False):
    w,h=im.size; pts={(x,y) for y in range(h) for x in range(w) if im.getpixel((x,y))[3]}
    offsets=[(-1,0),(1,0),(0,-1),(0,1)]
    if diagonals: offsets +=[(-1,-1),(-1,1),(1,-1),(1,1)]
    cc=[]
    while pts:
        s=next(iter(pts)); pts.remove(s); queue=[s]; cells=[s]
        while queue:
            x,y=queue.pop()
            for dx,dy in offsets:
                v=(x+dx,y+dy)
                if v in pts:pts.remove(v);queue.append(v);cells.append(v)
        cc.append(cells)
    cc.sort(key=len,reverse=True)
    return {'count':len(cc),'sizes':[len(v) for v in cc],'small_components':[sorted(v) for v in cc[1:] if len(v)<=20]}
def metric(p):
    im=Image.open(p).convert('RGBA'); pixels=list(im.getdata()); colors=Counter(t[:3] for t in pixels if t[3]>0); alpha=Counter(t[3] for t in pixels)
    box=im.getchannel('A').getbbox()
    m={'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes()),'size':list(im.size),'mode':Image.open(p).mode,'visible_rgb_count':len(colors),'visible_pixels':sum(colors.values()),'alpha_values':sorted(alpha),'partial_alpha_pixels':sum(v for k,v in alpha.items() if k not in (0,255)),'bbox':list(box) if box else None,'effective_size':[box[2]-box[0],box[3]-box[1]] if box else [0,0],'transparent_rgb_nonzero':sum(1 for r,g,b,a in pixels if a==0 and any((r,g,b)))}
    if im.size==(74,100):
        m['palette']=[{'rgb':list(k),'count':v} for k,v in colors.most_common()]
        m['single_pixel_colors']=sum(v==1 for v in colors.values())
        m['components_4']=components(im);m['components_8']=components(im,True)
        m['technical_pass']=len(colors)<=32 and set(alpha)<={0,255} and m['transparent_rgb_nonzero']==0
    return m

def raw_links(char):
    out=[]
    for p in (ROOT/char/'tool_returns').glob('*.json'):
        d=json.loads(p.read_text()); u=d.get('image_url','')
        if not u.startswith('data:image/'):continue
        data=base64.b64decode(u.split(',',1)[1]); raw_sha=sha(data)
        matches=[str(f.relative_to(ROOT)) for f in (ROOT/char/'raw').glob('*.png') if sha(f.read_bytes())==raw_sha]
        hint=d.get('output_hint',''); returned_source=re.findall(r'/workspace/[^\s`]+\.png',hint)
        source=[]
        for s in dict.fromkeys(returned_source):
            q=Path(s);source.append({'path':s,'exists':q.exists(),'same_bytes':q.exists() and q.read_bytes()==data})
        out.append({'return_path':str(p.relative_to(ROOT)),'return_sha256':sha(p.read_bytes()),'decoded_image_sha256':raw_sha,'identical_raw_files':matches,'original_output_hint_sources':source})
    return out

def recreate(raw, method, palette_scope):
    im=Image.open(raw).convert('RGBA').resize((74,100),Image.Resampling.NEAREST)
    alpha=im.getchannel('A').point(lambda v:255 if v>=128 else 0)
    rgb=im.convert('RGB')
    meth={'MEDIANCUT':Image.Quantize.MEDIANCUT,'MAXCOVERAGE':Image.Quantize.MAXCOVERAGE}[method]
    if palette_scope=='opaque':
        vals=[p[:3] for p,a in zip(im.getdata(),alpha.getdata()) if a]
        strip=Image.new('RGB',(len(vals),1));strip.putdata(vals)
        palette=strip.quantize(colors=32,method=meth,dither=Image.Dither.NONE)
        result=rgb.quantize(palette=palette,dither=Image.Dither.NONE).convert('RGBA')
    else:result=rgb.quantize(colors=32,method=meth,dither=Image.Dither.NONE).convert('RGBA')
    result.putalpha(alpha)
    result.putdata([p if p[3] else (0,0,0,0) for p in result.getdata()])
    return result

def main():
    result={'date_utc':'2026-10-15','pillow_version':Image.__version__,'note':'Independent read-only recomputation. No production script executed. Technical pass does not mean visual/native-art pass.','characters':{}}
    for c in NAMES:
        folder=ROOT/c
        paths=sorted(set(list((folder/'candidates').glob('*.png'))+list((folder/'assets').glob('portrait*.png'))+list((folder/'raw').glob('portrait*.png'))))
        x={'images':[metric(p) for p in paths],'raw_provenance':raw_links(c)}
        result['characters'][c]=x
    (OUT/'measurements.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    repro_config=OUT/'reproduction_config.json'
    if repro_config.exists():
        repro=[]
        for cfg in json.loads(repro_config.read_text()):
            im=recreate(ROOT/cfg['raw'],cfg['method'],cfg['palette_scope'])
            actual=Image.open(ROOT/cfg['target']).convert('RGBA')
            matches=im.size==actual.size and im.tobytes()==actual.tobytes()
            out={**cfg,'rgba_pixel_exact':matches,'different_pixel_count':sum(p!=q for p,q in zip(im.getdata(),actual.getdata())),'target_sha256':sha((ROOT/cfg['target']).read_bytes()),'recreated_rgba_sha256':sha(im.tobytes()),'actual_rgba_sha256':sha(actual.tobytes())}
            repro.append(out)
        (OUT/'reproduction_checks.json').write_text(json.dumps(repro,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({c:[{k:m[k] for k in ['path','size','visible_rgb_count','bbox','sha256']} for m in x['images']] for c,x in result['characters'].items()},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
