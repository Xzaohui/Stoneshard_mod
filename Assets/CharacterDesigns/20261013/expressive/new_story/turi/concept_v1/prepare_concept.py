from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=r/'Assets/CharacterDesigns/20261013/expressive/new_story'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for who,name,role in [('turi','图里','有限班机械检查匠'),('vila','维菈','普通支架匠 · 中性外观提案')]:
 d=base/who/'concept_v1';raw=d/f'{who}_v2_raw_imagegen.png'; im=Image.open(raw).convert('RGBA');a=im.getchannel('A');n=sum(a.histogram()[1:9]);im.putalpha(a.point(lambda x:0 if x<=8 else x));im.save(d/f'{who}_transparent.png')
 for mode,bg,fg in [('light',(237,232,216,255),(37,37,32,255)),('dark',(32,37,40,255),(236,230,213,255))]:
  board=Image.new('RGBA',(im.width+160,im.height+240),bg);board.alpha_composite(im,(80,140));dr=ImageDraw.Draw(board);font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';dr.text((55,30),name+'｜'+role,font=ImageFont.truetype(font,34),fill=fg);dr.text((55,90),'原创人物全身概念 · 非游戏运行验收',font=ImageFont.truetype(font,23),fill=fg);dr.text((55,im.height+170),'低魔中世纪 · 成熟表情 · 粗像素簇',font=ImageFont.truetype(font,22),fill=fg);board.convert('RGB').save(d/f'{who}_{mode}_board.png')
 shutil.copy2(__file__,d/'prepare_concept.py')
 log={'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'generator':'built-in image_gen.imagegen','transparent_background':True,'selected_raw':raw.name,'raw_sha256':sha(raw),'size':im.size,'operation':'Only alpha values <=8 zeroed. RGB and alpha>8 unchanged. Full image composited at native size with margins and Chinese labels. No crop, body/face drawing, resampling, palette quantization, or local edits.','alpha_1_to_8_cleared_pixels':n,'runtime_verified':False,'equipment_compatibility':'unknown','vila_note':'raw viewer may show hidden RGB halo; alpha-composited boards are authoritative for actual transparency' if who=='vila' else None}
 (d/'production_log.json').write_text(json.dumps(log,ensure_ascii=False,indent=2)+'\n')
 qa={'author_viewed_raw_versions':[1,2],'selected_version':2,'status':'awaiting final independent export review','v1_rejected_reason':'Fine-grained long-body style' if who=='turi' else 'Fine-grained style and raw-viewer visible halo; v2 coarse correction; transparency assessed through actual RGBA compositing','v2_author_checks':['Full body and complete hands/feet','Adult expressive distinct face','Required tools visible','No fictional story completion or payment','Coarse organized pixel clusters','Actual alpha-composited isolated silhouette'], 'source_limitations':['Concept only; no runtime or equipment validation']+(['Gender unspecified in canon; neutral appearance reversible','Exact bracket engineering dimensions unverified'] if who=='vila' else [])}
 (d/'author_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
 files=[{'path':str(p.relative_to(d)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(d.rglob('*')) if p.is_file() and p.name not in ['manifest.json','independent_QA.json','FINAL_STATUS.json']]
 manifest={'schema_version':1,'canonical_id':'HIG-NPC-'+who.upper(),'name':name,'selected_raw':raw.name,'transparent':f'{who}_transparent.png','status':'frozen candidate; independent review recorded separately','runtime_verified':False,'files':files}
 (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(who,sha(d/'manifest.json'))
