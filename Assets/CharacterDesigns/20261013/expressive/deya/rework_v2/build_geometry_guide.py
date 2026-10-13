from pathlib import Path
from PIL import Image
import json,hashlib
p=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive/deya/rework_v2');s=p.parent/'deya_raw_imagegen.png'; im=Image.open(s)
segments=[(0,330,330,'head and face unchanged'),(330,470,65,'shorten neck and upper chest'),(470,760,185,'compact torso and waist'),(760,1370,300,'compact skirt'),(1370,1536,166,'preserve feet') ]
out=Image.new('RGBA',(im.width,sum(z[2] for z in segments)));y=0
for a,b,h,reason in segments:
 crop=im.crop((0,a,im.width,b));out.paste(crop.resize((im.width,h),Image.Resampling.NEAREST),(0,y));y+=h
f=p/'deya_GEOMETRY_GUIDE_NOT_DELIVERABLE.png';out.save(f)
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
(p/'geometry_guide.json').write_text(json.dumps({'status':'GEOMETRY_GUIDE_NOT_DELIVERABLE','source':str(s),'source_sha256':sha(s),'guide_sha256':sha(f),'canvas':list(out.size),'segments':[{'source_y':[a,b],'target_height':h,'reason':why} for a,b,h,why in segments],'notes':'Nearest-neighbor segment geometry only. Not final sprite. Must be redrawn by built-in image_gen, especially hands, cloth and neckline.'},ensure_ascii=False,indent=2)+'\n')
print(f)
