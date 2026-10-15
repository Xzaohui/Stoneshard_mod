from pathlib import Path
from PIL import Image
import json,base64,hashlib,re,sys,numpy as np
root=Path(__file__).resolve().parents[7]
slug,key,version=sys.argv[1:]
d=root/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1'
p=d/'raw'/f'{key}_{version}_tool_return.json';j=json.loads(p.read_text());data=base64.b64decode(j['image_url'].split(',',1)[1]);raw=d/'raw'/f'{key}_{version}_raw.png'
if raw.exists():assert raw.read_bytes()==data
else:raw.write_bytes(data)
orig=Path(re.search(r'as (/[^\n]+\.png) by',j['output_hint']).group(1));assert orig.read_bytes()==data
im=Image.open(raw).convert('RGBA');a=np.asarray(im).copy();old=a.copy();a[a[:,:,3]<=8]=0;a[a[:,:,3]==0,:3]=0;clean=Image.fromarray(a)
cand=d/'review'/f'{key}_{version}_transparent.png';clean.save(cand)
for kind,bg in [('light',(242,236,220,255)),('dark',(31,36,44,255))]:
 base=Image.new('RGBA',im.size,bg);base.alpha_composite(clean);base.convert('RGB').save(d/'review'/f'{key}_{version}_{kind}.png')
assert np.array_equal(a[old[:,:,3]>8],old[old[:,:,3]>8])
rec={'key':key,'version':version,'raw':str(raw.relative_to(root)),'raw_sha256':hashlib.sha256(data).hexdigest(),'tool_return_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'tool_payload_matches_raw':True,'tool_saved_original_matches_raw':True,'raw_size':im.size,'raw_alpha_minmax':[int(old[:,:,3].min()),int(old[:,:,3].max())],'alpha_le8_cleared_pixels':int(np.sum((old[:,:,3]>0)&(old[:,:,3]<=8))),'hidden_rgb_cleared_pixels':int(np.sum((old[:,:,3]==0)&np.any(old[:,:,:3]!=0,axis=2))),'visible_pixels_gt8_unchanged':True,'transparent_candidate':str(cand.relative_to(root)),'transparent_sha256':hashlib.sha256(cand.read_bytes()).hexdigest(),'alpha_bbox':clean.getbbox(),'nontransparent_edge_pixels':int((a[0,:,3]>0).sum()+(a[-1,:,3]>0).sum()+(a[:,0,3]>0).sum()+(a[:,-1,3]>0).sum()),'postprocess':'Only alpha <=8 and hidden RGB cleanup. No resize, crop, draw, anatomy edits, quantization, or recoloring. True RGBA composites.'}
(d/'review'/f'{key}_{version}_technical_QA.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rec,ensure_ascii=False))
