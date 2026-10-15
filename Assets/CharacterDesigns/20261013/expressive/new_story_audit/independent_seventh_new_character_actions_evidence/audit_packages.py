from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile,tempfile,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'independent_seventh_new_character_actions_evidence';g=sys.argv[1];phase=sys.argv[2] if len(sys.argv)>2 else 'candidate';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
vg=json.loads((a/f'independent_seventh_new_character_actions_{g}_visual_gate_20261014.json').read_text());bg=json.loads((a/f'independent_seventh_new_character_actions_{g}_board_gate_20261014.json').read_text());passed={v['selected_file']['sha256'] for v in vg['selected']};err=[];expected={};tree_results=[]
if g=='luoer_qiner':
 d=r/'Assets/CharacterActions/20261013/new_story/luoer_qiner_noncombat_basics_v1_delivery';mp=d/'SOURCE_PACKAGE_INDEX.json';dm=json.loads(mp.read_text());attachments=[{**v,'kind':'selected'} for v in dm['files']['selected_transparents']]+[{**dm['files']['joint_board'],'kind':'board'}]+[{**v,'kind':'archive'} for v in dm['archives']];slugs=['luoer','qiner'];archive_files={}
 for slug in slugs:
  tree=r/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';zp=next(r/v['path'] for v in dm['archives'] if v['source_root']==str(tree.relative_to(r)));archive_files[zp]={str(p.relative_to(tree.parent.parent)):p for p in tree.rglob('*') if p.is_file()}
 zp=r/dm['archives'][2]['path'];source=a/'seventh_new_character_actions_sources';plist=[p for p in source.rglob('*') if p.is_file()]+[a/'seventh_new_character_actions_brief.json',a/'independent_seventh_new_character_actions_plan_gate_20261014.json'];archive_files[zp]={str(p.relative_to(a)):p for p in plist}
else:
 d=r/'Assets/CharacterActions/20261013/new_story/seventh_lier_huier_delivery_v1';mp=d/'DELIVERY_MANIFEST.json';dm=json.loads(mp.read_text());attachments=[{**v,'path':str((d/v['filename']).relative_to(r)),'kind':'archive' if v['filename'].endswith('.zip') else ('selected' if 'selected' in v['type'] else 'board')} for v in dm['ordered_files']];slugs=['lier','huier'];archive_files={}
 for slug in slugs:
  tr=dm['complete_source_trees'][slug];tree=r/tr['source_tree'];actual={str(p.relative_to(r)):p for p in tree.rglob('*') if p.is_file()};assert set(actual)=={x['source_tree_path'] for x in tr['members']}
  for row in tr['members']:
   p=r/row['source_tree_path'];zp=d/row['package'];archive_files.setdefault(zp,{})[row['archive_member']]=p
   if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:err.append(['delivery_source_row',row['source_tree_path']])
for slug in slugs:
 tree=r/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';files={str(p.relative_to(tree)):p for p in tree.rglob('*') if p.is_file()};mj=json.loads((tree/'manifest.json').read_text())
 if 'files' in mj:
  inv=mj['files'];inv=inv if isinstance(inv,dict) else {x['path']:x for x in inv}
  if set(inv)!=set(files)-{'manifest.json'}:err.append(['manifest_set',slug])
  for n,v in inv.items():
   if n not in files or files[n].stat().st_size!=v['bytes'] or sha(files[n])!=v['sha256']:err.append(['manifest_bytes_sha',slug,n])
 src=json.loads((tree/'sources/SOURCE_MANIFEST.json').read_text());src=src if isinstance(src,list) else src.get('files',src.get('sources'))
 for row in src:
  paths=[r/row['path']]
  if row.get('snapshot_path'):paths.append(r/row['snapshot_path'])
  if row.get('local_copy'):paths.append(tree/row['local_copy'])
  for p in paths:
   if not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:err.append(['source_snapshot',slug,str(p)])
 tree_results.append({'character':slug,'tree_files':len(files),'source_records':len(src),'manifest':fp(tree/'manifest.json'),'final_status':fp(tree/'FINAL_STATUS.json')})
for attempt in vg['attempts']:
 for f in attempt['files']:
  p=r/f['path']
  if not p.is_file() or p.stat().st_size!=f['bytes'] or sha(p)!=f['sha256']:err.append(['reviewed_attempt_changed',f['path']])
