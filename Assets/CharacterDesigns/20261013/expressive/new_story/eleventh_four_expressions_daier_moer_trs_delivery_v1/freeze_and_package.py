from pathlib import Path
import json,hashlib,datetime,zipfile,shutil
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Assets/CharacterDesigns/20261013/expressive/new_story').is_dir())
BASE=ROOT/'Assets/CharacterDesigns/20261013/expressive/new_story'
DEL=BASE/'eleventh_four_expressions_daier_moer_trs_delivery_v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
attachments=[];char_states=[]
for slug in ['daier','moer_trs']:
 d=BASE/slug/'expressions_v1'; c=json.loads((d/'brief-character.json').read_text());g=json.loads((d/'generation-log.json').read_text())
 for n in ['QA-independent-raw-visual.json','QA-independent.json']:
  assert (d/n).exists(),n
  review=json.loads((d/n).read_text());assert review['status']=='passed' and not review['hard_errors']
 assert not (d/'manifest.json').exists(), 'Manifest already frozen; do not overwrite.'
 files=[{'path':str(p.relative_to(d)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(d.rglob('*')) if p.is_file() and p not in (d/'manifest.json',d/'FINAL_STATUS.json')]
 m={'schema_version':1,'character':slug,'canonical_id':c['canonical_id'],'name_zh':c['name'],'status':'frozen_after_independent_visual_pass','frozen_utc':now(),'scope':'two_reversible_full_body_expression_concepts','generation_calls':2,'hard_error_revisions':0,'files':files,'excluded_from_file_list':['manifest.json self','FINAL_STATUS.json binds this manifest after freezing'],'selected':[{'path':x['selected'],'sha256':x['selected_sha256']} for x in g['calls']],'runtime_verified':False,'continuous_animation_verified':False}
 write(d/'manifest.json',m)
 status={'schema_version':1,'sole_writer':'draw_daier_moertrs_expressions','character':slug,'canonical_id':c['canonical_id'],'name_zh':c['name'],'status':'PASS_FROZEN_CONCEPT_ONLY','frozen_utc':now(),'manifest':{'path':'manifest.json','sha256':sha(d/'manifest.json')},'independent_reviews':[{'path':n,'sha256':sha(d/n)} for n in ['QA-independent-raw-visual.json','QA-independent.json']],'selected':m['selected'],'revisions_used':0,'runtime_verified':False,'continuous_animation_verified':False,'native_pixel_grid_verified':False,'equipment_compatibility_verified':False,'notes_zh':'独立可逆表情概念；不确认剧情结果、人物许可、游戏实现或连续动画。'}
 write(d/'FINAL_STATUS.json',status)
 for f in files: assert sha(d/f['path'])==f['sha256']
 char_states.append({'character':slug,'manifest_sha256':sha(d/'manifest.json'),'final_status_sha256':sha(d/'FINAL_STATUS.json'),'file_count':len(files)+2})
 for e in c['expressions']:
  src=d/'selected'/f'{e["key"]}_transparent.png'; out=DEL/f'{c["name"]}_{e["label_zh"]}_透明.png';shutil.copyfile(src,out)
  attachments.append({'path':str(out.relative_to(ROOT)),'sha256':sha(out),'bytes':out.stat().st_size,'mime_type':'image/png'})
board=DEL/'岱珥谟珥_四表情_中文浅深合板.png';attachments.append({'path':str(board.relative_to(ROOT)),'sha256':sha(board),'bytes':board.stat().st_size,'mime_type':'image/png'})
write(DEL/'frozen-character-status.json',char_states)
common=[DEL/'README.md',DEL/'generation-times.json',DEL/'prepare_assets.py',DEL/'freeze_and_package.py',DEL/'frozen-character-status.json',board]
for slug,name in [('daier','岱珥'),('moer_trs','谟珥')]:
 d=BASE/slug/'expressions_v1';zip_path=DEL/f'第十一批_{name}_两表情完整源包.zip';assert not zip_path.exists()
 review=json.loads((d/'QA-independent-raw-visual.json').read_text())
 extras=[ROOT/x['raw_composite']['path'] for x in review['source_chain']['records']]
 members=sorted(set([p for p in d.rglob('*') if p.is_file()]+common+extras))
 with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in members:z.write(p,str(p.relative_to(ROOT)))
 with zipfile.ZipFile(zip_path) as z:
  assert z.testzip() is None
  assert set(z.namelist())=={str(p.relative_to(ROOT)) for p in members}
  for p in members: assert z.read(str(p.relative_to(ROOT)))==p.read_bytes()
 assert zip_path.stat().st_size<18*2**20
 attachments.append({'path':str(zip_path.relative_to(ROOT)),'sha256':sha(zip_path),'bytes':zip_path.stat().st_size,'mime_type':'application/zip','independent_complete_archive':True,'members':len(members),'every_member_byte_verified':True,'contains_full_character_expression_tree':slug})
assert len(attachments)==7
write(DEL/'delivery-manifest.json',{'status':'ready_for_parent_delivery','created_utc':now(),'attachments':attachments,'characters':char_states,'archive_semantics':'两个独立ZIP，各含相应人物完整expressions_v1树及公共资料；非分卷。','not_uploaded':True,'not_committed':True,'runtime_verified':False,'continuous_animation_verified':False})
print(json.dumps({'attachments':attachments,'characters':char_states},ensure_ascii=False,indent=2))
