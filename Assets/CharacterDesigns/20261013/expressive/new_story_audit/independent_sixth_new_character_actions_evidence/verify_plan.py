from pathlib import Path
import json,hashlib,datetime
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');a=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';d=json.loads((a/'sixth_new_character_actions_brief.json').read_text());errs=[];count=0;by={s['source_id']:s for s in d['source_sha_snapshots']};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for s in by.values():
 for k in ['path','snapshot_path']:
  p=r/s[k];count+=1
  if not p.is_file() or p.stat().st_size!=s['bytes'] or sha(p)!=s['sha256']:errs.append([k,s['source_id']])
for c in d['characters']:
 p=r/c['mother_image']['manifest'];m=json.loads(p.read_text());sel=[c['mother_image']['raw'],c['mother_image']['transparent']]
 for name in sel:
  p=r/name;row=next(x for x in m['files'] if x['path']==p.name);count+=1
  if p.stat().st_size!=row['bytes'] or sha(p)!=row['sha256']:errs.append(['mother_manifest',name])
 for p in c['plans']:
  f=r/p['prompt_file'];count+=2
  if f.read_text()!=p['prompt'] or sha(f)!=p['prompt_sha256']:errs.append(['prompt',p['key']])
  for ev in p['evidence']:
   s=r/by[ev['source_id']]['path'];lines=s.read_text().splitlines();count+=1
   if ev['quote'] not in lines[ev['line_start']-1]:errs.append(['quote_line',p['key'],ev])
  for path,h in zip(p['reference_image_paths'],p['reference_sha256']):
   count+=1
   if sha(r/path)!=h:errs.append(['ref_sha',p['key']])
sm=r/d['source_snapshot_manifest']['path'];count+=1
if sha(sm)!=d['source_snapshot_manifest']['sha256']:errs.append(['snapshot_manifest'])
smj=json.loads(sm.read_text());count+=1
if smj['sources']!=d['source_sha_snapshots']:errs.append(['sources_disagree'])
for row in smj['derived_files']:
 p=r/row['path'];count+=1
 if not p.is_file() or sha(p)!=row['sha256'] or p.stat().st_size!=row['bytes']:errs.append(['derived',row['path']])
weier=next(c for c in d['characters'] if c['slug']=='weier');assert all('脚尖探触只是正常短步' not in p['prompt'] for p in weier['plans'])
out={'checks':count,'sources':len(by),'errors':errs,'brief_sha256':sha(a/'sixth_new_character_actions_brief.json')};print(json.dumps(out,ensure_ascii=False))
assert not errs
jr=json.loads((a/'independent_sixth_new_character_actions_20261014.json').read_text());jr['status']='plan_gate_pass_waiting_generated_assets';jr['brief']={'path':str((a/'sixth_new_character_actions_brief.json').relative_to(r)),'sha256':out['brief_sha256']};jr['mother_sha_bound_to_frozen_concept_manifests']=True
jr['plan_gate']={'verdict':'pass','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_snapshot_prompt_and_quote_checks':count,'source_count':len(by),'hash_errors':errs,'current_character_cards_and_four_dialogue_sections_read':True,'source_visual_views_field':'source_visual_views','all_eight_complete_prompts_read':True,'mother_raw_and_selected_sha_bound_to_frozen_manifest':True,'dedup_independent_scan':jr['independent_prior_action_scan'],'dedup_note':'Independently scanned action-tree paths and 210 Assets ZIPs. Target action directories absent; matching archive assets are existing mother/expression/reference material. FX-INK weier_ink excluded. Planning scan additionally covers action-tree and ZIP text with source-only matches. Eight proposed poses create new physical contacts or support geometry, not face-only updates.','corrections_before_generation':[{'prior_brief_sha256':'40da4052ecded1f97f2525f2341fb594c819ed92f3566773882fe9aff5f712fe','issue':'Weier A2 inherited affirmative toe-step wording in shared risk constraints despite full-sole standing.','resolved':'Shared risks now neutral daily-activity boundary; A1 retains toe probe and A2 explicitly retains full-sole low horizontal stick hold.'}],'visual_scope_notes':['Preserve each actual mother ratio; no global numeric ratio.','Erwei A1 grips original two pot ears; A2 right palm contacts red apron patch and left hand rests on grounded pot ear.','Chenger remains seated in both poses; lantern stays anatomical right, screen left, grounded.','Weier is FX-HOM, not FX-INK; shoulder bag stays anatomical left while A2 releases strap to support same short stick.','Fouer remains seated with one closed board, one original charcoal in anatomical left cuff; no exposed list.','First draft plus at most one genuine hard-error revision per pose; safety block stops without circumvention.'],'generation_count_at_gate':0,'current_action_delivery_index':{'path':by['action_delivery_index']['path'],'sha256':by['action_delivery_index']['sha256'],'delivered_existing_characters':20,'qualified_static_poses':38}}
jr['source_limitations']=[{'path':'research/field-npc-dialogue.json','sha256':by['field_dialogue_registry']['sha256'],'lines':'FX-HOM begins1157; Chinese site/visits1194–1226; mismatched English1234–1241','finding':'English site/visit slots contain dye-tub, grain-handout and relative semantics inconsistent with the current Chinese scavenger card/dialogue. This batch anchors Chinese and does not modify story source.'},{'finding':'FX-CP5 legacy spoken no-name/no-food wording conflicts with current DT13 voluntary/family-number route; poses do not implement or endorse that eligibility gate.','source_in_brief':'fouer.story_boundaries'}]
(a/'independent_sixth_new_character_actions_20261014.json').write_text(json.dumps(jr,ensure_ascii=False,indent=2)+'\n'); print('review sha',sha(a/'independent_sixth_new_character_actions_20261014.json'))
