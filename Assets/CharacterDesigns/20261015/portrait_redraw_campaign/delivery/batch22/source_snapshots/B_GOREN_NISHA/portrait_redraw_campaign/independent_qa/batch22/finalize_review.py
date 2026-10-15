from pathlib import Path
import json, hashlib, datetime
Q=Path(__file__).resolve().parent; B=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda f:json.loads((Q/f).read_text())
def save(f,d):(Q/f).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
tech=load('final_technical_audit.json'); visual=load('v2_visual_reviews.json'); replay=load('full_derivation_replay.json'); sources=load('source_freeze_checks.json');generation=load('generation_count_verification.json')
assert tech['all_technical_checks_complete'] and replay['pass'] and sources['pass'] and generation['pass']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
selection={'schema_version':1,'batch':22,'frozen_utc':now,'reviewer':'audit_campaign_twentysecond_batch','concept_pass_count':4,'held_count':0,'technical_integrity_pass':True,'native_pixel_approved':False,'runtime_verified':False,'max_substantive_generations_per_actor':2,'actors':{}}
deliverables=[]
for slug,vr in visual['actors'].items():
 root=B/slug; m=json.loads((root/'manifest.json').read_text()); a=tech['actors'][slug]
 selected=vr['selected']; version=Path(selected).stem.removesuffix('_74x100_candidate')
 assert m['selected_portrait']==selected and sha(root/selected)==vr['selected_sha256']==m['selected_sha256']
 assert sha(root/'manifest.json')==a['manifest']['sha256']
 selection['actors'][slug]={'status':'pass_concept_with_notes','deliverable':True,'selected_candidate':selected,'selected_candidate_sha256':vr['selected_sha256'],'displayed_version':version,'selected_version':version,'raw':'raw/portrait_v2_raw_imagegen.png','raw_sha256':vr['raw_sha256'],'author_manifest_sha256':sha(root/'manifest.json'),'author_SHA256SUMS_sha256':sha(root/'SHA256SUMS'),'generation_calls':2,'residual_limitations':[vr['identity_age_clothing'],vr['improvement'],vr['source_contour']]+vr['residual_limitations'],'native_pixel_approved':False,'runtime_verified':False}
 for relative,role in [(selected,'selected 74x100 derived candidate'),('raw/portrait_v2_raw_imagegen.png','unedited imagegen raw'),('tool_returns/portrait_v2.json','complete imagegen result'),('prompts/portrait_v2.json','actual generation parameters'),(f'previews/{version}_1x.png','exact 1x preview'),(f'previews/{version}_8x.png','exact 8x NN preview'),(f'previews/{version}_1x_backgrounds.png','three-background 1x preview'),(f'previews/{version}_4x_backgrounds.png','three-background 4x NN preview'),('sources/source_manifest.json','source provenance'),('derive_portrait.py','reviewed deterministic exporter'),('manifest.json','frozen author manifest'),('SHA256SUMS','complete author checksum list')]:
  p=root/relative;deliverables.append({'actor':slug,'path':str(p.relative_to(B)),'role':role,'bytes':p.stat().st_size,'sha256':sha(p)})
