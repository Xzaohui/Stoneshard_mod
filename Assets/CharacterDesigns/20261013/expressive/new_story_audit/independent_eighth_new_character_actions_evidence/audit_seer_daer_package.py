from pathlib import Path
import json,hashlib,zipfile,tempfile,datetime
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'independent_eighth_new_character_actions_evidence';d=r/'Assets/CharacterActions/20261013/new_story/eighth_noncombat_seer_daer_delivery_v1';mp=d/'delivery_manifest.json';dm=json.loads(mp.read_text());zp=d/'zip_content_manifest.json';j=json.loads(zp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)};errors=[];ex=Path(tempfile.mkdtemp(prefix='independent_eighth_seer_daer_final_'));allmembers={};reports=[]
for zrow in j['packages']:
 zp=r/zrow['path'];expected={row['path']:row for row in zrow['members']};report={**fp(zp),'under_18MiB':zp.stat().st_size<18*1024*1024,'members':[]}
 if sha(zp)!=zrow['sha256'] or zp.stat().st_size!=zrow['bytes'] or not report['under_18MiB']:errors.append(['archive_bytes_sha',str(zp)])
 with zipfile.ZipFile(zp) as z:
  ns=[x for x in z.namelist() if not x.endswith('/')];report['CRC_pass']=z.testzip() is None
  if not report['CRC_pass']:errors.append(['CRC',zp.name])
  if len(ns)!=len(set(ns)) or set(ns)!=set(expected):errors.append(['member_set',zp.name])
  for n in ns:
   if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError('unsafe path')
   data=z.read(n);dest=ex/zp.stem/n;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);h=hashlib.sha256(data).hexdigest();row=expected[n];src=r/n;ok=src.is_file() and len(data)==row['bytes']==src.stat().st_size and h==row['sha256']==sha(src)==sha(dest)
   if not ok:errors.append(['member_bytes_sha',zp.name,n])
   if n in allmembers:errors.append(['cross_archive_duplicate',n])
   allmembers[n]=row;report['members'].append({'path':n,'bytes':len(data),'sha256':h,'CRC32':f'{z.getinfo(n).CRC:08x}','extracted_matches_source':ok})
 reports.append(report)
for slug in ['seer','daer']:
 tree=r/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';fs={str(p.relative_to(r)):p for p in tree.rglob('*') if p.is_file()};missing=set(fs)-set(allmembers)
 if missing:errors.append(['source_tree_omitted',slug,sorted(missing)])
 m=json.loads((tree/'manifest.json').read_text());inv={v['path']:v for v in m['files']}
 if set(inv)!=set(fs)-{str((tree/'manifest.json').relative_to(r)),str((tree/'FINAL_STATUS.json').relative_to(r))}:errors.append(['character_manifest_set',slug])
 for n,row in inv.items():
  p=r/n
  if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append(['character_manifest_row',slug,n])
 for row in json.loads((tree/'sources/source_index.json').read_text())['complete_file_index']:
  for p in [r/row['original'],tree/row['snapshot']]:
   if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append(['source_hash_record',slug,str(p)])
 f=json.loads((tree/'FINAL_STATUS.json').read_text())
 if sha(tree/'manifest.json')!=f['manifest_sha256'] or f['selected_pass_count']!=2:errors.append(['final_status',slug])
 for row in f['frozen_files']:
  p=r/row['path']
  if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append(['final_frozen_member',slug,row['path']])
for p in (a/'eighth_new_character_actions_sources').rglob('*'):
 if p.is_file() and str(p.relative_to(r)) not in allmembers:errors.append(['planning_source_omitted',str(p)])
vg=json.loads((a/'independent_eighth_new_character_actions_seer_daer_visual_gate_20261014.json').read_text());anc={x['path']:x['current'] for x in vg['ancillary_qa_status_updates']}
for at in vg['attempts']:
 for row in at['files']:
  row=anc.get(row['path'],row);p=r/row['path']
  if not p.is_file() or sha(p)!=row['sha256'] or str(p.relative_to(r)) not in allmembers:errors.append(['attempt_source_changed_or_omitted',row['path']])
protected=0
for f in ['old_source_baseline.json','planning_frozen_baseline.json']:
 for row in json.loads((e/f).read_text())['files']:
  p=r/row['path'];protected+=1
  if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errors.append(['protected_changed',row['path']])
att=[];passed={v['selected_file']['sha256'] for v in vg['selected']};board_sha=json.loads((a/'independent_eighth_new_character_actions_seer_daer_board_gate_20261014.json').read_text())['board']['sha256']
for row in dm['attachments']:
 p=r/row['path'];rec={**fp(p),'order':row['order'],'kind':row['kind'],'under_18MiB':p.stat().st_size<18*1024*1024};att.append(rec)
 if rec['bytes']!=row['bytes'] or rec['sha256']!=row['sha256'] or not rec['under_18MiB']:errors.append(['attachment',row['path']])
 if row['kind']=='transparent_action_png' and sha(p) not in passed:errors.append(['selected_attachment',row['path']])
 if row['kind']=='joint_mother_action_light_dark_board' and sha(p)!=board_sha:errors.append(['board_attachment',row['path']])
out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'group':'seer_daer','phase':'final','status':'pass' if not errors else 'fail','delivery_manifest':fp(mp),'attachments':att,'archives':reports,'all_sources_member_count':len(allmembers),'all_archives_independently_openable':True,'every_member_actually_extracted':True,'extraction_directory':str(ex),'selected_count':len(vg['selected']),'complete_toolreturn_payload_count':sum(n.endswith('_tool_return.json') for n in allmembers),'failed_daer_A1_v1_retained_with_payload':any(n.endswith('daer_A1_smooth_left_forearm_sleeve_v1_tool_return.json') for n in allmembers),'protected_files_checked':protected,'errors':errors,'scope':'Complete source trees, all planning sources, actual ZIP extraction and CRC/bytes/SHA. Frozen selected and board match independent visual gates; no uploads or author mutations.'};op=a/'independent_eighth_new_character_actions_seer_daer_package_gate_20261014.json';op.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'gate':fp(op),'status':out['status'],'members':len(allmembers),'archives':len(reports),'errors':errors},ensure_ascii=False));assert not errors
