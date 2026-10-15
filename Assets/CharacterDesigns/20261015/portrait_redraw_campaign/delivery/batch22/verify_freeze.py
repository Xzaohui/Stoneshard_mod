#!/usr/bin/env python3
"""Read and verify the independent FINAL_SELECTION freeze; capture a delivery gate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
D=Path(__file__).resolve().parent;R=D.parent.parent;Q=R/'independent_qa/batch22'
ORDER=['madi','boh','goren','nisha'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((Q/'FINAL_SELECTION.json').read_text())
assert sha(Q/'FINAL_SELECTION.json')=='078c386aa288ce1b03a98aa5e098c2e0fa0de32ca053759607960ad246db1c18'
assert freeze['batch']==22 and freeze['concept_pass_count']==4 and freeze['held_count']==0 and freeze['technical_integrity_pass']
assert freeze['native_pixel_approved'] is False and freeze['runtime_verified'] is False and set(freeze['actors'])==set(ORDER)
audit=json.loads((Q/'final_technical_audit.json').read_text());assert not audit['hard_errors'] and not audit['pending'] and audit['all_technical_checks_complete'] and audit['all_available_technical_checks_pass']
replay=json.loads((Q/'full_derivation_replay.json').read_text());assert replay['pass'] and not replay['errors']
final=json.loads((Q/'frozen_verification.json').read_text());assert final['technical_integrity_pass'] and final['all_technical_checks_complete'] and final['selection']==freeze['actors']
actual={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()}
rows={}
for line in (Q/'SHA256SUMS.txt').read_text().splitlines():
 h,rel=line.split('  ',1);assert actual[rel]==h,rel;rows[rel]=h
assert set(rows)==set(actual)-{'SHA256SUMS.txt'}
qa_inventory=json.loads((Q/'QA_FILE_INVENTORY.json').read_text())['files']
assert {x['path'] for x in qa_inventory}==set(actual)-{'SHA256SUMS.txt','QA_FILE_INVENTORY.json'}
for x in qa_inventory:assert actual[x['path']]==x['sha256'] and (Q/x['path']).stat().st_size==x['bytes']
for x in json.loads((Q/'DELIVERY_CHECKLIST.json').read_text())['files']:assert sha(R/x['path'])==x['sha256'] and (R/x['path']).stat().st_size==x['bytes']
files={};characters=[]
for c in ORDER:
 actor=freeze['actors'][c];assert actor['deliverable'] and actor['status']=='pass_concept_with_notes'
 root=R/c;m=json.loads((root/'manifest.json').read_text());selected=root/actor['selected_candidate'];assert sha(selected)==actor['selected_candidate_sha256']==m['selected_sha256'] and m['selected_portrait']==actor['selected_candidate']
 assert sha(root/'manifest.json')==actor['author_manifest_sha256'] and sha(root/'SHA256SUMS')==actor['author_SHA256SUMS_sha256']
 checks={}
 for line in (root/'SHA256SUMS').read_text().splitlines():
  h,rel=line.split('  ',1);assert sha(root/rel)==h;checks[rel]=h
 paths=sorted(p for p in root.rglob('*') if p.is_file());assert {p.relative_to(root).as_posix() for p in paths}-{'SHA256SUMS'}==set(checks)
 inventory=[{'path':p.relative_to(root).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in paths]
 files[c]=inventory;characters.append({'slug':c,'name':m['name'],'selected_portrait':str(selected.relative_to(R)),'selected_sha256':actor['selected_candidate_sha256'],'production_manifest_sha256':actor['author_manifest_sha256'],'limitations':actor['residual_limitations']})
omitted=[];include={}
for rel,h in actual.items():
 parts=Path(rel).parts
 if len(parts)==4 and parts[0]=='replay' and parts[1] in ORDER and parts[2] in ('raw','tool_returns'):
  target=R/parts[1]/parts[2]/parts[3];assert sha(target)==h
  omitted.append({'qa_path':rel,'sha256':h,'bytes':(Q/rel).stat().st_size,'identical_preserved_path':target.relative_to(R).as_posix(),'preserved_package':'A_MADI_BOH' if parts[1] in ORDER[:2] else 'B_GOREN_NISHA','reason':'Only byte-identical QA replay input duplicate omitted; original production retained.'})
 else:include[rel]=h
result={'batch':'22','gate_utc':datetime.now(timezone.utc).isoformat(),'approved_to_package':True,'freeze_entrypoint':'FINAL_SELECTION.json','freeze_manifest_sha256':sha(Q/'FINAL_SELECTION.json'),'qualified_candidate_count':4,'held_count':0,'characters':characters,'frozen_character_files':files,'qa_all_files':actual,'qa_files':include,'qa_duplicated_replay_files_omitted':omitted,'qa_sha256sums_entries_verified':len(rows),'source_frozen_file_count':sum(map(len,files.values())),'native_pixel_approved':False,'runtime_verified':False}
(D/'freeze_gate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'frozen_character_files':result['source_frozen_file_count'],'qa_total':len(actual),'qa_included':len(include),'qa_duplicate_replay_omitted':len(omitted)}))
