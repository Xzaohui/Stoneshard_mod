import json,hashlib,sys
from pathlib import Path
from datetime import datetime,timezone
root=Path(__file__).resolve().parents[6];audit=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_expression_independent_details';brief=root/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_four_expression_brief.json'
def ref(p):return {'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
notes={
'dalan':{
'identity':'三十出头女子的深棕后束发、成熟颧面、鼻唇与原左向视线保留；本批来自 v2 母图。暗苔绿短披片、金色圆扣、米麻翻袖、棕胸腹护层、灰褐裤与绑靴未改；紧凑头身与双足承重稳定。',
'props':'唯一木弓持续位于画面右、画面右手握中段，另一手仍在腹前靠弦；弦未拉开，未搭箭。画面左肩背唯一箭囊和原浅色箭羽簇数保留。画面右眉眼外缘至颊部浅旧痕保留，双眼完整。',
'E1':'眉内收下压成明显蹙势、眼帘较窄，嘴角轻降并压唇；与母图平静直眉不同，读作克制的不耐夸赞。未画怒吼、羞媚或甜笑。',
'E2':'眉内端轻提、眼神比 E1 开放，嘴小幅分开如低声提醒；不同于母图闭嘴和 E1 皱眉压唇。侧听动作克制，不靠手势冒充表情。',
'story':'未新增哈比、巢、攻击、绳索或背景；不表示受雇、答应带路、D06/N7完成或清剿责任已结。',
'alpha':'作者只将 alpha<=8 设为 RGBA 零；逐像素确认 alpha>8 全部 RGBA 原样保留，无裁切、缩放、量化或重画。独立 raw 浅深合成与最终中文浅深板均无实体底板/广泛光晕。',
'nonblocking':['E2警觉幅度较轻，以眉眼和小幅开嘴共同成立，不能描述成惊恐或攻击预备。']},
'teman':{
'identity':'五十来岁灰发灰须男子，圆鼻与成年面型、左向目光、原紧凑头身和稳站双足一致。米白帽及围布、赭黄短衣、米白下摆、腰带、深褐裤与绑靴保留。',
'props':'网罩两幅始终完整下放围脸，原低密度网格及画面右帽身/右下网缘两块补丁保留，没有掀网、去网或涂黑脸。眉眼嘴在网后可读。双前臂旧皮袖保留，画面右袖的补缝和绑带明确。左手只低收或自然垂近腰、右手保持近腹，无烟具/蜂箱。',
'E1':'母图张口笑谈变为闭合笑线、微上扬唇角及轻松眉眼；笑意温和，瞳仍可见，不是闭眼卡通笑或露齿大笑。',
'E2':'内眉轻聚并提、外眉沉，嘴合成明显下转线，眼神收笑；与母图开口和 E1 闭口会笑都清楚不同，沉重认真可读，不是怒吼或病痛。',
'story':'亡巢只是话题，不补定谁死亡、哪家责任、烧地、蜂群归巢、补偿已付、DT04完成或认领蜂箱。',
'alpha':'raw 与 selected 逐字节相同。透明区有大量 alpha0 隐藏 RGB，直接查看可能显棕色渐层；按真实 alpha 在浅/深底合成均无实体背景或广泛光晕，因此不把隐藏 RGB 判为背景。',
'nonblocking':['E1挑眉与笑眼较克制，闭唇会意清楚；E2偏沉重担忧，未越成夸张悲恸。']},
'erlan':{
'identity':'三十多岁女子的成熟颧面、深棕散发及画面右后方长辫保留，原左向目光和成年体态没有改成幼态。灰橄榄绿开衩麻衣、米白领边/翻袖、腰带及左侧垂带、棕裤和绑靴一致。E1原返回1070×1470，E2为1118×1407，实际头身未明显漂移，未强行拉伸统一。',
'props':'两图画面右侧后腰髋带袋均恰三根浅木尖桩，三个尖端清楚，未拔桩/改成箭囊。双小腿厚棕皮护及各扣保留，双脚仍小步承重。左手保持低位：E1轻指、E2收成松垂手，右手垂侧，未高抬掌或握新工具。',
'E1':'眉心较母图松开、目光轻抬，嘴角微上扬并以小开口说话，显出谈熟悉话题的投入；与母图紧眉下望的警告口型不同。仍保留低指手势，没有用大动作代替表情。',
'E2':'两眉明确内收下压，眼帘较低、嘴唇闭合下压，冷淡坚决可读；与母图开口提醒及 E1 会意口型均不同。无露齿怒吼。',
'story':'只表现聊猎与拒绝为来人撤陷，不新增猎物、陷阱、交易对象、伤兽、撤陷执行、看牲口或DT10已安生结论。',
'alpha':'仅 alpha<=8 清零，逐像素确认 alpha>8 的全部 RGBA 保持原样。实际查看独立 raw 浅深合成与最终中文浅深板，未见实体背景、广泛光晕或轮廓截断。',
'nonblocking':['E1实际画布1070×1470与母图1118×1407不同；保留原返回，无拉伸，人物完整与本人比例成立。','E1小开口有窄牙色，属于克制说话口型，没有形成甜笑或捕杀兴奋；低指没有完全收回，仍在允许的低位范围。']},'fx_cv4_nier':{
'identity':'仅使用 FX-CV4/fx_cv4_nier 本人两母图；三十多岁男子、深灰棕蓬松短发、短须及宽颧成熟脸一致。灰褐旧长褂、米灰领内衫、腰带方扣、褐裤与棕绑带靴保留；各毛边仍是衣物。左向视线、头身和双足稳定站姿保持。',
'props':'唯一短木棍保持收在画面左侧后腰，只露母图短木身；没有拔棍、旋出尖端、变长杖或增加数量，尖端形制仍未核验。左手仍低伸松指、右手自然垂侧，没向观众握手或递物。',
'E1':'眉的紧势松开并呈轻微不对称，嘴闭合成一侧唇角微扬的克制短线；视线仍偏画面左，带局促的推辞感，区别于母图紧眉开口。',
'E2':'眉较平且内聚、眼神凝定向画面左，嘴合成无笑意的平短线；与母图开口说明及 E1非对称淡笑清楚不同，读作沉着专注，未成凶狠怒吼。',
'story':'不显示兽、踪迹数量、新印、清剿、安全保证、皮张归属或受雇守夜。R06兽道形象不演跨区到DT10的R03夜岗。',
'alpha':'raw与selected逐字节相同，未重绘身体、缩放或量化。独立 raw 浅深合成及最终中文浅深板均无实体背景或广泛光晕；alpha0隐藏RGB与極低alpha散点不当成真实底板。',
'nonblocking':['E2原拟左手轻收回腰旁的动作不明显，两图基本保留母图低伸掌；表情本身已明确区分，动作只是辅助，不以此消耗硬错修订。']}
}
slug=sys.argv[1];n=notes[slug];d=root/'Assets/CharacterDesigns/20261013/expressive/new_story'/slug/'expressions_v1';c=next(c for c in json.loads(brief.read_text())['characters'] if c['slug']==slug);chainp=audit/(slug+'_chain_check.json');chain=json.loads(chainp.read_text());assert not chain['failures'];now=datetime.now(timezone.utc).isoformat()
raw={'schema_version':1,'reviewer':'/root/review_ninth_character_expressions','review_type':'independent_raw_visual','created_utc':now,'slug':slug,'canonical_id':c['canonical_id'],'status':'passed','brief':ref(brief),'mother_images_viewed':[c['source_anchor'][k] for k in ['selected_raw','transparent']],'identity_and_proportion':n['identity'],'clothing_props_and_sides':n['props'],'story_scope':n['story'],'alpha_interpretation':n['alpha'],'view_method':'本独审在本轮以 tools.view_image 分别实际查看两张 raw，再实际查看独立生成的正确 RGBA 浅深合成；不以作者文字或旧 QA 替代看图。','poses':[{'id':p['expression'],'label_zh':p['label'],'raw':p['raw'],'status':'passed','face_observation':n[p['expression']],'hard_errors':[],'hard_error_revision_required':False,'reviewer_raw_composite':ref(audit/(slug+'_'+p['expression']+'_raw_light_dark.png'))} for p in chain['poses']],'request_return_source_chain':ref(chainp),'generation_count':chain['calls'],'hard_error_revisions_used':0,'not_claimed':['用户已认可本批','原生游戏像素网格','装备兼容','连续动画','runtime通过']}
(d/'QA-independent-raw-visual.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n')
boards=sorted((d/'review').glob('*zh*.png'))
qa={'schema_version':1,'reviewer':'/root/review_ninth_character_expressions','review_type':'independent_selected_and_presentation','created_utc':now,'slug':slug,'name':c['name'],'canonical_id':c['canonical_id'],'status':'passed','brief':ref(brief),'raw_visual_review':ref(d/'QA-independent-raw-visual.json'),'source_chain_evidence':ref(chainp),'view_method':'本独审分别实际查看两张 selected 与中文浅色/深色成对板，核对完整人物、中文姓名与两情绪标签；manifest SHA 只记此时快照，作者稍后独占终态冻结。','identity_and_proportion':n['identity'],'clothing_props_and_sides':n['props'],'story_scope':n['story'],'alpha_scope':n['alpha'],'poses':[{'id':p['expression'],'label_zh':p['label'],'selected':p['selected'],'status':'passed','face_observation':n[p['expression']],'full_body_and_clearance':'发、双手、双靴及所有必需道具完整，主体可见 alpha 轮廓留边；极低 alpha 散点不等于裁切。','hard_errors':[],'revisions_used':0} for p in chain['poses']],'review_boards':[ref(p) for p in boards],'review_boards_status':'两板姓名/标签正确，完整双人并列各自独立，无文字压住脸、手或道具；浅深底均可读。','manifest_path_at_review':str((d/'manifest.json').relative_to(root)),'manifest_sha256_at_review':chain['manifest']['sha256'],'manifest_entries_verified_at_review':len(chain['manifest_checks']),'source_snapshot_pairs_verified':chain['source_snapshot_pairs'],'nonblocking_notes':n['nonblocking'],'recommendation':'两表情可由作者 solewriter 冻结概念交付；无需硬错修订。','limitations':['仅独立全身表情概念，不是顺序结果或连续动画。','不证明用户已认可、引擎网格、装备组合或游戏运行。'],'mutations':'独审只新增 QA 文件及独审证据；未修改作者图片、prompt、日志、manifest、终态文件或源卡。'}
(d/'QA-independent.json').write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'slug':slug,'raw_qa':ref(d/'QA-independent-raw-visual.json'),'qa':ref(d/'QA-independent.json')},ensure_ascii=False))
