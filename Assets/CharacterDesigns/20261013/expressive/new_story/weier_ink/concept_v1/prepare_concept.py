from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,numpy as np
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
for who,name,ident,note,ref in [('weier_ink','韦珥','FX-INK','四十来岁男人 · 旅馆旧仆 · 洗白围裙与腰串旧钥匙','miloer'),('moer','摩珥','FX-WIL','四十来岁男人 · 酒馆账房 · 黄指节与木账板','luomin')]:
 d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/who/'concept_v1';raw=d/f'{who}_v1_raw_imagegen.png';im=Image.open(raw).convert('RGBA');a=np.array(im);hist=np.bincount(a[:,:,3].ravel(),minlength=256);out=a.copy();out[out[:,:,3]<=8]=0;clean=Image.fromarray(out);clean.save(d/f'{who}_transparent.png')
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',28);big=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',42)
 for label,color,ink in [('light',(239,234,220,255),(40,43,43)),('dark',(32,38,43,255),(234,229,214))]:
  canvas=Image.new('RGBA',(im.width+200,im.height+300),color);canvas.alpha_composite(clean,(100,160));dr=ImageDraw.Draw(canvas);dr.text((70,40),f'{name}  {ident} | 全身外观概念',font=big,fill=ink);dr.text((70,105),note,font=font,fill=ink);dr.text((70,im.height+185),'原创概念 · 发型配色可逆 · 装备与游戏运行未验证',font=font,fill=ink);dr.text((70,im.height+235),'第十一批 · 保留完整原稿 · 待独立审查',font=font,fill=ink);canvas.convert('RGB').save(d/f'{who}_{label}_board.png')
 (d/'prepare_concept.py').write_bytes(Path(__file__).read_bytes())
 log={'generator':'builtin image_gen.imagegen','transparent_background':True,'raw_size':im.size,'alpha_zero_pixels':int(hist[0]),'alpha_1_to_8_pixels':int(sum(hist[1:9])),'alpha_9_to_254_pixels':int(sum(hist[9:255])),'alpha_255_pixels':int(hist[255]),'alpha_bbox':im.getchannel('A').getbbox(),'cleanup_changed_pixels':int(np.any(a!=out,axis=2).sum()),'alpha_above_8_unchanged':bool(np.array_equal(a[a[:,:,3]>8],out[a[:,:,3]>8])),'operations':'Only alpha<=8 RGBA zeroed; no crop, repaint, quantization, stretching. Original-size image alpha composited on Chinese boards.','revisions':0,'selected_reference':f'Assets/CharacterDesigns/20261013/expressive/new_story/{ref}/concept_v1/{ref}_transparent.png','all_style_references_actually_viewed':['Sela G','Mia 1:1.5','luomin','miloer'],'runtime_verified':False}
 (d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
 (d/'author_QA.json').write_text(json.dumps({'canonical_id':ident,'name':name,'raw_actually_viewed':True,'light_dark_board_view_pending':True,'visible_requirements':note,'revision_count':0,'status':'pending independent review','story_guard':'无代人授权、结算、免账或帮派收债声明；道具无可读名单','age_gender':'四十来岁的男人；发型脸型配色为可逆提案','runtime_verified':False},ensure_ascii=False,indent=2))
 print(who,json.dumps(log,ensure_ascii=False))
