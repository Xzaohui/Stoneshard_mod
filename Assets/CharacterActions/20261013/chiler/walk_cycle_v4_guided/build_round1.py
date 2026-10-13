from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,json
p=Path('Stoneshard_mod/Assets/CharacterActions/20261013/chiler/walk_cycle_v4_guided'); im=Image.open(p/'originals/K1_round1_raw.png').convert('RGBA').resize((1536,1536),Image.Resampling.NEAREST)
m=Image.new('L',im.size);ImageDraw.Draw(m).polygon([(665,1140),(915,1140),(960,1190),(1080,1450),(1080,1535),(590,1535),(590,1220)],fill=255)
lo=Image.new('RGBA',im.size);lo.paste(im,(0,0),m);s=Image.new('RGBA',im.size);s.alpha_composite(lo,(0,-89))
u=Image.open(p.parent/'walk_cycle_v2/layers/identity_upper_master.png');up=Image.new('RGBA',im.size);up.alpha_composite(u,(0,-20));out=Image.alpha_composite(s,up)
for img,name in [(s,'layers/K1_round1_lower.png'),(up,'layers/K1_upper.png'),(out,'frames/K1_round1.png')]:
 a=np.array(img);a[a[:,:,3]==0]=0;Image.fromarray(a).save(p/name)
m.save(p/'masks/K1_round1_extract.png');sheet=Image.new('RGB',(1536,820),(35,39,43));d=ImageDraw.Draw(sheet);ft='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(ft,24)
for i,(path,lab) in enumerate([(p.parent/'idle_v1/frames/I0_still.png','原始裤靴'),(p.parent/'walk_cycle_v3_rig/frames/K1.png','仅姿势约束：未通过'),(p/'frames/K1_round1.png','局部重绘第1轮：待审')]):
 x=Image.open(path).convert('RGBA');r=x.resize((512,512),Image.Resampling.NEAREST);sheet.paste(r,(i*512,40),r);crop=x.crop((480,1050,1120,1450)).resize((512,320),Image.Resampling.NEAREST);sheet.paste(crop,(i*512,500),crop);d.text((i*512+20,10),lab,font=f,fill='white')
sheet.save(p/'K1_round1_comparison.png');(p/'K1_round1_registration.json').write_text(json.dumps({'canvas':[1536,1536],'lower_translation':[0,-89],'upper_bob':[0,-20],'sole_y':1380,'status':'research pending QA; pose deviates from guide, far foot remains rearward','complete_cycle':False},indent=2))
