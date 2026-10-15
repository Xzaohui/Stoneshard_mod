from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,shutil
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';ROOT=R/'Assets/CharacterActions/20261013/new_story';D=ROOT/'tenth_noncombat_jier_suier_lot_delivery_v1';D.mkdir(exist_ok=True);(D/'review').mkdir(exist_ok=True);(D/'selected').mkdir(exist_ok=True);(D/'scripts').mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();brief=json.loads((A/'tenth_new_character_actions_brief.json').read_text());gate=A/'independent_tenth_new_character_actions_jier_suier_lot_visual_gate_20261014.json'
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';fnt=lambda n:ImageFont.truetype(font,n)
selected={'jier':['jier_A1_open_arms_low_shoulder_stretch_initial','jier_A2_half_crouch_palms_on_knees_initial'],'suier_lot':['suier_lot_A1_support_half_cloth_tape_revision1','suier_lot_A2_smooth_left_apron_panel_initial']}
observations={'jier':['双臂侧下展开、两手各离躯干超过一个掌宽，指组放松；卷袖、灰发灰须、灰蓝粗衫、棕腰带褐裤与双靴完整。','双膝弯曲、髋后沉浅蹲、躯干轻前倾，两掌各贴同侧膝上裤面；双鞋支撑完整，不作伤病或恢复结果。'],'suier_lot':['唯一修订修回原半截软尺长度，右手画面左仍握上端，左掌向画面右托下段、两手分开，尺呈小软弧且短毛边断端外露。','左掌低伸贴本人左侧膝上围裙，与短尺保留清楚空隙；右手腹前仍握原尺，轻前倾、紧结围巾与双鞋完整。']}
layouts=[];charboards={}
for c in brief['characters']:
 slug=c['slug']
 if slug not in selected:continue
 b=ROOT/slug/'noncombat_basics_v1';(b/'scripts').mkdir(exist_ok=True)
 for p in ['/workspace/scratch/5ed8df2c5d81/prepare_tenth_jier_suier_lot_actions.py','/workspace/scratch/5ed8df2c5d81/archive_ninth_actions_image.py',__file__]:shutil.copy2(p,b/'scripts'/Path(p).name)
 shutil.copy2(gate,b/'review/independent'/gate.name)
 for p in sorted((A/'tenth_actions_independent_details').glob(slug+'_*')):
  if p.is_file():shutil.copy2(p,b/'review/independent'/p.name)
 active=[]
 for stem,plan,obs in zip(selected[slug],c['plans'],observations[slug]):
  p=b/'selected'/f'{stem}_transparent.png';shutil.copy2(p,D/'selected'/p.name);active.append({'key':plan['key'],'title_zh':plan['title_zh'],'stem':stem,'selected':str(p.relative_to(b)),'selected_sha256':sha(p),'visible_result':obs,'independent_verdict':'PASS','revision_used':int(stem.endswith('revision1'))})
 (b/'QA-author.json').write_text(json.dumps({'reviewed_utc':now,'scope':'作者自查，不替代独立审查','read_and_viewed_sources':{'current_card_and_full_chinese_dialogue':True,'mother_raw_and_transparent':True,'old_expression_board':True},'all_attempt_raw_transparent_selected_light_dark_actually_viewed':True,'active_selected':active,'initial_rejection':None if slug=='jier' else {'stem':'suier_lot_A1_support_half_cloth_tape_initial','hard_error':'原半截软布尺被显著延长为跨体宽大深弧；唯一修订缩回原短尺并收近左掌','unique_revision':'suier_lot_A1_support_half_cloth_tape_revision1','result':'PASS','all_attempt_artifacts_preserved':True},'not_animation':True,'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
 (b/'README.md').write_text(f'# {c["name"]}｜第十批基础动作概念\n\n两张独立、可逆的日常全身姿态，只作美术概念。不是连续动画、统一原生像素帧尺、装备兼容、碰撞或游戏运行验收。\n\n'+''.join('- '+x['title_zh']+'：`'+x['selected']+'`\n' for x in active)+'\n蓟珥保留原卷袖与指端少量土迹；绥珥严格使用suier_lot／FX-LOT母图，原右手握半截软尺，不与燧珥混用。两人按本人母图实际比例，不统一套头身数字。\n\n逐字prompt与实际参数在调用前保存；完整工具返回含原始image payload。raw逐字节对应payload及工具保存图。仅清理alpha≤8及隐藏RGB，不改主体像素，不裁切，不量化，不拉伸人物。浅深板只整图nearest等比排版。\n\n'+('绥珥A1首稿半截软尺被明显加长，已用唯一硬错修订恢复原短段及配合手位。首稿、清理候选、完整payload及全部比较图均保留；selected目录包含历史候选，只有manifest的active_selected两张为终选。\n\n' if slug=='suier_lot' else '')+'来源完整副本及SHA在sources；独审原件在review/independent。计划/初始日志中的“未生成/候审”为历史时间点，最终状态见FINAL_STATUS.json。\n\n未Git、未上传、未改冻结母图或旧表情、未改角色卡、游戏或存档。\n')
 sources=[(R/c['mother_image']['transparent'],'母图｜已有设定')]+[(b/x['selected'], ('A1｜' if i==0 else 'A2｜')+x['title_zh']) for i,x in enumerate(active)]
 for theme,bg,fg in [('light',(239,234,222,255),(44,39,34,255)),('dark',(35,40,46,255),(238,233,221,255))]:
  board=Image.new('RGBA',(1800,1040),bg);draw=ImageDraw.Draw(board);draw.text((40,24),f'{c["name"]}  {c["canonical_id"]}｜独立基础动作',font=fnt(36),fill=fg);draw.text((40,80),'本人母图对照 · 单帧概念 · 完整图等比展示',font=fnt(24),fill=fg)
  ls=[]
  for i,(p,label) in enumerate(sources):
   im=Image.open(p).convert('RGBA');w=round(im.width*.5);h=round(im.height*.5);im=im.resize((w,h),Image.Resampling.NEAREST);x=i*600+(600-w)//2;y=165;board.alpha_composite(im,(x,y));draw.text((i*600+25,910),label,font=fnt(26),fill=fg);ls.append({'source':str(p.relative_to(R)),'sha256':sha(p),'original_size':list(Image.open(p).size),'rendered_size':[w,h],'placement':[x,y],'scale':.5,'resample':'nearest','crop':False})
  draw.text((40,984),'保留原衣装与道具；不代表连续动画、装备兼容或游戏内验证',font=fnt(24),fill=fg)
  out=b/'review'/f'{slug}_actions_mother_review_zh_{theme}.png';board.convert('RGB').save(out);layouts.append({'path':str(out.relative_to(R)),'sha256':sha(out),'size':[1800,1040],'background':list(bg),'items':ls});charboards[(slug,theme)]=out
 (b/'review/layout.json').write_text(json.dumps({'boards':[x for x in layouts if '/'+slug+'/' in x['path']]},ensure_ascii=False,indent=2)+'\n')
 files=[{'path':str(p.relative_to(b)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(b.rglob('*')) if p.is_file() and p not in [b/'manifest.json',b/'FINAL_STATUS.json']]
 (b/'manifest.json').write_text(json.dumps({'schema_version':1,'status':'visual_pass_pending_tree_review','character':slug,'active_selected':active,'calls':len(json.loads((b/'generation-log.json').read_text())['calls']),'rejected_initial_count':int(slug=='suier_lot'),'source_index_sha256':sha(b/'sources/source_index.json'),'author_qa_sha256':sha(b/'QA-author.json'),'independent_visual_gate_sha256':sha(gate),'files':files,'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
for theme in ['light','dark']:
 im=Image.new('RGB',(1800,2080));im.paste(Image.open(charboards[('jier',theme)]),(0,0));im.paste(Image.open(charboards[('suier_lot',theme)]),(0,1040));im.save(D/'review'/f'tenth_jier_suier_lot_actions_mother_zh_{theme}.png')
(D/'review/layout.json').write_text(json.dumps({'per_character_boards':layouts,'combined_boards':[{ 'path':f'review/tenth_jier_suier_lot_actions_mother_zh_{theme}.png','size':[1800,2080],'assembled_without_resampling':[str(charboards[(s,theme)].relative_to(R)) for s in ['jier','suier_lot']]} for theme in ['light','dark']]},ensure_ascii=False,indent=2)+'\n')
(D/'README.md').write_text('# 蓟珥／绥珥第十批基础动作\n\n4张终选透明PNG、中文母图对照浅深板。完整源包按人物保存，不丢首稿、废稿、完整工具返回或来源；每包小于18MiB，若分包则合起来是完整树。\n\n范围只为独立静态美术概念；未做动画、装备兼容或运行落地。最终选稿与完整性以冻结清单为准。\n')
shutil.copy2(__file__,D/'scripts'/Path(__file__).name)
print(json.dumps({'delivery':str(D),'boards':[str(p) for p in sorted((D/'review').glob('*.png'))]},ensure_ascii=False,indent=2))
