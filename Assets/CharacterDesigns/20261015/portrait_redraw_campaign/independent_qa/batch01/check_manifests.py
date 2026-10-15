from pathlib import Path
import json, hashlib
QA=Path(__file__).resolve().parent
CAMPAIGN=QA.parents[1]
REPO=CAMPAIGN.parents[3]
NAMES=['mia','ena','nara','nell','sel']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else None
out={}
for name in NAMES:
 root=CAMPAIGN/name; path=root/'manifest.json'
 if not path.exists(): continue
 m=json.loads(path.read_text()); checks=[]
 for x in m.get('files',[]):
  p=root/x['path']; got=digest(p)
  checks.append({'path':x['path'],'expected':x['sha256'],'actual':got,'match':got==x['sha256']})
 sums=[]
 if (root/'SHA256SUMS.txt').exists():
  for line in (root/'SHA256SUMS.txt').read_text().splitlines():
   expected,rel=line.split('  ',1); got=digest(root/rel)
   sums.append({'path':rel,'match':got==expected,'expected':expected,'actual':got})
 src=json.loads((root/'sources/source_manifest.json').read_text()); entries=src.get('sources',[]) if isinstance(src,dict) else src
 source_checks=[]
 for e in entries:
  original=e.get('repository_source') or e.get('source')
  copy=e.get('archived_copy') or e.get('snapshot') or e.get('path')
  if not original or not copy: continue
  original=Path(original); original=original if original.is_absolute() else REPO/original
  copy=root/copy
  source_checks.append({'original':str(original),'copy':str(copy.relative_to(CAMPAIGN)),'source_sha256':digest(original),'copy_sha256':digest(copy),'recorded_sha256':e['sha256'],'source_matches':digest(original)==e['sha256'],'copy_matches':digest(copy)==e['sha256']})
 selected=m.get('selected_portrait'); selected_sha=digest(root/selected) if selected else None
 out[name]={'manifest_sha256':digest(path),'selected_portrait':selected,'selected_sha256':selected_sha,'recorded_selected_sha256':m.get('selected_portrait_sha256'),'selected_hash_matches':selected_sha==m.get('selected_portrait_sha256') if m.get('selected_portrait_sha256') else None,'generation_calls':m.get('generation_calls'),'image_generation_frozen':m.get('image_generation_frozen'),'source_files_frozen_for_delivery':m.get('source_files_frozen_for_delivery'),'independent_qa':m.get('independent_qa'),'file_inventory_count':len(checks),'file_inventory_all_match':all(x['match'] for x in checks),'file_inventory_mismatches':[x for x in checks if not x['match']],'sha256sums_count':len(sums),'sha256sums_all_match':all(x['match'] for x in sums),'sha256sums_mismatches':[x for x in sums if not x['match']],'source_checks':source_checks,'all_sources_match':all(x['source_matches'] and x['copy_matches'] for x in source_checks)}
(QA/'manifest_checks.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({name:{k:v for k,v in x.items() if k in ['selected_portrait','selected_hash_matches','generation_calls','image_generation_frozen','file_inventory_all_match','file_inventory_mismatches','sha256sums_all_match','sha256sums_mismatches','all_sources_match']} for name,x in out.items()},ensure_ascii=False,indent=2))
