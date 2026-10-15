from pathlib import Path
from PIL import Image
import numpy as np, shutil,json,hashlib,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');G=R.parent/'generated_images';B=json.loads((R/'Assets/EnemyDesigns/reference/20261013/action_pilot_monsters_brief.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
raws={'drag_step':'exec-6e60ccbc-1ef9-4d4a-9be5-0f6b07bee703.png','slow_reach':'exec-87b43687-2cab-4d1c-90e4-4a65e079fa51.png','forward_drift':'exec-66b7ce47-feae-4b67-a016-2e35a096b5d3.png','spectral_reach':'exec-00d209ee-9ec4-463b-a569-0651b5e236d6.png'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,a):p.write_text(json.dumps(a,ensure_ascii=False,indent=2)+'\n')
def rec(p):return {'path':str(p.relative_to(R)),'sha256':sha(p),'bytes':p.stat().st_size}
for c in B['characters'][:2]:
 root=R/'Assets/EnemyDesigns/20261013/first_six'/c['slug']/'action_v1'
 for pose in c['poses']:
  d=R/pose['output_directory'];s=d/'sources';s.mkdir(parents=True,exist_ok=True);prefix=c['slug']+'_'+pose['pose_id'];a=R/c['anchor']['path'];assert sha(a)==c['anchor']['sha256']
  for p in [a,R/c['static_independent_QA']['path'],R/'Assets/EnemyDesigns/reference/20261013/action_pilot_monsters_brief.json',R/'AGENTS.md'] :shutil.copy2(p,s/p.name)
  put(d/'source_snapshot.json',{'created_utc':now,'anchor_actually_viewed':True,'anchor_matches_brief':True,'files':[rec(p) for p in s.iterdir()]})
  raw=R/pose['planned_raw_path'];shutil.copy2(G/raws[pose['pose_id']],raw);im=Image.open(raw).convert('RGBA');arr=np.array(im);al=arr[:,:,3].copy();mask=al<=1;arr[mask,:3]=0;out=R/pose['planned_transparent_path'];Image.fromarray(arr).save(out)
  for n,col in [('light',(235,233,223,255)),('dark',(26,32,39,255))]:
   bg=Image.new('RGBA',im.size,col);bg.alpha_composite(Image.fromarray(arr));bg.save(d/(prefix+'_review_'+n+'.png'))
   bg.resize((512,768),Image.Resampling.NEAREST).save(d/(prefix+'_review_'+n+'_512.png'))
  def bbox(t):return Image.fromarray(((al>t)*255).astype('uint8')).getbbox()
  put(d/'alpha_audit.json',{'size':im.size,'mode':'RGBA','raw_sha256':sha(raw),'transparent_sha256':sha(out),'processing':'Only RGB at alpha <= 1 set to zero. Every alpha byte and all RGB above 1 retained. No body drawing, masks, alpha cutoff, rescaling, rotation or recoloring. Review composites use actual straight RGBA compositing. 512 review thumbnails use nearest-neighbor isotropic 0.5 scale.','alpha_unchanged':bool(np.array_equal(al,np.array(Image.open(out))[:,:,3])),'zero_alpha_pixels':int((al==0).sum()),'semi_transparent_pixels':int(((al>0)&(al<255)).sum()),'alpha_2_to_240_pixels':int(((al>1)&(al<=240)).sum()),'alpha_0_bbox':bbox(0),'alpha_16_bbox':bbox(16),'alpha_128_bbox':bbox(128),'hidden_rgb_cleaned_pixels':int(mask.sum())})
  put(d/'generation_record.json',{'tool':'builtin image_gen','generated_source_path':str(G/raws[pose['pose_id']]),'prompt_path':'prompt_v1.txt','reference':c['anchor'],'first_drafts':1,'hard_error_revisions':0,'generated_utc':now,'transparent_background':True,'raw_preserved':True})
 print(c['slug'],root)
