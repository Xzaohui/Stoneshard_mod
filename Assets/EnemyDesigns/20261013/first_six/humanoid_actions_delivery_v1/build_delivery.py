from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, zipfile, zlib
OUT=Path(__file__).resolve().parent
BASE=OUT.parent
SPEAR=BASE/'border_spear_rebel/action_v1';CLUB=BASE/'canal_club_brigand/action_v1'
SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
F=ImageFont.truetype(FONT,36);S=ImageFont.truetype(FONT,27)
items=[('001 预备｜前手引导握法',SPEAR/'spear_ready/border_spear_rebel_spear_ready_transparent.png',45,980,0,0),('001 短直刺｜前手引导握法',SPEAR/'spear_short_thrust/border_spear_rebel_spear_short_thrust_transparent.png',50,947,1,0),('002 紧凑预备',CLUB/'club_compact_ready/canal_club_brigand_club_compact_ready_transparent.png',45,1255,0,1),('002 控制回收定格',CLUB/'club_controlled_recover/canal_club_brigand_club_controlled_recover_transparent.png',55,1250,1,1)]
for name,bg,fg in [('light',(233,229,217,255),(37,35,31)),('dark',(29,34,40,255),(236,233,225))]:
 im=Image.new('RGBA',(2400,1950),bg);d=ImageDraw.Draw(im)
 d.text((45,25),'人形敌人动作试点｜四张独立关键姿势',font=F,fill=fg)
 d.text((45,85),'4张独立关键姿势，长矛采用前手引导握法。尚未制作连续动画。',font=S,fill=fg)
 for label,path,crown,sole,col,row in items:
  x=col*1200;y=200+row*825;d.text((x+45,y),label,font=F,fill=fg)
  src=Image.open(path).convert('RGBA');scale=620/(sole-crown);t=src.resize((round(src.width*scale),round(src.height*scale)),Image.Resampling.NEAREST);xx=x+(1200-t.width)//2;yy=round(y+710-sole*scale);im.alpha_composite(t,(xx,yy))
 d.text((45,1888),'预备与动作变化对照｜透明原图与完整源文件另附',font=S,fill=fg)
 im.convert('RGB').save(OUT/f'humanoid_actions_overview_{name}.png')
print('boards created')
