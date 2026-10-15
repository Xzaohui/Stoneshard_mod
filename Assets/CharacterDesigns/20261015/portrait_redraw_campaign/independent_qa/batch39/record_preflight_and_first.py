"""Record independent source/visual decisions. Writes only batch39 QA evidence."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,data):(Q/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
entries={e['suggested_slug']:e for e in json.loads((P/'campaign_roster.json').read_text())['characters'] if e['suggested_slug'] in ['don','fuduo','kofu','lema']}
identity={
 'don':{'name':'多恩','age':'五十多岁','identity':'芙朵父亲、农夫与本人旧债请求人','appearance':'高秃额、灰褐鬓发与灰须、长垂鼻、削瘦颧骨、左眼常眯；褪棕补丁农褂。最新卡软塌帽檐优先旧无帽母图，推后软帽保高额身份。','story':'本人旧债与女儿未来工分开；固执迟疑自辩，不可怜乞讨化，不画代签已同意或债务已清。'},
 'fuduo':{'name':'芙朵·谷','age':'二十多岁成年女性','identity':'多恩的佃农女儿，售粮救弟与自主学艺属于同人','appearance':'麦色皮肤、棕中央分发单侧辫、短略翘鼻、宽距小眼厚下唇；赭衣鼠尾草围裙。最新卡自染头巾优先旧裸发母图，颜色未指定，鼠尾草提案兼容。','story':'与蔻芙/德娅另一家庭分清，学艺与父债分开，不描绘婚事或种袋交付完成。'},
 'kofu':{'name':'蔻芙','age':'二十多岁成年女性','identity':'德娅成年女儿、井旁菜地使用权请求人','appearance':'麦肤、深棕双简辫、成年方颌较长直鼻厚平嘴；绿衣浅围裙。最新卡明确浅蓝自染头巾，优先旧母图无头巾。','story':'愿婚与移地分开，公共取水独立；不表现婚礼/转地已完成，不回到母QA排除的幼态娃娃脸。'},
 'lema':{'name':'雷玛','age':'三十多岁成年男性母版提案','identity':'三篱中想退出的邻户','appearance':'偏白肤色、窄肩；棕乱短发方颌淡胡茬母版辨识延续。最新卡家织粗布衣/洗白罩衫优先旧短披，浅燕麦外领与苔绿内领兼容。','story':'退出按实条件办，克制忧虑与坚定，不忘恩化，不描绘门已开或续约和好。'}
}
feedback={
 'don':'减少高耸八字眉和亮白大眼，左眼更窄，固执迟疑自辩而非可怜老人；显著缩短露颈和衣领、提高脸鼻颧块占比；保帽、高额、灰须、长鼻、真实完整边余。',
 'fuduo':'显著缩短露颈与胸领放大脸；小暗横向眼代亮白大圆眼，保成年麦肤、厚下唇短略翘鼻、坚韧隐忧、单侧完整辫、自染头巾和赭/鼠尾草色；辫底源余量稍增。',
 'kofu':'缩短颈、压窄领放大脸鼻颧骨块；减翼状上睫和亮白大眼，保方颌直鼻厚平嘴、成年麦肤、完整双辫和浅蓝头巾绿衣，不回幼态；真实边余量稍增。',
 'lema':'缩短颈、压窄洗白罩领和绿内领放大脸；小暗眼白、减细碎纹理，保三十多岁偏白肤色棕乱发方颌淡胡茬和克制忧虑坚定，避免少年帅脸；源发耳完整真实边余。'
}
pre=[];first=[]
for slug,details in identity.items():
 e=entries[slug];t=json.loads((Q/f'{slug}_technical_audit.json').read_text());v=t['versions'][0]
 assert all(x['all_equal'] for x in t['source_validation'])
 pre.append({'slug':slug,'actor_id':e['canonical_id'],**details,'current_card_sha256':e['current_cards'][0]['sha256'],'current_original_card_sha256':sha(R/e['current_cards'][0]['path']),'current_card_matches_roster':sha(R/e['current_cards'][0]['path'])==e['current_cards'][0]['sha256'],'latest_card_changed_since_historical_master':not e['current_cards'][0]['previous_hash_matches_current'],'mother_sha256':e['identity_master']['sha256'],'hard_identity_conflict':False,'priority':'latest card appearance details supersede compatible old concept omissions; changed hash alone is not conflict','actually_viewed':['selected identity mother in QA NN overview','Mara/Iwo/Leiya/Tore exact 4x NN board','v1 raw source','v1 4x light/mid/dark backgrounds'],'read_sources':['current original card (snapshot hash verified)','mother independent QA and manifests','campaign roster','related story actor passages','root/design AGENTS']})
 first.append({'slug':slug,'version':'portrait_v1','status':'one_necessary_revision_requested','consolidated_feedback_round':1,'candidate_path':v['derivatives'][0]['path'],'candidate_sha256':v['derivatives'][0]['sha256'],'raw_sha256':v['raw_sha256'],'visual_findings':feedback[slug],'source_boundary_review':'Actual silhouette intact with genuine margins. alpha1 noise at some borders is not silhouette clipping; thresholds >=5 have no source border contact. Fuduo braid bottom 16px, Kofu/Lema right about14px are small real margins, target-grid 1px is not raw clipping.','raw_boundary_thresholds':v['raw_boundary_thresholds'],'second_generation_allowed':True,'third_successful_generation_allowed':False})
 shutil.copyfile(Q/f'{slug}_technical_audit.json',Q/f'{slug}_v1_technical_audit.json')
save('identity_preflight.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'source_snapshots':'independent_source_manifest.json','characters':pre,'hard_conflicts':[]})
save('first_pass_visual_reviews.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'core_style':'大脸短颈窄领，小暗眼白，大鼻颧骨色块，身份年龄与个性优先','characters':first,'native_pixel_approved':False,'runtime_verified':False})
print('recorded independent identity preflight and unique first-pass feedback for 4 actors')
