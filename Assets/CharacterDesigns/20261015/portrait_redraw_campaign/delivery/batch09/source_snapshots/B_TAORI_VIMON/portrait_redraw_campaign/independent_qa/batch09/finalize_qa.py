from pathlib import Path
import json,hashlib,datetime
OUT=Path(__file__).resolve().parent;CAMP=OUT.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((OUT/'final_technical_audit.json').read_text())
assert audit['all_technical_checks_complete'],audit['hard_errors']+audit['pending']
choices={'sela':'portrait_v1_maxcoverage','sev':'portrait_v2_maxcoverage','taori':'portrait_v2_containment','vimon':'portrait_v2'}
notes={
'sela':{'name':'瑟拉','visual':'成熟侧目轻笑、高马尾和蓝绿双层工作衣成立，脸部大块连贯；保留v1避免不必要重绘。','limitations':['顶部留白7px，裸颈略多。','少量发纹仍较核心理想大面细。']},
'sev':{'name':'塞芙','visual':'唯一v2修复右侧低髻触边，MAXCOVERAGE保住深蓝/米领；眉更平、暗米灰眼白更自然，鼻梁细横纹、成年审视与闭唇成立。','limitations':['裸颈仍略长，发丝分块较多。','保持戒备感，不把审视误作军官权威。']},
 'taori':{'name':'陶芮','visual':'唯一v2显著降肤色饱和、半垂眼和平眉减忧，苍白疲惫与自主克制成立；灰紫粗布和旧毯窄边，没有康复笑或护理者身份。72×98整图NN后居中74×100保住全部发耳。','limitations':['鼻眉阴影略柔，仍不是逐像素原生手绘。','顶部留白5px；小幅技术留边使脸缩小约2.7%，可接受。']},
 'vimon':{'name':'维松','visual':'唯一v2把短剃头皮与浅须从碎纹归并为大面，40多岁窄脸长鼻、平嘴与蓝灰/燕麦衣色保留；按当前卡替换旧束发，无领奖英雄/悔罪暗示。','limitations':['两处小眼白仍偏亮，裸颈仍略长。','头皮平面偏平整；作为候选保留，不追加第三稿。']}}
rows=[]
for slug,v in choices.items():
 a=audit['actors'][slug];path='candidates/'+v+'_74x100_candidate.png';p=CAMP/slug/path
 found=next(c for c in a['candidates'] if c['path']==path)
 assert found['specification_pass'] and found['pixel_reproduction_pass'] and found['png_byte_identical']
 assert a['manifest']['selected']==path and a['manifest']['selected_hash_matches']
 row={'slug':slug,'canonical_id':json.loads((CAMP/slug/'sources/roster_entry.json').read_text())['canonical_id'],'name':notes[slug]['name'],'decision':'candidate_with_notes','selected_candidate':path,'selected_version':v,'selected_sha256':sha(p),'selected_raw':a['manifest'].get('selected_raw') or 'raw/'+v[:11]+'_raw_imagegen.png','production_manifest_sha256':sha(CAMP/slug/'manifest.json'),'production_SHA256SUMS_sha256':sha((CAMP/slug/'SHA256SUMS.txt') if (CAMP/slug/'SHA256SUMS.txt').exists() else (CAMP/slug/'SHA256SUMS')),'visual':notes[slug]['visual'],'limitations':notes[slug]['limitations'],'target_size':found['size'],'visible_rgb_colors':found['visible_rgb_colors'],'alpha_values':found['alpha_values'],'alpha_bbox':found['alpha_bbox'],'successful_generations':len(a['raw_integrity']),'native_authored':False,'native_pixel_approved':False,'runtime_verified':False,'user_approved':False}
 # Version prefix is exactly portrait_v1 or portrait_v2; derived suffixes never imply new generation.
 row['selected_raw']='raw/'+v.split('_',2)[0]+'_'+v.split('_',2)[1]+'_raw_imagegen.png'
 row['selected_raw_sha256']=sha(CAMP/slug/row['selected_raw'])
 rows.append(row)
