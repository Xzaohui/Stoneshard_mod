from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).parent
im=Image.open(p/'raw/sq05_r02_well_raw_v2.png').convert('RGB')
board=Image.new('RGB',(1600,1260),'#202723'); d=ImageDraw.Draw(board)
f='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
def txt(x,y,t,s,c='#e5e3d5'):d.text((x,y),t,font=ImageFont.truetype(f,s,index=2),fill=c)
txt(32,20,'渡民岸井｜场景风格试稿 01 · 修订',36)
txt(32,70,'SQ05 / R02-well　粗簇简化候选 · 待审美选择 · 非游戏地图',22,'#b9c2b3')
board.paste(im,(32,115))
txt(32,1153,'单井与过滤架 · 三处岸边取样点 · 关闭分柜 · 干岸回程',25)
txt(32,1197,'构图位置为美术提案；不认证水质、任务结果或通行。原图 1536 × 1024。',21,'#b9c2b3')
board.save(p/'presentation_board_zh.png')
