from pathlib import Path
from collections import defaultdict
from datetime import datetime,timezone
import json,hashlib,zipfile,sys
root=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');A=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def fp(p):return {'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':sha(p)}
def rows(d):
 if isinstance(d,list):return d
 return [{'path':p,**v} for p,v in d.items()]
group,dmname=sys.argv[1:3];dmp=root/dmname;dm=json.loads(dmp.read_text());jr=json.loads((A/'independent_sixth_new_character_actions_20261014.json').read_text());passed={next(f for f in r['files'] if '/exports/' in f['path'])['sha256'] for r in jr['pose_reviews'] if r['verdict']=='pass'}
errors=[];attchecks=[];zipgroups=defaultdict(list)
attachments=dm.get('attachments') or [{**a,'path':str((dmp.parent/a['filename']).relative_to(root)),'kind':a.get('type','')} for a in dm['ordered_files']]
for a in attachments:
 p=root/a['path'];rec=fp(p);ok=rec['bytes']==a['bytes'] and rec['sha256']==a['sha256'];rec.update(matches_delivery_manifest=ok,under_18_MiB=rec['bytes']<18*1024*1024)
 if not ok or not rec['under_18_MiB']:errors.append(['attachment',a['path']])
 if p.suffix=='.png' and ('transparent' in a.get('kind','') or rec['sha256'] in passed):
  rec['matches_passed_visual_selected']=rec['sha256'] in passed
  if not rec['matches_passed_visual_selected']:errors.append(['selected_not_passed',a['path']])
 if p.suffix=='.zip':zipgroups[a['character']].append(p)
 attchecks.append(rec)
results=[]
for c,zpaths in zipgroups.items():
 tree=root/'Assets/CharacterActions/20261013/new_story'/c/'noncombat_basics_v1';tfiles={str(p.relative_to(tree)):p for p in tree.rglob('*') if p.is_file()};mf=json.loads((tree/'manifest.json').read_text());local=[]
 if 'files' in mf:
  inv_name='manifest.json';mrows=rows(mf['files']);excluded={inv_name}
 elif (tree/'FILES_SHA256.json').exists():
  inv_name='FILES_SHA256.json';mrows=rows(json.loads((tree/inv_name).read_text())['files']);excluded={inv_name}
 else:
  inv_name='external DELIVERY_MANIFEST complete_source_trees';mrows=[{**r,'path':str((root/r['source_tree_path']).relative_to(tree))} for r in dm['complete_source_trees'][c]['members']];excluded=set()
 mmap={r['path']:r for r in mrows}
 if set(mmap)!=set(tfiles)-excluded:local.append(['inventory_tree_set',sorted(set(tfiles)-excluded-set(mmap)),sorted(set(mmap)-set(tfiles))])
 for n,r in mmap.items():
  p=tree/n
  if not p.is_file() or p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']:local.append(['inventory_bytes_sha',n])
 aliases={}
 for n,p in tfiles.items():
  for alias in [n,str(p.relative_to(root)),str(p.relative_to(tree.parent.parent))]:aliases[alias]=n
 union={};zipreports=[];dupes=[];package_metadata=[];actual_locations={}
 for zp in zpaths:
  zr={**fp(zp),'members':[]};zerrors=[]
  with zipfile.ZipFile(zp) as z:
   crc=z.testzip();names=[n for n in z.namelist() if not n.endswith('/')]
   if crc:zerrors.append(['CRC',crc])
   if len(names)!=len(set(names)):zerrors.append(['duplicate_member_names'])
   for n in names:
    b=z.read(n);h=hashlib.sha256(b).hexdigest()
    if n=='PACKAGE_SET_MANIFEST.json':
     package_metadata.append({'zip':zp.name,'sha256':h,'bytes':len(b),'data':json.loads(b)});continue
    actual_locations[n]=zp.name
    rec={'member':n,'bytes':len(b),'sha256':h,'crc32':f'{z.getinfo(n).CRC:08x}'};rel=aliases.get(n);rec['source_tree_relative_path']=rel
    if rel is None:zerrors.append(['unexpected_member',n])
    elif len(b)!=tfiles[rel].stat().st_size or h!=sha(tfiles[rel]):zerrors.append(['member_bytes_sha',n])
    else:
     if rel in union:
      dupes.append(rel)
      if union[rel]!=(len(b),h):zerrors.append(['conflicting_member_across_parts',n])
     union[rel]=(len(b),h)
    zr['members'].append(rec)
  zr.update(crc_all_pass=crc is None,errors=zerrors);local+=zerrors;zipreports.append(zr)
 for pm in package_metadata:
  md=pm['data']
  if md['character']!=c or set(md['complete_set'])!={p.name for p in zpaths}:local.append(['package_set_metadata',pm['zip']])
  expected_members={r['archive_member']:r for r in md['all_members']}
  if set(expected_members)!=set(actual_locations):local.append(['package_metadata_member_set',pm['zip']])
  for name,r in expected_members.items():
   f=root/r['source_tree_path']
   if not f.is_file() or f.stat().st_size!=r['bytes'] or sha(f)!=r['sha256'] or actual_locations.get(name)!=r['package']:local.append(['package_metadata_member',name])
 if len({pm['sha256'] for pm in package_metadata})>1:local.append(['package_metadata_not_identical_across_parts'])
 if set(union)!=set(tfiles):local.append(['zip_union_tree_set',sorted(set(tfiles)-set(union)),sorted(set(union)-set(tfiles))])
 sm=json.loads((tree/'sources/SOURCE_MANIFEST.json').read_text());srows=sm.get('files',sm.get('sources',sm.get('source_files',[]))) if isinstance(sm,dict) else sm
 for r in srows:
  for p in [root/r['path'],tree/r.get('package_path',r.get('local_snapshot',r.get('archive_path',r.get('snapshot_path',''))))]:
   if not p.is_file() or p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']:local.append(['source_original_or_snapshot',str(p)])
 fs=json.loads((tree/'FINAL_STATUS.json').read_text());results.append({'character':c,'zip_count':len(zpaths),'zip_reports':zipreports,'tree_files':len(tfiles),'union_members':len(union),'identical_shared_members':sorted(set(dupes)),'package_metadata':[ {k:v for k,v in pm.items() if k!='data'} for pm in package_metadata],'union_closes_entire_tree':set(union)==set(tfiles),'inventory_file':inv_name,'sources_checked':len(srows),'manifest':fp(tree/'manifest.json'),'final_status':fp(tree/'FINAL_STATUS.json'),'errors':local});errors+=local
out={'status':'pass' if not errors else 'fail','reviewed_utc':datetime.now(timezone.utc).isoformat(),'group':group,'delivery_manifest':fp(dmp),'attachments_checked':attchecks,'characters':results,'errors':errors,'scope':'Complete frozen source tree and all selected assets; each ordinary ZIP checked for CRC and bytes/SHA, multipart sources checked by member union. No source files modified.'}
op=A/f'independent_sixth_new_character_actions_{group}_package_gate_20261014.json';op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'status':out['status'],'delivery_manifest':out['delivery_manifest'],'characters':[{'character':r['character'],'zip_count':r['zip_count'],'tree_files':r['tree_files'],'union_members':r['union_members'],'sources_checked':r['sources_checked'],'errors':r['errors']} for r in results],'errors':errors},ensure_ascii=False,indent=2))
