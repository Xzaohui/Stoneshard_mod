from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib,subprocess,sys
p=Path(__file__).parent;r=p.parents[3]
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
f=p/'hase_native_v1.png';before=sha(f);subprocess.run([sys.executable,str(p/'build_native.py')],check=True);assert sha(f)==before
im=Image.open(f);a=np.array(im);alpha=a[:,:,3];mask=alpha>0
seen=set();components=[]
for y,x in zip(*np.where(mask)):
 if (x,y) in seen:continue
 q=[(x,y)];seen.add((x,y));n=0
 while q:
  xx,yy=q.pop();n+=1
  for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
   z=(xx+dx,yy+dy)
   if 0<=z[0]<35 and 0<=z[1]<44 and mask[z[1],z[0]] and z not in seen:seen.add(z);q.append(z)
 components.append(n)
qa={'schema_version':1,'character':'BRY-NPC-HASE','status':'single_pose_structural_study_not_production_accepted','technical':{'canvas':list(im.size),'visible_bbox_exclusive':list(im.getbbox()),'visible_height':34,'alpha_values':list(map(int,np.unique(alpha))),'opaque_colors':len(np.unique(a[mask,:3],axis=0)),'opaque_components_4_connected':sorted(components,reverse=True),'reproducible_native_sha256':before,'rebuild_byte_identical':True},'landmarks':{'convention':'zero-based inclusive rows; head includes crown, excludes trailing beard','crown_y':4,'inferred_anatomical_chin_y':[19,20],'chin_estimate_uncertainty':'Jaw is covered by short beard; inferred interval rather than visible skin contour. Do not treat beard end as chin.','beard_last_y':22,'sole_y':37,'head_rows_range':[16,17],'remaining_body_rows_range':[17,18],'body_per_head_range':[1.0,1.125],'cranium_width_estimate_px':[15,16],'free_neck_rows_estimate':[0,1]},'actual_visual_review':{'viewed':['concept_v1_unapproved.png','hase_native_v1_16x.png','hase_native_v1_8x.png','hase_old_native_originals_comparison.png','hase_native_landmarks_20x.png'],'findings':['Head/remaining-body mass is near 1:1, unlike tall prior illustration. Broad crown and neck nested in shoulders.','Two separate dark eye pixels, nose skin highlight and beard retained.','Olive garment is compact with simple neckline, no lapels or waistcoat chain.','One brown cross-body satchel with flap/clasp; one capped amber bottle with pale label and separate skin hold.','Nearest mapping alone was insufficient: explicit 221 pixel edits merge cloth/hair and restore face, hand/bottle.','Remaining limitation: stylized face is simplified; beard hides exact anatomical chin and reduced bottle needs user artistic review.']},'semantic_constraints':['Adult commercial medicinal-goods agent, not original pharmacist replacement','No diagnosis, healing efficacy, agreement or payment depicted','Taori source retained unchanged'],'not_verified':['local installation sprite match','all directions and animation','engine pivot/collision','in-game readability','final aesthetic acceptance'],'native_production_pass':False,'style_pass':False}
(p/'qa.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n')
old=json.loads((p/'draft_manifest.json').read_text());old.update(status=qa['status'],reason='Resumed after new near-1:1 landmark review; concept v1 retained unapproved as generated source.',method='Builtin structural generation with native-only reference input, followed by authorized deterministic Pillow/NumPy pixel preparation and explicit edits.',pixel_log='pixel_edits.json',qa='qa.json',reproduction=['python build_native.py','python build_comparison.py','python validate_native.py']);old['outputs']=[{'path':str(z.relative_to(r)),'sha256':sha(z)} for z in sorted(p.iterdir()) if z.is_file() and z.name not in ['draft_manifest.json','manifest.json']];(p/'manifest.json').write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n');print(json.dumps(qa['technical']))
