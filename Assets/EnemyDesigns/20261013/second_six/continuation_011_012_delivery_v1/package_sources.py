from pathlib import Path
import json,hashlib,zipfile,datetime
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[4]
brief=json.loads((ROOT.parent/'action_continuation_brief_v1.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source=[]
for x in brief['items'][-2:]:
 d=REPO/x['planned_output_directory']
 for p in sorted(d.rglob('*')):
  if p.is_file():source.append(p)
for name in ['011_012_相邻关键姿态_浅深对照.png','build_delivery_board.py','package_sources.py']:
 source.append(ROOT/name)
readme='''011 / 012 动作续帧概念完整来源（两包合用）

请将 source_part1.zip 与 source_part2.zip 都解压到同一个空目录。
它们是两个标准ZIP文件，不是分卷压缩格式；资料按相同项目相对路径合并。
两包共同覆盖全部来源文件。两份 README 与 SOURCE_CONTENTS.json 相同，遇到这两个同名文件可任选保留一份。

本批正选：011喉胸前送释放v2；012手铃外摆端点v1。
011的v1是未通过动作核心的废稿，保留供审计，不能当正选。

全部原始PNG、废稿、逐字实际prompt、工具参数、完整原工具返回、输入/输出SHA、来源参考、QA、manifest、FINAL_STATUS均保留。
source目录是本次所用母图与旧正选的冻结副本，原图未修改。
浅深对照图只做真实RGBA合成和等比最近邻排版。

仅为动作关键阶段概念，不代表完整动画、帧时序、精确锚点、装备运行或游戏集成通过。
本地制作时没有Git提交/上传、运行部署或用户侧附件发送；发送记录由父任务单独维护。
'''
(ROOT/'两包解压说明.txt').write_text(readme,encoding='utf8')
# Balance by uncompressed bytes; every source file is included exactly once.
groups=[[],[]];sizes=[0,0]
for p in sorted(source,key=lambda p:(-p.stat().st_size,str(p))):
 i=0 if sizes[0]<=sizes[1] else 1;groups[i].append(p);sizes[i]+=p.stat().st_size
inventory={'schema_version':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'extraction':'Extract BOTH independent standard-deflate ZIPs into the same directory. Their union contains the complete source tree.','file_count':len(source),'files':[{'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size,'part':i+1} for i,g in enumerate(groups) for p in sorted(g)]}
(ROOT/'SOURCE_CONTENTS.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2)+'\n')
outputs=[]
for i,g in enumerate(groups):
 o=ROOT/f'011_012_complete_sources_part{i+1}.zip'
 with zipfile.ZipFile(o,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  z.write(ROOT/'两包解压说明.txt','README_两包合用.txt');z.write(ROOT/'SOURCE_CONTENTS.json','SOURCE_CONTENTS.json')
  for p in sorted(g):z.write(p,str(p.relative_to(REPO)))
 assert o.stat().st_size<18*1024*1024
 with zipfile.ZipFile(o) as z:
  assert z.testzip() is None
  for p in g:assert hashlib.sha256(z.read(str(p.relative_to(REPO)))).hexdigest()==sha(p)
 outputs.append(o)
# Verify manifest-scoped frozen files and source tree coverage, without modifying frozen asset directories.
checks=[]
for x in brief['items'][-2:]:
 d=REPO/x['planned_output_directory'];m=json.loads((d/'manifest.json').read_text());f=json.loads((d/'FINAL_STATUS.json').read_text());assert sha(d/'manifest.json')==f['manifest']['sha256'];assert sha(d/f['selected_image']['path'])==f['selected_image']['sha256']
 for e in m['files']:assert sha(d/e['path'])==e['sha256']
 checks.append({'concept_id':x['concept_id'],'frozen_files_verified':len(m['files']),'final_status_sha256':sha(d/'FINAL_STATUS.json'),'selected_sha256':f['selected_image']['sha256']})
files=[ROOT/'011_喉胸前送释放.png',ROOT/'012_手铃外摆端点.png',ROOT/'011_012_相邻关键姿态_浅深对照.png']+outputs
manifest={'status':'ready_for_parent_delivery','attachment_count':5,'files':[{'path':str(p.relative_to(REPO)),'sha256':sha(p),'bytes':p.stat().st_size,'mib':round(p.stat().st_size/1048576,3)} for p in files],'source_zips_standard_deflate':True,'source_union_complete':True,'source_file_count':len(source),'archive_entries_decoded_sha_verified':True,'all_attachments_under_18MiB':True,'frozen_checks':checks,'board_actually_viewed':True,'new_selected_keyposes':2,'imagegen_calls':3,'continuous_animation_verified':False,'frame_anchors_verified':False,'equipment_runtime_verified':False,'runtimeIntegrated':False,'runtimeVerified':False,'delivery_performed_by_worker':False}
(ROOT/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n');print(json.dumps(manifest,ensure_ascii=False,indent=2))
