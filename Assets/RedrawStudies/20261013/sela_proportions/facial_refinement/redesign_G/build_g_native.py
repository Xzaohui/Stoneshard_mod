from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent
raw=Image.open(P/'sela_G_raw_imagegen.png').convert('RGBA');sample=raw.resize((35,44),Image.Resampling.NEAREST);sample.save(P/'sela_G_full_sample_native.png')
a=np.array(sample);base=np.array(Image.open(P.parent/'before_native.png').convert('RGBA'));c=np.array(Image.open(P.parent/'c_reorganized/sela_face_C_native.png').convert('RGBA'))
pal=np.array([(32,27,26),(53,39,31),(73,48,40),(102,67,51),(129,86,56),(179,102,65),(219,148,97),(239,187,130)],dtype=np.int32)
# Native-grid sampling and palette cleanup only, no hand-authored face features.
b=base.copy()
for y in range(4,21):
 for x in range(35):
  if a[y,x,3]<128:b[y,x]=[0,0,0,0]
  else:
   rgb=a[y,x,:3].astype(np.int32);best=np.argmin(np.sum((pal-rgb)**2,axis=1));b[y,x]=[*pal[best],255]
im=Image.fromarray(b);im.save(P/'sela_G_head_composite_native.png');im.resize((280,352),Image.Resampling.NEAREST).save(P/'sela_G_head_composite_8x.png')
board=Image.new('RGB',(600,600),(180,183,172));d=ImageDraw.Draw(board);font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18)
for i,(name,sprite) in enumerate([('C',Image.fromarray(c)),('G - generated head',im)]):
 x=i*300;d.text((x+30,20),name,font=font,fill=(28,28,28));sp=sprite.resize((210,264),Image.Resampling.NEAREST);board.paste(sp,(x+45,55),sp);sp=sprite.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST);board.paste(sp,(x+40,370),sp)
board.save(P/'comparison_C_G_mobile.png')
qa={'body_y21_and_below_equal':bool(np.array_equal(base[21:],b[21:])),'visible_y':[int(np.where(b[:,:,3]>0)[0].min()),int(np.where(b[:,:,3]>0)[0].max())],'head_span':17,'body_span':17,'head_outer_shape_identical':bool(np.array_equal(base[:21,:,3],b[:21,:,3])),'new_colors':list(set(map(tuple,b.reshape(-1,4)))-set(map(tuple,base.reshape(-1,4)))),'sha256':hashlib.sha256((P/'sela_G_head_composite_native.png').read_bytes()).hexdigest()};(P/'QA-G.json').write_text(json.dumps(qa,indent=2)+'\n');print(qa)
