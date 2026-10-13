import json,sys,pathlib,hashlib,shutil
from PIL import Image
root=pathlib.Path(__file__).resolve().parents[2]
b=root/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012'
x=json.loads(pathlib.Path(sys.argv[1]).read_text());folder=b/('batch'+str(x['batch']));folder.mkdir(exist_ok=True)
out=folder/x['filename'];assert not out.exists(),out
shutil.copy2(x['generated_file'],out)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x.update(saved_file=str(out),sha256=h(out),bytes=out.stat().st_size,status='review-draft',runtimeIntegrated=False,visual_reviewed=False)
with Image.open(out) as im:x.update(width=im.width,height=im.height,mode=im.mode)
x['source_sha256']={p:h(root/p) for p in x['sources']}
x['reference_sha256']={p:h(root/p) for p in x.get('references',[])}
x['reference_usage']='Style references viewed by assistant before generation; no source image supplied to generator.'
x['verification_limits']='Pixel-style review only; exact native grid, restricted palette, pivots, collision, runtime and animation consistency unverified. Appearance proposals are not narrative canon.'
manifest=folder/'manifest.json';d=json.loads(manifest.read_text()) if manifest.exists() else {'batch':str(x['batch']),'date':'2026-10-12','generator':'built-in image_gen','assets':[]}
d['assets'].append(x);manifest.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(str(out));print(x['sha256'],x['width'],x['height'])
