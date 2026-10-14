from pathlib import Path
import json,hashlib,datetime
from PIL import Image
import numpy as np
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
configs=[('luoer_qiner',r/'Assets/CharacterActions/20261013/new_story/luoer_qiner_noncombat_basics_v1_delivery/珞珥_芩珥_母图动作浅深对照.png','board_layout.json'),('lier_huier',r/'Assets/CharacterActions/20261013/new_story/lier/noncombat_basics_v1/review/栎珥_洄珥_母图动作浅深对照.png','joint_board_layout.json')]
for group,p,layout in configs:
 l=p.with_name(layout);j=json.loads(l.read_text());im=Image.open(p).convert('RGBA');cells=[]
 for row in j.get('source_images',j.get('cells')):
  f=row.get('file',row.get('image'))
  if f is None:cells.append({'status':'explicit_missing_no_image','row':row['row'],'column':row['column']});continue
  source=r/f; src=Image.open(source).convert('RGBA');wh=row.get('resize_size',row.get('display_size'));xy=row.get('position',[row.get('x'),row.get('y')]);act=im.crop((xy[0],xy[1],xy[0]+wh[0],xy[1]+wh[1]));bg=tuple(row.get('background',act.getpixel((0,0))));res=src.resize(tuple(wh),Image.Resampling.NEAREST);expected=Image.alpha_composite(Image.new('RGBA',tuple(wh),bg),res)
  checks={'source_sha_matches':sha(source)==row.get('sha256',row.get('source_sha256')),'full_source_dimensions_match':list(src.size)==row['source_size'],'whole_image_nearest_alpha_pixels_match':bool(np.array_equal(np.array(expected),np.array(act))),'uniform_aspect_with_integer_rounding':abs(wh[0]/src.width-wh[1]/src.height)<1/min(src.size)};assert all(checks.values()),(group,f,checks)
  cells.append({'source':f,'position':xy,'display_size':wh,'background':bg,'checks':checks})
 out={'schema_version':1,'reviewer':'review_seventh_character_actions','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'verdict':'pass','board':{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p),'size':list(im.size)},'layout':{'path':str(l.relative_to(r)),'sha256':sha(l)},'actual_visual_viewed':True,'cells':cells,'visual_findings':['Chinese labels readable, full silhouettes and props visible on true light and dark backgrounds.','Mother references clearly identified and not counted as new poses.','Only selected passing attempts displayed; no failed attempts represented as passing poses.','Lier A1 is explicitly missing with text-only cells; no third attempt or substitute pose.' if group=='lier_huier' else 'Four passing action poses plus two mother references shown in both themes.'],'scope':'Presentation-board review only; full-source archive closure remains pending.'}
 dest=a/f'independent_seventh_new_character_actions_{group}_board_gate_20261014.json';dest.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(group,str(dest.relative_to(r)),sha(dest),len(cells))
