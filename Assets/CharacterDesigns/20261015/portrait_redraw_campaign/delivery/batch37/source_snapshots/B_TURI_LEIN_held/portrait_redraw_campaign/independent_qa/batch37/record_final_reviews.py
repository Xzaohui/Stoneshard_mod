"""Write visual decisions from actual full raw, 1x, 4x/8x NN viewing.
No generation, retouching, or edits outside independent_qa/batch37.
"""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
decisions={
 'aro':{
  'tag':'portrait_v2','sha256':'e5a2cf8486261fff5a28f6106615891c67c39f0e9dea024780f4b29e646cb164','eligible':True,
  'findings':['成熟眼袋与鼻唇结构已补足约40岁读感，保持宽颧短宽鼻和颈后短辫。','眼白已缩暗，鼻颧大块、深色窄领符合当前卡；不延用旧橄榄宽披。','发顶、耳廓、短辫完整；raw alpha≥5 bbox [45,123,1050,1370]，1079×1458画布留真实四侧余量。'],
  'limits':['内眉仍略忧、颈部稍长，未达到完全沉静短颈的理想。','发束仍有平行层，1x个别皮肤折面小碎点；不以32色格式宣称风格零缺口。']},
 'gura':{
  'tag':'portrait_v2_inset','sha256':'1626640c4a14b9e39306b817f95e94dc2298315c4f5c0b9b3e32fe239e19e8d5','eligible':True,
  'findings':['三十多岁女性维护工、棕低髻与灰厚褂窄领保留；额竖纹消除，眼白缩暗，认真而独立。','脸占画面主体，鼻颧大块与紧嘴可读；灰领已简化，不添加工约承诺。','raw alpha≥5 bbox [16,113,1069,1404]，1079×1457四侧仍有真实空隙，发耳没有观察到实际裁断。inset仅整图containment；没有画回或补造轮廓。'],
  'limits':['内眉仍略V形、发丝平行层仍可见。','raw左右余量仅16/10源像素，源边距偏窄；inset增加目标透明格不代表满足原提示词的宽源边距要求。']},
 'lein':{
  'tag':'portrait_v2_inset','sha256':'7e1d2ba859c3656cd812b6e3f318665b4faf295c8cc14c422f113aa63a4298a6','eligible':False,
  'findings':['v2眉眼较平、眼白变暗、短颈窄绿领与粗鼻颧改善；成年女向导、软棕帽和同一截粉笔身份成立。','但v2 raw右界 alpha≥5有108像素、≥16有69像素，集中上段y769..847；最大右界alpha47，α≥128右界计数0，主体仅在x1084结束。不是全不透明边界裁断，也不只是目标NN采样贴边。','实际浅底3x边界裁片显示深发沿源右界呈直立结束；真实透明余量缺失，不能独立证明外层发廓完整。inset不能恢复缺失源空间，因此暂挂。','v1源图未见真裁断，但亮大眼白、抬内眉焦虑和较长颈领风格未达门槛，不回选v1。'],
  'limits':['源轮廓/真实余量门槛未过，selected=null，v2_inset仅保留审查证据，禁止进入交付选稿。','眼白仍不全暗、上眼线和发层仍强；风格改善不能抵消源边界风险。']},
 'turi':{
  'tag':'portrait_v2_inset','sha256':'995312565126d56e0fa4dc9d57e1741eadcaaf3277e7f53c4a8b8478290a1d2f','eligible':True,
  'findings':['约40岁精瘦男检查匠、窄脸灰鬓短灰须及橄榄/米白领成立；不误作全山保证者。','v2明显缩短颈部收窄披领，粗鼻颧和成熟脸保留，认真估量的微启嘴可读。','raw alpha≥5 bbox [25,35,1066,1423]，1079×1458四边真实空隙。发尖、侧发与耳完整，inset为同raw等比NN技术派生。'],
  'limits':['眼白仍偏浅、内眉稍忧，未完全达到小暗眼白目标。','发与灰鬓仍有平行长层，短须局部碎点；只作带限制候选。']}
}
for s,d in decisions.items():
 rel=f"{s}/candidates/{d['tag']}_74x100_candidate.png";assert sha(P/rel)==d['sha256']
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=next(x for x in t['versions'] if x['version']=='portrait_v2');der=next(x for x in v['derivatives'] if x['path']==rel)
 record={'slug':s,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'deliverable_as_NN_derived_candidate_with_notes' if d['eligible'] else 'held_source_contour_margin_and_style','delivery_eligible':d['eligible'],'selected_path':rel if d['eligible'] else None,'selected_sha256':d['sha256'] if d['eligible'] else None,'held_evidence_path':None if d['eligible'] else rel,'held_evidence_sha256':None if d['eligible'] else d['sha256'],'actually_viewed':['full selected mother raw','four core references in exact4xNN board','v1 and v2 full raw','v1 and v2 8x NN','final variant 1x and 4x backgrounds']+(['right raw boundary exact3xNN pale composite'] if s=='lein' else []),'findings':d['findings'],'limitations':d['limits']+['仅74×100 NN技术派生候选，非原生逐像素终稿；未集成游戏、未实机验证。'],'raw_sha256':v['raw_sha256'],'raw_size':v['raw_size'],'raw_boundary_thresholds':v['raw_boundary_thresholds'],'candidate_alpha_bbox':der['alpha_bbox'],'byte_reproduced':der['byte_reproduction'],'successful_generations':t['generation_count'],'parameter_rejections_without_image':t['preflight_rejections_without_image'],'consolidated_feedback_rounds':1,'third_generation_allowed':False,'native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False}
 (Q/f'{s}_final_visual_review.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print('Final visual decisions: ARO, GURA, TURI eligible with notes; LEIN held.')
