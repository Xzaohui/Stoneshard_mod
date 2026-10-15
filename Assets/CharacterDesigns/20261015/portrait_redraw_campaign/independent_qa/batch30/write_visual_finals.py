"""Save final independent visual decisions already made from actual raw and NN inspection."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
choices={
 'tio':{'eligible':True,'tag':'portrait_v2_inset','observations':['20+年轻成年无须脸、栗棕乱短发和橄榄开衩衫/浅围裙身份成立；未与贝洛混同。','第二稿重新生成完整发梢，原第一稿左右真实裁断已解决；母版耳轮廓完整，未靠加透明画布掩盖截断。','鼻梁、颧面、下颌有块面；眼白较第一稿缩小，表达仍为认真自持青年。','72×98全画布等比NN containment仅给74×100候选安全留边；source不裁切不补画。'],'limitations':['颈仍稍长、发线仍偏细，未完全达到四核心的短颈粗块精修程度。','同raw等比NEAREST/32色量化技术派生候选，不是原生逐像素或实机终稿。'],'framing':'final bbox(2,5,72,97)；左/上/右/下余量2/5/2/3。'},
 'saifu':{'eligible':False,'tag':'portrait_v2','observations':['短暗发、素锈红巾、蓝旧衣/棕围裙及30+身份意图可识别；不判为换人。','两份raw发、头巾结与耳均完整，不存在实际源裁断；第二稿顶部空白较第一稿减少。','第二稿颈胸衣领却扩大，亮白眼与上扬忧眉仍明显；第一稿脸占幅不足，同样有眼白/暖色问题。','本轮style/composition held，不能把格式合格说成紧脸风格达标；不回选，不第三张。'],'limitations':['大脸短颈窄领目标未达，眼白/表情仍偏离小暗眼与谨慎自尊的要求。','肤色仍偏暖，最新卡较浅肤色尚未充分体现在完成稿中；此是外观待改善，不构造新身份冲突。','仅保留v2为held evidence，selected=null，不得纳入交付选稿。'],'framing':'v2 bbox(2,8,73,98)，右侧仅1逻辑像素；未以边距技术派生掩盖主要风格问题。'},
 'kaino':{'eligible':True,'tag':'portrait_v2_safe','observations':['50岁上下后退发际、灰棕后梳发团与短方灰须、粗眉宽鼻及锈红系带工衣/棕围裙身份成立。','第二稿将灰发须从细碎高光合为大块，眼白明显收小压暗，裸颈衣领缩短，严肃技术自信与听人说明表情可读。','右发真实source alpha≥128边界止于x1072，原图宽1079，右有6像素；alpha≥16也不触边。极低alpha噪声不是真实发耳裁断。','full版最右逻辑格触边来自NN采样；72×98 inset仍只有1px，70×96 safe全画布等比containment得到2px真实透明成品边。'],'limitations':['肤色仍稍暖，须保留NN技术派生/临时32色限制。','只选70×96 safe导出；full与72×98 inset仅过程证据。','不是原生逐像素、游戏集成或实机验收终稿。'],'framing':'safe bbox(6,7,72,95)；左/上/右/下余量6/7/2/5。'},
 'buze':{'eligible':False,'tag':'portrait_v2_inset','observations':['最新卡40+干瘦优先旧母图壮实体态，第二稿瘦颊/窄肩与深棕短发短须、赭粗衫棕背心身份成立。','两份raw发耳完整，不存在实际源裁断；72×98 inset仅安全containment，技术没有问题。','第二稿仍大浅色眼块、忧眉和下撇口，谨慎说理/自辩未充分建立；长裸颈与系带领占幅明显。','第一稿同样存在这些问题；第二稿只有部分块面/比例改进，不足以消除唯一反馈的核心风格缺口。','style/composition held，selected=null，不回选或第三张；不是身份或格式失败。'],'limitations':['小暗眼白、短颈窄领及个性表情目标未充分满足。','v2_inset仅保留为held evidence，不可纳入交付选稿。','NN派生过程图不是原生逐像素或游戏终稿。'],'framing':'held inset bbox(5,8,71,97)；边距合格不能替代视觉合格。'}
}
for s,c in choices.items():
 f=P/s/'candidates'/f"{c['tag']}_74x100_candidate.png";a=Image.open(f).getchannel('A');bb=a.getbbox()
 d={'slug':s,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'status':'selected_derived_candidate_with_limitations' if c['eligible'] else 'held_after_two_generations_style_composition','delivery_eligible':c['eligible'],'selected_path':str(f.relative_to(P)) if c['eligible'] else None,'selected_sha256':sha(f) if c['eligible'] else None,'held_evidence_path':None if c['eligible'] else str(f.relative_to(P)),'held_evidence_sha256':None if c['eligible'] else sha(f),'successful_generations':2,'feedback_rounds':1,'third_generation_allowed':False,'actual_visual_review':['identity master','four core style portraits','v1 raw and integer NN preview','v2 raw and integer NN preview','final derivative preview'],'observations':c['observations'],'limitations':c['limitations'],'framing_notes':c['framing'],'actual_final_bbox':bb,'actual_final_margin_ltrb':[bb[0],bb[1],74-bb[2],100-bb[3]],'native_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False}
 if c['eligible']:assert min(d['actual_final_margin_ltrb'])>=2
 (Q/f'{s}_final_visual_review.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 print(s,d['status'],sha(f))