selection={'batch':'batch09','frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'characters':rows,'independent_qa_gate':'candidate_with_notes_all_technical_checks_pass','native_pixel_approval':False,'runtime_verified':False,'user_approved':False,'generation_limit':'Initial plus at most one necessary imagegen revision per person; technical variants are not extra generations.'}
(OUT/'final_selection.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
gate={'batch':'batch09','status':'PASS_CANDIDATE_WITH_NOTES','frozen_utc':selection['frozen_utc'],'selected_portraits':[{k:r[k] for k in ['slug','selected_candidate','selected_sha256']} for r in rows],'final_technical_audit':'final_technical_audit.json','final_technical_audit_sha256':sha(OUT/'final_technical_audit.json'),'final_selection':'final_selection.json','final_selection_sha256':sha(OUT/'final_selection.json'),'independently_reviewed_raws':sum(len(a['raw_integrity']) for a in audit['actors'].values()),'independent_source_checks':sum(len(a['sources']) for a in audit['actors'].values()),'candidate_derivatives_reproduced':sum(len(a['candidates']) for a in audit['actors'].values()),'raw_tool_bytes_match':True,'all_source_snapshots_match_live':True,'selected_portraits_frozen':True,'taori_containment_derivation':{'raw_source':'taori/raw/portrait_v2_raw_imagegen.png','resize_full_canvas':[72,98],'resampling':'NEAREST','output_canvas':[74,100],'paste_offset':[1,1],'paste_uses_alpha_mask':False,'alpha_threshold':128,'palette':'opaque sampled RGB MEDIANCUT 32 colors, Dither.NONE','transparent_rgb':[0,0,0],'no_crop':True,'no_pixel_repainting':True,'additional_imagegen_call':False},'native_pixel_final':False,'runtime_verified':False,'user_approved':False}
(OUT/'QA_GATE.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2)+'\n')
lines=['# Batch09 独立QA冻结报告','',f"冻结时间：{selection['frozen_utc']}",'','结论：4/4 可交付带备注头像候选。未宣称原生像素手绘终稿、用户验收或游戏内运行完成。','', '## 选稿与视觉结论','']
for r in rows:
 lines += [f"### {r['name']} / {r['canonical_id']}",f"选稿：`{r['slug']}/{r['selected_candidate']}`",f"SHA256：`{r['selected_sha256']}`",r['visual'],'保留意见：'+'；'.join(r['limitations']),f"技术：74×100，{r['visible_rgb_colors']}种可见RGB，alpha仅0/255，bbox={r['alpha_bbox']}。成功生成次数{r['successful_generations']}。",'']
lines += ['## 独立核验','',f"- {gate['independent_source_checks']}条源文件/快照SHA逐一吻合；四角色当前roster、当前人物卡、所选母版及历史manifest核对通过。",f"- {gate['independently_reviewed_raws']}份raw逐字节匹配完整工具返回的image payload及保留的原始生成文件。",f"- {gate['candidate_derivatives_reproduced']}个派生独立重跑，每个像素及PNG文件字节吻合；8x预览均为精确NEAREST。",'- 作者manifest选稿SHA、完整文件清单的SHA/字节数、SHA256SUMS均已独立复核，无缺项或错误。','- 所有最终选稿符合74×100、≤32临时可见色、二值alpha；不以数字合规替代审美。','- 陶芮的containment仅把完整raw最近邻至72×98并放进74×100透明画布(1,1)，再alpha128与32色MEDIANCUT；没有裁切、补画或额外生成。','- 维松左右底边触边均为衣肩，发与耳保持完整。','- 前期initial_technical_audit与first_pair_frozen_audit是生产仍在写入时的检查快照，其中缺文件/生成数差异不是最终gate。最终以QA_GATE.json及final_technical_audit.json为准。','', '## 范围与交付','', '- 实际逐张查看旧母版、四核心、全部新raw及目标1x/8x预览。身份约束与首次集中修订意见见INITIAL_VISUAL_REVIEW.md。','- 只写independent_qa/batch09；未运行作者派生脚本写生产目录，未改人物卡/旧图/代码，不生图，不提交或推送。','- 来源、参数、原始返回、候选与预览由作者目录保留；本目录保留独立复现PNG、审计脚本/报告、冻结选择与对照预览。','']
(OUT/'QA_REPORT.md').write_text('\n'.join(lines))
print(json.dumps(gate,ensure_ascii=False,indent=2))
