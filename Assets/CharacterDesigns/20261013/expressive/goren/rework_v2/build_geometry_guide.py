from pathlib import Path
from PIL import Image
import hashlib,json
p=Path(__file__).parent;s=p.parent/'goren_raw_imagegen.png';im=Image.open(s).convert('RGBA');segments=[(0,435,479,1.1),(435,580,65,1.0),(580,810,170,1.0),(810,1210,230,1.0),(1210,im.height,180,1.0)];out=Image.new('RGBA',(im.width,sum(a[2] for a in segments)),(0,0,0,0));y=0;record=[]
for a,b,h,sx in segments:
 w=round(im.width*sx);strip=im.crop((0,a,im.width,b)).resize((w,h),Image.Resampling.NEAREST);x=(im.width-w)//2;out.paste(strip,(x,y));record.append({'source_y':[a,b],'guide_y':[y,y+h],'x_offset':x,'x_scale':sx});y+=h
out.save(p/'goren_GEOMETRY_GUIDE_NOT_DELIVERABLE.png');(p/'geometry_transform.json').write_text(json.dumps({'status':'GEOMETRY_GUIDE_NOT_DELIVERABLE','source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'segments':record,'preserve':'Uniform head enlargement approximately 10 percent; shorten neck/chest/waist/legs. Keep adult stocky build, amulet and full boots.','limitations':'Guide has segment seams/nonsquare body pixels, must imagegen redraw.'},ensure_ascii=False,indent=2)+'\n')
