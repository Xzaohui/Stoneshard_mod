from pathlib import Path
import json, hashlib, base64, datetime, shutil
import numpy as np
from PIL import Image

r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
b=r/'Assets/CharacterActions/20261013/new_story'
audit=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slugs={'lier':{'name':'栎珥','id':'FX-CV5','selected':['lier_A2_low_right_foot_return_step_v1'],'failed':['lier_A1_gather_two_rope_tails_v1','lier_A1_gather_two_rope_tails_v2'],'missing':['lier_A1_gather_two_rope_tails']},'huier':{'name':'洄珥','id':'FX-CV6','selected':['huier_A1_raise_right_hand_brow_shade_v1','huier_A2_two_hand_settle_carry_strap_v1'],'failed':[],'missing':[]}}
vg=audit/'independent_seventh_new_character_actions_lier_huier_visual_gate_20261014.json'
bg=audit/'independent_seventh_new_character_actions_lier_huier_board_gate_20261014.json'
assert vg.exists() and bg.exists(),'Require independent visual and board gates before production closeout'
for slug,c in slugs.items():
 d=b/slug/'noncombat_basics_v1'
 for g,name in [(vg,'independent_visual_gate.json'),(bg,'independent_board_gate.json')]:shutil.copy2(g,d/'review'/name)
 evidence=audit/'independent_seventh_new_character_actions_evidence'
 for p in evidence.glob(slug+'*_byte_audit.json'):shutil.copy2(p,d/'review'/('independent_'+p.name))
 for name in ['audit_pose.py','record_visual.py']:
  if (evidence/name).exists():shutil.copy2(evidence/name,d/'sources'/('independent_'+name))
 attempts=[]
 for p in sorted((d/'raw').glob('*_tool_return.json')):
  stem=p.name.removesuffix('_tool_return.json');raw=d/'raw'/f'{stem}_raw.png';clean=d/'exports'/f'{stem}_transparent.png';pp=d/'prompts'/f'{stem}.txt';params=d/'prompts'/f'{stem}_parameters.json'
  ret=json.loads(p.read_text());args=json.loads(params.read_text());assert args['prompt']==pp.read_text();assert base64.b64decode(ret['image_url'].split(',',1)[1])==raw.read_bytes();assert args['transparent_background'] is True
  a=np.array(Image.open(raw).convert('RGBA'));q=np.array(Image.open(clean).convert('RGBA'));expected=a.copy();expected[expected[:,:,3]<=8]=0;assert np.array_equal(expected,q)
  refs=[{'path':s,'sha256':sha(Path(s))} for s in args['referenced_image_paths']]
  assert len(refs)==1 and slug+'/concept_v1/'+slug+'_transparent.png' in refs[0]['path']
  rec={'stem':stem,'status':'selected_independent_visual_pass' if stem in c['selected'] else 'failed_retained_not_selected','prompt_file':str(pp.relative_to(d)),'prompt_sha256':sha(pp),'parameters_file':str(params.relative_to(d)),'parameters_sha256':sha(params),'raw_file':str(raw.relative_to(d)),'raw_sha256':sha(raw),'transparent_file':str(clean.relative_to(d)),'transparent_sha256':sha(clean),'complete_tool_return_file':str(p.relative_to(d)),'complete_tool_return_sha256':sha(p),'image_payload_decodes_exactly_to_raw':True,'exact_saved_prompt_used_as_tool_argument':True,'reference_images':refs,'transparent_background_requested':True,'foreground_alpha_gt8_unchanged':True,'processing':'Only RGBA zeroing at alpha<=8; no other changes','raw_and_transparent_and_true_light_dark_actually_viewed_by_author':True,'output_hint':ret.get('output_hint')}
  attempts.append(rec)
 sourcechecks=[]
 for s in json.loads((d/'sources/SOURCE_MANIFEST.json').read_text()):
  p=r/s['path'];q=d/s['local_copy'];sourcechecks.append({'path':s['path'],'expected_sha256':s['sha256'],'copy_matches':sha(q)==s['sha256'],'original_still_matches':sha(p)==s['sha256']})
 assert all(x['copy_matches'] and x['original_still_matches'] for x in sourcechecks)
 manifest={'schema_version':1,'author_sole_writer':'draw_lier_huier_actions','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'character':slug,'name':c['name'],'canonical_id':c['id'],'scope':'independent fullbody noncombat keyposes; no new character or animation','planned_action_count':2,'selected_action_count':len(c['selected']),'generation_calls':len(attempts),'initial_calls':2,'hard_error_revision_calls':len(attempts)-2,'selected':c['selected'],'missing':c['missing'],'attempts':attempts,'independent_visual_gate_sha256':sha(vg),'independent_board_gate_sha256':sha(bg),'runtime_verified':False,'pixel_grid_verified':False,'equipment_layers_verified':False,'full_animation_verified':False,'git_upload_user_send_performed_by_author':False}
 (d/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
 qa={'author':'draw_lier_huier_actions','actual_visual_source_read_log':'review/source_visual_read_record.json','attempts':[{k:v for k,v in a.items() if k not in ['output_hint']} for a in attempts],'source_checks':sourcechecks,'gate_status':'independent_visual_and_board_pass_for_selected_only','missing_reason':('A1首稿及唯一修订均只有一个尾结在右掌上，另一个仍悬在指端外，未实现双尾同掌托起。预算用满，缺项，不第三稿、不改名重试。' if c['missing'] else None),'author_cannot_replace_independent_review':True}
 (d/'review/QA_author_source_and_pixels.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2))
 status={'status':'production_closed_with_one_missing' if c['missing'] else 'production_complete','author_sole_writer':'draw_lier_huier_actions','character':slug,'selected':c['selected'],'selected_count':len(c['selected']),'missing':c['missing'],'all_attempts_preserved':True,'first_draft_and_max_one_hard_error_revision_per_pose':True,'source_and_visual_gates_recorded':True,'production_source_frozen':True,'delivery_status':'package verification recorded separately in group delivery manifest','upload_or_user_send_performed':False,'runtime_verified':False}
 (d/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
 note=f'# {c["name"]}基础动作制作记录\n\n人物 {c["id"]}，已有角色。本次计划2张独立全身非战斗姿态，合格{len(c["selected"])}张。\n\n'
 note+='\n'.join('- '+s for s in c['selected'])+'\n\n'
 if c['missing']:note+='缺项：A1横臂收托两根绳尾。首稿及唯一修订未实现双尾同掌托住，均保留在raw/exports/review以供审计，不计选稿；不再重试。\n\n'
 note+='raw保留完整工具返回（含原图payload）与原PNG；prompts保留逐字提示词和实际参数；sources保留原始来源SHA、复制来源、冻结brief与计划门审；review含真实浅深合成、独审与作者检查。脚本仅清理alpha≤8及透明隐藏RGB、整图nearest等比排版，不修改人体或道具。\n\n非战斗静态演出提案，不代表任务结果、完整动画、目标像素网格、装备拆层、碰撞或游戏运行通过。未修改母图、表情、角色卡、游戏或存档，未Git、上传或发送。\n'
 (d/'README_中文.md').write_text(note)
 print(slug,'closed',len(c['selected']),'selected',len(c['missing']),'missing')
