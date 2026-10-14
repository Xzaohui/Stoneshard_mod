from pathlib import Path
import json,hashlib,datetime,shutil
from PIL import Image,ImageDraw,ImageFont
r=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');base=r/'Assets/CharacterDesigns/20261013/expressive/new_story';audit=r/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/fifth_expression_recovery_20261014';brief=audit.parent/'fifth_four_expression_brief.json';b=json.loads(brief.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();write=lambda p,x:p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n');now=datetime.datetime.now(datetime.timezone.utc).isoformat()
observations={
'endai':['E1眉内抬、眼睑下落、嘴合，较母图开口报岗转为沉思；灰短须、三补片披风及局部甲保留。','E2唯一修订已修正双人，但头明显变小、身腿变长；不符合本人母图比例锁，未通过且不计完成。'],
'wadun':['E1由母图闭嘴小笑变小开口干笑，眉眼仍有警觉；窄亮上齿与不用整齐白牙文字有轻微偏差，未形成夸张笑口，留注不返工。','E2眉压低且唇闭，敛笑防备清楚；两图低蹲、左右残甲和锅铲、双手双足完整。'],
'ertai':['E1低头垂眼看板、合唇沉思；板与笔仍由原手持有。','E2平眉闭嘴侧视，小幅避开交谈者；不是发令、登记承诺或交板。'],
'suier':['E1闭嘴、目光侧方警听；原护领手不变，另一手由开掌收低。','E2垂眼内眉抬、唇角沉，自省不安；两图画面左半靴包布、右完整靴保留，未混用FX-LOT女性。']}
oldmap={'endai_E1_quiet_waiting_reflection_initial.png':'exec-88cd87d2-b307-43cf-9d51-b9da94a1b52f.png','endai_E2_no_order_no_entry_initial.png':'exec-a5175dba-aacc-43bb-999f-a9dad52190ca.png','endai_E2_no_order_no_entry_revision1.png':'exec-11981b77-52a9-4594-916f-9f483c599ca4.png'}
rec=json.loads((audit/'RECOVERY_AUDIT.json').read_text())
for c in b['characters']:
 who=c['slug'];d=base/who/'expressions_v1';checks=json.loads((d/'technical_qa.json').read_text());calls=[]
 for p in sorted((d/'raw').glob('*.png')):
  key=next(e['key'] for e in c['expressions'] if p.name.startswith(e['key']));e=next(e for e in c['expressions'] if e['key']==key);rev='revision1' in p.name
  if who=='wadun':j=json.loads((d/'prompts'/f'{key}_call_20261014.json').read_text());j['record_type']='observed_exact_call';calls.append(j)
  else:
   prompt=d/'prompts'/f'{key}_{"revision1" if rev else "initial"}.txt';gpath=Path('/workspace/scratch/5ed8df2c5d81/generated_images')/oldmap[p.name] if who=='endai' else Path(next(x['generated_output_path'] for x in rec['recoveries'] if x['character']==who and x['expression']==e['id']))
   assert sha(p)==sha(gpath)
   calls.append({'record_type':'recovered_historical_output','expression':e['id'],'phase':'revision1' if rev else 'initial','raw_path':str(p.relative_to(d)),'raw_sha256':sha(p),'generated_output_path':str(gpath),'generated_output_mtime_utc':datetime.datetime.fromtimestamp(gpath.stat().st_mtime,datetime.timezone.utc).isoformat(),'matching_generated_output_sha_verified':True,'preserved_prompt_path':str(prompt.relative_to(d)),'preserved_prompt_sha256':sha(prompt),'prompt_provenance':'prewritten prompt recovered; exact historical tool-call arguments were not recoverable, so equality to the actual sent prompt is not claimed','actual_tool_arguments':None,'reference_identity_verified_now':c['source_anchor'],'selection':'rejected_double_person_initial' if who=='endai' and e['id']=='E2' and not rev else ('blocked_proportion_drift_revision_budget_exhausted' if who=='endai' and e['id']=='E2' else 'selected_after_recovery_QA')})
 write(d/'generation-log.json',{'created_utc':now,'generator':'builtin imagegen','new_calls_this_recovery':2 if who=='wadun' else 0,'historical_output_count':0 if who=='wadun' else len(calls),'initial_output_count':2,'hard_error_revision_output_count':1 if who=='endai' else 0,'max_revisions_per_pose':1,'calls':calls,'history_limit':'Historical call arguments are unavailable for recovered files; existing prompt, raw PNG, file metadata, source hashes and new visual QA are preserved. No regenerated substitute was made for missing logs.' if who!='wadun' else None})
 write(d/'QA-author.json',{'status':'author_seven_pass_one_blocked_final_independent_pending','character':who,'created_utc':now,'raw_and_mother_images_actually_viewed':True,'light_and_dark_boards_actually_viewed':True,'observations':observations[who],'selected_bindings':[{'path':x['transparent_path'],'sha256':x['transparent_sha256']} for x in checks if '/selected/' in '/'+x['transparent_path']],'blocking_issues':[observations[who][1]] if who=='endai' else [],'runtime_verified':False})
 (d/'README.md').write_text(f"# {c['name']} {c['canonical_id']}｜第五批表情\n\n"+('合格选稿1张：E1迟令沉思。E2未通过，不计为完成。E2首稿错误为双人，唯一修订虽改单人，但头变小、身腿拉长，偏离母图比例；全部原稿保留在raw/，pending/中仅为审查派生，均不可选用。未新增第三次调用。\n' if who=='endai' else '合格候选2张，表情为可逆美术演出提案，不是剧情结局或永久身份变更。\n')+'\n## 来源与提示词\n'+('本次恢复时新调用builtin imagegen两次，真实prompt在prompts/*actual_20261014.txt；对应call JSON保留逐字参数、引用母图路径与SHA、输出SHA。\n' if who=='wadun' else '本图恢复自既有生成PNG，未重复生图。保留既有预写prompt、原始PNG、生成目录来源与SHA；旧任务实际调用参数无法完整恢复，因此不将预写prompt冒称为已证实的真实调用。身份母图、角色卡、台本与新独审均逐SHA绑定。\n')+'\n## 图像处理\n仅将alpha≤8像素归零（含alpha0隐藏RGB）；alpha>8的RGBA逐像素不变。未重画、拉伸、裁切、调色或量化人物。浅深板仅完整图等比nearest排版，不代表运行网格。\n\n## 本人保持项\n'+c['observed_mother_image']+'\n\n'+'\n'.join('- '+x for x in observations[who])+'\n\n## 边界\n原始卡与台本不改；不新增任务完成、通行、任命、赦免、康复或关系。原生精灵网格、部件/遮罩/锚点、装备、动画与游戏运行均未验证。独审通过项冻结后再交付，文件保存不等于已送达。\n',encoding='utf-8')
 # Freeze manifest/status deliberately deferred until final independent derived-file QA.
font=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',27);title=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc',40);small=ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',25)
for slugs,folder,titletext,note,filename in [(['endai','wadun'],'fifth_four_expressions_endai_wadun_delivery_v1','恩岱 · 瓦顿｜三张合格表情','恩岱E2比例未通过，未列入合格图；原稿与问题说明在恩岱源包。','恩岱_瓦顿_三种合格表情_浅深对照.png'),(['ertai','suier'],'fifth_four_expressions_ertai_suier_delivery_v1','珥泰 · 燧珥｜四种表情','人物表情为可逆演出提案，不代表剧情已完成。','珥泰_燧珥_四种表情_浅深对照.png')]:
 out=base/folder;out.mkdir(exist_ok=True);entries=[]
 for who in slugs:
  c=next(c for c in b['characters'] if c['slug']==who)
  for e in c['expressions']:
   p=base/who/'expressions_v1/selected'/(e['key']+'_transparent.png')
   if p.exists():entries.append((p,c['name']+'｜'+e['label_zh']));shutil.copy2(p,out/p.name)
 width=1800;height=1800;board=Image.new('RGB',(width,height),'#ede8dc');dr=ImageDraw.Draw(board);dr.rectangle((0,900,width,height),fill='#20262b');dr.text((50,22),titletext,font=title,fill='#242a2e');dr.text((50,82),note,font=small,fill='#5a5047');col=width//len(entries)
 for row in range(2):
  ink='#242a2e' if row==0 else '#ede8dc';top=140 if row==0 else 950
  for i,(p,label) in enumerate(entries):
   dr.text((i*col+25,top),label,font=font,fill=ink);im=Image.open(p).convert('RGBA');im.thumbnail((col-40,655),Image.Resampling.NEAREST);board.paste(im,(i*col+(col-im.width)//2,top+55+(655-im.height)//2),im)
  dr.text((45,top+705),'全身透明原图另附｜未验证游戏运行、装备与动画兼容',font=small,fill=ink)
 board.save(out/filename)
 (out/'INDEX.md').write_text('# '+titletext+'\n\n'+note+'\n\n透明选稿'+str(len(entries))+'张、中文浅深对照1张、每人完整源ZIP各1份。源ZIP保留原稿、母图、提示词与来源、QA及冻结清单。\n\n未上传、未发送；不代表游戏落地。\n',encoding='utf-8')
 print(out/filename)
shutil.copy2(__file__,audit/'prepare_documentation_and_boards.py')
