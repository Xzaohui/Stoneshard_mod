from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent
source=p.parent/'vere_v2_raw_imagegen.png'
im=Image.open(source).convert('RGBA')
# Head untouched. Neck/upper torso slightly shortened, skirt substantially shortened.
segments=[(0,480,480),(480,600,70),(600,880,240),(880,1270,210),(1270,im.height,im.height-1270)]
out=Image.new('RGBA',(im.width,sum(v[2] for v in segments)),(0,0,0,0));dest_y=0
record=[]
for y0,y1,new_h in segments:
 strip=im.crop((0,y0,im.width,y1));strip=strip.resize((im.width,new_h),Image.Resampling.NEAREST);out.paste(strip,(0,dest_y));record.append({'source_y':[y0,y1],'guide_y':[dest_y,dest_y+new_h]});dest_y+=new_h
out.save(p/'vere_GEOMETRY_GUIDE_NOT_DELIVERABLE.png')
info={'status':'GEOMETRY_GUIDE_NOT_DELIVERABLE','purpose':'Authorized pixel-script outline optimization, input only for built-in redraw, not a final asset.','source_file':str(source),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'segments':record,'warning':'Nearest-neighbor segmented shortening can distort hand/cloth pixels and introduce seams. Built-in imagegen must redraw clean clusters and anatomy.'}
(p/'geometry_transform.json').write_text(json.dumps(info,ensure_ascii=False,indent=2)+'\n')
