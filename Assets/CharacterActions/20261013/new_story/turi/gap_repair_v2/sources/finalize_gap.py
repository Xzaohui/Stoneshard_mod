from pathlib import Path
import json,hashlib,zipfile,sys,shutil
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');b=r/'Assets/CharacterActions/20261013/new_story';out=b/'character_gap_repair_v2_delivery';out.mkdir(exist_ok=True)
for s in sys.argv[1:]:
 p=b/s/'gap_repair_v2'; qa=json.loads((p/'INDEPENDENT_QA.json').read_text());n=2 if s=='cuoer' else 1
 # QA recorded by separate reviewer; preserve unchanged.
 f=p/f'exports/attempt{n}_transparent.png'
 final={'character':s,'author_sole_writer':'repair_character_action_gaps','status':'accepted_static_concept','accepted_count':1,'missing_count':0,'action':'A1','selected':str(f.relative_to(r)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'new_generation_calls':n,'independent_qa_path':str((p/'INDEPENDENT_QA.json').relative_to(r)),'independent_qa_sha256':hashlib.sha256((p/'INDEPENDENT_QA.json').read_bytes()).hexdigest(),'author_actual_views':['original mother','previous failed v2','all new raw RGBA','all new true light and dark composites','mother-action comparison board'],'old_files_unchanged':True,'native_alpha_preserved':True,'continuous_animation':False,'runtime_verified':False,'uploaded':False,'git_operations':False,'limits':['仅独立静态动作概念，非连续动画与游戏适配。','所有新尝试完整保留，失败稿不计入通过。','无人体脚本绘制、拼接、裁切或拉伸；仅完整画布nearest等比展示排版。']}
 if s=='cuoer':final['limits'].append('原生alpha最高254，低alpha外晕保留；当前浅深底肉眼无明显背景，后续引擎适配未验。')
 (p/'FINAL_STATUS.json').write_text(json.dumps(final,ensure_ascii=False,indent=2));shutil.copy2('/tmp/finalize_gap.py',p/'sources/finalize_gap.py');shutil.copy2('/tmp/package_gap.py',p/'sources/package_gap.py')
 manifest=[]
 for x in sorted(p.rglob('*')):
  if x.is_file() and x.name!='SOURCE_MANIFEST.json': manifest.append({'path':str(x.relative_to(p)),'bytes':x.stat().st_size,'sha256':hashlib.sha256(x.read_bytes()).hexdigest()})
 (p/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2));z=out/f'{s}_A1_gap_repair_v2_sources.zip'
 with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as zz:
  for x in sorted(p.rglob('*')):
   if x.is_file():zz.write(x,str(x.relative_to(p.parent)))
 assert z.stat().st_size<18*1024*1024
 with zipfile.ZipFile(z) as zz:
  assert zz.testzip() is None
  for x in p.rglob('*'):
   if x.is_file():assert zz.read(str(x.relative_to(p.parent)))==x.read_bytes()
 print(json.dumps({'path':str(z.relative_to(r)),'bytes':z.stat().st_size,'sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'all_members_readback_equal':True}))
