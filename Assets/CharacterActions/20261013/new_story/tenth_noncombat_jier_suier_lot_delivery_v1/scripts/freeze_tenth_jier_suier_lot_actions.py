from pathlib import Path
import json,hashlib,base64,datetime,shutil,sys
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');ROOT=R/'Assets/CharacterActions/20261013/new_story';D=ROOT/'tenth_noncombat_jier_suier_lot_delivery_v1';report=Path(sys.argv[1]);qa=json.loads(report.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat()
assert 'PASS' in str(qa.get('verdict',qa.get('status',''))).upper()
for slug in ['jier','suier_lot']:
 b=ROOT/slug/'noncombat_basics_v1';assert not (b/'FINAL_STATUS.json').exists();mp=b/'manifest.json';m=json.loads(mp.read_text());reviewed=sha(mp)
 for e in m['files']:assert sha(b/e['path'])==e['sha256'],e['path']
 for e in json.loads((b/'sources/source_index.json').read_text())['entries']:assert sha(R/e['source_path'])==e['sha256']==sha(b/e['path'])
 calls=json.loads((b/'generation-log.json').read_text())['calls']
 for c in calls:
  args=json.loads((b/c['actual_tool_arguments_path']).read_text());assert args['prompt']==(b/c['prompt_path']).read_text()
  ret=json.loads((b/c['tool_return_path']).read_text());assert hashlib.sha256(base64.b64decode(ret['image_url'].split(',',1)[1])).hexdigest()==c['raw_sha256']==sha(b/c['raw_path'])
  assert sha(b/c['selected_path'])==c['selected_sha256']
 for x in m['active_selected']:assert sha(b/x['selected'])==x['selected_sha256']
 shutil.copy2(mp,b/'review/manifest_at_tree_review.json');shutil.copy2(report,b/'review/independent'/report.name);shutil.copy2(__file__,b/'scripts'/Path(__file__).name);shutil.copy2('/workspace/scratch/5ed8df2c5d81/package_tenth_jier_suier_lot_actions.py',b/'scripts/package_tenth_jier_suier_lot_actions.py')
 v={'frozen_utc':now,'pre_freeze_manifest_sha256':reviewed,'all_pre_freeze_manifest_members_verified':len(m['files']),'all_sources_unchanged':True,'all_payloads_decode_to_raw':True,'all_saved_actual_prompts_verified':True,'active_selected_count':2,'tree_review_report':{'path':str(report.relative_to(R)),'sha256':sha(report)},'all_attempts_retained':True,'rejected_initial_count':int(slug=='suier_lot'),'runtime_verified':False};(b/'freeze_validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
 m['status']='frozen_pass';m['frozen_utc']=now;m['reviewed_manifest_sha256']=reviewed;m['tree_review_report_sha256']=sha(report);m['files']=[{'path':str(p.relative_to(b)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(b.rglob('*')) if p.is_file() and p not in [b/'manifest.json',b/'FINAL_STATUS.json']];mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')
 f={'schema_version':1,'status':'final_clean_and_presentation_pass','frozen_utc':now,'character':slug,'qualified_selected_count':2,'active_selected':m['active_selected'],'manifest_sha256':sha(mp),'raw_attempt_count':len(calls),'initial_count':2,'revision_count':int(slug=='suier_lot'),'rejected_attempt_count':int(slug=='suier_lot'),'all_attempts_and_full_payload_retained':True,'author_sole_writer_freeze':True,'freeze_policy':'Character source tree is immutable after this FINAL_STATUS file. Delivery copies and archives remain separate.','not_uploaded':True,'not_deployed':True,'runtime_verified':False,'user_approval_claimed':False,'files':{str(p.relative_to(b)):sha(p) for p in sorted(b.rglob('*')) if p.is_file() and p!=b/'FINAL_STATUS.json'}}
 (b/'FINAL_STATUS.json').write_text(json.dumps(f,ensure_ascii=False,indent=2)+'\n')
 for p,h in f['files'].items():assert sha(b/p)==h
 print(slug,sha(mp),sha(b/'FINAL_STATUS.json'),len(f['files']))
(D/'scripts').mkdir(exist_ok=True);shutil.copy2(__file__,D/'scripts'/Path(__file__).name);shutil.copy2('/workspace/scratch/5ed8df2c5d81/package_tenth_jier_suier_lot_actions.py',D/'scripts/package_tenth_jier_suier_lot_actions.py')
