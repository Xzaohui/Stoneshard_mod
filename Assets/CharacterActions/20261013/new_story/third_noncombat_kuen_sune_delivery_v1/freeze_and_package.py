from pathlib import Path
import json,hashlib,shutil,datetime,zipfile
R=Path(__file__).resolve().parents[5];D=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
boardqa=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/independent_third_new_character_actions_kuen_sune_board_gate_20261014.json';assert sha(boardqa)=='6883ce29493484426f78eb608293cdd8be72de5692fca74b23d27fa67205d89c'
delivery=[];zips=[]
for slug in ['kuen','sune']:
 o=R/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';assert not(o/'FINAL_STATUS.json').exists();assets=json.loads((o/'asset_catalog.json').read_text());qa=json.loads((o/'QA-independent.json').read_text());assert qa['status']=='four_pose_visual_and_provenance_gate_pass'
 shutil.copy2(boardqa,o/'QA-independent-board.json')
 for p in ['finalize_metadata.py','freeze_and_package.py']:shutil.copy2(D/p,o/'delivery_support'/p)
 final={'schema_version':1,'writer':'draw_kuen_sune_actions','status':'frozen_independent_visual_and_provenance_pass','frozen':True,'frozen_utc':now,'selected_independent_keyposes':2,'initial_generations':2,'hard_error_revisions':0,'revision_budget_exceeded':False,'complete_original_tool_results_retained':True,'qa_independent':'QA-independent.json','qa_independent_sha256':sha(o/'QA-independent.json'),'qa_independent_board':'QA-independent-board.json','qa_independent_board_sha256':sha(o/'QA-independent-board.json'),'selected_assets':[{'key':a['key'],'path':a['selected'],'sha256':a['selected_sha256']} for a in assets],'history_note':'未清理透明字节副本及调用前计划/动态gate快照仅为历史，终态以本文件和manifest为准。','scope':'独立静态非战斗动作概念；非连续动画、非装备组合、非runtime或剧情完成证据。','sent':False,'uploaded':False,'git_operations':False,'package_verification':'Author packaging checks recorded externally in delivery_manifest.json; independent ZIP audit follows without modifying frozen trees.'}
 (o/'FINAL_STATUS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
 files=[p for p in sorted(o.rglob('*')) if p.is_file() and p.name!='manifest.json']
 manifest={'schema_version':1,'character':slug,'status':final['status'],'frozen_utc':now,'selected_assets':final['selected_assets'],'files':[{'path':str(p.relative_to(o)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files],'manifest_excludes_self':True,'file_count_without_manifest':len(files),'archive_scope':'整棵noncombat_basics_v1源树；包括raw、完整原工具返回、逐字prompt/参数、source快照、QA、manifest与FINAL_STATUS。','visual_only':True,'runtime_verified':False}
 (o/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 for a in assets:
  p=o/a['selected'];q=D/(a['key']+'_transparent.png');shutil.copy2(p,q);assert sha(q)==a['selected_sha256'];delivery.append({'kind':'transparent_action_png','character':slug,'key':a['key'],'title_zh':a['title_zh'],'path':str(q.relative_to(R)),'bytes':q.stat().st_size,'sha256':sha(q)})
 zp=D/(slug+'_noncombat_basics_complete_source_v1.zip')
 with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(o.rglob('*')):
   if p.is_file():z.write(p,f'{slug}/noncombat_basics_v1/'+str(p.relative_to(o)))
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None;members=z.namelist();expected=[f'{slug}/noncombat_basics_v1/'+str(p.relative_to(o)) for p in sorted(o.rglob('*')) if p.is_file()];assert set(members)==set(expected)
  for path in expected:
   local=o/path.split('/noncombat_basics_v1/',1)[1];assert hashlib.sha256(z.read(path)).hexdigest()==sha(local)
 assert zp.stat().st_size<18*1024*1024
 zips.append({'kind':'complete_source_zip','character':slug,'path':str(zp.relative_to(R)),'bytes':zp.stat().st_size,'sha256':sha(zp),'zip_crc_check':True,'all_members_match_frozen_tree_sha':True,'members':len(members),'includes_final_status':True,'includes_manifest':True,'under_18_MiB':True,'source_tree':str(o.relative_to(R)),'manifest_sha256':sha(o/'manifest.json'),'final_status_sha256':sha(o/'FINAL_STATUS.json')})
board=D/'kuen_sune_four_actions_light_dark_board.png';delivery.append({'kind':'chinese_light_dark_mother_action_board','path':str(board.relative_to(R)),'bytes':board.stat().st_size,'sha256':sha(board)});delivery+=zips
out={'schema_version':1,'created_utc':now,'status':'packaged_waiting_independent_zip_closure','selected_pose_count':4,'initial_generations':4,'revision_generations':0,'attachments':delivery,'attachment_count':7,'all_attachments_under_18_MiB':all(a['bytes']<18*1024*1024 for a in delivery),'standalone_archives':'两份普通完整ZIP，各包含对应人物完整源树，不是分卷；两份合起来覆盖4姿所有原始调用、源、QA及终态。','uploaded':False,'sent':False,'git_performed':False,'scope':'4张独立静态姿态；没有连续动画、过渡、循环、装备组合或runtime验证。'}
(D/'delivery_manifest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
