from pathlib import Path
import json,hashlib,datetime
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';b=a/'ninth_new_character_actions_brief.json';e=a/'ninth_actions_independent_details';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();j=json.loads(b.read_text()); by={s['source_id']:s for s in j['source_sha_snapshots']};errs=[];checks=0;quotes=[]
def chk(ok,kind,data):
 global checks
 checks+=1
 if not ok:errs.append({'kind':kind,'data':data})
for row in by.values():
 for k in ['path','snapshot_path']:
  p=r/row[k];chk(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'source',row[k])
for c in j['characters']:
 mp=r/c['mother_image']['manifest'];m=json.loads(mp.read_text())
 for row in m['files']:
  p=mp.parent/row['path'];chk(p.exists() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'mother_manifest_entry',str(p))
 for key in ['raw','transparent']:
  p=r/c['mother_image'][key];chk(sha(p)==c['mother_image'][key+'_sha256'],'mother_anchor',str(p))
 for plan in c['plans']:
  p=r/plan['prompt_file'];chk(p.read_text()==plan['prompt'] and sha(p)==plan['prompt_sha256'],'prompt_exact',plan['key'])
  for ev in plan['evidence']:
   p=r/by[ev['source_id']]['path'];line=p.read_text().splitlines()[ev['line_start']-1];chk(ev['quote'] in line,'literal_quote',[plan['key'],ev]);quotes.append({'pose':plan['key'],**ev,'actual_line':line})
  for path,h in zip(plan['reference_image_paths'],plan['reference_sha256']):chk(sha(r/path)==h,'ref_sha',plan['key'])
  others=[pp['title_zh'] for cc in j['characters'] for pp in cc['plans'] if pp['key']!=plan['key']];chk(not any(t in plan['prompt'] for t in others),'no_other_pose_title',plan['key'])
sm=r/j['source_snapshot_manifest']['path'];chk(sha(sm)==j['source_snapshot_manifest']['sha256'],'snapshot_manifest_hash',str(sm));s=json.loads(sm.read_text());chk(s['source_files']==j['source_sha_snapshots'],'source_index_identity',None)
for row in s['planning_support_files']:
 p=r/row['path'];chk(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'supporting',row['path'])
old=json.loads((e/'old_source_baseline.json').read_text())['files']
for row in old:
 p=r/row['path'];chk(p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'old_source_changed',row['path'])
out={'reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'brief_sha256':sha(b),'source_count':len(by),'old_source_count':len(old),'checks':checks,'errors':errs,'literal_quotes':quotes,'prompts':[{'key':p['key'],'prompt_sha256':p['prompt_sha256']} for c in j['characters'] for p in c['plans']]};(e/'plan_source_byte_audit.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['literal_quotes','prompts']},ensure_ascii=False));assert not errs
