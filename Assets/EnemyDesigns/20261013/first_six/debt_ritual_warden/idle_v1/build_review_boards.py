from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,shutil
ROOT=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for slug,name,rawname,num in [('blood_hunger_mutant','饥血潜行体','blood_hunger_mutant_idle_raw_imagegen.png',5),('debt_ritual_warden','债契仪式看守','debt_ritual_warden_idle_v2_raw_imagegen.png',6)]:
 d=ROOT/'Assets/EnemyDesigns/20261013/first_six'/slug/'idle_v1'
 raw=Image.open(d/rawname).convert('RGBA'); data=list(raw.getdata()); nlow=sum(0<a<=8 for r,g,b,a in data); nhidden=sum(a==0 and bool(r or g or b) for r,g,b,a in data)
 final=Image.new('RGBA',raw.size);final.putdata([(0,0,0,0) if a<=8 else (r,g,b,a) for r,g,b,a in data]);fn=f'{slug}_idle_transparent.png';final.save(d/fn)
 # Presentation layout only: preserve RGBA, nearest-neighbor proportional scaling.
 for theme,bg,fg in [('light',(238,232,218,255),(50,43,38)),('dark',(31,34,38,255),(225,220,205))]:
  board=Image.new('RGBA',(1600,1050),bg);dr=ImageDraw.Draw(board);dr.text((42,24),f'{num:03}  {name}｜静态全身概念',font=ImageFont.truetype(font,36),fill=fg)
  crop=final.crop(final.getbbox()); s=min(1090/crop.width,820/crop.height);big=crop.resize((round(crop.width*s),round(crop.height*s)),Image.Resampling.NEAREST);board.alpha_composite(big,(max(35,590-big.width//2),110+(820-big.height)//2))
  s=min(280/crop.width,350/crop.height);small=crop.resize((round(crop.width*s),round(crop.height*s)),Image.Resampling.NEAREST);board.alpha_composite(small,(1250+(280-small.width)//2,330+(350-small.height)//2))
  dr.text((1240,720),'缩小可读性预览',font=ImageFont.truetype(font,25),fill=fg)
  dr.text((42,970),'原创美术候选 · 非原版独立阵营 · 剧情身份待定 · 未制作动画或接入游戏',font=ImageFont.truetype(font,26),fill=fg)
  board.convert('RGB').save(d/f'{slug}_review_{theme}_zh.png')
 # correct raw alpha composite for inspection, no edits or inferred background removal.
 comp=Image.new('RGBA',raw.size,(238,232,218,255));comp.alpha_composite(raw);comp.convert('RGB').save(d/'raw_alpha_on_light.png')
 stats={'raw_mode':Image.open(d/rawname).mode,'dimensions':raw.size,'raw_alpha_extrema':raw.getchannel('A').getextrema(),'raw_alpha_zero':sum(a==0 for r,g,b,a in data),'cleared_alpha_1_to_8':nlow,'cleared_hidden_rgb_alpha_zero':nhidden,'final_bbox':final.getbbox(),'final_alpha_extrema':final.getchannel('A').getextrema(),'preserve_alpha_gt8':True,'no_palette_quantization':True,'no_body_pixel_edit':True}
 (d/'alpha_audit.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2))
 shutil.copyfile(__file__,d/'build_review_boards.py')
 print(slug,stats)
