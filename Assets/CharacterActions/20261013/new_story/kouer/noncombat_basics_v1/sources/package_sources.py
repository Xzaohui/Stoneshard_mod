from pathlib import Path
import json,hashlib,shutil,zipfile,datetime
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); b=r/'Assets/CharacterActions/20261013/new_story'; d=b/'fourth_noncombat_miloer_kouer_delivery_v1';o=d/'delivery';o.mkdir(exist_ok=True)
audit=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
meta=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
chars=[('miloer','米洛珥',[('miloer_A1_touch_closed_jar_lid_v1','托罐轻按原盖'),('miloer_A2_smooth_left_tied_cuff_v1','持罐按平左袖褶')]),('kouer','蔻珥',[('kouer_A1_low_lift_lime_bucket_v1','双手低提原木桶'),('kouer_A2_grounded_bucket_rim_steady_v2','俯身扶稳落地桶沿')])]
selection=[];attachments=[]
for slug,name,actions in chars:
 p=b/slug/'noncombat_basics_v1'
 for kind in ['visual','board']:
  f=audit/f'independent_fourth_new_character_actions_miloer_kouer_{kind}_gate_20261014.json';shutil.copyfile(f,p/'review'/f.name)
 evidence=audit/'independent_fourth_new_character_actions_evidence'
 for f in evidence.iterdir():
  if f.is_file() and (f.name.startswith(slug+'_') or f.name=='audit_pose.py'):
   shutil.copyfile(f,p/'review'/f.name)
 picks=[]
 for i,(key,title) in enumerate(actions,1):
  src=p/'exports'/f'{key}_transparent.png';dst=o/f'{name}_A{i}_{title}.png';shutil.copyfile(src,dst)
  item={'kind':'transparent_action_png','character':slug,'key':key,'title_zh':title,**meta(dst)};attachments.append(item)
  pick={'key':key,'title_zh':title,'path':str(src.relative_to(r)),'sha256':sha(src),'independent_verdict':'pass'};picks.append(pick);selection.append(pick)
 excluded=['kouer_A2_grounded_bucket_rim_steady_v1'] if slug=='kouer' else []
 status={'schema_version':1,'author':'draw_miloer_kouer_actions','sole_writer':True,'created_utc':now,'status':'complete_2_selected_independent_keyposes','selected_pose_count':2,'initial_generations':2,'revision_generations':1 if slug=='kouer' else 0,'selected':picks,'excluded_versions':excluded,'independent_visual_and_board_pass':True,'root_actual_board_view_and_acceptance':True,'package_readback':'Recorded separately after packing in delivery directory; final source tree must not change afterward.','runtime_verified':False,'continuous_animation':False,'new_story_result':False,'uploaded_or_git':False,'limits':['仅独立全身基础动作概念，未实现游戏。','不写医疗结果、任务结案、授权或道具消耗。','脚本只作alpha<=8透明清理、等比nearest展示与打包。']}
 (p/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
 notes=f'''# {name} · 日常基础动作原始源\n\n本目录保存{len(actions)}张独立全身关键姿态。内置imagegen首稿2次，定向硬错修订{1 if slug=='kouer' else 0}次。只保留逐姿通过独审的图作为selected，见FINAL_STATUS.json和manifest.json。\n\n'''+''.join(f'- {title}：{key}\n' for key,title in actions)+'''\nraw/保存所有原始PNG及完整工具返回（含image_url原图payload），prompts/保存调用前逐字提示词与实参，sources/保存来源原字节、SHA和实际处理脚本，review/保存作者及独立QA、真实浅深合成、母图对照合板与布局证据。\n\n仅alpha≤8透明清理；alpha>8的原始像素逐字节保持。合板用同一0.47比例nearest缩放，不拉伸、不脚本绘人体。透明区域隐藏RGB不作为硬错。\n\n'''+('米洛珥A2后发束轮廓较母图略突出，独审记为轻微漂移，不属身份硬错。\n' if slug=='miloer' else '蔻珥A2 v1出现中央第三鞋，已保留失败原稿与完整回执；唯一v2定向去除额外鞋后通过。v1不得作为selected，不再追加v3。\n')+'''\n人物身份与道具以现行母图为锚。这是非战斗日常动作概念，不构成连续动画、不代表医疗演示或剧情结果，也未部署到游戏。\n\n归档pixel skill已读取；其中引用的references/executor-pixel.md实际上不存在，没有杜撰该文件。当前生产沿用STYLE_DIRECTION及持续绘制授权。\n'''
 (p/'README_中文.md').write_text(notes)
 shutil.copyfile('/tmp/finalize_miloer_kouer.py',p/'sources/package_sources.py')
 files=[{'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(p.rglob('*')) if f.is_file() and f.name!='manifest.json']
 # Include nested historical manifest.json files. Exclude only this root manifest to avoid self hashing.
 files=[{'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(p.rglob('*')) if f.is_file() and f!=p/'manifest.json']
 manifest={'schema_version':1,'author':'draw_miloer_kouer_actions','created_utc':now,'status':'complete_sources_ready_for_zip_readback','character':slug,'selected':picks,'excluded_versions':excluded,'full_generated_tool_returns':len(list((p/'raw').glob('*_tool_return.json'))),'files':files,'manifest_self_hash':'external delivery_manifest and ZIP member verification','scope':'All files in this character task tree, including rejected draft, prompts, full raw returns, source snapshots, QA, board and author FINAL_STATUS.'}
 (p/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 z=o/f'{slug}_noncombat_basics_complete_source_v1.zip'
 with zipfile.ZipFile(z,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
  for f in sorted(p.rglob('*')):
   if f.is_file():zz.write(f,str(f.relative_to(b)))
 with zipfile.ZipFile(z) as zz:
  assert zz.testzip() is None
  actual={x for x in zz.namelist()};expected={str(f.relative_to(b)) for f in p.rglob('*') if f.is_file()};assert actual==expected
  for f in p.rglob('*'):
   if f.is_file():assert hashlib.sha256(zz.read(str(f.relative_to(b)))).hexdigest()==sha(f)
  count=len(zz.namelist())
 assert z.stat().st_size<18*1024*1024,(z,z.stat().st_size)
 attachments.append({'kind':'complete_source_zip','character':slug,**meta(z),'zip_crc_check':True,'all_members_match_frozen_tree_sha':True,'members':count,'includes_final_status':True,'includes_manifest':True,'source_tree':str(p.relative_to(r)),'manifest_sha256':sha(p/'manifest.json')})
 print(slug,'ZIP',z.stat().st_size,'members',count)
board=d/'米洛珥_蔻珥_母图动作浅深对照.png';shutil.copyfile(board,o/board.name);attachments.append({'kind':'chinese_light_dark_mother_action_board',**meta(o/board.name)})
# Sort PNG actions, board, then complete ZIPs for a maximum seven-attachment delivery.
attachments.sort(key=lambda x:{'transparent_action_png':0,'chinese_light_dark_mother_action_board':1,'complete_source_zip':2}[x['kind']])
manifest={'schema_version':1,'author':'draw_miloer_kouer_actions','created_utc':now,'status':'packaged_waiting_independent_zip_closure','selected_pose_count':4,'initial_generations':4,'revision_generations':1,'excluded_versions':['kouer_A2_grounded_bucket_rim_steady_v1'],'attachments':attachments,'attachment_count':len(attachments),'source_zip_limit_bytes':18*1024*1024,'runtime_verified':False,'continuous_animation':False,'git_or_upload_performed':False,'freeze_record':'FREEZE_RECORD.json will be written by author only after independent package readback; it is outside source ZIPs to avoid cyclic SHA dependencies.'}
(d/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');(d/'selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
(d/'README_中文.md').write_text('米洛珥/蔻珥：4张通过独审的独立日常动作透明PNG、1张中文母图/动作浅深对照、2份完整原始源ZIP。\n四次首稿，一次真实第三鞋硬错修订。蔻珥A2选v2，v1失败稿与完整工具回执均在源包中保留。\n源包是两个普通ZIP，各自独立可解压；合起来覆盖两人物全部本轮源目录。每份小于18MiB，包含作者FINAL_STATUS、manifest、逐字prompt/参数、所有raw与完整imagepayload工具返回、参考快照/哈希、透明图、QA、合板与脚本。\n仅概念，不是连续动画、剧情结果或游戏落地。未上传、未Git；等待独立封包读回后由根交付。\n')
print('delivery attachments',len(attachments));print(json.dumps([{k:v for k,v in x.items() if k in ['kind','path','bytes','sha256']} for x in attachments],ensure_ascii=False,indent=2))
