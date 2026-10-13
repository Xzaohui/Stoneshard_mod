from pathlib import Path
from PIL import Image
import json,hashlib
p=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive/elon/rework_v2');s=p.parent/'elon_raw_imagegen.png'; im=Image.open(s)
segments=[(0,365,365,'preserve independent mature head'),(365,610,140,'shorter neck upper chest'),(610,1020,245,'compact torso waist'),(1020,1340,185,'compact legs'),(1340,1536,196,'preserve boots') ]
out=Image.new('RGBA',(im.width,sum(z[2] for z in segments)));y=0
for a,b,h,reason in segments:
 crop=im.crop((0,a,im.width,b));out.paste(crop.resize((im.width,h),Image.Resampling.NEAREST),(0,y));y+=h
f=p/'elon_GEOMETRY_GUIDE_NOT_DELIVERABLE.png';out.save(f)
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
(p/'geometry_guide.json').write_text(json.dumps({'status':'GEOMETRY_GUIDE_NOT_DELIVERABLE','source':str(s),'source_sha256':sha(s),'guide_sha256':sha(f),'canvas':list(out.size),'segments':[{'source_y':[a,b],'target_height':h,'reason':why} for a,b,h,why in segments],'notes':'Nearest-neighbor segment geometry only. Not final sprite. Must be redrawn by built-in image_gen, especially hands, cloth and neckline.'},ensure_ascii=False,indent=2)+'\n')
print(f)
