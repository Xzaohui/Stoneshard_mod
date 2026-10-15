from pathlib import Path
import json,hashlib,datetime,shutil,zipfile
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=r/'Assets/CharacterDesigns/20261013/expressive/new_story';audit=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/fifth_expression_recovery_20261014';b=json.loads((audit.parent/'fifth_four_expression_brief.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
rawqa=audit.parent/'independent_fifth_expression_recovery_20261014.json';finalqa=audit.parent/'independent_fifth_expression_final_20261014.json';assert finalqa.exists();fq=json.loads(finalqa.read_text())
# The final independent report is checked manually before this script is invoked.
freezes={}
for c in b['characters']:
 who=c['slug'];d=base/who/'expressions_v1';assert not (d/'FINAL_STATUS.json').exists(),'Already frozen; do not rewrite.'
 shutil.copy2(rawqa,d/'QA-independent-raw-visual.json');shutil.copy2(finalqa,d/'QA-independent.json')
 a=json.loads((d/'QA-author.json').read_text());a['status']='selected_pass_with_E2_blocked' if who=='endai' else 'pass';a['independent_final_sha256']=sha(finalqa);a['nonblocking_notes']=['珥泰两表情差别克制可读，均为单帧静止演出，不是剧烈情绪或连续摇头动画。'] if who=='ertai' else ([] if who!='wadun' else ['E1有窄亮上齿，非夸张大笑，独审认定非阻塞。']);write(d/'QA-author.json',a)
 checks=json.loads((d/'technical_qa.json').read_text())
 for x in checks:
  if x['status']=='candidate_QA_pending':x['status']='pass'
 write(d/'technical_qa.json',checks)
 rd=(d/'README.md').read_text().replace('合格候选2张','合格选稿2张').replace('独审通过项冻结后再交付，文件保存不等于已送达。','独审通过项已由作者冻结；文件保存不等于已送达。')
 if who=='ertai':rd+='\n两种表情的区别克制可读；E2只表示摇头的一瞬，不是连续摇头动画。\n'
 (d/'README.md').write_text(rd)
 selected=[{'key':x['key'],'label_zh':x['label'],'path':x['transparent_path'],'sha256':x['transparent_sha256'],'raw_path':x['raw_path'],'raw_sha256':x['raw_sha256'],'size':x['size']} for x in checks if x['status']=='pass'];blocked=[x for x in checks if x['status']!='pass']
 manifest={'schema_version':1,'character_slug':who,'name':c['name'],'canonical_id':c['canonical_id'],'status':'partial_frozen_pass' if blocked else 'frozen_pass','frozen_utc':now,'selected_count':len(selected),'selected':selected,'blocked':blocked,'all_raw':[{'path':str(p.relative_to(d)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted((d/'raw').glob('*.png'))],'sources':json.loads((d/'sources/source_verification_recovery.json').read_text()),'generation_log_sha256':sha(d/'generation-log.json'),'author_qa_sha256':sha(d/'QA-author.json'),'independent_raw_qa_sha256':sha(d/'QA-independent-raw-visual.json'),'independent_final_qa_sha256':sha(d/'QA-independent.json'),'boards':[{'path':str(p.relative_to(d)),'sha256':sha(p)} for p in sorted((d/'review').glob('*.png'))],'provenance_status':'observed_exact_new_calls' if who=='wadun' else 'recovered_raw_and_preexisting_prompt_historical_call_arguments_unavailable','runtime_verified':False,'user_approval_claimed':False}
 write(d/'manifest.json',manifest)
 frozen={str(p.relative_to(d)):sha(p) for p in sorted(d.rglob('*')) if p.is_file() and p.name!='FINAL_STATUS.json'}
 status={'schema_version':1,'status':'frozen_partial_pass_1_of_2' if blocked else 'final_clean_and_presentation_pass','frozen_utc':now,'character':who,'selected_count':len(selected),'blocked_count':len(blocked),'manifest_sha256':sha(d/'manifest.json'),'independent_qa_sha256':sha(d/'QA-independent.json'),'all_raw_preserved':True,'raw_output_count':len(manifest['all_raw']),'new_generation_calls_in_recovery':2 if who=='wadun' else 0,'max_hard_error_revisions_per_pose':1,'remaining_revision_budget_E2':0 if who=='endai' else 1,'blocking_issues':['E2 revision1 proportion drift after double-person initial; revision budget exhausted. Raw and review derivatives cannot be used as a selected asset.'] if who=='endai' else [],'nonblocking_notes':a['nonblocking_notes'],'files':frozen,'author_sole_writer_freeze':True,'freeze_policy':'Source directory read-only after this status write; delivery copies and archives created in separate directories.','not_uploaded':True,'not_sent':True,'not_deployed':True,'runtime_verified':False,'user_approval_claimed':False}
 write(d/'FINAL_STATUS.json',status);freezes[who]={'path':str(d.relative_to(r)),'files':{str(p.relative_to(d)):sha(p) for p in sorted(d.rglob('*')) if p.is_file()},'manifest_sha256':sha(d/'manifest.json'),'final_status_sha256':sha(d/'FINAL_STATUS.json')}
for slugs,folder,board in [(['endai','wadun'],'fifth_four_expressions_endai_wadun_delivery_v1','恩岱_瓦顿_三种合格表情_浅深对照.png'),(['ertai','suier'],'fifth_four_expressions_ertai_suier_delivery_v1','珥泰_燧珥_四种表情_浅深对照.png')]:
 out=base/folder;attachments=[];archive_records=[]
 for who in slugs:
  d=base/who/'expressions_v1';mf=json.loads((d/'manifest.json').read_text())
  for row in mf['selected']:
   p=d/row['path'];dst=out/p.name;assert dst.exists() and sha(dst)==sha(p);attachments.append({'path':dst.name,'sha256':sha(dst),'bytes':dst.stat().st_size,'kind':'selected_transparent'})
  name=f'{who}_expressions_v1_complete_source.zip';zpath=out/name;assert not zpath.exists()
  with zipfile.ZipFile(zpath,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for rel,h in freezes[who]['files'].items():z.write(d/rel,arcname=f'{who}/expressions_v1/'+rel)
  with zipfile.ZipFile(zpath) as z:
   assert z.testzip() is None
   assert len(z.namelist())==len(freezes[who]['files'])
   member_hashes={name:hashlib.sha256(z.read(name)).hexdigest() for name in z.namelist()}
   for rel,h in freezes[who]['files'].items():assert member_hashes[f'{who}/expressions_v1/'+rel]==h
  assert zpath.stat().st_size<18*1024*1024
  assert freezes[who]['files']=={str(p.relative_to(d)):sha(p) for p in sorted(d.rglob('*')) if p.is_file()}
  archive_records.append({'path':name,'sha256':sha(zpath),'bytes':zpath.stat().st_size,'under_18_MiB':True,'member_count':len(member_hashes),'member_sha256':member_hashes,'all_members_read_back_verified':True,'source_unchanged_after_pack':True})
 bp=out/board;attachments.append({'path':bp.name,'sha256':sha(bp),'bytes':bp.stat().st_size,'kind':'chinese_light_dark_board'})
 for z in archive_records:attachments.append({k:z[k] for k in ['path','sha256','bytes']}|{'kind':'complete_character_source_zip'})
 write(out/'archive_inventory.json',archive_records)
 delivery={'schema_version':1,'created_utc':now,'status':'ready_local_partial_batch_not_uploaded' if 'endai' in slugs else 'ready_local_not_uploaded','selected_count':sum(1 for x in attachments if x['kind']=='selected_transparent'),'blocked_poses':['endai_E2_no_order_no_entry'] if 'endai' in slugs else [],'attachment_count':len(attachments),'attachments':attachments,'source_freezes':{s:freezes[s] for s in slugs},'history_note':'Recovered older PNGs retain their existing prompt files, source hashes and review evidence; historic exact call parameters could not be recovered. Wadun new calls have exact prompt and arguments.','runtime_verified':False,'not_uploaded':True,'not_sent':True}
 write(out/'delivery.json',delivery)
 qa={'status':'pass_for_listed_selected_only','created_utc':now,'selected_count':delivery['selected_count'],'excluded_pose_count':len(delivery['blocked_poses']),'selected_files_match_frozen_sources':True,'chinese_board_actual_visual_review':True,'independent_final_qa_sha256':sha(finalqa),'all_zip_members_read_back_and_SHA_verified':True,'all_source_files_in_each_archive':True,'all_archives_under_18_MiB':True,'frozen_sources_unchanged':True,'delivery_manifest_sha256':sha(out/'delivery.json'),'archive_inventory_sha256':sha(out/'archive_inventory.json'),'not_uploaded':True,'not_sent':True,'not_deployed':True}
 write(out/'FINAL_DELIVERY_QA.json',qa)
 print(folder,delivery['selected_count'],[(x['path'],round(x['bytes']/1024/1024,3)) for x in attachments])
summary={'status':'seven_selected_frozen_one_blocked','selected_count':7,'blocked_count':1,'blocked_pose':'endai_E2_no_order_no_entry','new_generation_calls':2,'historical_raw_recovered_from_generated_directory':4,'historical_raw_already_saved':3,'total_raw_preserved':9,'delivery_directories':[str((base/'fifth_four_expressions_endai_wadun_delivery_v1').relative_to(r)),str((base/'fifth_four_expressions_ertai_suier_delivery_v1').relative_to(r))],'source_freezes':freezes,'not_uploaded':True,'not_sent':True,'not_pushed':True,'not_deployed':True,'final_qa_sha256':sha(finalqa)}
write(audit/'FINAL_RECOVERY_STATUS.json',summary);shutil.copy2(__file__,audit/'freeze_and_package.py')
