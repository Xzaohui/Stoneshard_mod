#!/usr/bin/env python3
"""Verify independently frozen QA and record exact production/source inventory."""
from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parent.parent;Q=R/'independent_qa/batch23'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Q/'FINAL_SELECTION.json')=='acd4a1244c4e28e7dd14445ba12be105b8b4f038531a5df96461a63e02da6f24'
assert sha(Q/'SHA256SUMS.txt')=='60c0736e557e0fa78a64f0e008043dbc0929eb7eda15ad0a16ee641dc63d2e00'
f=json.loads((Q/'FINAL_SELECTION.json').read_text()); assert f['technical_integrity_pass'] and f['concept_pass_count']==3 and f['held_count']==1
for line in (Q/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split('  ',1);assert sha(Q/n)==h,n
qfiles={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()}; included={};omitted={};maps=[]
for rel,h in sorted(qfiles.items()):
 p=Path(rel)
 if len(p.parts)==5 and p.parts[0]=='reproduction' and p.parts[3] in ['raw','tool_returns']:
  target=R/p.parts[1]/p.parts[3]/p.parts[4]; assert sha(target)==h
  omitted[rel]=h;maps.append({'omitted_qa_path':rel,'production_path':target.relative_to(R).as_posix(),'sha256':h,'bytes_identical':True})
 else:included[rel]=h
assert len(omitted)==20
characters=[];held=[];inventories={}
for c in ['saler','wenno','buran','reha']:
 root=R/c;m=json.loads((root/'manifest.json').read_text()); a=f['actors'][c]
 assert sha(root/'manifest.json')==a['author_manifest_sha256']
 assert sha(root/'SHA256SUMS')==a['author_SHA256SUMS_sha256']
 assert m['selected_portrait']==a['selected_candidate']
 row={'slug':c,'name':m['name'],'selected_portrait':f"{c}/{a['selected_candidate']}" if a['selected_candidate'] else None,'selected_sha256':a['selected_candidate_sha256'],'production_manifest_sha256':a['author_manifest_sha256'],'production_SHA256SUMS_sha256':a['author_SHA256SUMS_sha256'],'decision':a['status'],'generation_calls':a['generation_calls'],'qualified':a['deliverable'],'approved_to_package':a['deliverable'],'source_contour_gate_pass':a['deliverable'],'residual':a['residual_limitations']}
 if a['deliverable']:
  assert sha(root/a['selected_candidate'])==a['selected_candidate_sha256'];characters.append(row)
 else:
  assert c=='reha' and a['selected_candidate'] is None
  row.update(held_evidence_portrait=f"{c}/{a['held_evidence_candidate']}",held_evidence_sha256=a['held_evidence_sha256'],historical_fallback_approved=False)
  assert sha(root/a['held_evidence_candidate'])==a['held_evidence_sha256'];held.append(row)
 inventories[c]=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()]
gate={'schema_version':1,'batch':'batch23','frozen_utc':datetime.now(timezone.utc).isoformat(),'independent_frozen_utc':f['frozen_utc'],'approved_to_package':True,'qualified_candidate_count':3,'held_count':1,'characters':characters,'held':held,'frozen_character_files':inventories,'verified_production_file_count':sum(map(len,inventories.values())),'qa_files':included,'qa_all_files':qfiles,'qa_duplicated_replay_files_omitted':omitted,'qa_duplicate_replay_production_mapping':maps,'boundaries':{'held_is_not_success':True,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'user_final_approved':False}}
(D/'freeze_gate.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'verified_production_files':gate['verified_production_file_count'],'qa_all_files':len(qfiles),'qa_packaged_files':len(included),'qa_duplicate_replays_omitted':len(omitted)},ensure_ascii=False))
