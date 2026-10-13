from pathlib import Path
import json, hashlib, shutil, zipfile, zlib
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod')
BASE=R/'Assets/CharacterActions/20261013'
D=BASE/'delivery_sena_kaem_story_v1'
P=D/'sena_kaem_story_v1'
H=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
brief=json.loads((R/'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_supplements.json').read_text())
files={}
for k,cid in [('sena','NPC-SENA'),('kaem','MAE-NPC-KAEM')]:
 source=BASE/k/'story_gesture_v1'
 assert (source/'QA-independent.json').exists(),f'{k} independent QA pending'
 assert (source/'FINAL_STATUS.json').exists(),f'{k} final status pending'
 target=P/k/'story_gesture_v1';shutil.copytree(source,target,dirs_exist_ok=True)
 c=next(c for c in brief['characters'] if c['canonical_id']==cid)
 paths=[c['current_anchor']['path'],'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_supplements.json']+[s['path'] for s in c['source_cards']]+[s['path'] for s in c['related_main_scripts']]
 for name in paths:
  src=R/name;dst=P/'source_evidence'/name;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);assert H(src)==H(dst)
 for name in [f'{k}_story_gesture_review_zh_light.png',f'{k}_story_gesture_preview_once.gif']:shutil.copyfile(source/name,D/name)
(P/'README_交付说明.md').write_text('# 塞娜与凯姆：主线剧情关键姿态\n\n每人两张新全身姿态，首末复用已选锚，共四阶段；0 新人物。每人目录含深浅双底板、透明逐帧、单次GIF、完整raw和prompt、处理脚本及作者/独立审查。FINAL_STATUS记录审后状态，manifest保留作者阶段原样。source_evidence保留原字节锚、完整brief与人物卡/台本来源。\n\n塞娜：限定查阅→让出解释位置。闭册闭袋，不替莉德授权或开放整库。\n凯姆：小幅辩解→放低空手等人说完。闭筒不交接，沉默不等于认罪。\n\n概念设定与关键姿态通过不等于连续动画、运行资源、任务状态或游戏验收。\n')
shutil.copyfile(Path(__file__),P/'package_sena_kaem_story.py')
for f in sorted(P.rglob('*')):
 if f.is_file() and f.name!='PACKAGE_MEMBER_SHA256.json':files[str(f.relative_to(P))]=H(f)
(P/'PACKAGE_MEMBER_SHA256.json').write_text(json.dumps(files,ensure_ascii=False,indent=2))
z=D/'sena_kaem_story_v1_reviewed.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as out:
 for f in sorted(P.rglob('*')):
  if f.is_file():out.write(f,str(f.relative_to(D)))
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None
 checked=[]
 for member in a.infolist():
  data=a.read(member.filename);local=D/member.filename
  assert hashlib.sha256(data).hexdigest()==H(local)
  assert zlib.crc32(data)&0xffffffff==member.CRC
  checked.append({'path':member.filename,'bytes':len(data),'sha256':H(local),'crc32':f'{member.CRC:08x}'})
assert z.stat().st_size<18*1024*1024
deliver=[D/f'{k}_story_gesture_review_zh_light.png' for k in ['sena','kaem']]+[D/f'{k}_story_gesture_preview_once.gif' for k in ['sena','kaem']]+[z]
report={'status':'frozen_delivery_candidates_not_uploaded','zip_bytes':z.stat().st_size,'zip_crc_test':'pass','member_sha256_test':'all pass','zip_members':len(checked),'members':checked,'deliverables':[{'path':str(f),'bytes':f.stat().st_size,'sha256':H(f)} for f in deliver]}
(D/'DELIVERY_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='members'},ensure_ascii=False,indent=2))
