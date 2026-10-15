"""Freeze independent audit outputs only after production owners freeze their selections."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
OUT=Path(__file__).resolve().parent;CAMPAIGN=OUT.parent.parent;REPO=CAMPAIGN.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slugs=['avi','daran','elen','hase']
versions={'avi':'portrait_v2','daran':'portrait_v2_maxcoverage','elen':'portrait_v2','hase':'portrait_v1'}
notes={
'avi':{'improvements':'蓝头巾、赭色改制男式短褂与三十多岁身份清楚。v2脸更大、裸颈更短、鬓发成束且眼白压暗；较饱满面颊和较少纹路区别达兰，直接稍不耐烦的审视可读。','residuals':'眉心仍偏强硬，宽头巾占据较多上部空间；不称彻底消除共享眉形。'},
'daran':{'improvements':'BRY-NPC-DARAN约40岁结实女板材商、亡者姐姐身份明确，非dalan。v2下巴与领口收紧、成熟法令和反问/克制失落可读。MAXCOVERAGE保回raw已有的短灰白粉笔和苔绿领，避免粉笔变肤色。','residuals':'灰奶色眼白比MEDIANCUT版更亮，法令/眼下纹理与忧眉仍较明显；这是保小面积职业色的技术取舍。'},
'elen':{'improvements':'BRY-NPC-ELEN约40岁女性装帧修复者，非aren男性逃兵。窄椭圆脸、长鼻、棕色低髻及酒红/深灰工作领成立；v2高领和短颈明显改善，眼白压暗，审视更集中。','residuals':'内眉仍有轻微焦虑折角，未完全脱离核心参考的严肃眉模板；发束仍有细阶梯边。'},
'hase':{'improvements':'BRY-NPC-HASE约40岁男性医药商品代理。圆卷发、紧凑厚须、偏侧礼貌浅笑及温和却计算的目光成立，深绿商褂可读；无医生/官方药师或疗效保证暗示。v1已足以作候选，未消耗不必要修订。','residuals':'颈侧稍长，须边有少量细点与尖角；不称完全纯大块设计。'}}
roster=json.loads((CAMPAIGN/'campaign_roster.json').read_text());r={c['suggested_slug']:c for c in roster['characters'] if c.get('suggested_slug') in slugs}
audit=json.loads((OUT/'independent_measurements.json').read_text());a={c['slug']:c for c in audit['characters']}
assert all(s['hash_match'] for s in audit['source_checks'])
selection=[]
for slug in slugs:
 root=CAMPAIGN/slug;manifest=json.loads((root/'manifest.json').read_text());selected=f'candidates/{versions[slug]}_74x100_candidate.png'
 assert manifest['selected_portrait']==selected
 c=a[slug]
 for flag in ['manifest_all_file_hashes_match','manifest_inventory_complete','source_copies_all_match','sha256sums_all_match','generation_call_count_matches','roster_entry_copy_equal','within_two_generation_limit']:assert c[flag],(slug,flag)
 assert c['manifest_sha256']==sha(root/'manifest.json')
 for m in c['candidates']:assert m['technical_pass'] and m['independent_PNG_bytes_equal'] and m['raw_equals_original_generated_bytes']
 target=next(m for m in c['candidates'] if m['target']['path']==str((root/selected).relative_to(REPO)))
 assert target['target']['sha256']==sha(root/selected)
 selection.append({'slug':slug,'canonical_id':r[slug]['canonical_id'],'name':r[slug]['name'],'selected_path':str((root/selected).relative_to(REPO)),'selected_sha256':sha(root/selected),'manifest_sha256':sha(root/'manifest.json'),'manifest_file_count':len(manifest['files']),'visible_RGB_colors':target['target']['visible_rgb_colors'],'status':'candidate','technical_pass':True,'visual_review':notes[slug],'native_final':False,'runtime_integrated':False})
raws={m['raw']['path']:m for c in audit['characters'] for m in c['candidates']}
exports=[m for c in audit['characters'] for m in c['candidates']]
final={'freeze_verified_utc':datetime.now(timezone.utc).isoformat(),'batch_id':'batch05','approved_for_packaging':True,'selection':selection,'scope_limit':'Packaging readiness only; not user-approved final art, native pixel authorship or runtime verification.','QA_report':'QA_REPORT.md','measurements':'independent_measurements.json','independently_reproduced_export_count':len(exports),'raws_equal_tool_return_and_original_generated_count':len(raws),'all_source_checks_pass':True,'all_manifest_checks_pass':True,'all_manifest_inventories_complete':True,'all_SHA256SUMS_checks_pass':True,'nonrendering_parameter_events':sum(len(c['separately_recorded_nonrendering_events']) for c in audit['characters'])}
(OUT/'final_selection.json').write_text(json.dumps(final,ensure_ascii=False,indent=2)+'\n')
lines=['# Batch05 独立头像候选验收','',f"冻结后复验：{final['freeze_verified_utc']}",'','## 结论','','4人均为candidate，可打包送审；无fail选稿。此结论不等于原生逐像素终稿、用户最终认可或游戏内验收。','','| 人物/稳定ID | 选稿 | 可见RGB色 | 候选SHA256 |','|---|---|---:|---|']
for e in selection:lines.append(f"| {e['name']} / {e['canonical_id']} | {versions[e['slug']]} | {e['visible_RGB_colors']} | {e['selected_sha256']} |")
lines+=['','## 实际视觉审阅','','已读现人物卡及关联台本关键内容、AGENTS，实际查看四个身份母版、玛拉/伊沃/蕾雅/托雷四认可风格锚；逐版本看74×100和最近邻放大稿。用现卡明确年龄/性别/衣装校正旧图，而不因历史卡SHA变化自动否定身份。']
for slug in slugs:lines+=['',f"### {r[slug]['name']} / {slug}",'',notes[slug]['improvements'],'','残留：'+notes[slug]['residuals']]
lines+=['','## 修订与取舍','','Avi/Daran/Elen均初稿加一次必要实质重绘；Hase初稿已符合候选要求，仅用1次生成。两位女性v1的长颈/共享忧眉与达兰肤色粉笔问题有记录，未把历史初稿或技术派生额外计为新人。达兰同一v2 raw另导MAXCOVERAGE版，仅改量化算法，采样、几何和alpha一致，无手涂。','','Elen另有一次参考图片数量超过5的入参校验错误，发生在生成之前，记录于其qa/portrait_v2_parameter_validation.json；不算额外生成，不是安全阻断。','','## 独立技术与来源核验','',f'- {len(raws)}份唯一raw逐字节等于完整tool-return的image_url解码内容，也等于对应原生成文件。',f'- {len(exports)}份74×100候选导出均由独立脚本重实现，RGBA与PNG字节完全一致；未运行作者脚本来代替独立复现。','- 全部导出为≤32可见RGB色、alpha只含0/255；32为临时上限，不证明原生调色设计。','- Avi/Daran：alpha≥128外接框裁切，等比NN fit72×98居中置于74×100，阈值128，MEDIANCUT（达兰选稿MAXCOVERAGE），无抖动。','- Elen/Hase：全画布NN到74×100，阈值128，32色MEDIANCUT，无抖动。','- 全部人物现卡/历史母版/历史选稿证据与名册SHA一致；source_manifest快照逐字节相等，roster_entry与现名册语义一致。','- 冻结后重验所有manifest列项SHA/字节、清单完整性和SHA256SUMS全通过；选稿与最终manifest明确一致。','- independent_measurements.json保留alpha外接框、透明RGB、连通分量、各导出和raw哈希等明细。','','## 交付边界','','只交四个选定的imagegen重绘后技术降采样/量化头像候选。旧图原样保留。未编辑生产图、现人物卡或代码，未生成新游戏包、未集成、未push。候选紧脸、骨相、年龄与服装读数已改善，但共享严肃眉式、量化色彩取舍及少量细发须仍需用户审美判断；不得将技术全过表述成原生完成。','','## 审计文件','','- final_selection.json：冻结选稿和manifestSHA','- independent_measurements.json：来源/清单/原返回/独立复现明细','- review_basis.json、preflight_source_checks.json：身份及风格依据','- revision_feedback.md：一次集中修订意见','- selected_candidates_1x_4x.png、comparison_manifest.json：仅NN拼版，无生产像素修改','- audit_measurements.py、reproduction_config.json：独立复现实验','- QA_FILE_INVENTORY.json、SHA256SUMS.txt：审计输出冻结清单']
(OUT/'QA_REPORT.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({'candidate_count':len(selection),'exports':len(exports),'raws':len(raws),'selection':[(e['slug'],e['selected_sha256']) for e in selection]},ensure_ascii=False,indent=2))
