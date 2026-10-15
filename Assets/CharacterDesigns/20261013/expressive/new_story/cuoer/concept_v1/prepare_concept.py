from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
for slug,name,ident,desc in [('erde','珥德','FX-MIN','矿洞捡拾者 · 五十来岁'),('cuoer','锉珥','FX-MN2','矿车修理工 · 四十来岁')]:
 d=R/'Assets/CharacterDesigns/20261013/expressive/new_story'/slug/'concept_v1'
 im=Image.open(d/f'{slug}_v2_raw_imagegen.png').convert('RGBA'); arr=np.array(im); mask=arr[:,:,3]<=8;changed=int(mask.sum());arr[mask]=0;clean=Image.fromarray(arr);clean.save(d/f'{slug}_transparent.png')
 font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';title=ImageFont.truetype(font,38);body=ImageFont.truetype(font,23)
 scale=min(860/clean.width,1260/clean.height);scaled=clean.resize((round(clean.width*scale),round(clean.height*scale)),Image.Resampling.NEAREST)
 for theme,bg,fg in [('light',(238,230,212,255),(51,43,34)),('dark',(33,37,45,255),(232,224,208))]:
  board=Image.new('RGBA',(1000,1500),bg);draw=ImageDraw.Draw(board);draw.text((44,24),f'{name}  |  {ident}',font=title,fill=fg);draw.text((44,78),desc+' · 原创全身概念',font=body,fill=fg);board.alpha_composite(scaled,((1000-scaled.width)//2,120));draw.text((44,1430),'外观与衣装提案 · 非游戏运行/装备兼容验收',font=body,fill=fg);board.convert('RGB').save(d/f'{slug}_{theme}_board.png')
 qa={'status':'author_visual_checked_pending_independent_review','selected_raw':f'{slug}_v2_raw_imagegen.png','generation':'builtin image_gen true transparency; one initial and one hard-error revision','raw_actually_viewed':['v1','v2'],'identity_and_props':'成年男性身份、各自脸型与必需道具可读；双手双脚完整。','revision_reason':'v1像素过细，v2改为粗像素；锉珥raw晕影曾被误判为背景，经RGBA检测纠正为alpha=0隐藏RGB。','postprocess':'Only pixels alpha<=8 zeroed RGBA. Other pixels bit-for-bit unchanged. Full original canvas retained; board nearest aspect-fit only. No body drawing, crop, quantization, flood-fill or background removal.','alpha_zero_before':int((np.array(im)[:,:,3]==0).sum()),'alpha_le8_cleared':changed,'opaque_or_near_opaque':int((arr[:,:,3]>=245).sum()),'scope_limit':'Concept only. No runtime, equipment, body-part or animation compatibility verified.'}
 (d/'author_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 log={'raw_versions':[{'file':f'{slug}_v1_raw_imagegen.png','selected':False},{'file':f'{slug}_v2_raw_imagegen.png','selected':True}],'tool':'image_gen.imagegen','transparent_background':True,'reference_inputs_v2':[f'{slug}_v1_raw_imagegen.png','deru_v2_raw_imagegen.png']+(['mia_ratio_1_to_1_5_v2_raw_imagegen.png'] if slug=='erde' else []),'postprocess':'prepare_concept.py','independent_review':'pending frozen manifest review'}
 (d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2))
 shutil.copy2(__file__,d/'prepare_concept.py')
 print(slug,'prepared',clean.size)
