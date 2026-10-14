from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json, hashlib, numpy as np, sys
ROOT=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
FONT='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SELECTIONS={'vila': [('vila_A1_gauge_bracket_selfcheck','revision1','量规贴近样品底槽'),('vila_A2_return_gauge_to_pocket','initial','样品自持，量规归袋')], 'luomin':[('luomin_A1_lantern_low_hold','initial','低位稳提油灯'),('luomin_A2_lower_lantern_to_ground','revision1','俯身稳放油灯')]}
NAMES={'vila':'维菈','luomin':'洛珉'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,d):p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def prep(slug):
 p=ROOT/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1'; sel=SELECTIONS[slug]
 for key,attempt,title in sel:
  im=Image.open(p/f'selected/{key}.png').convert('RGBA')
  for name,color in [('light',(238,233,216,255)),('dark',(36,42,50,255))]:
   b=Image.new('RGBA',im.size,color);b.alpha_composite(im);b.convert('RGB').save(p/f'review/{key}_selected_{name}.png')
 for name,color,fg in [('light',(238,233,216,255),(36,36,32)),('dark',(36,42,50,255),(242,236,220))]:
  board=Image.new('RGBA',(1800,1260),color); draw=ImageDraw.Draw(board);font=ImageFont.truetype(FONT,35);small=ImageFont.truetype(FONT,24)
  draw.text((36,25),f'{NAMES[slug]}｜非战斗独立关键姿势',font=font,fill=fg)
  draw.text((36,80),'母图对照与两张动作概念；不是连续动画，不表示剧情已完成',font=small,fill=fg)
  images=[(p/f'sources/{slug}_anchor.png','母图｜既有姿势')]+[(p/f'selected/{k}.png',t) for k,a,t in sel]
  for i,(ip,label) in enumerate(images):
   im=Image.open(ip).convert('RGBA'); r=min(530/im.width,1000/im.height);size=(round(im.width*r),round(im.height*r));im=im.resize(size,Image.Resampling.NEAREST);board.alpha_composite(im,(i*600+(600-im.width)//2,190+(1000-im.height)//2));draw.text((i*600+35,140),label,font=small,fill=fg)
  draw.text((36,1206),'透明选稿仅清零 alpha≤8；比例排版不改身体；装备与引擎尚未验收',font=small,fill=fg)
  board.convert('RGB').save(p/f'review/{slug}_mother_actions_{name}.png')
 return p
if __name__=='__main__':
 for slug in SELECTIONS: print(prep(slug))
