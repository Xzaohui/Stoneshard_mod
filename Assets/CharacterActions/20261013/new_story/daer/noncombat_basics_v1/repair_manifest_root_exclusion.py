from pathlib import Path
import hashlib,json,zipfile,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');N=R/'Assets/CharacterActions/20261013/new_story';D=N/'eighth_noncombat_seer_daer_delivery_v1';S=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();F=lambda p:{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':S(p)}
newpackages={}
for slug in ['seer','daer']:
 d=N/slug/'noncombat_basics_v1';shutil.copyfile(__file__,d/'repair_manifest_root_exclusion.py')
 mf=d/'manifest.json';ff=d/'FINAL_STATUS.json';oldm=S(mf);oldf=S(ff);m=json.loads(mf.read_text());f=json.loads(ff.read_text())
 entries=[F(p) for p in sorted(d.rglob('*')) if p.is_file() and p not in [mf,ff]]
 m['files']=entries;m['manifest_collection_note']='仅排除本人物目录根级manifest.json与FINAL_STATUS.json；嵌套来源同名文件必须纳入。';mf.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 f['frozen_utc']='2026-10-14T07:41:41Z';f['manifest_sha256']=S(mf);f['frozen_files']=entries+[F(mf)];f['pre_package_index_correction']={'reason':'包审要求将已存在包内的嵌套concept/manifest.json与expression/FINAL_STATUS.json纳入人物manifest与冻结文件索引。','prior_manifest_sha256':oldm,'prior_final_status_sha256':oldf,'image_and_prompt_data_unchanged':True};ff.write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
 zpath=D/'delivery'/f'{slug}_complete_action_sources_v1.zip'
 with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,6) as z:
  for p in sorted(d.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(R))
 with zipfile.ZipFile(zpath) as z:
  assert z.testzip() is None;members=[]
  for n in z.namelist():
   b=z.read(n);assert (R/n).read_bytes()==b;members.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 assert zpath.stat().st_size<18*1024*1024
 newpackages[str(zpath.relative_to(R))]={**F(zpath),'crc_pass':True,'member_count':len(members),'members':members}
 print(slug,'indexed',len(entries),'nested',[x['path'] for x in entries if '/sources/' in x['path'] and x['path'].endswith(('manifest.json','FINAL_STATUS.json'))])
mp=D/'delivery_manifest.json';m=json.loads(mp.read_text())
for a in m['attachments']:
 if a['path'] in newpackages:a.update({k:newpackages[a['path']][k] for k in ['bytes','sha256']})
mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n');zp=D/'zip_content_manifest.json';z=json.loads(zp.read_text());z['packages']=[newpackages.get(x['path'],x) for x in z['packages']];zp.write_text(json.dumps(z,ensure_ascii=False,indent=2)+'\n')
for x in newpackages.values():print({k:x[k] for k in ['path','bytes','sha256','member_count']})
