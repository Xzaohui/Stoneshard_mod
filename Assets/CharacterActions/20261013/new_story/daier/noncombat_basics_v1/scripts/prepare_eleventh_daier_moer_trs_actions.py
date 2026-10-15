from pathlib import Path
import json,hashlib,shutil,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod'); A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'; brief=A/'eleventh_new_character_actions_brief.json';gate=A/'independent_eleventh_new_character_actions_plan_gate_20261014.json';b=json.loads(brief.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();import sys;assert sha(brief)==sys.argv[1];assert json.loads(gate.read_text())['verdict']=='PASS_ELEVENTH_NEW_CHARACTER_ACTIONS_PLAN_GATE'
for c in b['characters']:
 if c['slug'] not in ['daier','moer_trs']:continue
 d=R/c['proposed_output_directory'];assert not d.exists()
 for p in ['sources/files','prompts','raw','selected','review/raw_composites','review/independent']:(d/p).mkdir(parents=True,exist_ok=True)
 ids=set(c['source_ids']+['root_agents','design_agents','archived_pixel_skill','style_direction','eleventh_mother_qa',c['slug']+'_mother_spec_historical',c['slug']+'_expression_manifest',c['slug']+'_expression_independent_qa'])
 entries=[]
 for e in b['source_sha_snapshots']:
  if e['source_id'] not in ids:continue
  p=R/e['path'];assert sha(p)==e['sha256'];q=d/'sources/files'/e['path'];q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q);entries.append({'role':e['source_id'],'source_path':e['path'],'path':str(q.relative_to(d)),'sha256':sha(p)})
 for p in [brief,gate,A/'eleventh_new_character_actions_sources/SNAPSHOT_MANIFEST.json',A/'eleventh_new_character_actions_sources/daier_moer_trs_author_handoff.txt']:
  q=d/'sources'/p.name;shutil.copy2(p,q);entries.append({'role':'plan_gate_or_handoff','source_path':str(p.relative_to(R)),'path':str(q.relative_to(d)),'sha256':sha(p)})
 (d/'sources/source_index.json').write_text(json.dumps({'entries':entries},ensure_ascii=False,indent=2)+'\n')
 (d/'spec_lock.md').write_text('# '+c['name']+' 第十一批基础动作锁定\n\n'+json.dumps(c,ensure_ascii=False,indent=2)+'\n\n只按本姿独立prompt调用。母图实比，不套数字。每姿1首稿，最多1次真硬错修订，安全block停止；内置imagegen负责人物，脚本只alpha≤8与隐藏RGB清理、整图nearest等比排版；保全返回payload与所有尝试。不动画、不游戏落地、不Git、不上传。\n')
 (d/'generation-log.json').write_text(json.dumps({'generator':'builtin imagegen','calls':[]},indent=2)+'\n')
 for p in c['plans']:
  s=p['key']+'_initial';prompt=(R/p['prompt_file']).read_text();assert hashlib.sha256(prompt.encode()).hexdigest()==p['prompt_sha256'];(d/'prompts'/f'{s}.txt').write_text(prompt)
  args={'prompt':prompt,'referenced_image_paths':[str(R/x) for x in p['reference_image_paths']],'transparent_background':True};(d/'prompts'/f'{s}_tool_arguments.json').write_text(json.dumps(args,ensure_ascii=False,indent=2)+'\n')
 print(d)
