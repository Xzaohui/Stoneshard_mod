import pathlib,json,hashlib,shutil,zipfile
r=pathlib.Path(__file__).resolve()
while r.name!='Stoneshard_mod':r=r.parent
root=r/'Assets/CharacterActions/20261013/new_story';d=root/'third_noncombat_tian_lein_delivery_v1';sel=json.loads((d/'selection.json').read_text());audit=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def filedata(p):return {'path':str(p.relative_to(r)),'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,v):
 assert not p.exists(),str(p)
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
visual='independent_third_new_character_actions_tian_lein_visual_gate_20261014.json';boardqa='independent_third_new_character_actions_tian_lein_board_gate_20261014.json'
assert sha(audit/visual)=='346300eec3cca81b5b5454e1d61551cc74807707395be44fd5578b936a5d23d6'
assert sha(audit/boardqa)=='456852b6312620c9b198f72cbd7bfbf57669c4611bf5423fc9b9395a968b1f07'
attachments=[];archives=[];ts='2026-10-14T04:47:00Z'
for c in sel:
 p=root/c['slug']/'noncombat_basics_v1';assert not (p/'FINAL_STATUS.json').exists()
 shutil.copyfile(audit/boardqa,p/'review'/boardqa)
 shutil.copyfile(d/'delivery/缇安_蕾因_母图动作浅深对照.png',p/'review/缇安_蕾因_母图动作浅深对照.png')
 shutil.copyfile(d/'board_layout.json',p/'review/board_layout.json')
 shutil.copyfile(d/'scripts/compose_board.py',p/'sources/compose_board.py')
 shutil.copyfile(d/'selection.json',p/'sources/board_selection.json')
 qa=json.loads((p/'review/QA_author_source_and_pixels.json').read_text());assert qa['sources_originals_unchanged'] and qa['source_snapshots_verified']
 for a in qa['assets']:assert a['full_return_image_matches_raw_bytes'] and a['parameters_prompt_matches_stored_prompt'] and a['A_gt8_pixels_unchanged']
 selected=[]
 for x in c['selected']:
  img=r/x['path'];entry={'key':x['key'],'title_zh':x['label'].split(' · ')[1],'transparent':filedata(img),'raw':filedata(p/'raw'/f"{x['key']}_raw.png"),'status':'pass_independent_visual_and_provenance'};selected.append(entry)
  deliver=d/'delivery'/f"{c['name']}_{x['key'].split('_')[1]}_{entry['title_zh']}.png";assert sha(deliver)==sha(img)
  attachments.append({'kind':'transparent_action_png','character':c['slug'],'key':x['key'],'title_zh':entry['title_zh'],**filedata(deliver)})
 final={'schema_version':1,'created_utc':ts,'author':'draw_tian_lein_actions','solewriter':True,'status':'frozen_after_independent_visual_and_board_review','character':c['slug'],'canonical_id':json.loads((p/'source_brief.json').read_text())['canonical_id'],'selected_pose_count':2,'initial_generations':2,'revision_generations':0 if c['slug']=='tian' else 1,'selected':selected,'excluded_versions':[] if c['slug']=='tian' else [{'key':'lein_A1_reseat_chalk_in_hat_loop_v1','reason':'左指未实际接粉笔；保留原稿与唯一修订溯源，不计合格动作。'}],'visual_gate':filedata(p/'review'/visual),'board_gate':filedata(p/'review'/boardqa),'postprocess':'原A<=8的近零alpha背景RGBA归零；原A>8实体像素逐通道不变。完整原raw保留。只用NEAREST等比版式，不画或伸缩身体。','source_originals_unchanged':True,'animation':False,'runtime_verified':False,'git_performed':False,'uploaded':False,'sent':False}
 write(p/'FINAL_STATUS.json',final)
 inventory=[]
 for f in sorted(p.rglob('*')):
  if f.is_file() and f != p/'manifest.json':inventory.append({'path':str(f.relative_to(p)),'bytes':f.stat().st_size,'sha256':sha(f)})
 manifest={'schema_version':1,'created_utc':ts,'status':'frozen','character':c['slug'],'selected_pose_count':2,'raw_generation_count':len(qa['assets']),'postprocess':final['postprocess'],'root_manifest_exclusion_only':'manifest.json（仅本文件自身；所有嵌套source manifest均包含）','files':inventory,'files_count':len(inventory),'final_status_sha256':sha(p/'FINAL_STATUS.json'),'selected':selected,'runtime_verified':False}
 write(p/'manifest.json',manifest)
 actual=[f for f in p.rglob('*') if f.is_file()];assert len(actual)==len(inventory)+1
 zip_path=d/'delivery'/f"{c['slug']}_noncombat_basics_complete_source_v1.zip";assert not zip_path.exists()
 with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  for f in sorted(actual):z.write(f,str(f.relative_to(r)))
 with zipfile.ZipFile(zip_path) as z:
  assert z.testzip() is None
  assert set(z.namelist())=={str(f.relative_to(r)) for f in actual}
  assert all(hashlib.sha256(z.read(str(f.relative_to(r)))).hexdigest()==sha(f) for f in actual)
 assert zip_path.stat().st_size<18*1024*1024
 archives.append({'kind':'complete_source_zip','character':c['slug'],**filedata(zip_path),'zip_crc_check':True,'all_members_match_frozen_tree_sha':True,'members':len(actual),'includes_final_status':True,'includes_manifest':True,'source_tree':str(p.relative_to(r)),'manifest_sha256':sha(p/'manifest.json'),'final_status_sha256':sha(p/'FINAL_STATUS.json'),'under_18_MiB':True})
attachments.append({'kind':'chinese_light_dark_mother_action_board',**filedata(d/'delivery/缇安_蕾因_母图动作浅深对照.png')});attachments+=archives
assert len(attachments)==7 and all(x['bytes']<18*1024*1024 for x in attachments)
write(d/'delivery_manifest.json',{'schema_version':1,'created_utc':ts,'status':'packaged_waiting_independent_zip_closure','selected_pose_count':4,'initial_generations':4,'revision_generations':1,'excluded_versions':['lein_A1_reseat_chalk_in_hat_loop_v1'],'attachments':attachments,'attachment_count':7,'all_attachments_under_18_MiB':True,'standalone_archives':'两份普通完整ZIP，各自覆盖对应人物完整源树；不是分卷。包含本轮全部raw、未选稿、逐字prompt、完整原返回、参数、源快照、QA、manifest、FINAL_STATUS。','uploaded':False,'sent':False,'git_performed':False,'scope':'4张独立静态姿态；不是连续动画、过渡帧或runtime验收。','visual_gate':filedata(audit/visual),'board_gate':filedata(audit/boardqa)})
print(json.dumps({'manifest':str((d/'delivery_manifest.json').relative_to(r)),'sha256':sha(d/'delivery_manifest.json'),'attachments':[(x['kind'],x['bytes'],x['sha256']) for x in attachments]},ensure_ascii=False,indent=2))
