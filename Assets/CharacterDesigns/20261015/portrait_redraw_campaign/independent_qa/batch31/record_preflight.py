"""Record independently viewed batch31 identities and the single v1 feedback round."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil
Q=Path(__file__).resolve().parent; P=Q.parent.parent; R=P.parents[3]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
write=lambda n,x:(Q/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
actors={
 'folan': {
  'name':'佛兰','age':'四十多岁',
  'identity':'只追一笔真实私人旧债的务实谨慎债权人，不是黑帮打手；不得画成地址披露或归款已完成。',
  'appearance':'保灰短须、后退发际、成熟脸和茄紫内衫/棕直襟罩衣。卡片的无标记帽是配件说明，母图及头像无帽不自动变成身份冲突。',
  'reconciliation':'现卡年龄和衣着优先；不以全身鞋底、腰带、算珠必须出现在紧脸头像中。',
  'v1_findings':['发耳完整，alpha>=128 bbox(60,77,1055,1433)，边缘零接触，非源裁断。','大亮眼白压为小暗暖灰缝；长裸颈与深开衩收为短颈窄领，鼻颧保大块。','眉心上扬偏委屈，收平为谈规矩的务实谨慎；灰发须细碎亮点合并大块，保40+而不再加老。']},
 'geli': {
  'name':'葛黎','age':'二十多岁',
  'identity':'苏槿的同一成年侄女与弓材学徒；专注略无奈、会试错，不是天赋继承人。',
  'appearance':'暗棕侧辫、年轻成年、锈红工衫浅领边和棕围裙。闭口无需强行显示虎牙；护指和练习弦在头像外。',
  'reconciliation':'母图脸龄衣色与现卡兼容；虎牙只在笑时可见，不为标记身份强改成笑脸。',
  'v1_findings':['raw alpha>=128 bbox(33,83,1075,1441)，右4px仍为真实余量；74x100导出右贴边属于NN紧边风险，不是已源裁断。','整辫发耳须在新源图留足真实余量；不靠padding伪修。','眼白过大亮、颈胸过长，改小暗眼白和短颈窄领；弱化眉心竖皱/惊惧上扬，保专注略无奈的年轻成年，不变娃娃、老练贵妇。']},
 'lin': {
  'name':'黎恩·岗','age':'三十多岁',
  'identity':'新原创护林者，清瘦、沉静倾听；只管本段边界，不作林地法官。',
  'appearance':'保棕发、净面长鼻、苔绿短披和棕衣；最新卡低帽檐优先旧母图裸发落兜帽。',
  'reconciliation':'低檐帽属最新卡正常衣着更新，非硬身份冲突；不机械照搬旧母图裸头。',
  'v1_findings':['源帽发耳完整，alpha>=128 bbox(66,125,1032,1411)，无真实源裁断。','帽冠过高、上空9逻辑像素，加上长颈宽披领挤掉脸幅；压低帽冠和上空，短颈窄领，同一清瘦脸更占幅，不靠裁帽发耳。','眼白缩小压暗为暖灰缝，保鼻颧骨块面与沉静倾听，不加老年皱纹或法官威严。']},
 'ola': {
  'name':'奥菈·纹','age':'四十多岁',
  'identity':'成熟、直接且戒备的锯工，只经手本批订单，不是林业总管。',
  'appearance':'棕发髻、锈红圆开衩衫、棕厚围裙与肩部皮料；现卡40+优先母版的偏年轻化。',
  'reconciliation':'使用母QA选定rework_v2，不采用已退役初版；锯链、木牌和手臂在头像外，不增加情节演出。',
  'v1_findings':['源alpha>=128 bbox(36,93,1068,1427)，右有11px真实余量，无真实裁断。','发髻适度压低但保发型、发髻耳侧足够真实余量；短裸颈、围裙扣肩带减为窄领，让脸更占幅。','眼白压小压暗、去眼内亮点；平缓上扬眉心/下撇嘴的惊惧委屈，保成熟直接戒备与大鼻颧块面，不变少女或老太。']}
}
roster=json.loads((P/'campaign_roster.json').read_text())['characters']
for s,v in actors.items():
 row=next(x for x in roster if x['suggested_slug']==s)
 v['actor_id']=row['canonical_id']; v['current_card_checks']=[]
 for c in row['current_cards']:
  actual=sha(R/c['path']);v['current_card_checks'].append({'path':c['path'],'current_sha256':actual,'roster_sha256':c['sha256'],'matches':actual==c['sha256']})
 v['identity_master_sha256']=sha(R/row['identity_master']['path']);v['identity_master_roster_matches']=v['identity_master_sha256']==row['identity_master']['sha256']
 v['master_qa_sha256']=sha(R/row['master_selection_evidence']['path']);v['master_qa_roster_matches']=v['master_qa_sha256']==row['master_selection_evidence']['sha256']
 v['visually_viewed']=['original selected identity mother','Mara/Iwo/Leiya/Tore exact 4x NEAREST style board','v1 full raw','v1 exact 8x NEAREST preview']
 v['hard_identity_conflict_remaining']=False;v['v1_decision']='one_imagegen_revision_required'
 shutil.copyfile(Q/f'{s}_technical_audit.json',Q/f'{s}_v1_technical_audit.json')
write('identity_preflight.json',{'batch':31,'checked_utc':datetime.now(timezone.utc).isoformat(),'independent_original_source_count':32,'characters':actors,'latest_card_appearance_takes_priority':True,'runtime_verified':False})
write('first_pass_visual_reviews.json',{'batch':31,'feedback_rounds_per_person':1,'third_successful_generation_allowed':False,'characters':{s:{k:v[k] for k in ['name','actor_id','v1_decision','v1_findings']} for s,v in actors.items()},'technical':'All four v1 raw files byte-match decoded complete tool returns. Independently reproduced 74x100 RGBA, <=32 visible colors, binary alpha, transparent RGB zero, candidate PNG bytes and integer NN preview PNG bytes. This does not replace visual judgment or source silhouette inspection.'})
print('batch31 identity preflight and four unique v1 reviews saved')
