#!/usr/bin/env python3
"""Validate independent batch28 selection and freeze all source bytes for delivery."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
D=Path(__file__).resolve().parent; R=D.parent.parent; Q=R/'independent_qa/batch28'; REPO=R.parents[3]
ORDER=['viko','ile','harlen','belo']; sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lock=json.loads((Q/'selection_lock.json').read_text())
assert sha(Q/'selection_lock.json')=='de8b2f90560ff2a80ea7b68ea943ade9272a9e04dbd90fa103061daef5f6ea0b'
summary=json.loads((Q/'QA_summary.json').read_text())
assert summary['batch']==lock['batch']==28 and not lock['native_pixel_approved'] and not lock['runtime_verified']
assert summary['delivery_include']==lock['delivery_include_only'] and len(lock['delivery_include_only'])==4
assert {x['slug'] for x in lock['delivery_include_only']}==set(ORDER)
actual={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()}
rows={}
for line in (Q/'SHA256SUMS').read_text().splitlines():
 h,rel=line.split('  ',1); assert actual[rel]==h,rel; rows[rel]=h
assert set(rows)==set(actual)-{'SHA256SUMS'}
qa_manifest=json.loads((Q/'manifest.json').read_text()); qa_inventory=qa_manifest['files']
assert qa_manifest['selected']==lock['delivery_include_only']
assert {x['path'] for x in qa_inventory}==set(actual)-{'SHA256SUMS','manifest.json'}
for x in qa_inventory: assert actual[x['path']]==x['sha256'] and (Q/x['path']).stat().st_size==x['bytes']
sources=json.loads((Q/'independent_source_manifest.json').read_text())
assert sources['independent_original_file_count']==len(sources['sources'])==30
for x in sources['sources']:
 assert sha(REPO/x['path'])==x['sha256']==sha(Q/x['snapshot'])
 assert (REPO/x['path']).stat().st_size==x['bytes']
assert json.loads((Q/'independent_source_final_recheck.json').read_text())['all_unchanged']
files={}; characters=[]
for c in ORDER:
 actor=next(x for x in summary['characters'] if x['slug']==c)
 selected=next(x for x in lock['delivery_include_only'] if x['slug']==c)
 assert actor['delivery_eligible'] and actor['status']=='deliverable_candidate_with_notes'
 assert actor['selected_path']==selected['path'] and actor['selected_sha256']==selected['sha256']
 for k in ['manifest_hashes_all_match','sha256sums_all_match','all_author_source_hashes_match','raws_equal_full_returns','all_derivatives_byte_reproduce','all_derivatives_format_pass','all_integer_NN_previews_reproduce','all_present_author_style_reference_enlargements_NN_reproduce','all_prompts_exact_and_transparent']:
  assert actor[k] is True,(c,k)
 assert not actor['manifest_missing_files'] and not actor['sha256sums_missing_files']
 root=R/c; m=json.loads((root/'manifest.json').read_text())
 assert sha(root/'manifest.json')==actor['author_manifest_sha256']
 assert sha(R/selected['path'])==selected['sha256']==m['selected_sha256']
 assert (root/m['selected_portrait']).resolve()==(R/selected['path']).resolve()
 assert m['generation_calls']==summary['successful_generations_per_person'][c]==2
 checks={}
 for line in (root/'SHA256SUMS').read_text().splitlines():
  h,rel=line.split('  ',1);assert sha(root/rel)==h; checks[rel]=h
 paths=sorted(p for p in root.rglob('*') if p.is_file())
 assert {p.relative_to(root).as_posix() for p in paths}-{'SHA256SUMS'}==set(checks)
 assert len(checks)==actor['sha256sums_entries']
 files[c]=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in paths]
 characters.append({'slug':c,'name':m['name'],'selected_portrait':selected['path'],'selected_sha256':selected['sha256'],'production_manifest_sha256':actor['author_manifest_sha256'],'limitations':actor['limitations']})
result={'batch':'28','gate_utc':datetime.now(timezone.utc).isoformat(),'approved_to_package':True,'freeze_entrypoint':'selection_lock.json','freeze_manifest_sha256':sha(Q/'selection_lock.json'),'qualified_candidate_count':4,'held_count':0,'characters':characters,'frozen_character_files':files,'qa_all_files':actual,'qa_files':actual,'qa_duplicated_replay_files_omitted':[],'qa_sha256sums_entries_verified':len(rows),'independent_source_file_count':30,'source_frozen_file_count':sum(map(len,files.values())),'native_pixel_approved':False,'runtime_verified':False}
(D/'freeze_gate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'frozen_character_files':result['source_frozen_file_count'],'qa_total':len(actual),'qa_included':len(actual),'qa_omitted':0,'all_pass':True}))
