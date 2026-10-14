from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,numpy as np
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');b=R/'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief_v2.json';B=json.loads(b.read_text());SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',24)
for c in B['characters'][:1]:
 for p in c['poses']:
  d=R/p['output_directory'];raw=R/p['planned_raw_path'];dst=R/p['planned_transparent_path']
  if (d/'FINAL_STATUS.json').exists():
   print('Final status present; refusing to regenerate review records:',d);continue
  if not raw.exists():continue
  a=np.array(Image.open(raw).convert('RGBA'));v=a.copy();v[a[:,:,3]<=8]=0;im=Image.fromarray(v);im.save(dst)
  qa={'size':list(im.size),'bbox':im.getbbox(),'sha256':SHA(dst),'raw_sha256':SHA(raw),'alpha_zero':int((v[:,:,3]==0).sum()),'alpha_full':int((v[:,:,3]==255).sum()),'alpha_partial':int(((v[:,:,3]>0)&(v[:,:,3]<255)).sum()),'raw_alpha_1_to_8_cleared':int(((a[:,:,3]>0)&(a[:,:,3]<=8)).sum()),'visible_gt8_unchanged':bool(np.array_equal(a[a[:,:,3]>8],v[a[:,:,3]>8])),'processing':'仅将alpha<=8清零并同步隐藏RGB清零。无重绘、裁切、量化或主体缩放。','author_visual':'原始图实际view通过；同脸衣物和武器握持、支撑与姿势核心可读。待独审。'}
  (d/'alpha_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
  for mode,bg,fg in [('light',(235,230,216),(35,35,35)),('dark',(26,32,40),(240,237,226))]:
   board=Image.new('RGB',(1200,900),bg);dr=ImageDraw.Draw(board);dr.text((25,18),c['working_name']+'｜'+p['label']+'｜首稿待独审',font=f,fill=fg)
   for path,x,w,label in [(R/c['anchor']['path'],0,400,'静态母图'),(dst,400,550,'动作候选'),(dst,970,200,'缩小检查')]:
    it=Image.open(path).convert('RGBA');scale=min(w/it.width,(700 if w>200 else 280)/it.height);it=it.resize((round(it.width*scale),round(it.height*scale)),Image.Resampling.NEAREST);board.paste(it,(x+(w-it.width)//2,100+(700-it.height)),it);dr.text((x+15,65),label,font=f,fill=fg)
   dr.text((25,850),'独立关键姿势概念；非连续动画、绑定或游戏运行验收。',font=f,fill=fg);board.save(d/f'review_{mode}.png')
  man={'concept_id':c['concept_id'],'pose_id':p['pose_id'],'status':'candidate_waiting_independent_review','anchor':c['anchor'],'brief_path':str(b.relative_to(R)),'brief_sha256':SHA(b),'generator':'builtin image_gen','prompt':'prompt.txt','raw':raw.name,'transparent':dst.name,'first_drafts':1,'hard_error_revisions_used':0,'max_hard_error_revisions':1,'runtimeIntegrated':False,'runtimeVerified':False,'alpha_qa':qa,'files':{x.name:SHA(x) for x in d.iterdir() if x.is_file() and x.name!='manifest.json'}};(d/'manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=2))
