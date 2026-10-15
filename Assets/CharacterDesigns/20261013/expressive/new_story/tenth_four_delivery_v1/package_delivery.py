from pathlib import Path
import json,hashlib,zipfile,datetime
OUT=Path(__file__).resolve().parent; BASE=OUT.parent;ROOT=BASE.parents[4];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
items=[('suoda','FX-WCH'),('kelin','FX-HUT'),('jier','FX-FRM'),('suier_lot','FX-LOT')]
qa=BASE.parent/'new_story_audit/independent_visual_qa_tenth_four_20261013.json'
assert qa.exists(),'Awaiting final independent QA'
chars=[]
for slug,cid in items:
 d=BASE/slug/'concept_v1';m=d/'manifest.json';assert m.exists();data=json.loads(m.read_text());members=data.get('members',data.get('files',[]));
 if isinstance(members,dict):members=[{'path':k,'sha256':v} for k,v in members.items()]
 for x in members:
  p=d/x.get('path',x.get('file',''));assert sha(p)==x['sha256'],str(p)
 chars.append({'slug':slug,'canonical_id':cid,'directory':str(d.relative_to(ROOT)),'transparent':str((d/f'{slug}_transparent.png').relative_to(ROOT)),'transparent_sha256':sha(d/f'{slug}_transparent.png'),'frozen_manifest':str(m.relative_to(ROOT)),'frozen_manifest_sha256':sha(m)})
ov=OUT/'第十批四人_中文概览.png';archives=[]
for slugs,label in [(['suoda','kelin'],'索妲珂琳'),(['jier','suier_lot'],'蓟珥绥珥')]:
 z=OUT/f'新增剧情人物_{label}源包.zip'
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as arc:
  for slug in slugs:
   d=BASE/slug/'concept_v1'
   for p in sorted(d.rglob('*')):
    if p.is_file():arc.write(p,str(p.relative_to(BASE)))
  for p in [qa,ov,OUT/'build_overview.py',OUT/'package_delivery.py']:arc.write(p,'batch_review/'+p.name)
 with zipfile.ZipFile(z) as arc:assert arc.testzip() is None;count=len(arc.namelist())
 assert z.stat().st_size<18*1024*1024
 archives.append({'path':str(z.relative_to(ROOT)),'sha256':sha(z),'bytes':z.stat().st_size,'entry_count':count})
for c in chars:assert sha(ROOT/c['frozen_manifest'])==c['frozen_manifest_sha256']
result={'status':'ready_not_uploaded','characters':chars,'overview':{'path':str(ov.relative_to(ROOT)),'sha256':sha(ov),'bytes':ov.stat().st_size},'archives':archives,'independent_qa':{'path':str(qa.relative_to(ROOT)),'sha256':sha(qa)},'final_status':str((OUT/'FINAL_STATUS.json').relative_to(ROOT)),'manifest_files_unchanged':True,'zip_integrity':'testzip pass','packaging_only':True}
(OUT/'delivery.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');(OUT/'FINAL_STATUS.json').write_text(json.dumps({'status':'independent_review_pass_ready_not_uploaded','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runtime_verified':False,'equipment_compatibility':'unknown','characters':[x[0] for x in items],'delivery':'delivery.json'},ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False,indent=2))
