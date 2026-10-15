from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib,datetime
O=Path(__file__).resolve().parent; C=O.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selected={'emo':'portrait_v2_maxcoverage_74x100_candidate.png','kien':'portrait_v2_74x100_candidate.png','kona':'portrait_v2_74x100_candidate.png'}
names={'emo':'埃墨·衬','kien':'奇恩','kona':'科纳'}
notes={'emo':'少量约2px眼白、帽部细纹仍可见；已保暖棕肤、卷发亚麻帽、成熟清瘦脸及蓝灰窄领。','kien':'沙发仍有少量平行细簇、嘴角偏急；宽厚下颌与短颈已显著改善，符合现卡40岁敦实成年。','kona':'谨慎眉势与颈部斜亮面仍略突出；平内眉、短颈窄领改善，30多暗波发短须及深蓝领成立。'}
report=json.loads((O/'frozen_technical_audit.json').read_text());assert report['all_technical_checks_complete'],report['pending']+report['hard_errors']
held=json.loads((O/'hel_frozen_held_verification.json').read_text());assert held['all_sha256sums_pass'] and held['generation_calls']==held['tool_returns']==held['raw_pngs']==held['candidate_pngs']==0
records=[]
for s,file in selected.items():
 p=C/s/'candidates'/file; a=report['actors'][s];m=a['manifest'];assert m['selected']==str(p.relative_to(C/s)) and m['selected_hash_matches']
 row=next(x for x in a['candidates'] if x['path']==str(p.relative_to(C/s)))
 assert row['png_byte_identical'] and row['specification_pass'] and row['preview_exact_8x_nearest_neighbor']
 records.append({'slug':s,'canonical_id':'ALD-NPC-'+s.upper(),'name':names[s],'selected':str(p.relative_to(C)),'sha256':sha(p),'decision':'candidate_with_notes','visual_note':notes[s],'native_pixel_approved':False,'runtime_verified':False,'generation_calls':len(a['raw_integrity']),'size':row['size'],'visible_rgb_colors':row['visible_rgb_colors'],'alpha_values':row['alpha_values'],'alpha_bbox':row['alpha_bbox'],'pixel_reproduction_pass':True,'png_byte_identical':True,'edge_clipping':False,'independent_actual_pixel_review':True})
