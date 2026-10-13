from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,hashlib,shutil
B=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod/Assets/CharacterDesigns/20261013/expressive');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();brief=json.loads((B/'briefs/next_main_cast_expressions_nara_ena_01.json').read_text());font=lambda n:ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',n)
# Coordinates manually observed on native 1254 square raw images. Used for uniform whole-image board scale only.
landmarks={'nara':[(60,860),(57,877),(49,824)],'ena':[(58,844),(75,818),(95,766)]}
notes={'nara':['不对称压眉 · 窄眼侧看 · 闭唇','内眉上提 · 倦眼低视 · 短横气口','平眉申明 · 直视 · 横向开口'],'ena':['非对称问眉 · 斜视 · 问话开口','内眉上扬 · 侧看 · 内收闭唇','舒平眉 · 稳视 · 平角发言']}
for c in brief['characters']:
 slug=c['slug'];o=B/slug/'expressions_v1';shutil.copy2(__file__,o/'build_review.py');ims=[];stats=[];trans=[]
 for i,p in enumerate(sorted((o/'raw').glob('*.png'))):
  im=Image.open(p).convert('RGBA');a=np.array(im);mask=a[:,:,3]<32;n=int(np.sum((a[:,:,3]>0)&mask));a[mask]=0;clean=Image.fromarray(a);q=o/'selected'/p.name.replace('_raw_imagegen','_transparent');clean.save(q);ims.append(clean)
  stats.append({'raw':str(p.relative_to(o)),'selected':str(q.relative_to(o)),'dimensions':list(im.size),'raw_sha256':sha(p),'selected_sha256':sha(q),'cleanup':'Set RGBA to zero only where source alpha <32; all other pixels exact','nonzero_alpha_pixels_cleared':n,'preserved_pixels_exact':bool(np.array_equal(a[~mask],np.array(im)[~mask]))})
 for theme,bg,fg in [('light','#eee8dc','#302b29'),('dark','#202630','#eee8dc')]:
  board=Image.new('RGB',(1800,920),bg);d=ImageDraw.Draw(board);d.text((30,20),f"{c['name']} {c['english_name']} · 三态表情设定",font=font(34),fill=fg);d.text((30,75),'同一成人身份锚｜眉眼与口型独立可读｜条件表演素材，尚未接入游戏',font=font(23),fill=fg)
  for i,im in enumerate(ims):
   crown,chin=landmarks[slug][i];scale=365/(chin-crown);box=im.getbbox();crop=im.crop(box);sz=(round(crop.width*scale),round(crop.height*scale));thumb=crop.resize(sz,Image.Resampling.NEAREST);x=i*600+(600-sz[0])//2;y=140;board.paste(thumb,(x,y),thumb)
   if theme=='light':trans.append({'index':i+1,'source_alpha_bbox':list(box),'head_crown_chin_y':[crown,chin],'uniform_scale_requested':scale,'destination_size':list(sz),'destination_xy':[x,y],'resample':'NEAREST','rounding':'round whole-image dimensions independently to integer; no local warping','selected_native_unscaled':True})
   d.text((i*600+30,755),f"E{i+1}  {c['expressions'][i]['label']}",font=font(27),fill=fg);d.text((i*600+30,800),notes[slug][i],font=font(21),fill=fg)
  d.text((30,870),'不代表伤愈、丧偶、赔付、公开住址或本人同意；使用时仍须核对台本条件。',font=font(23),fill=fg);board.save(o/'review'/f'{slug}_expressions_review_zh_{theme}.png')
 qa={'character':slug,'status':'author_review_complete_pending_final_independent','raw_actually_viewed':True,'transparent_board_actually_viewed':False,'revision_count':0,'expression_notes':notes[slug],'limitations':['Head pose, hair clusters and collar folds vary modestly; not a locked animation sprite sheet.','Expression depicts no completed branch, no new injury and no consent.']+(['E2 mouth is a short horizontal breathing gap, not the planned vertical aperture. E3 hair/collar has minor drift.'] if slug=='nara' else ['E1 inner eyebrows retain concern; E3 has a little brown coat at lower edge unlike E1/E2. Pending independent judgment.']),'processing':stats,'board_transforms':trans}
 (o/'QA-author.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2));(o/'README.md').write_text(f"# {c['name']} 胸像表情设定\n\n逐张内置imagegen生成，保留raw、提示词、原始v2身份锚、卡与台本和brief。selected仅清零原alpha<32区域，其余逐像素保留。中文浅深板只使用全图等比最近邻缩放与透明边界裁切；没有脚本绘脸或局部拉伸。\n\n六态属于独立条件表演，不是顺序剧情或结果。Nara仍是伤腿坐姿身份；Ena仅指NPC-N-ENA，与冷窗驿同名者分人。未改roster或游戏内容。当前最终独审待完成，详见QA文件。\n")
 manifest={'schema_version':1,'character':slug,'canonical_id':c['canonical_id'],'generator':'built-in image_gen.imagegen','source_anchor':c['anchor'],'brief_sha256':sha(o/'sources/brief.json'),'expressions':c['expressions'],'runtime_integrated':False,'roster_changed':False,'independent_review':'pending','files':[]}
 for p in sorted(o.rglob('*')):
  if p.is_file() and p.name!='manifest.json':manifest['files'].append({'path':str(p.relative_to(o)),'bytes':p.stat().st_size,'sha256':sha(p)})
 (o/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(slug,[(Image.open(p).size,p.stat().st_size) for p in sorted((o/'raw').glob('*.png'))])
