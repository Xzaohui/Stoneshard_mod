from pathlib import Path
from PIL import Image,ImageDraw
D=Path(__file__).resolve().parent;P=D.parent;R=P.parents[3]
figs=[('LIQUI v2',P/'v2/liqui_native_v2.png',16),('LIQUI 1:1',D/'liqui_native_1to1.png',20),('Gunda',R/'Assets/ReferenceAudit/20261013/originals/s_peasantfemale_09_0.png',None),('Bert',R/'Assets/ReferenceAudit/20261013/originals/s_npc_merchant01_0.png',None)]
b=Image.new('RGB',(180,48),'#777777')
for n,(name,p,chin) in enumerate(figs):
 im=Image.open(p).convert('RGBA');b.paste(im,(n*45,0),im)
b.save(D/'same_ground_1x.png')
b=Image.new('RGB',(1280,460),'#777777');d=ImageDraw.Draw(b)
for n,(name,p,chin) in enumerate(figs):
 im=Image.open(p).convert('RGBA').resize((280,352),Image.Resampling.NEAREST);x=n*320+10;y=40;b.paste(im,(x,y),im);d.text((x,10),name,fill='white')
 # Tick lines outside body avoid obscuring facial pixels. Coordinates refer to native row boundaries.
 for row,c,label in [(4,'#98d7ff','top4'),(38,'#dddddd','ground38')]+([(chin+1,'#ffcc66',f'after chin{chin}')] if chin is not None else []):
  yy=y+row*8;d.line((x,yy,x+60,yy),fill=c,width=1);d.line((x+235,yy,x+280,yy),fill=c,width=1);d.text((x+237,yy+1),label,fill=c)
 if chin is not None:d.text((x,400),f'Head rows4..{chin}; remainder{chin+1}..37',fill='white')
d.text((10,435),'Same 8x and foot-bottom y37. Reference chin lines intentionally not asserted; reviewer must inspect actual jaw.',fill='white');b.save(D/'same_ground_8x_landmarks.png')
# Coordinate grid for jaw inspection, only candidate enlarged, no inferred ratio metadata.
im=Image.open(D/'liqui_native_1to1.png').resize((560,704),Image.Resampling.NEAREST);b=Image.new('RGBA',(620,740),'#777777');b.alpha_composite(im,(40,20));d=ImageDraw.Draw(b)
for y in range(4,23):d.text((4,20+y*16),str(y),fill='white');d.line((36,20+y*16,600,20+y*16),fill=(255,255,255,30))
b.convert('RGB').save(D/'jaw_row_inspection_16x.png')
