from pathlib import Path
import json,hashlib,base64,sys,datetime
from PIL import Image,ImageDraw
import numpy as np
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'eleventh_actions_independent_details';slug,stem=sys.argv[1:3];d=r/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
files=[p for p in d.rglob('*') if p.is_file() and p.name.startswith(stem) and 'sources' not in p.relative_to(d).parts];raw=next(p for p in files if p.parent.name=='raw' and p.suffix=='.png');sel=next(p for p in files if p.parent.name in ['selected','exports','review'] and p.suffix=='.png' and 'transparent' in p.name);ret=next(p for p in files if any(t in p.name for t in ['tool_return','tool_result']) and p.suffix=='.json');arg=next(p for p in files if any(t in p.name for t in ['tool_arguments','tool_args','parameters']) and p.suffix=='.json');prompt=next(p for p in files if p.suffix=='.txt');pa=json.loads(arg.read_text());pa=pa.get('parameters',pa.get('tool_parameters',pa));pr=prompt.read_text();checks=[]
def ck(kind,ok,**x):checks.append({'kind':kind,'pass':bool(ok),**x})
def dec(o):
 out=[]
 if isinstance(o,str) and o.startswith('data:image/') and ';base64,' in o:out.append(base64.b64decode(o.split(';base64,',1)[1]))
 elif isinstance(o,dict):
  if o.get('type')=='image' and 'data' in o:out.append(base64.b64decode(o['data']))
  for v in o.values():out+=dec(v)
 elif isinstance(o,list):
  for v in o:out+=dec(v)
 return out
ims=dec(json.loads(ret.read_text()));ck('full_return_decoded_image_matches_raw',any(hashlib.sha256(b).hexdigest()==sha(raw) for b in ims),decoded_images=len(ims));ck('exact_prompt_in_arguments',pa['prompt']==pr);ck('prompt_arguments_saved_before_raw',max(arg.stat().st_mtime,prompt.stat().st_mtime)<=raw.stat().st_mtime);ck('transparent_requested',pa.get('transparent_background') is True)
b=json.loads((a/'eleventh_new_character_actions_brief.json').read_text());c=next(c for c in b['characters'] if c['slug']==slug);plan=next(p for p in c['plans'] if stem.startswith(p['key']));ck('initial_prompt_exact_frozen_plan',pr==plan['prompt'] if any(x in stem for x in ['initial','_v1']) else True,revision=not any(x in stem for x in ['initial','_v1']))
refs=pa.get('referenced_image_paths',[]); refhashes=[sha(Path(f)) for f in refs if Path(f).is_file()]; allowed={c['mother_image']['transparent_sha256']}
if 'revision' in stem:
 first=next((f for f in (d/'raw').glob(plan['key']+'*initial*.png')),None)
 if first:allowed.add(sha(first))
ck('only_mother_and_same_pose_revision_reference',len(refhashes)==len(refs) and set(refhashes)<=allowed and c['mother_image']['transparent_sha256'] in refhashes,reference_files=refs)
x=np.array(Image.open(raw).convert('RGBA'));y=np.array(Image.open(sel).convert('RGBA'));ck('raw_selected_same_dimensions',x.shape==y.shape)
if x.shape==y.shape:
 mask=np.any(x!=y,axis=2);ck('all_changed_pixels_have_raw_alpha_le8',np.all(x[mask,3]<=8),changed_pixels=int(mask.sum()));ck('visible_body_pixels_unchanged',np.array_equal(x[x[:,:,3]>8],y[x[:,:,3]>8]))
ck('true_alpha_transparency',int(y[:,:,3].min())==0 and int(y[:,:,3].max())>=250)
metrics=[]
for p in [raw,sel]:
 im=Image.open(p).convert('RGBA');ar=np.array(im);al=ar[:,:,3];ys,xs=np.where(al>8);bb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];metrics.append({**fp(p),'mode':Image.open(p).mode,'size':list(im.size),'bbox_gt8':bb,'margins_gt8':[bb[0],bb[1],im.width-bb[2],im.height-bb[3]],'alpha_zero_pixels':int((al==0).sum()),'hidden_rgb_alpha0_pixels':int(((al==0)&np.any(ar[:,:,:3]!=0,axis=2)).sum())})
for p in files:
 if p.suffix=='.png' and any(s in p.name for s in ['_light','_dark']):
  im=Image.open(p).convert('RGBA');src=Image.open(raw if '_raw_light' in p.name or '_raw_dark' in p.name else (sel if 'selected' in p.name or p.parent.name=='review' else raw)).convert('RGBA');bg=((239,234,222,255) if '_light' in p.name else (35,40,46,255)) if slug in ['jier','suier_lot'] else im.getpixel((0,0));expected=Image.alpha_composite(Image.new('RGBA',src.size,bg),src);ck('author_true_alpha_composite',im.size==src.size and np.array_equal(np.array(im),np.array(expected)),path=str(p.relative_to(r)),background=list(bg))
# Reviewer constructs original and selected alpha comparisons, without touching authors' image files.
board=Image.new('RGB',(1920,760),(235,233,225));draw=ImageDraw.Draw(board)
for i,(p,bg,lab) in enumerate([(raw,(244,241,233),'raw light'),(raw,(30,33,40),'raw dark'),(sel,(244,241,233),'selected light'),(sel,(30,33,40),'selected dark')]):
 im=Image.open(p).convert('RGBA');im.thumbnail((480,710),Image.Resampling.NEAREST);pane=Image.new('RGBA',(480,760),bg+(255,));pane.alpha_composite(im,((480-im.width)//2,40));board.paste(pane.convert('RGB'),(i*480,0));draw.text((i*480+8,10),slug+' '+plan['key'].split('_A')[1][:2]+' '+lab,fill=(0,0,0) if i%2==0 else (255,255,255))
view=e/(stem+'_raw_selected_true_alpha.png');board.save(view)
out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'slug':slug,'stem':stem,'plan_key':plan['key'],'status':'pending_actual_visual_review','files':[fp(p) for p in files],'checks':checks,'metrics':metrics,'comparison':fp(view),'failures':[x for x in checks if not x['pass']]};p=e/(stem+'_byte_audit.json');p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'stem':stem,'checks':len(checks),'failures':out['failures'],'metrics':metrics,'view':str(view)},ensure_ascii=False))
