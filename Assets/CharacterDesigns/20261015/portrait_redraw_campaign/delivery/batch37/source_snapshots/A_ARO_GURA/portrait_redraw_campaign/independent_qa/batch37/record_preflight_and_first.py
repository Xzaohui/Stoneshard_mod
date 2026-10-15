"""Record the independent human visual judgments made after actual image viewing.
Writes only this batch's QA directory; never changes an author image or source.
"""
from pathlib import Path
import json, hashlib, shutil
from datetime import datetime, timezone
Q=Path(__file__).resolve().parent; P=Q.parent.parent; R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.now(timezone.utc).isoformat()
roster=json.loads((P/'campaign_roster.json').read_text())
ids=['aro','gura','lein','turi']
notes={
 'aro':{'identity':'约40岁女性维护图保管者；宽颧、短宽鼻、低粗眉、深棕侧分厚发与颈后短辫。最新卡明确深色长衣，优先于旧母图的橄榄短披/棕夹棉衣。','card_update':'历史母QA引用旧卡 f3b9483c22a961ad262271e316b880a8df3420e928487f66adfeb671a8698220；当前卡 938458786699a96eb55e4b85144b0c39c95ae751d89b47b91be354a7bbf53fb1 明确年龄衣着。按当前卡更新，不是身份硬冲突。','story_guard':'可以更正自己写过的永久声明，不代表全山权威；不是替别人续约。','feedback':'v1约20–30岁读感偏年轻，亮眼白与内高眉偏忧怒，平行发束仍密；唯一v2优先成熟眼袋/鼻唇大块、沉静较平眉、小暗眼白、减少平行发束，保留深色窄领与原鼻颧和短辫。'},
 'gura':{'identity':'三十多岁女性本次外段维护工；棕低髻、厚眉、暖肤，灰厚工作褂与少量棕带。','card_update':'当前卡与母图身份、年龄和衣着无硬冲突。','story_guard':'认真自主，只签本段本班；不替她作续约、结薪或终身留山承诺。','feedback':'v1眉心尖V、两条额纹和亮眼白使认真变怒；唯一v2优先平稳核段眉与克制嘴、小暗眼白，发与领口合并大块。'},
 'lein':{'identity':'三十多岁成年女向导；宽颧风晒肤、棕外翻短发、软棕帽，一截粉笔中段由帽带遮挡，绿短披米褐内领。','card_update':'当前卡与母图身份、年龄和衣色无硬冲突。','story_guard':'认真解释自己的客约责任，不画奸商笑或已退款/已撤停牌。','feedback':'v1内高眉与亮大眼偏焦虑；唯一v2优先较平轻不对称解释眉、小暗眼白、鼻颧大块、短颈窄绿领，保留微启嘴、粉笔和外翻发。'},
 'turi':{'identity':'约40岁精瘦男机械检查匠；窄脸、棕乱短发、灰鬓短灰须，橄榄短披米白内领。','card_update':'当前卡与选定v2母图身份、年龄和衣色无硬冲突。','story_guard':'只对实核段和本班说结论，不画全山保人或新伤；工具在紧脸裁幅外。','feedback':'v1亮白眼占比大、长颈V领、灰鬓和发平行细纹；唯一v2优先小暗眼白、认真估量、粗鼻颧块、短颈小橄榄领和灰鬓短须大块。'}
}
pre=[];first=[]
for s in ids:
 row=next(x for x in roster['characters'] if x['suggested_slug']==s)
 refs=row['current_cards']+[row['identity_master'],row['master_selection_evidence']]+row['master_manifests']
 checks=[{'path':x['path'],'roster_sha256':x['sha256'],'actual_sha256':sha(R/x['path']),'matches':x['sha256']==sha(R/x['path'])} for x in refs]
 assert all(x['matches'] for x in checks)
 pre.append({'slug':s,'canonical_id':row['canonical_id'],'checked_utc':now,'identity':notes[s]['identity'],'card_update':notes[s]['card_update'],'story_guard':notes[s]['story_guard'],'identity_hard_conflict':False,'roster_checks':checks,'actually_viewed':['selected identity raw in full','Mara v2, Iwo v1, Leiya v2 maxcoverage, Tore v1 in integer 4x NN board'],'read':['current card','matching selected mother QA result and source SHA','master manifest','relevant named scene passages']})
 audit=json.loads((Q/f'{s}_technical_audit.json').read_text());shutil.copyfile(Q/f'{s}_technical_audit.json',Q/f'{s}_v1_technical_audit.json')
 v=audit['versions'][0]
 first.append({'slug':s,'reviewed_utc':now,'status':'one_consolidated_revision_requested','feedback':notes[s]['feedback'],'candidate_sha256':v['derivatives'][0]['sha256'],'raw_sha256':v['raw_sha256'],'actual_views':['v1 raw full','v1 8x NN','selected mother raw','four core references'],'source_hair_hat_ears_complete':True,'source_boundary_note':'alpha>=5 body has real margins on all sides. Low-alpha 1..4 background dust at some borders does not prove subject clipping. Lein x=73 candidate contact is NN sampling, not actual source truncation.','source_alpha_ge128_bbox':v['raw_alpha_bbox_ge128'],'raw_size':v['raw_size'],'single_feedback_sent':True,'max_successful_generations':2,'third_generation_allowed':False,'technical_checks':{'sources':all(x['all_equal'] for x in audit['source_validation']),'raw_return':v['raw_equals_return'],'byte_reproduction':all(d['byte_reproduction'] for d in v['derivatives']),'manifest':audit['manifest_all_hashes_match']}})
(Q/'identity_preflight.json').write_text(json.dumps({'checked_utc':now,'characters':pre},ensure_ascii=False,indent=2)+'\n')
(Q/'first_pass_visual_reviews.json').write_text(json.dumps({'checked_utc':now,'characters':first},ensure_ascii=False,indent=2)+'\n')
print('Recorded four independent preflight and first-pass reviews.')
