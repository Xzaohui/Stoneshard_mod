from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,zipfile
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'; e=a/'independent_seventh_new_character_actions_evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
load=lambda p:json.loads(p.read_text())
for g in ['lier_huier','luoer_qiner']:
 errors=[];protected={}
 def verify(row,p=None):
  p=p or r/row['path'];v=fp(p);protected[v['path']]=v
  if v['bytes']!=row['bytes'] or v['sha256']!=row['sha256']:errors.append(['bytes_sha',str(p)])
  return v
 pp=a/f'independent_seventh_new_character_actions_{g}_package_gate_20261014.json';pkg=load(pp);assert pkg['status']=='pass';protected[str(pp.relative_to(r))]=fp(pp)
 vgpath=a/f'independent_seventh_new_character_actions_{g}_visual_gate_20261014.json';vg=load(vgpath);protected[str(vgpath.relative_to(r))]=fp(vgpath)
 bp=a/f'independent_seventh_new_character_actions_{g}_board_gate_20261014.json';protected[str(bp.relative_to(r))]=fp(bp)
 if g=='lier_huier':
  d=r/'Assets/CharacterActions/20261013/new_story/seventh_lier_huier_delivery_v1';fr=d/'FREEZE.json';f=load(fr);mp=d/'DELIVERY_MANIFEST.json';m=load(mp);candidate=d/'DELIVERY_MANIFEST_CANDIDATE_REVIEWED.json';verify(pkg['delivery_inventory'],candidate);verify(f['delivery_manifest'])
  if f['independent_package_gate_sha256']!=sha(pp):errors.append(['freeze_gate_sha'])
  if f['ordered_files']!=m['ordered_files']:errors.append(['freeze_inventory_rows'])
  if m['complete_source_trees']!=load(candidate)['complete_source_trees']:errors.append(['frozen_source_tree_changed'])
  if f['source_tree_file_count']!=pkg['actual_extracted_source_files']:errors.append(['source_count'])
  attachments=[{'path':str((d/x['filename']).relative_to(r)),**x} for x in m['ordered_files']]
 else:
  d=r/'Assets/CharacterActions/20261013/new_story/luoer_qiner_noncombat_basics_v1_delivery';fr=d/'FREEZE_RECORD.json';f=load(fr);mp=d/'delivery_manifest.json';m=load(mp)
  for k in ['package_gate','source_package_index','ordered_delivery_manifest']:verify(f[k])
  verify(pkg['delivery_inventory'])
  if f['attachments']!=m['files']:errors.append(['freeze_inventory_rows'])
  attachments=m['files']
 protected[str(fr.relative_to(r))]=fp(fr);protected[str(mp.relative_to(r))]=fp(mp)
 expected={x['path']:(x['bytes'],x['sha256']) for x in pkg['attachments_checked']};actual={x['path']:(x['bytes'],x['sha256']) for x in attachments}
 if expected!=actual:errors.append(['frozen_attachments_differ_from_package_gate'])
 for x in attachments:verify(x)
 selected={x['sha256'] for x in pkg['attachments_checked'] if x['kind']=='selected'}
 if selected!={x['selected_file']['sha256'] for x in vg['selected']}:errors.append(['selected_set'])
 for z in pkg['zip_reports']:
  verify(z)
  with zipfile.ZipFile(r/z['path']) as zz:
   if zz.testzip() is not None:errors.append(['frozen_CRC',z['path']])
  for member in z['members']:verify({'path':member['source'],'bytes':member['bytes'],'sha256':member['sha256']})
 for c in pkg['characters']:
  tr=r/f"Assets/CharacterActions/20261013/new_story/{c['character']}/noncombat_basics_v1"
  expected_src={row['source'] for z in pkg['zip_reports'] for row in z['members'] if row['source'].startswith(str(tr.relative_to(r))+'/')}
  current={str(p.relative_to(r)) for p in tr.rglob('*') if p.is_file()}
  if expected_src!=current:errors.append(['frozen_source_set',c['character']])
 for baseline in ['old_source_baseline.json','planning_frozen_baseline.json']:
  for row in load(e/baseline)['files']:verify(row)
 out={'schema_version':1,'status':'pass_ready_for_library_save' if not errors else 'fail_do_not_save','reviewer':'review_seventh_character_actions','reviewed_utc':datetime.now(timezone.utc).isoformat(),'group':g,'author_freeze':fp(fr),'frozen_delivery_manifest':fp(mp),'immutable_package_gate':fp(pp),'visual_gate':fp(vgpath),'board_gate':fp(bp),'selected_count':vg['selected_count'],'explicit_missing':vg['explicit_missing'],'attachment_count':len(attachments),'archive_count':pkg['ordinary_zip_count'],'actual_extracted_source_files_in_package_gate':pkg['actual_extracted_source_files'],'all_source_trees_unchanged_since_actual_extraction':not errors,'all_archives_same_bytes_as_independently_extracted_and_CRC_rechecked':not errors,'all_delivery_files_unchanged':not errors,'old_source_count':246,'planning_source_count':85,'protected_files':sorted(protected.values(),key=lambda x:x['path']),'errors':errors,'status_precedence':'This final read-only byte gate resolves historical pending fields without rewriting author freezes, source trees, packages, or previously cited independent reports. Library upload and user delivery remain separate actions.'}
 outp=a/f'independent_seventh_new_character_actions_{g}_frozen_byte_gate_20261014.json';outp.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'group':g,'status':out['status'],'gate':fp(outp),'freeze':fp(fr),'manifest':fp(mp),'protected_count':len(protected),'errors':errors},ensure_ascii=False))
 assert not errors
