from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=r/'Assets/CharacterDesigns/20261013/expressive/new_story';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
refs=['Assets/CharacterDesigns/20261013/expressive/new_story/luomin/concept_v1/luomin_transparent.png','Assets/RedrawStudies/20261013/sela_proportions/facial_refinement/redesign_G/sela_G_raw_imagegen.png','Assets/CharacterDesigns/20261013/expressive/mia/ratio_1_to_1_5/mia_ratio_1_to_1_5_v2_raw_imagegen.png','Assets/CharacterDesigns/20261013/expressive/new_story/miloer/concept_v1/miloer_transparent.png']
for s,name,ident,note in [('weier','苇珥','FX-HOM','五十来岁妇人 · 背布袋与短探路棍 · 自嘲而警醒'),('fouer','缶珥','FX-CP5','四十来岁女人 · 膝上合拢木板 · 袖口炭笔')]:
 d=base/s/'concept_v1';raw=d/f'{s}_v1_raw_imagegen.png';im=Image.open(raw).convert('RGBA');hist=im.getchannel('A').histogram();box=im.getchannel('A').getbbox();pixels=list(im.getdata());changed=sum(1 for p in pixels if p[3]<=8 and p!=(0,0,0,0));clean=Image.new('RGBA',im.size);clean.putdata([(0,0,0,0) if p[3]<=8 else p for p in pixels]);clean.save(d/f'{s}_transparent.png')
 title=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',40);font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',26)
 for label,col,ink in [('light',(239,234,220,255),(40,43,43)),('dark',(32,38,43,255),(234,229,214))]:
  canvas=Image.new('RGBA',(im.width+200,im.height+280),col);canvas.alpha_composite(clean,(100,145));dr=ImageDraw.Draw(canvas);dr.text((60,32),f'{name} {ident} | 全身外观概念',font=title,fill=ink);dr.text((60,95),note,font=font,fill=ink);dr.text((60,im.height+170),'第六批原创概念 · 发型配色可逆 · 待独立审查',font=font,fill=ink);dr.text((60,im.height+215),'未验证游戏体型、装备兼容、动作帧或实际运行',font=font,fill=ink);canvas.convert('RGB').save(d/f'{s}_{label}_board.png')
 (d/'style_refs').mkdir(exist_ok=True)
 refrecords=[]
 for i,p in enumerate(refs):
  src=r/p;dest=d/'style_refs'/src.name;shutil.copy2(src,dest);refrecords.append({'path':p,'snapshot':str(dest.relative_to(d)),'sha256':sha(src),'used_in_generation':i<3,'actual_viewed':True})
 (d/'reference_hashes.json').write_text(json.dumps(refrecords,ensure_ascii=False,indent=2))
 (d/'prepare_concept.py').write_bytes(Path(__file__).read_bytes())
 log={'generator':'builtin image_gen.imagegen','transparent_background':True,'revision_count':0,'raw_sha256':sha(raw),'size':im.size,'alpha_bbox':box,'alpha_zero_pixels':hist[0],'alpha_1_to_8_pixels':sum(hist[1:9]),'alpha_9_to_254_pixels':sum(hist[9:255]),'alpha_255_pixels':hist[255],'cleanup_changed_pixels':changed,'operation':'Only alpha<=8 pixels zeroed; all alpha>8 RGBA unchanged. No crop, resize, quantization or scripted person drawing. Full-size alpha composited on labeled boards.','runtime_verified':False}
 (d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2));print(s,json.dumps(log))
