import json,pathlib,shutil,hashlib,datetime
from PIL import Image,ImageDraw
import numpy as np
R=pathlib.Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); B=json.loads((R/'Assets/EnemyDesigns/reference/20261013/action_pilot_monsters_brief.json').read_text())
files={'low_coil':'exec-cda3a269-08dc-4a15-be6a-8a425b69a95a.png','short_claw_extend':'exec-9458504f-860a-40d1-95ea-c4df2cc7cec7.png','bar_guard':'exec-39906ad5-381d-42f7-a8e0-6aa7b8aaed4a.png','side_step_guard':'exec-5eeea992-e947-4920-9547-4ab365478f35.png'}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for c in B['characters'][2:]:
 for p in c['poses']:
  d=R/p['output_directory']; raw=R/p['planned_raw_path']; out=R/p['planned_transparent_path']; shutil.copy2(R.parent/'generated_images'/files[p['pose_id']],raw)
  im=Image.open(raw).convert('RGBA'); a=np.array(im); before=a.copy(); mask=a[:,:,3]<=8; a[mask]=0; clean=Image.fromarray(a); clean.save(out)
  board=Image.new('RGB',(im.width*2,im.height),(239,234,223));board.paste((29,33,40),(im.width,0,im.width*2,im.height));board.paste(clean,(0,0),clean);board.paste(clean,(im.width,0),clean);board.save(d/'preview_light_dark.png')
  thumb=clean.copy();thumb.thumbnail((320,320),Image.Resampling.NEAREST);thumb.save(d/'thumbnail.png')
  evidence={'alpha_threshold':8,'operation':'Set RGBA=(0,0,0,0) only where original alpha<=8. All pixels with alpha>8 unchanged. No recolor, body drawing, geometry edits or resizing of transparent output. Preview uses alpha compositing; thumbnail nearest-neighbor isotropic only.','raw_size':list(im.size),'raw_bbox_alpha_gt0':im.getbbox(),'clean_bbox_alpha_gt0':clean.getbbox(),'low_alpha_nonzero_pixels_removed':int(((before[:,:,3]>0)&mask).sum()),'hidden_rgb_pixels_cleared':int(((before[:,:,:3]!=0).any(axis=2)&mask).sum()),'preserved_foreground_exactly':bool(np.array_equal(a[~mask],before[~mask])),'alpha_zero_count':int((a[:,:,3]==0).sum()),'alpha_nonzero_count':int((a[:,:,3]>0).sum()),'alpha_max':int(a[:,:,3].max())}
  (d/'alpha_evidence.json').write_text(json.dumps(evidence,indent=2))
  qa={'status':'author_pass_pending_independent_review','actually_viewed':['static anchor','raw full image'],'hard_errors_found':[],'observations':{'low_coil':'低宽双足蹲势、屈膝加深，双爪较静态收拢且悬空。保持有意长臂；画面右爪与膝相邻但无断肢。','short_claw_extend':'画面左长臂前送、爪形展开，支撑腿与低伏明显有别；长臂比例属于怪物身份。','bar_guard':'同一短钩杆横于腰腹，两手连接可信，两端可见；钝钩未变长矛。','side_step_guard':'短杆收直斜护、两靴错步，仍朝左戒备，腰侧酒红缝线保持。'}[p['pose_id']],'budget':{'first_drafts':1,'hard_error_revisions':0,'maximum_hard_error_revisions':1},'runtimeVerified':False,'continuous_animation':False}
  (d/'author_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
  shutil.copy2('/tmp/package_mutant_warden.py',d/'prepare_artifacts.py')
  manifest={'schema_version':1,'character':c['slug'],'pose_id':p['pose_id'],'status':'author_pass_pending_independent_review','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tool':'built-in image_gen','source_anchor':c['anchor'],'output':{'path':str(out.relative_to(R)),'sha256':sha(out),'size':list(im.size)},'budget':qa['budget'],'runtimeIntegrated':False,'runtimeVerified':False,'animation_frames_produced':0,'files':[{'path':str(x.relative_to(d)),'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(d.rglob('*')) if x.is_file() and x.name!='manifest.json']}
  (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
  print(c['slug'],p['pose_id'],sha(out),clean.getbbox())
