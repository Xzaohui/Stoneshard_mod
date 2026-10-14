from pathlib import Path
import hashlib,json,zipfile,zlib,datetime
OUT=Path(__file__).resolve().parent;BASE=OUT.parent;REPO=BASE.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def info(p):
 b=p.read_bytes();return {'path':str(p.relative_to(REPO)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'crc32':f'{zlib.crc32(b)&0xffffffff:08x}'}
def write(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
roles=['border_spear_rebel','canal_club_brigand'];qa=BASE/'action_independent_QA_v1'
assert (qa/'independent_QA.json').exists(), 'Wait for final independent QA'
common=[p for p in qa.rglob('*') if p.is_file()]+[OUT/n for n in ['README.md','build_delivery.py','package_delivery.py','humanoid_actions_overview_light.png','humanoid_actions_overview_dark.png']]
archives=[];directories=[]
for role in roles:
 root=BASE/role/'action_v1';assert (root/'FINAL_STATUS.json').exists()
 files=sorted(p for p in root.rglob('*') if p.is_file());directories.append({'directory':str(root.relative_to(REPO)),'members':[info(p) for p in files]})
 zpath=OUT/f'{role}_action_v1_complete_sources.zip'
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for p in files+common:z.write(p,str(p.relative_to(BASE)))
 assert zpath.stat().st_size<18*1024*1024
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None
  members=[{'name':e.filename,'bytes':e.file_size,'compressed_bytes':e.compress_size,'crc32':f'{e.CRC:08x}','sha256':hashlib.sha256(z.read(e.filename)).hexdigest()} for e in z.infolist()]
 archives.append({**info(zpath),'testzip':'pass','members':members})
attachments=[]
for role in roles:
 attachments += [info(p) for p in sorted((BASE/role/'action_v1').glob('*/*_transparent.png')) if p.parent.name != 'sources']
attachments += [info(OUT/'humanoid_actions_overview_light.png')]+[{k:v for k,v in a.items() if k!='members'} for a in archives]
d={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'four independent key poses; spear natural forward-grip variants; not a continuous animation','runtimeIntegrated':False,'runtimeVerified':False,'attachment_count':len(attachments),'attachments':attachments,'role_directories':directories,'common_members':[info(p) for p in common],'archives':archives}
write(OUT/'delivery.json',d)
write(OUT/'FINAL_DELIVERY_QA.json',{'status':'package_pass_pending_parent_delivery','attachment_count':len(attachments),'max_attachments':10,'all_archives_under_18MiB':True,'archive_crc_test':'pass','all_directory_members_included':True,'overview_light_and_dark_actually_viewed':True,'all_four_bodies_weapons_and_feet_visible':True,'Chinese_labels_legible':True,'independent_qa_sha256':sha(qa/'independent_QA.json'),'delivery_sha256':sha(OUT/'delivery.json'),'known_limits':['001 original rear-grip brief not met; natural forward-grip variants separately reviewed','Cross-pose precise spear length unverified','No continuous animation, runtime, collision or equipment-composition verification'],'uploaded':False,'committed':False})
print(json.dumps({'attachments':attachments,'archives':[{'path':a['path'],'bytes':a['bytes'],'members':len(a['members'])} for a in archives]},ensure_ascii=False,indent=2))
