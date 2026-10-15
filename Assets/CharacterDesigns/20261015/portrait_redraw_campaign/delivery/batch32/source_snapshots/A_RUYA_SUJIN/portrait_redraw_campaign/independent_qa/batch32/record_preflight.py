"""Record independent, source-locked batch32 identity and first-pass visual QA.
Reads original roster and cards; writes only in this file's QA directory.
"""
from pathlib import Path
import json, hashlib, shutil
from datetime import datetime, timezone
Q=Path(__file__).resolve().parent
P=Q.parent.parent
R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
slugs=['ruya','sujin','suoya','ousha']
roster=json.loads((P/'campaign_roster.json').read_text())
notes={
 'ruya':{'age':'三十多岁','identity':'本批有限桥材采购经手者；不代表布林全城','appearance':'暗棕发侧长辫、暖肤、成熟紧眉审视；最新卡深色布林式外褂优先于旧锈披占比','hard_conflict':False},
 'sujin':{'age':'五十岁上下','identity':'弓材匠与家艺传人，沉静哀伤及守艺防卫，非隐世宗师','appearance':'灰棕短发、土灰头巾、宽脸年龄块、最新卡深绿磨旧工装','hard_conflict':False},
 'suoya':{'age':'三十多岁','identity':'桦阴成年猎户，有真实旧欠但不以家庭地址作公共安全代价','appearance':'棕发、风雪纹、本人左眉断口、棕猎衣与暗橄榄边','hard_conflict':False,'mother_status':'v3c原始母图真实存在且SHA吻合；旧QA身份结构通过、风格研究未通过，不等于缺母图，也不把旧研究稿改称已交付'},
 'ousha':{'age':'三十多岁','identity':'桦阴巡林者，谨慎不安警觉；不是林地法官','appearance':'低髻灰缕与褪绿巡装保持；最新卡要求低帽檐、防刮短斗篷，优先于旧母图裸头单圆领','hard_conflict':False},
}
rows=[]
for s in slugs:
 e=next(x for x in roster['characters'] if x['suggested_slug']==s)
 checks=[]
 for item in e['current_cards']+[e['identity_master'],e['master_selection_evidence']]+e['master_manifests']:
  src=R/item['path'];snap=Q/'source_snapshots'/item['path']
  checks.append({'path':item['path'],'roster_sha256':item['sha256'],'actual_sha256':sha(src),'snapshot_sha256':sha(snap),'match':sha(src)==item['sha256']==sha(snap)})
 rows.append({'slug':s,'canonical_id':e['canonical_id'],'name':e['name'],'reconciliation':notes[s],'source_checks':checks,'mother_pixels_viewed':True,'current_card_and_historical_QA_read':True,'four_core_pixels_viewed':True})
out={'batch':'batch32','reviewer':'independent_qa','checked_utc':datetime.now(timezone.utc).isoformat(),'roster_sha256':sha(P/'campaign_roster.json'),'decision':'identity_preflight_pass','identity_hard_conflicts':[],'characters':rows,'visual_method':'Read latest original cards/QA and relevant scene constraints; independently view all four identity mothers, Mara/Iwo/Leiya/Tore NN comparison, raw and exact NN previews. Technical format alone is not visual approval.'}
assert all(c['match'] for r in rows for c in r['source_checks'])
(Q/'identity_preflight.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
feedback={
 'ruya':'保暗发长辫、成熟紧眉审视和暗蓝衣领；大亮眼白压为低亮度小窄眼，压短裸颈、扩大面部占画幅、领口只留紧窄边，颧鼻用更少更硬的大色块。',
 'sujin':'保灰缕头巾、深绿工装、宽脸约50岁沉静防卫；压小压暗眼白、明显收短裸颈与宽露上胸，强化眼下/鼻唇与下颌年龄块；头巾右结原始画布留清楚真实余量。',
 'suoya':'保棕发、左眉断口、30多岁风雪纹与棕猎衣橄榄边；明显压短颈部、面部下半扩大为紧凑肖像、衣领更窄；眼白再小再暗、鼻颧做硬大块；完整右发轮廓保真实源余量。',
 'ousha':'最新低帽檐短斗篷成立；保灰缕低髻褪绿、30多岁不加老；换纵向大脸构图解决方形源contain造成脸小，帽冠体量减、脸居主导，眼白明显压小压暗、缩裸颈/宽领，保不安警觉闭嘴。',
}
first=[]
for s in slugs:
 audit=json.loads((Q/f'{s}_technical_audit.json').read_text())
 v=audit['versions'][0]
 shutil.copyfile(Q/f'{s}_technical_audit.json',Q/f'{s}_v1_technical_audit.json')
 first.append({'slug':s,'version':'portrait_v1','raw_sha256':v['raw_sha256'],'candidate_sha256':v['derivatives'][0]['sha256'],'decision':'one_concentrated_imagegen_revision_needed','concentrated_feedback':feedback[s],'feedback_sent_to_author':True,'feedback_rounds':1,'source_true_contour_cut':False,'boundary_note':'alpha>=5主体在原画布四边均不接触；alpha1底/侧噪点不作裁断。苏槿右12px、朔娅右16px余量紧，要求真实源余量，禁止padding掩盖裁断。','max_successful_generation_count':2,'third_generation_allowed':False})
(Q/'first_pass_visual_reviews.json').write_text(json.dumps({'batch':'batch32','reviewer':'independent_qa','characters':first},ensure_ascii=False,indent=2)+'\n')
print('Identity source checks passed; first-pass visual decisions recorded for all four.')
