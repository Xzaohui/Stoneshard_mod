from pathlib import Path
from PIL import Image, ImageDraw
import hashlib, json, datetime
OUT=Path(__file__).resolve().parent
CAMP=OUT.parent.parent
SLUGS=('niv','ouran','vere','zaho')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((OUT/'final_technical_audit.json').read_text())
assert audit['all_technical_checks_complete']
assert audit['source_contour_gate_failures']==['vere']
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
verdicts={
'niv':{'decision':'frozen_deliverable_candidate_with_minor_notes','deliverable':True,'identity':'二十多岁成年女性、浅肤棕松卷、暖棕衣米领暗绿边。独立表达边界的警醒侧目成立。','improvement':'v2缩短裸颈、眼白收敛；完整轮廓与透明安全边关闭v1触边问题。','residual':'睫眼仍稍大，平行发束高光未完全合并；当前是重绘派生候选。'},
'ouran':{'decision':'frozen_deliverable_candidate_with_minor_notes','deliverable':True,'identity':'四十多岁男性、灰褐乱短发短须、灰外层暖棕内领。警戒侧目与成熟面骨可读，未误读为银发老者。','improvement':'v2眼更窄暗、口线更平、颈缩短；inset确保完整轮廓透明边。','residual':'眉根仍有忧虑、顶部发量和条状高光偏多；保留审慎不安而非声称完全去忧眉。'},
'vere':{'decision':'held_review_candidate_source_edge_clipping','deliverable':False,'identity':'三十多岁女性、棕色松侧辫与尖颌、现卡灰学院袍改制窄领。身份没有新增矛盾。','improvement':'v2短颈和灰领明显优于v1。','residual':'真实源图右侧发束裁边：x1078、y989–1053共65像素alpha>=128。外框padding不修复原始源轮廓。仍有忧眉和眼白/发束细条。','selection':'保留v2作held审阅记录；不回选v1，不追加生成；父于2026-10-15T10:47:42Z明确确认。'},
'zaho':{'decision':'frozen_deliverable_candidate_with_minor_notes','deliverable':True,'identity':'三十多岁成年女性、较宽成熟颌面、暗短发低小束、蓝染工作窄领。轻微不对称闭口保留自尊与记恩。','improvement':'v2显著短颈，嘴角微抬与维芮区分，发块略合并，源轮廓完整。','residual':'小块浅眼白、平行发束和较多顶部透明留白仍留备注；不改变全幅等比派生。'} }
freeze={'schema_version':1,'batch':'batch16','audit_utc':now,'successful_deliverables':['niv','ouran','zaho'],'held':['vere'],'native_pixel_approved':False,'runtime_verified':False,'no_additional_generation':True,'technical_audit':'final_technical_audit.json','technical_reproducibility_pass':True,'source_contour_gate_failures':['vere'],'identity_source_conflict_note':'扎禾卡末孤立他与同卡弧线她冲突；现行CM-MAE及CS-MAE-04多处她与已审女性母版一致。父确认继续成年女性，保留冲突证据不更改卡。','actors':{}}
for slug in SLUGS:
 root=CAMP/slug;manifest=root/'manifest.json';m=json.loads(manifest.read_text());selected=root/m['selected_portrait'];row=dict(verdicts[slug]);row.update(selected_portrait=str(selected.relative_to(CAMP)),selected_sha256=sha(selected),author_status=m['status'],manifest_sha256=sha(manifest),generation_calls=2,source_contour_gate_pass=audit['actors'][slug]['manifest']['selected_raw_source_contour_gate_pass'],source_manifest_sha256=sha(root/'sources/source_manifest.json'),directory_files=[])
 for p in sorted(root.rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:
   row['directory_files'].append({'path':str(p.relative_to(CAMP)),'bytes':p.stat().st_size,'sha256':sha(p)})
 freeze['actors'][slug]=row
(OUT/'freeze_manifest.json').write_text(json.dumps(freeze,ensure_ascii=False,indent=2)+'\n')
(OUT/'final_visual_review.json').write_text(json.dumps({'audit_utc':now,'actual_viewed':'四历史母版、四核心风格、四人v1及v2目标与NN预览、四人v2 raw；维芮右边界另放大实际查看。','actors':verdicts,'technical_is_not_visual_approval':True,'native_pixel_approved':False,'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
board=Image.new('RGB',(1184,560),(58,58,60));d=ImageDraw.Draw(board)
for i,slug in enumerate(('niv','ouran','zaho','vere')):
 row=freeze['actors'][slug];im=Image.open(CAMP/row['selected_portrait']).convert('RGBA');x=i*296
 d.text((x+8,8),slug.upper()+(' / FROZEN CANDIDATE' if row['deliverable'] else ' / HELD - SOURCE CLIP'),fill=(240,240,230) if row['deliverable'] else (255,145,135))
 for j,bg in enumerate(((12,12,15),(105,105,105),(235,235,229))):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(im);board.paste(tile.convert('RGB'),(x+8+94*j,30))
 large=im.resize((296,400),Image.Resampling.NEAREST);board.paste(large,(x,145),large)
board.save(OUT/'final_1x_4x_contact.png')
lines=['# Batch16 独立 QA：3 人冻结候选，1 人 held','',f'审计时间：{now}','', '## 结论','', '- 可交付：尼芙 niv v2_inset、欧岚 ouran v2_inset、扎禾 zaho v2。三人源轮廓完整，保留个别审美残留备注。','- 暂扣：维芮 vere v2。源图右发束真实裁边，父确认本批 held，不回选 v1、不追加生图。','- 四人的 PNG 技术与来源链校验通过，不等于四人轮廓通过。均非原生逐像素终稿，未做游戏整合或运行验收。','', '## 技术证据','', '- 46 份来源记录：当前原件、快照与所记 SHA 全匹配；四人的现卡、母版、旧 QA 与 manifest 也独立匹配 campaign roster。','- 8 份 imagegen 回包：base64 解码、保存 raw 与工具保存原文件逐字节相同；每人恰为初稿加一次修订。','- 10 份派生候选：独立执行整幅 NEAREST、MAXCOVERAGE≤32 色、alpha 128 二值化，输出 PNG 字节复现一致；8x 预览与严格 NN 一致。','- 4 目录 manifest、选中 SHA、全文件清单、SHA256SUMS 均完整通过；详见 final_technical_audit.json。','- 最终目标均为 74×100 RGBA、32 个可见 RGB 色、alpha仅0/255；透明像素 RGB 为0。','', '## 独立目检','']
for slug in ('niv','ouran','zaho','vere'):
 r=freeze['actors'][slug];lines.extend([f'### {slug}：{r["decision"]}',f'- 文件：`{r["selected_portrait"]}`',f'- SHA256：`{r["selected_sha256"]}`',f'- 身份：{r["identity"]}',f'- 改善：{r["improvement"]}',f'- 残留／阻塞：{r["residual"]}',''])
lines+=['## 扎禾身份文字不一致','', '卡的弧线与当前两份台本多处使用“她”，与已审成年女性母版一致；卡末风格守卫单独写“他”。已独立核验并保留证据，依父明确确认按成年女性绘制。现卡蓝染工装优先旧锈红衣领；未改生产人物卡或母版。','', '## 维芮裁边证据与交付边界','', '- `vere_v2_source_edge_blocker.json`：原始源图 SHA、逐像素边界数据、连续65像素alpha≥128。','- `vere_v2_source_edge_evidence.png`：原图边界4x NN诊断，不是修补稿。','- `final_1x_4x_contact.png`：三人可交付与维芮held明确分栏。','- `freeze_manifest.json`：各目录所有文件冻结SHA及选中路径。后续打包应保持这些字节；维芮不得计入成功人数。','- 独立审计仅写本 batch16 目录；未生图、未修改生产卡/代码/旧资产、未提交推送。','']
(OUT/'FINAL_QA.md').write_text('\n'.join(lines))
checks=[]
for slug,row in freeze['actors'].items():
 for item in row['directory_files']:
  p=CAMP/item['path'];checks.append(p.exists() and sha(p)==item['sha256'])
assert all(checks)
print(json.dumps({'successful':['niv','ouran','zaho'],'held':['vere'],'frozen_production_files':len(checks),'freeze_verified':all(checks),'final_report':str(OUT/'FINAL_QA.md'),'freeze_manifest_sha256':sha(OUT/'freeze_manifest.json')},ensure_ascii=False))
