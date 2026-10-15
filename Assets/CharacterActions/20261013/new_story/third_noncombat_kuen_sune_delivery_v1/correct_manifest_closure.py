from pathlib import Path
import json,hashlib,shutil,datetime,zipfile
R=Path(__file__).resolve().parents[5];D=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();hist=D/'preclosure_history';hist.mkdir(exist_ok=False)
mp=D/'delivery_manifest.json';shutil.copy2(mp,hist/mp.name);dm=json.loads(mp.read_text());changes=[]
for slug in ['kuen','sune']:
 o=R/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';m=o/'manifest.json';shutil.copy2(m,hist/(slug+'_manifest.json'));before={str(p.relative_to(o)):sha(p) for p in o.rglob('*') if p.is_file()}
 j=json.loads(m.read_text());old={x['path'] for x in j['files']};files=[p for p in sorted(o.rglob('*')) if p.is_file() and p!=m]
 j['files']=[{'path':str(p.relative_to(o)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files];j['file_count_without_manifest']=len(files);j['manifest_closure_corrected_utc']=now;j['closure_correction']='仅根manifest自身排除；补入已存在的两份嵌套来源manifest。图、源、FINAL_STATUS均未修改。'
 m.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 for p,h in before.items():
  if p!='manifest.json':assert sha(o/p)==h
 zp=D/(slug+'_noncombat_basics_complete_source_v1.zip');oldzip=sha(zp);shutil.move(zp,hist/zp.name)
 with zipfile.ZipFile(zp,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(o.rglob('*')):
   if p.is_file():z.write(p,f'{slug}/noncombat_basics_v1/'+str(p.relative_to(o)))
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None;expected={f'{slug}/noncombat_basics_v1/'+str(p.relative_to(o)) for p in o.rglob('*') if p.is_file()};assert set(z.namelist())==expected
  for a in expected:assert hashlib.sha256(z.read(a)).hexdigest()==sha(o/a.split('/noncombat_basics_v1/',1)[1])
 assert zp.stat().st_size<18*1024*1024
 row=next(a for a in dm['attachments'] if a.get('kind')=='complete_source_zip' and a.get('character')==slug);row.update(bytes=zp.stat().st_size,sha256=sha(zp),manifest_sha256=sha(m));changes.append({'character':slug,'old_manifest_sha256':before['manifest.json'],'new_manifest_sha256':sha(m),'added_manifest_entries':sorted({x['path'] for x in j['files']}-old),'manifest_file_count':len(files),'old_zip_sha256':oldzip,'new_zip_sha256':sha(zp),'final_status_unchanged':sha(o/'FINAL_STATUS.json')==before['FINAL_STATUS.json'],'all_other_frozen_files_unchanged':True})
dm['manifest_closure_corrected_utc']=now;mp.write_text(json.dumps(dm,ensure_ascii=False,indent=2)+'\n');(D/'manifest_closure_correction.json').write_text(json.dumps({'created_utc':now,'reason':'独审查出根manifest排除条件过宽，漏列两份嵌套来源manifest；ZIP一直包含这些源。只修清单，不改视觉或源。','changes':changes},ensure_ascii=False,indent=2)+'\n');print(json.dumps(changes,ensure_ascii=False,indent=2));print('delivery_manifest',sha(mp))
