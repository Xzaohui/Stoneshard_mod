from pathlib import Path
import json,hashlib,shutil,zipfile,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=r/'Assets/CharacterActions/20261013/new_story';d=base/'luoer_qiner_noncombat_basics_v1_delivery';audit=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';brief=json.loads((audit/'seventh_new_character_actions_brief.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rec=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
vis=audit/'independent_seventh_new_character_actions_luoer_qiner_visual_gate_20261014.json'; bg=audit/'independent_seventh_new_character_actions_luoer_qiner_board_gate_20261014.json'
assert vis.exists(); assert bg.exists()
report={'author':'draw_luoer_qiner_actions','actual_source_views':['luoer mother raw','luoer mother transparent','luoer expression light board','qiner mother raw','qiner mother transparent','qiner expression light board'],'generation_views':20,'joint_board_actually_viewed':True,'source_sha_checks':[],'processing_policy':'Only alpha <=8 and hidden RGB zeroing; original high-alpha RGBA pixels unchanged. Full canvas NEAREST uniform board scaling only; no body/prop editing.','qiner_A1_deviation':'叶梢略高于下巴，但与口鼻有明显侧向空隙，不入口；独审视为轻微构图偏差，保留，不作无效审美修订。'}
for s in brief['source_sha_snapshots']:
 f=r/s['path'];ok=sha(f)==s['sha256'];assert ok,s['path'];report['source_sha_checks'].append({'source_id':s['source_id'],'path':s['path'],'sha256':s['sha256'],'current_matches':ok})
(d/'QA_author_source_and_pixels.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
selecteds={'luoer':['luoer_A1_support_lower_rope_coil_v2','luoer_A2_settle_neck_scarf_v1'],'qiner':['qiner_A1_raise_existing_sprig_v1','qiner_A2_smooth_basket_lining_front_v1']}
for c in brief['characters'][:2]:
 slug=c['slug'];p=base/slug/'noncombat_basics_v1';keys=selecteds[slug]
 for f in [vis,bg,d/'QA_author_source_and_pixels.json']:shutil.copy2(f,p/'review'/f.name)
 for f in ['/tmp/process_luoer_qiner_actions.py','/tmp/compose_luoer_qiner_board.py','/tmp/finalize_luoer_qiner_actions.py']:shutil.copy2(f,p/'sources'/Path(f).name)
 selected=[]
 for key,a in zip(keys,c['plans']):
  transparent=p/'exports'/f'{key}_transparent.png';raw=p/'raw'/f'{key}_raw.png';selected.append({'key':key,'title_zh':a['title_zh'],'transparent':rec(transparent),'raw':rec(raw),'status':'pass_independent_visual_and_provenance'});shutil.copy2(transparent,d/transparent.name)
 status={'schema_version':1,'created_utc':'2026-10-14T06:48:00Z','author':'draw_luoer_qiner_actions','solewriter':True,'status':'independent_visual_and_board_pass_package_review_pending','character':slug,'canonical_id':c['canonical_id'],'selected_pose_count':2,'initial_generations':2,'revision_generations':1 if slug=='luoer' else 0,'selected':selected,'excluded_versions':[{'key':'luoer_A1_support_lower_rope_coil_v1','status':'failed_contact_retained','reason':'右掌位于下卷前面/孔口附近，未托最低外侧底缘。全部证据保留；唯一v2修订已通过。'}] if slug=='luoer' else [],'missing_poses':[],'visual_gate':rec(vis),'board_gate':rec(bg),'board':rec(d/'珞珥_芩珥_母图动作浅深对照.png'),'plan_sha256':'ecdd08ad29f8408455edd158430b24dfe37fd88fedf81349566696b48e89483a','runtime_verified':False,'animation_verified':False,'uploaded':False,'git_actions':False}
 (p/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
 (p/'README_中文.md').write_text('# '+c['name']+'基础动作概念\n\n两张独立非战斗全身关键姿态。原母图身份、年龄、衣装、物件与比例保留。不是连续动画、装备层、精灵网格或游戏运行验收。\n\n'+ '\n'.join('- '+x['key']+'：'+x['title_zh'] for x in selected)+'\n\n首稿2张；硬错修订'+str(status['revision_generations'])+'张。所有原稿、完整含图片payload的生成返回、逐字prompt/实际参数、透明版、真浅深、来源副本/哈希、处理脚本与独审保存。\n\n'+('A1首稿托底接点失败留档，选唯一v2；A2选v1。' if slug=='luoer' else 'A1叶梢高于计划下巴线，但距口鼻有侧向空隙；独审认定不构成真实硬错，保留轻微构图偏差。')+'\n\n状态以作者唯一写入的FINAL_STATUS.json为准。\n')
 manifest={str(f.relative_to(p)):{'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(p.rglob('*')) if f.is_file() and f != p/'manifest.json'}
 (p/'manifest.json').write_text(json.dumps({'files':manifest,'scope':'This character working artifact tree, including rejected attempt if present; complete planning snapshot supplied as separate ordinary ZIP.'},ensure_ascii=False,indent=2)+'\n')
# Each archive is an independently openable standard ZIP; no split-volume format, no missing evidence.
archives=[]
for slug,name in [('luoer','珞珥'),('qiner','芩珥')]:
 p=base/slug/'noncombat_basics_v1';z=d/(name+'_基础动作_完整源包.zip')
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
  for f in sorted(p.rglob('*')):
   if f.is_file():out.write(f,str(f.relative_to(base)))
 with zipfile.ZipFile(z) as zz:assert zz.testzip() is None
 assert z.stat().st_size<18*1024**2,(z,z.stat().st_size);archives.append(rec(z))
z=d/'第七批_规划全量来源.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
 for f in sorted((audit/'seventh_new_character_actions_sources').rglob('*')):
  if f.is_file():out.write(f,str(f.relative_to(audit)))
 for f in [audit/'seventh_new_character_actions_brief.json',audit/'independent_seventh_new_character_actions_plan_gate_20261014.json']:out.write(f,f.name)
with zipfile.ZipFile(z) as zz:assert zz.testzip() is None
assert z.stat().st_size<18*1024**2;archives.append(rec(z))
(d/'SOURCE_PACKAGE_INDEX.json').write_text(json.dumps({'status':'package_independent_review_pending','ordinary_zip_count':len(archives),'archives':archives,'files':{'selected_transparents':[rec(d/(key+'_transparent.png')) for keys in selecteds.values() for key in keys],'joint_board':rec(d/'珞珥_芩珥_母图动作浅深对照.png')},'selected_pose_count':4,'retained_rejected_attempt_count':1,'complete_payloads_preserved':5,'full_planning_source_snapshot_count':69,'not_delivered_or_uploaded':True},ensure_ascii=False,indent=2)+'\n')
for a in archives:print(json.dumps(a,ensure_ascii=False))
