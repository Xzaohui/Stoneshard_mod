from pathlib import Path
import json,hashlib,shutil,zipfile,datetime,base64
from PIL import Image
import numpy as np
R=Path.cwd();B=R/'Assets/EnemyDesigns/20261013/second_six';O=B/'continuation_009_010_delivery_v1';b=json.loads((B/'action_continuation_brief_v1.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def info(p,root):return {'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size}
def J(p,v):
 assert not p.exists(),p
 p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
attachments=[];checks=[]
for i in b['items']:
 n=i['concept_id'][-3:]
 if n not in ['009','010']:continue
 d=R/i['planned_output_directory'];qa=d/'independent_QA_v1.json'
 assert qa.exists(),'Independent QA not yet saved'
 q=json.loads(qa.read_text()); assert any('pass' in str(q.get(k,'')) for k in ['status','result','verdict','overall_status','overall_result']),(q.keys(),'Check reviewer result manually')
 assert not (d/'FINAL_STATUS.json').exists(),'Already frozen; do not repeat'
 # Read candidate immutable inventory; later metadata is additive.
 m=json.loads((d/'manifest.json').read_text())
 for f in m['files']:
  p=d/f['path'];assert p.stat().st_size==f['bytes'] and sha(p)==f['sha256'],p
 raw=d/f"{i['slug']}_{i['pose_id']}_raw_v1.png";selected=d/f"{i['slug']}_{i['pose_id']}_transparent.png"
 rt=json.loads((d/'tool_return_v1.json').read_text());assert base64.b64decode(rt['image_url'].split(',',1)[1])==raw.read_bytes()
 args=json.loads((d/'tool_args_v1.json').read_text());assert (d/'prompt_v1.txt').read_text()==args['prompt']==i['planned_tool_call']['arguments']['prompt']
 assert np.array_equal(np.asarray(Image.open(selected))[48:-48,48:-48],np.asarray(Image.open(raw)))
 for f in json.loads((d/'sources/source_manifest.json').read_text())['files']:
  assert sha(R/f['source_path'])==f['sha256'];assert sha(d/f['copied_path'])==f['sha256']
 readme=f'''# {n} {i['working_name']}：{i['label']}\n\n独立审查通过的单张关键阶段概念，选中首稿 v1。首稿1次，硬错修订0次。\n\n- 本目录包含完整实际提示词、全部工具参数和未删减原返回（含图像数据）、原始输出、候选透明PNG、浅深合成、相邻对照、来源快照与哈希、作者与独立QA。\n- 候选只在原始RGBA四周增加48px透明留边；内部RGBA逐像素相同。没有身体绘制、拉伸、阈值去光或调色。\n- 旧母图与旧动作仅用于参照和等比最近邻对照排版，源文件未改。009沿idle_style_v2；010沿原选guard/probe首稿，未选旧revision不当作当前输入。\n- 相邻图是分离的关键阶段概念，并非已验证连续三帧动画；没有挥落中间帧、碰撞、精确锚点、装备运行合成或游戏内验证。\n- 本轮没有Git提交、上传或部署。\n\n## 实际审核边界\n\n{'高举重斧与双手连贯承载清楚，后脚接重表现保守但双足基底可承载；独审明确不需为审美偏好修订。' if n=='009' else '屈肘回胸侧与斜上短剑清楚，胸肩后收幅度较小；盾、短双尾与握持连贯。'}\n\nmanifest.json 保留送独审时的候选快照；final_manifest.json 为封存前全文件清单，排除其自身避免自哈希循环。FINAL_STATUS.json 由作者写入，送达状态由外层交付记录管理。\n'''
 (d/'README_zh.md').write_text(readme)
 shutil.copy2(O/'finalize_and_package.py',d/'finalize_and_package_reference.py')
 final={'concept_id':i['concept_id'],'pose_id':i['pose_id'],'status':'selected_independent_keypose_concept','selected':True,'selected_version':'v1','selected_image':info(selected,R),'raw_image':info(raw,R),'independent_review':info(qa,R),'author_review':info(d/'author_QA.json',R),'candidate_manifest':info(d/'manifest.json',R),'first_drafts':1,'hard_error_revisions_used':0,'generation_calls':1,'postprocessing':'48px transparent padding only; original RGBA pixels unchanged','author_directory_frozen':True,'frozen':True,'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'delivered_by_this_worker':False,'continuous_animation_verified':False,'exact_anchor_verified':False,'equipment_runtime_verified':False,'runtimeIntegrated':False,'runtimeVerified':False,'git_committed':False,'uploaded_by_this_worker':False}
 J(d/'FINAL_STATUS.json',final)
 J(d/'final_manifest.json',{'status':'frozen_selected_v1','scope':'All files in this action directory excluding final_manifest.json itself; selected art and reviewed candidate are unchanged.','files':[info(p,d) for p in sorted(d.rglob('*')) if p.is_file()]})
 target=O/f"{n}_{i['working_name']}_{i['label']}.png";shutil.copy2(selected,target);attachments.append(info(target,R))
 zp=O/f"{n}_{i['slug']}_{i['pose_id']}_完整源文件.zip"
 with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(d.rglob('*')):
   if p.is_file():z.write(p,str(Path(f"{n}_{i['slug']}_{i['pose_id']}")/p.relative_to(d)))
 with zipfile.ZipFile(zp) as z:
  assert z.testzip() is None
  pref=f"{n}_{i['slug']}_{i['pose_id']}/"
  for f in json.loads((d/'final_manifest.json').read_text())['files']:
   data=z.read(pref+f['path']);assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
 assert zp.stat().st_size<18*1024*1024
 attachments.append(info(zp,R));checks.append({'concept_id':i['concept_id'],'all_candidate_hashes_unchanged':True,'all_old_sources_unchanged':True,'full_tool_return_decodes_to_raw':True,'exact_prompt_matches_actual_args':True,'rgba_padding_only':True,'zip_crc_and_manifest_hashes_pass':True,'package_bytes':zp.stat().st_size,'final_status':info(d/'FINAL_STATUS.json',R)})
board=O/'009_010_相邻关键姿态_浅深对照.png';attachments.append(info(board,R))
assert len(attachments)==5 and all(x['bytes']<18*1024*1024 for x in attachments)
J(O/'delivery_manifest.json',{'status':'ready_for_parent_delivery','selected_keypose_concepts':2,'attachment_count':5,'attachments':attachments,'checks':checks,'board_actual_viewed':True,'delivered':False,'uploads':False,'git_actions':False,'runtimeVerified':False,'continuous_animation_verified':False})
J(O/'package_validation.json',{'passed':True,'checks':checks,'files':attachments})
print(json.dumps({'attachments':attachments,'all_checks_passed':True},ensure_ascii=False,indent=2))
