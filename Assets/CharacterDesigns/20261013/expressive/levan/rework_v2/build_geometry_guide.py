from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent;s=p.parent/'levan_raw_imagegen.png';im=Image.open(s).convert('RGBA')
segments=[(0,360,360),(360,510,70),(510,920,300),(920,1220,225),(1220,1407,187)]
out=Image.new('RGBA',(im.width,sum(q[2] for q in segments)),(0,0,0,0));y=0;record=[]
for a,b,h in segments:
 strip=im.crop((0,a,im.width,b)).resize((im.width,h),Image.Resampling.NEAREST);out.paste(strip,(0,y));record.append({'source_y':[a,b],'guide_y':[y,y+h]});y+=h
out.save(p/'levan_GEOMETRY_GUIDE_NOT_DELIVERABLE.png')
(p/'geometry_transform.json').write_text(json.dumps({'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'segments':record,'preserve':'Adult shoulders, homesick subdued face, dark wavy hair rust tunic patched brown trousers empty hands boots.','limitations':'GEOMETRY GUIDE ONLY. Nearest segmented compression is not deliverable; imagegen must redraw seams, hands, tool and pixels.'},indent=2))
