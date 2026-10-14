from pathlib import Path
import json,shutil,hashlib,datetime
R=Path.cwd(); B=R/'Assets/EnemyDesigns/20261013/second_six'; bp=B/'action_continuation_brief_v1.json'; b=json.loads(bp.read_text()); sm=json.loads((B/'action_continuation_sources_v1/source_manifest.json').read_text())
assert hashlib.sha256(bp.read_bytes()).hexdigest()=='aaf6be2a971fc0b1b8fd9b8be91a6789d8a9be9ad5683fc6cd0032aeaed2e1f3'
def write(p,v):
 assert not p.exists(),p
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
for i in b['items']:
 if not i['concept_id'].endswith(('009','010')):continue
 d=R/i['planned_output_directory'];d.mkdir(parents=True,exist_ok=False)
 write(d/'item_brief.json',i)
 shutil.copy2(bp,d/'sources/action_continuation_brief_v1.json') if (d/'sources').exists() else ((d/'sources').mkdir(),shutil.copy2(bp,d/'sources/action_continuation_brief_v1.json'))
 copied=[]
 for s in sm['files']:
  sp=s['source_path']; is_enemy='/second_six/' in sp and any(x in sp for x in [f'/{j["slug"]}/' for j in b['items']])
  if is_enemy and f'/{i["slug"]}/' not in sp:continue
  p=R/s['snapshot_path']; dest=d/'sources/files'/sp;dest.parent.mkdir(parents=True,exist_ok=True)
  assert hashlib.sha256(p.read_bytes()).hexdigest()==s['sha256'],p
  shutil.copy2(p,dest);copied.append({**s,'copied_path':str(dest.relative_to(d))})
 write(d/'sources/source_manifest.json',{'scope':'All relevant frozen item references and shared production sources. Non-input old rejected images are not reclassified as current inputs.','files':copied})
 shutil.copy2(B/'action_continuation_sources_v1/source_manifest.json',d/'sources/planning_source_manifest_full.json')
 (d/'spec_lock.md').write_text('# 本轮关键姿态执行锁定\n\n'+json.dumps({'concept_id':i['concept_id'],'identity_lock':i['identity_lock'],'pose_mechanics':i['pose_mechanics'],'pass_conditions':i['pass_conditions'],'hard_fail_conditions':i['hard_fail_conditions'],'format':'Native RGBA; entire subject and props fit with margin; canvas follows pose. No fixed runtime grid.','processing':'Only alpha cleanup if visibly justified, and nearest-neighbor uniform display scaling. No body painting or stretching.','budget':'One first draft; at most one documented hard-error revision.','claims':'Independent keypose concept; animation anchors, exact palette, equipment integration and runtime unverified.'},ensure_ascii=False,indent=2)+'\n')
 # Prompt is exactly the argument string, deliberately no added newline.
 args=i['planned_tool_call']['arguments'];(d/'prompt_v1.txt').write_text(args['prompt']);write(d/'tool_args_v1.json',args)
 write(d/'pre_generation_checks.json',{'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'brief_sha256':hashlib.sha256(bp.read_bytes()).hexdigest(),'root_release':'Explicit generation release received 2026-10-14 04:20:27 UTC.','independent_plan_gate':'Reviewer explicitly passed 2026-10-14 04:20:02 UTC.','source_images':[{'path':s['snapshot_path'],'sha256':s['sha256'],'actual_viewed':True,'sha256_verified':True} for s in i['source_images']],'missing_archived_reference':'pixel-asset-master/references/executor-pixel.md not present; archived SKILL.md and current approved brief/STYLE_DIRECTION read.','subagent_style_authorization':'Parent confirms user explicitly authorized continued pixel-art subagent generation using existing style without repeating six-confirmation workflow.','generation_calls_so_far':0})
 print(str(d.relative_to(R)),len(copied),'sources')
