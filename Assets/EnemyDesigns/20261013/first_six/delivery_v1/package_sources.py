from pathlib import Path
import json,hashlib,zipfile,datetime
D=Path(__file__).resolve().parent;B=D.parent
pairs=[('01_02_rebel_brigand',['border_spear_rebel','canal_club_brigand']),('03_04_restless_wraith',['canal_tomb_restless','crypt_drifter_wraith']),('05_06_mutant_warden',['blood_hunger_mutant','debt_ritual_warden'])]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
packages=[]
for label,slugs in pairs:
 files=[]
 for slug in slugs:
  p=B/slug/'idle_v1'
  assert (p/'independent_QA.json').is_file(), 'Independent QA missing: '+slug
  assert any(p.glob('FINAL_STATUS*')), 'Final status missing: '+slug
  files += sorted(f for f in p.rglob('*') if f.is_file() and '__pycache__' not in str(f))
 if label=='01_02_rebel_brigand':
  files.append(B/'independent_batch_QA.json')
  files += [f for f in sorted(D.iterdir()) if f.is_file() and f.suffix in ['.py','.png','.md'] or (f.is_file() and f.name in ['overview_inputs.json','overview_QA.json'])]
 zip_path=D/('enemy_first_six_'+label+'_complete_sources.zip')
 inv=[{'path':str(f.relative_to(B)),'sha256':sha(f),'bytes':f.stat().st_size} for f in files]
 with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in files:z.write(f,str(f.relative_to(B)))
  z.writestr('PACKAGE_CONTENTS.json',json.dumps(inv,ensure_ascii=False,indent=2))
 with zipfile.ZipFile(zip_path) as z:
  assert z.testzip() is None
  for i in inv:assert hashlib.sha256(z.read(i['path'])).hexdigest()==i['sha256']
 assert zip_path.stat().st_size <18*1024*1024,'Split archive required'
 packages.append({'path':zip_path.name,'bytes':zip_path.stat().st_size,'MiB':round(zip_path.stat().st_size/1024**2,3),'sha256':sha(zip_path),'source_file_count':len(inv),'all_source_files_included':True,'crc_and_content_hash_verified':True,'contents':inv})
overview=[{'path':f.name,'sha256':sha(f),'bytes':f.stat().st_size} for f in sorted(D.glob('enemy_first_six_overview*.png'))]
delivery={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'首6原创敌人外观静态概念。原作证据/项目设定/可逆外观提案分开，不新增剧情或runtime。','concept_count':6,'selected_concepts':json.loads((D/'overview_inputs.json').read_text()),'overview':overview,'packages':packages,'uploaded':False,'runtimeIntegrated':False,'runtimeVerified':False,'existing_manifests_unchanged':True}
(D/'delivery.json').write_text(json.dumps(delivery,ensure_ascii=False,indent=2))
print(json.dumps([{'path':p['path'],'MiB':p['MiB'],'files':p['source_file_count']} for p in packages],ensure_ascii=False,indent=2))
