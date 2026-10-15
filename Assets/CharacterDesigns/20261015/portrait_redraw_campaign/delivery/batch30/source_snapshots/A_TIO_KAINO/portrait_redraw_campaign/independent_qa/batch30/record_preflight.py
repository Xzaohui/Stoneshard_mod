"""Write the independently observed identity and first-pass review record; QA paths only."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
write=lambda n,x:(Q/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
actors={
'tio':{'name':'提奥·桶','age':'二十多岁','identity':'归乡酿酒学徒，与罗莎师徒；不是箍桶学徒贝洛。','appearance':'栗棕短乱发，无须，橄榄开衩圆领衫、浅围裙。','reconciliation':'现卡写箍桶磨痕、腰锤等与现台本工艺区分有文本差异；地域主章及演出审查明确提奥为酿酒学徒，贝洛为箍桶学徒。此头像不画手、腰或器具，不重写卡片，不以姓桶合并角色。','v1_decision':'one_imagegen_revision_required','v1_findings':['原始左右发梢在画布边真实截断，不是NN贴边；alpha≥128左22像素(y597–618)、右159像素(y496–752)。技术inset不能补发。','白眼块偏大亮，裸颈略长，需完整留边、短颈窄领与朴实鼻颧块面，保认真青年。']},
'saifu':{'name':'赛芙','age':'三十多岁','identity':'迁居后的试种人，谨慎自尊轻声坚定，不作可怜外来者。','appearance':'最新卡浅于本地人的肤色、素披巾和旧布衣本地新围裙优先；沿母图短暗发、朴素锈红巾、蓝衣、棕围裙。','reconciliation':'母图偏橙少女感只作为身份底稿；本轮须落实30+与中性较浅肤色。','v1_decision':'one_imagegen_revision_required','v1_findings':['源发巾耳完整，无alpha≥128边界接触；右余量13源像素、NN后仅1逻辑像素，边距需改善。','上方空15逻辑像素，脸占幅不足；收紧构图，短颈窄领但不能裁巾结。','眉心上扬偏忧惧，改谨慎自尊；眼白小暗，肤色去较重橙调，保30+。']},
'kaino':{'name':'凯诺','age':'五十岁上下','identity':'桶石箍桶工/师傅，技术自信正在听人说明，不作坏脾气老顽固。','appearance':'后退发际、灰棕往后梳粗发团、短方灰须、粗眉宽鼻、锈红圆领系带衫棕围裙。','reconciliation':'母图与现卡外观相容；右耳有点背不等于耳伤或耳具，不额外绘制。','v1_decision':'one_imagegen_revision_required','v1_findings':['源发耳完整、无边界接触；alpha≥128 bbox(47,124,1041,1408)。','大亮白眼、斜尖眉读为瞪眼坏脾气；平缓眉眼、缩小压暗眼白。','裸颈衣领较长，需短颈窄领；灰发须细碎闪花合并为大块，不增加衰老。']},
'buze':{'name':'布泽','age':'四十多岁','identity':'沉木旧屋产权请求人，谨慎说理、自辩，有帮助与强迫的缺点，不画成侵占者或已定结局。','appearance':'最新卡干瘦优先旧母图/旧QA壮实宽脸；保留深棕短发短须、鼻形、赭圆领粗衫棕直襟背心色系，瘦颊窄肩。','reconciliation':'源母版壮实体态不继承；右小指、墨斗与界图在头像外，肩线可极少露墨斗绳。','v1_decision':'one_imagegen_revision_required','v1_findings':['源发耳完整，无alpha≥128边缘接触；bbox(42,137,1053,1433)。','干瘦与40+成立；眉心上扬及下撇口过于委屈，改谨慎说理/自辩的略收口和平缓不对称眉。','眼白小暗去亮点，鼻颧大块；裸颈系带衣襟缩短成窄领，保持瘦颊不变宽胖老脸。']}}
roster=json.loads((P/'campaign_roster.json').read_text())['characters']
for s,v in actors.items():
 row=next(x for x in roster if x['suggested_slug']==s)
 v['actor_id']=row['canonical_id'];v['current_card_checks']=[]
 for card in row['current_cards']:
  v['current_card_checks'].append({'path':card['path'],'roster_sha256':card['sha256'],'current_sha256':sha(R/card['path']),'matches':sha(R/card['path'])==card['sha256']})
 v['identity_master_sha256']=sha(R/row['identity_master']['path']);v['identity_master_roster_matches']=v['identity_master_sha256']==row['identity_master']['sha256']
 v['master_qa_sha256']=sha(R/row['master_selection_evidence']['path']);v['master_qa_roster_matches']=v['master_qa_sha256']==row['master_selection_evidence']['sha256']
 v['visually_viewed']=['selected identity master','Mara/Iwo/Leiya/Tore core 4x NEAREST board','v1 full returned raw','v1 exact 8x NEAREST preview'];v['hard_identity_conflict_remaining']=False
 shutil.copyfile(Q/f'{s}_technical_audit.json',Q/f'{s}_v1_technical_audit.json')
write('identity_preflight.json',{'batch':30,'checked_utc':datetime.now(timezone.utc).isoformat(),'sources':'30 independently copied original files, not merely trusting author snapshots.','characters':actors,'all_current_card_appearance_updates_take_priority':True,'runtime_verified':False})
write('first_pass_visual_reviews.json',{'batch':30,'feedback_rounds_per_person':1,'third_successful_generation_allowed':False,'characters':{s:{k:v[k] for k in ['name','actor_id','v1_decision','v1_findings']} for s,v in actors.items()},'technical':'Every v1 passes actual raw vs full tool-return byte match, 74x100 RGBA, <=32 visible colors, binary alpha, zero transparent RGB, export byte reproduction, and integer NN preview reproduction. Technical pass never overrides source clipping or visual rejection.'})
print('preflight and v1 reviews saved')
