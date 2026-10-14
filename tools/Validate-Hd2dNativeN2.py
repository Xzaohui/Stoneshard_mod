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
report=dict(check_count=len(checks),assets=len(m['assets']),scenes=len(m['scenes']),passed=True,runtime_verified=False)
(ROOT/'artifacts/native-n2-art-validation.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
print(json.dumps(report))
