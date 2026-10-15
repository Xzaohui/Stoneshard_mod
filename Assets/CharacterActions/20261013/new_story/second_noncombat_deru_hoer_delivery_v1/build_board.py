from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
F = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',38)
S = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
items=[]
for slug,name in [('deru','德茹'),('hoer','霍珥')]:
    d=BASE/slug/'noncombat_basics_v1'
    for a in json.loads((d/'asset_catalog.json').read_text()):
        items.append((name,a['title_zh'],Image.open(d/a['export']).convert('RGBA')))
board=Image.new('RGBA',(2400,2050),(237,233,222,255))
draw=ImageDraw.Draw(board)
draw.text((35,18),'德茹与霍珥｜四种独立基础动作',font=F,fill=(35,35,35))
draw.text((35,74),'每列同一姿态分别在浅底与深底展示；不是连续帧，不构成动画。',font=S,fill=(35,35,35))
for row,(bg,fg,y0) in enumerate([((237,233,222,255),(35,35,35),120),((31,36,42,255),(237,233,222),1040)]):
    draw.rectangle((0,y0,2400,y0+920),fill=bg)
    for col,(name,title,img) in enumerate(items):
        x=col*600
        draw.text((x+28,y0+15),name+' · '+title,font=S,fill=fg)
        n=img.copy();n.thumbnail((560,825),Image.Resampling.NEAREST)
        board.alpha_composite(n,(x+(600-n.width)//2,y0+76+(825-n.height)//2))
draw.text((35,1986),'独立非战斗姿态概念。未接入游戏；不表示任务完成、修复、授权或治疗。',font=S,fill=(35,35,35))
board.convert('RGB').save(HERE/'delivery/deru_hoer_four_actions_light_dark_board.png')
print(HERE/'delivery/deru_hoer_four_actions_light_dark_board.png')
