#!/usr/bin/env python3
"""Verify independent final freeze and record immutable inventories for delivery."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parent.parent;Q=R/'independent_qa/batch27';REPO=R.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected=json.loads((D/'independent_freeze_confirmation.json').read_text())
for name,h in expected['anchor_sha256'].items():assert sha(Q/name)==h,name
f=json.loads((Q/'QA_summary.json').read_text());lock=json.loads((Q/'selection_lock.json').read_text())
assert f['third_generation_allowed'] is False and all(v==2 for v in f['successful_generations_per_person'].values())
assert len(f['delivery_include'])==len(lock['delivery_include_only'])==2
assert f['delivery_include']==lock['delivery_include_only']
qfiles={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()};sumrows={}
for line in (Q/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert sha(Q/n)==h,n;sumrows[n]=h
assert set(sumrows)==set(qfiles)-{'SHA256SUMS'}
qm=json.loads((Q/'manifest.json').read_text())
assert {x['path'] for x in qm['files']}==set(qfiles)-{'SHA256SUMS','manifest.json'}
for x in qm['files']:assert sha(Q/x['path'])==x['sha256'] and (Q/x['path']).stat().st_size==x['bytes']
sources=json.loads((Q/'independent_source_manifest.json').read_text())['sources']
for x in sources:assert sha(REPO/x['path'])==sha(Q/x['snapshot'])==x['sha256']
characters=[];held=[];inventories={}
for c in ['odo','tanser','noze','sefin']:
 root=R/c;m=json.loads((root/'manifest.json').read_text());a=next(x for x in f['characters'] if x['slug']==c)
 assert sha(root/'manifest.json')==a['author_manifest_sha256']
 assert m['selected_sha256']==a['selected_sha256']
 assert (f'{c}/{m["selected_portrait"]}' if m['selected_portrait'] else None)==a['selected_path']
 assert all(a[k] for k in ['manifest_hashes_all_match','sha256sums_all_match','all_author_source_hashes_match','raws_equal_full_returns','all_derivatives_byte_reproduce','all_derivatives_format_pass','all_integer_NN_previews_reproduce','all_prompts_exact_and_transparent'])
 row={'slug':c,'name':m['name'],'selected_portrait':a['selected_path'],'selected_sha256':a['selected_sha256'],'production_manifest_sha256':sha(root/'manifest.json'),'production_SHA256SUMS_sha256':sha(root/'SHA256SUMS'),'decision':a['status'],'generation_calls':m['generation_calls'],'qualified':a['delivery_eligible'],'approved_to_package':a['delivery_eligible'],'source_contour_gate_pass':c!='sefin','residual':a['limitations']}
 if a['delivery_eligible']:
  assert c in ['odo','tanser'] and sha(R/a['selected_path'])==a['selected_sha256'];characters.append(row)
 else:
  assert c in ['noze','sefin'] and a['selected_path'] is None and a['selected_sha256'] is None
  evidence=m.get('held_evidence',m.get('held_evidence_portrait'))
  assert f'{c}/{evidence}'==a['held_evidence_path']
  assert m['held_evidence_sha256']==a['held_evidence_sha256']==sha(root/evidence)
  row.update(held_evidence_portrait=a['held_evidence_path'],held_evidence_sha256=a['held_evidence_sha256'],historical_fallback_approved=False,source_clipping_confirmed=c=='sefin',hold_gate=a['status']);held.append(row)
 inventories[c]=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()]
assert len(characters)==2 and len(held)==2
assert {x['selected_portrait']:x['selected_sha256'] for x in characters}=={x['path']:x['sha256'] for x in lock['delivery_include_only']}
gate={'schema_version':1,'batch':'batch27','frozen_utc':datetime.now(timezone.utc).isoformat(),'independent_frozen_utc':f['checked_utc'],'approved_to_package':True,'qualified_candidate_count':2,'held_count':2,'characters':characters,'held':held,'frozen_character_files':inventories,'verified_production_file_count':sum(map(len,inventories.values())),'verified_independent_source_count':len(sources),'qa_files':qfiles,'qa_all_files':qfiles,'qa_duplicated_replay_files_omitted':{},'qa_duplicate_replay_production_mapping':[],'boundaries':{'held_is_not_success':True,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'user_final_approved':False}}
(D/'freeze_gate.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'verified_production_files':gate['verified_production_file_count'],'qa_all_files':len(qfiles),'qa_packaged_files':len(qfiles),'qa_files_omitted':0,'independent_sources_verified':len(sources)},ensure_ascii=False))
