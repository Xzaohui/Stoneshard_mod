from pathlib import Path
from datetime import datetime, timezone
from source_validation import validate_sources, validate_prompts
import json,hashlib,sys
D=Path(__file__).resolve().parent;R=D.parent.parent;REPO=R.parents[3];Q=R/'independent_qa/batch37'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
g=json.loads((D/'freeze_gate.json').read_text());sm=json.loads((D/'selected_delivery_manifest.json').read_text());pv=json.loads((D/'package_verification.json').read_text());u=json.loads((D/'upload_request.json').read_text())
for c,files in g['frozen_character_files'].items():
 actual={p.relative_to(R/c).as_posix() for p in (R/c).rglob('*') if p.is_file()};assert actual=={x['path'] for x in files}
 for x in files:assert sha(R/c/x['path'])==x['sha256']
 for flag in ['selected_portrait','selected_sha256']:assert json.loads((R/'lein/manifest.json').read_text())[flag] is None
source_count=sum(len(validate_sources(R/c,REPO)) for c in g['frozen_character_files'])
for c in g['frozen_character_files']:validate_prompts(R/c)
assert {p.relative_to(Q).as_posix() for p in Q.rglob('*') if p.is_file()}==set(g['qa_files'])
for p,h in g['qa_files'].items():assert sha(Q/p)==h
sources=json.loads((Q/'independent_source_manifest.json').read_text())['sources']
for x in sources:assert sha(REPO/x['path'])==x['sha256']==sha(Q/x['snapshot'])
expected=[sm['board']['file']]+[x['delivery_file'] for x in sm['characters']]+[x['file'] for x in pv['packages']]
assert [Path(x['local_path']).name for x in u['uploads']]==expected and len(expected)==6
hashes={x['delivery_file']:x['delivery_sha256'] for x in sm['characters']};hashes[sm['board']['file']]=sm['board']['sha256'];hashes.update({x['file']:x['sha256'] for x in pv['packages']})
files=[]
for n in expected:
 p=D/n;assert p.is_file() and sha(p)==hashes[n];files.append({'file':n,'bytes':p.stat().st_size,'sha256':sha(p)})
for p in pv['packages']:
 assert p['crc_all_pass'] and p['member_hash_all_pass'] and p['actual_extracted_zip_reproduction_all_pass'] and p['bytes']<18*1024**2
n=sum(len(x['reproduction']['candidates']) for x in pv['packages']);assert n==11
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'all_pass':True,'production_frozen_files_verified':sum(len(v) for v in g['frozen_character_files'].values()),'QA_files_verified':len(g['qa_files']),'all_sources_and_QA_unchanged':True,'source_manifest_checks':source_count,'independent_source_checks':len(sources),'archive_members_checked':[x['checks']['member_count'] for x in pv['packages']],'historical_candidates_reproduced':n,'held_selected_is_null':True,'held_not_counted_as_success':True,'all_six_attachments_unchanged':True,'files':files}
if (D/'library_upload_result.json').exists():
 data=json.loads((D/'library_upload_result.json').read_text()); rows=data['results']; assert len(rows)==6
 assert [x['local_path'] for x in rows]==[x['local_path'] for x in u['uploads']]
 assert all(x['status']=='succeeded' and x.get('local_metadata_applied') is True and x.get('library_file_id') for x in rows)
 assert len({x['library_file_id'] for x in rows})==6
 report.update(all_uploads_succeeded=True,ordered_paths_exact=True,unique_library_ids=True,all_local_library_metadata_applied=True,library_file_ids=[x['library_file_id'] for x in rows])
if (D/'send_receipt.json').exists():
 receipt=json.loads((D/'send_receipt.json').read_text());assert receipt['status']=='accepted' and receipt['library_file_ids']==report['library_file_ids']
 report.update(send_accepted_receipt_recorded=True,send_accepted_message_id=receipt['message_id'])
name=sys.argv[1] if len(sys.argv)>1 else 'pre_upload_checkpoint.json';(D/name).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ['files','library_file_ids']},ensure_ascii=False,indent=2))
