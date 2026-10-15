"""Write independent identity evidence and the sole initial visual feedback per actor.
Only writes batch38 independent QA. Does not mutate production assets.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,shutil,subprocess
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
def write(name,data): (Q/name).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for s in ['vila','hepo','siyu']:
 shutil.copyfile(Q/f'{s}_technical_audit.json',Q/f'{s}_v1_technical_audit.json')
extra=[]
for path,role in [
 ('Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_osbrook_grain_bounds_40.json','Buxi female appearance evidence lines 50 and 93'),
 ('design/04_人物/人物细描与随身物.md','S91 repeated appearance wording, no independent male identity source')]:
 src=R/path
 if not src.exists():
  matches=list(R.glob('design/**/人物细描与随身物.md'));src=matches[0];path=str(src.relative_to(R))
 dst=Q/'source_snapshots'/path;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
 extra.append({'path':path,'snapshot':str(dst.relative_to(Q)),'role':role,'sha256':sha(src),'bytes':src.stat().st_size})
path='design/04_人物/城市人物/人物_OSB-NPC-BUXI_布希.md'
for commit in ['be19635','09216ad']:
 data=subprocess.check_output(['git','show',f'{commit}:{path}'],cwd=R)
 dst=Q/'source_snapshots/git'/commit/'buxi_card.md';dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
 extra.append({'path':f'git {commit}:{path}','snapshot':str(dst.relative_to(Q)),'role':'Buxi character card before and after S91 append','sha256':sha(dst),'bytes':len(data)})
write('supplemental_source_manifest.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'sources':extra})
identity={
 'vila':{'status':'continue_androgynous_reversible_proposal','age':'约40岁','gender':'未定；不因名字或外貌冻结','source_basis':'现卡无性别；母QA明确40岁中性成年可逆提案；人物解剖左眼即画面右眼透明单片夹，双眼可见','costume':'炭灰工装、赭棕皮围裙肩带','story':'普通单副有限支架，不作全山担保或已交货象征'},
 'hepo':{'status':'identity_clear_latest_appearance_takes_precedence','age':'40多岁','gender':'男性，现卡正文他','source_basis':'最新卡粗红风吹皮肤、厚褂；与母图棕乱发短浓胡、绿短披赭衣不矛盾','costume':'绿短披/赭厚衣，窄棕系带','story':'温和忧虑且仍欢迎探索，停一段而非全山'},
 'siyu':{'status':'continue_female_with_documented_pronoun_ambiguity','age':'30多岁','gender':'女性母身份，现卡正文她/末S91一处他不一致','source_basis':'现卡动机连续她、母prompt明确female及母图女性；协调裁定按正文继续，不改源卡','costume':'素蓝罩衣/窄蓝领、浅褐肩披边','story':'谨慎读细数、薄平嘴，不画复测完成或全山安全认证'},
 'buxi':{'status':'continue_female_after_independent_history_check_and_coordinator_decision','age':'约40岁','gender':'女性母身份；最新S91孤立他保留为歧义','source_basis':'git be19635旧卡SHA a0e89e40202e840b5750cd42572f033f93cb24c3a0d066fd8a8b98f09274e11d且无性别；09216ad只追加S91末他；总表同句镜像非第二独立证据；母brief 50/93明确女性、母prompt mature woman/Around forty；现行CM-OSB本人发言无男性正文。父协调确认继续，不held','costume':'保棕低髻靛蓝/棕披身份，最新厚围裙/鼻粉优先','story':'只本季有限采购，不画付款交接或长期兜底'}
}
write('identity_preflight.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'read_rules':['AGENTS.md','design/AGENTS.md'],'mother_and_four_core_visuals_actually_viewed':True,'source_priority':'latest appearance updates first; hard identity conflicts stop; hash changes alone are not conflicts','actors':identity,'limitations':['No source card or historical asset changed.','Gender appearance proposals are not new canon assertions.']})
first={
 'vila':{'version':'portrait_v1','candidate_sha256':sha(P/'vila/candidates/portrait_v1_74x100_candidate.png'),'status':'one_consolidated_revision_requested','identity':'短灰发、左眼透明夹和皮围裙身份正确；整体面偏年轻，约40岁读数不足','feedback':['缩暗白眼并压低睫状黑上缘，保双眼透明可见','鼻梁鼻翼和宽颧用更大平面，少量眉间/眼下年龄块，不画老年皱网','短露颈、窄衣领/围裙下沿，脸本体更占框','发耳真实余量保留，勿用padding伪装裁断'],'boundary':'Raw alpha>=5 four borders clear; alpha1 left-edge specks are not visible hair crop. Full head and ear preserved.'},
 'hepo':{'version':'portrait_v1','candidate_sha256':sha(P/'hepo/candidates/portrait_v1_74x100_candidate.png'),'status':'one_consolidated_revision_requested','identity':'棕乱发浓短胡、绿披赭衣、40多岁风红皮肤身份成立','feedback':['缩暗亮大白眼，保抬内眉温和忧虑，减少惊惶上视','大鼻颧骨整块替代细斑','缩绿披和颈下占比，脸更近','真实发耳余量须保留'],'boundary':'Raw alpha>=5 borders clear; alpha1 border specks do not represent visible crop.'},
 'siyu':{'version':'portrait_v1','candidate_sha256':sha(P/'siyu/candidates/portrait_v1_74x100_candidate.png'),'status':'one_consolidated_revision_requested_v1_fallback_allowed','identity':'约30多岁女性、低髻、窄长脸直鼻薄嘴、蓝衣浅褐边成立','feedback':['压窄压暗白眼为灰褐眼缝，保谨慎侧目与读数轻眯','下颌至蓝领露颈缩约1/4，脸稍增但保持窄领','额面细斑并为清楚鼻颧骨块，别加纹显40多岁','源发髻耳完整及真实余量保持；v2退步可选v1，不第三次'],'boundary':'Raw alpha>=5 all four borders clear; alpha1 tiny particles at border are not haircut. Output bbox [2,4,72,97].'}
}
write('first_pass_visual_reviews.json',{'checked_utc':datetime.now(timezone.utc).isoformat(),'actual_views':['mother_overview_NN.png','core_style_4x_NN.png','vila/hepo/siyu full raw','vila/hepo/siyu 1x and 4x integer-NN three-background previews'],'feedback_rule':'Exactly one consolidated initial feedback per actor; max two successful images, no third.','actors':first,'native_pixel_approved':False,'runtime_verified':False})
print('wrote preflight, initial reviews and supplemental original evidence')
