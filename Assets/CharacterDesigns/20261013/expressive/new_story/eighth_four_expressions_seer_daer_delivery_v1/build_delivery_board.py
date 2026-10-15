from pathlib import Path
from PIL import Image,ImageFont,ImageDraw
import shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=R/'Assets/CharacterDesigns/20261013/expressive/new_story';out=base/'eighth_four_expressions_seer_daer_delivery_v1';font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
items=[('seer','seer_E2_hurried_defence_of_intent','瑟珥','E2 急辩来意'),('daer','daer_E1_hushed_listening','达珥','E1 噤声侧听'),('daer','daer_E2_wry_acceptance_of_timidity','达珥','E2 自嘲认怯')]
b=Image.new('RGBA',(1800,2150),'#ebe5d8');draw=ImageDraw.Draw(b)
for i,(tag,bg,fg,sub) in enumerate([('浅底','#ebe5d8','#252623','#625e54'),('深底','#252a33','#eee7d8','#b7b4ab')]):
 y=i*1075;draw.rectangle((0,y,1800,y+1074),fill=bg);draw.text((52,y+25),'瑟珥与达珥 · 三张表情选稿 · '+tag,font=ImageFont.truetype(bold,42),fill=fg)
 draw.text((54,y+86),'瑟珥 E1「默数牵挂」待处理，不计入本页合格选稿',font=ImageFont.truetype(font,25),fill=sub)
 for j,(slug,stem,name,label) in enumerate(items):
  p=base/slug/'expressions_v1'/'selected'/f'{stem}_transparent.png';im=Image.open(p).convert('RGBA');bbox=im.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox();im=im.crop(bbox);scale=min(520/im.width,825/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);b.alpha_composite(im,(j*600+(600-im.width)//2,y+170+(855-im.height)));draw.text((j*600+65,y+127),name+' · '+label,font=ImageFont.truetype(bold,27),fill=fg)
 draw.text((54,y+1030),'可逆情绪概念 · 不代表任务结果、人物关系或游戏运行',font=ImageFont.truetype(font,24),fill=sub)
b.convert('RGB').save(out/'瑟珥达珥_三种表情_浅深合板.png')
for slug,stem,name,label in items:shutil.copy2(base/slug/'expressions_v1'/'selected'/f'{stem}_transparent.png',out/(name+'_'+label.replace(' ','_')+'_透明.png'))
print(out)
