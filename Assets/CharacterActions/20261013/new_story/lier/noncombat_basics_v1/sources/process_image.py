import json,base64,hashlib,sys,datetime
from pathlib import Path
import numpy as np
from PIL import Image

d=Path(sys.argv[1]); stem=sys.argv[2]
ret=d/'raw'/f'{stem}_tool_return.json'; r=json.loads(ret.read_text())
assert r['image_url'].startswith('data:image/png;base64,')
raw=d/'raw'/f'{stem}_raw.png'; raw.write_bytes(base64.b64decode(r['image_url'].split(',',1)[1]))
im=Image.open(raw).convert('RGBA'); a=np.array(im); clean=a.copy(); clean[clean[:,:,3]<=8]=0
out=d/'exports'/f'{stem}_transparent.png'; Image.fromarray(clean).save(out)
audit={'stem':stem,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'raw_size':list(im.size),'raw_mode':im.mode,'raw_sha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'transparent_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'tool_return_sha256':hashlib.sha256(ret.read_bytes()).hexdigest(),'tool_return_full_image_payload_retained':True,'payload_decoded_bytes_match_raw':True,'alpha_zero_pixels':int(np.sum(a[:,:,3]==0)),'alpha_1_to_8_pixels':int(np.sum((a[:,:,3]>0)&(a[:,:,3]<=8))),'alpha_9_to_254_pixels':int(np.sum((a[:,:,3]>8)&(a[:,:,3]<255))),'hidden_rgb_pixels':int(np.sum((a[:,:,3]==0)&np.any(a[:,:,:3]!=0,axis=2))),'foreground_alpha_gt8_bytes_unchanged':bool(np.array_equal(clean[a[:,:,3]>8],a[a[:,:,3]>8])),'processing':'Set RGBA to zero only where alpha<=8; no crop, resize, recolor, drawing or body edits. Hidden RGB is not a hard visual error.','bbox':Image.fromarray(clean).getbbox(),'boards':[]}
for name,bg in [('light',(239,234,221,255)),('dark',(33,37,41,255))]:
 board=Image.new('RGBA',im.size,bg);board.alpha_composite(Image.fromarray(clean));p=d/'review'/f'{stem}_{name}.png';board.convert('RGB').save(p);audit['boards'].append({'path':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(d/'review'/f'{stem}_byte_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
params=json.loads((d/'prompts'/f'{stem}_parameters.json').read_text()); provenance={'tool':'builtin image_gen.imagegen','parameters_path':f'prompts/{stem}_parameters.json','prompt_path':f'prompts/{stem}.txt','prompt_sha256':hashlib.sha256(params['prompt'].encode()).hexdigest(),'reference_source_sha256':[{ 'path':p,'sha256':hashlib.sha256(Path(p).read_bytes()).hexdigest()} for p in params['referenced_image_paths']],'raw_sha256':audit['raw_sha256'],'transparent_sha256':audit['transparent_sha256'],'tool_payload_retained':True,'output_hint':r.get('output_hint'),'transparent_background_requested':params['transparent_background']}
(d/'raw'/f'{stem}_provenance.json').write_text(json.dumps(provenance,ensure_ascii=False,indent=2))
print(json.dumps(audit,ensure_ascii=False))
