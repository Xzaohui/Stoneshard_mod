from pathlib import Path
import json,hashlib,zipfile,datetime
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');D=Path(__file__).resolve().parent;B=json.loads((R/'Assets/EnemyDesigns/reference/20261013/action_pilot_second_six_brief_v2.json').read_text());SHA=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();write=lambda p,d:p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
attachments=[]
for c in B['characters'][:2]:
 for p in c['poses']:
  d=R/p['output_directory'];q=d/'QA_INDEPENDENT.json';assert q.exists(),q
  qa=json.loads(q.read_text());assert qa['result'].startswith('pass'),qa
  m=json.loads((d/'manifest.json').read_text());m['status']='selected_frozen';m['independent_qa_sha256']=SHA(q);m['files']['QA_INDEPENDENT.json']=SHA(q);m['actual_reference_images']=[c['anchor']['path']]
  if m['hard_error_revisions_used']:m['revision_reference_images']=[p['planned_raw_path'],c['anchor']['path']];m['revision_reason']='首稿右靴主体到画布右边，唯一修订补足主体留边；无脚本补画。'
  write(d/'manifest.json',m)
  st={'status':'selected_frozen','author':'draw_shield_crossbow_actions','selected_file':m['transparent'],'selected_sha256':SHA(d/m['transparent']),'independent_qa_sha256':SHA(q),'manifest_sha256':SHA(d/'manifest.json'),'first_drafts':1,'hard_error_revisions_used':m['hard_error_revisions_used'],'runtimeIntegrated':False,'runtimeVerified':False,'animation_frames_produced':0,'frozen':True,'root_visual_approval':'Root actually viewed joint light/dark board and approved concept delivery 2026-10-13 20:24 UTC'}
  write(d/'FINAL_STATUS.json',st);path=d/m['transparent'];attachments.append({'path':str(path.relative_to(R)),'sha256':SHA(path),'bytes':path.stat().st_size,'kind':'transparent_png'})
 root=R/c['poses'][0]['output_directory'];root=root.parent
 (root/'README.txt').write_text(c['working_name']+'：两张原创基础关键姿势，非连续动画或运行素材验收。\n包含准确调用提示词、母图快照、raw、透明清理图、浅深审核、alpha统计、独立审核及作者状态。\n所有静态原文件只读。处理仅alpha<=8及隐藏RGB清理；审核板nearest等比排版。\n')
 z=D/(c['concept_id'][-3:]+'_'+c['slug']+'_action_v1_complete.zip')
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,9) as out:
  for f in sorted(root.rglob('*')):
   if f.is_file():out.write(f,f.relative_to(root.parent))
 assert z.stat().st_size<18*1024*1024
 with zipfile.ZipFile(z) as test:assert test.testzip() is None
 attachments.append({'path':str(z.relative_to(R)),'sha256':SHA(z),'bytes':z.stat().st_size,'kind':'complete_zip'})
board=D/'007_008_action_light_dark.png';attachments.append({'path':str(board.relative_to(R)),'sha256':SHA(board),'bytes':board.stat().st_size,'kind':'joint_light_dark_board'})
write(D/'delivery.json',{'status':'frozen_after_root_visual_approval','attachment_count':7,'attachments':attachments,'runtimeIntegrated':False,'runtimeVerified':False})
write(D/'FINAL_DELIVERY_QA.json',{'status':'pass_technical_delivery_and_root_visual_approval','attachments':len(attachments),'zip_under_18MiB':True,'zip_integrity':True,'all_four_independent_pass':True,'board_actually_viewed_by_author':True,'board_alignment':'人物发顶至靴底近似等比，nearest；不按武器总框压小人物。','prompt_archive':'All actual tool prompt strings preserved; shield_recover prompt originally undefined due asynchronous store read, restored directly from completed generator cell original p2 variable before freeze.','generation_calls':5,'revisions':{'crossbow_aim':1,'other_poses':0},'scope':'4独立基础关键姿势，无连续动画/运行声明；不上传git；旧静态未写。'})
print(json.dumps(attachments,ensure_ascii=False,indent=2))
