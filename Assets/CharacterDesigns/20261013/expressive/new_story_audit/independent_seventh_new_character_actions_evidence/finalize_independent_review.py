from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';e=a/'independent_seventh_new_character_actions_evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();fp=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)};load=lambda p:json.loads(p.read_text())
p=a/'independent_seventh_new_character_actions_20261014.json';main=load(p)
vg=[load(a/f'independent_seventh_new_character_actions_{g}_visual_gate_20261014.json') for g in ['luoer_qiner','lier_huier']]
pg=[load(a/f'independent_seventh_new_character_actions_{g}_package_gate_20261014.json') for g in ['luoer_qiner','lier_huier']]
fg=[load(a/f'independent_seventh_new_character_actions_{g}_frozen_byte_gate_20261014.json') for g in ['luoer_qiner','lier_huier']]
assert all(x['status']=='pass_ready_for_library_save' and not x['errors'] for x in fg)
for pose in main['pose_results']:
 ep=r/pose['evidence'];ev=load(ep);pose['evidence_sha256']=sha(ep);pose['visual_review']=ev['visual_review'];pose['technical_checks']=ev['checks']
assert len(main['pose_results'])==10
main['status']='independent_review_complete_ready_for_library_save_with_one_explicit_missing_pose';main['final_reviewed_utc']=datetime.now(timezone.utc).isoformat()
main['counts']={'established_characters':4,'new_characters_created':0,'planned_poses':8,'selected_poses':7,'new_explicit_missing_poses':1,'generation_calls':10,'initial_generations':8,'hard_error_revisions':2,'rejected_attempts_preserved':3,'complete_tool_payloads_preserved':10,'source_images_actually_viewed':12,'generated_attempt_images_actually_viewed':40,'joint_boards_actually_viewed':2,'selected_transparent_attachments':7,'board_attachments':2,'complete_source_zip_attachments':5,'total_attachments':14,'character_source_tree_files':sum(y['tree_files'] for x in pg for y in x['characters']),'planning_package_files':86,'actual_extracted_source_files_across_five_archives':sum(x['actual_extracted_source_files'] for x in pg),'additional_package_metadata_entries':2}
main['selected_poses']=[v for x in vg for v in x['selected']]
main['new_explicit_missing']=[v for x in vg for v in x['explicit_missing']]
main['old_missing_unchanged']=['turi_A1','cuoer_A1','weier_A1']
main['accepted_minor_deviation']={'pose':'qiner_A1_raise_existing_sprig_v1','finding':'Leaf tip slightly exceeds chin-level target. Clear lateral face separation, visible chest-height stem grasp and unchanged basket remain valid; no ingestion/medical implication. Cosmetic height alone did not trigger an extra generation.'}
main['missing_resolution']={'pose':'lier_A1_gather_two_rope_tails','reason':'Only one rope tail visibly held; second remains outside palm in both v1 and the sole v2 correction.','action':'Both attempts retained fully as rejected evidence; no selected attachment or selected board cell; text-only missing cells retained. No third generation.'}
main['gates']={}
for g in ['luoer_qiner','lier_huier']:
 main['gates'][g]={k:fp(a/f'independent_seventh_new_character_actions_{g}_{k}_20261014.json') for k in ['visual_gate','board_gate','package_gate','frozen_byte_gate']}
main['delivery_freezes']=[x['author_freeze'] for x in fg];main['delivery_manifests']=[x['frozen_delivery_manifest'] for x in fg]
main['source_protection']={'mother_expression_rules_and_cards_files':246,'frozen_planning_files':85,'old_action_tree_files':3359,'old_repository_archives':215,'unique_old_action_and_archive_files_rechecked':3509,'status':'all_unchanged_at_final_pre_upload_check','full_old_action_and_archive_verification':fp(e/'prior_action_and_archive_preservation_final.json'),'old_source_baseline':fp(e/'old_source_baseline.json'),'planning_baseline':fp(e/'planning_frozen_baseline.json')}
main['archive_closure']={'status':'pass','actual_decompression_and_source_bytes_sha_compared':True,'all_five_standard_zips_independently_openable':True,'all_crc_checks_passed':True,'largest_archive_bytes':max(z['bytes'] for x in pg for z in x['zip_reports']),'limit_each_archive_bytes':18*1024*1024,'full_payloads_including_rejected_versions_retained':True,'final_freeze_rechecked_without_mutating_cited_gates':True,'extraction_note':'Lier and Huier ZIPs must use separate extraction directories because each contains its own root PACKAGE_SET_MANIFEST.json. Luoer/Qiner/planning archives are ordinary independent ZIPs.'}
main['delivery_accounting']={'before_this_batch':{'established_characters_with_delivered_actions':24,'selected_poses':45,'delivery_groups':12,'missing_poses':3},'increment_if_uploads_and_sends_are_confirmed':{'established_characters_with_delivered_actions':4,'selected_poses':7,'delivery_groups':2,'missing_poses':1},'expected_after_confirmed_delivery':{'established_characters_with_delivered_actions':28,'selected_poses':52,'delivery_groups':14,'missing_poses':4},'delivery_verified_by_this_reviewer':False,'note':'Do not mark expected cumulative counts as delivered until root validates actual Library/send receipts. No animation, integration or runtime claim.'}
main['historical_fields']='Earlier gates and author files preserve phase-at-creation pending states; the new frozen-byte gates resolve final byte readiness without rewriting immutable history.'
main['review_scope_complete']=True;main['reviewer_uploads']=0
p.write_text(json.dumps(main,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'final_report':fp(p),'counts':main['counts'],'status':main['status']},ensure_ascii=False,indent=2))
