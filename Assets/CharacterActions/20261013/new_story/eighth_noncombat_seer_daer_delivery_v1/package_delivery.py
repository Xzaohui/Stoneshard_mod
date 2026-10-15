from pathlib import Path
import json,hashlib,shutil,datetime,zipfile
from PIL import Image,ImageDraw,ImageFont
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');N=R/'Assets/CharacterActions/20261013/new_story';D=N/'eighth_noncombat_seer_daer_delivery_v1';D.mkdir(exist_ok=True);(D/'delivery').mkdir(exist_ok=True)
S=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
rows=[('seer','瑟珥',[('seer_A1_brush_left_tunic_hem','v1','左手拂平左侧衣摆'),('seer_A2_smooth_left_hair','v1','抬左手轻理侧发')]),('daer','达珥',[('daer_A1_smooth_left_forearm_sleeve','revision1','右掌抚平左前臂衣袖'),('daer_A2_grip_left_bag_strap','v1','左手上提扶稳空袋背带')])]
selection=[]
for slug,name,acts in rows:
 d=N/slug/'noncombat_basics_v1'
 for key,v,label in acts:
  src=d/'review'/f'{key}_{v}_transparent.png';dst=d/'selected'/f'{key}_transparent.png';shutil.copyfile(src,dst);assert S(src)==S(dst)
  deliver=D/'delivery'/f'{name}_{key.split("_")[1]}_{label}.png';shutil.copyfile(dst,deliver)
  selection.append({'character':slug,'name_zh':name,'key':key,'label_zh':label,'selected_version':v,'selected_path':str(dst.relative_to(R)),'selected_sha256':S(dst),'raw_path':str((d/'raw'/f'{key}_{v}_raw_imagegen.png').relative_to(R)),'raw_sha256':S(d/'raw'/f'{key}_{v}_raw_imagegen.png'),'delivery_path':str(deliver.relative_to(R))})
(D/'selection.json').write_text(json.dumps({'selected_count':4,'new_characters':0,'independent_poses':4,'rejected_attempts':[{'key':'daer_A1_smooth_left_forearm_sleeve','version':'v1','reason':'双臂解剖侧别反了','preserved':True}],'selected':selection},ensure_ascii=False,indent=2)+'\n')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';bold='/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
f=lambda size,b=False:ImageFont.truetype(bold if b else font,size)
W,H=3200,1620;board=Image.new('RGB',(W,H),(238,232,217));draw=ImageDraw.Draw(board)
draw.rectangle((1600,0,3199,H-1),fill=(37,40,45))
for x,col in [(40,(40,38,34)),(1640,(238,232,217))]:
 draw.text((x,22),'瑟珥 · 达珥｜普通基础动作概念',font=f(43,True),fill=col)
 draw.text((x,83),'母图 + 两张独立动作 · '+('浅底' if x<1600 else '深底'),font=f(28),fill=col)
layout=[]
for ri,(slug,name,acts) in enumerate(rows):
 y=135+ri*710
 for bi,bgx in enumerate([0,1600]):
  color=(40,38,34) if bi==0 else (238,232,217)
  imgs=[(R/f'Assets/CharacterDesigns/20261013/expressive/new_story/{slug}/concept_v1/{slug}_transparent.png',name+'｜原母图')]+[(N/slug/'noncombat_basics_v1/selected'/f'{key}_transparent.png',name+' '+key.split('_')[1]+'｜'+label) for key,v,label in acts]
  for ci,(p,label) in enumerate(imgs):
   x=bgx+ci*533;im=Image.open(p).convert('RGBA');scale=min(500/im.width,620/im.height);size=(round(im.width*scale),round(im.height*scale));small=im.resize(size,Image.Resampling.NEAREST);tx=x+(533-size[0])//2;ty=y+62
   draw.text((x+22,y+9),label,font=f(27,True),fill=color);board.paste(small,(tx,ty),small)
   layout.append({'source':str(p.relative_to(R)),'sha256':S(p),'source_size':list(im.size),'display_size':list(size),'position':[tx,ty],'resample':'NEAREST','full_canvas_no_crop':True,'background':'light' if bi==0 else 'dark','uniform_scale':scale})
for x,col in [(40,(70,66,59)),(1640,(215,210,202))]:
 draw.text((x,1565),'静态可逆概念；不代表连续动画、任务结果或游戏运行。',font=f(27),fill=col)
p=D/'瑟珥_达珥_母图动作浅深对照.png';board.save(p);shutil.copyfile(p,D/'delivery'/p.name)
(D/'board_layout.json').write_text(json.dumps({'size':[W,H],'composition':'each source full RGBA canvas is nearest aspect-preserved onto true opaque light and dark backgrounds','layout':layout},ensure_ascii=False,indent=2)+'\n')
(D/'README_中文.md').write_text('# 瑟珥与达珥 · 第八批普通基础动作\n\n2位既有人物，4张独立透明全身动作概念。瑟珥理衣摆、理侧发；达珥理左袖、扶空袋带。\n\n达珥A1首稿两臂侧别反向，唯一修订后通过，失败首稿raw/透明/浅深/完整工具返回和提示词全部保留。瑟珥旧E1安全阻断表情未重试，不计本次动作。\n\n人物由内置imagegen串行绘制；仅清理alpha≤8及透明像素隐藏RGB，完整图nearest等比排板，不拼人体、镜像或拉伸。透明PNG保留原生分辨率1118×1407。\n\n仅可逆概念，不表示剧情已发生、连续动画、装备、碰撞或runtime通过。未Git、未上传。完整源ZIP按目录相对路径合并解压；独立ZIP不是分卷格式。\n')
shutil.copyfile(__file__,D/'package_delivery.py')
print(json.dumps({'directory':str(D),'board':str(p),'board_sha256':S(p),'selected_count':len(selection)},ensure_ascii=False,indent=2))
