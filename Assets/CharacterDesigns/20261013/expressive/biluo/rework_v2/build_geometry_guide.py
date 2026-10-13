from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent;s=p.parent/'biluo_raw_imagegen.png';im=Image.open(s).convert('RGBA')
segments=[(0,435,435),(435,535,48),(535,740,170),(740,1225,330),(1225,1407,182)]
out=Image.new('RGBA',(im.width,sum(q[2] for q in segments)),(0,0,0,0));y=0;record=[]
for a,b,h in segments:
 strip=im.crop((0,a,im.width,b)).resize((im.width,h),Image.Resampling.NEAREST);out.paste(strip,(0,y));record.append({'source_y':[a,b],'guide_y':[y,y+h]});y+=h
out.save(p/'biluo_GEOMETRY_GUIDE_NOT_DELIVERABLE.png')
(p/'geometry_transform.json').write_text(json.dumps({'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'segments':record,'preserve':'Mature hesitant female, wine dress grey shawl, empty hands full shoes. Face independently redrawn.','limitations':'GEOMETRY GUIDE ONLY. Nearest segmented compression is not deliverable; imagegen must redraw seams, hands, tool and pixels.'},indent=2))
