from pathlib import Path
import json,hashlib,shutil,datetime
R=Path.cwd(); B=R/'Assets/CharacterDesigns/20261013/expressive'; brief=B/'new_story_audit/eleventh_four_expression_brief.json'; j=json.loads(brief.read_text()); assert hashlib.sha256(brief.read_bytes()).hexdigest()=='24285adc443e0584a90b7ca885c0aff5d5ed60bb08e42fd2045ae9a95e3c6226'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for c in j['characters'][:2]:
 d=B/'new_story'/c['slug']/'expressions_v1'
 assert not d.exists(),str(d)
 for sub in ['sources/files','prompts','raw','selected','review']: (d/sub).mkdir(parents=True,exist_ok=True)
 paths=['AGENTS.md','design/AGENTS.md',str(brief.relative_to(R)),str((B/'STYLE_DIRECTION.md').relative_to(R)),str((B/'reference/pixel-asset-master/SKILL.md').relative_to(R)),c['current_card']['path'],c['source_anchor']['selected_raw']['path'],c['source_anchor']['transparent']['path'],c['source_anchor']['manifest']['path'],c['source_anchor']['directory']+'/spec_lock.md',j['source_independent_review']['path']]
 for e in c['expressions']:
  paths += [e['story_support']['path'],e['research_support']['path']]
 for conflict in j['source_conflicts']:
  if conflict['character']==c['slug']: paths += [p['path'] for p in conflict['sources']]
 idx=[]
 for p in dict.fromkeys(paths):
  src=R/p; dst=d/'sources/files'/p;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);assert sha(src)==sha(dst)
  idx.append({'original_path':p,'snapshot_path':str(dst.relative_to(d)),'sha256':sha(src),'bytes':src.stat().st_size})
 (d/'sources/source_index.json').write_text(json.dumps({'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':idx},ensure_ascii=False,indent=2))
 (d/'spec_lock.md').write_text(f"# {c['name']} 两张可逆表情执行锁定\nID {c['canonical_id']} / {c['slug']}。既有已授权风格延续；独立静态概念，不是动画或运行资源。\n"+c['age_identity_lock']+'\n'+c['observed_mother_image']+'\n'+'\n'.join(c['fixed_prop_sides'])+'\n母图1118×1407，保留完整纵向构图与本人实际比例；builtin imagegen透明背景，色彩只从本人母图延续。不拉伸、不脚本绘人、不量化，只alpha≤8归零及alpha0隐藏RGB清理，展示只等比nearest。每张首稿最多一次明确硬错修订；安全拦截停止该张。\n'+'\n'.join(e['key']+'：'+e['label_zh']+'；'+e['face_changes'] for e in c['expressions']))
 for e in c['expressions']:
  p=d/'prompts'/f"{e['key']}_initial.txt";p.write_text(e['prompt_text'],encoding='utf-8')
  args={'prompt':e['prompt_text'],'referenced_image_paths':[str(R/c['source_anchor'][k]['path']) for k in ['selected_raw','transparent']],'transparent_background':True}
  (d/'prompts'/f"{e['key']}_initial_parameters.json").write_text(json.dumps(args,ensure_ascii=False,indent=2))
  evidence={'phase':'initial','status':'ready_not_called','prompt_file':str(p.relative_to(d)),'prompt_sha256':sha(p),'parameters_file':f"prompts/{e['key']}_initial_parameters.json",'input_images':[c['source_anchor'][k] for k in ['selected_raw','transparent']]}
  (d/'prompts'/f"{e['key']}_initial_evidence.json").write_text(json.dumps(evidence,ensure_ascii=False,indent=2))
 print(c['slug'],len(idx),'source snapshots prepared')
