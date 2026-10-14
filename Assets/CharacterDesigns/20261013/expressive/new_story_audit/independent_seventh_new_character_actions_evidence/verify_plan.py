from pathlib import Path
import json,hashlib,datetime
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';b=a/'seventh_new_character_actions_brief.json';e=a/'independent_seventh_new_character_actions_evidence';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=json.loads(b.read_text()); by={s['source_id']:s for s in j['source_sha_snapshots']};errs=[];checks=0
for row in by.values():
 for k in ['path','snapshot_path']:
  p=r/row[k];checks+=1
  if not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:errs.append([k,row['source_id']])
for c in j['characters']:
 m=json.loads((r/c['mother_image']['manifest']).read_text())
 for key in ['raw','transparent']:
  p=r/c['mother_image'][key];row=next(x for x in m['files'] if x['path']==p.name);checks+=1
  if sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes'] or sha(p)!=c['mother_image'][key+'_sha256']:errs.append(['mother_manifest',str(p)])
 for plan in c['plans']:
  p=r/plan['prompt_file'];checks+=1
  if p.read_text()!=plan['prompt'] or sha(p)!=plan['prompt_sha256']:errs.append(['prompt',plan['key']])
  for ev in plan['evidence']:
   p=r/by[ev['source_id']]['path'];checks+=1
   if ev['quote'] not in p.read_text().splitlines()[ev['line_start']-1]:errs.append(['quote',plan['key'],ev])
  for path,h in zip(plan['reference_image_paths'],plan['reference_sha256']):
   checks+=1
   if sha(r/path)!=h:errs.append(['reference',plan['key']])
sm=r/j['source_snapshot_manifest']['path'];checks+=1
if sha(sm)!=j['source_snapshot_manifest']['sha256']:errs.append(['snapshot_manifest_hash'])
s=json.loads(sm.read_text());checks+=1
if s['sources']!=j['source_sha_snapshots']:errs.append(['snapshot_sources'])
for row in s['supporting_files']:
 p=r/row['path'];checks+=1
 if not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:errs.append(['supporting',row['path']])
for row in json.loads((e/'old_source_baseline.json').read_text())['files']:
 p=r/row['path'];checks+=1
 if not p.is_file() or p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:errs.append(['old_source_changed',row['path']])
rows=[]
for c in j['characters']:
 for p in c['plans']:rows.append({'key':p['key'],'prompt_sha256':p['prompt_sha256']})
out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'brief_sha256':sha(b),'source_count':len(by),'old_source_count':246,'checks':checks,'errors':errs,'prompts':rows}
(e/'plan_source_byte_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps(out,ensure_ascii=False));assert not errs
