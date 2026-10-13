from pathlib import Path
import json,hashlib,zipfile,shutil
B=Path(__file__).resolve().parent.parent;D=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'lyd':'bdd283ae295ec8e1c61a3ea48245ec7fac21580ea990ab9cd41230e84edb971d','hers':'098ded9b7a0b8c9d13460396ca85aa0d9eaa93ab030bd049884f508c3253d432'}
for s in expected:
 o=B/s/'expressions_v1';assert sha(o/'manifest.json')==expected[s]
 qa=json.loads((o/'QA-independent.json').read_text());print(s,'QA',qa.get('status',qa.get('overall_status','See independent QA')))
 for f in json.loads((o/'manifest.json').read_text())['files']:assert sha(o/f['path'])==f['sha256'],f['path']
 status={'status':'independent_review_passed_concept_only','canonical_id':'NPC-'+s.upper(),'new_bust_count':2,'new_character_count':0,'runtime_integrated':False,'roster_changed':False,'manifest_sha256':expected[s],'independent_qa_sha256':sha(o/'QA-independent.json'),'raw_visual_qa_sha256':sha(o/'QA-independent-raw-visual.json'),'post_QA_modification_to_reviewed_manifest_or_images':False,'delivered_to_user':False}
 (o/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
 for p in sorted((o/'selected').glob('*.png')):shutil.copy2(p,D/p.name)
pack=D/'lyd_hers_expressions_source_v1.zip'
sourcefiles=[p for s in expected for p in sorted((B/s/'expressions_v1').rglob('*')) if p.is_file()]
sourcefiles += [D/'lyd_hers_expressions_zh_light.png',Path(__file__)]
with zipfile.ZipFile(pack,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sourcefiles:z.write(p,str(p.relative_to(B)))
assert pack.stat().st_size<18*1024*1024
with zipfile.ZipFile(pack) as z:
 assert z.testzip() is None
 members=[]
 for info in z.infolist():
  local=B/info.filename;h=hashlib.sha256(z.read(info.filename)).hexdigest();assert h==sha(local)
  members.append({'member':info.filename,'bytes':info.file_size,'crc32':f'{info.CRC:08x}','sha256':h})
(D/'ZIP_VERIFICATION.json').write_text(json.dumps({'zip':pack.name,'sha256':sha(pack),'bytes':pack.stat().st_size,'crc_test':'passed','all_member_sha256_match':True,'members':members},ensure_ascii=False,indent=2))
deliver=[D/'lyd_hers_expressions_zh_light.png']+sorted(D.glob('*_transparent.png'))+[pack]
(D/'DELIVERY_MANIFEST.json').write_text(json.dumps({'status':'prepared_not_uploaded','count':len(deliver),'files':[{'path':str(p),'filename':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in deliver],'zip_verification':str(D/'ZIP_VERIFICATION.json'),'new_bust_count':4,'new_characters':0,'runtime_integrated':False,'roster_changed':False},ensure_ascii=False,indent=2))
print('DELIVERY',D/'DELIVERY_MANIFEST.json', 'ZIP bytes',pack.stat().st_size,'members',len(members))
