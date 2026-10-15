"""Record independent visual decisions; no production writes or drawing."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
info={
 'vila':{'tag':'portrait_v2_inset','sha256':'49f48179cf94d2aaef4db5e5362b0c752a64a861573ef9acb43ef8b620949627','identity':'短灰发、宽颧、约40岁中性成年可逆提案；解剖左眼即画面右眼透明夹，双眼可见；炭灰工装与赭棕围裙肩带符合源','improvement':'V2眼白缩小压暗，鼻颧和眼下成熟块、短颈明显改善；抬眉开口精确解释限制，未改成英雄技师','boundary':'实看完整raw及右缘3x浅深合成，右侧放大夹与发束轮廓在源内闭合；右边最大alpha=1，alpha>=5四边不接触。full NN右边贴网格并非源裁断；72×98同raw等比inset仅技术留边。','limitations':['性别仍未定，不据中性外观冻结身份canon。','夹镜边及眼白仍较亮，面部仍有imagegen细簇；仅有注记NN派生候选。','源边余量偏窄；inset不是重绘或原生像素验收。']},
 'hepo':{'tag':'portrait_v2_inset','sha256':'a95180b96ffa8cdae43fdfa4b4b42e0bb5d338fdc00b2c71ce7e08894df088be','identity':'40多岁粗红风吹肤色、棕乱发短浓胡、圆大鼻、宽颧、绿短披/赭厚衣成立；温和忧虑仍愿听旅人归来','improvement':'V2眼白面积减小、上视惊惶缓和；面鼻块更集中，脸相对占比略增；保个人风乱发与温和沉重表情','boundary':'右边最大alpha=5，alpha>=5仅6边点；alpha>=16四边零接触。3x源边浅深合成明确主发束黑轮廓在源内闭合，最右3px仅微弱alpha羽化/噪点，不是切去一束发。full NN右/底贴边是采样，inset可安全留目标网格余量，不声称raw每个alpha阈值完全透明。','limitations':['白眼仍偏浅，绿披及下颈占比仍略大于核心；仅有注记NN派生候选。','源右边只留很窄的主要轮廓余量，边缘alpha5噪点仍记录；不把inset说成裁断修复。']},
 'siyu':{'tag':'portrait_v2','sha256':'b1fb37e69591762d7d868b20e9367b29f6a0abe49618decfd8871d3645fe696d','identity':'30多岁女性母身份，窄长脸直鼻薄平嘴、谨慎微眯/侧目、低髻与素蓝衣浅褐肩边成立；按最新正文她继续','improvement':'V2颈显著缩短、蓝窄领上移，鼻颧整块更清楚，保成年但不强加40岁皱纹；选优于V1','boundary':'alpha>=5 bbox [22,64,1054,1375]，四边真留余量；alpha1极低边点不判发髻裁断。完整raw和三底预览均见闭合发髻/耳。','limitations':['末S91他与正文她的代词不一致留痕，沿正文及女性母图，不修改源卡。','眼白仍偏浅，额部有细碎簇；仅有注记NN派生候选。']},
 'buxi':{'tag':'portrait_v2','sha256':'f9b70515f015f28b7fa4b004d14abab888b245287c5ac572aec7b54171879ddd','identity':'约40岁女性低髻窄成熟脸、谨慎风险估量薄闭嘴；最新鼻粉、蓝衣厚围裙肩带成立；与司榆面向、发形、年龄及口吻相区分','improvement':'V2脸增大、颈缩短；眼下/鼻唇与颧骨成熟块足以建立约40岁，保窄脸而未过度老化','boundary':'alpha>=5 bbox [46,104,1049,1408]四边不接触；alpha1少数边点不形成可见轮廓裁断。低髻耳在raw和三底均完整。','limitations':['现卡S91孤立他与旧女性母设定歧义，经git/brief/prompt及剧情核对后协调保女性继续，未改源卡。','少量眼白及鼻粉仍浅、面簇偏柔；仅有注记NN派生候选。']}
}
for s,x in info.items():
 path=f"{s}/candidates/{x['tag']}_74x100_candidate.png";assert sha(P/path)==x['sha256'],s
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=next(v for v in t['versions'] if v['version']=='portrait_v2');d=next(d for d in v['derivatives'] if d['path']==path)
 row={'slug':s,'checked_utc':datetime.now(timezone.utc).isoformat(),'status':'accepted_with_notes_as_NN_derived_candidate','delivery_eligible':True,'selected_path':path,'selected_sha256':x['sha256'],'reviewed_raw':v['raw_path'],'reviewed_raw_sha256':v['raw_sha256'],'identity_and_age_costume':x['identity'],'visual_comparison':x['improvement'],'boundary_assessment':x['boundary'],'raw_multilevel_alpha':v['raw_boundary_thresholds'],'candidate_bbox':d['alpha_bbox'],'technical_candidate_valid_and_byte_reproduced':d['valid_format'] and d['byte_reproduction'],'actual_views':['historical identity mother and four core references','full v1 and v2 raw','1x three-background previews','4x integer-nearest three-background previews']+(['3x source-right-edge light/dark alpha composite'] if s in ['vila','hepo'] else []),'limitations':x['limitations']+['未逐像素原生绘制，未集成或实机验收。'],'consolidated_feedback_rounds':1,'successful_generations':t['generation_count'],'third_generation_allowed':False,'native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False}
 (Q/f'{s}_final_visual_review.json').write_text(json.dumps(row,ensure_ascii=False,indent=2)+'\n')
print('recorded four selected-byte visual decisions')
