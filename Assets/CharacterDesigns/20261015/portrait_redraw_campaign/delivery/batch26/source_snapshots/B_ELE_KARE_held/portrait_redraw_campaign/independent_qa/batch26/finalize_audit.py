"""Seal independent QA only; run after author freeze and technical audit."""
from pathlib import Path
import hashlib,json,shutil
from datetime import datetime,timezone
from PIL import Image,ImageDraw
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,j:p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n')
slugs=['yur','bevi','ele','kare'];rows=[];locks=[]
for s in slugs:
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=json.loads((Q/f'{s}_final_visual_review.json').read_text());w=P/s
 ds=[d for vr in t['versions'] for d in vr['derivatives']]
 row={'slug':s,'status':v['status'],'delivery_eligible':v['delivery_eligible'],'selected_path':v['selected_path'],'selected_sha256':v['selected_sha256'],'held_evidence_path':v.get('held_evidence_path'),'held_evidence_sha256':v.get('held_evidence_sha256'),'limitations':v['limitations'],'author_manifest_sha256':t['manifest_sha256'],'author_manifest_file_count':len(t['manifest_file_checks']),'manifest_hashes_all_match':t['manifest_all_hashes_match'],'manifest_missing_files':t['manifest_missing_files'],'sha256sums_entries':t['sha256sums_count'],'sha256sums_all_match':t['sha256sums_all_match'],'all_author_source_hashes_match':all(x['all_equal'] for x in t['source_validation']),'raws_equal_full_returns':all(x['raw_equals_return'] for x in t['versions']),'all_derivatives_byte_reproduce':all(x['byte_reproduction'] for x in ds),'all_derivatives_format_pass':all(x['valid_format'] and x['transparent_rgb_zero'] for x in ds),'all_integer_NN_previews_reproduce':all(all(x['previews'].values()) for x in ds),'all_style_references_NN_reproduce':all(x['pixels_exact_8x_NN'] and x['bytes_exact_8x_NN'] for x in t['style_reference_NN_checks']),'derivative_count':len(ds),'raw_count':t['generation_count']}
 assert row['raw_count']<=2 and all(row[k] for k in ['manifest_hashes_all_match','sha256sums_all_match','all_author_source_hashes_match','raws_equal_full_returns','all_derivatives_byte_reproduce','all_derivatives_format_pass','all_integer_NN_previews_reproduce','all_style_references_NN_reproduce']) and not row['manifest_missing_files'],s
 if v['delivery_eligible']:
  assert sha(P/v['selected_path'])==v['selected_sha256'];assert t['manifest_selected_hash_matches'] and t['manifest_selected_sha256']==v['selected_sha256']
  locks.append({'slug':s,'path':v['selected_path'],'sha256':v['selected_sha256']})
 rows.append(row)
 dst=Q/'author_evidence'/s;dst.mkdir(parents=True,exist_ok=True)
 for name in ['derive_portrait.py','finalize_manifest.py','manifest.json','SHA256SUMS','SHA256SUMS.txt','sources/source_manifest.json']:
  if (w/name).exists():
   out=dst/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(w/name,out)
source=json.loads((Q/'independent_source_manifest.json').read_text());checks=[]
for x in source['sources']:
 current=sha(R/x['path']);snapshot=sha(Q/x['snapshot']);checks.append({'source_path':x['path'],'initial_sha256':x['sha256'],'current_sha256':current,'snapshot_sha256':snapshot,'all_equal':current==snapshot==x['sha256']})
assert all(x['all_equal'] for x in checks)
write(Q/'independent_source_final_recheck.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'all_unchanged':True,'items':checks})
write(Q/'selection_lock.json',{'batch':26,'delivery_include_only':locks,'delivery_exclude':'All other candidate versions and raw images are source/review evidence, not selected portraits. Any selected byte change requires a new independent check.','native_pixel_authored':False,'runtime_verified':False})
write(Q/'QA_summary.json',{'batch':26,'checked_utc':datetime.now(timezone.utc).isoformat(),'consolidated_feedback_rounds_per_person':1,'successful_generations_per_person':2,'third_generation_allowed':False,'characters':rows,'delivery_include':locks,'source_clipping_note':'First-pass bevi/kare NN border contact came from sampling narrow true source margins. Kare v2 has 82 solid pixels on the original right edge at y606–687, unlike Ele v2 closed silhouette with one real source pixel of right margin. Actual source clipping gate is held, never fixed by inset.','nonblocking_source_text_conflict':'Bevi card has 哥哥/姐姐 relationship wording inconsistency. Current CM-DEN says siblings brother/sister; no identity invention or card edits.','native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False})
board=Image.new('RGB',(4*304,420),(78,78,78));d=ImageDraw.Draw(board)
for i,x in enumerate(locks):
 im=Image.open(P/x['path']).convert('RGBA').resize((296,400),Image.Resampling.NEAREST);board.paste(im,(i*304,20),im);d.text((i*304+4,5),x['slug'],fill='white')
board.save(Q/'selected_contact_4x_NN.png')
text=['# Batch26 独立QA终审','', '四人各完成首稿＋一次集中反馈后的修订，均不得第三次生图。技术通过不等于原生逐像素或游戏内验收。','']
for x in rows:
 text += [f"## {x['slug']} · {x['status']}",f"选稿：`{x['selected_path']}`；暂挂证据：`{x['held_evidence_path']}`",f"SHA256：`{x['selected_sha256'] or x['held_evidence_sha256']}`",'限制：'+'；'.join(x['limitations']), '']
text += ['## 证据与边界','- 33份原始源文件独立快照与终检SHA不变；卡、母图/母QA、四核心与相关台本已读，母图与输出实际查看。','- 所有成功回包解码字节与raw相等；74×100、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。','- 作者manifest/全SHA覆盖完整；selected只允许selection_lock列出的文件及哈希。','- 蓓薇兄/姐文本差异仅记录；最新卡衣装优先旧母图；不改卡、旧图、生产代码或提交推送。','- inset为同raw整画布等比NN技术派生；非新生图、非原生像素终稿，未集成或实机验证。']
(Q/'FINAL_REVIEW.md').write_text('\n'.join(text)+'\n')
files=[{'path':str(f.relative_to(Q)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(Q.rglob('*')) if f.is_file() and f not in [Q/'manifest.json',Q/'SHA256SUMS']]
write(Q/'manifest.json',{'batch':26,'scope':'independent QA only','files':sorted(files,key=lambda x:x['path']),'selected':locks,'native_pixel_authored':False,'runtime_verified':False})
allfiles=[f for f in sorted(Q.rglob('*')) if f.is_file() and f!=Q/'SHA256SUMS'];(Q/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.relative_to(Q)}\n' for f in allfiles))
print(json.dumps({'batch':26,'selected':locks,'qa_manifest_files':len(files),'qa_sha_entries':len(allfiles)},indent=2))
