from PIL import Image,ImageDraw,ImageFont
import numpy as np,json,pathlib,hashlib,shutil
r=pathlib.Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');b=r/'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief_v2.json';x=json.loads(b.read_text())
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for c in x['characters'][-2:]:
 for p in c['poses']:
  d=r/p['output_directory'];raw=r/p['planned_raw_path'];out=r/p['planned_transparent_path']
  im=Image.open(raw).convert('RGBA');a=np.array(im);count=int((a[:,:,3]<32).sum());a[a[:,:,3]<32]=0;im=Image.fromarray(a);im.save(out)
  for name,col in [('light',(239,235,225,255)),('dark',(30,34,40,255))]:
   bg=Image.new('RGBA',im.size,col);bg.alpha_composite(im);bg.convert('RGB').save(d/f'review_{name}.png')
  sm=im.copy();sm.thumbnail((240,300),Image.Resampling.NEAREST);bg=Image.new('RGBA',(480,330),(239,235,225,255));bg.paste(Image.new('RGBA',(240,330),(30,34,40,255)),(240,0));bg.alpha_composite(sm,((240-sm.width)//2,15));bg.alpha_composite(sm,(240+(240-sm.width)//2,15));bg.convert('RGB').save(d/'review_small.png')
  manifest={'concept_id':c['concept_id'],'pose_id':p['pose_id'],'label':p['label'],'status':'candidate_pending_independent_review','tool':'builtin image_gen.imagegen','first_drafts':1,'hard_error_revisions_used':0,'source':c['anchor'],'source_sha_verified':h(r/c['anchor']['path']),'source_actually_viewed_utc':'2026-10-13T20:16:46Z','raw':{'path':str(raw.relative_to(r)),'sha256':h(raw)},'candidate':{'path':str(out.relative_to(r)),'sha256':h(out),'size':list(im.size),'alpha_bbox':list(im.getbbox()),'alpha_extrema':list(im.getchannel('A').getextrema())},'prompt':{'path':str((d/'prompt_v1.txt').relative_to(r)),'sha256':h(d/'prompt_v1.txt')},'processing':'Only alpha <32 set to zero with hidden RGB cleared at these pixels; all other RGBA unchanged. No body redraw, warp, crop, or rescale in selected. Review_small uses nearest proportional layout.','runtimeIntegrated':False,'runtimeVerified':False,'animation_frames_produced':0}
  (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
