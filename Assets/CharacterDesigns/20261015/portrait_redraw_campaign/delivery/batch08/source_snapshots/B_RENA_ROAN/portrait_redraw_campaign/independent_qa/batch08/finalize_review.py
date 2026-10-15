from pathlib import Path
import json,hashlib,datetime
out=Path(__file__).resolve().parent;camp=out.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
audit=json.loads((out/'frozen_technical_audit.json').read_text())
assert audit['all_technical_checks_complete'],(audit['hard_errors'],audit['pending'])
expected={
'osin':('candidates/portrait_v2_74x100_candidate.png','061e1ac4dd4e1a6c697bc555b1631691171b63ce2c5f955422c19f4c55029ab4'),
'pelan':('candidates/portrait_v2_74x100_candidate.png','6f14f367905ad8d6fbbe77e97fe13d36be6185cdc51d6560a4ac4fc83fe09411'),
'rena':('candidates/portrait_v2_maxcoverage_74x100_candidate.png','b768da21616d3d32004f55fe230f9ab5219eb3f72edc9d55f8b4cab5ef06448d'),
'roan':('candidates/portrait_v2_maxcoverage_74x100_candidate.png','68aa2e58e34899fdf72b3f5e2fdf1b236ccbc0bd6c94197206905de858df12c3')}
notes={
'osin':{'identity_and_current_card':'40多岁秃顶宽脸男班长；棕皮围裙铆钉/橄榄领口。','improvement':'v2连须大块、短颈窄领明显改善，力感与主见保留。','remaining':['眼白仍为较宽赭灰条。','额/颧局部细点仍有。','右侧只有1像素余量，未触边。'],'safe_side_margin_target_met':False},
'pelan':{'identity_and_current_card':'约50岁女住客；成熟眼睑/鼻唇面、发髻、灰褐挺领。','improvement':'v2平眉闭嘴和成熟面较v1自持，侧发收拢。','remaining':['发仍有条束。','少量亮眼缝。','颈还能进一步压短。','右侧2像素余量，低于约3像素目标，未触边。'],'safe_side_margin_target_met':False},
'rena':{'identity_and_current_card':'40多岁女租屋记录员；米白头巾、棕发、深绿罩衣边。','improvement':'v2下颏/领底收紧，克制愧意保留；MAXCOVERAGE保住深绿色。','remaining':['左侧x=0,y=41/42仍有2个发轮廓像素触框，安全边目标未完全达到。','右侧1像素余量。','亮眼缝与条状发纹仍存。'],'safe_side_margin_target_met':False,'frame_contact_persists':True},
'roan':{'identity_and_current_card':'30多岁固执男装配匠；深短发厚须、赭衣与棕皮围裙。','improvement':'v2怒V改较平压眉、脸更大颈更短，MAXCOVERAGE保住眼/衣色分层。','remaining':['眼白仍偏亮。','须发仍有细碎纹。','右侧仅1像素余量，未触边。'],'safe_side_margin_target_met':False}}
selection={'batch':'batch08','reviewed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'selected_candidates_with_limitations','technical_audit_pass':True,'visual_target_fully_met':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False,'new_generation_requested':False,'selected':[]}
frozen={'verified_utc':selection['reviewed_utc'],'technical_audit_sha256':sha(out/'frozen_technical_audit.json'),'actors':{}}
for slug,(path,digest) in expected.items():
 root=camp/slug;m=json.loads((root/'manifest.json').read_text());assert m['selected_portrait']==path;assert sha(root/path)==digest
 ar=audit['actors'][slug]; row=next(x for x in ar['candidates'] if x['path']==path)
 selection['selected'].append(dict(slug=slug,path=str((root/path).relative_to(camp)),sha256=digest,alpha_bbox=row['alpha_bbox'],visible_rgb_colors=row['visible_rgb_colors'],alpha_values=row['alpha_values'],png_byte_identical_reproduction=row['png_byte_identical'],successful_generation_calls=len(ar['raw_integrity']),**notes[slug]))
 frozen['actors'][slug]={'manifest_sha256':sha(root/'manifest.json'),'sha256sums_sha256':sha(root/'SHA256SUMS.txt'),'selected_sha256':digest,'source_hash_checks':len(ar['sources']),'raw_payload_checks':len(ar['raw_integrity']),'candidate_reproductions':len(ar['candidates']),'manifest_file_checks':len(ar['manifest']['file_checks']),'sha256sum_checks':len(ar['SHA256SUMS']),'all_pass':not ar['errors'] and not ar['pending']}
(out/'FINAL_SELECTION.json').write_text(json.dumps(selection,ensure_ascii=False,indent=2)+'\n')
(out/'frozen_verification.json').write_text(json.dumps(frozen,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(frozen,ensure_ascii=False,indent=2))
