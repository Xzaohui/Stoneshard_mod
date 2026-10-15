from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for who,name,ident,notes in [('suoda','索妲','FX-WCH','四十多岁农妇 · 围巾裹下巴 · 空篮 · 压声侧望'),('kelin','珂琳','FX-HUT','十七至十八岁药师学徒 · 草药袋围裙 · 守规矩的认真神情')]:
 d=r/'Assets/CharacterDesigns/20261013/expressive/new_story'/who/'concept_v1';raw=d/f'{who}_v1_raw_imagegen.png';im=Image.open(raw).convert('RGBA');orig=im.copy();hist=im.getchannel('A').histogram();pix=im.load();changed=0
 for y in range(im.height):
  for x in range(im.width):
   rr,g,b,a=pix[x,y]
   if a<=8:changed+=int((rr,g,b,a)!=(0,0,0,0));pix[x,y]=(0,0,0,0)
 im.save(d/f'{who}_transparent.png')
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',27);titlefont=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',40)
 for label,color,ink in [('light',(239,234,220,255),(40,43,43)),('dark',(32,38,43,255),(234,229,214))]:
  canvas=Image.new('RGBA',(im.width+200,im.height+300),color);canvas.alpha_composite(im,(100,160));dr=ImageDraw.Draw(canvas);dr.text((65,40),f'{name}  {ident}  |  全身外观概念',font=titlefont,fill=ink);dr.text((65,105),notes,font=font,fill=ink);dr.text((65,im.height+185),'原创概念 · 发型配色可逆 · 装备与游戏运行未验证',font=font,fill=ink);dr.text((65,im.height+235),'第十批 · 完整原稿保留 · 待独立审查',font=font,fill=ink);canvas.convert('RGB').save(d/f'{who}_{label}_board.png')
 (d/'prepare_concept.py').write_bytes(Path(__file__).read_bytes())
 log={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator':'built-in image_gen.imagegen','transparent_background':True,'selected_raw':raw.name,'raw_sha256':sha(raw),'raw_size':im.size,'alpha_zero_pixels':hist[0],'alpha_1_to_8_pixels':sum(hist[1:9]),'alpha_9_to_254_pixels':sum(hist[9:255]),'alpha_255_pixels':hist[255],'alpha_bbox':orig.getchannel('A').getbbox(),'cleanup_changed_pixels':changed,'operation':'Only pixels with alpha<=8 zeroed; all alpha>8 RGBA untouched. No crop, scale, quantization, recoloring or drawing on anatomy. Same-size true RGBA composite on labeled light/dark boards.','runtime_verified':False,'equipment_compatibility':'unknown','revision_count':0,'status':'pending independent review'}
 (d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n');print(who,json.dumps(log,ensure_ascii=False))