save('FINAL_SELECTION.json',selection)
save('DELIVERY_CHECKLIST.json',{'batch':22,'base':'Assets/CharacterDesigns/20261015/portrait_redraw_campaign','files':deliverables,'historical_v1_retained':True,'source_snapshots_retained':True,'not_native_or_runtime_final':True})
save('frozen_verification.json',{'checked_utc':now,'technical_integrity_pass':True,'all_technical_checks_complete':True,'source_checks':49,'independently_replayed_versions':8,'independently_replayed_files':48,'manifest_file_checks':sum(len(a['manifest']['file_checks']) for a in tech['actors'].values()),'SHA256SUMS_file_checks':sum(len(a['SHA256SUMS']) for a in tech['actors'].values()),'successful_image_outputs':8,'non_generating_parameter_rejections':1,'selection':selection['actors'],'native_pixel_approved':False,'runtime_verified':False})
lines=['# Batch22 独立 QA 终审','',f'冻结时间：{now}','', '结论：4张v2带备注概念候选可交付，0 held。仅74×100 NN/二值alpha/≤32可见色量化派生候选，非原生像素终稿，未集成或实机验收。','', '## 证据与技术验收','', '- 当前人物卡、指定母图、母图QA、mara/iwo/leiya/tore四核心均已读取并实际看图；49项来源/快照SHA全部一致，最终复核无漂移。','- 各2份成功生图，共8份完整toolreturn的image_url解码与raw逐字节一致。古烈另有一次六参照参数预检拒绝，无图返回，实参/错误均保留，不计第三份生图。','- 8候选均74×100、≤32可见RGB色、二值alpha；独立算法复算PNG逐字节一致。','- 完整读取并SHA锁定导出脚本后，只在本QA目录重放；8版本共48个候选/1x/8x/三底1x/4x/metrics文件逐字节一致。没有在作者目录重跑。','- 最终作者manifest共181文件项、SHA256SUMS共185文件项全匹配，全部文件已覆盖，selected SHA一致。','- 四个所选源的发、巾、耳完整；raw alpha>=5四边均清。madi/boh的inset为全画布技术缩放，不补回任何缺失轮廓。妮莎v1贴框风险由v2真实重画内收解决。','- 本审计不改变vere/naya的既有held裁边判断，不以透明padding洗掉源裁边。','', '## 冻结选择','']
for slug,row in selection['actors'].items():
 lines += [f'### {slug}',f'- 候选：`{slug}/{row["selected_candidate"]}`',f'- SHA256：`{row["selected_candidate_sha256"]}`']+[f'- {n}' for n in row['residual_limitations']]+['']
lines += ['## 交付入口与限制','', '- `FINAL_SELECTION.json`：唯一冻结选图/哈希/交付标记；`DELIVERY_CHECKLIST.json`：48项交付证据清单。','- `final_technical_audit.json`、`frozen_verification.json`、`full_derivation_replay.json`：最终证据；`selected_v2_1x_4x.png`：不插值1x/4x总览。','- `v1_visual_feedback.json`保存每人唯一集中反馈；`v2_visual_reviews.json`保存终审。中途initial/prefreeze报告保留历史，其中未冻结时的manifest待项已被final_technical_audit全部关闭。','- 仍有亮眼簇、发/巾细纹和头部留白差异，妮莎眼白较明显；需后续原生像素制作与游戏内可读性/透明边缘/定位验收。不能以本技术通过替代这些验收。','- 本独立QA全部写入仅限`independent_qa/batch22`，未改生产角色文件、旧图、人物卡、代码，未commit/push。']
(Q/'FINAL_REVIEW.md').write_text('\n'.join(lines)+'\n')
files=[{'path':str(p.relative_to(Q)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(Q.rglob('*')) if p.is_file() and p.name not in ('QA_FILE_INVENTORY.json','SHA256SUMS.txt')]
save('QA_FILE_INVENTORY.json',{'batch':22,'files':files,'self_excluded':'QA_FILE_INVENTORY.json and SHA256SUMS.txt excluded to avoid circular hashes'})
paths=[p for p in sorted(Q.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt']
(Q/'SHA256SUMS.txt').write_text(''.join(f'{sha(p)}  {p.relative_to(Q)}\n' for p in paths))
for row in files:assert sha(Q/row['path'])==row['sha256']
for line in (Q/'SHA256SUMS.txt').read_text().splitlines():
 digest,path=line.split(maxsplit=1);assert sha(Q/path)==digest
print(json.dumps({'complete':True,'selected':{s:r['selected_candidate_sha256'] for s,r in selection['actors'].items()},'QA_inventory_files':len(files),'QA_SHA_files':len(paths),'delivery_checklist_files':len(deliverables)},ensure_ascii=False))
