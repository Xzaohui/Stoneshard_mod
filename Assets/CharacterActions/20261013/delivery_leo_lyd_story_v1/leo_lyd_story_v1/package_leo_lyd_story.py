from pathlib import Path
import json,hashlib,shutil,zipfile,zlib
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');BASE=R/'Assets/CharacterActions/20261013';D=BASE/'delivery_leo_lyd_story_v1';P=D/'leo_lyd_story_v1';H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B=R/'Assets/CharacterDesigns/20261013/expressive/briefs/next_main_cast_supplements_02.json';brief=json.loads(B.read_text())
for k,cid in [('leo','NPC-REY'),('lyd','NPC-LYD')]:
 s=BASE/k/'story_gesture_v1';qpath=s/'QA-independent.json';q=json.loads(qpath.read_text());assert q['status'].startswith('pass'),q['status'];m=s/'manifest.json';assert H(m)==q['manifest_at_review_sha256'];status={'status':'independent_pass_concept_with_notes','canonical_id':cid,'independent_qa_sha256':H(qpath),'reviewed_manifest_sha256':H(m),'new_poses':2,'new_characters':0,'runtime_integrated':False,'limitations':q.get('limitations',[]),'animation_sequence':[0,1,2,0] if k=='leo' else [1,2,1],'original_anchor_reference_only':k=='lyd'};(s/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2));shutil.copytree(s,P/k/'story_gesture_v1',dirs_exist_ok=True)
 c=next(c for c in brief['characters'] if c['canonical_id']==cid)
 for path in [c['current_anchor']['path'],str(B.relative_to(R))]+[x['path'] for x in c['source_cards']]+[x['path'] for x in c['related_main_scripts']]:
  src=R/path;dst=P/'source_evidence'/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst);assert H(src)==H(dst)
 for name in [f'{k}_story_gesture_review_zh_light.png',f'{k}_story_gesture_preview_once.gif']:shutil.copyfile(s/name,D/name)
(P/'README_交付说明.md').write_text('# 雷奥与莉德：主线关键姿态\n\n各2张新全身姿态，0新人。内置imagegen生成；保留原始图、提示词、处理脚本、原字节锚、完整brief及人物台本来源、SHA、manifest、作者与独立QA。\n\n雷奥：低头查闭匣→放低闭匣侧头听；原锚首末复用，四阶段。独审通过稀疏概念，但新匣较原锚扁宽，厚度变化不能全归于透视；没有锁定刚性道具动画几何。\n\n莉德：低头核本人纸段→收纸近身抬眼要求说完。原锚无纸，只在参考栏；GIF仅新姿1→2→1，三阶段两新姿。未制作取纸动作。外侧纸空白，不公开身份、不转手。\n\n单次GIF无循环扩展，非连续插帧或游戏运行资源。动作不认证证词或封印，不等于接管、签约、结盟或剧情结案。FINAL_STATUS记录审后通过，manifest保留已审原样。\n')
shutil.copyfile(__file__,P/Path(__file__).name)
members={str(f.relative_to(P)):H(f) for f in sorted(P.rglob('*')) if f.is_file() and f.name!='PACKAGE_MEMBER_SHA256.json'};(P/'PACKAGE_MEMBER_SHA256.json').write_text(json.dumps(members,ensure_ascii=False,indent=2));z=D/'leo_lyd_story_v1_reviewed.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as a:
 for f in sorted(P.rglob('*')):
  if f.is_file():a.write(f,str(f.relative_to(D)))
checked=[]
with zipfile.ZipFile(z) as a:
 assert a.testzip() is None
 for m in a.infolist():
  data=a.read(m.filename);assert hashlib.sha256(data).hexdigest()==H(D/m.filename);assert zlib.crc32(data)&0xffffffff==m.CRC;checked.append({'path':m.filename,'bytes':len(data),'sha256':H(D/m.filename),'crc32':f'{m.CRC:08x}'})
assert z.stat().st_size<18*1024*1024
files=[D/f'{k}_story_gesture_review_zh_light.png' for k in ['leo','lyd']]+[D/f'{k}_story_gesture_preview_once.gif' for k in ['leo','lyd']]+[z];report={'status':'frozen_verified_not_uploaded','zip_bytes':z.stat().st_size,'crc_test':'pass','member_hash_test':'all_pass','members':checked,'deliverables':[{'path':str(f),'bytes':f.stat().st_size,'sha256':H(f)} for f in files]};(D/'DELIVERY_CHECKS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='members'},ensure_ascii=False,indent=2))
