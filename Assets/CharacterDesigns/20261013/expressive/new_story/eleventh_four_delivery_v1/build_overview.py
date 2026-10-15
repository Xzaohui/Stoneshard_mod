from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ft=ImageFont.truetype(font,38);fs=ImageFont.truetype(font,26);fm=ImageFont.truetype(font,23)
board=Image.new('RGB',(2400,1100),(236,232,221));d=ImageDraw.Draw(board)
d.text((55,28),'新增剧情人物｜第十一批四人',font=ft,fill=(40,43,40))
d.text((55,85),'韦珥 · 摩珥 · 岱珥 · 谟珥     独立人物外观概念',font=fs,fill=(65,65,58))
items=[('weier_ink','韦珥','FX-INK','洗白围裙与旧钥匙的旅馆旧仆'),('moer','摩珥','FX-WIL','黄指节与木账板的酒馆账房'),('daier','岱珥','FX-MAN','补旧外套与无用钥匙的看守'),('moer_trs','谟珥','FX-TRS','背短铲、鞋沾崖灰的堡垒寻宝者')]
for i,(slug,name,cid,role) in enumerate(items):
 x=i*600
 d.text((x+45,145),name+'  '+cid,font=fs,fill=(40,43,40));d.text((x+45,195),role,font=fm,fill=(65,65,58))
 im=Image.open(BASE/slug/'concept_v1'/f'{slug}_transparent.png').convert('RGBA')
 # Display layout only: full canvas preserved, uniform nearest-neighbor scale.
 im.thumbnail((530,740),Image.Resampling.NEAREST)
 board.paste(im,(x+(600-im.width)//2,250+(740-im.height)),im)
d.text((55,1045),'各栏独立等比展示，不代表相对身高；仅外观概念，不表示剧情结算、装备兼容或游戏运行通过。',font=fs,fill=(40,43,40))
board.save(OUT/'第十一批四人_中文概览.png')
