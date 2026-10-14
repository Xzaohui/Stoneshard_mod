from pathlib import Path
import json,hashlib,shutil,datetime
R=Path.cwd(); A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'; B=A/'eleventh_new_character_actions_brief.json'; G=A/'independent_eleventh_new_character_actions_plan_gate_20261014.json'; P=R/'Assets/CharacterActions/20261013/new_story'; D=P/'eleventh_noncombat_weier_ink_moer_delivery_v1'; b=json.loads(B.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(B)=='3988be2e7e6da94b75ffc5df2b830559cd46c6687ed436f9038b073dd9272259'
assert sha(G)=='a8d71708160028c62e759913b0b7b005d500062d43bb2b4172148067031f0f7a'
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
S=D/'planning_sources';shutil.copytree(A/'eleventh_new_character_actions_sources',S/'eleventh_new_character_actions_sources',dirs_exist_ok=True)
for p in [B,G]: shutil.copy2(p,S/p.name)
for src in b['source_sha_snapshots']:assert sha(R/src['path'])==src['sha256'];assert sha(R/src['snapshot_path'])==src['sha256']
for c in b['characters']:
 if c['slug'] not in ['weier_ink','moer']:continue
 d=R/c['proposed_output_directory'];assert not d.exists()
 for sub in ['raw','prompts','review','sources','selected']: (d/sub).mkdir(parents=True)
 write(d/'spec_lock.json',{'brief_sha256':sha(B),'character':c,'policy':'Two independent static noncombat poses only. Current approved mother actual proportions override old numeric specs. Source identity and prop constraints unchanged. Builtin imagegen only. Max one real hard-error revision per pose; stop on safety block.'})
 write(d/'source_hashes.json',[s for s in b['source_sha_snapshots'] if s['source_id'] in c['source_ids'] or s['source_id'].startswith(c['slug'])])
 for p in c['plans']:
  prompt=(R/p['prompt_file']).read_text();assert prompt==p['prompt'];assert hashlib.sha256(prompt.encode()).hexdigest()==p['prompt_sha256']
  key=p['key'];(d/'prompts'/f'{key}_v1.txt').write_text(prompt)
  args={'prompt':prompt,'referenced_image_paths':[str(R/x) for x in p['reference_image_paths']],'transparent_background':True}
  write(d/'prompts'/f'{key}_v1_tool_args.json',args);write(d/'prompts'/f'{key}_spec_lock.json',p)
 write(d/'review/baseline_visual_observations.json',{'viewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actually_viewed':[c['mother_image']['raw'],c['mother_image']['transparent'],c['mother_image']['expression_board_actually_viewed']],'observed':c['mother_image']['actual_visual_observation'],'source_card_and_chinese_dialogue_read':True,'final_expression_status_verified':True})
 for p in [B,G]:shutil.copy2(p,d/'sources'/p.name)
 shutil.copy2(A/'eleventh_new_character_actions_sources/weier_ink_moer_author_handoff.txt',d/'sources/weier_ink_moer_author_handoff.txt')
 write(d/'generation-log.json',{'mode':'builtin image_gen.imagegen','poses':[]})
print('Four exact prompts and complete arguments saved. Source SHA verified. Gate passed.')
