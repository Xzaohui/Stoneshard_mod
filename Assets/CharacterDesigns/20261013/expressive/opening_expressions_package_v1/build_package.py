from pathlib import Path
import hashlib,json,zipfile
p=Path(__file__).resolve().parent;root=p.parents[4];base=p.parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
files=set();deliver=[]
for c in ['mara','ivo']:
 d=base/c/'expressions_v1';q=d/'QA-independent.json'
 assert q.exists(),f'{c}: independent review is pending'
 qa=json.loads(q.read_text());decision=qa.get('status',qa.get('decision',''))
 assert decision.startswith('pass'),f'{c}: {decision}'
 m=json.loads((d/'manifest.json').read_text())
 for a in m['deliverables']:
  f=d/a['file'];assert sha(f)==a['sha256'];deliver.append(f)
 for a in m['assets']:
  raw=root/a['file'];assert sha(raw)==a['sha256'];assert raw.read_bytes()==(d/f'{c}_{raw.name.replace("_raw_imagegen","")}').read_bytes()
 for s in json.loads((d/'sourcehash.json').read_text())['sources']:
  f=root/s['file'];assert sha(f)==s['sha256'];files.add(f)
 status={'character':f'n1_{c}','status':'independently_reviewed_concept_ready_for_delivery','review_decision':decision,'review_sha256':sha(q),'user_approved':False,'runtime_verified':False,'animation':False,'new_characters':0,'new_expression_images':3,'manifest_preserved_as_reviewed':True,'note':'manifest内awaiting independent review为送审时快照；本状态记录独审后阶段。无剧情结果承诺。'}
 (d/'FINAL_STATUS.json').write_text(json.dumps(status,ensure_ascii=False,indent=2)+'\n')
 files.update(f for f in d.rglob('*') if f.is_file() and f.suffix!='.zip')
files.add(Path(__file__).resolve())
readme=p/'README.md';readme.write_text('# 玛拉与伊沃：六张对话表情概念\n\n两人各三张静态胸像，身份沿用已交付v2候选。两组独立审查可交付并附细微漂移说明；不表示用户逐人美感认可、动画或游戏运行验收。\n\nZIP保留项目目录结构，含六张生图原稿、六张字节一致导出、两张中文黑白底检查板、提示词、排版脚本、源身份锚原字节、来源文件、manifest、作者及独立QA、独审后FINAL_STATUS。原manifest作为被审记录不改；最新审查状态见FINAL_STATUS。\n\nSourcehash中的资料用于溯源；情绪不代表团圆、逃离成功、免债、结案或免责。\n')
files.add(readme)
zipout=base/'mara_ivo_expressions_v1_source.zip'
with zipfile.ZipFile(zipout,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for f in sorted(files):z.write(f,f.relative_to(root))
assert zipout.stat().st_size<18*1024*1024
with zipfile.ZipFile(zipout) as z:
 assert z.testzip() is None
 for f in files:assert hashlib.sha256(z.read(str(f.relative_to(root)))).hexdigest()==sha(f)
# User attachment order: two boards, six independent expressions, source zip.
deliver=sorted(deliver,key=lambda f:(0 if 'review_zh' in f.name else 1,str(f)))+[zipout]
records=[{'absolute_path':str(f.resolve()),'bytes':f.stat().st_size,'sha256':sha(f)} for f in deliver]
report={'status':'frozen_ready_for_delivery','member_count':len(files),'zip_crc_pass':True,'all_member_bytes_sha256_match':True,'attachments':records}
(p/'PACKAGE_VERIFICATION.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
