from pathlib import Path
import json,hashlib,zipfile,sys,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');ROOT=R/'Assets/CharacterActions/20261013/new_story';D=ROOT/'eleventh_noncombat_daier_moer_trs_delivery_v1';mode=sys.argv[1];assert mode in ['preflight','final'];tag=sys.argv[2] if len(sys.argv)>2 else mode;Z=D/('preflight_archives' if mode=='preflight' else 'source_zips');Z.mkdir(exist_ok=True);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();out=[]
for slug in ['daier','moer_trs']:
 b=ROOT/slug/'noncombat_basics_v1';ps=[p for p in sorted(b.rglob('*')) if p.is_file()];groups=[ps]
 # Preserve every member, bound each ZIP conservatively at 15MiB uncompressed.
 if sum(p.stat().st_size for p in ps)>18*1024*1024:
  groups=[];batch=[];n=0
  for p in ps:
   if batch and n+p.stat().st_size>15*1024*1024:groups.append(batch);batch=[];n=0
   batch.append(p);n+=p.stat().st_size
  if batch:groups.append(batch)
 for i,files in enumerate(groups,1):
  name=f'{slug}_actions_complete_source'+(f'_part{i}of{len(groups)}' if len(groups)>1 else '')+f'_{tag}.zip';p=Z/name;assert not p.exists(),p
  with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for f in files:z.write(f,str(f.relative_to(R)))
  with zipfile.ZipFile(p) as z:
   assert z.testzip() is None;assert len(z.namelist())==len(files)
   for f in files:assert hashlib.sha256(z.read(str(f.relative_to(R)))).hexdigest()==sha(f)
  assert p.stat().st_size<18*1024*1024
  out.append({'character':slug,'path':str(p.relative_to(D)),'bytes':p.stat().st_size,'sha256':sha(p),'members':[{'repo_path':str(f.relative_to(R)),'sha256':sha(f),'bytes':f.stat().st_size} for f in files],'crc_test':'PASS','all_members_equal_disk':True})
(D/f'{tag.upper()}_PACKAGE_MANIFEST.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'phase':mode,'all_character_tree_members_included':True,'zips':out},ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{k:v for k,v in e.items() if k!='members'} for e in out],ensure_ascii=False,indent=2))
