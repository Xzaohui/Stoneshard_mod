from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent;s=p.parent/'ali_raw_imagegen.png';im=Image.open(s).convert('RGBA')
segments=[(0,405,405),(405,485,38),(485,710,180),(710,1280,340),(1280,1407,127)]
out=Image.new('RGBA',(im.width,sum(q[2] for q in segments)),(0,0,0,0));y=0;record=[]
for a,b,h in segments:
 strip=im.crop((0,a,im.width,b)).resize((im.width,h),Image.Resampling.NEAREST);out.paste(strip,(0,y));record.append({'source_y':[a,b],'guide_y':[y,y+h]});y+=h
out.save(p/'ali_GEOMETRY_GUIDE_NOT_DELIVERABLE.png')
(p/'geometry_transform.json').write_text(json.dumps({'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'segments':record,'preserve':'Original face and expression, high red-bound knot, ochre tunic leather apron, lowered blunt tool, full feet.','limitations':'GEOMETRY GUIDE ONLY. Nearest segmented compression is not deliverable; imagegen must redraw seams, hands, tool and pixels.'},indent=2))
