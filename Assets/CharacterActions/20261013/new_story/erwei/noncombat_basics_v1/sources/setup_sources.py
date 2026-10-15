from pathlib import Path
import json,hashlib,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';bp=a/'sixth_new_character_actions_brief.json';b=json.loads(bp.read_text());h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert h(bp)=='2c3cd7e2481605a735ba5643dbe9cfe2cf86cfb825d59b1033c379cf897b98b8'
gate=a/'independent_sixth_new_character_actions_20261014.json';assert h(gate)=='453b6bd359f3e5ef401bcdd2557a5bdb07703e3090fbe417c61746626909fb9a'
for c in b['characters'][:2]:
 p=r/c['proposed_output_directory'];assert not p.exists();p.mkdir(parents=True)
 for x in ['raw','prompts','exports','review','sources/files','sources/planning_evidence']:(p/x).mkdir(parents=True,exist_ok=True)
 shutil.copyfile(bp,p/'sources'/bp.name);shutil.copyfile(gate,p/'sources'/gate.name)
 records=[]
 for s in b['source_sha_snapshots']:
  sid=s['source_id']
  if any(sid.startswith(other+'_') for other in ['erwei','chenger','weier','fouer'] if other!=c['slug']):continue
  source=r/s['snapshot_path'];assert h(source)==s['sha256']
  dst=p/'sources/files'/s['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dst)
  records.append({**s,'archive_path':str(dst.relative_to(p))})
 for f in (a/'sixth_new_character_actions_sources').iterdir():
  if f.is_file() and f.suffix=='.json':shutil.copyfile(f,p/'sources/planning_evidence'/f.name)
 (p/'sources/SOURCE_MANIFEST.json').write_text(json.dumps({'brief_sha256':h(bp),'plan_gate_sha256':h(gate),'sources':records},ensure_ascii=False,indent=2)+'\n')
 (p/'spec_lock.md').write_text('# '+c['name']+' '+c['canonical_id']+' 基础动作\n\n实际母图成年比例、像素簇、衣色与原道具为唯一身份锚；不复活历史数字。原画布完整人物加透明边距；内置imagegen纯alpha透明。一姿首稿加至多一次明确硬错修订；安全block即停止，不重试绕过。只允许alpha<=8和隐藏RGB清理，整图nearest等比合板，不脚本绘人体/道具、不拉伸/拼接/量化。\n'+c['mother_image']['fixed_sides']+'\n'+'\n'.join(c['story_boundaries'])+'\n只画独立关键姿态，非连续动画、非游戏落地或剧情结果。\n')
 for plan in c['plans']:
  key=plan['key']+'_v1';prompt=(r/plan['prompt_file']).read_text();assert prompt==plan['prompt'];assert hashlib.sha256(prompt.encode()).hexdigest()==plan['prompt_sha256']
  (p/'prompts'/f'{key}.txt').write_text(prompt)
  pars={'prompt':prompt,'referenced_image_paths':[str(r/x) for x in plan['reference_image_paths']],'transparent_background':True}
  (p/'prompts'/f'{key}_parameters.json').write_text(json.dumps(pars,ensure_ascii=False,indent=2)+'\n')
  print(str(p/'prompts'/f'{key}_parameters.json'))
 shutil.copyfile('/tmp/setup_erwei_chenger_actions.py',p/'sources/setup_sources.py')
