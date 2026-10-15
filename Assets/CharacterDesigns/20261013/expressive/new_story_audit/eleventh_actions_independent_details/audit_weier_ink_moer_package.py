from pathlib import Path
import json,hashlib,zipfile,datetime,re,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'eleventh_actions_independent_details';d=r/'Assets/CharacterActions/20261013/new_story/eleventh_noncombat_weier_ink_moer_delivery_v1';stage=sys.argv[1] if len(sys.argv)>1 else 'candidate';mp=d/(sys.argv[2] if len(sys.argv)>2 else 'candidate_package_manifest.json');j=json.loads(mp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[];members=[];pkgs=[]
def ck(k,ok,**x):checks.append({'kind':k,'pass':bool(ok),**x})
for s in ['weier_ink','moer']:
 cd=d.parent/s/'noncombat_basics_v1';m=json.loads((cd/'manifest.json').read_text());mf={x['path'] for x in m['files']};actual={str(p.relative_to(cd)) for p in cd.rglob('*') if p.is_file()}-{'manifest.json','FINAL_STATUS.json'};ck('full_character_manifest_coverage',mf==actual,slug=s,missing=sorted(actual-mf),extra=sorted(mf-actual))
 for row in m['files']:
  p=cd/row['path'];ck('character_manifest_entry',p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],path=str(p.relative_to(r)))
 for row in json.loads((cd/'source_hashes.json').read_text()):
  p=r/row['source_path'];q=r/row['snapshot'];ck('source_snapshot_pair',p.is_file() and q.is_file() and p.stat().st_size==q.stat().st_size==row['bytes'] and sha(p)==sha(q)==row['sha256'],path=row['source_path'])
 for p in (cd/'raw').glob('*tool_return.json'):
  ret=json.loads(p.read_text());hints=re.findall(r'/workspace/[^\s]+\.png',ret.get('output_hint',''));raw=p.with_name(p.name.replace('_tool_return.json','_raw.png'));ck('tool_original_png_matches_raw',len(hints)==1 and Path(hints[0]).is_file() and sha(Path(hints[0]))==sha(raw),raw=str(raw.relative_to(r)),original=hints)
for row in j['packages']:
 p=r/row['path'];ck('zip_archive_sha_size_and_limit',p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'] and p.stat().st_size<18*1024*1024,path=row['path']);names=[]
 with zipfile.ZipFile(p) as z:
  ck('zip_crc_all_members',z.testzip() is None,path=row['path']);names=z.namelist();expected={x['path']:x for x in row['members']};ck('zip_inventory_exact',set(names)==set(expected)|{'PACKAGE_CONTENTS.json'} and len(names)==len(set(names))==row['member_count'],path=row['path'])
  for n in names:
   if n=='PACKAGE_CONTENTS.json':
    ck('internal_package_contents_matches_manifest',json.loads(z.read(n))['members']==row['members'],archive=row['path']);continue
   bs=z.read(n);local=r/n;h=hashlib.sha256(bs).hexdigest();q=expected[n];ck('zip_extracted_member_local_and_manifest_byte_identity',local.is_file() and local.read_bytes()==bs and h==q['sha256'] and len(bs)==q['bytes'],path=n);members.append(n)
 pkgs.append({'path':row['path'],'bytes':p.stat().st_size,'sha256':sha(p),'member_count':len(names)})
ck('package_union_no_duplicate_members',len(members)==len(set(members))==j['all_files_count'])
for s in ['weier_ink','moer']:
 cd=d.parent/s/'noncombat_basics_v1';required={str(p.relative_to(r)) for p in cd.rglob('*') if p.is_file()};ck('whole_character_tree_in_packages',required<=set(members),slug=s,missing=sorted(required-set(members)))
for row in json.loads((d/'selected_files.json').read_text()):ck('selected_matches_independently_reviewed_sha',sha(r/row['path'])==row['sha256'],path=row['path'])
fails=[x for x in checks if not x['pass']];out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'stage':stage,'verdict':'pass' if not fails else 'fail','package_manifest':{'path':str(mp.relative_to(r)),'bytes':mp.stat().st_size,'sha256':sha(mp)},'packages':pkgs,'checks':checks,'failures':fails,'source_member_count':len(members),'notes':['Every member actually decompressed and byte-compared with local source; zipfile.testzip CRC passed.','Complete imagegen returned image payloads and original tool-generated PNG identity independently checked; no return JSON removed to meet size threshold.','Candidate packaging PASS does not replace final freeze readback.']};p=e/(stage+'_weier_ink_moer_package_audit.json');p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'path':str(p.relative_to(r)),'sha256':sha(p),'checks':len(checks),'members':len(members),'packages':pkgs,'failures':fails},ensure_ascii=False));assert not fails
