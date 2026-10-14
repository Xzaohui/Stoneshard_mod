from pathlib import Path
import json,hashlib,shutil,zipfile,sys
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');b=r/'Assets/CharacterActions/20261013/new_story';d=b/'luoer_qiner_noncombat_basics_v1_delivery';gate=r/sys.argv[1];gate_data=json.loads(gate.read_text());assert gate_data.get('errors') == [['manifest_set', 'luoer'], ['manifest_set', 'qiner']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rec=lambda p:{'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
for slug in ['luoer','qiner']:
 p=b/slug/'noncombat_basics_v1';shutil.copy2(gate,p/'review'/gate.name);shutil.copy2(__file__,p/'sources'/Path(__file__).name);shutil.copy2('/tmp/finalize_luoer_qiner_actions.py',p/'sources/finalize_luoer_qiner_actions.py')
 f=p/'FINAL_STATUS.json';j=json.loads(f.read_text());j['status']='frozen_visual_selection_package_closure_recorded_externally';j['package_state_at_creation']='pending_final_review_after_manifest_coverage_fix';j['group_freeze_record']='Assets/CharacterActions/20261013/new_story/luoer_qiner_noncombat_basics_v1_delivery/FREEZE_RECORD.json';j['package_review']=rec(gate);j['frozen_at_utc']=sys.argv[2];j['solewriter']=True;f.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
 files={str(q.relative_to(p)):{'bytes':q.stat().st_size,'sha256':sha(q)} for q in sorted(p.rglob('*')) if q.is_file() and q != p/'manifest.json'}
 (p/'manifest.json').write_text(json.dumps({'files':files,'scope':'Frozen full character artifact tree. Complete shared planning snapshot is the separate planning source ZIP.'},ensure_ascii=False,indent=2)+'\n')
 name='珞珥' if slug=='luoer' else '芩珥';z=d/(name+'_基础动作_完整源包.zip')
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as zz:
  for q in sorted(p.rglob('*')):
   if q.is_file():zz.write(q,str(q.relative_to(b)))
 with zipfile.ZipFile(z) as zz:assert zz.testzip() is None
 assert z.stat().st_size<18*1024**2
idx_path=d/'SOURCE_PACKAGE_INDEX.json';idx=json.loads(idx_path.read_text());
for a in idx['archives']:
 a.update(rec(r/a['path']))
idx['status']='frozen_after_candidate_full_source_review_final_bytes_verification_pending';idx['candidate_package_review']=rec(gate);idx['character_final_statuses']=[rec(b/s/'noncombat_basics_v1/FINAL_STATUS.json') for s in ['luoer','qiner']];idx_path.write_text(json.dumps(idx,ensure_ascii=False,indent=2)+'\n')
order=['珞珥_芩珥_母图动作浅深对照.png','luoer_A1_support_lower_rope_coil_v2_transparent.png','luoer_A2_settle_neck_scarf_v1_transparent.png','qiner_A1_raise_existing_sprig_v1_transparent.png','qiner_A2_smooth_basket_lining_front_v1_transparent.png','珞珥_基础动作_完整源包.zip','芩珥_基础动作_完整源包.zip','第七批_规划全量来源.zip'];items=[]
for i,name in enumerate(order):
 q=d/name;v=rec(q);v['order']=i+1;v['filename']=name;v['kind']='board' if i==0 else ('selected_transparent' if i<5 else 'complete_source_zip');items.append(v)
manifest={'status':'frozen_artifacts_awaiting_final_archive_byte_confirmation','author':'draw_luoer_qiner_actions','selected_count':4,'initial_calls':4,'hard_error_revisions':1,'rejected_versions_retained':1,'missing_poses':[],'files':items,'archives_independently_openable':True,'archive_merge_required':False,'source_package_index':rec(idx_path),'uploaded':False}
(d/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
for x in items:print(json.dumps(x,ensure_ascii=False))
