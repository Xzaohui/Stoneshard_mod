"""Write independently observed final decisions with exact selected/held hashes."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results={
'beina':{'sha':'9ee071b9643c6305e982e9d163c2035c07c6cbfc55c6009f541e238f0674d4de','eligible':True,
'assessment':'约40岁洗砂住户女性、蓝巾棕发灰罩衣及锈内领保持；鼻翼颧骨与眼袋口周成熟折面明确。v2相对v1缩短裸颈，窄领与脸主体更集中。完整头巾/结尾与发耳实际未裁断，inset仅同raw等比containment改善目标左右余量。仍带担忧眉嘴，但能读出质疑立场，不是无主见儿童或甜脸。',
'limitations':['内眉仍略忧惧、嘴角略低，神态未完全改成平稳坚定','眼白不全暗，发巾仍有平行层；头上透明余量较大，未宣称风格缺口全部清零']},
'anni':{'sha':'1e16522451cd110f00dfd96e835ffca630ecc55ce19f8973102ffcf377471125','eligible':False,
'assessment':'20多岁女性普通当班护理者、棕低髻与米灰素护理领保持。v2确实重新生成完整右侧发轮廓，alpha≥5/16/128四边无接触；v1真实发裁断已解决，暂挂原因不是裁边。v2眼白仍亮且大，上眼线仍强，小鼻与甜脸组织相对四核心成人大鼻颧骨目标仍明显不符，不能把格式通过当风格通过。',
'limitations':['风格暂挂：大亮眼白、妆感上眼线、小鼻甜脸仍主导，未通过四核心系列风格gate','v2真源裁断已修好；不靠inset或padding掩盖裁断。保留完整新raw和inset作证据，不列入交付选稿']}
}
results.update({
'kuen':{'sha':'f5789504824665242a16f5a30ce6bf533168a0b6146dccec3d72449aed2c68c8','eligible':True,
'assessment':'三十多岁苍白成年男性自主患者身份保持；棕乱发、稀胡茬、灰褐厚披肩和灰蓝内领可辨。v2大幅压缩长裸颈与胸，脸部主体、成人鼻翼颧骨和眼下疲惫块面较v1更有力。发耳轮廓在原raw中完整，inset将目标左右余量均增为2px，不补画源轮廓。眉口仍略忧，具体自决与疲惫不等于痊愈或爱情考题。',
'limitations':['眼白仍偏亮、内眉仍略提，未完全达到小暗眼白/平稳眉口目标','胡茬仍有细碎点和锯齿，平行发束仍偏密；仅带限制候选，不能以技术格式宣称纯原生手绘']},
'lint':{'sha':'466434bdc2e245be6716f902080e607ceb2323aefdd2f75686a491600e9d557a','eligible':True,
'assessment':'三十多岁成年女性接收员、短棕发别耳后及素米灰护理领符合最新卡；不沿用旧母图高髻赭裙。方颊明确鼻翼和厚说话嘴保身份。v2脸占幅明显增加，长裸颈收短、衣领更窄，鼻颧骨大面明确。原raw发耳完整，inset仅同raw等比containment，目标左右余量3/2px。略忧眉及亮眼线仍是限制，不是童脸或身份硬错。',
'limitations':['内眉仍略忧、眼白偏亮及上眼线较强，平稳利落表现未完全满足理想','头发仍有平行层和皮肤小折面；窄领不能证明完整护理褂袖扣/随身物已制作']}
})
for s in sys.argv[1:] or list(results):
 e=results[s];path=f'{s}/candidates/portrait_v2_inset_74x100_candidate.png';assert sha(P/path)==e['sha']
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=next(x for x in t['versions'] if x['version']=='portrait_v2');d=next(x for x in v['derivatives'] if x['path']==path)
 out={'batch':35,'slug':s,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'deliverable_as_NN_derived_candidate_with_notes' if e['eligible'] else 'held_style_not_clipping','delivery_eligible':e['eligible'],'selected_path':path if e['eligible'] else None,'selected_sha256':e['sha'] if e['eligible'] else None,'held_evidence_path':None if e['eligible'] else path,'held_evidence_sha256':None if e['eligible'] else e['sha'],'source_raw_sha256':v['raw_sha256'],'comparison_actually_viewed':['full identity mother','Mara/Iwo/Leiya/Tore integer4xNN reference board','v1 raw and 8xNN','v2 raw and full 8xNN','v2 inset 8xNN','v2 inset 1x three backgrounds'],'assessment':e['assessment'],'raw_boundary_thresholds':v['raw_boundary_thresholds'],'source_clipping_decision':'Selected/reviewed v2 raw has no genuine hair/ear cut: alpha>=5/16/128/255 has no border contact. Alpha1 trace spill is not opaque silhouette. Inset cannot repair source clipping and is only a technical containment export. Anni v1 was genuinely clipped and is not selected.','selected_or_held_alpha_bbox':d['alpha_bbox'],'selected_export':'Same v2 raw entire-canvas NEAREST fit72x98 contained within74x100; no crop, synthetic hair/ear extension or facial editing.','limitations':e['limitations']+['仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证'],'single_consolidated_feedback_round':True,'successful_imagegen_results':t['generation_count'],'third_generation_allowed':False,'native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False}
 assert t['generation_count']==2
 (Q/f'{s}_final_visual_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
 print(s,out['status'],e['sha'])
