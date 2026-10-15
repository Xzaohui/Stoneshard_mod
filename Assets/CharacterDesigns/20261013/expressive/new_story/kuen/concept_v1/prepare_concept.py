from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json,hashlib,shutil,datetime,sys
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); who=sys.argv[1];d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/who/'concept_v1'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=d/f'{who}_v1_raw_imagegen.png'; im=Image.open(raw).convert('RGBA'); src=im.copy(); pix=list(im.getdata()); out=[(0,0,0,0) if p[3]<=8 else p for p in pix];im.putdata(out);im.save(d/f'{who}_transparent.png');hist=src.getchannel('A').histogram();
name,subtitle=('枯恩','成年患者 · 具体表达所需帮助 · 水杯未触碰') if who=='kuen' else ('苏奈','成年记录员 · 先问许可 · 两栏留空未记录')
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
for mode,bg,fg in [('light',(239,234,223,255),(43,41,40)),('dark',(30,35,40,255),(235,231,219))]:
 board=Image.new('RGBA',(im.width+160,im.height+220),bg);board.alpha_composite(im,(80,120));draw=ImageDraw.Draw(board);draw.text((50,20),name+'｜全身概念',font=ImageFont.truetype(font,34),fill=fg);draw.text((50,68),subtitle,font=ImageFont.truetype(font,24),fill=fg);draw.text((50,board.height-45),'原创外观提案｜非游戏实装验收',font=ImageFont.truetype(font,22),fill=fg);board.convert('RGB').save(d/f'{who}_{mode}_board.png')
shutil.copyfile(__file__,d/'prepare_concept.py');
if who=='sune':
 p=root/'Assets/CharacterDesigns/20261013/expressive/new_story/deru/concept_v1/deru_v2_raw_imagegen.png';shutil.copyfile(p,d/'style_refs'/p.name); f=d/'source_hashes.json';j=json.loads(f.read_text());j.append({'path':str(p.relative_to(root)),'sha256':sha(p),'use':'coarse pixel style only; viewed before generation'});f.write_text(json.dumps(j,ensure_ascii=False,indent=2))
log={'generator':'builtin image_gen.imagegen','transparent_background':True,'selected_raw':raw.name,'raw_sha256':sha(raw),'raw_size':im.size,'alpha_1_to_8_cleared':sum(hist[1:9]),'raw_alpha_0':hist[0],'raw_alpha_255':hist[255],'alpha_bbox':im.getchannel('A').getbbox(),'permitted_operations':'alpha <=8 set zero; hidden RGB zero only for resulting alpha=0. All pixels alpha>8 exactly unchanged. Boards full image at native scale; Chinese labels only in surrounding margins. No cropping, redrawing, resampling, quantization or deformation.','runtime_verified':False,'equipment_compatibility':'unknown','status':'pending final independent review'}
(d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
qa={'author_actual_view':True,'selected_raw':raw.name,'character':name,'identity':'成年男性三十多岁，清醒坐姿' if who=='kuen' else '成年女性二十多岁，征询许可而非冷面实验者','observed_story_props':['厚披肩','背部布卷','杯置独立矮凳，双手未碰杯','手背轻微旧青，无现代针具','完整裤袜鞋与椅子'] if who=='kuen' else ['短低辫','朴素木板，两空栏','两支炭笔收在笔插','空手掌心上提，未写字','紧袖口与完整衣鞋'],'style_observation':'大头紧凑成年体态、完整轮廓、清楚块状像素，面部有独立情绪。','proposals_not_canon':['发型','配色','鞋式'],'not_claimed':['用户最终选稿','游戏运行','装备兼容','同意已获或剧情结案'],'status':'author check complete, independent review separate'}
(d/'author_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
print(json.dumps(log,ensure_ascii=False))
