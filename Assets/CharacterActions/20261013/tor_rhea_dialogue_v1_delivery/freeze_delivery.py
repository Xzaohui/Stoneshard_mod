from pathlib import Path
import json,hashlib,shutil,zipfile
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'Assets/CharacterActions/20261013'
OUT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
expected={'tor':'e40ec9fc935932c8b4027b69d3e4f9ea5575fa968d789cffb68f9bab4f5e9287','rhea':'866d8468e7810dfeb39c97d2854bc9d0786a6b62cfe8594c45971e974343bfb9'}
notes=['4张新绘全身，2人各3独立身体状态及4展示阶段；首末复用。','蕾雅眉眼变化较小，主要由嘴和手势承担表达；毯端尺寸、裙褶及轮廓有轻微生成漂移。','托雷D1头发、鞋及外衣轮廓有轻微漂移；手指为像素簇概括。','只有稀疏关键姿态；没有补间、装备、碰撞、脚轨迹或游戏运行验收。','闭账本与普通卷毯不表示裁决、免债或撤离完成；没有新增角色。']
for c in expected:
 p=BASE/c/'dialogue_gesture_v1'
 assert sha(p/'QA-independent.json')==expected[c]
 st={'status':'independent_and_parent_visual_review_pass_concept_with_notes','independent_qa_sha256':expected[c],'reviewed_manifest_sha256':sha(p/'manifest.json'),'reviewed_assets_unchanged':True,'user_approved':False,'runtime_verified':False,'complete_animation':False,'notes':notes}
 (p/'FINAL_STATUS.json').write_text(json.dumps(st,ensure_ascii=False,indent=2)+'\n')
 # Old SHA256 remains pre-independent snapshot. This current member inventory supersedes only file-set completeness.
 for src,dest in [('dialogue_gesture_review_zh.png',f'{c}_dialogue_gesture_review_zh.png'),('dialogue_gesture_once.gif',f'{c}_dialogue_gesture_once.gif')]:shutil.copy2(p/src,OUT/dest)
files=[]
for c in expected:
 p=BASE/c/'dialogue_gesture_v1'
 files += [(f,f'{c}/dialogue_gesture_v1/{f.relative_to(p)}') for f in sorted(p.rglob('*')) if f.is_file()]
hashes={name:sha(f) for f,name in files}
(OUT/'SOURCE_MEMBER_SHA256.json').write_text(json.dumps(hashes,ensure_ascii=False,indent=2)+'\n')
zp=OUT/'tor_rhea_dialogue_v1_reviewed_sources.zip'
with zipfile.ZipFile(zp,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f,name in files:z.write(f,name)
 z.write(OUT/'SOURCE_MEMBER_SHA256.json','SOURCE_MEMBER_SHA256.json')
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 for name,s in hashes.items():assert hashlib.sha256(z.read(name)).hexdigest()==s
members=[{'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(OUT.glob('*')) if p.suffix in ['.png','.gif','.zip']]
assert len(members)==5 and sum(m['bytes'] for m in members)<18*1024**2
freeze={'status':'frozen_reviewed_concept_delivery','files':members,'total_bytes':sum(m['bytes'] for m in members),'zip_crc_valid':True,'zip_members_sha256_verified':True,'source_file_count':len(files),'qa_sha256':expected,'notes':notes,'user_approved':False,'runtime_verified':False}
(OUT/'DELIVERY_FREEZE.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(freeze,ensure_ascii=False,indent=2))
