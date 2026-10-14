import json, hashlib
from pathlib import Path
from datetime import datetime, timezone
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[6]
base=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
out=base/'ninth_expression_independent_details'
brief=base/'ninth_four_expression_brief.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(p,h,origin):
 p=Path(p); p=p if p.is_absolute() else root/p
 a=sha(p) if p.exists() else None
 return {'path':str(p.relative_to(root)),'expected_sha256':h,'actual_sha256':a,'pass':a==h,'origin':origin}
def walk(d,origin):
 if isinstance(d,dict):
  if isinstance(d.get('path'),str) and isinstance(d.get('sha256'),str):yield check(d['path'],d['sha256'],origin)
  for k,v in d.items():yield from walk(v,origin)
 elif isinstance(d,list):
  for v in d:yield from walk(v,origin)
b=json.loads(brief.read_text());checks=list(walk(b,'brief'))
ix=root/b['source_snapshot_index']['path'];checks+=list(walk(json.loads(ix.read_text()),'brief_source_index'))
man=[]; mothers=[]
for c in b['characters']:
 p=root/c['source_anchor']['manifest']['path'];m=json.loads(p.read_text())
 for f in m['files']:man.append(check(p.parent/f['path'],f['sha256'],c['slug']+'_mother_manifest'))
 for typ in ['selected_raw','transparent']:
  p=root/c['source_anchor'][typ]['path'];im=Image.open(p).convert('RGBA');a=im.getchannel('A');mothers.append({'slug':c['slug'],'type':typ,'path':str(p.relative_to(root)),'sha256':sha(p),'mode':im.mode,'size':list(im.size),'alpha_extrema':a.getextrema(),'bbox':a.getbbox()})
 # Show actual selected mother on light/dark using correct alpha compositing. No source pixels changed.
 im=Image.open(root/c['source_anchor']['transparent']['path']).convert('RGBA');s=.60;sz=tuple(round(x*s) for x in im.size);im=im.resize(sz,Image.Resampling.NEAREST)
 plate=Image.new('RGB',(sz[0]*2,sz[1]+30));dr=ImageDraw.Draw(plate)
 for i,col in enumerate([(240,238,230),(31,34,40)]):
  panel=Image.new('RGBA',sz,col+(255,));panel.alpha_composite(im);plate.paste(panel.convert('RGB'),(i*sz[0],30));dr.rectangle((i*sz[0],0,(i+1)*sz[0],29),fill=col);dr.text((i*sz[0]+10,8),c['slug']+' mother '+('light' if i==0 else 'dark'),fill=(20,20,20) if i==0 else (240,240,240))
 plate.save(out/(c['slug']+'_mother_light_dark.png'))
r={'created_utc':datetime.now(timezone.utc).isoformat(),'brief_sha256':sha(brief),'brief_and_snapshot_checks':checks,'mother_manifest_checks':man,'mothers':mothers,'failures':[v for v in checks+man if not v['pass']]}
(out/'baseline_source_verification.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'root':str(root),'brief_sha256':sha(brief),'brief_and_snapshot_path_sha_checks':len(checks),'mother_manifest_entries':len(man),'failures':r['failures']},ensure_ascii=False))
