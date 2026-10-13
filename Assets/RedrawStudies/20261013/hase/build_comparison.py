from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,numpy as np,hashlib
p=Path(__file__).parent;r=p.parents[2]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',11)
refs=[('Hase new','hase_native_v1.png'),('Bert','s_npc_merchant01_0.png'),('Jurg','s_npc_carpenter_0.png'),('Frid','s_npc_herbalist_0.png')]
sheet=Image.new('RGB',(1260,760),'#777778');d=ImageDraw.Draw(sheet)
d.text((20,12),'HASE | near 1:1 head/body study | original references are comparison only',font=font,fill='white')
for i,(name,f) in enumerate(refs):
 im=Image.open(p/f if i==0 else r/'ReferenceAudit/20261013/originals'/f).convert('RGBA');x=15+i*310;y=80
 sheet.paste(im.resize((280,352),Image.Resampling.NEAREST),(x,y),im.resize((280,352),Image.Resampling.NEAREST));d.text((x,50),name+' | native 35 x 44, 8x NN',font=small,fill='white')
 for yy,col in [(4,'#bce6f5'),(20,'#ffc660'),(37,'#bce6f5')]:d.line((x,y+yy*8,x+280,y+yy*8),fill=col,width=1)
 if i==0:
  d.line((x,y+19*8,x+280,y+19*8),fill='#f5db9a');d.line((x,y+23*8,x+280,y+23*8),fill='#d787dd');
  d.text((x,440),'Crown 4; inferred chin 19-20;',font=small,fill='white');d.text((x,457),'beard ends 22; soles 37.',font=small,fill='white');d.text((x,474),'Head 16-17 / rest 18-17.',font=small,fill='white')
 else:d.text((x,440),'Lines at Hase rows 4/20/37 for comparison.',font=small,fill='white')
old=r.parent/'src/EmbersAndOaths/Assets/ConceptDrafts/20261012/batch34/130_bry_taori_hase_cast.png'
im=Image.open(old).crop((260,522,570,1170));im.thumbnail((110,230),Image.Resampling.LANCZOS);sheet.paste(im,(20,515));d.text((140,520),'Old Hase only: enlarged illustration concept.',font=font,fill='white');d.text((140,548),'Long neck, coat/waistcoat layers, long legs.',font=font,fill='white');d.text((140,576),'New: large cranium; jaw estimated under beard.',font=font,fill='white');d.text((140,604),'Not an engine standard, direction set, or runtime pass.',font=font,fill='white')
d.text((140,634),'Warm skin, olive cloth, brown satchel, one capped bottle.',font=font,fill='white');d.text((140,662),'Commercial agent only; no treatment, efficacy or sale outcome.',font=font,fill='white')
sheet.save(p/'hase_old_native_originals_comparison.png')
# Native 20x annotation, every coordinate available for inspection.
im=Image.open(p/'hase_native_v1.png'); ann=Image.new('RGB',(860,960),'#777778');ann.paste(im.resize((700,880),Image.Resampling.NEAREST),(55,40),im.resize((700,880),Image.Resampling.NEAREST));d=ImageDraw.Draw(ann)
for y in range(44):d.text((10,40+y*20),str(y),font=small,fill='white')
for x in range(35):d.text((55+x*20,18),str(x),font=small,fill='white')
for y,label,col in [(4,'crown','#bce6f5'),(19,'chin lo','#ffcc66'),(21,'chin hi +1','#ffcc66'),(23,'beard end+1','#d787dd'),(38,'sole+1','#bce6f5')]:d.line((50,40+y*20,760,40+y*20),fill=col);d.text((765,40+y*20),label,font=small,fill=col)
ann.save(p/'hase_native_landmarks_20x.png')
print(p/'hase_old_native_originals_comparison.png')
