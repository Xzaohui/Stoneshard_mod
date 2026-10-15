#!/usr/bin/env python3
"""Verify frozen selections and hash every QA file except each self-referential index."""
from pathlib import Path
import hashlib,json,datetime
Q=Path(__file__).resolve().parent;C=Q.parent.parent;R=C.parents[3];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((Q/'FINAL_SELECTION.json').read_text());pre=json.loads((Q/'preflight_source_checks.json').read_text());checks=[]
for slug,row in s['actors'].items():
 root=C/slug;m=root/'manifest.json';assert sha(m)==row['author_manifest_sha256'];assert sha(root/'SHA256SUMS')==row['author_SHA256SUMS_sha256']
 selected=row['selected_candidate'];assert selected is None or sha(root/selected)==row['selected_candidate_sha256']
 for line in (root/'SHA256SUMS').read_text().splitlines():
  h,p=line.split(maxsplit=1);assert sha(root/p.lstrip('*'))==h
for actor in pre['actors'].values():
 for row in actor['source_checks']:assert sha(R/row['path'])==row['actual_sha256']==sha(Q/row['snapshot'])
for folder in Q.rglob('__pycache__'):
 for p in folder.glob('*.pyc'):p.unlink()
 folder.rmdir()
records=[]
for p in sorted(Q.rglob('*')):
 if not p.is_file() or p.name in ('QA_FILE_INVENTORY.json','SHA256SUMS.txt'):continue
 records.append({'path':str(p.relative_to(Q)),'sha256':sha(p),'bytes':p.stat().st_size})
inv={'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'excludes':['QA_FILE_INVENTORY.json','SHA256SUMS.txt'],'reason':'Avoid circular/self hashes; SHA256SUMS includes this inventory.','files':records}
(Q/'QA_FILE_INVENTORY.json').write_text(json.dumps(inv,ensure_ascii=False,indent=2)+'\n')
paths=sorted(p for p in Q.rglob('*') if p.is_file() and p.name!='SHA256SUMS.txt')
(Q/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+str(p.relative_to(Q))+'\n' for p in paths))
for row in records:assert sha(Q/row['path'])==row['sha256']
for line in (Q/'SHA256SUMS.txt').read_text().splitlines():h,p=line.split(maxsplit=1);assert sha(Q/p)==h
print(json.dumps({'inventory_files':len(records),'SHA256SUMS_files':len(paths),'all_verified':True,'selection_sha256':sha(Q/'FINAL_SELECTION.json'),'report_sha256':sha(Q/'FINAL_REVIEW.md'),'SHA256SUMS_sha256':sha(Q/'SHA256SUMS.txt')}))
