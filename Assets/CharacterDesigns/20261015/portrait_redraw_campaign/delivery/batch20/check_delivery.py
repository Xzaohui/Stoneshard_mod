#!/usr/bin/env python3
"""Read-only frozen-source and attachment checkpoint; writes only its report."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,zipfile,base64
D=Path(__file__).resolve().parent;R=D.parent.parent;REPO=R.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads((D/'freeze_gate.json').read_text());m=json.loads((D/'selected_delivery_manifest.json').read_text());pv=json.loads((D/'package_verification.json').read_text())
counts={'production_frozen_files_verified':0,'source_records_verified':0,'QA_files_verified':0,'QA_files_packaged':len(g['qa_files']),'duplicate_QA_files_omitted':len(g['qa_duplicated_replay_files_omitted']),'raws_exact_to_full_tool_returns':0,'prompts_verified':0,'candidate_reproductions_from_actual_extracted_ZIPs':sum(len(p['reproduction']['candidates']) for p in pv['packages'])}
for c,files in g['frozen_character_files'].items():
 root=R/c;assert {x['path'] for x in files}=={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 for x in files:assert sha(root/x['path'])==x['sha256'];counts['production_frozen_files_verified']+=1
 source=json.loads((root/'sources/source_manifest.json').read_text())['items']
 for x in source:assert sha(REPO/x['original_path'])==x['sha256']==sha(root/x['snapshot_path']);counts['source_records_verified']+=1
 for v in ['portrait_v1','portrait_v2']:
  ret=json.loads((root/'tool_returns'/f'{v}.json').read_text());assert base64.b64decode(ret['image_url'].split(',',1)[1])==(root/'raw'/f'{v}_raw_imagegen.png').read_bytes();counts['raws_exact_to_full_tool_returns']+=1
  args=json.loads((root/'prompts'/f'{v}.json').read_text());assert args['prompt'].strip()==(root/'prompts'/f'{v}.txt').read_text().strip();counts['prompts_verified']+=1
for rel,h in g['qa_all_files'].items():assert sha(R/'independent_qa/batch20'/rel)==h;counts['QA_files_verified']+=1
for x in m['characters']:assert sha(D/x['delivery_file'])==x['source_sha256']==sha(R/x['source'])
assert sha(D/m['board']['file'])==m['board']['sha256'];assert [x['actor'] for x in m['characters']]==['luling','noda','sailuo']
assert json.loads((R/'naya/manifest.json').read_text())['selected_portrait'] is None
for x in pv['packages']:
 p=D/x['file'];assert sha(p)==x['sha256'] and p.stat().st_size==x['bytes'] and p.stat().st_size<18*1024**2
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  inv=json.loads(z.read('package_inventory.json'))
  for item in inv['files']:assert hashlib.sha256(z.read(item['path'])).hexdigest()==item['sha256']
counts.update(all_source_and_QA_hashes_unchanged=True,all_CRC_and_member_SHA_pass=True)
files=[]
for x in json.loads((D/'upload_request.json').read_text())['uploads']:
 p=Path(x['local_path']);files.append({'file':p.name,'bytes':p.stat().st_size,'sha256':sha(p)})
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'all_pass':True,'validation':counts,'attachments':files,'qualified_candidate_count':3,'held_count':1,'native_pixel_approved':False,'runtime_verified':False}
(D/(sys.argv[1] if len(sys.argv)>1 else 'pre_upload_checkpoint.json')).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
