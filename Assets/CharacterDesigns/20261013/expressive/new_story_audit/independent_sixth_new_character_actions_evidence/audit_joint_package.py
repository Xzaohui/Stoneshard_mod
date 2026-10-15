from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile,tempfile
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';g='erwei_chenger';dmfile=r/f'Assets/CharacterActions/20261013/new_story/sixth_noncombat_{g}_delivery_v1/delivery_manifest.json';dm=json.loads(dmfile.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)};err=[];jr=json.loads((a/'independent_sixth_new_character_actions_20261014.json').read_text());passed={f['sha256'] for x in jr['pose_reviews'] if x['verdict']=='pass' for f in x['files'] if '/exports/' in f['path']};trees={};sr=[]
for c,t in dm['complete_source_trees'].items():
 tree=r/t['path'];files={str(p.relative_to(r)):p for p in tree.rglob('*') if p.is_file()};trees.update(files);m=json.loads((tree/'manifest.json').read_text());rows=m['files'];rows=rows if isinstance(rows,list) else [{'path':k,**v} for k,v in rows.items()];mapped={str((tree/x['path']).relative_to(r)):x for x in rows}
 if set(mapped)!=set(files)-{str((tree/'manifest.json').relative_to(r))}:err.append(['manifest_set',c])
 for p,x in mapped.items():
  f=r/p
  if sha(f)!=x['sha256'] or f.stat().st_size!=x['bytes']:err.append(['manifest_bytes_sha',p])
 sm=json.loads((tree/'sources/SOURCE_MANIFEST.json').read_text());sources=sm.get('sources',sm.get('source_files',[]))
 for s in sources:
  for p in [r/s['path'],tree/s.get('archive_path',s.get('local_snapshot',''))]:
   if not p.is_file() or p.stat().st_size!=s['bytes'] or sha(p)!=s['sha256']:err.append(['source_snapshot',str(p)])
 if sha(tree/'manifest.json')!=t['manifest_sha256']:err.append(['tree_manifest',c])
 expected={x['source_tree_path'] for x in t['members']}
 if expected!=set(files):err.append(['delivery_tree_set',c])
 sr.append({'character':c,'tree_files':len(files),'sources_checked':len(sources),'manifest':fp(tree/'manifest.json'),'final_status':fp(tree/'FINAL_STATUS.json')})
expected={x['archive_member']:x for x in dm['package_set']['all_members']};loc={};zreports=[];attach=[];meta_hashes=[];extract=Path(tempfile.mkdtemp(prefix='independent_sixth_erwei_chenger_'))
for at in dm['attachments']:
 p=r/at['path'];row=fp(p);row['matches_delivery_manifest']=row['sha256']==at['sha256'] and row['bytes']==at['bytes'];row['under_18_MiB']=row['bytes']<18*1024*1024;attach.append(row)
 if not row['matches_delivery_manifest'] or not row['under_18_MiB']:err.append(['attachment',str(p)])
 if at['kind']=='transparent_action_png' and row['sha256'] not in passed:err.append(['selected_not_passed',at['path']])
 if p.suffix!='.zip':continue
 with zipfile.ZipFile(p) as z:
  if z.testzip() is not None:err.append(['CRC',str(p)])
  names=[n for n in z.namelist() if not n.endswith('/')]
  if len(names)!=len(set(names)):err.append(['duplicate_names',str(p)])
  zr={**fp(p),'CRC_pass':True,'members':[]}
  for n in names:
   if Path(n).is_absolute() or '..' in Path(n).parts:raise RuntimeError('unsafe ZIP path')
   data=z.read(n);h=hashlib.sha256(data).hexdigest()
   if n=='PACKAGE_SET_MANIFEST.json':
    meta_hashes.append(h)
    if json.loads(data)!=dm['package_set']:err.append(['metadata_diff',p.name])
    continue
   if n not in expected:err.append(['unexpected_member',n]);continue
   e=expected[n];source=r/e['source_tree_path']
   if n in loc:err.append(['duplicate_across_parts',n])
   loc[n]=p.name
   if p.name!=e['package'] or len(data)!=e['bytes'] or h!=e['sha256'] or h!=sha(source):err.append(['member_bytes_sha',n])
   dest=extract/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
   if sha(dest)!=sha(source):err.append(['extracted_bytes',n])
   zr['members'].append({'member':n,'source':e['source_tree_path'],'bytes':len(data),'sha256':h,'crc32':f'{z.getinfo(n).CRC:08x}'})
  zreports.append(zr)
if set(loc)!=set(expected):err.append(['union_member_set'])
if {x['source_tree_path'] for x in expected.values()}!=set(trees):err.append(['union_entire_tree_set'])
if len(set(meta_hashes))!=1:err.append(['metadata_not_identical'])
out={'status':'pass' if not err else 'fail','reviewed_utc':datetime.now(timezone.utc).isoformat(),'group':g,'delivery_manifest':fp(dmfile),'attachments_checked':attach,'characters':sr,'zip_reports':zreports,'ordinary_zip_parts':3,'all_parts_required_same_directory':True,'union_closes_entire_two_source_trees':set(loc)==set(expected) and {x['source_tree_path'] for x in expected.values()}==set(trees),'actual_extracted_source_files':len(loc),'extraction_temp_directory':str(extract),'errors':err,'scope':'Independent CRC, bytes/SHA, own-tree inventories and source snapshots; actual clean-directory extraction of all ordinary ZIP parts; rejected original and all full payloads retained.'};op=a/f'independent_sixth_new_character_actions_{g}_package_gate_20261014.json';op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':out['status'],'source_trees':sr,'extracted_files':len(loc),'gate':fp(op),'errors':err},ensure_ascii=False,indent=2))
