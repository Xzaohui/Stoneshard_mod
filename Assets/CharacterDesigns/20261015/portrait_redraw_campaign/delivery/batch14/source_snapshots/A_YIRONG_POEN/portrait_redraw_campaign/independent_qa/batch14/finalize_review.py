#!/usr/bin/env python3
from pathlib import Path
from PIL import Image, ImageDraw
import datetime,hashlib,json
O=Path(__file__).resolve().parent;C=O.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
a=json.loads((O/'frozen_technical_audit.json').read_text())
assert a['all_technical_checks_complete'],(a['hard_errors'],a['pending'])
notes={
'yirong':'50多银低髻、素黑窄领与疲惫追问成立；v2删掉长垂碎发并简化发块、缩短颈领。中央眉势仍轻微偏忧，少量眼白和细簇留作候选备注。',
'poen':'约60瘦颧、灰卷发宽胡须、审视眯眼和短颈窄领成立；v2关闭原图发卷真实撞边与宽胸领问题。须发少量细簇、眼白和MEDIANCUT使极窄赭领偏棕保留备注。职业是旧料回收匠，非领班。',
'fenko':'30多长角脸、克制自尊抿嘴，亚麻帽棕发及绿/炭窄领成立；v2放大脸并显著缩短裸颈锁骨，同raw整图等比NN inset关闭导出右帽尾贴框。少量眼白、细发簇及颈领余量保留备注。',
'lodo':'40多宽鼻颧和成熟宽脸、偏侧专业接待小笑成立；v2缩短颈领并完整收进右巾结，暗锈/蓝灰领可辨，与芬珂瘦直嘴区分。少量发线、颈肩余量与眼白保留备注。'}
selection={'review_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'batch':'batch14','qualified_candidate_count':4,'held_count':0,'selected':[],'native_pixel_approved':False,'runtime_verified':False,'freeze_scope':'All four production directories read-only; independent QA only writes this batch14 folder.','technical_audit':'frozen_technical_audit.json','technical_audit_sha256':sha(O/'frozen_technical_audit.json'),'generation_budget':'Exactly two successful image-generation results per character: initial + one concentrated necessary revision. Fenko inset is a technical export from the same v2 raw, not another generation.'}
board=Image.new('RGB',(1280,540),(62,62,62));d=ImageDraw.Draw(board)
for i,slug in enumerate(['yirong','poen','fenko','lodo']):
 m=json.loads((C/slug/'manifest.json').read_text());selected=m['selected_portrait'];p=C/slug/selected
 actor=a['actors'][slug];metrics=next(x for x in actor['candidates'] if x['path']==selected)
 row={'slug':slug,'canonical_id':m['actor_id'],'name':m['name'],'selected':f'{slug}/{selected}','sha256':sha(p),'decision':'candidate_with_notes','visual_note':notes[slug],'native_pixel_approved':False,'runtime_verified':False,'generation_calls':len(actor['raw_integrity']),'independent_actual_pixel_review':True,'edge_clipping':False,'production_manifest_sha256':sha(C/slug/'manifest.json'),'production_sha256sums_sha256':sha(C/slug/('SHA256SUMS.txt' if (C/slug/'SHA256SUMS.txt').exists() else 'SHA256SUMS'))}
 for key in ['size','visible_rgb_colors','alpha_values','alpha_bbox','pixel_reproduction_pass','png_byte_identical','independently_matching_methods']:
  row[key]=metrics[key]
 row['source_checks_passed']=sum(x['hash_matches'] for x in actor['sources'])
 row['inventory_checks_passed']=len(actor['manifest']['file_checks'])
 selection['selected'].append(row)
 im=Image.open(p).convert('RGBA');d.text((i*320+10,5),slug+(' v2 inset' if slug=='fenko' else ' v2')+' / 1x + 4x',fill='white');board.paste(im,(i*320+10,27),im);big=im.resize((296,400),Image.Resampling.NEAREST);board.paste(big,(i*320+10,136),big)
(O/'FINAL_SELECTION.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n');board.save(O/'final_selected_1x_4x.png')
lines=['# Batch 14 独立冻结审查','','结论：4/4 可交付为带备注的重绘头像候选。没有原生逐像素批准，也没有游戏内验证。','','## 冻结选稿','']
for r in selection['selected']:
 lines += [f"- {r['name']}（{r['canonical_id']}）：`{r['selected']}`",f"  - SHA256：`{r['sha256']}`",f"  - {r['visual_note']}"]
lines+=['','## 来源、原始回包与导出复现','','- 已读现卡、关键关联台本、旧QA及母版manifest；实际看四身份母版、四核心风格参考、四首稿与四修订图。','- 年龄和伊榕黑衣按现卡优先。泊恩职业为旧料回收匠；父交接“领班”已澄清，生产prompt未采用错误身份。','- 每人两次成功生图，共8张raw；逐张独立比对完整tool image payload、归档raw和可访问generated original。全部字节一致。','- 四人所有来源snapshot与原来源及记录SHA一致；原人物卡和旧母版未改。','- 所有74×100候选均独立复现导出像素与PNG文件字节，并校验≤32可见色、二值alpha、透明RGB归零、8x严格最近邻。','- 4个终选四边透明。芬珂inset前的raw本来轮廓完整；仅通过等比整图NN留边避免采样后贴框，没有画补边或第三次生图。','- 完整生产manifest files、SHA256SUMS及所选SHA逐一实核通过。','- 初稿或生产收尾过程中记录的清单缺项/暂时哈希差异均在冻结审计关闭；以frozen_technical_audit.json为最终技术结论。','','## 边界','','- 限色是临时候选导出预算；生成图经最近邻、alpha阈值和无抖动量化，不是原生74×100手工逐像素绘制。','- 仍有少量亮眼白、细簇及个别眉势/颈领余量，已作为非阻断候选备注，不得转述为毫无问题的原生终稿。','- 本QA仅写independent_qa/batch14；没有改生产图、人物卡或代码，没有提交或推送。','']
(O/'FINAL_REVIEW.md').write_text('\n'.join(lines))
production=[]
for slug in ['yirong','poen','fenko','lodo']:
 for p in sorted((C/slug).rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts: production.append({'path':str(p.relative_to(C)),'bytes':p.stat().st_size,'sha256':sha(p)})
(O/'frozen_production_inventory.json').write_text(json.dumps({'recorded_utc':selection['review_utc'],'files':production},ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'qualified':4,'source_checks':sum(r['source_checks_passed'] for r in selection['selected']),'production_inventory_files':len(production),'selected':[{k:r[k] for k in ['slug','selected','sha256','visible_rgb_colors']} for r in selection['selected']]},ensure_ascii=False,indent=2))
