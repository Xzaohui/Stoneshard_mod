from pathlib import Path
from PIL import Image
import json,base64,hashlib,sys
import numpy as np
d=Path(sys.argv[1]); key=sys.argv[2]
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
ret=d/'raw'/f'{key}_tool_return.json'
r=json.loads(ret.read_text()); raw=d/'raw'/f'{key}_raw.png'
payload=base64.b64decode(r['image_url'].split(',',1)[1]); raw.write_bytes(payload)
im=Image.open(raw).convert('RGBA'); a=np.array(im); orig=a.copy()
mask=a[:,:,3]<=8; cleaned_nonzero=int(((a[:,:,3]>0)&mask).sum()); a[mask]=0
out=d/'exports'/f'{key}_transparent.png';Image.fromarray(a).save(out)
for name,color in [('light',(237,233,221,255)),('dark',(31,38,45,255))]:
 bg=Image.new('RGBA',im.size,color);bg.alpha_composite(Image.fromarray(a));bg.convert('RGB').save(d/'review'/f'{key}_{name}.png')
alpha=a[:,:,3]; bbox=Image.fromarray(alpha).getbbox()
params=d/'prompts'/f'{key}_parameters.json'; p=json.loads(params.read_text())
prompt=d/'prompts'/f'{key}.txt'; assert p['prompt']==prompt.read_text()
refs=[{'path':rp,'sha256':h(Path(rp))} for rp in p['referenced_image_paths']]
audit={'key':key,'raw_mode':im.mode,'size':list(im.size),'alpha_cleanup_threshold':8,'alpha_only_pixels_cleared':cleaned_nonzero,'hidden_rgb_cleanup_allowed':True,'nontransparent_body_pixels_modified':bool(np.any(orig[orig[:,:,3]>8]!=a[orig[:,:,3]>8])),'bbox':bbox,'full_canvas_retained':True,'image_payload_decoded_matches_raw':hashlib.sha256(payload).hexdigest()==h(raw),'actual_parameters_equal_saved_prompt':True,'reference_inputs':refs,'source_brief_sha256':h(d/'sources/fifth_new_character_actions_brief.json'),'transparency':{'zero_alpha_pixels':int((alpha==0).sum()),'opaque_pixels':int((alpha==255).sum()),'intermediate_alpha_pixels':int(((alpha>0)&(alpha<255)).sum()),'border_alpha_max':int(max(alpha[0,:].max(),alpha[-1,:].max(),alpha[:,0].max(),alpha[:,-1].max()))},'files':{str(pth.relative_to(d)):{'sha256':h(pth),'bytes':pth.stat().st_size} for pth in [raw,ret,out,prompt,params,d/'review'/f'{key}_light.png',d/'review'/f'{key}_dark.png']}}
(d/'raw'/f'{key}_provenance.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print(json.dumps(audit,ensure_ascii=False))
