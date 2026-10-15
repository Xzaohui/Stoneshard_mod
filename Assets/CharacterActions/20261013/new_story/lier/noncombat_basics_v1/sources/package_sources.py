from pathlib import Path
import json, hashlib, zipfile, shutil, datetime, zlib

r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
b=r/'Assets/CharacterActions/20261013/new_story'
d=b/'seventh_lier_huier_delivery_v1';d.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files=[];trees={}
for slug,name in [('lier','栎珥'),('huier','洄珥')]:
 root=b/slug/'noncombat_basics_v1'
 assert (root/'FINAL_STATUS.json').exists()
 sourcefiles=[p for p in sorted(root.rglob('*')) if p.is_file()]
 # Ordinary ZIP files; a file is never byte-split and every source file is retained.
 groups=[[]];size=0
 for p in sourcefiles:
  estimated=len(zlib.compress(p.read_bytes(),9))+len(str(p).encode())+200
  if size+estimated>16*1048576 and groups[-1]:groups.append([]);size=0
  groups[-1].append(p);size+=estimated
 znames=[f'{name}_基础动作完整源.zip'] if len(groups)==1 else [f'{name}_基础动作完整源_{i+1}of{len(groups)}.zip' for i in range(len(groups))]
 members=[]
 for i,group in enumerate(groups):
  for p in group:members.append({'source_tree_path':str(p.relative_to(r)),'archive_member':str(p.relative_to(b)),'bytes':p.stat().st_size,'sha256':sha(p),'package':znames[i]})
 trees[slug]={'source_tree':str(root.relative_to(r)),'member_count':len(members),'source_bytes':sum(x['bytes'] for x in members),'members':members,'complete_set':znames}
 setmanifest={'character':slug,'complete_set':znames,'extract_all_to_same_directory':True,'all_source_files_retained':True,'failed_attempts_and_full_image_payload_retained':True,'source_tree':trees[slug]['source_tree'],'members':members,'additional_entry':'PACKAGE_SET_MANIFEST.json'}
 for i,group in enumerate(groups):
  target=d/znames[i]
  with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   z.writestr('PACKAGE_SET_MANIFEST.json',json.dumps(setmanifest,ensure_ascii=False,indent=2))
   for p in group:z.write(p,str(p.relative_to(b)))
  assert target.stat().st_size<18*1048576
  with zipfile.ZipFile(target) as z:
   assert z.testzip() is None
   for m in members:
    if m['package']==znames[i]:assert hashlib.sha256(z.read(m['archive_member'])).hexdigest()==m['sha256']
  files.append({'filename':target.name,'type':'complete_source_zip' if len(groups)==1 else 'complete_source_zip_part','character':slug,'bytes':target.stat().st_size,'sha256':sha(target),'complete_set':znames,'extract_all_to_same_directory':True})
images=[('lier','lier_A2_low_right_foot_return_step_v1','栎珥_动作2_低抬右脚收步.png'),('huier','huier_A1_raise_right_hand_brow_shade_v1','洄珥_动作1_抬臂遮额望天.png'),('huier','huier_A2_two_hand_settle_carry_strap_v1','洄珥_动作2_双手稳背带.png')]
imgfiles=[]
for slug,stem,name in images:
 p=b/slug/'noncombat_basics_v1/exports'/f'{stem}_transparent.png';q=d/name;shutil.copy2(p,q)
 imgfiles.append({'filename':name,'source':str(p.relative_to(r)),'bytes':q.stat().st_size,'sha256':sha(q),'type':'selected_transparent_png'})
p=b/'lier/noncombat_basics_v1/review/栎珥_洄珥_母图动作浅深对照.png';q=d/p.name;shutil.copy2(p,q)
imgfiles.append({'filename':q.name,'source':str(p.relative_to(r)),'bytes':q.stat().st_size,'sha256':sha(q),'type':'joint_chinese_light_dark_board'})
manifest={'status':'candidate_pending_independent_package_gate','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'author_sole_writer':'draw_lier_huier_actions','delivery_directory':str(d.relative_to(r)),'selected_actions':3,'missing_actions':['lier_A1_gather_two_rope_tails'],'generated_calls':5,'hard_error_revision_calls':1,'new_characters':0,'complete_source_trees':trees,'ordered_files':imgfiles+files,'all_attachments_under_18_MiB':True,'upload_or_user_send_performed':False,'git_performed':False,'runtime_verified':False}
(d/'DELIVERY_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps(manifest['ordered_files'],ensure_ascii=False,indent=2))
