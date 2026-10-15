"""Record independently read/viewed identity evidence and the single first-pass review."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
Q=Path(__file__).resolve().parent; P=Q.parent.parent; R=P.parents[3]
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda p,o:p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n')
roster=json.loads((P/'campaign_roster.json').read_text())
specs={
 'sune':{'identity':'二十多岁本批自愿观察记录员；怕丢有限差事但先问许可，不能冷酷或把研究当护理。','appearance':'深棕分缝短辫、窄长面，暗李紫旧罩衫及米麻内领。','resolution':'当前卡与母图母QA没有身份/年龄/衣着硬矛盾；短辫和衣色由母图补充。','first':'身份、年龄和衣色可留；脸偏小，眼白大亮、裸颈长、发丝平行细线多。','feedback':'显著大脸、短颈、窄衣领、小暗眼白，大块鼻与颧骨；保短辫及征询不冷酷表情，完整发耳与真实余量。'},
 'tian':{'identity':'三十多岁妮蔻成年姐姐、旧屋另一合法住者；长期缺觉、怕独担护理而非夺屋恶人。','appearance':'棕发低髻及脸旁碎发，窄面窄肩、眼下阴影；厚陶红布衫和旧灰麻围裙。','resolution':'最新卡与所选tian_v2母图一致，不能误选tian旧v1。','first':'衣色身份及缺觉感可留；大亮眼白偏萌、裸颈过长、发顶厚，脸比例偏小；右余量紧但非源裁断。','feedback':'大脸短颈窄领，小暗眼白、大鼻颧块，合并发丝；保勉强温和而非坏笑，右侧真实余量至少约2逻辑像素。'},
 'niko':{'identity':'三十多岁苍白患者，独立表达仍想住旧屋，缇安的妹妹；不以病弱符号或痊愈迁出代表好结局。','appearance':'蓝头巾、灰棕发、宽厚颊圆鼻；暗蓝厚居家衫、肩披自缝棕毯角有粗线。','resolution':'当前卡SHA不同历史母QA卡，当前卡明确30多岁及自缝毯角优先；灰发不能推断为老年。','first':'蓝巾宽颊圆鼻可留；灰鬓、额纹及口周线组合读龄偏老；眼白大亮，裸颈与棕V领占比大。','feedback':'明确回到30多岁，保苍白自主戒备；大脸短颈窄领、小暗眼白、大整块鼻颧；自缝毯边少量粗线可辨，暗蓝厚衫保留。'},
 'oya':{'identity':'三十多岁疲惫陪护者、肩颈僵硬眼下发青；想休一班而非放弃患者或怨妇。','appearance':'棕低髻、随手系布发绳、窄颧长鼻、紧唇；梅色衣、棕黄披肩与厚灰围裙领边。','resolution':'当前卡SHA不同历史母QA卡，当前30多岁、围裙及布发绳优先；使用已复核rework_v2母图。','first':'窄颧长鼻疲倦紧唇和衣色可留；眼白大亮、颈长领高、发丝平行繁密，右髻真余量紧但未裁断。','feedback':'大脸短颈窄领，小暗眼白、大鼻颧块，合并发丝；保疲倦个性与布发绳围裙，增加右髻真实余量。'}
}
pre=[];first=[]
for s,x in specs.items():
 r=next(y for y in roster['characters'] if y['suggested_slug']==s)
 cards=[{'path':z['path'],'sha256':sha(R/z['path']),'roster_matches':sha(R/z['path'])==z['sha256']} for z in r['current_cards']]
 master=r['identity_master']; qa=r['master_selection_evidence']
 pre.append({'slug':s,'canonical_id':r['canonical_id'],'name':r['name'],'current_cards':cards,'identity':x['identity'],'appearance':x['appearance'],'resolution':x['resolution'],'blocking_identity_conflict':False,'master':{'path':master['path'],'sha256':sha(R/master['path']),'roster_matches':sha(R/master['path'])==master['sha256'],'actually_viewed':True},'master_QA':{'path':qa['path'],'sha256':sha(R/qa['path']),'actually_read':True}})
 t=json.loads((Q/f'{s}_v1_technical_audit.json').read_text());v=t['versions'][0];d=v['derivatives'][0]
 first.append({'slug':s,'version':'portrait_v1','candidate_path':d['path'],'candidate_sha256':d['sha256'],'status':'one_targeted_revision_requested','feedback_round':1,'findings':x['first'],'single_consolidated_feedback':x['feedback'],'actual_views':['identity master','four core style 4x NN comparison','full v1 raw','v1 4x three-background NN preview'],'raw_boundary':v['raw_boundary_thresholds'],'source_clipping_decision':'Hair/ears silhouette intact; alpha>=5 has no canvas-edge contact. Very-low-alpha edge specks are not source silhouette clipping.','technical':{'raw_return_bytes_match':v['raw_equals_return'],'candidate_byte_reproduced':d['byte_reproduction'],'format_pass':d['valid_format'],'all_integer_NN_previews_reproduced':all(d['previews'].values())},'allowed_remaining_successful_generations':1,'third_generation_allowed':False})
write(Q/'identity_preflight.json',{'batch':36,'checked_utc':datetime.now(timezone.utc).isoformat(),'independent_original_source_snapshot_count':28,'source_manifest':'independent_source_manifest.json','characters':pre,'four_core_style_images_actually_viewed':['mara','iwo','leiya','tore'],'story_read_scope':'Current actor-specific passages with neighbouring context in CM-ASH, CS-ASH-01/02/03 and care/highland review, including separate patient/caregiver consent, finite shift, unresolved home rights, stopping observation and later choices.','native_pixel_approved':False,'runtime_verified':False})
write(Q/'first_pass_visual_reviews.json',{'batch':36,'reviewed_utc':datetime.now(timezone.utc).isoformat(),'feedback_rounds_per_person':1,'characters':first})
print('Recorded four independent identity preflights and four unique first-pass feedback rounds.')