selection={'review_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'batch':'batch12','qualified_candidate_count':3,'held_count':1,'selected':records,'held':{'slug':'hel','name':'赫莲·金','canonical_id':'ALD-NPC-HEL','status':'blocked_source_conflict','generation_calls':0,'qualified':False,'reason':'当前卡明确女性代词，与锁定历史男性短须母版及历史QA真实冲突，等待身份决定。'},'global_boundary':'Imagegen redraw + NN/limited-palette derivative candidates; not native pixel authorship or runtime approval.','all_available_technical_checks_pass':True}
(O/'FINAL_SELECTION.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
board=Image.new('RGB',(1020,850),(72,72,76));d=ImageDraw.Draw(board);d.text((20,14),'BATCH 12 | 3 PORTRAIT CANDIDATES + HEL HELD | Independent visual/byte QA',fill='white');d.text((20,34),'Top: 1x on dark / gray / light. Main: exact 4x NEAREST. Non-native candidates.',fill=(220,220,220))
for i,r in enumerate(records):
 x=20+i*335; im=Image.open(C/r['selected']).convert('RGBA');d.text((x,65),r['slug'].upper()+' / '+str(r['visible_rgb_colors'])+' colors / candidate with notes',fill='white')
 for j,bg in enumerate([(15,15,18),(108,108,108),(235,235,229)]):
  tile=Image.new('RGBA',(74,100),bg+(255,));tile.alpha_composite(im);board.paste(tile.convert('RGB'),(x+j*95,89))
 zoom=im.resize((296,400),Image.Resampling.NEAREST);board.paste(zoom,(x,210),zoom)
d.text((20,635),'HEL: HELD SOURCE CONFLICT | 0 generations | excluded from qualified count',fill=(246,200,125))
d.text((20,660),'Four core style anchors below (1x); style only, never identity replacements.',fill=(225,225,225))
for i,key in enumerate(['mara','iwo','leiya','tore']):
 im=Image.open(C/'emo/sources'/f'{key}_style_reference.png').convert('RGBA');x=20+i*120;d.text((x,686),key.upper(),fill='white');board.paste(im,(x,705),im)
d.text((525,706),'Emo: mature slender face, linen cap, warm brown skin',fill='white');d.text((525,730),'Kien: age 40, sturdy jaw, sandy hair, clean-shaven',fill='white');d.text((525,754),'Kona: thirties, broad face, short beard, navy collar',fill='white');d.text((525,788),'No old assets replaced. No game/runtime acceptance.',fill=(225,225,225))
board.save(O/'selected_candidates_1x_4x.png')
(O/'comparison_manifest.json').write_text(json.dumps({'inputs':[{'path':r['selected'],'sha256':r['sha256']} for r in records],'output':'selected_candidates_1x_4x.png','sha256':sha(O/'selected_candidates_1x_4x.png'),'transform':'RGBA composites over flat backgrounds; whole-canvas exact 4x NEAREST; labels only; no pixel edits'},indent=2)+'\n')
sources=json.loads((O/'preflight_source_checks.json').read_text());n_sources=sum(len(x['source_checks']) for x in sources['actors'].values());n_outputs=sum(len(x['candidates']) for x in report['actors'].values())
text=f'''# Batch12 独立终审\n\n结论：3张可交付候选，1人身份冲突暂挂。全部仍为非原生终稿的对白头像候选，未入游戏验收。\n\n## 选稿\n\n'''
for r in records:
 text+=f"- {r['name']}（{r['canonical_id']}）：`{r['selected']}`。{r['visible_rgb_colors']}色，SHA256 `{r['sha256']}`。{r['visual_note']}\n"
text+='''\n三张已实际查看原图、74×100及1×/8×最近邻预览，并与四核心风格锚比较。均为紧脸、短颈窄领、整齐鼻颧骨块面，帽/发/耳未因放大被裁。三人面型、发色、帽/胡须与表情可区分。当前卡的年龄体貌服装优先于旧视觉假设：埃墨40多、奇恩40敦实、科纳30多深蓝短褂。初稿问题均集中反馈，每人仅一次生图修订。\n\n## 赫莲·金暂挂\n\nALD-NPC-HEL：现卡“她的尺只量本件”与所锁历史短须成年男性母版/历史QA构成真实冲突；来源SHA相符，非文件误配。保持blocked_source_conflict，生图0、候选0，不计合格。等待父任务/用户身份决定。没有重画、改卡或覆盖旧图。这是来源身份冲突，并非安全阻断。\n\n## 独立技术检查\n\n'''
text+=f'''- 当前卡、母版、历史QA/manifest、四核心与脚本来源共{n_sources}份源快照的原件/快照/SHA相符；另核名册锁定身份源。\n- 6份成功工具返回与raw逐字节相等，工具输出原文件仍在且相等；每人恰好2次，赫莲0次。\n- 独立从raw重建全部{n_outputs}份74×100候选，像素与保存后的PNG字节均一致；所有8×预览确为NEAREST。\n- 所选埃墨32色、奇恩32色、科纳30色；alpha均仅0/255，无框边不透明像素，无透明RGB污染。\n- 埃墨v2使用72×98安全域等比例NN并MAXCOVERAGE无抖动32色，保蓝灰小领。奇恩v2使用整图74×100 NN fit并MEDIANCUT；科纳v2使用72×98安全域等比例NN及MEDIANCUT，保留完整发耳。没有剪裁/拉伸/局部手绘。\n- 全部作者manifest文件、明确选稿SHA与SHA256SUMS再次核验通过。赫莲冻结包全SHA通过，生成与候选计数均为0。\n\n## 边界\n\n≤32色是临时候选色数上限，不是全局锁定调色板。统计通过不代替上述视觉判断。未证明原生逐像素作者工作、装备兼容、运行导入或用户终稿批准。独审只写本batch12目录，未修改人物生产文件、故事卡、旧资产或代码，未提交/推送。\n\n证据入口：`FINAL_SELECTION.json`、`frozen_technical_audit.json`、`preflight_source_checks.json`、`hel_frozen_held_verification.json`及`selected_candidates_1x_4x.png`。\n'''
(O/'FINAL_REVIEW.md').write_text(text)
print(json.dumps({'qualified':3,'held':1,'sources':n_sources,'candidate_exports':n_outputs,'selected':records},ensure_ascii=False,indent=2))
