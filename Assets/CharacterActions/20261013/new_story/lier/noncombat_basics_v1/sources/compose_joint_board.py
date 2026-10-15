from pathlib import Path
import json,hashlib,shutil
from PIL import Image, ImageDraw, ImageFont

r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
b=r/'Assets/CharacterActions/20261013/new_story'
delivery=b/'seventh_lier_huier_delivery_v1'
delivery.mkdir(exist_ok=True)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
F=lambda size:ImageFont.truetype(font,size)
B=lambda size:ImageFont.truetype(bold,size)
W,H=3240,1730
board=Image.new('RGBA',(W,H),(242,237,224,255))
draw=ImageDraw.Draw(board)
draw.text((45,25),'栎珥 · 洄珥｜母图与基础动作',font=B(48),fill='#282724')
draw.text((45,90),'2 位既有人物 · 3 张合格独立姿态 · 栎珥 A1 缺项｜母图与动作分别展示，不代表连续动画',font=F(28),fill='#45413a')
items=[('lier','母图（已审）',r/'Assets/CharacterDesigns/20261013/expressive/new_story/lier/concept_v1/lier_transparent.png'),('lier','A1 缺项：横臂收托两绳尾',None),('lier','A2 稳身低抬右脚收步',b/'lier/noncombat_basics_v1/exports/lier_A2_low_right_foot_return_step_v1_transparent.png'),('huier','母图（已审）',r/'Assets/CharacterDesigns/20261013/expressive/new_story/huier/concept_v1/huier_transparent.png'),('huier','A1 抬右臂遮额望天',b/'huier/noncombat_basics_v1/exports/huier_A1_raise_right_hand_brow_shade_v1_transparent.png'),('huier','A2 双手分握背带稳肩载',b/'huier/noncombat_basics_v1/exports/huier_A2_two_hand_settle_carry_strap_v1_transparent.png')]
layout=[]
for row,(tone,bg,fg) in enumerate([('浅底',(239,234,221,255),'#272824'),('深底',(33,37,41,255),'#ede9df')]):
 top=150+row*735
 draw.rectangle((0,top,W,top+735),fill=bg)
 for i,(slug,title,p) in enumerate(items):
  left=i*540
  draw.text((left+22,top+16),('栎珥' if slug=='lier' else '洄珥')+' · '+tone,font=B(28),fill=fg)
  draw.text((left+22,top+62),title,font=F(25),fill=fg)
  if p is None:
   draw.text((left+52,top+305),'未达到双尾同掌收托接点',font=F(25),fill=fg)
   draw.text((left+52,top+350),'首稿及唯一修订保留源包',font=F(25),fill=fg)
   draw.text((left+52,top+395),'不计合格姿态',font=B(28),fill=fg)
   layout.append({'row':row,'column':i,'status':'missing_after_one_revision','image':None})
   continue
  im=Image.open(p).convert('RGBA')
  scale=min(520/im.width,610/im.height)
  size=(round(im.width*scale),round(im.height*scale))
  x=left+(540-size[0])//2;y=top+110+(610-size[1])//2
  resized=im.resize(size,Image.Resampling.NEAREST)
  board.alpha_composite(resized,(x,y))
  layout.append({'row':row,'column':i,'image':str(p.relative_to(r)),'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_size':list(im.size),'display_size':list(size),'x':x,'y':y,'resampling':'NEAREST','whole_image_uniform_scale':scale,'background':list(bg)})
 draw.line((1620,top+15,1620,top+715),fill=('#c6bba8' if row==0 else '#4c5155'),width=2)
draw=ImageDraw.Draw(board)
draw.text((45,1640),'可逆非战斗演出提案；不表示道路安全、天气判断、拾柴收获或任务完成。',font=F(28),fill='#45413a')
draw.text((45,1680),'完整透明图与首稿／修订／提示词／工具返回另存；游戏像素网格、装备、碰撞、动画与运行未验证。',font=F(26),fill='#45413a')
out=b/'lier/noncombat_basics_v1/review/栎珥_洄珥_母图动作浅深对照.png'
board.convert('RGB').save(out)
record={'board':str(out.relative_to(r)),'size':[W,H],'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'actual_alpha_composite':True,'resampling':'NEAREST','no_body_edit':True,'selected_count':3,'missing':['lier_A1_gather_two_rope_tails'],'cells':layout}
(out.parent/'joint_board_layout.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
shutil.copy2(out,delivery/out.name)
print(out,record['sha256'])
