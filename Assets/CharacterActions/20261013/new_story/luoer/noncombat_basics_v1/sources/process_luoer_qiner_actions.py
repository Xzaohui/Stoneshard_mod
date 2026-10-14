from pathlib import Path
from PIL import Image
import sys,json,hashlib,shutil,re,base64,numpy as np
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');slug,key=sys.argv[1:3];p=r/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1'
ret=json.loads((p/'raw'/f'{key}_tool_return.json').read_text());m=re.search(r'as (/[^\n]+\.png) by default',ret.get('output_hint',''));raw=p/'raw'/f'{key}_raw.png';assert not raw.exists()
if m:shutil.copy2(m[1],raw)
else:raw.write_bytes(base64.b64decode(ret['image_url'].split(',',1)[1]))
if 'image_url' in ret and ret['image_url'].startswith('data:'):assert hashlib.sha256(raw.read_bytes()).digest()==hashlib.sha256(base64.b64decode(ret['image_url'].split(',',1)[1])).digest()
a=np.array(Image.open(raw).convert('RGBA'));original=a.copy(); count=int(((a[:,:,3]>0)&(a[:,:,3]<=8)).sum());a[a[:,:,3]<=8]=0
out=Image.fromarray(a);out.save(p/'exports'/f'{key}_transparent.png')
for name,color in [('light',(242,236,223,255)),('dark',(29,34,39,255))]:
 im=Image.new('RGBA',out.size,color);im.alpha_composite(out);im.convert('RGB').save(p/'review'/f'{key}_{name}.png')
files=[raw,p/'raw'/f'{key}_tool_return.json',p/'exports'/f'{key}_transparent.png',p/'prompts'/f'{key}.txt',p/'prompts'/f'{key}_parameters.json']+[p/'review'/f'{key}_{name}.png' for name in ['light','dark']]
rep={'key':key,'raw_mode':Image.open(raw).mode,'size':list(out.size),'cleanup_alpha_max':8,'near_zero_alpha_cleaned':count,'pixels_alpha_above_8_unchanged':bool(np.array_equal(a[original[:,:,3]>8],original[original[:,:,3]>8])),'alpha_bbox':out.getbbox(),'corners_alpha':[int(a[y,x,3]) for x,y in [(0,0),(out.width-1,0),(0,out.height-1),(out.width-1,out.height-1)]],'generator':'builtin imagegen','full_return_including_payload_preserved':True,'raw_equals_decoded_payload':True,'independent_review':'pending','files':{str(f.relative_to(p)):{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in files}}
(p/'raw'/f'{key}_provenance.json').write_text(json.dumps(rep,ensure_ascii=False,indent=2)+'\n');print(json.dumps(rep,ensure_ascii=False))
