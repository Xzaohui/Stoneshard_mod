#!/usr/bin/env python3
"""Verify independently frozen QA and record exact production/source inventory."""
from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
D=Path(__file__).resolve().parent;R=D.parent.parent;Q=R/'independent_qa/batch20'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(Q/'FINAL_SELECTION.json')=='7cd38da8a1b62cc96cc64acea568482f15f5967f81b0fb9d0767e72a5e8c63b0'
assert sha(Q/'SHA256SUMS.txt')=='52e84bb525689baf0f83ce9334221d8ce23781c598bef5db0dd57dee55f9fd27'
f=json.loads((Q/'FINAL_SELECTION.json').read_text()); assert f['technical_integrity_pass'] and f['concept_pass_count']==3 and f['held_count']==1
for line in (Q/'SHA256SUMS.txt').read_text().splitlines():
 h,n=line.split('  ',1);assert sha(Q/n)==h,n
qfiles={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()}; included={};omitted={};maps=[]
for rel,h in sorted(qfiles.items()):
 p=Path(rel)
 if len(p.parts)==4 and p.parts[0]=='replay' and p.parts[2] in ['raw','tool_returns']:
  target=R/p.parts[1]/p.parts[2]/p.parts[3]; assert sha(target)==h
  omitted[rel]=h;maps.append({'omitted_qa_path':rel,'production_path':target.relative_to(R).as_posix(),'sha256':h,'bytes_identical':True})
 else:included[rel]=h
assert len(omitted)==16
characters=[];held=[];inventories={}
for c in ['luling','noda','sailuo','naya']:
 root=R/c;m=json.loads((root/'manifest.json').read_text()); a=f['actors'][c]
 assert sha(root/'manifest.json')==a['author_manifest_sha256']
 assert sha(root/'SHA256SUMS')==a['author_SHA256SUMS_sha256']
 assert m['selected_portrait']==a['selected_candidate']
 row={'slug':c,'name':m['name'],'selected_portrait':f"{c}/{a['selected_candidate']}" if a['selected_candidate'] else None,'selected_sha256':a['selected_candidate_sha256'],'production_manifest_sha256':a['author_manifest_sha256'],'production_SHA256SUMS_sha256':a['author_SHA256SUMS_sha256'],'decision':a['status'],'generation_calls':a['generation_calls'],'qualified':a['deliverable'],'approved_to_package':a['deliverable'],'source_contour_gate_pass':a['deliverable'],'residual':a['residual_limitations']}
 if a['deliverable']:
  assert sha(root/a['selected_candidate'])==a['selected_candidate_sha256'];characters.append(row)
 else:
  assert c=='naya' and a['selected_candidate'] is None
  row.update(held_evidence_portrait=f"{c}/{a['held_evidence_candidate']}",held_evidence_sha256=a['held_evidence_sha256'],historical_fallback_approved=False)
  assert sha(root/a['held_evidence_candidate'])==a['held_evidence_sha256'];held.append(row)
 inventories[c]=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(root.rglob('*')) if p.is_file()]
gate={'schema_version':1,'batch':'batch20','frozen_utc':datetime.now(timezone.utc).isoformat(),'independent_frozen_utc':f['frozen_utc'],'approved_to_package':True,'qualified_candidate_count':3,'held_count':1,'characters':characters,'held':held,'frozen_character_files':inventories,'verified_production_file_count':sum(map(len,inventories.values())),'qa_files':included,'qa_all_files':qfiles,'qa_duplicated_replay_files_omitted':omitted,'qa_duplicate_replay_production_mapping':maps,'boundaries':{'held_is_not_success':True,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'user_final_approved':False}}
(D/'freeze_gate.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'verified_production_files':gate['verified_production_file_count'],'qa_all_files':len(qfiles),'qa_packaged_files':len(included),'qa_duplicate_replays_omitted':len(omitted)},ensure_ascii=False))
