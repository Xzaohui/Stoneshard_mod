from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ft=ImageFont.truetype(font,38);fs=ImageFont.truetype(font,26);fm=ImageFont.truetype(font,23)
board=Image.new('RGB',(2400,1340),(236,232,221));d=ImageDraw.Draw(board)
d.text((55,28),'新增剧情人物｜首批四人',font=ft,fill=(40,43,40))
d.text((55,85),'安妮 · 古菈 · 德茹 · 霍珥     独立人物外观概念',font=fs,fill=(65,65,58))
items=[('anni','安妮','ASH-NPC-ANNI','限定当班普通护理者'),('gura','古菈','HIG-NPC-GURA','只签本次外段的维护工'),('deru','德茹','FX-QRY','五十岁上下的石场看守'),('hoer','霍珥','FX-MIL','三十来岁的水磨坊守磨人')]
for i,(slug,name,cid,role) in enumerate(items):
 x=i*600
 d.text((x+45,145),name+'  '+cid,font=fs,fill=(40,43,40));d.text((x+45,195),role,font=fm,fill=(65,65,58))
 im=Image.open(BASE/slug/'concept_v1'/f'{slug}_transparent.png').convert('RGBA')
 # Display layout only: trim empty transparent margins; preserve all character pixels and aspect ratio. Raw/transparent files remain untouched.
 im=im.crop(im.getbbox())
 im.thumbnail((530,980),Image.Resampling.NEAREST)
 board.paste(im,(x+(600-im.width)//2,250+(980-im.height)),im)
d.text((55,1285),'服色与未定发型为可逆提案；只作概念，不表示剧情结算、装备兼容或游戏运行通过。',font=fs,fill=(40,43,40))
board.save(OUT/'首批四人_中文概览.png')
