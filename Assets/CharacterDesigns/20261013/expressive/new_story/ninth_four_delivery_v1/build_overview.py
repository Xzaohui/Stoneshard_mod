from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ft=ImageFont.truetype(font,38);fs=ImageFont.truetype(font,26);fm=ImageFont.truetype(font,23)
board=Image.new('RGB',(2400,1100),(236,232,221));d=ImageDraw.Draw(board)
d.text((55,28),'新增剧情人物｜第九批四人',font=ft,fill=(40,43,40))
d.text((55,85),'妲兰 · 珥兰 · 忒曼 · 佴珥     独立人物外观概念',font=fs,fill=(65,65,58))
items=[('dalan','妲兰','FX-HRP','弓囊与旧痕的巢下猎人'),('erlan','珥兰','FX-HNT','腿绑皮护、腰后三桩的设陷者'),('teman','忒曼','FX-HNY','补网面罩与旧皮袖的养蜂人'),('fx_cv4_nier','佴珥','FX-CV4','带毛旧褂与短棍的兽道守望者')]
for i,(slug,name,cid,role) in enumerate(items):
 x=i*600
 d.text((x+45,145),name+'  '+cid,font=fs,fill=(40,43,40));d.text((x+45,195),role,font=fm,fill=(65,65,58))
 im=Image.open(BASE/slug/'concept_v1'/f'{slug}_transparent.png').convert('RGBA')
 # Display layout only: full canvas preserved, uniform nearest-neighbor scale.
 im.thumbnail((530,740),Image.Resampling.NEAREST)
 board.paste(im,(x+(600-im.width)//2,250+(740-im.height)),im)
d.text((55,1045),'各栏独立等比展示，不代表相对身高；仅外观概念，不表示剧情结算、装备兼容或游戏运行通过。',font=fs,fill=(40,43,40))
board.save(OUT/'第九批四人_中文概览.png')
