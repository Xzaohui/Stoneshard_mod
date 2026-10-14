from pathlib import Path
import json,hashlib,base64,sys,io
import numpy as np
from PIL import Image
from datetime import datetime,timezone
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
A=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fp(p):
 p=Path(p); return {'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)}
def decode_images(o):
 out=[]
 if isinstance(o,str) and o.startswith('data:image/') and ';base64,' in o:
  out.append(base64.b64decode(o.split(';base64,',1)[1]))
 elif isinstance(o,dict):
  if o.get('type')=='image' and isinstance(o.get('data'),str):
   try:out.append(base64.b64decode(o['data']))
   except:pass
  for v in o.values():out+=decode_images(v)
 elif isinstance(o,list):
  for v in o:out+=decode_images(v)
 return out
if __name__=='__main__':
 slug,key=sys.argv[1:3];folder=root/'Assets/CharacterActions/20261013/new_story'/slug/'noncombat_basics_v1'
 files=[p for p in folder.rglob('*') if p.is_file() and p.name.startswith(key)]
 raw=next(p for p in files if p.parent.name=='raw' and p.suffix=='.png')
 selected=next(p for p in files if p.suffix=='.png' and p.parent.name in ['exports','review'] and 'transparent' in p.name)
 ret=next(p for p in files if p.suffix=='.json' and ('tool_return' in p.name or 'tool_result' in p.name))
 param=next(p for p in files if p.suffix=='.json' and ('parameters' in p.name or 'tool_args' in p.name))
 prompt=next(p for p in files if p.parent.name=='prompts' and p.suffix=='.txt')
 pa=json.loads(param.read_text()); pp=pa.get('parameters',pa.get('tool_parameters',pa));
 rr=json.loads(ret.read_text()); decoded=decode_images(rr)
 im=Image.open(raw).convert('RGBA'); sel=Image.open(selected).convert('RGBA'); rawarr=np.array(im);selarr=np.array(sel)
 checks={'raw_matches_decoded_complete_tool_result':any(hashlib.sha256(b).hexdigest()==sha(raw) for b in decoded),'decoded_images':len(decoded),'prompt_matches_parameters':pp.get('prompt')==prompt.read_text(),'source_prompt_saved_before_raw':max(param.stat().st_mtime,prompt.stat().st_mtime)<=raw.stat().st_mtime,'transparent_requested':pp.get('transparent_background') is True,'raw_and_selected_same_dimensions':im.size==sel.size,'raw_mode':Image.open(raw).mode,'selected_mode':Image.open(selected).mode,'alpha_extrema':sel.getchannel('A').getextrema(),'canvas':list(sel.size)}
 if im.size==sel.size:
  mask=rawarr[:,:,3]>8
  checks['body_alpha_gt8_bytes_unchanged']=bool(np.array_equal(rawarr[mask],selarr[mask]));checks['all_changed_pixels_raw_alpha_le8']=bool(np.all(rawarr[np.any(rawarr!=selarr,axis=2),3]<=8))
  checks['transparent_background_clear']=bool(np.any(selarr[:,:,3]==0) and np.any(selarr[:,:,3]>=250))
 lightdark=[]
 for p in files:
  if p.suffix=='.png' and p.parent.name=='review' and any(t in p.name for t in ['_light','_dark']):
   out=Image.open(p).convert('RGBA')
   if out.size==sel.size:
    bg=out.getpixel((0,0)); expected=Image.alpha_composite(Image.new('RGBA',sel.size,bg),sel)
    lightdark.append({'path':str(p.relative_to(root)),'background_rgba':list(bg),'matches_true_composite':np.array_equal(np.array(expected),np.array(out))})
 checks['light_dark_composites']=lightdark
 bref=json.loads((A/'eighth_new_character_actions_brief.json').read_text()); plan=next(p for c in bref['characters'] if c['slug']==slug for p in c['plans'] if key.startswith(p['key']))
 if key.endswith('_v1'):checks['first_prompt_matches_frozen_brief']=prompt.read_text()==plan['prompt']
 provenance=next((p for p in files if 'provenance' in p.name),None)
 provenance_errors=[]
 if provenance:
  pd=json.loads(provenance.read_text())
  for rel,row in pd.get('files',{}).items():
   f=folder/rel
   if not f.is_file() or sha(f)!=row['sha256'] or ('bytes' in row and f.stat().st_size!=row['bytes']): provenance_errors.append(rel)
  for row in pd.get('reference_hashes',[]):
   f=Path(row['path']);f=f if f.is_absolute() else root/f
   if not f.is_file() or sha(f)!=row['sha256']: provenance_errors.append(row['path'])
 checks['provenance_file_present']=provenance is not None
 checks['provenance_all_file_and_reference_hashes_match']=not provenance_errors
 checks['provenance_errors']=provenance_errors
 refs=[Path(f) if Path(f).is_absolute() else root/f for f in pp.get('referenced_image_paths',[])]
 checks['submitted_reference_files_exist']=bool(refs) and all(f.is_file() for f in refs)
 mother=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/slug/'concept_v1'/f'{slug}_transparent.png'
 checks['submitted_reference_includes_sha_verified_mother']=any(f.is_file() and sha(f)==sha(mother) for f in refs)
 result={'character':slug,'pose_version':key,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'verdict':'pending_visual_review','files':[fp(p) for p in files],'checks':checks}
 target=A/'independent_eighth_new_character_actions_evidence'/f'{key}_byte_audit.json';target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({"character":slug,"pose":key,"checks":checks,"evidence":str(target.relative_to(root))},ensure_ascii=False))
