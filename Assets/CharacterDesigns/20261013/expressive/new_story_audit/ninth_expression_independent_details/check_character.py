import json,hashlib,base64,sys
from pathlib import Path
from datetime import datetime,timezone
from PIL import Image,ImageDraw
import numpy as np
root=Path(__file__).resolve().parents[6]
audit=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_expression_independent_details'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(root)) if p.is_relative_to(root) else str(p),'sha256':sha(p)}
def metrics(p):
 im=Image.open(p);arr=np.asarray(im);a=arr[:,:,3];d=ref(p)|{'size':list(im.size),'mode':im.mode,'alpha_zero_pixels':int((a==0).sum()),'alpha_1_to_8_pixels':int(((a>0)&(a<=8)).sum()),'alpha0_hidden_rgb_pixels':int(((a==0)&(arr[:,:,:3]!=0).any(2)).sum())}
 for t in [0,8,128]:
  ys,xs=np.where(a>t);bb=[int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)];d['bbox_alpha_gt'+str(t)]=bb;d['margins_alpha_gt'+str(t)]=[bb[0],bb[1],im.width-bb[2],im.height-bb[3]]
 return d
slug=sys.argv[1];d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/slug/'expressions_v1';brief=json.loads((root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_four_expression_brief.json').read_text());char=next(c for c in brief['characters'] if c['slug']==slug)
checks=[]
def ck(kind,ok,**data):checks.append({'kind':kind,'pass':bool(ok),**data})
sx=json.loads((d/'sources/source_index.json').read_text());ss=sx.get('entries',sx.get('sources',[]))
for s in ss:
 a=root/s.get('source_path',s.get('original_path'));b=d/s.get('path',s.get('snapshot_path'));h=s['sha256'];ck('source_snapshot_pair',a.exists() and b.exists() and sha(a)==sha(b)==h,source=str(a),snapshot=str(b),sha256=h)
mf=d/'manifest.json';mfchecks=[]
if mf.exists():
 m=json.loads(mf.read_text())
 for f in m['files']:
  p=d/f['path'];mfchecks.append({'path':str(p.relative_to(root)),'sha256':sha(p) if p.exists() else None,'pass':p.exists() and sha(p)==f['sha256']})
log=json.loads((d/'generation-log.json').read_text());calls=log.get('calls',[]) if isinstance(log,dict) else log;poses=[]
for c in calls:
 e=next(x for x in char['expressions'] if x['id']==c['expression']);req=d/c.get('actual_tool_arguments_path',c.get('request'));prompt=d/c.get('prompt_path',c.get('prompt'));ret=d/c.get('tool_return_path',c.get('original_return'));raw=d/c.get('raw_path',c.get('raw'));sel=d/c.get('selected_path',c.get('selected'));orig=Path(c.get('output_original_path',c.get('tool_output_path')));args=json.loads(req.read_text());r=json.loads(ret.read_text());pr=prompt.read_text();
 ck('prompt_exact_archive',args['prompt']==pr.rstrip('\n'),expression=e['id'],prompt=ref(prompt),request=ref(req));ck('initial_prompt_matches_brief',args['prompt']==e['prompt_text'],expression=e['id']);ck('parameters',args.get('transparent_background') is True and args.get('referenced_image_paths')==[str(root/char['source_anchor'][k]['path']) for k in ['selected_raw','transparent']],expression=e['id']);
 b64=r.get('image_url','');returned_sha=hashlib.sha256(base64.b64decode(b64.split(',',1)[1])).hexdigest() if b64.startswith('data:') else None
 ck('return_raw_original_identity',returned_sha==sha(raw)==sha(orig),expression=e['id'],raw=ref(raw),original=ref(orig),original_return=ref(ret),return_image_sha256=returned_sha)
 for k,v in c.items():
  if k.endswith('_sha256'):
   pk=k[:-7];candidates=[pk,pk+'_path'];match=next((c[x] for x in candidates if x in c and isinstance(c[x],str)),None)
   if match:
    p=Path(match);p=p if p.is_absolute() else d/p;ck('logged_sha',p.exists() and sha(p)==v,key=k,path=str(p),expected=v)
 a=np.asarray(Image.open(raw));b=np.asarray(Image.open(sel));same=a.shape==b.shape;eq=same and np.array_equal(a,b);clipped=same and np.array_equal(a[a[:,:,3]>8],b[a[:,:,3]>8]) and np.all(b[a[:,:,3]<=8]==0)
 ck('selected_pixel_scope',eq or clipped,expression=e['id'],raw_selected_identical=bool(eq),only_alpha_le8_zeroed=bool(clipped))
 poses.append({'expression':e['id'],'label':e['label_zh'],'raw':metrics(raw),'selected':metrics(sel),'request':ref(req),'prompt':ref(prompt),'return':ref(ret),'raw_selected_identical':bool(eq),'only_alpha_le8_zeroed':bool(clipped)})
 # Reviewer-owned raw light/dark composite for actual inspection, source unchanged.
 im=Image.open(raw).convert('RGBA');sz=tuple(round(x*.6) for x in im.size);im=im.resize(sz,Image.Resampling.NEAREST);board=Image.new('RGB',(sz[0]*2,sz[1]+30));dr=ImageDraw.Draw(board)
 for i,col in enumerate([(240,238,230),(31,34,40)]):
  pane=Image.new('RGBA',sz,col+(255,));pane.alpha_composite(im);board.paste(pane.convert('RGB'),(i*sz[0],30));dr.rectangle((i*sz[0],0,(i+1)*sz[0],29),fill=col);dr.text((i*sz[0]+10,8),slug+' '+e['id']+' raw '+('light' if i==0 else 'dark'),fill=(20,20,20) if i==0 else (240,240,240))
 board.save(audit/(slug+'_'+e['id']+'_raw_light_dark.png'))
result={'created_utc':datetime.now(timezone.utc).isoformat(),'slug':slug,'manifest':ref(mf) if mf.exists() else None,'manifest_checks':mfchecks,'source_snapshot_pairs':len(ss),'calls':len(calls),'checks':checks,'poses':poses,'failures':[c for c in checks+mfchecks if not c['pass']]};(audit/(slug+'_chain_check.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'slug':slug,'manifest':result['manifest'],'manifest_entries':len(mfchecks),'source_snapshot_pairs':len(ss),'checks':len(checks),'calls':len(calls),'failures':result['failures']},ensure_ascii=False))
