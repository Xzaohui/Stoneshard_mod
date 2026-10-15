from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ft=ImageFont.truetype(font,38);fs=ImageFont.truetype(font,26);fm=ImageFont.truetype(font,23)
board=Image.new('RGB',(2400,1340),(236,232,221));d=ImageDraw.Draw(board)
d.text((55,28),'新增剧情人物｜第二批四人',font=ft,fill=(40,43,40))
d.text((55,85),'枯恩 · 苏奈 · 缇安 · 蕾因     独立人物外观概念',font=fs,fill=(65,65,58))
items=[('kuen','枯恩','ASH-NPC-KUEN','清醒表达需要的成年患者'),('sune','苏奈','ASH-NPC-SUNE','先问许可的观察记录员'),('tian','缇安','ASH-NPC-TIAN','守住共住边界的成年姐姐'),('lein','蕾因','HIG-NPC-LEIN','仍须核实通行条件的向导')]
for i,(slug,name,cid,role) in enumerate(items):
 x=i*600
 d.text((x+45,145),name+'  '+cid,font=fs,fill=(40,43,40));d.text((x+45,195),role,font=fm,fill=(65,65,58))
 im=Image.open(BASE/slug/'concept_v1'/f'{slug}_transparent.png').convert('RGBA')
 # Display layout only: trim empty transparent margins; preserve all character pixels and aspect ratio. Raw/transparent files remain untouched.
 im=im.crop(im.getbbox())
 im.thumbnail((530,980),Image.Resampling.NEAREST)
 board.paste(im,(x+(600-im.width)//2,250+(980-im.height)),im)
d.text((55,1285),'各栏独立等比展示，不代表相对身高；仅外观概念，不表示剧情结算、装备兼容或游戏运行通过。',font=fs,fill=(40,43,40))
board.save(OUT/'第二批四人_中文概览.png')
