from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent;s=p.parent/'ousha_raw_imagegen.png';im=Image.open(s).convert('RGBA');segments=[(0,395,395),(395,530,55),(530,925,270),(925,1140,145),(1140,im.height,190)];out=Image.new('RGBA',(im.width,sum(a[2] for a in segments)),(0,0,0,0));y=0;record=[]
for a,b,h in segments:
 strip=im.crop((0,a,im.width,b)).resize((im.width,h),Image.Resampling.NEAREST);out.paste(strip,(0,y));record.append({'source_y':[a,b],'guide_y':[y,y+h]});y+=h
out.save(p/'ousha_GEOMETRY_GUIDE_NOT_DELIVERABLE.png');(p/'geometry_transform.json').write_text(json.dumps({'status':'GEOMETRY_GUIDE_NOT_DELIVERABLE','source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'segments':record,'preserve':'Head and face untouched. Shorten exposed neck, chest/waist and skirt column.','limitations':'Segment seams and nonsquare pixels require imagegen redraw.'},ensure_ascii=False,indent=2)+'\n')
