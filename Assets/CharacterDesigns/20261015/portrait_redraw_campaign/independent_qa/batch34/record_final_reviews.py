"""Record actual final visual decisions, not inferred technical approval."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
selected={
 'mano':'2bae88536962d009ebb40ed6476a4d1344e5d62d9e4ca6e75b71ae50a9fae7b6',
 'qiduo':'7be587908584abd2d86a77b7f6e8c41e94008429a94e6a935153eb35caa69a25',
 'xijie':'423e64fb078e27cf10bef5712e6d6403899c874633e1034c58f10c40fd9d2a08',
 'aiqin':'a987c64d2f276a3bf4597934f6657d3fc165f57f7e0631048d353f6dd438c285'
}
assessment={
 'mano':'约50岁女性班长成熟度成立，稀眉相对v1明显减淡，棕布帽/暗棕后束发和赭黄厚工衣窄圆系领保持。v2缩短裸颈胸并放大脸部，鼻颧骨和口边年龄折面更清楚。full在左右各仅1px，inset真实同raw等比采样后左右各2px；帽发耳全部完整。仍留少许担忧眉口及细平行发帽层，非理想化终稿。',
 'qiduo':'三十多岁成年兄长与伤矿工身份成立，宽颊短钝鼻、眼袋、矿尘灰棕短发、灰棕工衣小系扣可辨。v2短颈窄领和脸占幅有效改善，胡须大簇较v1集中。完整耳发与自决疲惫保持，不推导伤愈/复井。inset同raw等比导出使右余量2px，源图未真裁断。',
 'xijie':'约40岁成年女性井段检查匠，高额长椭圆脸、长直鼻、窄眼薄嘴及短低辫保持。v2大幅改善v1脸占幅偏小和长裸颈，窄橄榄内领与棕皮护领遵当前卡。沉着独立与明确年龄可读；inset保发辫耳完整且目标右2px，仍有偏亮眼白和较多平行发束。',
 'aiqin':'三十多岁成年女性与祁铎之妹可读，宽圆颊短鼻、中分暗棕后梳低辫保持；改小父亲褪蓝工装以窄工作领呈现，未沿用旧裙披巾。v2宽大脸、短颈窄领、大鼻颧骨块较v1清楚，眼白比v1压暗。眉口仍略忧郁，尚非充分平静自控；不推导家族和解/复仇或官职。inset右2px，源发辫完整。'
}
limitations={
 'mano':['内眉仍略带担忧；raw中少量亮眼点和平行帽发层未完全消除','当前卡L17她/L40他孤立代词冲突原文与SHA完整保留；依父任务明确允许及母图母QA女性证据继续女性，不修改源卡'],
 'qiduo':['唇上与下颌仍有细点/锯齿胡茬，眼白偏亮、眉略厚于母QA薄平眉；不声称全部风格缺口清零','伤与去留是台本条件，紧脸裁幅没有呈现护腕/腿伤不等于伤愈或同意复井'],
 'xijie':['眼白仍偏亮、上眼线与平行发束比四核心粗簇目标更醒目；只准带限制候选','最新卡旧皮护具覆盖历史橄榄衣短围裙，窄领不能展示全身皮护磨损、锤与记录板'],
 'aiqin':['眉口仍略忧郁，原raw眼白不全暗、头发仍有平行层；没有宣称克制旧怒的表现已完美','最新卡改小父亲旧工装覆盖历史蓝裙披巾，紧脸不表现手茧、卷袖、腰扳手或工作牌']
}
for s,h in selected.items():
 path=f'{s}/candidates/portrait_v2_inset_74x100_candidate.png';assert sha(P/path)==h
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=next(x for x in t['versions'] if x['version']=='portrait_v2')
 derivatives=[x for x in v['derivatives'] if x['path']==path];assert len(derivatives)==1
 out={'batch':34,'slug':s,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'deliverable_as_NN_derived_candidate_with_notes','delivery_eligible':True,'selected_path':path,'selected_sha256':h,'source_raw_sha256':v['raw_sha256'],'comparison_actually_viewed':['selected mother image','Mara/Iwo/Leiya/Tore integer4x reference board','v1 raw and 8x NN','v2 raw and full 8x NN','v2 inset 8x NN'],'assessment':assessment[s],'raw_boundary_thresholds':v['raw_boundary_thresholds'],'source_clipping_decision':'No genuine source hair/ear cutting. Alpha>=5/16/128/255 has zero border contact. Alpha1 edge spill, where present, is explicitly distinguished from an opaque silhouette cut. Inset cannot and does not repair source clipping.','selected_alpha_bbox':derivatives[0]['alpha_bbox'],'selected_export':'Same v2 raw entire-canvas NEAREST fit 72x98 contained within 74x100; no crop, synthetic hair/ear padding or facial editing.','limitations':limitations[s]+['仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证'],'single_consolidated_feedback_round':True,'successful_imagegen_results':2,'third_generation_allowed':False,'native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False}
 (Q/f'{s}_final_visual_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Four visually reviewed v2_inset candidates SHA-locked with explicit limitations.')
