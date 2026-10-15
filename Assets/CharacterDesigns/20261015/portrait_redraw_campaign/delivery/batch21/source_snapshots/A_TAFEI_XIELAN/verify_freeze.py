#!/usr/bin/env python3
"""Verify independent freeze and capture a read-only delivery gate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json
D=Path(__file__).resolve().parent; R=D.parent.parent; Q=R/'independent_qa/batch21'
ORDER=['tafei','xielan','yuen','arlin']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
freeze=json.loads((Q/'freeze_manifest.json').read_text())
assert freeze['batch']==21 and freeze['status']=='four_derived_candidates_pass_with_notes'
assert freeze['native_pixel_approved'] is False and freeze['runtime_verified'] is False
assert set(freeze['actors'])==set(ORDER)
audit=json.loads((Q/'final_technical_audit.json').read_text());assert not audit['hard_errors'] and not audit['pending'] and audit['all_technical_checks_complete'] and audit['all_available_technical_checks_pass']
replay=json.loads((Q/'final_derivation_replay.json').read_text());assert replay['pass'] and not replay['errors']
actual={p.relative_to(Q).as_posix():sha(p) for p in Q.rglob('*') if p.is_file()}
rows={}
for line in (Q/'SHA256SUMS').read_text().splitlines():
 h,rel=line.split('  ',1);assert actual[rel]==h,rel;rows[rel]=h
assert set(rows)==set(actual)-{'SHA256SUMS'}
files={};characters=[]
for c in ORDER:
 actor=freeze['actors'][c];selected=R/actor['selected_portrait'];assert sha(selected)==actor['selected_sha256']
 assert sha(R/actor['author_manifest'])==actor['author_manifest_sha256']
 m=json.loads((R/actor['author_manifest']).read_text());assert m['selected_sha256']==actor['selected_sha256'] and actor['selected_portrait']==c+'/'+m['selected_portrait']
 inventory=[dict(x,path=x['path'].removeprefix(c+'/')) for x in freeze['delivery_inventory'] if x['path'].startswith(c+'/')]
 assert {p.relative_to(R/c).as_posix() for p in (R/c).rglob('*') if p.is_file()}=={x['path'] for x in inventory}
 for x in inventory:assert sha(R/c/x['path'])==x['sha256'] and (R/c/x['path']).stat().st_size==x['bytes']
 files[c]=inventory;characters.append({'slug':c,'name':actor['name'],'selected_portrait':actor['selected_portrait'],'selected_sha256':actor['selected_sha256'],'production_manifest_sha256':actor['author_manifest_sha256'],'limitations':actor['limitations']})
assert sum(map(len,files.values()))==len(freeze['delivery_inventory'])
omitted=[];include={}
for rel,h in actual.items():
 parts=Path(rel).parts
 if len(parts)==4 and parts[0]=='replay' and parts[1] in ORDER and parts[2] in ('raw','tool_returns'):
  target=R/parts[1]/parts[2]/parts[3];assert sha(target)==h
  omitted.append({'qa_path':rel,'sha256':h,'bytes':(Q/rel).stat().st_size,'identical_preserved_path':target.relative_to(R).as_posix(),'preserved_package':'A_TAFEI_XIELAN' if parts[1] in ORDER[:2] else 'B_YUEN_ARLIN','reason':'Only byte-identical QA replay input duplicate omitted; original production retained.'})
 else:include[rel]=h
result={'batch':'21','gate_utc':datetime.now(timezone.utc).isoformat(),'approved_to_package':True,'freeze_manifest_sha256':sha(Q/'freeze_manifest.json'),'qualified_candidate_count':4,'held_count':0,'characters':characters,'frozen_character_files':files,'qa_all_files':actual,'qa_files':include,'qa_duplicated_replay_files_omitted':omitted,'qa_sha256sums_entries_verified':len(rows),'source_frozen_file_count':sum(map(len,files.values())),'native_pixel_approved':False,'runtime_verified':False}
(D/'freeze_gate.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'frozen_character_files':result['source_frozen_file_count'],'qa_total':len(actual),'qa_included':len(include),'qa_duplicate_replay_omitted':len(omitted)}))
