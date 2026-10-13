from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
BASE=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive')
brief=json.loads((BASE/'briefs/sena_kaem_expressions_v1_brief.json').read_text())
F=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
labels={'sena':['审慎立界','难过但不免责','收住代述，认真听'],'kaem':['自负辩解','核验下紧张','克制停嘴，让来源人说']}
notes={'sena':['非对称追问眉 · 窄发话口形','内眉上提 · 下视闭唇','舒眉开眼 · 平视放松唇'],'kaem':['斜压眉 · 横向反驳口形','忧眉睁眼 · 短小停顿口形','较平缓眉 · 压住插话的闭唇']}
# Hand-inspected head crown-to-chin landmarks for UNIFORM board scale only. Never warp anatomy.
landmarks={'sena':[(83,859),(72,865),(91,804)],'kaem':[(80,900),(120,894),(30,824)]}
for slug,c in zip(['sena','kaem'],brief['characters']):
 out=BASE/slug/'expressions_v1';shutil.copy2(__file__,out/'build_review.py');ims=[];stats=[]
 for p in sorted((out/'raw').glob('*.png')):
  im=Image.open(p).convert('RGBA');a=np.array(im);mask=a[:,:,3]<32;n=int(np.sum((a[:,:,3]>0)&mask));a[mask]=0
  clean=Image.fromarray(a); q=out/'selected'/p.name.replace('_raw_imagegen','_transparent');clean.save(q);ims.append(clean)
  stats.append({'raw':str(p.relative_to(out)),'selected':str(q.relative_to(out)),'dimensions':list(im.size),'raw_sha256':sha(p),'selected_sha256':sha(q),'cleanup':'RGBA cleared only where source alpha <32; other pixels unchanged','nonzero_alpha_pixels_cleared':n,'preserved_pixels_exact':bool(np.array_equal(a[~mask],np.array(im)[~mask]))})
 for theme,bg,fg in [('light','#eee8dc','#302b29'),('dark','#202630','#eee8dc')]:
  board=Image.new('RGB',(1800,900),bg);d=ImageDraw.Draw(board)
  d.text((30,20),f"{c['name']} · 三态表情设定",font=F(34),fill=fg)
  d.text((30,70),'独立条件场景｜同一人物与衣装｜五官表演研究，未接入游戏',font=F(23),fill=fg)
  for i,im in enumerate(ims):
   crown,chin=landmarks[slug][i];scale=340/(chin-crown);box=im.getbbox();crop=im.crop(box);sz=(round(crop.width*scale),round(crop.height*scale));thumb=crop.resize(sz,Image.Resampling.NEAREST)
   x=i*600+(600-sz[0])//2;y=125;board.paste(thumb,(x,y),thumb)
   d.text((i*600+30,730),f"E{i+1}  {labels[slug][i]}",font=F(27),fill=fg)
   d.text((i*600+30,775),notes[slug][i],font=F(22),fill=fg)
  d.text((30,850),'不是连续悔改或结案；存活、在场、愿谈、核验与本人授权仍以台本为准。',font=F(23),fill=fg)
  board.save(out/'review'/f'{slug}_expressions_review_zh_{theme}.png')
 qa={'character':slug,'status':'author_review_complete_pending_independent','raw_actually_viewed':True,'transparent_board_actually_viewed':False,'revision_count':0,'identity':'anchor face, hair, skin and medieval collar retained','expression_notes':notes[slug],'limitations':['Generated bust crop, head angle and scarf folds vary modestly; board scale uniformly normalizes head height, does not warp anatomy.','Conditional expressions are concept studies, not an animation or story outcome.']+(['Sena E1 mouth is more finely rendered than surrounding coarse clusters.'] if slug=='sena' else []),'processing':stats,'board_processing':'Manual crown/chin measurements; uniform nearest-neighbor per-image scale to 340px head height; alpha bounding-box crop only; native selected images unscaled.','landmarks_crown_chin_y':landmarks[slug]}
 (out/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 (out/'README.md').write_text(f"# {c['name']} 表情设定\n\n三幅胸像均由内置 imagegen 逐幅生成。sources 保存原始身份锚、人物卡、条件台本与原字节 brief。raw 完整保留生成原稿；selected 仅将 alpha 小于32的像素清零，其余像素不变。review 为统一头高、等比最近邻缩放的中文浅深板，未拉伸或脚本绘脸。\n\n这是独立条件分支的表演素材，不是连续悔改、永久成长或结案证明。未接入游戏，未改 roster。独审结果以 QA-independent.json 为准。\n")
 manifest={'schema_version':1,'character':slug,'canonical_id':c['canonical_id'],'aliases':c['aliases'],'generator':'built-in image_gen.imagegen','source_anchor':c['anchor'],'brief_sha256':sha(out/'sources/brief.json'),'expressions':c['expressions'],'runtime_integrated':False,'roster_changed':False,'independent_review':'pending','files':[]}
 for p in sorted(out.rglob('*')):
  if p.is_file() and p.name!='manifest.json':manifest['files'].append({'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)})
 (out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 print(out)
