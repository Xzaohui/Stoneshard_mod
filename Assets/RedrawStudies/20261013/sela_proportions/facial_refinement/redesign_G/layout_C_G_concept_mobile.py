from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
P=Path(__file__).resolve().parent
C=Image.open(P.parent/'c_reorganized/sela_face_C_native.png').convert('RGBA');G=Image.open(P/'sela_G_raw_imagegen.png').convert('RGBA')
b=Image.new('RGB',(600,760),(180,183,172));d=ImageDraw.Draw(b)
f='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';title=ImageFont.truetype(f,24);label=ImageFont.truetype(f,21);small=ImageFont.truetype(f,15);en=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
def center(text,cx,y,font,color=(28,28,28)):
 box=d.textbbox((0,0),text,font=font);d.text((cx-(box[2]-box[0])/2,y),text,font=font,fill=color)
center('瑟拉 · 表情方向对照',300,22,title)
center('C 旧稿',150,80,label);center('G 新表情设计',450,80,label)
# Full visible figures matched to 238px height, original artwork unchanged.
c=C.crop((8,4,28,38)).resize((140,238),Image.Resampling.NEAREST);g=G.crop((278,127,891,1215)).resize((134,238),Image.Resampling.LANCZOS)
b.paste(c,(80,122),c);b.paste(g,(383,122),g)
center('脸部特写',150,405,small);center('脸部特写',450,405,small)
c=C.crop((7,3,29,23)).resize((220,200),Image.Resampling.NEAREST);g=G.crop((247,96,922,721)).resize((220,204),Image.Resampling.LANCZOS)
b.paste(c,(40,448),c);b.paste(g,(340,448),g)
center('旧像素候选',150,684,small)
center('CONCEPT / NOT IN-GAME',450,681,en)
center('表情设计概念，尚非游戏成品',450,708,small)
b.save(P/'mobile_C_old_G_new_concept.png')
print(P/'mobile_C_old_G_new_concept.png')
