from pathlib import Path
import json,hashlib,shutil,datetime
R=Path(__file__).resolve().parents[5];D=Path(__file__).resolve().parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
qa=R/'Assets/CharacterDesigns/20261013/expressive/new_story_audit/independent_third_new_character_actions_kuen_sune_visual_gate_20261014.json';assert sha(qa)=='86a6d18ddeba09cc9dbf98ba0a055e5d4a9e2e57191aea3ccf32460a50c20295'
observations={
'kuen_A1_draw_shawl_edges_in':'两手分别捏住同一披肩前缘，向中间合拢；布料连续至肩背，未增加独立毯子。左手旧青仍原侧；臀部坐实、双足与椅/背卷支撑保留，杯凳布条未碰。',
'kuen_A2_seated_turn_with_seat_contact':'肩胸随头由母图朝画面左斜向转更正面向画面右，右掌落右腿，左手轻搭原椅座边。臀部未离座、左臂未读作锁肘撑起、双足仍原支撑；杯凳布条与背卷保留。',
'sune_A1_reseat_charcoal_in_slot':'右手接正在收回原笔插的一支炭笔，另一支低位留插，总数2。左臂仍抱单块竖板，两栏空白，笔与板未接触，无记录数据或用途授权结果。',
'sune_A2_turn_board_inward_carry':'双手分别接同一木板两端并横置腹前，外向朴素棕色木背，没有新夹具/纸页/数据；两支炭笔均在原右前腰插内，双足完整稳站。'}
for slug in ['kuen','sune']:
 o=R/f'Assets/CharacterActions/20261013/new_story/{slug}/noncombat_basics_v1';c=json.loads((o/'production_brief.json').read_text());assets=[];logs=[]
 assert not (o/'FINAL_STATUS.json').exists()
 for p in c['plans']:
  key=p['key'];stem=key+'_v1';raw=o/'raw'/f'{stem}.png';clean=o/'exports'/f'{stem}_transparent_clean.png';proc=json.loads((o/'raw'/f'{stem}.processing.json').read_text());rec=json.loads((o/'raw'/f'{stem}.receipt.json').read_text())
  assert sha(clean)==proc['output_sha256'];assets.append({'key':key,'title_zh':p['title_zh'],'selected_version':1,'selected':str(clean.relative_to(o)),'selected_sha256':sha(clean),'raw':str(raw.relative_to(o)),'raw_sha256':sha(raw),'kind':'independent_noncombat_fullbody_keypose','animation_claim':False,'story_state_changes':False,'author_visual_observation':observations[key]})
  logs.append({'raw_receipt':str((o/'raw'/f'{stem}.receipt.json').relative_to(o)),'receipt_sha256':sha(o/'raw'/f'{stem}.receipt.json'),'raw_complete_result':rec['complete_tool_result'],'complete_tool_result_sha256':rec['complete_tool_result_sha256'],'prompt':rec['prompt'],'prompt_sha256':rec['prompt_sha256'],'parameters':rec['parameters'],'parameters_sha256':rec['parameters_sha256'],'processing_receipt':str((o/'raw'/f'{stem}.processing.json').relative_to(o)),'processing_sha256':sha(o/'raw'/f'{stem}.processing.json'),'result_file_captured_utc':datetime.datetime.fromtimestamp((o/'raw'/f'{stem}.tool_result.json').stat().st_mtime,datetime.timezone.utc).isoformat(),'prompt_saved_before_result':(o/rec['prompt']).stat().st_mtime<(o/rec['complete_tool_result']).stat().st_mtime,'parameter_saved_before_result':(o/rec['parameters']).stat().st_mtime<(o/rec['complete_tool_result']).stat().st_mtime})
 check=[]
 for s in json.loads((o/'sources/SNAPSHOT_MANIFEST.json').read_text()):
  assert sha(o/s['snapshot'])==s['sha256'];dynamic=Path(s['original']).name=='independent_third_new_character_actions_20261014.json'
  if not dynamic:assert sha(R/s['original'])==s['sha256']
  check.append({'source':s['original'],'snapshot_sha256':s['sha256'],'snapshot_unchanged':True,'original_source_still_matches':sha(R/s['original'])==s['sha256'],'dynamic_review_report':dynamic})
 (o/'sources/source_reverification.json').write_text(json.dumps({'checks':check,'dynamic_report_note':'全8姿态独审汇总由独审者继续更新；调用前gate快照保留不覆盖。终稿以QA-independent.json的本组稳定独审切片为准。'},ensure_ascii=False,indent=2)+'\n')
 (o/'asset_catalog.json').write_text(json.dumps(assets,ensure_ascii=False,indent=2)+'\n');(o/'generation-log.json').write_text(json.dumps(logs,ensure_ascii=False,indent=2)+'\n')
 (o/'QA-author.json').write_text(json.dumps({'reviewer':'draw_kuen_sune_actions','review_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'author_visual_and_provenance_pass','mother_raw_transparent_expression_board_actually_viewed':True,'current_card_read':True,'each_raw_clean_and_light_dark_board_actually_viewed':True,'assets':assets,'complete_original_tool_results_preserved':True,'unchanged_source_sha_reverified':True,'sole_processing':'alpha threshold; nearest-neighbor uniform scale and proper RGBA composition for review only','scope':'静态独立动作，非连续动画/runtime/剧情结果'},ensure_ascii=False,indent=2)+'\n')
 (o/'selection_versions.json').write_text(json.dumps({a['key']:1 for a in assets},ensure_ascii=False,indent=2)+'\n')
 support=o/'delivery_support';support.mkdir(exist_ok=True)
 for p in ['prepare_review.py','prepare_review_original.py','build_delivery_board.py','board_inputs.json','kuen_sune_four_actions_light_dark_board.png']:shutil.copy2(D/p,support/p)
 shutil.copy2(qa,o/'QA-independent.json')
 (o/'README.md').write_text('# '+c['name']+'：两种独立非战斗基础动作\n\n选稿以 asset_catalog.json 的 selected 字段为准：均为 exports/*_transparent_clean.png。exports/*_transparent.png 是保留原字节的未清理历史副本，不能作为另一个动作计数。\n\n每个姿态均通过 builtin imagegen 独立生成，首稿各一次，未用修订。raw/ 保留原图、完整原工具返回（包含原始图像数据）、原始receipt及alpha处理记录；prompts/保留调用前落盘的真实逐字提示词与完整参数。sources/ 保留母图、人物卡、既有表情、关联台本、规则与brief来源快照及哈希。\n\n透明清理仅把原alpha≥128设255、其余设0；RGB、画布尺寸与像素位置完全不变，不画人体、不拉伸、不拼接或强量化。浅深板使用真实RGBA alpha_composite及最近邻等比缩放。\n\n同目录旧production_brief/spec_lock中的planned/pending字样是调用前原始计划快照，不代表终态。最终选稿与冻结结论以FINAL_STATUS.json、manifest.json及QA-independent.json为准。\n\n四姿彼此独立，没有连续动画、过渡、循环、装备组合、原生尺寸/方向/origin或游戏运行验收。动作不证明任何治疗、授权、交接、付款或任务完成。\n')
 print(slug,'author metadata ready')
