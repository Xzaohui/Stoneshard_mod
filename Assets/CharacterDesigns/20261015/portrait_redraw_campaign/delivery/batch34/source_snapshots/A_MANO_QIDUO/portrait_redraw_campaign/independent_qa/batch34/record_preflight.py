"""Record independent source/identity review and the only v1 feedback round."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil
Q=Path(__file__).resolve().parent; P=Q.parent.parent; R=P.parents[3]
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
roster=json.loads((P/'campaign_roster.json').read_text())
slugs=['mano','qiduo','xijie','aiqin']
identities={
 'mano': '约五十岁厚实成年女班长，稀疏眉；保留棕布帽、暗棕后束发、赭黄厚工褂。不是安全官。现卡L17她与L40他冲突明确存档，母图与母QA女性一致，按父任务已授权继续女性；不修改原卡。',
 'qiduo': '三十多岁成年男性伤矿工，艾钦成年兄长；宽圆颊、短钝鼻、薄平眉、重眼袋、稀短胡茬；当前卡矿尘灰发及加厚肩垫优先旧母图深发，灰棕矿工短褂。伤未因肖像或结案痊愈，不假定愿意复井。',
 'xijie': '约四十岁成年女性独立井段检查匠；高额长椭圆脸、窄眼、长直鼻、薄闭嘴、暗棕后梳短低辫。当前卡旧皮护具优先历史橄榄衣短围裙，以窄橄榄内领及棕皮护领呈现；不写全矿安全或官方监察。',
 'aiqin': '三十多岁成年女性，老维护者之女、祁铎之妹；中分暗棕后梳低辫、宽圆颊、宽短鼻、小下垂眼；当前卡父亲旧工装改小优先旧蓝裙披巾，窄褪蓝工领，克制旧怒而非复仇。'
}
feedback={
 'mano': '唯一v2：缩短裸颈/胸，仅窄赭黄圆系领；眉按现卡减稀，去内眉上提与下压嘴角的统一忧惧，保成熟承担。小暗眼白、去高光，合并皮肤发束成大鼻颧骨面。保约50岁厚实女性、棕帽暗发，扩大真实右帽发余量，不能padding伪修。',
 'qiduo': '唯一v2：短颈窄领、缩暗眼白；矿尘短发归大簇，去唇上/下颌点状胡茬噪声成为稀短胡茬块。保三十多岁宽圆颊、短钝鼻、重眼袋、薄平眉与自决疲惫，避免厚眉悲情。',
 'xijie': '唯一v2：头在目标y12至88偏小且颈长，实质重绘更大脸、短颈、窄皮护领；保沉着平眉、长直鼻薄闭嘴，合并皮肤发束大簇、缩暗眼白及减上睫，保完整发辫耳真实余量。',
 'aiqin': '唯一v2：长颈胸抢幅，缩短为宽脸主导、窄蓝工领；保中分低辫、宽圆颊短鼻，改忧惧提眉/下嘴角为克制旧怒自控，皮肤发束大块、小暗眼白。raw右辫真实完整，非裁断，不用padding。'
}
rows=[]; reviews=[]
for s in slugs:
 e=next(x for x in roster['characters'] if x['suggested_slug']==s)
 author=json.loads((P/s/'sources/roster_entry.json').read_text())
 assert e==author
 refs=e['current_cards']+[e['identity_master'],e['master_selection_evidence']]+e['master_manifests']
 checks=[{'path':x['path'],'roster_sha256':x['sha256'],'actual_sha256':sha(R/x['path']),'matches':x['sha256']==sha(R/x['path'])} for x in refs]
 assert all(x['matches'] for x in checks)
 rows.append({'slug':s,'actor_id':e['canonical_id'],'source_checks':checks,'identity_resolution':identities[s],'actual_visual_inspection':['selected mother image full resolution','Mara v2 4x NN','Iwo v1 4x NN','Leiya v2 maxcoverage 4x NN','Tore v1 4x NN'],'latest_card_precedence':True,'unresolved_hard_conflict':False})
 t=json.loads((Q/f'{s}_technical_audit.json').read_text());v=t['versions'][0]
 shutil.copyfile(Q/f'{s}_technical_audit.json',Q/f'{s}_v1_technical_audit.json')
 reviews.append({'slug':s,'reviewed_raw_sha256':v['raw_sha256'],'reviewed_candidate_sha256':v['derivatives'][0]['sha256'],'visual_review':'Actual raw and integer 8x target preview viewed against actual mother and four core references.','feedback_round':1,'decision':'one necessary substantive imagegen revision','feedback':feedback[s],'raw_boundary_assessment':'No real silhouette clipping: alpha>=5 has zero border contact; alpha1 border traces are faint spill, not opaque cut hair/ears.','raw_boundary_thresholds':v['raw_boundary_thresholds'],'third_generation_allowed':False})
card=R/rows[0]['source_checks'][0]['path'];lines=card.read_text().splitlines()
assert '她能带班' in lines[16] and '他只能保证' in lines[39]
masterqa=json.loads((R/rows[0]['source_checks'][2]['path']).read_text())
write(Q/'mano_pronoun_reconciliation.json',{'card_path':str(card.relative_to(R)),'card_sha256':sha(card),'female_subject':{'line':17,'exact_line':lines[16]},'isolated_male_pronoun':{'line':40,'exact_line':lines[39]},'master_qa_path':rows[0]['source_checks'][2]['path'],'master_qa_sha256':rows[0]['source_checks'][2]['actual_sha256'],'master_qa_visualAssessment':masterqa['visualAssessment'],'mother_image_sha256':rows[0]['source_checks'][1]['actual_sha256'],'independent_visual_assessment':'Actual selected mother depicts adult woman in brown cap and ochre work clothing.','resolution':'Parent task explicitly permits continuing as female; isolated male pronoun retained as source conflict, not silently corrected. Card age around fifty and sparse eyebrows take precedence over youthful mother face.'})
write(Q/'identity_preflight.json',{'batch':34,'checked_utc':datetime.now(timezone.utc).isoformat(),'sources_snapshot_manifest':'independent_source_manifest.json','source_count':29,'instructions_read':['AGENTS.md','design/AGENTS.md'],'story_sources_read':['台本_CM-FOR_金价之外','台本_CS-FOR-01_旧骑卫的杯','台本_CS-FOR-03_矿份传给谁','伊德斯与佛尔霍特人物演出审查','人物细描与随身物'],'characters':rows})
write(Q/'first_pass_visual_reviews.json',{'batch':34,'checked_utc':datetime.now(timezone.utc).isoformat(),'feedback_rounds_per_person':1,'characters':reviews})
print('Recorded four independent preflights, first reviews and Mano exact pronoun evidence.')
