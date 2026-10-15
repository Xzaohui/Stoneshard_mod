"""Record the single consolidated v1 review for each actor; no author writes."""
from pathlib import Path
from datetime import datetime,timezone
import json,shutil
Q=Path(__file__).resolve().parent
feedback={
'beina':'保蓝巾棕发灰罩衣锈内领、40岁成熟质疑脸；需大脸短颈、仅窄领，内眉别高挑成受气忧惧，眼白继续缩暗、鼻颧块合并，右巾扩大真实余量。raw alpha≥5无边触，属余量窄非真裁断。',
'anni':'显著缩暗大亮眼白/去睫毛妆感、鼻梁鼻翼颧骨成人化大块、短颈窄米灰护理领；保20多岁、棕低髻及坦诚报班神态。raw右边x1078、y692–764有73个alpha≥128主体像素，实际右发被截，不仅NN贴边；必须重绘完整右发并留真实透明余量，不能inset/padding掩盖。',
'kuen':'保30多岁苍白成年男性、棕乱发稀胡茬、灰褐厚披肩和灰蓝内领、自主具体说话的疲态；长裸颈/V领占幅过大、眼白仍亮、发/胡茬碎簇密，内眉高提忧惧。重绘大脸短颈窄领、小暗眼白与平稳有主见眉口，鼻颧成人大块，合并胡茬发束。raw alpha≥5无边触，完整余量窄，不用padding代修。',
'lint':'新卡短发别耳后、素护理褂及30多岁女性成立，保方颊明确鼻翼厚嘴；实质大脸短颈，长裸颈胸厚领缩为窄米灰护理领，眼白缩暗去睫妆感，平眉稳嘴保利落接收员，别忧惧提眉下嘴角。发肤大簇，鼻颧结构别甜化。raw alpha≥5无边触、轮廓完整，保持短发耳真实余量。'}
rows=[]
for s,note in feedback.items():
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=t['versions'][0]
 assert v['version']=='portrait_v1'
 shutil.copyfile(Q/f'{s}_technical_audit.json',Q/f'{s}_v1_technical_audit.json')
 rows.append({'slug':s,'reviewed_raw_sha256':v['raw_sha256'],'reviewed_candidate_sha256':v['derivatives'][0]['sha256'],'actually_viewed':['full raw','8x integer nearest-neighbor target preview','full identity mother','4x integer nearest-neighbor four-core style reference'],'feedback_round':1,'decision':'one necessary substantive imagegen revision','feedback':note,'raw_boundary_thresholds':v['raw_boundary_thresholds'],'source_real_clipping':s=='anni','third_generation_allowed':False})
(Q/'first_pass_visual_reviews.json').write_text(json.dumps({'batch':35,'checked_utc':datetime.now(timezone.utc).isoformat(),'feedback_rounds_per_person':1,'characters':rows},ensure_ascii=False,indent=2)+'\n')
print('Four single-round v1 reviews recorded.')
