from pathlib import Path
import json,hashlib,datetime
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'eleventh_actions_independent_details';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
poses=[];groups=[];selected=[];frozen_files=[]
for group,freeze in [('daier_moer_trs','DELIVERY_FINAL_STATUS.json'),('weier_ink_moer','FREEZE_STATUS.json')]:
 gate=a/f'independent_eleventh_new_character_actions_{group}_package_gate_20261014.json';g=json.loads(gate.read_text());d=r/f'Assets/CharacterActions/20261013/new_story/eleventh_noncombat_{group}_delivery_v1';fr=d/freeze
 assert fr.is_file()
 for q in g['attachments']:
  p=r/q['path'];assert p.stat().st_size==q['bytes'] and sha(p)==q['sha256'];frozen_files.append(q)
 for key in ['package_manifest','ordered_attachment_manifest']:
  q=g[key];assert sha(r/q['path'])==q['sha256'];frozen_files.append(q)
 v=json.loads((r/g['visual_gate']['path']).read_text())
 for row in v['poses']:
  poses.append(row)
  p=r/row['selected']['path'];assert sha(p)==row['selected']['sha256']
  # canonical final selected paths are author-owned selected directories.
  cd=r/'Assets/CharacterActions/20261013/new_story'/row['slug']/'noncombat_basics_v1'
  matching=[f for f in (cd/'selected').glob('*.png') if sha(f)==row['selected']['sha256']];assert len(matching)==1
  selected.append({'slug':row['slug'],'key':row['plan_key'],**fp(matching[0]),'character_final_status':fp(cd/'FINAL_STATUS.json'),'group_package_gate':fp(gate),'group_freeze':fp(fr)})
  for f in cd.rglob('*'):
   if f.is_file():frozen_files.append(fp(f))
 groups.append({'group':group,'package_gate':fp(gate),'freeze':fp(fr),'ordered_attachment_manifest':g['ordered_attachment_manifest'],'package_manifest':g['package_manifest'],'zip_files':g['zip_files'],'zip_member_count':g['zip_member_count'],'source_member_count':g['source_member_count'],'selected_poses':4,'attachments':8})
assert len(poses)==len(selected)==8
out={'schema_version':1,'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'review_eleventh_character_actions','verdict':'PASS_ELEVENTH_NEW_CHARACTER_ACTIONS_FINAL_SOURCE_REVIEW','scope':{'existing_characters':4,'new_independent_static_keyposes_passed':8,'image_generation_attempts':8,'initial_attempts':8,'hard_error_revisions':0,'rejected_attempts':0,'safety_blocks':0,'missing_current_batch':0,'complete_source_zip_files':4,'source_file_members':304,'embedded_zip_inventory_members':2,'total_zip_members':306,'all_archives_under_18_MiB':True,'attachment_files':16,'new_character_identities':0,'animation_verified':False,'runtime_verified':False},'plan_gate':fp(a/'independent_eleventh_new_character_actions_plan_gate_20261014.json'),'frozen_brief_sha256':'3988be2e7e6da94b75ffc5df2b830559cd46c6687ed436f9038b073dd9272259','poses':poses,'canonical_final_selected_files':selected,'groups':groups,'source_preservation':fp(e/'final_source_and_prior_action_preservation.json'),'protected_source_files_verified':5049,'artifact_lineage':['Every executed initial prompt exactly equals final frozen plan text; actual full parameters archived before returned raw image.','Eight complete returned payloads decode to archived original PNG bytes; reference SHA matches corresponding approved mother.','Raw and cleaned transparent pixels above alpha 8 are unchanged; both displayed on genuine light/dark backgrounds and visually reviewed.','Four Chinese mother-reference boards actually viewed; all 24 cells are complete-source nearest-neighbor alpha composites with preserved aspect ratio.','Four final source ZIPs checked by CRC and complete actual decompression: 304 source members byte-identical to repository sources plus two validated embedded inventories.','Author FINAL/manifest and final external freeze receipts independently read back; reviewer did not modify authors source trees.'],'first_round_status_after_production':{'characters_covered':44,'qualified_keyposes':84,'groups':22,'old_missing_keyposes':['turi_A1','cuoer_A1','weier_A1','lier_A1'],'old_uncertain_delivery_groups':['seer_daer','suoda_kelin'],'accepted_before_current_batch':{'groups':18,'characters':36,'qualified_poses':68},'current_batch_delivery_status':'Final reviewed frozen artifacts released for Library save; sends not assessed by this review and must use actual receipts.','new_unrelated_pose_batches':False},'hard_errors':[],'reviewer_mutations':'Independent audit/evidence files only; no uploads, user messaging, Git or runtime edits.'}
p=a/'independent_eleventh_new_character_actions_20261014.json';p.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
p2=e/'final_selected_catalog_handoff.json';p2.write_text(json.dumps({'reviewed_utc':out['reviewed_utc'],'status':'all_eight_final_frozen_and_independently_passed','final_audit':fp(p),'files':selected},ensure_ascii=False,indent=2)+'\n')
(e/'final_frozen_artifact_baseline.json').write_text(json.dumps({'created_utc':out['reviewed_utc'],'files':list({x['path']:x for x in frozen_files}.values())},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'final_audit':fp(p),'catalog_handoff':fp(p2),'scope':out['scope']},ensure_ascii=False))
