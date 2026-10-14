from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,zipfile,zlib
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');b=r/'Assets/CharacterActions/20261013/new_story';a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';d=b/'sixth_noncombat_erwei_chenger_delivery_v1';o=d/'delivery';o.mkdir(exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.now(timezone.utc).isoformat();jwrite=lambda p,v:p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
meta=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':h(p)}
chars=[('erwei','珥薇',[('erwei_A1_low_lift_pot_by_two_ears_v1','双手握两耳低提旧锅'),('erwei_A2_smooth_right_apron_patch_v2','右掌按平围裙赭补片')]),('chenger','埕珥',[('chenger_A1_press_left_outer_blanket_v1','坐姿按稳左上臂外毯'),('chenger_A2_seated_reach_grounded_lantern_ring_v1','坐稳侧俯握原灯环')])]
attachments=[];selection=[];source_trees={}
for slug,name,actions in chars:
 p=b/slug/'noncombat_basics_v1'
 for kind in ['visual','board']:
  f=a/f'independent_sixth_new_character_actions_erwei_chenger_{kind}_gate_20261014.json';assert f.exists();shutil.copyfile(f,p/'review'/f.name)
 for f in (a/'independent_sixth_new_character_actions_evidence').iterdir():
  if f.is_file() and (f.name.startswith(slug+'_') or f.name=='audit_pose.py'):shutil.copyfile(f,p/'review'/f.name)
 picks=[]
 for i,(key,title) in enumerate(actions,1):
  src=p/'exports'/f'{key}_transparent.png';dst=o/f'{name}_A{i}_{title}.png';shutil.copyfile(src,dst)
  attachments.append({'kind':'transparent_action_png','character':slug,'key':key,'title_zh':title,**meta(dst)})
  pick={'key':key,'title_zh':title,'path':str(src.relative_to(r)),'sha256':h(src),'independent_verdict':'pass'};picks.append(pick);selection.append(pick)
 excluded=[{'key':'erwei_A2_smooth_right_apron_patch_v1','status':'rejected_hard_contact_error','reason':'左手未接近身锅耳而落锅口；唯一v2修复通过。','complete_sources_retained':True}] if slug=='erwei' else []
 status={'schema_version':1,'author':'draw_erwei_chenger_actions','sole_writer':True,'created_utc':now,'status':'complete_2_selected_independent_keyposes','selected_pose_count':2,'initial_generations':2,'revision_generations':1 if slug=='erwei' else 0,'selected':picks,'excluded_versions':excluded,'independent_visual_and_board_pass':True,'root_actual_board_view_and_acceptance':True,'root_board_acceptance_utc':'2026-10-14T06:07:51Z','package_readback':'Recorded separately in group delivery directory after independent package audit.','runtime_verified':False,'continuous_animation':False,'new_story_result':False,'uploaded_or_git':False,'limits':['独立全身基础动作概念，非连续动画或运行精灵。','仅alpha<=8及隐藏RGB清理；alpha>8主体原像素不改。','完整人物同一0.47等比nearest合板。','三份普通ZIP的并集覆盖两人物完整源树；须一起保留。']}
 jwrite(p/'FINAL_STATUS.json',status)
 (p/'README_中文.md').write_text(f'# {name} 日常基础动作完整源\n\n2张独立全身姿态通过独审。'+('2次首稿、1次接触硬错修订；A2选v2，失败v1全部保留。' if slug=='erwei' else '2次首稿、0修订。')+'\n\nraw保存所有原始PNG及完整工具返回（含image_url payload）；prompts保存调用前逐字prompt与相同实参；sources保存来源字节快照、SHA、计划与门审；review保存全部真实浅深图、中文联合板、独审及作者QA。\n\n脚本只做alpha<=8与隐藏RGB清理及整图nearest等比合板，不绘制或修补人体。归档pixel skill的references/executor-pixel.md未提供，没有假称读到。\n\n仅可逆日常动作，不改变剧情、授权或任务状态，未做游戏落地。\n\n本组完整资料分为3个普通ZIP，三包共同构成珥薇/埕珥完整源；按PACKAGE_SET_MANIFEST.json的清单合并解压至同一目录。没有分割单个文件，没有删除失败稿或原始payload。\n')
 shutil.copyfile('/tmp/finalize_erwei_chenger_actions.py',p/'sources/package_sources.py')
 files=[{'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':h(f)} for f in sorted(p.rglob('*')) if f.is_file() and f!=p/'manifest.json']
 jwrite(p/'manifest.json',{'schema_version':1,'author':'draw_erwei_chenger_actions','created_utc':now,'character':slug,'status':'complete_sources_ready_for_zip_readback','selected':picks,'excluded_versions':excluded,'full_generated_tool_returns':len(list((p/'raw').glob('*_tool_return.json'))),'files':files,'manifest_self_hash':'external delivery manifest','scope':'All files in character task tree including every rejected draft and complete tool return.'})
 source_trees[slug]={'path':str(p.relative_to(r)),'manifest_sha256':h(p/'manifest.json'),'members':[{'source_tree_path':str(f.relative_to(r)),'archive_member':str(f.relative_to(b)),'bytes':f.stat().st_size,'sha256':h(f)} for f in sorted(p.rglob('*')) if f.is_file()]}
board=d/'珥薇_埕珥_母图动作浅深对照.png';shutil.copyfile(board,o/board.name);attachments.append({'kind':'chinese_light_dark_mother_action_board',**meta(o/board.name)})
# Three normal ZIPs. Every source file remains whole; member union closes both source trees.
allrows=[x for c in source_trees.values() for x in c['members']];bins=[[] for _ in range(3)];loads=[0]*3
for row in sorted(allrows,key=lambda x:x['bytes'],reverse=True):
 i=min(range(3),key=lambda i:loads[i]);bins[i].append(row);loads[i]+=len(zlib.compress((r/row['source_tree_path']).read_bytes(),9))+300
names=[f'erwei_chenger_complete_sources_part{i+1:02}_of_03_v1.zip' for i in range(3)]
for i,rows in enumerate(bins):
 for row in rows:row['package']=names[i]
package_meta={'schema_version':1,'character':'erwei_chenger','source_trees':[x['path'] for x in source_trees.values()],'complete_set':names,'instructions_zh':'三个普通ZIP共同覆盖两人物完整源树。请全部保留并解压至同一目录。每个来源文件只在一包，完整payload及失败稿均保留。','all_members':sorted(allrows,key=lambda x:x['archive_member'])}
mp=json.dumps(package_meta,ensure_ascii=False,indent=2).encode()
for i,rows in enumerate(bins):
 zp=o/names[i]
 with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for row in sorted(rows,key=lambda x:x['archive_member']):z.write(r/row['source_tree_path'],row['archive_member'])
  z.writestr('PACKAGE_SET_MANIFEST.json',mp)
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  assert set(z.namelist())=={x['archive_member'] for x in rows}|{'PACKAGE_SET_MANIFEST.json'}
  for row in rows:assert hashlib.sha256(z.read(row['archive_member'])).hexdigest()==row['sha256']
 assert zp.stat().st_size<18*1024*1024,(zp,zp.stat().st_size)
 attachments.append({'kind':'complete_source_zip_part','character':'erwei_chenger','characters':['erwei','chenger'],'source_trees':[x['path'] for x in source_trees.values()],'part':i+1,'parts':3,'ordinary_zip':True,'members':len(rows)+1,'zip_crc_check':True,'all_members_match_source_tree_sha':True,**meta(zp)})
 print(names[i],zp.stat().st_size,'members',len(rows)+1)
attachments.sort(key=lambda x:0 if x['kind']=='transparent_action_png' else 1 if x['kind']=='chinese_light_dark_mother_action_board' else 2)
jwrite(d/'delivery_manifest.json',{'schema_version':2,'author':'draw_erwei_chenger_actions','created_utc':now,'status':'packaged_waiting_independent_zip_closure','selected_pose_count':4,'initial_generations':4,'revision_generations':1,'excluded_versions':['erwei_A2_smooth_right_apron_patch_v1'],'attachments':attachments,'attachment_count':len(attachments),'complete_source_trees':source_trees,'package_set':package_meta,'source_zip_limit_bytes':18*1024*1024,'runtime_verified':False,'continuous_animation':False,'git_or_upload_performed':False})
jwrite(d/'selection.json',selection)
(d/'README_中文.md').write_text('珥薇/埕珥：4张合格透明基础动作PNG、1张中文母图动作浅深板、3份普通ZIP完整源。\n4次首稿+1次珥薇A2接触硬错修订，5份完整工具返回均保留。\n3份ZIP合起来涵盖两个完整源树，每个文件完整保留，不是分卷压缩格式；每包都含完整PACKAGE_SET_MANIFEST.json分配清单。三包解压到同一目录即可还原。\n独立静态概念，不是完整动画或游戏落地；未上传未Git。\n')
print('attachments',len(attachments))
