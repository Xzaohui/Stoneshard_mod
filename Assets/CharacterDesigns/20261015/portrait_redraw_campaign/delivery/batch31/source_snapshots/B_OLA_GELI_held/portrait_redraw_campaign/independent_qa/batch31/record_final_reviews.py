"""Store actual independent visual decisions. Never edit author assets."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
data={
 'folan':{
  'status':'selected_nn_candidate_with_visual_limitations','delivery_eligible':True,
  'selected_path':'folan/candidates/portrait_v2_74x100_candidate.png',
  'selected_sha256':'a8efb17508770bd5babfa28f295038a725418b4068e962df94b3b47fbcabcfdc',
  'visual_assessment':'实际查看v2原始回包图和full/inset的8x NN；full的短颈窄领明显改善，脸占幅增加，40多岁灰发短须/后退发际与茄紫内衫棕罩衣保持。full导出眼白更克制，鼻颧骨块面与务实谨慎成立。源发耳完整，不需要inset缩脸。',
  'source_clipping':'raw alpha>=128 bbox(73,70,1055,1414)，画布1079x1458，真实边距左73/上70/右24/下44；四边无有效轮廓接触。alpha1零星边缘噪点不等同发耳裁断。',
  'target_margin':'full bbox(5,5,72,97)，左右均有透明余量。',
  'limitations':['灰发短须仍有细碎亮色、眉心略带忧虑；保留成熟个性但不称四核心风格完全等同。','此为整画布NN缩放/限色/二值alpha技术派生候选，非原生逐像素或实机终稿。'],
 },
 'geli':{
  'status':'held_source_braid_clipping_and_style_incomplete','delivery_eligible':False,
  'selected_path':None,'selected_sha256':None,
  'held_evidence_path':'geli/candidates/portrait_v2_74x100_candidate.png',
  'held_evidence_sha256':'72213ea23c3c5760e481f31c37c31585fd98750991e435e3fde9840ead786ae9',
  'visual_assessment':'已实际查看v1/v2原raw和NN导出；v2发辫尾继续伸至画布底部后被切断，没有自然完整收尖。颈胸仍长、眼白仍偏亮，集中反馈未有效完成。v1源完整但未过本轮亮大眼白/长颈风格门槛，不因v2失败而回退称完成。',
  'source_clipping':'v2画布1079x1458，alpha>=128 bbox(32,87,1077,1458)，底边36px接触x1012..1047；alpha>=5仍38px触底。可见轮廓与像素共同证明真实辫尾截断，不是NN贴边或有意肩胸断幅。',
  'target_margin':'v2 full bbox(2,6,74,100)；v2 inset bbox(3,7,73,98)只把原截断尾巴缩入画布，不能修复。v1 raw右4px/底17px为真实余量，与v2真裁断分开记录。',
  'limitations':['v1、v2及所有inset仅保留审查证据，均排除已选交付列表。','已用两份成功生图，禁止第三次；不以padding、脚本补发或回退未达标旧稿伪造通过。','未有合格的本批候选，不代表角色身份或旧母版不可用；未做原生逐像素或实机验收。'],
 },
 'ola':{
  'status':'selected_nn_candidate_with_visual_limitations','delivery_eligible':True,
  'selected_path':'ola/candidates/portrait_v2_74x100_candidate.png',
  'selected_sha256':'3ad917cfd8888927ed4d124c936e5efeb84b182c135a538dd376e9b44e0bac84',
  'visual_assessment':'实际查看v2 raw和8x NN；颈胸与大围裙扣明显减少、脸幅增加，40多岁成熟骨相、棕髻、锈衫保持。棕发髻与耳侧轮廓完整。成熟戒备读法可接受，仍有轻忧惧，不称完全达到四核心风格。',
  'source_clipping':'raw alpha>=128 bbox(41,157,1068,1339)，1079x1458，真实右余量11px，四边有效轮廓无接触。alpha1底73px/左8px为极低alpha噪点；alpha>=5已经完全退离边界，不是头发/耳朵裁断。',
  'target_margin':'full bbox(3,11,73,92)，右1逻辑像素有真实源余量，不另inset再缩脸。',
  'limitations':['顶部透明空11逻辑像素、底部空8像素；眼白略亮、眉心仍稍忧惧。','肩皮与围裙主体位于此次紧脸裁景范围外，不据此声称全身工装或器具已验收。','仅NN技术派生候选，非原生逐像素或实机终稿。'],
 },
 'lin':{
  'status':'selected_nn_candidate_with_visual_limitations','delivery_eligible':True,
  'selected_path':'lin/candidates/portrait_v2_74x100_candidate.png',
  'selected_sha256':'24fa414638fce73b0884b8060b48b880b1e79cf674ae5fd4121fcb4f86178490',
  'visual_assessment':'实际查看v2 raw与8x NN；脸较v1更占幅、颈领收短，30多岁清瘦净面长鼻与苔绿披棕衣成立。最新卡低檐帽可见且帽、发、耳完整。眉口沉静，不作高权威法官。可用为有保留的NN候选，不称完全达四核心紧脸标准。',
  'source_clipping':'raw alpha>=128 bbox(42,188,1060,1425)，1079x1458，右19px真实余量；四边无有效轮廓接触。alpha1左7px是低alpha噪点，不是源发耳裁断。',
  'target_margin':'full bbox(3,13,73,98)，右仅1逻辑像素为紧边限制，有真实源余量；不另inset缩小已有脸幅。',
  'limitations':['顶部透明空13逻辑像素、眼白仍稍亮、颈侧仍略长；这些未完全达到四核心紧脸标准。','六参考参数一次前置校验拒绝无生成图，完整错误另存；实际成功生图仅v1/v2两份。','仅NN技术派生候选，非原生逐像素或实机终稿。'],
 }
}
for slug,row in data.items():
 row.update({'batch':31,'slug':slug,'checked_utc':datetime.now(timezone.utc).isoformat(),'feedback_rounds':1,'successful_generation_limit':2,'third_generation_allowed':False,'native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False})
 path=row['selected_path'] or row['held_evidence_path']; expected=row['selected_sha256'] or row['held_evidence_sha256'];assert sha(P/path)==expected
 (Q/f'{slug}_final_visual_review.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
print('Wrote final decisions for',','.join(data))
