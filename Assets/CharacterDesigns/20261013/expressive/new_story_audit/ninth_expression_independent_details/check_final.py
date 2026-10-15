import json,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[6];audit=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_expression_independent_details'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return {'path':str(p.relative_to(root)),'sha256':sha(p)}
for slug in sys.argv[1:]:
 d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/slug/'expressions_v1';mf=d/'manifest.json';fs=d/'FINAL_STATUS.json';m=json.loads(mf.read_text());f=json.loads(fs.read_text());checks=[]
 for e in m['files']:
  p=d/e['path'];checks.append({'stage':'manifest','path':str(p.relative_to(root)),'sha256':sha(p),'pass':sha(p)==e['sha256']})
 def walk(o):
  if isinstance(o,dict):
   if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
    p=d/o['path'];checks.append({'stage':'final_status','path':str(p.relative_to(root)),'sha256':sha(p),'pass':sha(p)==o['sha256']})
   for v in o.values():walk(v)
  elif isinstance(o,list):
   for v in o:walk(v)
 walk(f)
 for k,v in f.get('files',{}).items():
  p=d/k;checks.append({'stage':'final_status_files','path':str(p.relative_to(root)),'sha256':sha(p),'pass':sha(p)==v})
 if 'manifest_sha256' in f:checks.append({'stage':'manifest_binding','pass':sha(mf)==f['manifest_sha256']})
 for name in ['QA-independent-raw-visual.json','QA-independent.json']:
  q=json.loads((d/name).read_text());checks.append({'stage':'independent_status','file':name,'pass':q['status']=='passed'})
  # All linked independent review evidence except historical manifest-at-review must remain exact.
  def verify(o):
   if isinstance(o,dict):
    if isinstance(o.get('path'),str) and isinstance(o.get('sha256'),str):
     p=Path(o['path']);p=p if p.is_absolute() else root/p;checks.append({'stage':'qa_evidence','path':str(p),'sha256':sha(p),'pass':sha(p)==o['sha256']})
    for v in o.values():verify(v)
   elif isinstance(o,list):
    for v in o:verify(v)
  verify(q)
 r={'created_utc':datetime.now(timezone.utc).isoformat(),'slug':slug,'manifest':ref(mf),'final_status':ref(fs),'manifest_entries':len(m['files']),'checks':checks,'status':'passed' if all(x['pass'] for x in checks) else 'failed','failures':[x for x in checks if not x['pass']]};(audit/(slug+'_final_readback.json')).write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='checks'},ensure_ascii=False))
