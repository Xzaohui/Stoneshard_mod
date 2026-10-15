from pathlib import Path
import json,hashlib,zipfile,shutil,datetime
r=Path.cwd();base=r/'Assets/CharacterActions/20261013/new_story';delivery=base/'fifth_endai_wadun_delivery_v1';delivery.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();records=[];trees={}
zipnames={'endai':['恩岱_基础动作完整源.zip'],'wadun':['瓦顿_基础动作完整源_1of2.zip','瓦顿_基础动作完整源_2of2.zip']}
for slug in ['endai','wadun']:
 d=base/slug/'noncombat_basics_v1';files=[p for p in sorted(d.rglob('*')) if p.is_file()];members=[]
 for p in files:
  rel=str(p.relative_to(d));part=0 if slug=='endai' or rel.split('/')[0] in ('raw','prompts') else 1
  members.append({'source_tree_path':str(p.relative_to(r)),'archive_member':f'{slug}/noncombat_basics_v1/{rel}','bytes':p.stat().st_size,'sha256':sha(p),'package':zipnames[slug][part]})
 trees[slug]={'source_tree':str(d.relative_to(r)),'member_count':len(members),'total_source_bytes':sum(x['bytes'] for x in members),'members':members}
 package_manifest={'schema_version':1,'character':slug,'source_tree':trees[slug]['source_tree'],'complete_set':zipnames[slug],'extract_all_to_same_directory':True,'all_members':members,'metadata_entry':'PACKAGE_SET_MANIFEST.json is byte-identical in every ZIP of this character set and is additional to the complete source tree.','failed_raw_and_full_imagepayload_preserved':True}
 for name in zipnames[slug]:
  z=delivery/name
  with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as f:
   f.writestr('PACKAGE_SET_MANIFEST.json',json.dumps(package_manifest,ensure_ascii=False,indent=2))
   for m in members:
    if m['package']==name:f.write(r/m['source_tree_path'],m['archive_member'])
  assert z.stat().st_size<18*1048576,(str(z),z.stat().st_size)
  with zipfile.ZipFile(z) as f:assert f.testzip() is None
  records.append({'filename':name,'bytes':z.stat().st_size,'sha256':sha(z),'type':'complete_source_zip' if slug=='endai' else 'complete_source_zip_part','source_character':slug,'character':slug,'complete_set':zipnames[slug],'extract_all_to_same_directory':True,'part_scope':'all source files' if slug=='endai' else 'raw and prompts' if name==zipnames[slug][0] else 'all remaining source files; union of both ZIPs is complete'})
images=[('endai','endai_A1_settle_left_bracer_v1','恩岱_动作1_按稳护腕.png'),('endai','endai_A2_press_right_cloak_patch_v1','恩岱_动作2_按平补片.png'),('wadun','wadun_A1_low_hold_original_spatula_v2','瓦顿_动作1_低蹲持铲.png'),('wadun','wadun_A2_brace_knees_resettle_squat_v1','瓦顿_动作2_扶膝重蹲.png')]
imgrecords=[]
for slug,stem,name in images:
 p=base/slug/'noncombat_basics_v1/exports'/f'{stem}_transparent.png';q=delivery/name;shutil.copy2(p,q);assert p.read_bytes()==q.read_bytes();imgrecords.append({'filename':name,'bytes':q.stat().st_size,'sha256':sha(q),'source':str(p.relative_to(r)),'type':'selected_transparent_png'})
p=base/'endai/noncombat_basics_v1/review/恩岱_瓦顿_母图动作浅深对照.png';q=delivery/p.name;shutil.copy2(p,q);imgrecords.append({'filename':q.name,'bytes':q.stat().st_size,'sha256':sha(q),'source':str(p.relative_to(r)),'type':'joint_chinese_light_dark_board'})
manifest={'status':'candidate_pending_final_independent_package_review_not_frozen','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'delivery_directory':str(delivery.relative_to(r)),'attachment_count':8,'ordered_files':imgrecords+records,'complete_source_trees':trees,'all_packages_under_18_MiB':True,'generation_calls':5,'selected_actions':4,'failed_first_drafts_retained':1,'upload_or_send_performed':False,'runtime_verified':False}
(delivery/'DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));print(json.dumps(manifest['ordered_files'],ensure_ascii=False,indent=2))
