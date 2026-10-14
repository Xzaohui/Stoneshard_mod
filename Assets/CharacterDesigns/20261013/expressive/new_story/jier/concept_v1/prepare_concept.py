from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import hashlib,json,datetime,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=r/'Assets/CharacterDesigns/20261013/expressive/new_story';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for s,name,ident,note in [('jier','蓟珥','FX-FRM','五十来岁农宅住户 · 卷袖与土指 · 寡言侧目'),('suier_lot','绥珥','FX-LOT','四十来岁裁缝亲属 · 紧结围巾与半截软布尺')]:
 d=base/s/'concept_v1';raw=d/f'{s}_v1_raw_imagegen.png';im=Image.open(raw).convert('RGBA');hist=im.getchannel('A').histogram();orig=im.copy();px=im.load();changed=0
 for y in range(im.height):
  for x in range(im.width):
   a=px[x,y][3]
   if a<=8:
    changed+=px[x,y]!=(0,0,0,0);px[x,y]=(0,0,0,0)
 im.save(d/f'{s}_transparent.png')
 font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',29);big=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',42)
 for label,bg,ink in [('light',(239,234,220,255),(40,43,43)),('dark',(32,38,43,255),(234,229,214))]:
  cv=Image.new('RGBA',(im.width+200,im.height+300),bg);cv.alpha_composite(im,(100,160));dr=ImageDraw.Draw(cv);dr.text((65,35),f'{name} {ident}｜全身外观概念',font=big,fill=ink);dr.text((65,100),note,font=font,fill=ink);dr.text((65,im.height+185),'第十批 · 原创外观提案 · 待独立审查',font=font,fill=ink);dr.text((65,im.height+235),'发型配色可逆 · 装备兼容与游戏运行未验证',font=font,fill=ink);cv.convert('RGB').save(d/f'{s}_{label}_board.png')
 log={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'canonical_id':ident,'generator':'built-in image_gen.imagegen','transparent_background':True,'selected_raw':raw.name,'raw_sha256':sha(raw),'raw_size':im.size,'alpha_zero_pixels':hist[0],'alpha_1_to_8_pixels':sum(hist[1:9]),'alpha_9_to_254_pixels':sum(hist[9:255]),'alpha_255_pixels':hist[255],'alpha_bbox':orig.getchannel('A').getbbox(),'cleanup_changed_pixels':changed,'operation':'Only pixels with alpha<=8 zeroed; all pixels alpha>8 unchanged. No crop or scaling, no quantization, no drawing on character; proper RGBA composite on full-size light and dark Chinese boards.','revision_count':0,'runtime_verified':False,'status':'pending independent review'}
 (d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2));shutil.copy2(__file__,d/'prepare_concept.py')
 qa={'canonical_id':ident,'name':name,'raw_viewed':True,'references_viewed':['Sela G','Mia 1:1.5 v2','Luomin transparent','Miloer transparent'],'full_body':'头、双手、双脚完整；紧凑粗像素簇，未缩放伪造比例','source_match':note,'identity_guard':'绥珥FX-LOT，独立于燧珥FX-CP1' if s=='suier_lot' else '蓟珥FX-FRM独立原始身份','limitations':['发型、配色和未设定衣装为可逆美术提案','小尺度手指泥土不宣称逐甲缝复原' if s=='jier' else '成熟年龄通过眉眼与轮廓呈现，不依赖夸张皱纹','概念不证明游戏体型、装备槽、原帧或运行通过'],'needs_hard_error_revision':False,'revision_count':0,'independent_review':'pending','alpha_cleanup_policy':'仅alpha≤8/隐藏RGB清理，未脚本绘人物'}
 (d/'author_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));print(s,json.dumps(log,ensure_ascii=False))
