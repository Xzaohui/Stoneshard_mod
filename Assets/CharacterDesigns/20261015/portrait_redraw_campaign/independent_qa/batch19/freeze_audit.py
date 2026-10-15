#!/usr/bin/env python3
"""Freeze independently reviewed batch19; writes only this audit directory."""
from pathlib import Path
import datetime,hashlib,json
from PIL import Image,ImageDraw
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
ids=('xinya','wupo','biluo','evan')
audit=load(OUT/'final_technical_audit.json')
replay=load(OUT/'final_derivation_replay.json')
reviews=load(OUT/'v2_visual_reviews.json')['actors']
preflight=load(OUT/'preflight_source_checks.json')
assert audit['all_technical_checks_complete'] and replay['pass']
assert set(reviews)==set(ids)
frozen={'schema_version':1,'batch':19,'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'four_derived_candidates_pass_with_notes','native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'production_asset_replacement':False,'third_imagegen_permitted':False,'read_only_production_inputs':True,'write_scope':'independent_qa/batch19','actors':{},'evidence':{'technical_audit':'final_technical_audit.json','replay':'final_derivation_replay.json','source_preflight':'preflight_source_checks.json','concentrated_feedback':'v1_visual_feedback.json','visual_reviews':'v2_visual_reviews.json'},'delivery_inventory':[]}
for slug in ids:
 root=CAMP/slug; a=audit['actors'][slug]; v=reviews[slug]; m=load(root/'manifest.json'); candidate=root/v['selected']
 assert len(a['raw_integrity'])==2 and len(replay['actors'][slug]['versions'])==2
 assert sha(root/'manifest.json')==a['manifest']['sha256']
 assert v['selected']==m['selected_portrait'] and sha(candidate)==v['selected_sha256']==m['selected_sha256']
 assert all(not x['raw_alpha128_edge_counts'][edge] for x in a['raw_integrity'] if x['version']=='portrait_v2' for edge in ('left','right','top','bottom'))
 source_recheck=[]
 for rec in preflight['actors'][slug]['source_checks']:
  p=CAMP.parents[3]/rec['path'];source_recheck.append({'path':rec['path'],'sha256':sha(p),'unchanged_from_preflight':sha(p)==rec['actual_sha256']})
 assert all(x['unchanged_from_preflight'] for x in source_recheck)
 files=[{'path':str(p.relative_to(CAMP)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
 frozen['actors'][slug]={'id':m['actor_id'],'name':m['name'],'status':v['status'],'selected_portrait':str(candidate.relative_to(CAMP)),'selected_sha256':sha(candidate),'author_manifest':str((root/'manifest.json').relative_to(CAMP)),'author_manifest_sha256':sha(root/'manifest.json'),'successful_imagegen_payloads':2,'nongenerating_tool_records':a['nongenerating_tool_records'],'concentrated_revision_rounds':1,'raw_v2_four_borders_clear_at_alpha128':True,'identity_reconciliation':preflight['actors'][slug]['identity_reconciliation'],'limitations':v['limitations'],'source_recheck':source_recheck,'candidate_specification':next(x for x in a['candidates'] if x['path']==v['selected'])}
 frozen['delivery_inventory'].extend(files)
board=Image.new('RGB',(1280,570),(72,74,76));d=ImageDraw.Draw(board)
for index,slug in enumerate(ids):
 im=Image.open(CAMP/frozen['actors'][slug]['selected_portrait']).convert('RGBA');x=index*320+12
 d.text((x,8),slug+' | v2 | derived candidate',fill=(245,245,245))
 board.paste(im,(x,30),im);large=im.resize((296,400),Image.Resampling.NEAREST);board.paste(large,(x,145),large)
board.save(OUT/'selected_v2_four_character_contact.png')
# Display references directly from the audited snapshots without interpolation.
cores=Image.new('RGB',(1280,570),(72,74,76));draw=ImageDraw.Draw(cores)
for index,slug in enumerate(('mara','iwo','leiya','tore')):
 im=Image.open(CAMP/'xinya/sources'/f'{slug}_style_reference.png').convert('RGBA');x=index*320+12
 draw.text((x,8),slug+' | approved style reference',fill=(245,245,245));cores.paste(im,(x,30),im)
 big=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST);cores.paste(big,(x,145),big)
cores.save(OUT/'core_style_1x_4x.png')
(OUT/'freeze_manifest.json').write_text(json.dumps(frozen,ensure_ascii=False,indent=2)+'\n')
lines=['# Batch19 独立审计冻结','',f"冻结时间：{frozen['frozen_utc']}",'','四人均终选 v2，状态为 pass_derived_candidate_with_notes。每人 2 份实际 imagegen 回包，1 轮集中反馈；没有第三次生图。','', '## 选择与完整 SHA-256','']
for slug,a in frozen['actors'].items():
 lines += [f"- {a['name']}（{slug}）：{a['selected_portrait']}",f"  SHA-256：{a['selected_sha256']}"]
lines += ['','## 独立核验','', '- 准确当前人物卡、roster、选定母图、母图 QA、认可四核心均已核对；母图与候选真实打开查看。','- 所有 source snapshot 与原文件 SHA-256 相同，冻结时再次核对原卡/母图/母 QA/母清单未变。','- 完整工具回包图片字节与 raw 一致，并核对工具保存的原始文件。','- 先完整阅读作者脚本，再在本 QA 目录副本复跑；8 版候选、1x、8x、三底预览和 metrics 逐字节相同。','- 额外独立实现重新生成候选，74×100、最多32个可见RGB色、二值alpha和8x最近邻预览通过。','- raw 与候选分别检验真实边界；四个选定 raw 都保完整发耳，不以透明 padding 伪装裁边修复。','- 作者 manifest 全文件 SHA 与字节数、SHA256SUMS 完整覆盖均通过；freeze_manifest.json 列出全部交付文件哈希。','', '## 保留限制','']
for slug,a in frozen['actors'].items():
 lines.append(f"- {a['name']}："+'；'.join(a['limitations']))
lines += ['- 埃文现行卡的低檐帽/早白鬓角优先于旧卡时期裸头母图；已记录差异，保母图独立面形和苔披风赭衣。','- 这些是高分辨率重绘经最近邻缩小、阈值alpha和32色量化的派生候选。规格检查不能证明原生像素终稿。','- 未替换任何生产旧图、人物卡或游戏代码；未接入游戏、未实机验证；未 commit/push。','','## 交付清单','', '- 四个角色目录各含 sources、prompts、完整 tool_returns、raw、两版 candidates、1x/8x/三底 previews、QA、spec lock、manifest、SHA256SUMS、可复跑导出脚本。','- 本审计目录含来源核对、集中反馈、终选视觉评审、最终技术审计、脚本副本逐字节复跑证据、独立生成候选、四人1x/4x对照、四核心参考、冻结清单和全目录SHA256SUMS。','- 碧珞另有一次6参考图参数校验拒绝记录，未生成图片；成功成图仍为2份。无第三份成图。','- replay/ 为独立审计副本，不是新的生图调用。','']
(OUT/'README.md').write_text('\n'.join(lines))
files=[p for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='SHA256SUMS']
(OUT/'SHA256SUMS').write_text(''.join(f'{sha(p)}  {p.relative_to(OUT)}\n' for p in files))
print(json.dumps({'status':frozen['status'],'actors':{k:v['selected_sha256'] for k,v in frozen['actors'].items()},'delivery_inventory_files':len(frozen['delivery_inventory']),'qa_files_hashed':len(files)},ensure_ascii=False,indent=2))
