import pathlib,json,hashlib,shutil
import numpy as np
from PIL import Image
R=pathlib.Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); d=R/'Assets/EnemyDesigns/20261013/first_six/blood_hunger_mutant/action_v1/short_claw_extend/revision_v2'; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
raw=d/'blood_hunger_mutant_short_claw_extend_raw_imagegen_v2.png';out=d/'blood_hunger_mutant_short_claw_extend_transparent_v2.png';shutil.copy2(R.parent/'generated_images/exec-fb3d7363-f8de-4b9c-b49e-c37ba6b12c52.png',raw)
im=Image.open(raw).convert('RGBA');a=np.array(im);before=a.copy();mask=a[:,:,3]<=8;a[mask]=0;clean=Image.fromarray(a);clean.save(out)
board=Image.new('RGB',(im.width*2,im.height),(239,234,223));board.paste((29,33,40),(im.width,0,im.width*2,im.height));board.paste(clean,(0,0),clean);board.paste(clean,(im.width,0),clean);board.save(d/'preview_light_dark.png')
thumb=clean.copy();thumb.thumbnail((320,320),Image.Resampling.NEAREST);thumb.save(d/'thumbnail.png')
evidence={'alpha_threshold':8,'operation':'Only original alpha<=8 set RGBA to zero; alpha>8 pixels unchanged. No geometry/body edit.','size':im.size,'raw_bbox':im.getbbox(),'clean_bbox':clean.getbbox(),'preserved_foreground_exactly':bool(np.array_equal(a[~mask],before[~mask])),'low_alpha_nonzero_pixels_removed':int(((before[:,:,3]>0)&mask).sum()),'edge_alpha_max':{'top':int(a[0,:,3].max()),'bottom':int(a[-1,:,3].max()),'left':int(a[:,0,3].max()),'right':int(a[:,-1,3].max())},'alpha_zero_count':int((a[:,:,3]==0).sum())}
(d/'alpha_evidence.json').write_text(json.dumps(evidence,indent=2))
(d/'author_QA.json').write_text(json.dumps({'status':'author_pass_pending_independent_review','hard_error_revised':'v1 right claw outer edge clipped at right border: 41 pixels with alpha>8 (max250). v2 expands framing, all tips now present.','actually_viewed':['v2 raw'],'budget':{'first_drafts':1,'hard_error_revisions':1,'max_revisions':1},'runtimeVerified':False},ensure_ascii=False,indent=2))
(d/'source_snapshot.json').write_text(json.dumps({'immutable_anchor':{'path':str(d.parent/'sources/blood_hunger_mutant_idle_transparent.png'),'sha256':sha(d.parent/'sources/blood_hunger_mutant_idle_transparent.png')},'edit_target_v1':{'path':str(d.parent/'blood_hunger_mutant_short_claw_extend_raw_imagegen.png'),'sha256':sha(d.parent/'blood_hunger_mutant_short_claw_extend_raw_imagegen.png')}},indent=2))
shutil.copy2('/tmp/prepare_mutant_revision.py',d/'prepare_revision.py')
(d/'manifest.json').write_text(json.dumps({'status':'author_pass_pending_independent_review','tool':'built-in image_gen','first_drafts':1,'hard_error_revisions':1,'output':{'path':str(out.relative_to(R)),'sha256':sha(out),'size':im.size},'files':[{'path':str(x.relative_to(d)),'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(d.rglob('*')) if x.is_file() and x.name!='manifest.json']},indent=2))
print(sha(out),evidence)
