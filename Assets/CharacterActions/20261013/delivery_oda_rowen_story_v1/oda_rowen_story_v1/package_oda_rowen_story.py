from pathlib import Path
import json,hashlib,shutil,zipfile,zlib
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');BASE=R/'Assets/CharacterActions/20261013';D=BASE/'delivery_oda_rowen_story_v1';P=D/'oda_rowen_story_v1';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B=R/'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_supplements_03.json';brief=json.loads(B.read_text())
for k,cid in [('oda','NPC09'),('rowen','NPC11')]:
 s=BASE/k/'story_gesture_v1';qpath=s/'QA-independent.json';q=json.loads(qpath.read_text());assert q['status'].startswith('pass'),q['status'];m=s/'manifest.json';assert H(m)==q['manifest_at_review_sha256'];status={'status':'independent_pass_concept_with_notes','canonical_id':cid,'independent_qa_sha256':H(qpath),'reviewed_manifest_sha256':H(m),'new_poses':2 if k=='oda' else 1,'new_characters':0,'runtime_integrated':False,'limitations':q.get('limitations',[]),'animation_sequence':[0,1,2,0] if k=='oda' else [0,1,0],'original_anchor_reference_only':False};(s/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2));shutil.copytree(s,P/k/'story_gesture_v1',dirs_exist_ok=True)
 c=next(c for c in brief['characters'] if c['canonical_id']==cid)
 for path in [c['current_anchor']['path'],str(B.relative_to(R))]+[x['path'] for x in c['sources']]+[x['path'] for x in c['scripts']]:
  src=R/path;dst=P/'source_evidence'/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);assert H(src)==H(dst)
 for name in [f'{k}_story_gesture_review_zh_light.png',f'{k}_story_gesture_preview_once.gif']:shutil.copyfile(s/name,D/name)
(P/'README_交付说明.md').write_text('# 欧达与罗温：主线关键姿态\n\n2人共3张新姿态、0新人。内置imagegen生成；保留raw、提示词、处理脚本、原字节锚、完整brief和人物台本来源、SHA、manifest、作者与独立QA。\n\n欧达2新姿：垂眼检查原腰绳→停下看向请求者。原锚→新1→新2→原锚，共4阶段。绳圈保持收纳闭合，不解结，不生成船桩或船；不据此判断开船或N8到场。\n\n罗温仅1新姿：低位收臂戒备重新估量。原锚→新姿→原锚，共3阶段，复用不计新增。始终空手，肩包闭合；不新增地图、钱、地址纸，不表明交割完成。\n\n单次GIF无循环扩展；稀疏关键姿态，不是完整动画或运行资源。生成姿态存在局部衣褶和轮廓微差，不等同刚性动画连续性。FINAL_STATUS记录审后通过，manifest保留已审原样。\n')
shutil.copyfile(__file__,P/Path(__file__).name)
members={str(f.relative_to(P)):H(f) for f in sorted(P.rglob('*')) if f.is_file() and f.name!='PACKAGE_MEMBER_SHA256.json'};(P/'PACKAGE_MEMBER_SHA256.json').write_text(json.dumps(members,ensure_ascii=False,indent=2));z=D/'oda_rowen_story_v1_reviewed.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in sorted(P.rglob('*')):
  if f.is_file():a.write(f,str(f.relative_to(D)))
checked=[]
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None
 for m in a.infolist():
  data=a.read(m.filename);assert hashlib.sha256(data).hexdigest()==H(D/m.filename);assert zlib.crc32(data)&0xffffffff==m.CRC;checked.append({'path':m.filename,'bytes':len(data),'sha256':H(D/m.filename),'crc32':f'{m.CRC:08x}'})
assert z.stat().st_size<18*1024*1024
files=[D/f'{k}_story_gesture_review_zh_light.png' for k in ['oda','rowen']]+[D/f'{k}_story_gesture_preview_once.gif' for k in ['oda','rowen']]+[z];report={'status':'frozen_verified_not_uploaded','zip_bytes':z.stat().st_size,'crc_test':'pass','member_hash_test':'all_pass','members':checked,'deliverables':[{'path':str(f),'bytes':f.stat().st_size,'sha256':H(f)} for f in files]};(D/'DELIVERY_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='members'},ensure_ascii=False,indent=2))
