"""Freeze QA only after author manifests and final visual decisions are locked.
All original files are read-only. Selected bytes are explicitly allowlisted.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,io,subprocess
from PIL import Image,ImageDraw
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
slugs=['vila','hepo','siyu','buxi'];rows=[];locks=[]
for s in slugs:
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=json.loads((Q/f'{s}_final_visual_review.json').read_text());w=P/s
 ds=[d for vr in t['versions'] for d in vr['derivatives']]
 row={'slug':s,'status':v['status'],'delivery_eligible':v['delivery_eligible'],'selected_path':v['selected_path'],'selected_sha256':v['selected_sha256'],'held_evidence_path':v.get('held_evidence_path'),'held_evidence_sha256':v.get('held_evidence_sha256'),'limitations':v['limitations'],'author_manifest_sha256':t['manifest_sha256'],'author_manifest_file_count':len(t['manifest_file_checks']),'manifest_hashes_all_match':t['manifest_all_hashes_match'],'manifest_missing_files':t['manifest_missing_files'],'sha256sums_entries':t['sha256sums_count'],'sha256sums_all_match':t['sha256sums_all_match'],'sha256sums_missing_files':t['sha256sums_missing_files'],'all_author_source_hashes_match':all(x['all_equal'] for x in t['source_validation']),'raws_equal_full_returns':all(x['raw_equals_return'] for x in t['versions']),'all_derivatives_byte_reproduce':all(x['byte_reproduction'] for x in ds),'all_derivatives_format_pass':all(x['valid_format'] and x['transparent_rgb_zero'] for x in ds),'all_integer_NN_previews_reproduce':all(all(x['previews'].values()) for x in ds),'all_present_author_style_reference_enlargements_NN_reproduce':all(x['pixels_exact_8x_NN'] and x['bytes_exact_8x_NN'] for x in t['style_reference_NN_checks']),'author_style_reference_enlargement_count':len(t['style_reference_NN_checks']),'all_prompts_exact_and_transparent':all(x['prompt_text_equals_exact_args'] and x['transparent_background'] for x in t['versions']),'derivative_count':len(ds),'raw_count':t['generation_count'],'successful_tool_returns':t['successful_tool_returns'],'raw_count_matches_successful_tool_returns':t['raw_count_matches_successful_tool_returns'],'preflight_rejections_without_image':t['preflight_rejections_without_image']}
 assert row['raw_count']<=2 and row['raw_count_matches_successful_tool_returns'] and all(row[k] for k in ['manifest_hashes_all_match','sha256sums_all_match','all_author_source_hashes_match','raws_equal_full_returns','all_derivatives_byte_reproduce','all_derivatives_format_pass','all_integer_NN_previews_reproduce','all_present_author_style_reference_enlargements_NN_reproduce','all_prompts_exact_and_transparent']) and not row['manifest_missing_files'] and not row['sha256sums_missing_files'],s
 assert all(t['manifest_false_native_runtime_flags'][k] is False for k in ['native_authored','native_pixel_approved','runtime_integrated','runtime_verified']),s
 if v['delivery_eligible']:
  assert sha(P/v['selected_path'])==v['selected_sha256'];assert t['manifest_selected_hash_matches'] and t['manifest_selected_sha256']==v['selected_sha256']
  locks.append({'slug':s,'path':v['selected_path'],'sha256':v['selected_sha256']})
 else:
  assert t['manifest_selected_path'] is None and t['manifest_selected_sha256'] is None and t['manifest_delivery_eligible'] is False,s
  assert str(Path(s)/t['manifest_held_evidence'])==v['held_evidence_path'] and t['manifest_held_evidence_sha256']==v['held_evidence_sha256'],s
 rows.append(row)
 dst=Q/'author_evidence'/s;dst.mkdir(parents=True,exist_ok=True)
 for name in ['derive_portrait.py','finalize_manifest.py','manifest.json','SHA256SUMS','SHA256SUMS.txt','sources/source_manifest.json']:
  if (w/name).exists():
   out=dst/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(w/name,out)
core=Image.new('RGB',(1216,420),(78,78,78));draw=ImageDraw.Draw(core)
for i,n in enumerate(['mara','iwo','leiya','tore']):
 im=Image.open(P/'vila/sources'/f'{n}_style_reference.png').convert('RGBA').resize((296,400),Image.Resampling.NEAREST);core.paste(im,(i*304,20),im);draw.text((i*304+4,5),n,fill='white')
buf=io.BytesIO();core.save(buf,format='PNG');assert buf.getvalue()==(Q/'core_style_4x_NN.png').read_bytes()
write(Q/'core_style_NN_audit.json',{'integer_factor':4,'compositing':'RGBA on gray, no filtering or face editing','byte_reproduced':True,'preview_sha256':sha(Q/'core_style_4x_NN.png')})
checks=[]
for mf in ['independent_source_manifest.json','supplemental_source_manifest.json']:
 for x in json.loads((Q/mf).read_text())['sources']:
  path=x['path'];data=subprocess.check_output(['git','show',path[4:]],cwd=R) if path.startswith(('git ','git:')) else (R/path).read_bytes()
  current=hashlib.sha256(data).hexdigest();snapshot=sha(Q/x['snapshot']);checks.append({'source_path':path,'initial_sha256':x['sha256'],'current_sha256':current,'snapshot_sha256':snapshot,'all_equal':current==snapshot==x['sha256']})
assert all(x['all_equal'] for x in checks)
write(Q/'independent_source_final_recheck.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'all_unchanged':True,'items':checks})
write(Q/'selection_lock.json',{'batch':38,'delivery_include_only':locks,'delivery_exclude':'Every other version/raw is review evidence, not a selected portrait. Any selected byte change requires another independent check.','native_pixel_authored':False,'native_pixel_approved':False,'runtime_verified':False})
write(Q/'QA_summary.json',{'batch':38,'checked_utc':datetime.now(timezone.utc).isoformat(),'consolidated_feedback_rounds_per_person':1,'successful_generations_per_person':{r['slug']:r['raw_count'] for r in rows},'third_generation_allowed':False,'characters':rows,'delivery_include':locks,'source_clipping_policy':'Assess actual raw silhouette and multilevel alpha boundaries. Target-grid edge contact with real source margin is not source clipping; inset never repairs genuinely cut source hair/ears. Each final visual review records its own evidence.','native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False})
board=Image.new('RGB',(max(1,len(locks))*304,420),(78,78,78));d=ImageDraw.Draw(board)
for i,x in enumerate(locks):
 im=Image.open(P/x['path']).convert('RGBA').resize((296,400),Image.Resampling.NEAREST);board.paste(im,(i*304,20),im);d.text((i*304+4,5),x['slug'],fill='white')
board.save(Q/'selected_contact_4x_NN.png')
lines=['# Batch38 独立QA终审','','每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。','']
for x in rows:
 lines += [f"## {x['slug']} · {x['status']}",f"选稿：`{x['selected_path']}`" if x['delivery_eligible'] else f"暂挂证据：`{x['held_evidence_path']}`",f"SHA256：`{x['selected_sha256'] or x['held_evidence_sha256']}`",'限制：'+'；'.join(z.rstrip('。') for z in x['limitations'])+'。','']
lines += ['## 证据与边界',f"- {len(checks)}份原始源/历史git证据独立快照与终检SHA一致；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。",'- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。','- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。','- 维菈约40岁中性可逆提案，性别未定，人物左眼放大夹不反向。司榆遵最新正文女性，末段单他记录为歧义。布希旧卡未定、母brief/prompt女性与现卡S91孤立他经历史核对后由协调保女性继续，未改源卡；最新年龄衣装细描优先。','- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。']
(Q/'FINAL_REVIEW.md').write_text('\n'.join(lines)+'\n')
files=[{'path':str(f.relative_to(Q)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(Q.rglob('*')) if f.is_file() and f not in [Q/'manifest.json',Q/'SHA256SUMS']]
write(Q/'manifest.json',{'batch':38,'scope':'independent QA only','files':files,'selected':locks,'native_pixel_authored':False,'runtime_verified':False})
allfiles=[f for f in sorted(Q.rglob('*')) if f.is_file() and f!=Q/'SHA256SUMS'];(Q/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.relative_to(Q)}\n' for f in allfiles))
print(json.dumps({'batch':38,'selected':locks,'qa_manifest_files':len(files),'qa_sha_entries':len(allfiles)},ensure_ascii=False,indent=2))
