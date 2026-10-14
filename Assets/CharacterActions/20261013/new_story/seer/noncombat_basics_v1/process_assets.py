from pathlib import Path
import json,hashlib,base64,re,sys,datetime
from PIL import Image
import numpy as np
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
slug,key,version=sys.argv[1:4]
d=R/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1'
s=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=d/'raw'/f'{key}_{version}_tool_return.json';r=json.loads(f.read_text());url=r.get('image_url','')
if not url.startswith('data:image/'):
 print('NO_IMAGE',str(r)[:2000]);sys.exit(2)
raw=d/'raw'/f'{key}_{version}_raw_imagegen.png';raw.write_bytes(base64.b64decode(url.split(',',1)[1]));im=Image.open(raw).convert('RGBA');a=np.array(im);before=a.copy();m=a[:,:,3]<=8;a[m]=0
out=d/'review'/f'{key}_{version}_transparent.png';Image.fromarray(a).save(out)
comps=[]
for mode,col in [('light',(238,232,217)),('dark',(37,40,45))]:
 bg=Image.new('RGBA',im.size,col+(255,));bg.alpha_composite(Image.fromarray(a));p=d/'review'/f'{key}_{version}_{mode}_inspect.png';bg.convert('RGB').save(p);comps.append(str(p.relative_to(d)))
q={'key':key,'version':version,'status':'candidate_pending_independent_review','imagegen_native_size':list(im.size),'raw_sha256':s(raw),'transparent_sha256':s(out),'full_tool_return_sha256':s(f),'parameters_sha256':s(d/'prompts'/f'{key}_{version}_parameters.json'),'prompt_sha256':s(d/'prompts'/f'{key}_{version}.txt'),'raw_path':str(raw.relative_to(d)),'transparent_path':str(out.relative_to(d)),'composite_paths':comps,'alpha_zero_before':int((before[:,:,3]==0).sum()),'alpha_1_to_8_before':int(((before[:,:,3]>0)&(before[:,:,3]<=8)).sum()),'hidden_rgb_before':int(((before[:,:,3]==0)&(before[:,:,:3]!=0).any(2)).sum()),'alpha_zero_after':int((a[:,:,3]==0).sum()),'visible_pixels_unchanged':bool(np.array_equal(a[before[:,:,3]>8],before[before[:,:,3]>8])),'only_allowed_alpha_cleanup':True,'actual_native_raw_and_transparent_views_pending':True,'geometry_transform':'none','runtime_verified':False}
(d/'qa'/f'{key}_{version}_technical.json').write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(q,ensure_ascii=False,indent=2))
