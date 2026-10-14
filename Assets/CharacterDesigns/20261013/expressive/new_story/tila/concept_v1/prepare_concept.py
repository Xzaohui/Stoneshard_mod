from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,sys,datetime
who=sys.argv[1]; root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/who/'concept_v1';raw=d/f'{who}_v1_raw_imagegen.png';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
im=Image.open(raw).convert('RGBA'); orig=im.copy();hist=im.getchannel('A').histogram(); pix=im.load(); changed=0
for y in range(im.height):
 for x in range(im.width):
  r,g,b,a=pix[x,y]
  if a<=8:
   changed+=int((r,g,b,a)!=(0,0,0,0));pix[x,y]=(0,0,0,0)
im.save(d/f'{who}_transparent.png')
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',28);titlefont=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',42)
name,ident,notes=('洛珉','FX-CAT','四十多岁 · 性别未明的中性外观提案 · 泥袍与落地油灯') if who=='luomin' else ('缇菈','FX-ABY','三十多岁妇人 · 两层旧披巾 · 一只完整鞋与一只破鞋')
for label,color,ink in [('light',(239,234,220,255),(40,43,43)),('dark',(32,38,43,255),(234,229,214))]:
 canvas=Image.new('RGBA',(im.width+200,im.height+300),color);canvas.alpha_composite(im,(100,160));dr=ImageDraw.Draw(canvas);dr.text((70,40),f'{name}  {ident}  |  全身外观概念',font=titlefont,fill=ink);dr.text((70,105),notes,font=font,fill=ink);dr.text((70,im.height+185),'原创概念 · 发型配色可逆 · 装备与游戏运行未验证',font=font,fill=ink);dr.text((70,im.height+235),'第四批 · 保留完整原稿 · 待独立审查',font=font,fill=ink);canvas.convert('RGB').save(d/f'{who}_{label}_board.png')
(d/'prepare_concept.py').write_bytes(Path(__file__).read_bytes())
log={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator':'built-in image_gen.imagegen','transparent_background':True,'selected_raw':raw.name,'raw_sha256':sha(raw),'raw_size':im.size,'alpha_zero_pixels':hist[0],'alpha_1_to_8_pixels':sum(hist[1:9]),'alpha_9_to_254_pixels':sum(hist[9:255]),'alpha_255_pixels':hist[255],'alpha_bbox':orig.getchannel('A').getbbox(),'cleanup_changed_pixels':changed,'operation':'Only RGBA pixels with alpha<=8 zeroed. Pixels alpha>8 unchanged. No crop, scale, quantization, drawing on body, face or props; same-size complete image alpha-composited on labeled light/dark boards.','runtime_verified':False,'equipment_compatibility':'unknown','revision_count':0,'status':'pending independent review'}
(d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n');print(json.dumps(log,ensure_ascii=False))
