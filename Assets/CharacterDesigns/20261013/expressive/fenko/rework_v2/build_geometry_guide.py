from pathlib import Path
from PIL import Image
import json,hashlib
p=Path(__file__).resolve().parent;s=p.parent/'fenko_raw_imagegen.png'; im=Image.open(s)
segments=[(0,500,500,'head/face unchanged'),(500,660,60,'shorten exposed neck and upper chest'),(660,960,260,'modest torso compression; guide hand sample geometry only'),(960,1280,230,'shorten long apron/skirt'),(1280,1407,127,'feet unchanged')]
out=Image.new('RGBA',(im.width,sum(z[2] for z in segments)));y=0
for a,b,h,reason in segments:
 crop=im.crop((0,a,im.width,b));out.paste(crop.resize((im.width,h),Image.Resampling.NEAREST),(0,y));y+=h
f=p/'fenko_GEOMETRY_GUIDE_NOT_DELIVERABLE.png';out.save(f)
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
(p/'geometry_guide.json').write_text(json.dumps({'status':'GEOMETRY_GUIDE_NOT_DELIVERABLE','source':str(s),'source_sha256':sha(s),'guide_sha256':sha(f),'canvas':list(out.size),'segments':[{'source_y':[a,b],'target_height':h,'reason':why} for a,b,h,why in segments],'notes':'Nearest-neighbor segment geometry only. Not final sprite. Must be redrawn by built-in image_gen, especially hands, cloth and neckline.'},ensure_ascii=False,indent=2)+'\n')
print(f)
