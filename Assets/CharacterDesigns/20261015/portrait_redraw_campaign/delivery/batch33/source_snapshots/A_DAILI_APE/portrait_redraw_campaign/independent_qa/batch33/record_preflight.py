"""Record actual independent input/image inspection; writes QA only."""
from pathlib import Path
import json,hashlib
from datetime import datetime,timezone
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
r=json.loads((P/'campaign_roster.json').read_text());rows=[]
notes={
'daili':('EED-S02-NPC','六十岁上下女性看屋人','母图深褐灰缕卷发、亚麻白巾、宽颊阔鼻、质疑抿嘴、橄榄厚衣暖褐围裙。母图年龄含蓄，最新卡约60岁优先，补眼袋/鼻唇/松弛下颊块；油布肩角与颈绳钥匙为最新卡补充，窄领不可强塞全身物。','不代全家迁居同意，不演新屋接收或产权结案。'),
'ape':('FOR-NPC-APE','四十岁上下男性本段通风维护者','母图灰短发短须、方宽脸阔鼻、低眉眼袋紧口、褪蓝旧罩衣。最新卡40岁优先，灰发是身份特征但不能据此推成70岁；可见测风布条只限窄肩角。','只知本段失风，不演全矿安全/通风权威。'),
'kewei':('FOR-NPC-KEWEI','五十岁上下男性有限矿份出资者','母图整齐灰发、短尖胡、精算防御小眼紧嘴，棕披紫内领。现卡耐脏深色外套优先；约50岁，不演年轻英俊或邪恶东家。','本段有限出资，不以纸面矿价表示实付，不演复工安全结论。'),
'luofu':('FOR-NPC-LUOFU','三十多岁女性生活水与排渠维护者','母图宽方颌扁宽鼻、小深眼粗眉、收发白巾、橄榄工装暖褐围裙。最新卡扎紧头巾与旧罩衣优先；保30多岁实干、不改甜脸或长卷发。','只核本段生活水与渠；不试喝，不诊断全因或净水认证。')}
for s,(id,age,visual,story) in notes.items():
 e=next(x for x in r['characters'] if x['suggested_slug']==s)
 rows.append({'slug':s,'canonical_id':id,'identity_conflict':False,'age_sex_role':age,'current_card_sha256':sha(R/e['current_cards'][0]['path']),'campaign_card_sha_matches':sha(R/e['current_cards'][0]['path'])==e['current_cards'][0]['sha256'],'mother_sha256':sha(R/e['identity_master']['path']),'mother_QA_sha256':sha(R/e['master_selection_evidence']['path']),'actual_visual_assessment':visual,'story_guard':story,'latest_card_priority':True})
write(Q/'identity_preflight.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'method':'Read live cards, roster, root/design AGENTS, mother QA, linked character passages; actually viewed all four identity masters on independent mother overview and all four unchanged style anchors on integer 4x NN board. Current age/clothing addenda supersede older mother appearance without changing identity.','characters':rows,'hard_conflicts':[],'native_pixel_approved':False,'runtime_verified':False})
reviews=[]
for s in ['daili','ape']:
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=t['versions'][0]
 feedback=('压小压暗白眼；加强60岁眼睑眼袋、鼻唇和松弛下颊的大块；显著缩颈、把衣领压底窄带；收紧发巾与大卷发占幅、扩大脸面；保宽颊鼻、灰缕白巾及衣色。' if s=='daili' else '压小压暗白眼；灰白碎亮须发改灰褐主块与有限灰缕，避免60+误读但保40岁疲惫眼袋；再缩短裸颈，保持宽方脸鼻与褪蓝窄领。')
 reviews.append({'slug':s,'version':'portrait_v1','decision':'revision_required','reviewed_raw_sha256':v['raw_sha256'],'reviewed_candidate_sha256':next(d['sha256'] for d in v['derivatives'] if '_inset_' in d['path']),'feedback_round':1,'consolidated_feedback':feedback,'actual_raw_visual_inspection':True,'actual_74x100_and_NN_inspection':True,'source_clipping':False,'raw_boundary_interpretation':'Visible alpha>=5 silhouette has real margins on every side. Alpha=1 border specks are fringe, not severed hair or ears. Inset is technical sampling only and cannot repair raw clipping.','allowed_remaining_successful_generations':1})
write(Q/'first_pass_visual_reviews.json',{'consolidated_feedback_rounds_per_person':1,'characters':reviews})
print('Preflight and first two visual reviews recorded.')
