from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib
R=Path(__file__).resolve().parents[5];D=Path(__file__).resolve().parent
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',42)
small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',28)
board=Image.new('RGBA',(2400,3260),(236,231,220,255));d=ImageDraw.Draw(board)
d.text((38,24),'枯恩与苏奈｜四个独立基础动作',font=font,fill=(44,39,34,255))
d.text((38,84),'母图身份对照 · 浅深底透明检查 · 每张均为独立静态姿态',font=small,fill=(44,39,34,255))
rows=[];inputs=[]
for slug in ['kuen','sune']:
 o=R/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';c=json.loads((o/'production_brief.json').read_text())
 items=[(R/c['mother_image']['transparent'],'母图 · 身份与道具')]+[(o/'exports'/f"{p['key']}_v1_transparent_clean.png",p['title_zh']) for p in c['plans']]
 for theme,bg,fg in [('浅底',(239,235,224,255),(44,39,34,255)),('深底',(28,33,40,255),(236,231,220,255))]:
  y=145+len(rows)*745;panel=Image.new('RGBA',(2400,745),bg);pd=ImageDraw.Draw(panel)
  pd.text((35,12),c['name']+' · '+theme,font=small,fill=fg)
  for i,(p,label) in enumerate(items):
   im=Image.open(p).convert('RGBA');im.thumbnail((730,625),Image.Resampling.NEAREST);panel.alpha_composite(im,(800*i+(800-im.width)//2,95+(625-im.height)//2));pd.text((800*i+35,54),label,font=small,fill=fg)
   inputs.append({'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'label':label,'theme':theme})
  board.alpha_composite(panel,(0,y));rows.append(slug+'_'+theme)
d=ImageDraw.Draw(board);d.text((38,3160),'未制作过渡、循环、装备组合或游戏接入；姿态不表示治疗、授权、交接或任务完成。',font=small,fill=(44,39,34,255))
p=D/'kuen_sune_four_actions_light_dark_board.png';board.convert('RGB').save(p)
(D/'board_inputs.json').write_text(json.dumps({'inputs':inputs,'processing':'Correct RGBA alpha_composite on opaque backgrounds. Nearest-neighbor uniform aspect-preserving thumbnails; no character/body edits.','board_sha256':hashlib.sha256(p.read_bytes()).hexdigest()},ensure_ascii=False,indent=2)+'\n')
print(p, p.stat().st_size)
