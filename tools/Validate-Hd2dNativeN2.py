"""Check derived art against source bytes and native N2 floor geometry."""
import json, re, hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'src/Art/native-n2-hd2d-v1'
m=json.loads((P/'manifest.json').read_text(encoding='utf8'))
checks=[]
def check(ok,label):
    if not ok: raise AssertionError(label)
    checks.append(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in m['source_sha256'].items():check(sha(ROOT/p)==h,'source:'+p)
for a in m['assets']:
    p=P/a['path'];im=Image.open(p).convert('RGBA')
    check(sha(p)==a['sha256'],a['id']+':sha')
    check(list(im.size)==a['size'],a['id']+':size')
    check(set(im.getchannel('A').tobytes())<={0,255},a['id']+':binary-alpha')
    if a.get('style_repair'):
        check(all(px[3] or px[:3]==(0,0,0) for px in im.get_flattened_data()),a['id']+':transparent-rgb-zero')
for s in m['scenes']:
    cells={(x,y) for a,b,c,d in s['walkable_rectangles'] for x in range(a,c+1) for y in range(b,d+1)}
    alpha=Image.open(P/'assets'/(s['room']+'__floor.png')).convert('RGBA').getchannel('A')
    for y in range(30):
        for x in range(40):
            target=255 if (x,y) in cells else 0
            check(alpha.crop((x*26,y*26,x*26+26,y*26+26)).getextrema()==(target,target),s['room']+f':floor-cell-{x}-{y}')
    for layer in ['structure','foreground']:
        a=Image.open(P/'assets'/(s['room']+'__'+layer+'.png')).getchannel('A')
        check(all(a.crop((x*26,y*26,x*26+26,y*26+26)).getextrema()==(0,0) for x,y in cells),s['room']+':'+layer+'-outside-floor')
if m.get('style_repair'):
    layout=json.loads((P/'interior-style-layout.json').read_text(encoding='utf8'))
    for spec in layout['scenes']:
        scene=next(s for s in m['scenes'] if s['room']==spec['room'])
        check(scene['door_anchors']==spec['doors'],spec['room']+':doorway-contract')
        check(scene['backing_style']==spec['backing'],spec['room']+':backing-contract')
        if spec['backing']=='cutaway-dark':
            backing=Image.open(P/'assets'/(spec['room']+'__backing.png')).convert('RGBA')
            check(len(set(backing.get_flattened_data()))==1,spec['room']+':cutaway-outside-has-no-boulder-mosaic')
    sprite=next(a for a in m['assets'] if a['id']=='r01_doorway_open')
    check(sprite['size']==[52,65] and sprite['origin']==[26,52],'doorway-foot-at-cell-bottom')
report=dict(check_count=len(checks),assets=len(m['assets']),scenes=len(m['scenes']),passed=True,runtime_verified=False)
(ROOT/'artifacts/native-n2-art-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8',newline='\n')
print(json.dumps(report))
