from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,shutil,zipfile
root=Path(__file__).resolve().parents[5]
base=root/'Assets/EnemyDesigns/20261013/first_six';delivery=Path(__file__).resolve().parent
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26)
small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',23)
bold=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',33)
brief=json.loads((base/'action_continuation_brief_v1.json').read_text())
rows=[]
for r in brief['items'][:2]:
 p=root/r['planned_generation']['output_directory_if_later_executed'];refs=[root/x['path'] for x in r['planned_generation']['reference_order'][:2]];new=p/f"{r['role']}_{r['proposed_keypose']['pose_id']}_transparent_candidate_v2.png"
 if r['id']=='001':paths=[refs[1],refs[0],new];labels=['旧选稿：架矛戒备','旧选稿：短促前刺','新增选稿：短刺后收矛 v2'];outcome='001 边地长矛手｜通过：收矛及后移承重';color='#39714c'
 else:paths=[refs[0],new,refs[1]];labels=['旧选稿：紧凑备击','未通过／不选稿：下挥候选 v2','旧选稿：收势回防'];outcome='002 旧渠劫道者｜未通过：棍头仍偏低，停止修订';color='#933e32'
 rows.append((paths,labels,outcome,color))
W=2160;cw=720;scale=.44;total=90+sum(70+2*(int(max(Image.open(p).height for p in paths)*scale)+55) for paths,_,_,_ in rows)+110
board=Image.new('RGB',(W,total),'#f3eee4');draw=ImageDraw.Draw(board);draw.text((26,18),'首六敌人动作补缺｜001–002 相邻阶段审查',font=bold,fill='#20262c');y=80
for paths,labels,outcome,color in rows:
 draw.rectangle((0,y,W,y+65),fill='#f3eee4');draw.text((26,y+12),outcome,fill=color,font=font);y+=70;images=[Image.open(p).convert('RGBA') for p in paths];rh=int(max(i.height for i in images)*scale)+55
 for ri,bg in enumerate(['#e6dfd0','#23272e']):
  for k,(im,label) in enumerate(zip(images,labels)):
   tmp=Image.new('RGBA',(cw,rh),bg);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);tmp.alpha_composite(im,((cw-im.width)//2,48));board.paste(tmp.convert('RGB'),(k*cw,y));draw.text((k*cw+15,y+10),label,font=small,fill=('#252b31' if ri==0 else '#f1eadc'))
  y+=rh
 draw=ImageDraw.Draw(board)
draw.text((26,y+17),'旧动作原图未变。仅独立关键姿势概念；不代表连续动画、精确锚点、统一武器尺度或游戏验收。',font=small,fill='#343a40')
draw.text((26,y+51),'001 跨姿矛长与整体尺度仍待核；002 修订额度已用完，无新增选稿。浅底／深底均为正常 RGBA 合成。',font=small,fill='#343a40')
board.save(delivery/'001_002_动作补缺_浅深阶段对照.png')
p=base/'border_spear_rebel/action_continuation_v1/spear_retract_weight_back';src=p/'border_spear_rebel_spear_retract_weight_back_transparent_candidate_v2.png';dst=p/'border_spear_rebel_spear_retract_weight_back_transparent.png'
if not dst.exists():shutil.copy2(src,dst)
shutil.copy2(dst,delivery/dst.name)
print('Board:',board.size,'selected SHA:',hashlib.sha256(dst.read_bytes()).hexdigest())
