#!/usr/bin/env python3
"""Verify independent final freeze and record immutable inventories for delivery."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parent.parent;Q=R/'independent_qa/batch24'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Q/'QA_summary.json')=='20fd61b65b6a573407cf522074c8323e4b9627791bf5998732fdddc66ac26e85'
assert sha(Q/'SHA256SUMS')=='0771f04fe91d08561171db74b10e7fe7c8752e07483912bcf075b5596589e415'
assert sha(Q/'selection_lock.json')=='bd6eb4fad5e365dbeb2f9634bebcc5ead93916909ae05ec42c261db570e0d991'
f=json.loads((Q/'QA_summary.json').read_text());assert f['final_status']=='three_candidates_one_held'
qfiles={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()};sumrows={}
for line in (Q/'SHA256SUMS').read_text().splitlines():
 h,n=line.split('  ',1);assert sha(Q/n)==h,n;sumrows[n]=h
assert set(sumrows)==set(qfiles)-{'SHA256SUMS'}
characters=[];held=[];inventories={}
for c in ['liqui','arlo','ondo','hure']:
 root=R/c;m=json.loads((root/'manifest.json').read_text());a=next(x for x in f['characters'] if x['slug']==c)
 assert sha(root/'manifest.json')==a['author_manifest_sha256']
 assert m['selected_sha256']==a['selected_sha256']
 assert (f'{c}/{m["selected_portrait"]}' if m['selected_portrait'] else None)==a['selected_path']
 row={'slug':c,'name':m['name'],'selected_portrait':a['selected_path'],'selected_sha256':a['selected_sha256'],'production_manifest_sha256':a['author_manifest_sha256'],'production_SHA256SUMS_sha256':sha(root/'SHA256SUMS'),'decision':a['status'],'generation_calls':m['generation_calls'],'qualified':a['delivery_eligible'],'approved_to_package':a['delivery_eligible'],'source_contour_gate_pass':True,'residual':a['limitations']}
 if a['delivery_eligible']:
  assert sha(R/a['selected_path'])==a['selected_sha256'];characters.append(row)
 else:
  assert c=='hure' and a['selected_path'] is None
  row.update(held_evidence_portrait=a['held_evidence_path'],held_evidence_sha256=a['held_evidence_sha256'],historical_fallback_approved=False,source_clipping_confirmed=False,hold_gate='composition_scale_and_eye_sclera')
  assert sha(R/a['held_evidence_path'])==a['held_evidence_sha256'];held.append(row)
 inventories[c]=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()]
assert len(characters)==3 and len(held)==1
gate={'schema_version':1,'batch':'batch24','frozen_utc':datetime.now(timezone.utc).isoformat(),'independent_frozen_utc':f['checked_utc'],'approved_to_package':True,'qualified_candidate_count':3,'held_count':1,'characters':characters,'held':held,'frozen_character_files':inventories,'verified_production_file_count':sum(map(len,inventories.values())),'qa_files':qfiles,'qa_all_files':qfiles,'qa_duplicated_replay_files_omitted':{},'qa_duplicate_replay_production_mapping':[],'boundaries':{'held_is_not_success':True,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'user_final_approved':False}}
(D/'freeze_gate.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'verified_production_files':gate['verified_production_file_count'],'qa_all_files':len(qfiles),'qa_packaged_files':len(qfiles),'qa_files_omitted':0},ensure_ascii=False))
