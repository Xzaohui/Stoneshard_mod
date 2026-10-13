from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent;s=p.parent/'sailuo_raw_imagegen.png';im=Image.open(s).convert('RGBA')
segments=[(0,325,325),(325,455,65),(455,870,290),(870,1225,245),(1225,1407,182)]
out=Image.new('RGBA',(im.width,sum(q[2] for q in segments)),(0,0,0,0));y=0;record=[]
for a,b,h in segments:
 strip=im.crop((0,a,im.width,b)).resize((im.width,h),Image.Resampling.NEAREST);out.paste(strip,(0,y));record.append({'source_y':[a,b],'guide_y':[y,y+h]});y+=h
out.save(p/'sailuo_GEOMETRY_GUIDE_NOT_DELIVERABLE.png')
(p/'geometry_transform.json').write_text(json.dumps({'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'segments':record,'preserve':'Adult broad shoulders and calm autonomous expression, dark hair green tunic, empty hands, full boots.','limitations':'GEOMETRY GUIDE ONLY. Nearest segmented compression is not deliverable; imagegen must redraw seams, hands, tool and pixels.'},indent=2))
