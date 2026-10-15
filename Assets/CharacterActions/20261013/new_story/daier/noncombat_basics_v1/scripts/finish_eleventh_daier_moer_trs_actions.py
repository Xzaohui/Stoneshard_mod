from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import json,hashlib,datetime,shutil,sys
R=Path('/workspace/scratch/5ed8df2c5d81/Stoneshard_mod');A=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit';ROOT=R/'Assets/CharacterActions/20261013/new_story';D=ROOT/'eleventh_noncombat_daier_moer_trs_delivery_v1';D.mkdir(exist_ok=True)
for x in ['review','selected','scripts']:(D/x).mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();now=datetime.datetime.now(datetime.timezone.utc).isoformat();brief=json.loads((A/'eleventh_new_character_actions_brief.json').read_text());gate=Path(sys.argv[1]);g=json.loads(gate.read_text());assert 'pass' in str(g.get('verdict',g.get('status',''))).lower()
font='/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc';fnt=lambda n:ImageFont.truetype(font,n)
observations={'daier':['双掌分别平贴两侧外套前片、双肘外开，原左手搭右袖接点消失；两手在原画面右腰钥匙上方。','双臂侧下打开成宽轮廓，双手松弛朝内下、与身体分开；原钥匙、外套补片、灰鬓与双鞋保持。'],'moer_trs':['双膝浅屈、髋后下沉、躯干轻前倾，右掌画面左低贴右膝上裤面，低于背后铲刃且无接触；左手继续肩旁握原D柄。','右肘高抬、右掌轻贴本人发顶外缘，眉眼无遮，左手仍握v2背铲，两腿直立、双靴全掌支撑。']}
layouts=[];charboards={}
for c in brief['characters']:
 slug=c['slug']
 if slug not in observations:continue
 b=ROOT/slug/'noncombat_basics_v1';(b/'scripts').mkdir(exist_ok=True)
 for p in ['/workspace/scratch/5ed8df2c5d81/prepare_eleventh_daier_moer_trs_actions.py','/workspace/scratch/5ed8df2c5d81/archive_ninth_actions_image.py',__file__]:shutil.copy2(p,b/'scripts'/Path(p).name)
 shutil.copy2(gate,b/'review/independent'/gate.name)
 for p in sorted((A/'eleventh_actions_independent_details').glob(slug+'_A*')):
  if p.is_file():shutil.copy2(p,b/'review/independent'/p.name)
 active=[]
 for plan,obs in zip(c['plans'],observations[slug]):
  stem=plan['key']+'_initial';p=b/'selected'/f'{stem}_transparent.png';shutil.copy2(p,D/'selected'/p.name);active.append({'key':plan['key'],'title_zh':plan['title_zh'],'stem':stem,'selected':str(p.relative_to(b)),'selected_sha256':sha(p),'visible_result':obs,'independent_verdict':'PASS','revision_used':0})
 (b/'QA-author.json').write_text(json.dumps({'reviewed_utc':now,'scope':'作者自查，不替独立审查','read_and_viewed_sources':{'current_card_and_full_chinese_dialogue':True,'mother_raw_and_transparent':True,'old_expression_board':True},'all_attempt_raw_transparent_selected_light_dark_actually_viewed':True,'active_selected':active,'initial_rejection':None,'revisions_used':0,'not_animation':True,'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
 (b/'README.md').write_text(f'# {c["name"]}｜第十一批基础动作概念\n\n两张独立、可逆的日常全身姿态，只作美术概念。不是连续动画、原生像素帧尺、装备兼容、碰撞或游戏运行验收。\n\n'+''.join('- '+x['title_zh']+'：`'+x['selected']+'`\n' for x in active)+'\n岱珥FX-MAN与达珥分人；谟珥FX-TRS/moer_trs严格使用v2背铲母图，不是摩珥moer。按本人实际年龄比例、原衣装与道具左右，不统一套头身数字；不添加剧情事实。\n\n每姿1首稿，4首稿全部保留，未使用修订。逐字prompt和实际参数调用前保存；完整工具返回含原image payload，raw逐字节等于payload与工具保存图。仅清理alpha≤8和隐藏RGB，不改主体像素，不裁切量化，不拉伸人体。展示只整图nearest等比与真实alpha合成。\n\n来源完整副本及SHA在sources，逐稿和本组独审证据在review/independent。历史计划和日志中的未生成/候审是当时时点，最终状态以FINAL_STATUS为准。未Git、未上传、未改冻结母图表情、角色卡、游戏或存档。\n')
 sources=[(R/c['mother_image']['transparent'],'母图｜已有设定')]+[(b/x['selected'],('A1｜' if i==0 else 'A2｜')+x['title_zh']) for i,x in enumerate(active)]
 for theme,bg,fg in [('light',(239,234,222,255),(44,39,34,255)),('dark',(35,40,46,255),(238,233,221,255))]:
  board=Image.new('RGBA',(1800,1040),bg);draw=ImageDraw.Draw(board);draw.text((40,24),f'{c["name"]}  {c["canonical_id"]}｜独立基础动作',font=fnt(36),fill=fg);draw.text((40,80),'本人母图对照 · 单帧概念 · 完整图等比展示',font=fnt(24),fill=fg);ls=[]
  for i,(p,label) in enumerate(sources):
   src=Image.open(p).convert('RGBA');w=round(src.width*.5);h=round(src.height*.5);im=src.resize((w,h),Image.Resampling.NEAREST);x=i*600+(600-w)//2;y=165;board.alpha_composite(im,(x,y));draw.text((i*600+25,910),label,font=fnt(26),fill=fg);ls.append({'source':str(p.relative_to(R)),'sha256':sha(p),'original_size':list(src.size),'rendered_size':[w,h],'placement':[x,y],'scale':.5,'resample':'nearest','crop':False})
  draw.text((40,984),'保留原衣装与道具；不代表连续动画、装备兼容或游戏内验证',font=fnt(24),fill=fg);out=b/'review'/f'{slug}_actions_mother_review_zh_{theme}.png';board.convert('RGB').save(out);layouts.append({'path':str(out.relative_to(R)),'sha256':sha(out),'size':[1800,1040],'background':list(bg),'items':ls});charboards[(slug,theme)]=out
 (b/'review/layout.json').write_text(json.dumps({'boards':[x for x in layouts if '/'+slug+'/' in x['path']]},ensure_ascii=False,indent=2)+'\n')
 files=[{'path':str(p.relative_to(b)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(b.rglob('*')) if p.is_file() and p not in [b/'manifest.json',b/'FINAL_STATUS.json']]
 (b/'manifest.json').write_text(json.dumps({'schema_version':1,'status':'visual_pass_pending_tree_review','character':slug,'active_selected':active,'calls':2,'rejected_initial_count':0,'source_index_sha256':sha(b/'sources/source_index.json'),'author_qa_sha256':sha(b/'QA-author.json'),'independent_visual_gate_sha256':sha(gate),'files':files,'runtime_verified':False},ensure_ascii=False,indent=2)+'\n')
for theme in ['light','dark']:
 im=Image.new('RGB',(1800,2080));im.paste(Image.open(charboards[('daier',theme)]),(0,0));im.paste(Image.open(charboards[('moer_trs',theme)]),(0,1040));im.save(D/'review'/f'eleventh_daier_moer_trs_actions_mother_zh_{theme}.png')
(D/'review/layout.json').write_text(json.dumps({'per_character_boards':layouts,'combined_boards':[{'path':f'review/eleventh_daier_moer_trs_actions_mother_zh_{theme}.png','size':[1800,2080],'assembled_without_resampling':[str(charboards[(s,theme)].relative_to(R)) for s in ['daier','moer_trs']]} for theme in ['light','dark']]},ensure_ascii=False,indent=2)+'\n')
(D/'README.md').write_text('# 岱珥／谟珥第十一批基础动作\n\n4张透明终选与中文母图浅深对照板，母图不重计。本组每姿1首稿、0修订。完整源包包括全部raw、完整tool return与payload、逐字prompt、实参、相关完整源副本及SHA、作者与独审QA。每ZIP小于18MiB，多包需合看。\n\n只为独立静态美术概念，非连续动画、原生尺寸、装备兼容或运行落地。最终选稿与完整性见冻结清单。未上传或Git。\n')
shutil.copy2(__file__,D/'scripts'/Path(__file__).name)
print(json.dumps({'delivery':str(D),'boards':[str(p) for p in sorted((D/'review').glob('*.png'))]},ensure_ascii=False,indent=2))
