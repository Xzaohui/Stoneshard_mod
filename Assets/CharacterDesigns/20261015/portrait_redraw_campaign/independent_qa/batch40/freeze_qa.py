"""Freeze the existing v1 review only. Never run author scripts or modify author files.
The user stopped new generation while this first-pass review was in progress.
All QA writes, snapshots and independent reproductions stay under batch40.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,shutil
from PIL import Image,ImageDraw
Q=Path(__file__).resolve().parent;P=Q.parent.parent;R=P.parents[3]
S=['luoshan','ruiyin','vasen','yaduo']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def put(name,obj):(Q/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
now=datetime.now(timezone.utc).isoformat()
identities={
'luoshan':{'name':'洛珊','id':'OSB-NPC-LUOSHAN','age':'五十多岁','identity':'田庄外堤修筐匠，本次自愿有限教作；非永久收留或父债补工。','costume':'棕发、亚麻裹发、酒红衣、棕围裙；最新卡新增磨毛草帽优先于旧母图遗漏。','feedback':'保宽颧颌阔鼻与有边界的神情；草帽收成贴头短沿但不能删掉，重构纵幅大脸短颈窄衣边；缩暗眼白，少量年龄块及稀灰发体现五十多岁；原始帽耳发左右给真实余量，禁止裁断后padding。','visual':'身份服色和最新草帽正确；草帽横幅使74格中脸偏小，上下留空明显，颈偏长、眼白亮、年龄经历感可加强。','boundary':'alpha128 raw bbox [26,61,1182,1277]，1190×1322，右侧8px真实余量。74格bbox右界74是NN采样贴边，未证实源帽/发真裁断；alpha1零星边界噪声不能当实体轮廓。'},
'ruiyin':{'name':'芮茵','id':'OSB-NPC-RUIYIN','age':'四十多岁','identity':'第三篱户，愿有限共护但担忧费用；不替别户同意。','costume':'棕发、蓝头巾及最新卡木钉、灰衣；原母图土黄腰围裙可在窄胸构图外，不凭缺失整身道具判错。','feedback':'保宽实颧颌、长直鼻、薄平口、蓝巾木钉和四十多岁克制担忧；更紧原始纵幅、大脸短颈窄领，眼裂缩窄眼白压暗；不老化成老妇怒容。','visual':'母图rework_v2独立身份及蓝巾木钉正确；头巾到胸仅约77px，空白与裸颈偏多，眼白较亮，需更接近四核心大脸占幅。','boundary':'alpha128 raw bbox [96,51,1162,1294]，1189×1323，真实边界留空；74格bbox [6,12,72,89]，耳、巾、发完整。'},
'vasen':{'name':'瓦森·磨','id':'OSB-NPC-VAS','age':'五十岁上下','identity':'老磨租人，赊粮是真且缓期可谈；迟疑忧虑不等于黑心债主或已完成弧线。','costume':'棕布帽、灰眉灰胡、锈色圆开衩工衣、暗围裙带，衣色延续母图。','feedback':'保完整灰胡、阔厚鼻和迟疑神情；眼裂缩窄眼白压暗，灰胡合并大明暗块少碎亮点，颈与衣带再收薄；原始帽耳发留真实余量。','visual':'大脸整体占幅可用，五十岁上下和服色成立；眼白为亮块，灰胡碎高光偏多，颈与胸仍可收短。','boundary':'alpha128 raw bbox [47,83,1060,1410]，1079×1458，右侧实际19px真实余量（早期消息约16px为粗估，以此精确测量为准）；74格右侧剩1px，非源裁断。'},
'yaduo':{'name':'雅铎','id':'OSB-NPC-YADUO','age':'二十多岁','identity':'蔻芙的成年订婚对象，犹豫不安；非自动地权继承人，不替她答婚。','costume':'棕发无须、暗蓝圆系领短褂，干净青年农户衣色延续母图。','feedback':'保棕发无须、二十多岁与犹豫内眉；原生重构大脸短颈窄衣边，鼻和颧骨明暗更实、眼白小暗；避免光滑美少年模板，不老化成三四十岁。','visual':'青年身份、棕发无须蓝衣正确，犹豫可读；裸颈明显偏长，发量与胸领夹住脸占幅，亮眼白及光滑颊面偏柔。','boundary':'alpha128 raw bbox [58,111,1056,1394]，1079×1458，耳发完整且四边有真实余量；74格bbox [4,8,72,96]。'}}
roster=json.loads((P/'campaign_roster.json').read_text())
entries={x['suggested_slug']:x for x in roster['characters'] if x.get('suggested_slug') in S}
pre=[];reviews=[];summary=[]
for s in S:
 w=P/s;t=json.loads((Q/f'{s}_technical_audit.json').read_text());m=json.loads((w/'manifest.json').read_text());d=identities[s]
 assert t['generation_count']==t['successful_tool_returns']==1,s
 assert t['manifest_selected_path'] is None and t['manifest_selected_sha256'] is None and t['manifest_delivery_eligible'] is False,(s,'author not yet frozen')
 assert t['manifest_all_hashes_match'] and not t['manifest_missing_files'] and t['sha256sums_all_match'] and not t['sha256sums_missing_files'],s
 assert all(x['all_equal'] for x in t['source_validation']),s
 assert all(t['manifest_false_native_runtime_flags'][k] is False for k in ['native_authored','native_pixel_approved','runtime_integrated','runtime_verified']),s
 v=t['versions'][0];assert v['raw_equals_return'] and v['prompt_text_equals_exact_args'] and v['transparent_background'],s
 for a in v['derivatives']:assert a['valid_format'] and a['transparent_rgb_zero'] and a['byte_reproduction'] and a['pixel_reproduction'] and all(a['previews'].values()),s
 cand=w/'candidates/portrait_v1_74x100_candidate.png'
 review={'slug':s,**d,'checked_utc':now,'status':'first_pass_needs_revision_frozen','delivery_eligible':False,'selected_path':None,'selected_sha256':None,'held_evidence_path':str(cand.relative_to(P)),'held_evidence_sha256':sha(cand),'successful_generations':1,'consolidated_feedback_rounds':1,'feedback_execution':'Not executed. New generation stopped at parent relaying the user request to merge/push current changes. No v2 image exists.','actually_viewed':['sources/identity_reference.png','raw/portrait_v1_raw_imagegen.png','previews/portrait_v1_4x_backgrounds.png','independent_qa/batch40/core_style_4x_NN.png'],'limitations':['仅NN技术派生候选，非原生逐像素终稿。','首审待修订，当前用户要求冻结，不发起第二次或第三次生图。','未集成、未实机验证；不得作为通过选稿交付。']}
 put(f'{s}_first_pass_visual_review.json',review);reviews.append(review)
 card=entries[s]['current_cards'][0];master=entries[s]['identity_master'];qa=entries[s]['master_selection_evidence']
 pre.append({'slug':s,'canonical_id':d['id'],'name':d['name'],'age':d['age'],'identity':d['identity'],'clothing':d['costume'],'current_card':card['path'],'card_sha256':sha(R/card['path']),'card_matches_roster':sha(R/card['path'])==card['sha256'],'mother_path':master['path'],'mother_sha256':sha(R/master['path']),'mother_matches_roster':sha(R/master['path'])==master['sha256'],'mother_QA':qa['path'],'mother_QA_sha256':sha(R/qa['path']),'mother_QA_matches_roster':sha(R/qa['path'])==qa['sha256'],'hard_identity_conflict':False,'latest_card_priority':True})
 assert pre[-1]['card_matches_roster'] and pre[-1]['mother_matches_roster'] and pre[-1]['mother_QA_matches_roster']
 summary.append({'slug':s,'status':review['status'],'delivery_eligible':False,'selected_path':None,'selected_sha256':None,'held_evidence_path':review['held_evidence_path'],'held_evidence_sha256':review['held_evidence_sha256'],'raw_sha256':v['raw_sha256'],'technical_format_and_byte_reproduction_pass':True,'author_manifest_sha256':sha(w/'manifest.json'),'author_manifest_file_count':len(t['manifest_file_checks']),'author_all_sha_entries':t['sha256sums_count'],'all_author_hashes_complete_and_match':True,'successful_generations':1,'feedback_rounds':1,'limitations':review['limitations']})
 dst=Q/'author_evidence'/s
 for name in ['derive_portrait.py','finalize_manifest.py','manifest.json','SHA256SUMS','SHA256SUMS.txt','sources/source_manifest.json']:
  if (w/name).exists():
   out=dst/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(w/name,out)
put('identity_preflight.json',{'checked_utc':now,'roster_sha256':sha(P/'campaign_roster.json'),'sources_independently_snapshotted':30,'hard_conflicts':[],'current_card_over_old_appearance_omissions':True,'characters':pre})
put('first_pass_visual_reviews.json',{'batch':40,'characters':reviews,'one_consolidated_feedback_round_each':True,'feedback_is_not_permission_to_resume_generation':True})
checks=[]
for x in json.loads((Q/'independent_source_manifest.json').read_text())['sources']:
 current=sha(R/x['path']);snap=sha(Q/x['snapshot']);checks.append({'source':x['path'],'initial_sha256':x['sha256'],'current_sha256':current,'snapshot_sha256':snap,'all_equal':current==snap==x['sha256']})
assert all(x['all_equal'] for x in checks)
put('independent_source_final_recheck.json',{'checked_utc':now,'all_unchanged':True,'items':checks})
core=Image.new('RGB',(1216,420),(78,78,78));draw=ImageDraw.Draw(core)
for i,n in enumerate(['mara','iwo','leiya','tore']):
 im=Image.open(P/'luoshan/sources'/f'{n}_style_reference.png').convert('RGBA').resize((296,400),Image.Resampling.NEAREST);core.paste(im,(i*304,20),im);draw.text((i*304+4,5),n,fill='white')
b=io.BytesIO();core.save(b,format='PNG');assert b.getvalue()==(Q/'core_style_4x_NN.png').read_bytes()
put('core_style_NN_audit.json',{'integer_factor':4,'byte_reproduced':True,'sha256':sha(Q/'core_style_4x_NN.png')})
put('selection_lock.json',{'batch':40,'status':'all_first_pass_needs_revision_frozen','delivery_include_only':[],'held_evidence_only':[{'slug':r['slug'],'path':r['held_evidence_path'],'sha256':r['held_evidence_sha256']} for r in reviews],'restriction':'No portrait is approved or selected. All v1 candidates/raws are review evidence only. Unexecuted v2 prompts are not generated images or completed work.','native_pixel_authored':False,'native_pixel_approved':False,'runtime_verified':False})
put('QA_summary.json',{'batch':40,'checked_utc':now,'status':'first_pass_needs_revision_frozen','delivery_include':[],'consolidated_feedback_rounds_per_person':1,'successful_generations_per_person':{s:1 for s in S},'new_generation_stopped':True,'third_generation_allowed':False,'characters':summary,'source_clipping_policy':'Actual raw silhouette and alpha5/16/128/255 boundaries distinguish target NN edge contact from true source clipping. Padding cannot repair real clipping.','native_pixel_authored':False,'native_pixel_approved':False,'runtime_integrated':False,'runtime_verified':False})
lines=['# Batch40 独立QA封存','','结论：四人均为初审待修订；当前用户要求合并推送，已停止新增生图。每人仅一份v1成功图、一轮集中反馈，0份通过选稿。技术通过不等于视觉终审通过。','',f'封存时间：{now}','']
for r in reviews:lines += [f"## {r['name']} / {r['slug']}",'状态：first_pass_needs_revision_frozen；不进入交付选稿清单。',f"待修订证据：`{r['held_evidence_path']}`",f"SHA256：`{r['held_evidence_sha256']}`",'身份：'+r['age']+'，'+r['identity'],'实看：'+r['visual'],'唯一集中反馈：'+r['feedback'],'边界：'+r['boundary'],'']
lines += ['## 验证范围','- 30份独立源快照与当前原始文件SHA全部一致；当前卡、母QA、母图和四核心已核读实看。','- 四份raw均与完整生图回包解码逐字节相等；74×100 RGBA、32可见色、二值alpha、透明RGB归零通过。','- 四份候选逐字节独立复现，1x、8x NN和三底1x/4x NN预览通过；核心4x NN预览独立复现。','- 作者manifest与全SHA均完整覆盖并匹配；作者selected已清空，delivery_eligible=false。','- selection_lock.json的delivery_include_only为空；v1只作待修订证据。保存的未执行v2提示词不算生图或已完成修订。','- 没有原生逐像素终稿、游戏集成或实机验证；QA只写本目录，未改旧图、卡、生产代码或git状态。']
(Q/'FINAL_REVIEW.md').write_text('\n'.join(lines)+'\n')
files=[{'path':str(f.relative_to(Q)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(Q.rglob('*')) if f.is_file() and f.name not in ['manifest.json','SHA256SUMS']]
# Nested author manifest and SHA evidence must be included too.
files=[{'path':str(f.relative_to(Q)),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted(Q.rglob('*')) if f.is_file() and f not in [Q/'manifest.json',Q/'SHA256SUMS']]
put('manifest.json',{'batch':40,'scope':'independent QA only; first-pass hold, no selected deliverables','files':files,'selected':[],'native_pixel_authored':False,'runtime_verified':False})
allfiles=[f for f in sorted(Q.rglob('*')) if f.is_file() and f!=Q/'SHA256SUMS'];(Q/'SHA256SUMS').write_text(''.join(f'{sha(f)}  {f.relative_to(Q)}\n' for f in allfiles))
print(json.dumps({'batch':40,'status':'first_pass_needs_revision_frozen','selected':[],'source_files':len(checks),'qa_manifest_files':len(files),'qa_sha_entries':len(allfiles)},ensure_ascii=False,indent=2))
