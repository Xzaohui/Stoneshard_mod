"""Freeze QA only, after final technical audit and manual visual reviews exist."""
from pathlib import Path
import json,hashlib,datetime,re
from PIL import Image,ImageDraw
Q=Path(__file__).resolve().parent;CAMP=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())
def save(name,data):(Q/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
audit=load(Q/'final_technical_audit.json');reviews=load(Q/'v2_visual_reviews.json')
assert audit['technical_checks_pass'], 'Final technical audit incomplete or failed'
actors={}; checklist=[];counts=[];frozen=[]
for a in audit['characters']:
 slug=a['slug'];w=CAMP/slug;rv=reviews[slug];m=load(w/'manifest.json');sel=m.get('selected_portrait') or m.get('held_evidence_portrait');sp=w/sel;version=re.match(r'portrait_v\d+',Path(sel).name).group(0);tag=Path(sel).stem.removesuffix('_74x100_candidate')
 assert sha(sp)==rv['selected_sha256']==(m.get('selected_sha256') or m.get('held_evidence_sha256'))
 assert sha(w/'manifest.json')==a['manifest']['sha256']
 assert a['successful_image_returns']==2
 deliverable=rv['visual_pass'];assert deliverable or m['status'].startswith('held')
 actors[slug]={'name':a['name'],'canonical_id':a['canonical_id'],'status':rv['status'],'deliverable':deliverable,'selected_candidate':sel,'selected_candidate_sha256':sha(sp),'selected_version':tag,'displayed_version':tag,'raw':f'raw/{version}_raw_imagegen.png','raw_sha256':sha(w/'raw'/f'{version}_raw_imagegen.png'),'author_manifest_sha256':sha(w/'manifest.json'),'author_SHA256SUMS_sha256':sha(w/'SHA256SUMS'),'generation_calls':2,'visual_observations':rv['observations'],'residual_limitations':rv['residual_limitations'],'native_pixel_approved':False,'runtime_verified':False}
 if not deliverable:
  actors[slug]['evidence_only']=True;actors[slug]['blocker']=rv['blocker'];actors[slug]['held_evidence_candidate']=sel;actors[slug]['held_evidence_sha256']=sha(sp);actors[slug]['selected_candidate']=None;actors[slug]['selected_candidate_sha256']=None;actors[slug]['selected_version']=None
 counts.append({'actor':slug,'successful_image_returns':a['successful_image_returns'],'raw_files':len(list((w/'raw').glob('*_raw_imagegen.png'))),'author_generation_calls':m['generation_calls'],'non_image_tool_records':a.get('non_image_tool_records',[]),'within_two_image_limit':True})
 selected_files=[(sel,'selected derived candidate' if deliverable else 'HELD evidence candidate only'),(f'raw/{version}_raw_imagegen.png','unedited imagegen raw'),(f'tool_returns/{version}.json','complete imagegen result'),(f'prompts/{version}.json','actual generation arguments'),(f'previews/{tag}_1x.png','exact 1x preview'),(f'previews/{tag}_8x.png','exact 8x NN preview'),(f'previews/{tag}_1x_backgrounds.png','three-background 1x preview'),(f'previews/{tag}_4x_backgrounds.png','three-background exact 4x NN preview'),('sources/source_manifest.json','source provenance'),('spec_lock.md','identity and style constraints'),('derive_portrait.py','read-reviewed deterministic exporter'),('manifest.json','frozen author manifest'),('SHA256SUMS','complete author hashes')]
 for rel,role in selected_files:
  p=w/rel;checklist.append({'actor':slug,'deliverable':deliverable,'path':str(p.relative_to(CAMP)),'role':role,'bytes':p.stat().st_size,'sha256':sha(p)})
 for row in m['files']:
  p=w/row['path'];frozen.append({'path':str(p.relative_to(CAMP)),'sha256':row['sha256']})
 for rel in ['manifest.json','SHA256SUMS']:frozen.append({'path':f'{slug}/{rel}','sha256':sha(w/rel)})
selection={'schema_version':1,'batch':23,'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reviewer':'audit_campaign_twentythird_batch','concept_pass_count':sum(x['deliverable'] for x in actors.values()),'held_count':sum(not x['deliverable'] for x in actors.values()),'technical_integrity_pass':True,'native_pixel_approved':False,'runtime_verified':False,'max_substantive_generations_per_actor':2,'actors':actors,'scope':'Technical integrity can pass while visual source cropping is held. Reha is evidence only and must not be merged into accepted candidate delivery.'}
save('FINAL_SELECTION.json',selection);save('DELIVERY_CHECKLIST.json',{'batch':23,'base':str(CAMP.relative_to(CAMP.parents[3])),'accepted_actors':[k for k,v in actors.items() if v['deliverable']],'held_actors':[k for k,v in actors.items() if not v['deliverable']],'files':checklist,'instructions':'Keep accepted candidate files separate from HELD evidence. Include limitations, source provenance, raw returns, and QA. No runtime or native-final claims.'})
save('generation_count_verification.json',counts)
# Recheck immutable source snapshot inventory from first preflight against current originals and snapshots.
pre=load(Q/'preflight_source_checks.json'); source_rows=[]
for a in pre['characters']:
 for r in a['sources']:
  op=CAMP.parents[3]/r['source'];lp=CAMP/a['slug']/r['snapshot'];source_rows.append({'actor':a['slug'],'source':r['source'],'snapshot':r['snapshot'],'expected_sha256':r['recorded_sha256'],'source_matches':sha(op)==r['recorded_sha256'],'snapshot_matches':sha(lp)==r['recorded_sha256']})
assert all(x['source_matches'] and x['snapshot_matches'] for x in source_rows)
save('source_freeze_checks.json',{'all_original_and_snapshot_hashes_unchanged':True,'count':len(source_rows),'checks':source_rows})
# Labelled review sheet, without overlap, accepted then held; no image redrawing.
board=Image.new('RGB',(1280,560),(83,83,83));draw=ImageDraw.Draw(board)
for i,(slug,a) in enumerate(actors.items()):
 im=Image.open(CAMP/slug/(a['selected_candidate'] or a['held_evidence_candidate'])).convert('RGBA');bg=Image.new('RGBA',im.size,(226,222,210,255));bg.alpha_composite(im)
 board.paste(bg.convert('RGB'),(i*320+8,25));board.paste(bg.resize((296,400),Image.Resampling.NEAREST).convert('RGB'),(i*320+8,145));draw.text((i*320+8,6),slug+(' - CANDIDATE' if a['deliverable'] else ' - HELD / CROPPED'),fill=(255,255,255))
board.save(Q/'selected_v2_1x_4x.png')
lines=['# Batch23 独立肖像QA','',f"结论：{selection['concept_pass_count']}人可交带限制技术候选，{selection['held_count']}人保留为held证据。",'','## 范围与验证','- 已读AGENTS、当前roster与四张现卡、母QA和相关剧情；实际看母图、Mara/Iwo/Leiya/Tore四核心、四人两轮raw及1×/整数NN三背景。','- 原件/源快照SHA、完整回包base64与raw字节一致、74×100/≤32可见RGB/二值alpha/透明RGB归零，逐候选独立重构与复制已读脚本重放，候选和所有预览逐字节复现；manifest与SHA全覆盖通过。','- 每人2份成功图像。桑勒另有六参考超限请求，在生成前被拒绝，0图像，不算第三份成功图像。','- 四人身份与当前年龄/衣色成立；现卡明确外观优先于旧概念图。','', '## 各人结论']
for slug,a in actors.items():
 lines += ['',f"### {a['name']} / {a['canonical_id']}",f"状态：{a['status']}；可交={a['deliverable']}。",f"候选/held证据：`{slug}/{a['selected_candidate'] or a['held_evidence_candidate']}`",f"SHA256：`{a['selected_candidate_sha256'] or a['held_evidence_sha256']}`"]
 lines += ['- '+x for x in a['visual_observations']]
 lines += ['- 限制：'+x for x in a['residual_limitations']]
 if not a['deliverable']:lines += ['- 阻断：'+a['blocker']]
lines += ['', '## 交付边界','仅桑勒、温诺、布岚进入可交候选。雷哈v2是锁定的失败证据，不回退不安全v1，也不进行第三次生成。','NN缩放、居中与临时量化是技术派生，inset/containment不会补回裁掉的源发尖；不是原生逐像素终稿，没有游戏内集成或实机验收。','仅写本QA目录。未修改旧图、源卡、代码，未commit/push。','交付具体路径及全SHA见FINAL_SELECTION.json、DELIVERY_CHECKLIST.json与SHA256SUMS.txt。','早期进度审计是在作者目录尚未冻结时运行，缺raw或清单不一致保留为历史；新加8×NN源在后续审计按派生预览验证。最终以final_technical_audit.json和frozen_verification.json为准。']
(Q/'FINAL_REVIEW.md').write_text('\n'.join(lines)+'\n')
checks=[dict(x,current_sha256=sha(CAMP/x['path']),matches=sha(CAMP/x['path'])==x['sha256']) for x in frozen]
assert all(x['matches'] for x in checks)
save('frozen_verification.json',{'all_author_files_still_match_final_audit':True,'count':len(checks),'checks':checks})
files=[p for p in sorted(Q.rglob('*')) if p.is_file() and p.name not in ['QA_FILE_INVENTORY.json','SHA256SUMS.txt']]
save('QA_FILE_INVENTORY.json',{'batch':23,'files':[{'path':str(p.relative_to(Q)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files],'self_exclusions':['QA_FILE_INVENTORY.json','SHA256SUMS.txt']})
files=[p for p in sorted(Q.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt'];(Q/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(Q)}\n' for p in files))
for ln in (Q/'SHA256SUMS.txt').read_text().splitlines():
 digest,rel=ln.split('  ',1);assert sha(Q/rel)==digest
print(json.dumps({'accepted':selection['concept_pass_count'],'held':selection['held_count'],'qa_files':len(files),'final_selection_sha256':sha(Q/'FINAL_SELECTION.json'),'qa_sha256sums_sha256':sha(Q/'SHA256SUMS.txt')},ensure_ascii=False,indent=2))
