from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json,hashlib,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); b=r/'Assets/CharacterActions/20261013/new_story'; delivery=b/'sixth_noncombat_weier_fouer_delivery_v1';delivery.mkdir(exist_ok=True)
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';titlefont=ImageFont.truetype(font,43);labelfont=ImageFont.truetype(font,29);notefont=ImageFont.truetype(font,25)
w,rh,top,bottom,cw=2240,740,150,100,720;board=Image.new('RGB',(w,top+4*rh+bottom),'#f4efe3');draw=ImageDraw.Draw(board)
draw.text((40,24),'苇珥 / 缶珥 · 日常基础动作',font=titlefont,fill='#2b2c28');draw.text((40,86),'母图与动作浅底 / 深底对照 · 3 张通过，1 张缺项 · 独立静态关键姿态',font=notefont,fill='#535650')
characters=[('weier','苇珥',[(None,'A1 · 短棍斜探右脚尖点地'),('weier_A2_two_hand_low_crosswise_stick_v1','A2 · 双手近身横收原短棍')]),('fouer','缶珥',[('fouer_A1_tilt_closed_board_upright_on_lap_v1','A1 · 坐稳将合板竖靠膝前'),('fouer_A2_reseat_charcoal_in_left_cuff_v1','A2 · 稳板按回左袖原炭笔')])]
placements=[];missing=[];row=0;scale=.47
for slug,name,actions in characters:
 mother=r/f'Assets/CharacterDesigns/20261013/expressive/new_story/{slug}/concept_v1/{slug}_transparent.png'
 images=[(mother,'母图 · 身份锚')]+[(b/slug/'noncombat_basics_v1/exports'/f'{k}_transparent.png' if k else None,t) for k,t in actions]
 for tone,color,ink in [('浅底',(239,233,219),(43,44,40)),('深底',(29,34,38),(242,235,219))]:
  y0=top+row*rh;draw.rectangle((0,y0,w,y0+rh-1),fill=color)
  for col,(path,title) in enumerate(images):
   x0=40+col*cw;label=f'{name} · {tone} · {title}';draw.text((x0+12,y0+17),label,font=labelfont,fill=ink)
   if path is None:
    for offset,line in [(240,'缺项 · 未纳入通过成稿'),(292,'首稿与唯一修订均未达到'),(338,'“脚尖轻落、鞋跟抬起”接点'),(406,'两稿与完整生成记录保留在源包')]:draw.text((x0+85,y0+offset),line,font=notefont,fill=ink)
    missing.append({'row':row,'column':col,'key':'weier_A1_toe_probe_with_slanted_stick','reason':'Both drafts fail toe contact / raised heel; no third attempt.','image_shown':False});continue
   im=Image.open(path).convert('RGBA');size=(round(im.width*scale),round(im.height*scale));preview=im.resize(size,Image.Resampling.NEAREST);xy=(x0+(cw-size[0])//2,y0+rh-16-size[1]);board.paste(preview,xy,preview)
   placements.append({'row':row,'column':col,'character':slug,'tone':tone,'label':label,'source':str(path.relative_to(r)),'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'source_size':list(im.size),'scale':scale,'resample':'NEAREST','target_size':list(size),'paste_xy':list(xy),'body_crop_or_stretch':False})
  row+=1
draw.text((40,board.height-76),'日常动作概念；非连续动画，不代表游戏落地或剧情结果。',font=notefont,fill='#535650');draw.text((40,board.height-39),'苇珥 = FX-HOM 荒宅拾荒妇；缶珥保持原木凳坐姿、闭合木板与左袖单炭笔。',font=notefont,fill='#535650')
out=delivery/'苇珥_缶珥_母图动作浅深对照.png';board.save(out);layout={'board':str(out.relative_to(r)),'board_size':list(board.size),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'placements':placements,'missing_cells':missing,'method':'Exact RGBA source composited on true light/dark backgrounds at shared isotropic .47 scale using nearest; labels only.'}
for slug,_,_ in characters:
 p=b/slug/'noncombat_basics_v1';shutil.copyfile(out,p/'review'/out.name);(p/'review/board_layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');shutil.copyfile('/tmp/compose_weier_fouer.py',p/'sources/compose_board.py')
(delivery/'board_layout.json').write_text(json.dumps(layout,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'board':str(out),'size':board.size,'sha256':layout['sha256']}))
