#!/usr/bin/env python3
"""Record independently frozen batch37 and verify exact production/source inventories."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parent.parent;Q=R/'independent_qa/batch37'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Independent batch37 QA final is complete and parent confirmed the freeze.
summary=json.loads((Q/'QA_summary.json').read_text());lock=json.loads((Q/'selection_lock.json').read_text());qm=json.loads((Q/'manifest.json').read_text())
assert summary['batch']==37 and summary['successful_generations_per_person']==dict.fromkeys(['aro','lein','gura','turi'],2) and not summary['third_generation_allowed']
assert lock['delivery_include_only']==summary['delivery_include']==qm['selected']
assert sha(Q/'selection_lock.json')=='67fcd44a619e4663429c40aa44e90642dd8c73a0787162eb9c5c62661f4c6edd'
REPO=R.parents[3]
independent_sources=json.loads((Q/'independent_source_manifest.json').read_text())
assert independent_sources['independent_original_file_count']==len(independent_sources['sources'])==28
for x in independent_sources['sources']:
 assert sha(REPO/x['path'])==x['sha256']==sha(Q/x['snapshot'])
assert json.loads((Q/'independent_source_final_recheck.json').read_text())['all_unchanged']
assert [x['slug'] for x in lock['delivery_include_only']]==['aro','gura','turi']
qfiles={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()}
assert {x['path'] for x in qm['files']}==set(qfiles)-{'manifest.json','SHA256SUMS'}
for x in qm['files']: assert sha(Q/x['path'])==x['sha256'] and (Q/x['path']).stat().st_size==x['bytes']
qsums={}
for line in (Q/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert sha(Q/n)==h,n;qsums[n]=h
assert set(qsums)==set(qfiles)-{'SHA256SUMS'}
characters=[];held=[];inventories={}
for c in ['aro','gura','turi','lein']:
 root=R/c;m=json.loads((root/'manifest.json').read_text());a=next(x for x in summary['characters'] if x['slug']==c)
 assert sha(root/'manifest.json')==a['author_manifest_sha256']
 for flag in ['manifest_hashes_all_match','sha256sums_all_match','all_author_source_hashes_match','raws_equal_full_returns','all_derivatives_byte_reproduce','all_derivatives_format_pass','all_integer_NN_previews_reproduce','all_present_author_style_reference_enlargements_NN_reproduce','all_prompts_exact_and_transparent']:assert a[flag]
 actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
 assert {x['path'] for x in m['files']}==actual-{'manifest.json','SHA256SUMS'}
 for x in m['files']:assert sha(root/x['path'])==x['sha256'] and (root/x['path']).stat().st_size==x['bytes']
 sums={}
 for line in (root/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1);assert sha(root/n)==h;sums[n]=h
 assert set(sums)==actual-{'SHA256SUMS'}
 selected=f"{c}/{m['selected_portrait']}" if m['selected_portrait'] else None
 assert selected==a['selected_path'] and m['selected_sha256']==a['selected_sha256']
 row={'slug':c,'name':m['name'],'selected_portrait':selected,'selected_sha256':a['selected_sha256'],'production_manifest_sha256':a['author_manifest_sha256'],'production_SHA256SUMS_sha256':sha(root/'SHA256SUMS'),'decision':a['status'],'generation_calls':m['generation_calls'],'qualified':a['delivery_eligible'],'approved_to_package':a['delivery_eligible'],'source_contour_gate_pass':a['delivery_eligible'],'residual':a['limitations']}
 if a['delivery_eligible']:
  assert sha(R/selected)==a['selected_sha256'];characters.append(row)
 else:
  assert c=='lein' and selected is None and m['status']=='held_source_contour_margin_and_style'
  row.update(held_evidence_portrait=a['held_evidence_path'],held_evidence_sha256=a['held_evidence_sha256'],historical_fallback_approved=False)
  assert sha(R/a['held_evidence_path'])==a['held_evidence_sha256'];held.append(row)
 inventories[c]=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()]
assert len(characters)==3 and len(held)==1
f={'schema_version':1,'batch':'batch37','frozen_utc':datetime.now(timezone.utc).isoformat(),'independent_frozen_utc':summary['checked_utc'],'approved_to_package':True,'qualified_candidate_count':3,'held_count':1,'characters':characters,'held':held,'frozen_character_files':inventories,'verified_production_file_count':sum(map(len,inventories.values())),'qa_files':qfiles,'qa_all_files':qfiles,'qa_duplicated_replay_files_omitted':{},'qa_duplicate_replay_production_mapping':[],'qa_manifest_sha256':sha(Q/'manifest.json'),'qa_sha256sums_sha256':sha(Q/'SHA256SUMS'),'qa_selection_lock_sha256':sha(Q/'selection_lock.json'),'qa_summary_sha256':sha(Q/'QA_summary.json'),'boundaries':{'held_is_not_success':True,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'user_final_approved':False}}
(D/'freeze_gate.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'production_files':f['verified_production_file_count'],'QA_files':len(qfiles),'QA_manifest_items':len(qm['files']),'QA_SHA_items':len(qsums),'qualified':3,'held':1,'all_pass':True}))
