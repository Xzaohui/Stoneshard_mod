from pathlib import Path
import hashlib,json,shutil,zipfile,datetime
root=Path(__file__).resolve().parents[4]
base=root/'Assets/CharacterDesigns/20261013/expressive'
out=base/'tor_rhea_turnaround_delivery_v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
entries=[];status=[];sources=set()
for who in ['tor','rhea']:
 p=base/who/'turnaround_v1';q=p/'QA-independent.json'
 assert q.exists(),f'{who} independent review pending'
 report=json.loads(q.read_text());assert report['status'].startswith('pass'),f'{who} did not pass'
 status.append({'character':'n1_'+who,'status':report['status'],'independent_qa':str(q.relative_to(root)),'independent_qa_sha256':sha(q),'manifest_at_freeze_sha256':sha(p/'manifest.json'),'notes':report.get('limitations',[]),'new_views':2,'new_characters':0,'user_approved':False,'runtimeVerified':False,'equipment_compatibility_verified':False})
 for f in p.iterdir():
  if f.is_file():sources.add(f)
 sh=json.loads((p/'sourcehash.json').read_text())
 for s in [sh['anchor']]+sh['sources']:
  f=root/s['file'];assert sha(f)==s['sha256'],str(f)+' source changed';sources.add(f)
sources.add(base/'tor/period_costume_v2/tor_period_costume_v2_raw_imagegen.png')
sources.add(base/'tor/period_costume_v2/prompt.txt')
sources.add(base/'tor/period_costume_v2/manifest.json')
sources.add(base/'rhea/prompt.txt');sources.add(base/'rhea/manifest.json')
sources.add(Path(__file__).resolve())
out.mkdir(exist_ok=True)
final={'frozen_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'independently_reviewed_concept_with_notes','characters':status,'manifest_policy':'Original reviewed manifests and README wording preserved byte-for-byte as generation-stage snapshots; this FINAL_STATUS supersedes their pending-review labels only.','scope':'4 new views of 2 existing characters; no newly completed character count. Back construction is design inference. Concept only; not exact orthographic animation, engine assets or runtime verification.','processing':'All boards use common 0.60 nearest-neighbor scale and foot translation; no per-view stretching. Tor back +5.69% visible height is retained and independently accepted as concept with notes.'}
(out/'FINAL_STATUS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
sources.add(out/'FINAL_STATUS.json')
for who in ['tor','rhea']:
 p=base/who/'turnaround_v1'
 for name in [f'{who}_turnaround_review_zh.png',f'{who}_left_transparent.png',f'{who}_back_transparent.png']:
  shutil.copyfile(p/name,out/name);entries.append(out/name)
member=[{'file':str(f.relative_to(root)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(sources)]
(out/'SOURCE_MEMBERS.json').write_text(json.dumps(member,ensure_ascii=False,indent=2)+'\n')
z=out/'tor_rhea_turnaround_v1_source.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as a:
 for f in sorted(sources):a.write(f,str(f.relative_to(root)))
 a.write(out/'SOURCE_MEMBERS.json','SOURCE_MEMBERS.json')
assert z.stat().st_size<18*1024*1024,'archive exceeds delivery limit'
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None
 for m in member:assert hashlib.sha256(a.read(m['file'])).hexdigest()==m['sha256']
 verify={'crc_test':'pass','all_member_sha256_verified':True,'members':len(a.namelist()),'archive_bytes':z.stat().st_size,'archive_sha256':sha(z)}
entries.append(z)
inventory=[{'path':str(f.resolve()),'bytes':f.stat().st_size,'sha256':sha(f)} for f in entries]
(out/'DELIVERY_INVENTORY.json').write_text(json.dumps({'files':inventory,'verification':verify},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'files':inventory,'verification':verify},ensure_ascii=False,indent=2))
