"""Final human visual findings, recorded after direct image inspection; QA-only writes."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
Q=Path(__file__).resolve().parent;P=Q.parent.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
findings={
'don':('portrait_v2_inset','高额软塌棕帽、灰褐鬓发灰须、长垂鼻和削瘦颧骨保持；五十多岁劳作父亲辨识清楚。v2眼白变小变暗，左眼更眯，八字哀苦减弱为迟疑自辩；露颈大幅缩短，窄棕领，头脸占比提高。','须发纹理仍比四核心细碎，年长面相略显苍老；这是概念提案而非精确年龄测量。'),
'fuduo':('portrait_v2','成年麦肤、中央分发与完整单侧辫、自染鼠尾草头巾、赭衣和鼠尾草围裙带保持；宽距小眼、短略翘鼻厚下唇，与蔻芙区别明确。v2眼白显著减弱，颈缩短，坚韧隐忧可读。','高领仍偏厚且占底部面积，面貌仍略秀气；无儿童化硬冲突，但不是完全达到四核心窄领与粗块终稿。'),
'kofu':('portrait_v2','成年方颌、较长直鼻和厚平嘴、深棕完整双辫、麦肤、浅蓝自染头巾、绿衣浅围裙保留。v2脸放大、颈略缩短，克制自主，与芙朵短翘鼻/单辫有别。','颈仍稍长，眼白和上睫线仍偏亮强，领/围裙带有一定面积；可交带注候选，未达原生终稿。'),
'lema':('portrait_v2','棕乱短发、方颌淡胡茬、偏白肤色和三十多岁成年邻户辨识保持，克制忧虑且坚定；v2脸显著放大、露颈缩短、洗白粗布罩领和苔绿内领压窄，符合最新卡。','眼白仍较亮，胡茬与发丝细点仍多于核心大块语法；属于有保留的NN候选而非原生逐像素完成。')}
for s,(tag,assessment,note) in findings.items():
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());vr=next(x for x in t['versions'] if x['version']=='portrait_v2');candidate=P/s/'candidates'/f'{tag}_74x100_candidate.png';d=next(x for x in vr['derivatives'] if x['sha256']==sha(candidate))
 box=vr['raw_boundary_thresholds']['5']['bbox'];ww,hh=vr['raw_size'];margins=[box[0],box[1],ww-box[2],hh-box[3]]
 assert not any(vr['raw_boundary_thresholds']['5']['border_counts'].values())
 o={'slug':s,'checked_utc':datetime.now(timezone.utc).isoformat(),'status':'deliverable_with_notes','delivery_eligible':True,'selected_path':str(candidate.relative_to(P)),'selected_sha256':sha(candidate),'selected_raw_sha256':vr['raw_sha256'],'successful_generations':t['generation_count'],'consolidated_feedback_rounds':1,'third_generation_allowed':False,'actually_viewed':['identity mother overview','four core exact 4x NN','v1 and v2 raw','v1 and v2 three-background 4x NN']+(['v2 inset three-background 4x NN'] if s=='don' else []),'visual_assessment':assessment,'limitations':[note,'仅74×100 NN等比缩放/32色无抖动/二值alpha技术派生候选，非原生逐像素终稿，未集成未实机验收。'],'source_boundary':{'raw_size':vr['raw_size'],'alpha_ge5_bbox':box,'alpha_ge5_margins_LTRB':margins,'threshold_evidence':vr['raw_boundary_thresholds'],'candidate_bbox':d['alpha_bbox'],'actual_hair_ears_complete':True,'genuine_source_margin':True,'source_clipped':False,'rationale':'已实看源轮廓且α≥5四边均无接触；低α边缘噪声不作实体裁断。目标少量余量不等同源裁断。Don inset仅缩小完整源以增加目标网格余量，不补画缺失。'},'native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False}
 (Q/f'{s}_final_visual_review.json').write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
print('four final visual reviews recorded')
