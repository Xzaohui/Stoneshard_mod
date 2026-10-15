from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BASE=Path(__file__).resolve().parent.parent
OUT=Path(__file__).resolve().parent
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
ft=ImageFont.truetype(font,38);fs=ImageFont.truetype(font,26);fm=ImageFont.truetype(font,23)
board=Image.new('RGB',(2400,1340),(236,232,221));d=ImageDraw.Draw(board)
d.text((55,28),'新增剧情人物｜第三批四人',font=ft,fill=(40,43,40))
d.text((55,85),'图里 · 维菈 · 珥德 · 锉珥     独立人物外观概念',font=fs,fill=(65,65,58))
items=[('turi','图里','HIG-NPC-TURI','只验本段本班的检查匠'),('vila','维菈','HIG-NPC-VILA','普通支架匠 · 中性外观提案'),('erde','珥德','FX-MIN','不下最深段的矿洞捡拾者'),('cuoer','锉珥','FX-MN2','留着修车工具的矿车修理工')]
for i,(slug,name,cid,role) in enumerate(items):
 x=i*600
 d.text((x+45,145),name+'  '+cid,font=fs,fill=(40,43,40));d.text((x+45,195),role,font=fm,fill=(65,65,58))
 im=Image.open(BASE/slug/'concept_v1'/f'{slug}_transparent.png').convert('RGBA')
 # Display layout only: trim empty transparent margins; preserve all character pixels and aspect ratio. Raw/transparent files remain untouched.
 im=im.crop(im.getbbox())
 im.thumbnail((530,980),Image.Resampling.NEAREST)
 board.paste(im,(x+(600-im.width)//2,250+(980-im.height)),im)
d.text((55,1285),'各栏独立等比展示，不代表相对身高；仅外观概念，不表示剧情结算、装备兼容或游戏运行通过。',font=fs,fill=(40,43,40))
board.save(OUT/'第三批四人_中文概览.png')
