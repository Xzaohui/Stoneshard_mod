from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,datetime
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
base=root/'Assets/EnemyDesigns/20261013/first_six/canal_club_brigand/action_v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sources=[{'path':str(p.relative_to(root)), 'sha256':sha(p)} for p in sorted((base/'sources').iterdir())]
dump(base/'source_snapshot_manifest.json',{'frozen':True,'files':sources,'generation_authorized_by':'Parent task explicitly started 002 two poses; source brief not_started fields are historical snapshot.','anchor_verified_sha256':'9683b1a41ba261800702c45617ed6fd2b737b54caf24a1c89010d3f5ce81cceb','anchor_viewed_utc':'2026-10-13T19:23:51Z','references_used_for_generation':['sources/canal_club_brigand_transparent.png']})
for pose in ['club_compact_ready','club_controlled_recover']:
 d=base/pose;prefix='canal_club_brigand_'+pose
 raw=d/(prefix+'_raw_imagegen.png');im=Image.open(raw).convert('RGBA');a=np.array(im);mask=a[:,:,3]<=3; changed=((a!=0).any(axis=2)&mask).sum();a[mask]=0
 out=Image.fromarray(a);tp=d/(prefix+'_transparent.png');out.save(tp)
 for name,c in [('light',(234,230,219,255)),('dark',(32,37,43,255))]:
  bg=Image.new('RGBA',im.size,c);bg.alpha_composite(out);bg.convert('RGB').save(d/(prefix+'_review_'+name+'.png'))
 stats={'raw_size':list(im.size),'raw_alpha_bbox':list(im.getchannel('A').getbbox()),'transparent_size':list(out.size),'transparent_alpha_bbox':list(out.getchannel('A').getbbox()),'zero_alpha_pixels':int((a[:,:,3]==0).sum()),'partial_alpha_pixels':int(((a[:,:,3]>0)&(a[:,:,3]<255)).sum()),'edge_alpha_max':{'top':int(a[0,:,3].max()),'bottom':int(a[-1,:,3].max()),'left':int(a[:,0,3].max()),'right':int(a[:,-1,3].max())},'cleanup':'Only RGBA zeroing where original alpha <= 3; alpha > 3 unchanged. No body painting, limb compositing, scaling, cropping or mirroring.','cleanup_changed_pixels':int(changed),'raw_sha256':sha(raw),'transparent_sha256':sha(tp)}
 dump(d/'alpha_audit.json',stats)
 dump(d/'generation_record.json',{'tool':'builtin image_gen.imagegen','use_case':'identity-preserve','transparent_background':True,'referenced_image_paths':['Assets/EnemyDesigns/20261013/first_six/canal_club_brigand/idle_v1/canal_club_brigand_transparent.png'],'reference_sha256':'9683b1a41ba261800702c45617ed6fd2b737b54caf24a1c89010d3f5ce81cceb','prompt_file':'prompt.txt','first_drafts':1,'hard_error_revisions':0,'generated_original_path':'/workspace/scratch/5ed8df2c5d81/generated_images/'+('exec-86650e08-0173-4d73-8f24-630d067fd19f.png' if pose=='club_compact_ready' else 'exec-50cb88eb-25fa-492b-a083-64015ae9db2e.png'),'output_sha256':sha(raw)})
print('Prepared',base)
