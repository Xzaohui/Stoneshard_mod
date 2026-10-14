# 妲兰 第九批基础动作锁定

{
  "slug": "dalan",
  "canonical_id": "FX-HRP",
  "name": "妲兰",
  "status": "planned_not_generated",
  "selection_status": "requested_candidate_retained_no_substitution",
  "current_card": {
    "path": "design/04_人物/野外人物/人物_FX-HRP_妲兰.md",
    "bytes": 1046,
    "sha256": "e944360f7e224a66396212b01110dc1a117f6700da1a69adce3922d9d983b42b",
    "source_id": "dalan_card",
    "snapshot_path": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/files/design/04_人物/野外人物/人物_FX-HRP_妲兰.md"
  },
  "source_ids": [
    "dalan_card",
    "field_dialogue",
    "field_dialogue_registry",
    "D06",
    "dalan_mother_raw",
    "dalan_mother_transparent",
    "dalan_mother_manifest",
    "dalan_expression_final_status",
    "dalan_expressions_view"
  ],
  "mother_image": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/dalan/concept_v1/raw/dalan_v2_raw_imagegen.png",
    "raw_sha256": "3bd277f33601d966e1900116ba8cb2e2ef1b70e42eb69ec44c0c0fdeb1131463",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/dalan/concept_v1/dalan_transparent.png",
    "transparent_sha256": "4d013aefc9293ae2b9320a7e6892967e83eb24f704b16ce056ce43b26710d98a",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/dalan/concept_v1/manifest.json",
    "manifest_sha256": "2da79b28bb8efee395787994816f6a47ec50f04d329987c2c2fdc10513ccde80",
    "independent_qa_source_id": "ninth_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "实际查看v2 raw、透明母图及旧表情板：成熟成年女猎人，深棕盘束发、画面右眉侧旧痕；绿短披、浅麻衣、两层棕腰扣、皮护腕和棕靴。人物左手在画面右握竖立长弓中段，右手在腹前靠弓弦。箭囊和原箭羽在画面左肩后。两张旧表情都保留持弓/近弦的手位，区别为闻夸蹙眉与侧听警觉。母图必须选v2，不回用修订前v1。",
    "fixed_sides": "人物左手（画面右）始终握住母图同一把棕木长弓的原中段握柄，弓在身体画面右侧近竖直、上下弓梢完整；原一根弓弦仍连接两端并保持未拉开状态。箭囊和原有箭羽始终在画面左肩后，数量/形状照母图；不取箭、不搭箭、不拉弦、不新增第二弓。绿披、腰扣、护腕与双靴保持。右手仅按本张动作移动。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/dalan/expressions_v1/review/dalan_expressions_review_zh_light.png"
  },
  "existing_expressions": {
    "status": "final_clean_and_presentation_pass",
    "qualified_count": 2,
    "not_action_coverage": true
  },
  "duplicate_check": {
    "own_action_directory_count": 0,
    "own_action_semantic_match_found": false,
    "existing_expressions_actually_compared": true,
    "interpretation": "只将本人新身体/肢体/接触变化计动作；母图、表情和来源副本不重计。普通动作大类可跨人物出现，不声称全库首次。"
  },
  "story_boundaries": [
    "只是闭口的短暂自理片刻，右手暂离弦；不演说话状态，不改源卡“说话时手一直搭在弓弦上”的习惯。",
    "不画射击、瞄准、狩猎、带人上崖、哈比巢或D06结果；原弓和箭仍由本人原方式持有/背载。"
  ],
  "risks": [
    "弓保持完整未拉开，动作判据是宽掌贴披面/衣摆，不以几像素弓弦指尖接点作新目标。",
    "右手不能同时留在原弦边又出现在新接点；画面右眉侧原浅痕只是已有美术特征，不扩成新伤。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/dalan/noncombat_basics_v1",
  "plans": [
    {
      "key": "dalan_A1_smooth_right_shoulder_cape",
      "title_zh": "右掌轻理右肩披面",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "dalan_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "肩背箭囊"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-HRP／体貌，仅约束说话时习惯；本张闭口自理",
          "line_start": 280,
          "quote": "说话时手一直搭在弓弦上"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体理披/拂衣/抚护片/理袖/扶帽/拢襟/舒展是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "从母图持弓、右手近弦的姿态开始；暂时停止说话。",
      "pose": "双靴原位分开站稳，左手仍在画面右握住原竖弓中段。闭口自理片刻，右手完全离开腹前弓弦，右肘朝画面左外抬，右前臂斜向上，右掌和并拢指组平贴自己的右肩前侧、锁骨外侧的绿披宽布面，停在顺平披肩的一瞬。接触点位于画面左肩前，避开颈口扣、箭羽和脸；原披肩不脱离肩膀，箭囊仍在同肩后。弓弦不拉开，右手不再留在弦边。头脸保持母图朝向，嘴轻合、神态平静。",
      "end_pose_description_only": "右手可离开肩披并回原弦旁；未改变弓箭收纳。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "右肘明确外抬，整条右前臂从腹前移到肩前，宽掌接触绿色肩披；左手原竖弓仍完整。",
      "pose_specific_sidedness": "右掌位于画面左的本人右肩前绿披；左手位于画面右握原弓，箭羽仍画面左肩后。",
      "contact_and_support_checks": [
        "右掌广面贴肩披而不伸进颈口，不遮脸和箭羽。",
        "右手从原弦边完全移走，不留下第三手；弓仍由左手稳握。",
        "双脚全掌着地，肩披/箭囊/弓弦均保持原连属。"
      ],
      "prop_state_and_retention": [
        "人物左手（画面右）始终握住母图同一把棕木长弓的原中段握柄，弓在身体画面右侧近竖直、上下弓梢完整；原一根弓弦仍连接两端并保持未拉开状态。箭囊和原有箭羽始终在画面左肩后，数量/形状照母图；不取箭、不搭箭、不拉弦、不新增第二弓。绿披、腰扣、护腕与双靴保持。右手仅按本张动作移动。"
      ],
      "difference_from_mother_expression_and_batch": "母图和旧E1/E2右手均在腹前弦边，本张右肘高抬、掌贴右肩披。与低位拂衣摆的另一独立动作在整条手臂高度和接触区域上不同。",
      "risk_level": "medium_pose_and_contact",
      "new_contact_prop": null,
      "new_story_fact": false,
      "sequence_required": false,
      "animation_claim": false,
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "revision_only_for": "真实、明确且可定位的身份、人体、原物数量/侧别、目标动作、接触支撑、比例、裁切或透明硬错。",
        "after_failed_revision": "全部尝试保留，失败标缺项；不得第三稿、脚本修人体或改动作名继续。",
        "safety_blocked": "立即停止该动作并记录工具返回；不重试、不换工具、不改写规避。"
      },
      "review_status": "planning_author_checked; independent_plan_review_pending",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/dalan/concept_v1/dalan_transparent.png"
      ],
      "reference_sha256": [
        "4d013aefc9293ae2b9320a7e6892967e83eb24f704b16ce056ce43b26710d98a"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图紧凑而成熟的成年身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：妲兰 FX-HRP。三十出头的成年女子；深棕盘束乱发、画面右眉侧向颊延伸的原浅旧痕、原成熟脸型，脸仍朝画面左。橄榄绿短肩披、浅麻衣袖与下摆、棕皮胸腰束带和护腕、暗裤及棕靴保持。\n固定衣装与原物件：人物左手（画面右）始终握住母图同一把棕木长弓的原中段握柄，弓在身体画面右侧近竖直、上下弓梢完整；原一根弓弦仍连接两端并保持未拉开状态。箭囊和原有箭羽始终在画面左肩后，数量/形状照母图；不取箭、不搭箭、不拉弦、不新增第二弓。绿披、腰扣、护腕与双靴保持。右手仅按本张动作移动。\n本张动作：右掌轻理右肩披面。双靴原位分开站稳，左手仍在画面右握住原竖弓中段。闭口自理片刻，右手完全离开腹前弓弦，右肘朝画面左外抬，右前臂斜向上，右掌和并拢指组平贴自己的右肩前侧、锁骨外侧的绿披宽布面，停在顺平披肩的一瞬。接触点位于画面左肩前，避开颈口扣、箭羽和脸；原披肩不脱离肩膀，箭囊仍在同肩后。弓弦不拉开，右手不再留在弦边。头脸保持母图朝向，嘴轻合、神态平静。\n本张侧别：右掌位于画面左的本人右肩前绿披；左手位于画面右握原弓，箭羽仍画面左肩后。\n必须明显可见：右肘明确外抬，整条右前臂从腹前移到肩前，宽掌接触绿色肩披；左手原竖弓仍完整。\n接触与支撑：右掌广面贴肩披而不伸进颈口，不遮脸和箭羽。；右手从原弦边完全移走，不留下第三手；弓仍由左手稳握。；双脚全掌着地，肩披/箭囊/弓弦均保持原连属。。\n",
      "prompt_sha256": "194f23ec83906c8a9dfa876263e27c9612e4a15e08d2aaa28ac9c88ce069c446",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/dalan_A1_smooth_right_shoulder_cape_prompt.txt",
      "negative_constraints": [
        "只是闭口的短暂自理片刻，右手暂离弦；不演说话状态，不改源卡“说话时手一直搭在弓弦上”的习惯。",
        "不画射击、瞄准、狩猎、带人上崖、哈比巢或D06结果；原弓和箭仍由本人原方式持有/背载。",
        "弓保持完整未拉开，动作判据是宽掌贴披面/衣摆，不以几像素弓弦指尖接点作新目标。",
        "右手不能同时留在原弦边又出现在新接点；画面右眉侧原浅痕只是已有美术特征，不扩成新伤。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图和旧E1/E2右手均在腹前弦边，本张右肘高抬、掌贴右肩披。与低位拂衣摆的另一独立动作在整条手臂高度和接触区域上不同。"
      }
    },
    {
      "key": "dalan_A2_smooth_right_tunic_hem",
      "title_zh": "右掌下拂右侧衣摆",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "dalan_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "三十出头的女子"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-HRP／任务进行中，仅作日常衣物动作联想，不表示到过地窖",
          "line_start": 302,
          "quote": "先掸干净，崖上闻得出。"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体理披/拂衣/抚护片/理袖/扶帽/拢襟/舒展是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图站姿开始，右手尚在弦旁。",
      "pose": "双靴分开站稳，躯干从髋部轻向前倾，头脸仍朝画面左。闭口自理片刻，右臂由腹前弦旁落下，右掌自然并拢，平贴本人右大腿前、棕腰带以下的浅麻衣摆大片布面，停在向下拂平的一瞬；右肘低垂在画面左，衣摆轻折但不掀高。左手在画面右仍握原竖弓中段，弓跟随左臂轻移保持完整并位于身体外侧，弓梢不扎地、不穿靴。原弓弦未拉开，箭囊原位。嘴轻合，不表现讲解或警告。",
      "end_pose_description_only": "右掌可离开衣摆回到原弦旁，衣物与弓箭仍原样。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "右掌明显低于腰带并贴在右大腿前浅色衣摆，右臂低伸，躯干轻前倾；不能仍停在腹前弦旁。",
      "pose_specific_sidedness": "右手在画面左的本人右大腿前衣摆；左手在画面右持竖弓；不交换手或箭囊侧别。",
      "contact_and_support_checks": [
        "右掌贴浅色布面，不改为腰带扣或棕皮带上的小接点。",
        "左手原弓完整，弓底端与靴不相穿，不以杵地作为支撑。",
        "身体前倾仍由双脚稳稳支撑，不缩短身体来制造低手位。"
      ],
      "prop_state_and_retention": [
        "人物左手（画面右）始终握住母图同一把棕木长弓的原中段握柄，弓在身体画面右侧近竖直、上下弓梢完整；原一根弓弦仍连接两端并保持未拉开状态。箭囊和原有箭羽始终在画面左肩后，数量/形状照母图；不取箭、不搭箭、不拉弦、不新增第二弓。绿披、腰扣、护腕与双靴保持。右手仅按本张动作移动。"
      ],
      "difference_from_mother_expression_and_batch": "母图及旧表情没有右掌贴大腿衣摆、躯干前倾的动作；与右手高到肩披的姿态相区分，不把“掸干净”对白当作剧情已执行。",
      "risk_level": "medium_pose_and_contact",
      "new_contact_prop": null,
      "new_story_fact": false,
      "sequence_required": false,
      "animation_claim": false,
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "revision_only_for": "真实、明确且可定位的身份、人体、原物数量/侧别、目标动作、接触支撑、比例、裁切或透明硬错。",
        "after_failed_revision": "全部尝试保留，失败标缺项；不得第三稿、脚本修人体或改动作名继续。",
        "safety_blocked": "立即停止该动作并记录工具返回；不重试、不换工具、不改写规避。"
      },
      "review_status": "planning_author_checked; independent_plan_review_pending",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/dalan/concept_v1/dalan_transparent.png"
      ],
      "reference_sha256": [
        "4d013aefc9293ae2b9320a7e6892967e83eb24f704b16ce056ce43b26710d98a"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图紧凑而成熟的成年身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：妲兰 FX-HRP。三十出头的成年女子；深棕盘束乱发、画面右眉侧向颊延伸的原浅旧痕、原成熟脸型，脸仍朝画面左。橄榄绿短肩披、浅麻衣袖与下摆、棕皮胸腰束带和护腕、暗裤及棕靴保持。\n固定衣装与原物件：人物左手（画面右）始终握住母图同一把棕木长弓的原中段握柄，弓在身体画面右侧近竖直、上下弓梢完整；原一根弓弦仍连接两端并保持未拉开状态。箭囊和原有箭羽始终在画面左肩后，数量/形状照母图；不取箭、不搭箭、不拉弦、不新增第二弓。绿披、腰扣、护腕与双靴保持。右手仅按本张动作移动。\n本张动作：右掌下拂右侧衣摆。双靴分开站稳，躯干从髋部轻向前倾，头脸仍朝画面左。闭口自理片刻，右臂由腹前弦旁落下，右掌自然并拢，平贴本人右大腿前、棕腰带以下的浅麻衣摆大片布面，停在向下拂平的一瞬；右肘低垂在画面左，衣摆轻折但不掀高。左手在画面右仍握原竖弓中段，弓跟随左臂轻移保持完整并位于身体外侧，弓梢不扎地、不穿靴。原弓弦未拉开，箭囊原位。嘴轻合，不表现讲解或警告。\n本张侧别：右手在画面左的本人右大腿前衣摆；左手在画面右持竖弓；不交换手或箭囊侧别。\n必须明显可见：右掌明显低于腰带并贴在右大腿前浅色衣摆，右臂低伸，躯干轻前倾；不能仍停在腹前弦旁。\n接触与支撑：右掌贴浅色布面，不改为腰带扣或棕皮带上的小接点。；左手原弓完整，弓底端与靴不相穿，不以杵地作为支撑。；身体前倾仍由双脚稳稳支撑，不缩短身体来制造低手位。。\n",
      "prompt_sha256": "8616332d65dcaeb2de61281f2a5028897092a2c83cfbf3ea0670354b98eefef8",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/dalan_A2_smooth_right_tunic_hem_prompt.txt",
      "negative_constraints": [
        "只是闭口的短暂自理片刻，右手暂离弦；不演说话状态，不改源卡“说话时手一直搭在弓弦上”的习惯。",
        "不画射击、瞄准、狩猎、带人上崖、哈比巢或D06结果；原弓和箭仍由本人原方式持有/背载。",
        "弓保持完整未拉开，动作判据是宽掌贴披面/衣摆，不以几像素弓弦指尖接点作新目标。",
        "右手不能同时留在原弦边又出现在新接点；画面右眉侧原浅痕只是已有美术特征，不扩成新伤。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图及旧表情没有右掌贴大腿衣摆、躯干前倾的动作；与右手高到肩披的姿态相区分，不把“掸干净”对白当作剧情已执行。"
      }
    }
  ]
}

只按本姿独立prompt调用。母图实比，不套数字。每姿1首稿，最多1次真硬错修订，安全block停止；内置imagegen负责人物，脚本只alpha≤8与隐藏RGB清理、整图nearest等比排版；保全返回payload与所有尝试。不动画、不游戏落地、不Git、不上传。
