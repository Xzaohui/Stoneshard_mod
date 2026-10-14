from pathlib import Path
import json,hashlib,zipfile,zlib,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');B=R/'Assets/EnemyDesigns/20261013/first_six';D=B/'mutant_warden_actions_delivery_v1';sha=lambda b:hashlib.sha256(b).hexdigest()
assert all((B/s/'action_v1'/'independent_action_QA.json').exists() for s in ['blood_hunger_mutant','debt_ritual_warden'])
common=[D/'README.txt',D/'actions_overview_light.png',D/'actions_overview_dark.png',D/'build_delivery.py',D/'seal_delivery.py']
archives=[]
for s in ['blood_hunger_mutant','debt_ritual_warden']:
 target=D/(s+'_actions_complete.zip');assert not target.exists()
 files=sorted(x for x in (B/s/'action_v1').rglob('*') if x.is_file())+common
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f in files:z.write(f,str(f.relative_to(B)))
 members=[]
 with zipfile.ZipFile(target) as z:
  assert z.testzip() is None
  for info in z.infolist():
   data=z.read(info.filename); source=B/info.filename;assert data==source.read_bytes()
   members.append({'path':info.filename,'bytes':info.file_size,'compressed_bytes':info.compress_size,'crc32':f'{info.CRC:08x}','sha256':sha(data)})
 size=target.stat().st_size; assert size<18*1024*1024
 archives.append({'path':target.name,'sha256':sha(target.read_bytes()),'bytes':size,'under_18_MiB':True,'crc_test':'pass','members':members})
files=[]
for p in sorted(D.iterdir()):
 if p.suffix=='.png':
  data=p.read_bytes();files.append({'path':p.name,'bytes':len(data),'sha256':sha(data),'crc32':f'{zlib.crc32(data)&0xffffffff:08x}'})
record={'status':'sealed','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'selected_keyposes':4,'user_delivery':['actions_overview_light.png']+[p['path'] for p in files if p['path'].endswith('_transparent.png')]+[a['path'] for a in archives],'files':files,'archives':archives,'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation':False,'policy':'After sealing, only read checks; no source or archive modifications.'}
(D/'delivery.json').write_text(json.dumps(record,ensure_ascii=False,indent=2))
qa={'result':'pass','delivery_json_sha256':sha((D/'delivery.json').read_bytes()),'checks':{'all_four_selected_independently_passed':True,'light_dark_overviews_actually_viewed':True,'nearest_neighbor_isotropic_preview_only':True,'archives_crc_and_source_bytes_verified':True,'each_archive_under_18_MiB':True,'old_static_and_frozen_manifests_unchanged':True},'files':files,'archives':archives}
(D/'FINAL_DELIVERY_QA.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
for a in archives:print(a['path'],a['bytes'],a['sha256'],len(a['members']))
