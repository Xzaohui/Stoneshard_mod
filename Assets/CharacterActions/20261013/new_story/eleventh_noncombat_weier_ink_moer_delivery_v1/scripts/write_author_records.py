from pathlib import Path
import json,hashlib,shutil,datetime
R=Path.cwd();P=R/'Assets/CharacterActions/20261013/new_story';D=P/'eleventh_noncombat_weier_ink_moer_delivery_v1';A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';b=json.loads((D/'planning_sources/eleventh_new_character_actions_brief.json').read_text());g=A/'independent_eleventh_new_character_actions_weier_ink_moer_visual_gate_20261014.json';gate=json.loads(g.read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}
selected=[]
shutil.copy2(g,D/'independent_visual_gate.json')
write(D/'parent_board_review.json',{'reviewer':'root','received_utc':now,'result':'accepted','verbatim_confirmation':'根已实际看浅深两板4姿，接受，继续完整源包独审freeze。','boards':[ref(D/f'weier_ink_moer_mother_actions_{k}.png') for k in ['light','dark']]})
for c in b['characters']:
 if c['slug'] not in ['weier_ink','moer']:continue
 d=R/c['proposed_output_directory']; poses=[];ind=[]
 for p in c['plans']:
  key=p['key'];tag=key+'_v1';tech=json.loads((d/'review'/f'{tag}_technical_QA.json').read_text());audit=A/'eleventh_actions_independent_details'/f'{tag}_byte_audit.json';assert not json.loads(audit.read_text())['failures'];assert not json.loads(audit.read_text())['actual_visual_review']['hard_errors'];shutil.copy2(audit,d/'review'/('independent_'+audit.name))
  path=d/'selected'/f'{key}.png';assert sha(path)==tech['transparent_sha256'];selected.append({'character':c['slug'],'key':key,'title_zh':p['title_zh'],**ref(path)})
  q=next(x for x in gate['poses'] if x['plan_key']==key);assert q['status']=='PASS_INDEPENDENT_VISUAL_AND_BYTE_REVIEW';ind.append(q)
  poses.append({'key':key,'title_zh':p['title_zh'],'selected':ref(path),'raw':ref(d/'raw'/f'{tag}_raw.png'),'complete_tool_return':ref(d/'raw'/f'{tag}_tool_return.json'),'prompt':ref(d/'prompts'/f'{tag}.txt'),'actual_arguments':ref(d/'prompts'/f'{tag}_tool_args.json'),'call_started':json.loads((d/'raw'/f'{tag}_call_times.json').read_text()),'call_completed':json.loads((d/'raw'/f'{tag}_completion_time.json').read_text()),'status':'independent_visual_pass','first_drafts':1,'revisions':0,'failed_attempts':0,'safety_blocks':0})
 write(d/'generation-log.json',{'mode':'builtin image_gen.imagegen','first_drafts':2,'revisions':0,'total_calls':2,'poses':poses,'all_image_payloads_retained':True})
 write(d/'QA-independent.json',{'scope':'Independent raw/transparent true-light/dark per-pose review. Final package review separate.','group_visual_gate':ref(g),'poses':ind,'qualified_count':2,'revisions_used':0})
 write(d/'QA-author.json',{'author':'draw_weier_ink_moer_actions','reviewed_utc':now,'status':'author_visual_pass_and_independent_pose_pass','character':c['slug'],'actual_viewed':['raw mother','transparent mother','old expression board','each generated raw','each selected true light and dark composite','combined Chinese light and dark board'],'poses':[json.loads((d/'review'/f'{p["key"]}_v1_author_visual_QA.json').read_text()) for p in c['plans']],'source_identity_and_sidedness':c['mother_image']['fixed_sides'],'processing':'Only alpha <=8 and alpha0 RGB cleanup; no anatomy edits, crops, palette changes, or stretching.','noncombat_static_only':True,'runtime_verified':False,'hard_errors':[]})
 source_ids=set(c['source_ids'])|{'root_agents','design_agents','archived_pixel_skill'}
 rows=[]
 for s in b['source_sha_snapshots']:
  if s['source_id'] not in source_ids and not s['source_id'].startswith(c['slug']):continue
  snap=D/'planning_sources/eleventh_new_character_actions_sources/files'/s['path'];assert snap.exists() and sha(snap)==s['sha256'] and sha(R/s['path'])==s['sha256'];rows.append({'source_id':s['source_id'],'source_path':s['path'],'snapshot':str(snap.relative_to(R)),'bytes':s['bytes'],'sha256':s['sha256']})
 write(d/'source_hashes.json',rows)
 (d/'README.md').write_text(f'# {c["name"]}（{c["canonical_id"]}）独立基础动作\n\n本目录为2张独立、非战斗、可逆静态关键姿态，均首稿通过，0修订。仅美术概念，不表示连续动画、任务已发生、装备兼容、碰撞或运行验收。\n\n逐字提示词、完整真实参数与全工具返回（含图像payload）、原始PNG、透明选稿、真浅深比较和逐稿独立审查均保留。源快照位于同批交付目录的 planning_sources 中，与 source_hashes.json 指向一致。所有输出先保存参数再用内置 imagegen 绘制；只清理 alpha≤8 与隐藏RGB。\n\n'+''.join(f'- {x["title_zh"]}：selected/{x["key"]}.png\n' for x in c['plans'])+'\n本角色与任何同名近名角色严格分开。未改母图、旧表情、角色卡、剧情文本、游戏、存档或Git。\n')
write(D/'selected_files.json',selected)
(D/'README.md').write_text('# 韦珥／摩珥基础动作完整来源包\n\n本组4张新独立全身静态动作，4首稿、0修订、0失败、0安全阻断。先通过计划门审，再逐稿独立审查，并由根实际查看中文母图浅深板。\n\n透明PNG为选稿；母图仅对照参考，不计新图。完整来源含相关卡、中文对白、母图、旧表情证据、逐字prompt/实际参数、完整工具返回image payload、raw和清理后PNG、浅深真alpha复合图、技术和独立QA、脚本与来源SHA。多个ZIP合起来是完整源包，各包可单独打开。\n\n本组仅静态美术概念，不代表连续动画、任务结果、装备兼容、碰撞或游戏运行验收。生成与用户收件是分开状态，本目录不声明已发送或已收件。\n')
print('Author records saved; waiting presentation gate before manifests/final package.')