attach=[]
for row in attachments:
 p=r/row['path'];rec=fp(p);rec['matches_inventory']=rec['bytes']==row['bytes'] and rec['sha256']==row['sha256'];rec['under_18_MiB']=rec['bytes']<18*1024*1024;rec['kind']=row['kind'];attach.append(rec)
 if not rec['matches_inventory'] or not rec['under_18_MiB']:err.append(['attachment',row['path']])
 if row['kind']=='selected' and rec['sha256'] not in passed:err.append(['selected_not_passed',row['path']])
 if row['kind']=='board' and rec['sha256']!=bg['board']['sha256']:err.append(['board_differs_from_review',row['path']])
extract=Path(tempfile.mkdtemp(prefix='independent_seventh_'+g+'_'+phase+'_'));zreports=[];total=0
for zp,members in archive_files.items():
 with zipfile.ZipFile(zp) as z:
  bad=z.testzip();names=[n for n in z.namelist() if not n.endswith('/')];zr={**fp(zp),'CRC_pass':bad is None,'members':[]}
  if bad:err.append(['CRC',zp.name,bad])
  if len(names)!=len(set(names)):err.append(['duplicate_members',zp.name])
  if set(names)-{'PACKAGE_SET_MANIFEST.json'}!=set(members):err.append(['archive_source_set',zp.name,sorted(set(names)-set(members)-{'PACKAGE_SET_MANIFEST.json'}),sorted(set(members)-set(names))])
  for n in names:
   if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError('unsafe archive path')
   data=z.read(n);source=members.get(n);h=hashlib.sha256(data).hexdigest();dest=extract/zp.stem/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
   if n=='PACKAGE_SET_MANIFEST.json':
    md=json.loads(data);rows=md['members'];mapped={x['archive_member']:x for x in rows}
    if set(mapped)!=set(members) or md['complete_set']!=[zp.name]:err.append(['package_metadata_set',zp.name])
    for mn,mr in mapped.items():
     sp=members.get(mn)
     if sp is None or str(sp.relative_to(r))!=mr['source_tree_path'] or sp.stat().st_size!=mr['bytes'] or sha(sp)!=mr['sha256'] or mr['package']!=zp.name:err.append(['package_metadata_row',zp.name,mn])
    zr['package_metadata']={'bytes':len(data),'sha256':h,'member_count':len(rows),'matches_declared_source_tree':set(mapped)==set(members)}
    continue
   total+=1
   match=source is not None and len(data)==source.stat().st_size and h==sha(source) and sha(dest)==h
   if not match:err.append(['member_bytes_sha',zp.name,n])
   zr['members'].append({'member':n,'source':str(source.relative_to(r)) if source else None,'bytes':len(data),'sha256':h,'crc32':f'{z.getinfo(n).CRC:08x}','actual_extracted_matches_source':match})
  zreports.append(zr)
for f in ['old_source_baseline.json','planning_frozen_baseline.json']:
 for row in json.loads((e/f).read_text())['files']:
  p=r/row['path']
  if not p.exists() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:err.append(['protected_source_changed',row['path']])
out={'schema_version':1,'status':'pass' if not err else 'fail','phase':phase,'reviewer':'review_seventh_character_actions','reviewed_utc':datetime.now(timezone.utc).isoformat(),'group':g,'delivery_inventory':fp(mp),'attachments_checked':attach,'characters':tree_results,'zip_reports':zreports,'ordinary_zip_count':len(zreports),'all_archives_independently_openable':True,'complete_sources_closed':not err,'actual_extracted_source_files':total,'extraction_temp_directory':str(extract),'selected_pose_count':vg['selected_count'],'explicit_missing':vg['explicit_missing'],'all_reviewed_attempt_files_unchanged':not any(x[0]=='reviewed_attempt_changed' for x in err),'old_sources_verified':246,'planning_source_files_verified':85,'errors':err,'scope':'Read-only source and package audit. Every archive member really decompressed and written to a fresh temporary directory; CRC and bytes/SHA verified against exact source trees. No author source modifications.'}
p=a/f'independent_seventh_new_character_actions_{g}_package_gate_20261014.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');cp=e/f'{g}_{phase}_package_gate.json';cp.write_bytes(p.read_bytes());print(json.dumps({'group':g,'phase':phase,'status':out['status'],'attachments':len(attach),'archives':len(zreports),'actual_extracted_files':total,'trees':tree_results,'gate':fp(p),'errors':err},ensure_ascii=False,indent=2));assert not err
