from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=r/'Assets/CharacterActions/20261013/new_story';delivery=base/'luoer_qiner_noncombat_basics_v1_delivery';delivery.mkdir(exist_ok=True)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'; ft=lambda n:ImageFont.truetype(font,n)
board=Image.new('RGB',(1760,3300),(236,230,216)); d=ImageDraw.Draw(board);d.text((32,20),'珞珥 · 芩珥｜母图与基础动作 · 浅深对照',font=ft(35),fill=(44,40,36));d.text((32,67),'每人两张独立关键姿态；母图仅供对照，不计新增动作',font=ft(24),fill=(75,69,61))
rows=[('luoer','珞珥',['luoer_A1_support_lower_rope_coil_v2','luoer_A2_settle_neck_scarf_v1'],['A1 右手低托下层绳卷','A2 抬右手收稳颈巾']),('qiner','芩珥',['qiner_A1_raise_existing_sprig_v1','qiner_A2_smooth_basket_lining_front_v1'],['A1 右手提起篓内原草枝','A2 前俯按平篓沿旧布'])];entries=[]
for ci,(slug,name,keys,labels) in enumerate(rows):
 for theme,color,ink in [('浅底',(242,236,223),(42,39,34)),('深底',(29,34,39),(242,236,223))]:
  ri=ci*2+(theme=='深底');y=112+ri*780;d.rectangle((0,y,1759,y+779),fill=color);d.text((30,y+12),name+' · '+theme,font=ft(28),fill=ink)
  ims=[r/f'Assets/CharacterDesigns/20261013/expressive/new_story/{slug}/concept_v1/{slug}_transparent.png']+[base/slug/'noncombat_basics_v1/exports'/f'{key}_transparent.png' for key in keys]
  for col,(f,label) in enumerate(zip(ims,['母图 · 身份与比例锚']+labels)):
   x=28+col*580;d.text((x,y+54),label,font=ft(24),fill=ink);im=Image.open(f).convert('RGBA');new=(round(im.width*0.47),round(im.height*0.47));im=im.resize(new,Image.Resampling.NEAREST);pos=(x+(560-im.width)//2,y+99);board.paste(im,pos,im);entries.append({'file':str(f.relative_to(r)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'theme':theme,'source_size':list(Image.open(f).size),'resize_size':new,'scale':0.47,'resample':'NEAREST','whole_canvas':True,'position':pos})
d.text((30,3240),'可逆非战斗动作概念 · 非连续动画、装备兼容或游戏运行验收',font=ft(26),fill=(51,46,39));p=delivery/'珞珥_芩珥_母图动作浅深对照.png';board.save(p)
(delivery/'board_layout.json').write_text(json.dumps({'size':board.size,'source_images':entries,'method':'whole-canvas uniform NEAREST resize then true alpha composite onto named RGB background; no crop or body editing'},ensure_ascii=False,indent=2)+'\n')
for slug,_,keys,_ in rows:
 target=base/slug/'noncombat_basics_v1/review';shutil.copy2(p,target/p.name);shutil.copy2(delivery/'board_layout.json',target/'board_layout.json')
print(p,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
