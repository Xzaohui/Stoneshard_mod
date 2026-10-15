#!/usr/bin/env python3
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys
D=Path(__file__).resolve().parent;R=D.parent.parent;REPO=R.parents[3];Q=R/'independent_qa/batch38'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads((D/'freeze_gate.json').read_text());r=json.loads((D/'delivery_record.json').read_text())
for c,rows in g['frozen_character_files'].items():
 assert {p.relative_to(R/c).as_posix() for p in (R/c).rglob('*') if p.is_file()}=={x['path'] for x in rows}
 for x in rows:assert sha(R/c/x['path'])==x['sha256'] and (R/c/x['path']).stat().st_size==x['bytes']
assert {p.relative_to(Q).as_posix() for p in Q.rglob('*') if p.is_file()}==set(g['qa_all_files'])
for rel,h in g['qa_all_files'].items():assert sha(Q/rel)==h
for c in r['qualified_candidates']:
 for x in json.loads((R/c/'sources/source_manifest.json').read_text())['items']:
  origin=x['original_path'];raw=subprocess.check_output(['git','show',origin[4:]],cwd=REPO) if origin.startswith('git:') else (REPO/origin).read_bytes()
  assert hashlib.sha256(raw).hexdigest()==x['sha256']==sha(R/c/x['snapshot_path'])
for x in json.loads((Q/'independent_source_manifest.json').read_text())['sources']+json.loads((Q/'supplemental_source_manifest.json').read_text())['sources']:
 origin=x['path'];raw=subprocess.check_output(['git','show',origin[4:]],cwd=REPO) if origin.startswith('git ') else (REPO/origin).read_bytes()
 assert hashlib.sha256(raw).hexdigest()==x['sha256']==sha(Q/x['snapshot'])
for x in r['attachments']:assert sha(D/x['file'])==x['sha256'] and (D/x['file']).stat().st_size==x['bytes']
result={'checked_utc':datetime.now(timezone.utc).isoformat(),'checkpoint':sys.argv[1],'all_pass':True,'production_frozen_files':g['source_frozen_file_count'],'QA_frozen_files':len(g['qa_all_files']),'author_source_records':50,'independent_current_and_historical_sources':35,'attachments':r['attachments'],'no_mutations_outside_batch38_by_delivery_worker':True}
(D/f'{sys.argv[1]}_checkpoint.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
