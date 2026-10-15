from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,zipfile
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');D=Path(__file__).resolve().parent;B=json.loads((R/'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief_v2.json').read_text());SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';f=ImageFont.truetype(font,26);sm=ImageFont.truetype(font,21)
items=[(c,p,R/p['planned_transparent_path']) for c in B['characters'][:2] for p in c['poses']]; boards=[]
for mode,bg,fg in [('light',(234,230,216),(35,36,39)),('dark',(26,32,40),(239,236,225))]:
 board=Image.new('RGB',(2000,1000),bg);dr=ImageDraw.Draw(board);dr.text((25,18),'第二组 007／008｜四张独立基础关键姿势｜'+('浅底' if mode=='light' else '深底'),font=f,fill=fg)
 dr.text((25,62),'按人物发顶—靴底近似等比排版；非统一游戏网格。未拉伸身体或武器。',font=sm,fill=fg)
 for i,(c,p,path) in enumerate(items):
  im=Image.open(path).convert('RGBA');bbox=im.getbbox();scale=590/(bbox[3]-bbox[1]);out=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);x=i*500+(500-out.width)//2;y=round(800-bbox[3]*scale);board.paste(out,(x,y),out)
  dr.text((i*500+20,110),c['concept_id'][-3:]+' '+c['working_name'],font=f,fill=fg);dr.text((i*500+20,150),p['label'],font=sm,fill=fg)
  mini=im.resize((round(im.width*0.07),round(im.height*0.07)),Image.Resampling.NEAREST);board.paste(mini,(i*500+395,850),mini)
  dr.text((i*500+20,850),'身份、支撑、握持及留边已审',font=sm,fill=fg)
 dr.text((25,952),'原创动作概念；不代表连续动画、帧序、绑定、碰撞、装备合成或游戏运行验收。',font=sm,fill=fg);board.save(D/f'007_008_action_{mode}.png');boards.append(board)
combo=Image.new('RGB',(2000,2000));combo.paste(boards[0],(0,0));combo.paste(boards[1],(0,1000));combo.save(D/'007_008_action_light_dark.png')
print(D/'007_008_action_light_dark.png')
