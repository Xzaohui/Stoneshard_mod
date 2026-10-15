"""Persist human visual judgments; does not infer aesthetic approval from metrics."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reviews={
 'ruya':{
  'expected_sha256':'6d1ac8737309fcc958086a2208817372d2129bd93c1207a691037d6bba61844b',
  'visual_assessment':'实际查看v2 raw、74×100三背景1x及8xNN；暗棕长辫、暖肤、紧眉警觉闭嘴和深蓝外褂领保住三十多岁有限采购经手者。小眼白由大片亮白收为小暗块，眼眶与大鼻颧更硬，面部占比增大，颈明显缩短，窄领下收。与苏槿头巾宽脸的50岁身份可区分。',
  'limitations':['原始左右实体透明余量13/25px，仍较紧；74×100主体bbox(1,5,72,96)，窄边留存。','头发及脸部仍有少量细碎量化色块，非原生逐像素人工终稿。','NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。'],
 },
 'sujin':{
  'expected_sha256':'5b196320ec4770973ba897c659e8bd35dbd187ace3449859373988d6e5127e08',
  'visual_assessment':'实际查看v2 raw、74×100三背景1x及8xNN；灰棕短发土灰头巾、深绿磨旧工装和宽脸约五十岁弓材匠成立。眼白缩暗，眼袋/鼻唇/下颌年龄大块强化，沉静哀伤防卫紧嘴保住；颈和露上胸较v1明显缩紧，头巾结/耳/发轮廓完整。',
  'limitations':['原始左右实体透明余量10/18px，仍较紧；74×100主体bbox(1,7,73,89)，窄边留存。','头巾体量偏大，裸颈仍略显长；作为带限制候选保留，不继续第三次生成。','NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。'],
 },
 'suoya':{
  'expected_sha256':'5e73bc68655674b727afb39acdfa107bab7ecf92dc3c03fe69c954b106444437',
  'visual_assessment':'实际查看v2 raw、full/inset的三背景1x及8xNN；选择full保大脸。面部下半与鼻颧更有体块，颈与衣领明显收紧。棕发、三十多岁风雪纹、本人左眉断口（画面右侧眉外段）、棕猎衣暗橄榄领和闭嘴警惕身份成立；不将母图旧风格研究未通过改写为已通过。',
  'limitations':['原始左右实体透明余量13/11px，仍较紧；74×100主体bbox(1,3,73,97)，不是源真裁断。','眼白仍可更收敛，头发体量偏大；full优先脸部占比，已有inset只作未选技术派生。','NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。'],
 },
 'ousha':{
  'expected_sha256':'80cdadb272f181747fb6eca76f24e46d79c2f88bd74fabdf47b21188052c7251',
  'delivery_eligible':False,
  'status':'held_style_not_deliverable',
  'visual_assessment':'实际查看v2 raw、full/inset的三背景1x及8xNN。纵向画幅已解决v1脸偏小，低帽檐/灰缕低髻/褪绿短斗篷符合最新卡，三十多岁身份没有硬冲突，原始轮廓完整。然而两眼保留大片高亮白与偏卡通宽眼型，裸颈仍细长，仍未达到四核心小暗眼白、短颈的整体风格。inset仅增加技术空边，不改善核心问题。本轮暂挂，v2仅保审阅证据，无第三次。',
  'limitations':['核心风格未通过：两眼大亮白、偏卡通眼型与细长裸颈；不能因技术格式通过或大脸构图改善而列为可交付选稿。','原始左右实体透明余量17/13px、底18px，轮廓完整但余量紧；full bbox(1,9,73,99)，inset不修复风格。','selected为空、delivery_eligible=false；full v2和inset均只留研究审阅证据，不进入选稿交付清单。','NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。'],
 },
}
for slug,data in reviews.items():
 path=f'{slug}/candidates/portrait_v2_74x100_candidate.png'
 assert sha(P/path)==data['expected_sha256'],slug
 t=json.loads((Q/f'{slug}_technical_audit.json').read_text())
 v=next(x for x in t['versions'] if x['version']=='portrait_v2')
 threshold=v['raw_boundary_thresholds']['128'];bbox=threshold['bbox'];ww,hh=v['raw_size']
 eligible=data.get('delivery_eligible',True)
 out={'slug':slug,'reviewer':'independent_qa','checked_utc':datetime.now(timezone.utc).isoformat(),'status':data.get('status','candidate_with_limitations'),'delivery_eligible':eligible,'selected_path':path if eligible else None,'selected_sha256':data['expected_sha256'] if eligible else None,'held_evidence_path':None if eligible else path,'held_evidence_sha256':None if eligible else data['expected_sha256'],'visual_assessment':data['visual_assessment'],'limitations':data['limitations'],'raw_path':v['raw_path'],'raw_sha256':v['raw_sha256'],'raw_dimensions':v['raw_size'],'raw_subject_bbox_alpha_ge128':bbox,'raw_real_margin_px':{'left':bbox[0],'top':bbox[1],'right':ww-bbox[2],'bottom':hh-bbox[3]},'raw_boundary_thresholds':v['raw_boundary_thresholds'],'raw_true_silhouette_clipping':False,'boundary_judgment':'实际原图轮廓完整，alpha>=5四边均无实体接触。alpha1孤立残余不是头发/耳的真裁断。边距紧记录限制，未通过padding或inset掩盖。','viewed':['identity mother','four core style references','portrait_v1 raw and NN','portrait_v2 raw','portrait_v2 1x three backgrounds','portrait_v2 8x exact NN']+(['portrait_v2_inset 1x three backgrounds','portrait_v2_inset 8x exact NN'] if slug in ['suoya','ousha'] else []),'feedback_rounds':1,'successful_image_generations':2,'third_generation_allowed':False,'native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False}
 (Q/f'{slug}_final_visual_review.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Wrote independent visual reviews:',', '.join(reviews))
