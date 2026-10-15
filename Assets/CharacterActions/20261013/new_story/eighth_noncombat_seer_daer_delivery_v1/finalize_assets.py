from pathlib import Path
import hashlib,json,shutil,zipfile
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');N=R/'Assets/CharacterActions/20261013/new_story';A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';D=N/'eighth_noncombat_seer_daer_delivery_v1';S=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();F=lambda p:{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':S(p)}
sel=json.loads((D/'selection.json').read_text());group=A/'independent_eighth_new_character_actions_seer_daer_visual_gate_20261014.json';board=A/'independent_eighth_new_character_actions_seer_daer_board_gate_20261014.json';assert S(group)=='26ff6746c3e9dbf4e59a0855c550f9d80e413c53bc4ba5e9f9e7267a903082f7';assert S(board)=='510a52c4e3edfadd2021ee3bc2571729efc2e7f4ab04a08df27206917347926a'
for p in [group,board]:shutil.copyfile(p,D/p.name)
for slug in ['seer','daer']:
 d=N/slug/'noncombat_basics_v1';shutil.copyfile(group,d/'QA-independent.json');shutil.copyfile(board,d/'QA-independent-board.json')
 (d/'README_中文.md').write_text('# '+('瑟珥' if slug=='seer' else '达珥')+' · 普通基础动作\n\n两张已独审通过的静态独立全身动作。PNG保留imagegen原生1118×1407，无拉伸、镜像或脚本人体修改。每稿raw、完整toolreturn含payload、逐字prompt/实参、alpha透明与真浅深检查图均保留。\n\n'+('瑟珥两张均首稿通过；旧E1安全阻断表情保持封存，本次不补做。' if slug=='seer' else '达珥A1首稿双臂侧别画反，唯一修订通过。首稿仍保留于raw/review/prompts，不计selected。A2首稿通过。')+'\n\n作者QA不替代独审。最终采用版本与SHA见FINAL_STATUS.json；每稿技术QA初始pending关闭的附属元数据变动已由组门审记录。仅概念，不称动画或游戏运行通过。\n')
 entries=[F(p) for p in sorted(d.rglob('*')) if p.is_file() and p.name not in ['manifest.json','FINAL_STATUS.json']]
 manifest={'character':slug,'scope':'2 approved independent noncombat fullbody action concepts','status':'independent_visual_pass','selected':[x for x in sel['selected'] if x['character']==slug],'files':entries,'all_attempts_retained':True,'no_git_upload_runtime':True};(d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 finals={'schema_version':1,'character':slug,'sole_writer':'draw_seer_daer_actions','frozen_utc':'2026-10-14T07:37:07Z','status':'two_selected_passed','requested_count':2,'selected_pass_count':2,'selected':manifest['selected'],'initial_generations':2,'revision_generations':0 if slug=='seer' else 1,'failed_attempts':[] if slug=='seer' else [{'key':'daer_A1_smooth_left_forearm_sleeve','version':'v1','reason':'双臂侧别反了','status':'preserved_research_only_not_selected'}],'moderation_blocks_in_current_actions':0,'seer_old_E1_not_attempted':True,'independent_visual_gate_sha256':S(d/'QA-independent.json'),'independent_board_gate_sha256':S(d/'QA-independent-board.json'),'manifest_sha256':S(d/'manifest.json'),'author_actual_raw_transparent_light_dark_views':True,'selected_copy_matches_actually_viewed_transparent_bytes':True,'runtime_verified':False,'source_assets_modified':False,'frozen_files':entries+[F(d/'manifest.json')]};(d/'FINAL_STATUS.json').write_text(json.dumps(finals,ensure_ascii=False,indent=2)+'\n')
shutil.copyfile(__file__,D/'finalize_assets.py')
# All production files including rejected attempt remain in the character source packages.
zips=[]
for slug in ['seer','daer']:
 p=D/'delivery'/f'{slug}_complete_action_sources_v1.zip';d=N/slug/'noncombat_basics_v1'
 with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,6) as z:
  for q in sorted(d.rglob('*')):
   if q.is_file():z.write(q,q.relative_to(R))
 with zipfile.ZipFile(p) as z:assert z.testzip() is None
 assert p.stat().st_size<18*1024*1024;zips.append(p)
p=D/'delivery'/'seer_daer_complete_planning_and_board_sources_v1.zip'
files=set(q for q in (A/'eighth_new_character_actions_sources').rglob('*') if q.is_file())
files.update([A/'eighth_new_character_actions_brief.json',A/'independent_eighth_new_character_actions_plan_gate_20261014.json',group,board])
files.update(q for q in (A/'independent_eighth_new_character_actions_evidence').glob('*_byte_audit.json') if q.name.startswith(('seer_','daer_')))
files.update(q for q in D.iterdir() if q.is_file() and q.suffix in ['.json','.md','.py','.png'])
with zipfile.ZipFile(p,'w',zipfile.ZIP_DEFLATED,6) as z:
 for q in sorted(files):z.write(q,q.relative_to(R))
with zipfile.ZipFile(p) as z:assert z.testzip() is None
assert p.stat().st_size<18*1024*1024;zips.append(p)
attachments=[]
for x in sel['selected']:
 p=R/x['delivery_path'];attachments.append({'order':len(attachments)+1,'kind':'transparent_action_png','character':x['character'],'title_zh':x['label_zh'],**F(p)})
p=D/'delivery'/'瑟珥_达珥_母图动作浅深对照.png';attachments.append({'order':5,'kind':'joint_mother_action_light_dark_board',**F(p)})
for p in zips:attachments.append({'order':len(attachments)+1,'kind':'complete_source_zip',**F(p)})
records=[]
for p in zips:
 with zipfile.ZipFile(p) as z:
  members=[]
  for n in z.namelist():
   b=z.read(n);assert (R/n).read_bytes()==b;members.append({'path':n,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 records.append({**F(p),'crc_pass':True,'member_count':len(members),'members':members})
(D/'zip_content_manifest.json').write_text(json.dumps({'packages':records,'all_source_member_hashes_match':True,'complete_raw_and_all_image_payloads_in_character_zips':True,'all_failed_attempt_material_retained':True,'all_packages_below_18_MiB':True},ensure_ascii=False,indent=2)+'\n')
(D/'delivery_manifest.json').write_text(json.dumps({'schema_version':1,'author':'draw_seer_daer_actions','status':'packaged_waiting_independent_package_gate','selected_pose_count':4,'existing_characters':2,'new_characters':0,'initial_generations':4,'revision_generations':1,'attempts':5,'failed_attempt_count':1,'current_missing_pose_count':0,'attachments':attachments,'complete_sources':True,'user_delivery_performed':False,'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(attachments,ensure_ascii=False,indent=2))
