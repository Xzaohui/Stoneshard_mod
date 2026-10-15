from pathlib import Path
import json,hashlib,zipfile,tempfile,datetime,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'independent_eighth_new_character_actions_evidence';mp=r/sys.argv[1];j=json.loads(mp.read_text());phase=sys.argv[2] if len(sys.argv)>2 else j['stage'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)};errors=[];ex=Path(tempfile.mkdtemp(prefix='independent_eighth_wuer_kuqi_'+phase+'_'));allmembers={};reports=[]
for zrow in j['packages']:
 zp=r/zrow['path'];expected={row['path']:row for row in zrow['members']};report={**fp(zp),'under_18MiB':zp.stat().st_size<18*1024*1024,'members':[]}
 if sha(zp)!=zrow['sha256'] or zp.stat().st_size!=zrow['bytes'] or not report['under_18MiB']:errors.append(['archive_bytes_sha',str(zp)])
 with zipfile.ZipFile(zp) as z:
  ns=[x for x in z.namelist() if not x.endswith('/')];report['CRC_pass']=z.testzip() is None
  if not report['CRC_pass']:errors.append(['CRC',zp.name])
  if len(ns)!=len(set(ns)) or set(ns)-{'PACKAGE_CONTENTS.json'}!=set(expected):errors.append(['member_set',zp.name])
  for n in ns:
   if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError('unsafe path')
   data=z.read(n);dest=ex/zp.stem/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);h=hashlib.sha256(data).hexdigest()
   if n=='PACKAGE_CONTENTS.json':
    report['metadata']={'bytes':len(data),'sha256':h};continue
   row=expected[n];src=r/n;ok=src.is_file() and len(data)==row['bytes']==src.stat().st_size and h==row['sha256']==sha(src)==sha(dest)
   if not ok:errors.append(['member_bytes_sha',zp.name,n])
   if n in allmembers:errors.append(['cross_archive_duplicate',n])
   allmembers[n]=row;report['members'].append({'path':n,'bytes':len(data),'sha256':h,'CRC32':f'{z.getinfo(n).CRC:08x}','extracted_matches_source':ok})
 reports.append(report)
for slug in ['wuer','kuqi']:
 tree=r/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';fs={str(p.relative_to(r)):p for p in tree.rglob('*') if p.is_file()};missing=set(fs)-set(allmembers)
 if missing:errors.append(['source_tree_omitted',slug,sorted(missing)])
 m=json.loads((tree/'manifest.json').read_text());inv={v['path']:v for v in m['files']};actual={str(p.relative_to(tree)):p for p in tree.rglob('*') if p.is_file()}
 if set(inv)!=set(actual)-{'manifest.json','FINAL_STATUS.json'}:errors.append(['character_manifest_set',slug])
 for n,row in inv.items():
  p=tree/n
  if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append(['character_manifest_row',slug,n])
 # The copied source hashes refer to both original and planning snapshot.
 for row in json.loads((tree/'source_hashes.json').read_text()):
  for k in ['path','snapshot_path']:
   if k not in row:continue
   p=r/row[k]
   if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append(['source_hash_record',slug,row[k]])
planning=a/'eighth_new_character_actions_sources';copied=mp.parent/'planning_sources'
for src in planning.rglob('*'):
 if src.is_file():
  p=copied/src.relative_to(planning)
  if not p.is_file() or sha(p)!=sha(src) or str(p.relative_to(r)) not in allmembers:errors.append(['planning_copy_omitted_or_changed',str(src)])
vg=json.loads((a/'independent_eighth_new_character_actions_wuer_kuqi_visual_gate_20261014.json').read_text())
for pose in vg['selected']:
 p=r/pose['selected_file']['path']
 if sha(p)!=pose['selected_file']['sha256']:errors.append(['selected_changed',str(p)])
for at in vg['attempts']:
 for row in at['files']:
  p=r/row['path']
  if not p.is_file() or sha(p)!=row['sha256'] or str(p.relative_to(r)) not in allmembers:errors.append(['attempt_source_changed_or_omitted',row['path']])
protected=0
for f in ['old_source_baseline.json','planning_frozen_baseline.json']:
 for row in json.loads((e/f).read_text())['files']:
  p=r/row['path'];protected+=1
  if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append(['protected_changed',row['path']])
out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'group':'wuer_kuqi','phase':phase,'status':'pass' if not errors else 'fail','manifest':fp(mp),'archives':reports,'all_sources_member_count':len(allmembers),'all_archives_independently_openable':True,'every_member_actually_extracted':True,'extraction_directory':str(ex),'selected_count':len(vg['selected']),'complete_toolreturn_payload_count':sum(n.endswith('_tool_return.json') for n in allmembers),'protected_files_checked':protected,'errors':errors,'scope':'Independent complete-tree/source-snapshot closure plus actual ZIP extraction, CRC, member bytes and SHA; no upload or author data mutation.'};op=e/f'wuer_kuqi_{phase}_package_gate.json';op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'gate':fp(op),'status':out['status'],'members':len(allmembers),'archives':len(reports),'errors':errors},ensure_ascii=False));assert not errors
