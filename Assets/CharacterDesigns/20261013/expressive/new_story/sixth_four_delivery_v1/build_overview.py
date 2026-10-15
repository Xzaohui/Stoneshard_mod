from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ft=ImageFont.truetype(font,38);fs=ImageFont.truetype(font,26);fm=ImageFont.truetype(font,23)
board=Image.new('RGB',(2400,1340),(236,232,221));d=ImageDraw.Draw(board)
d.text((55,28),'新增剧情人物｜第六批四人',font=ft,fill=(40,43,40))
d.text((55,85),'珥薇 · 埕珥 · 苇珥 · 缶珥     独立人物外观概念',font=fs,fill=(65,65,58))
items=[('erwei','珥薇','FX-RLY','补丁围裙与旧锅的营地中继人'),('chenger','埕珥','FX-GH2','双层旧毯与罩灯的窖口守夜人'),('weier','苇珥','FX-HOM','背布袋持短探棍的荒宅拾荒妇'),('fouer','缶珥','FX-CP5','膝上木板袖口炭笔的帐下记账人')]
for i,(slug,name,cid,role) in enumerate(items):
 x=i*600
 d.text((x+45,145),name+'  '+cid,font=fs,fill=(40,43,40));d.text((x+45,195),role,font=fm,fill=(65,65,58))
 im=Image.open(BASE/slug/'concept_v1'/f'{slug}_transparent.png').convert('RGBA')
 # Display layout only: trim empty transparent margins; preserve all character pixels and aspect ratio. Raw/transparent files remain untouched.
 im=im.crop(im.getbbox())
 im.thumbnail((530,980),Image.Resampling.NEAREST)
 board.paste(im,(x+(600-im.width)//2,250+(980-im.height)),im)
d.text((55,1285),'各栏独立等比展示，不代表相对身高；仅外观概念，不表示剧情结算、装备兼容或游戏运行通过。',font=fs,fill=(40,43,40))
board.save(OUT/'第六批四人_中文概览.png')
