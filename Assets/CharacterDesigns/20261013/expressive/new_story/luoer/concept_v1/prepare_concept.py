from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,shutil
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for who,name,ident,notes in [('luoer','珞珥','FX-CV1','三十多岁女子 · 两卷背绳 · 修补靴 · 克制判断'),('qiner','芩珥','FX-CV2','四十来岁女人 · 旧布垫背篓 · 指上草汁褐染')]:
 d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/who/'concept_v1';raw=d/f'{who}_v1_raw_imagegen.png'
 im=Image.open(raw).convert('RGBA');orig=im.copy();hist=im.getchannel('A').histogram();px=im.load();changed=0
 for y in range(im.height):
  for x in range(im.width):
   r,g,b,a=px[x,y]
   if a<=8:
    changed+=int((r,g,b,a)!=(0,0,0,0));px[x,y]=(0,0,0,0)
 im.save(d/f'{who}_transparent.png')
 assert all(a==b or a[3]<=8 for a,b in zip(orig.getdata(),im.getdata()))
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',28);tf=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',42)
 for label,bg,ink in [('light',(239,234,220,255),(40,43,43)),('dark',(32,38,43,255),(234,229,214))]:
  board=Image.new('RGBA',(im.width+200,im.height+300),bg);board.alpha_composite(im,(100,160));dr=ImageDraw.Draw(board)
  dr.text((70,40),f'{name}  {ident}  |  全身外观概念',font=tf,fill=ink);dr.text((70,105),notes,font=font,fill=ink)
  dr.text((70,im.height+185),'原创概念 · 发型配色可逆 · 装备与游戏运行未验证',font=font,fill=ink)
  dr.text((70,im.height+235),'第七批 · 保留完整原稿 · 待独立审查',font=font,fill=ink)
  board.convert('RGB').save(d/f'{who}_{label}_board.png')
 shutil.copy2(__file__,d/'prepare_concept.py')
 log={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator':'built-in image_gen.imagegen','transparent_background':True,'selected_raw':raw.name,'raw_sha256':sha(raw),'raw_size':im.size,'alpha_zero_pixels':hist[0],'alpha_1_to_8_pixels':sum(hist[1:9]),'alpha_9_to_254_pixels':sum(hist[9:255]),'alpha_255_pixels':hist[255],'alpha_bbox':orig.getchannel('A').getbbox(),'cleanup_changed_pixels':changed,'alpha_gt_8_exactly_preserved':True,'operation':'Only RGBA alpha<=8 zeroed. No crop, resize, quantization, repaint or added body/face/prop pixels. Same-size full PNG alpha-composited on labeled light/dark boards.','runtime_verified':False,'equipment_compatibility':'unknown','revision_count':0,'status':'pending independent review'}
 (d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
 qa={'canonical_id':ident,'author_viewed':['Sela G','Mia 1:1.5 v2','Luomin transparent','Miloer transparent',raw.name],'source_identity':notes,'coarse_pixel_clusters':True,'whole_body_and_props_visible':True,'story_guard':'无新授权、处方、交易、奖励、安全担保或治疗承诺。','proposals':'脸型、发型、配色及未定服饰均可逆。','limitations':(['补靴可读性较弱：靴前帮有分色加固与接缝，明显补片集中裤腿和衣摆；独审预览不判明确硬错。'] if who=='luoer' else ['草汁染痕为褐绿像素色块，不是创伤或血液。背篓较大以保证旧布与手指可读。']),'revision_count':0,'independent_review':'pending','runtime_verified':False}
 (d/'author_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(who,json.dumps(log,ensure_ascii=False))
