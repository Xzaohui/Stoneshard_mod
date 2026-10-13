"""Chinese presentation layout only; preserves both prior 0.5x image panels pixel for pixel."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
D=Path(__file__).resolve().parent
src=Image.open(D/'tor_old_new_same_scale.png').convert('RGB')
out=Image.new('RGB',(1178,930),(231,228,219));dr=ImageDraw.Draw(out)
f='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
b='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
font=lambda n,bold=False:ImageFont.truetype(b if bold else f,n,index=2)
dr.text((40,23),'托雷 · 衣装修订',font=font(36,True),fill=(44,36,30))
dr.text((40,78),'简化翻领与内衫，保留脸型、比例和随身物品',font=font(25),fill=(78,65,53))
for x,t in [(20,'旧稿'),(599,'中世纪衣装修订')]:
    dr.text((x+20,135),t,font=font(29,True),fill=(59,45,34))
    out.paste(src.crop((x,50,x+559,754)),(x,185))
out.save(D/'tor_old_new_same_scale_zh.png')
