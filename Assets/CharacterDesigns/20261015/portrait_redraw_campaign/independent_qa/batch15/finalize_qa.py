#!/usr/bin/env python3
"""Freeze the independent batch15 audit; never modifies production assets."""
from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,datetime
OUT=Path(__file__).resolve().parent; CAMP=OUT.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((OUT/'final_technical_audit.json').read_text())
assert audit['all_technical_checks_complete'] and not audit['hard_errors'] and not audit['pending']
labels={'beno':'Beno','doro':'Doro','fil':'Fil','gulan':'Gulan'}
visual={
 'beno':{'decision':'candidate_with_notes','identity':'约30岁成年男性呈现，宽直鼻、深棕发短须、蓝护理衫与白围裙带；现卡与母版无硬冲突。','improvements':'v2眼白降低、须部更成块、颈部有所收短；安全派生留出四边。','remaining':'须发仍有细碎条纹，眉眼略偏忧郁；颈领仍可进一步压窄。'},
 'doro':{'decision':'candidate_with_notes','identity':'40岁成熟女性呈现，紧束黄褐发巾、栗棕发、橄榄衣与赭色围裙带；疲劳护理人身份可读。','improvements':'v2比v1下半脸缩短、圆颊更明显；安全派生恢复完整透明边。','remaining':'上抬内眉和闭嘴下转仍带较强忧色，年龄观感偏熟；裸颈/衣领面积偏多，未完全达到极短颈窄领理想。'},
 'fil':{'decision':'candidate_with_notes','identity':'约50岁旧织街工头，后移发际、宽方脸、灰须、海蓝旧短褂；与古岚浓发长鼻清楚区分。','improvements':'v2亮白眼缝显著压暗，颈部与领口明显缩短，发顶耳缘完整。','remaining':'灰须仍有纵向条束，部分脸颊过渡稍碎；未达到全部人工控色阶/控像素簇的风格终审。'},
 'gulan':{'decision':'candidate_with_notes','identity':'50多岁本地民粮动员者，灰黑浓发后束、长鼻尖颧、浓须、橄榄内衫/粗褐马甲，无军官徽记。','improvements':'v2眼白压暗；同raw安全派生修复目标右边贴边。原raw四边完整，无裁切补画。','remaining':'发须仍有较多长条细分，颈领稍多；目光压暗后偏窄，不当作人工原生像素终稿。'}
}
report={'schema_version':1,'batch':15,'freeze_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':list(labels),'gate':'pass_candidate_freeze_with_notes','held':[],'technical_audit':'final_technical_audit.json','technical_audit_sha256':sha(OUT/'final_technical_audit.json'),'technical_pass':True,'all_current_source_hashes_pass':True,'actual_viewed_identity_and_four_core_references':True,'candidate_native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'maximum_successful_generations_per_actor':2,'total_successful_generations':8,'temporary_palette_ceiling':32,'actors':{},'boundaries':['这是可归档/交付的图像生成重绘候选和等比NN量化派生，不是原生74×100逐像素作者终稿。','32色为本批临时上限，不能代表项目统一调色板或色阶已通过风格终审。','每人初稿加一次必要修订；技术安全留边从同一v2 raw导出，不新增生图、补画或第三轮创作。','源母版、当前人物卡、正式代码和游戏运行素材未改；未进行游戏接入/实机验收。','早期technical_audit是工作中快照，最终以final_technical_audit和本gate为准。']}
for n in labels:
 a=audit['actors'][n];m=a['manifest'];candidate=CAMP/n/m['selected'];cm=next(c for c in a['candidates'] if c['path']==m['selected'])
 assert sha(CAMP/n/'manifest.json')==m['sha256'] and sha(candidate)==m['selected_actual_sha256']
 report['actors'][n]={'candidate':str(candidate.relative_to(CAMP)),'candidate_sha256':sha(candidate),'production_manifest':n+'/manifest.json','production_manifest_sha256':sha(CAMP/n/'manifest.json'),'production_checksums':n+'/SHA256SUMS.txt','production_checksums_sha256':sha(CAMP/n/'SHA256SUMS.txt'),'selected_preview':n+'/previews/'+candidate.stem.replace('_74x100_candidate','_1x_8x')+'.png','dimensions':cm['size'],'visible_rgb_colors':cm['visible_rgb_colors'],'alpha_values':cm['alpha_values'],'alpha_bbox':cm['alpha_bbox'],'four_edges_transparent':m['selected_four_borders_transparent'],'raw_tool_payload_exact':all(x['raw_equals_tool_payload_bytes'] for x in a['raw_integrity']),'all_source_hashes_exact':all(x['hash_matches'] for x in a['sources']),'png_byte_reproduction':cm['png_byte_identical'],'pixel_reproduction':cm['pixel_reproduction_pass'],'reproduced_png_sha256':cm['reproduced_sha256'],'independent_derivation_matches':cm['independently_matching_methods'],'preview_8x_exact':cm['preview_exact_8x_nearest_neighbor'],'successful_image_returns':len(a['raw_integrity']),'visual_review':visual[n]}
board=Image.new('RGB',(1272,940),(76,76,76));d=ImageDraw.Draw(board)
d.text((16,14),'BATCH15 / SELECTED TECHNICAL CANDIDATES / 4x NN + 1x display',fill='white')
d.text((16,36),'All 74x100 / <=32 visible RGB / binary alpha / generated redraw derivatives; not native pixel-art final approval',fill='white')
for i,n in enumerate(labels):
 x=16+i*312;rec=report['actors'][n];im=Image.open(CAMP/rec['candidate']).convert('RGBA')
 d.text((x,68),labels[n]+' / '+str(rec['visible_rgb_colors'])+' colors',fill='white');big=im.resize((296,400),Image.Resampling.NEAREST);board.paste(big,(x,92),big)
 for j,bg in enumerate([(18,18,22),(100,100,100),(235,232,227)]):
  t=Image.new('RGBA',(74,100),bg+(255,));t.alpha_composite(im);board.paste(t.convert('RGB'),(x+j*96,516))
for i,n in enumerate(['mara','iwo','leiya','tore']):
 x=16+i*312;d.text((x,650),'Style reference only: '+n,fill='white');im=Image.open(CAMP/'beno/sources'/f'{n}_style_reference.png').convert('RGBA').resize((148,200),Image.Resampling.NEAREST);board.paste(im,(x,676),im)
d.text((16,910),'Beno / Doro / Gulan use same-raw 72x98 contained safe export. Source cards and identity masters preserved.',fill='white');board.save(OUT/'selected_contact_4x_1x.png')
(OUT/'QA-independent.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
lines=['# Batch15 独立验收冻结','',f"冻结时间：{report['freeze_utc']}",'','结论：四人可作为带已知风格局限的重绘候选归档和交付；无身份/性别硬冲突 held。不是原生像素终稿或游戏验收。','','## 逐人终选']
for n in labels:
 r=report['actors'][n];v=visual[n];lines += ['',f"### {labels[n]}",f"- 文件：`{r['candidate']}`",f"- SHA-256：`{r['candidate_sha256']}`",f"- 规格：74×100；{r['visible_rgb_colors']}种可见RGB；alpha 0/255；四边透明；raw字节与完整工具返回一致；独立导出PNG逐字节复现。",'- 身份：'+v['identity'],'- 改善：'+v['improvements'],'- 保留局限：'+v['remaining']]
lines += ['','## 验收范围','', '已实际查看四名角色母版、现行人物卡和 Mara/Iwo/Leiya/Tore 四核心参考；看过全部v1/v2的1x与整数NN图，安全版另行复看。逐条校验当前来源和存档副本SHA、完整工具返回解码raw字节、派生PNG字节、8x预览和生产manifest/SHA库存。每人两张成功生成，共8张。贝诺与多罗另有一次六参考参数校验拒绝记录，没有生成图像，不计入成功生成数。',''] + ['- '+x for x in report['boundaries']]
(OUT/'README.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'gate':report['gate'],'actors':{n:{k:v[k] for k in ['candidate','candidate_sha256','production_manifest_sha256','visible_rgb_colors']} for n,v in report['actors'].items()}},ensure_ascii=False,indent=2))
