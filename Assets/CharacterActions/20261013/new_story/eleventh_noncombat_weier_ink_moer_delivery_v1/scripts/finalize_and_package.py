from pathlib import Path
import json,hashlib,shutil,datetime,zipfile,zlib
R=Path.cwd();P=R/'Assets/CharacterActions/20261013/new_story';D=P/'eleventh_noncombat_weier_ink_moer_delivery_v1';A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';b=json.loads((D/'planning_sources/eleventh_new_character_actions_brief.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def ref(p):return {'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)}
bg=A/'independent_eleventh_new_character_actions_weier_ink_moer_board_gate_20261014.json';assert sha(bg)=='11900ca634e096c37b7f1e09d74a5a6d964d79efe111027047f9303ada982845';shutil.copy2(bg,D/'independent_board_gate.json')
chars=[]
for c in b['characters']:
 if c['slug'] not in ['weier_ink','moer']:continue
 d=R/c['proposed_output_directory']; chars.append(d)
 for p in c['plans']:
  q=A/'eleventh_actions_independent_details'/f'{p["key"]}_v1_raw_selected_true_alpha.png';shutil.copy2(q,d/'review'/('independent_'+q.name))
 m={'schema_version':1,'character':c['slug'],'files':[{'path':str(p.relative_to(d)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(d.rglob('*')) if p.is_file() and p.name not in ['manifest.json','FINAL_STATUS.json']]}
 write(d/'manifest.json',m)
 write(d/'FINAL_STATUS.json',{'schema_version':1,'status':'final_clean_and_presentation_pass','author':'draw_weier_ink_moer_actions','prepared_utc':now,'character':c['slug'],'canonical_id':c['canonical_id'],'selected_count':2,'raw_output_count':2,'generation_calls':2,'revisions_used':0,'failed_attempts':0,'blocked_count':0,'all_raw_and_complete_tool_payloads_preserved':True,'manifest_sha256':sha(d/'manifest.json'),'independent_qa_sha256':sha(d/'QA-independent.json'),'presentation_gate':ref(bg),'parent_board_review':ref(D/'parent_board_review.json'),'archive_freeze_record':'eleventh_noncombat_weier_ink_moer_delivery_v1/FREEZE_STATUS.json is written only after the final independent package audit.','runtime_verified':False,'uploaded_or_sent_to_user':False,'blocking_issues':[]})
write(D/'AUTHOR_HANDOFF.json',{'author':'draw_weier_ink_moer_actions','characters':['weier_ink','moer'],'qualified_poses':4,'calls':4,'first_drafts':4,'revisions':0,'failures':0,'safety_blocks':0,'visual_gate':ref(D/'independent_visual_gate.json'),'board_gate':ref(D/'independent_board_gate.json'),'parent_board_review':ref(D/'parent_board_review.json'),'source_and_script_scope':'Only own character action trees and own delivery folder were created; no frozen sources, old indexes, Git, runtime, or user uploads changed.','character_final_status':[ref(p/'FINAL_STATUS.json') for p in chars]})
# Freeze the package member set before adding external package/freeze records.
files=[]
for d in chars:
 files += [p for p in sorted(d.rglob('*')) if p.is_file()]
for p in sorted(D.rglob('*')):
 if not p.is_file():continue
 if p.suffix=='.zip' or p.name in ['package_manifest.json','candidate_package_manifest.json','ATTACHMENT_MANIFEST.json','FREEZE_STATUS.json']:continue
 files.append(p)
assert len(files)==len(set(files));files=sorted(files)
# Conservative cap on sum of each deflated member, with ample central-directory/manifest allowance.
groups=[];current=[];n=0
for p in files:
 cost=len(zlib.compress(p.read_bytes(),9))+len(str(p.relative_to(R)).encode())*2+300
 if current and n+cost>16.5*1024*1024:groups.append(current);current=[];n=0
 current.append(p);n+=cost
if current:groups.append(current)
packages=[]
for i,ps in enumerate(groups,1):
 name=f'weier_ink_moer_complete_sources_part{i:02d}_of_{len(groups):02d}.zip';out=D/name;members=[ref(p) for p in ps]
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in ps:z.write(p,str(p.relative_to(R)))
  z.writestr('PACKAGE_CONTENTS.json',json.dumps({'part':i,'parts':len(groups),'members':members},ensure_ascii=False,indent=2)+'\n')
 assert out.stat().st_size<18*1024*1024
 with zipfile.ZipFile(out) as z:
  assert z.testzip() is None
  for p in ps:assert z.read(str(p.relative_to(R)))==p.read_bytes()
 packages.append({**ref(out),'member_count':len(members)+1,'members':members})
manifest={'schema_version':1,'group':'weier_ink_moer','status':'sealed_for_final_independent_package_review','created_utc':now,'all_files_count':len(files),'packages':packages,'selected_count':4,'all_payloads_preserved':True,'archive_paths_are_repo_relative':True,'package_contents_internal_manifest_excluded_from_all_files_count':True}
write(D/'package_manifest.json',manifest)
selected=json.loads((D/'selected_files.json').read_text());attachments=[ref(D/f'weier_ink_moer_mother_actions_{x}.png') for x in ['light','dark']]+selected+[ref(D/Path(x['path']).name) for x in packages]
write(D/'ATTACHMENT_MANIFEST.json',{'group':'weier_ink_moer','attachment_count':len(attachments),'items':[{'order':i+1,**x} for i,x in enumerate(attachments)],'uploaded':False,'sent':False})
print(json.dumps({'files':len(files),'packages':[{k:v for k,v in x.items() if k!='members'} for x in packages],'package_manifest':ref(D/'package_manifest.json'),'attachments':len(attachments)},ensure_ascii=False,indent=2))
