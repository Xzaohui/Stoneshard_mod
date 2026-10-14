from pathlib import Path
import json,hashlib,shutil,zipfile,datetime
root=Path(__file__).resolve().parents[5];base=root/'Assets/EnemyDesigns/20261013/first_six';delivery=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
qa=base/'independent_action_continuation_QA_001_002.json';assert sha(qa)=='8b03e32aee36929d66a99c5803c4453108b726c274c104fb455ac08a6e5f7d01'
brief=json.loads((base/'action_continuation_brief_v1.json').read_text());summaries=[]
for r in brief['items'][:2]:
 par=base/r['role']/'action_continuation_v1';o=root/r['planned_generation']['output_directory_if_later_executed'];s=par/'sources'
 shutil.copy2(qa,s/'independent_continuation_QA.json')
 for name in ['prepare_review.py','build_delivery.py','finalize_packages.py']:shutil.copy2(delivery/name,s/name)
 shutil.copy2(delivery/'001_002_动作补缺_浅深阶段对照.png',par/'001_002_final_stage_review.png')
 (s/'README.md').write_text('这些是本轮实际生成输入与规格的快照。旧母图和两张旧动作原文件未修改；完整SHA核验见 original_asset_preservation_checks.json。相邻旧动作仅为阶段说明，未被回写、重画或拉伸。正式独审为原文件逐字节复制。准备脚本仅alpha背景清理和等比最近邻排版。\n')
 selected=o/f"{r['role']}_{r['proposed_keypose']['pose_id']}_transparent.png" if r['id']=='001' else None
 status='passed_independent_visual_review_frozen' if selected else 'failed_no_selected_revision_budget_exhausted'
 aq=json.loads((o/'author_QA_v2.json').read_text());aq['status']='accepted_as_independent_concept_after_review' if selected else status;aq['independent_QA']={'path':str((s/'independent_continuation_QA.json').relative_to(par)),'sha256':sha(qa)};write(o/'author_QA_v2.json',aq)
 final={'schema_version':1,'role':r['role'],'pose_id':r['proposed_keypose']['pose_id'],'status':status,'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'sole_writer':'draw_enemy_001_002_continuations','generation_calls':2,'first_drafts':1,'hard_error_revisions_used':1,'remaining_revision_budget':0,'selected_output':{'path':str(selected.relative_to(root)),'sha256':sha(selected)} if selected else None,'selected_new_keyposes_count':1 if selected else 0,'raw_versions_preserved':['v1','v2'],'reason':('低矛轴、双肘收回、前膝放松与后腿接重概念独审通过。' if selected else '修订后棍头仍低于腰带且拳近腰，未完成brief要求的胸腹中弧；两稿均不选用，停止生图。'),'independent_QA':{'path':str((s/'independent_continuation_QA.json').relative_to(root)),'sha256':sha(qa)},'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False,'exact_anchors_verified':False,'all_cross_pose_weapon_lengths_verified':False,'limitations':['只是独立概念，非完整循环或可运行动画。','共同origin、相机、身体/武器尺度需后续注册；未进行像素级锚点验收。','001旧戒备→短刺及本轮跨姿矛长未验证，保持该限制。'],'old_assets_modified':False,'git_operations':0,'uploads_by_author':0}
 write(par/'FINAL_STATUS.json',final)
 files=[{'path':str(p.relative_to(par)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(par.rglob('*')) if p.is_file() and p.name!='manifest.json'];manifest={'schema_version':1,'role':r['role'],'status':status,'selected_output':final['selected_output'],'generation_calls':2,'total_files_excluding_manifest':len(files),'excluded_from_self_hash':['manifest.json'],'files':files,'original_assets_unchanged':True,'runtimeVerified':False,'continuous_animation_verified':False};write(par/'manifest.json',manifest)
 zipname=('001_border_spear_rebel_收矛完整源包.zip' if selected else '002_canal_club_brigand_下挥失败完整源包.zip');zp=delivery/zipname
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for f in sorted(par.rglob('*')):
   if f.is_file():z.write(f,arcname=str(Path(r['role'])/'action_continuation_v1'/f.relative_to(par)))
 assert zp.stat().st_size<18*1024*1024
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  for f in files:
   assert hashlib.sha256(z.read(str(Path(r['role'])/'action_continuation_v1'/f['path']))).hexdigest()==f['sha256']
 summaries.append({'id':r['id'],'role':r['role'],'status':status,'selected':final['selected_output'],'manifest_path':str((par/'manifest.json').relative_to(root)),'manifest_sha256':sha(par/'manifest.json'),'final_status_path':str((par/'FINAL_STATUS.json').relative_to(root)),'final_status_sha256':sha(par/'FINAL_STATUS.json'),'zip_path':str(zp.relative_to(root)),'zip_sha256':sha(zp),'zip_bytes':zp.stat().st_size,'zip_integrity':'all members verified; testzip passed'})
attachments=[delivery/'border_spear_rebel_spear_retract_weight_back_transparent.png',delivery/'001_002_动作补缺_浅深阶段对照.png']+[root/x['zip_path'] for x in summaries]
dm={'schema_version':1,'frozen':True,'roles':summaries,'requested_maximum_attachments':5,'actual_attachments':4,'reduced_attachment_reason':'002 failed; no selected PNG delivered. Full failure source archive retained.','attachments':[{'path':str(p.relative_to(root)),'name':p.name,'sha256':sha(p),'bytes':p.stat().st_size} for p in attachments],'independent_QA_path':str(qa.relative_to(root)),'independent_QA_sha256':sha(qa),'old_assets_modified':False,'git_operations':0,'runtimeIntegrated':False,'runtimeVerified':False,'continuous_animation_verified':False};write(delivery/'delivery_manifest.json',dm)
print(json.dumps(dm,ensure_ascii=False,indent=2))
