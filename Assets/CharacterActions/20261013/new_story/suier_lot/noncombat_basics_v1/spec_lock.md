# 绥珥 第十批基础动作锁定

{
  "slug": "suier_lot",
  "canonical_id": "FX-LOT",
  "name": "绥珥",
  "status": "planned_not_generated",
  "selection_status": "requested_candidate_retained_no_substitution",
  "current_card": {
    "path": "design/04_人物/野外人物/人物_FX-LOT_绥珥.md",
    "bytes": 1065,
    "sha256": "cbbc691c7ec3456de776e2bdfa4a7cb992bf22490539c6d9ae1c59fc67b4a671",
    "source_id": "suier_lot_card",
    "snapshot_path": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/files/design/04_人物/野外人物/人物_FX-LOT_绥珥.md"
  },
  "source_ids": [
    "suier_lot_card",
    "field_dialogue",
    "field_dialogue_registry",
    "SQ03",
    "suier_lot_mother_raw",
    "suier_lot_mother_transparent",
    "suier_lot_mother_manifest",
    "suier_lot_expression_final_status",
    "suier_lot_expressions_view"
  ],
  "mother_image": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/suier_lot/concept_v1/suier_lot_v1_raw_imagegen.png",
    "raw_sha256": "1e6fafb4253d8d8fe1870303f22fa98c3545c2fe00b77b37c26ff29f772802de",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/suier_lot/concept_v1/suier_lot_transparent.png",
    "transparent_sha256": "3983d4b3de284ebe2e48c818f5d587d68051fef615d1d27f4506523038400d25",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/suier_lot/concept_v1/manifest.json",
    "manifest_sha256": "50a0e2c672474077e3501d0a414c9a374ede11cc95745a98ff890e415a44f8b9",
    "independent_qa_source_id": "tenth_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "本任务分别实际查看raw、透明母图与旧表情浅板：四十来岁妇人、棕发画面右低髻、蓝灰颈巾紧结、陶褐长袖长裙与米麻围裙。人物右手（画面左）在腹前握唯一半截软布尺上端，左手（画面右）托右手腕；软尺沿画面右下垂弯，原暗色间隔线和毛边断端可见。旧说起手艺/受疑缄默未改变双手腕前的原轮廓。",
    "fixed_sides": "唯一原半截软布尺的上端始终由人物右手（画面左）握住，右手留在腹前，不换手、不新增第二尺。保留母图原长度、宽度、暗色间隔线和毛边断端；左手仅按本张动作移动。尺只自然软弯，不伸长、不补齐、不拉成硬尺、不变现代卷尺；围巾仍紧结，发髻仍在画面右，衣装原样。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/suier_lot/expressions_v1/review/suier_lot_expressions_light.png"
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
    "只托理本人手中半截软布尺或抚本人围裙，不测量布匹、染缸或他人，不作交付、领取、修复或产权裁决。",
    "不作证、不认领他人财物、不替新主人说话、不确定丈夫去向，不画SQ03完成。",
    "绥珥suier_lot/FX-LOT与燧珥suier/FX-CP1严格分人；不能引用燧珥母图或动作。"
  ],
  "risks": [
    "A1左掌接的是软尺下段宽面，右手仍握原上端；毛边断端要外露，不靠微小刻度读数作目标。",
    "A2左掌与布尺之间留清楚空隙，不能一手既托腕又抚围裙；尺仍保持原软弯和长度。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/suier_lot/noncombat_basics_v1",
  "plans": [
    {
      "key": "suier_lot_A1_support_half_cloth_tape",
      "title_zh": "双手托理半截布尺",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "suier_lot_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "手里攥着半截布尺"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-LOT／知情边界",
          "line_start": 732,
          "quote": "不认领别人家的东西"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托篮/扶巾/理袖/扶腰/舒肩/半蹲/托尺/拂围裙是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图右手握尺上端、左手托右腕的站姿开始。",
      "pose": "双鞋稳站，右手仍在画面左的腹前握住原半截软布尺上端，握物手不换侧。左手从托右手腕的位置向画面右外移，左肘稍外开、左前臂展开，左掌朝上托住同一半截软布尺下半段的宽布面，让尺在两手之间自然形成一个浅软弧。毛边断端从左掌外侧短短垂出、保持可见；原尺长度不增加、不绷直、不修补。两手之间有清楚距离，动作是自己托理原物，不伸向画外、不测量任何东西。头脸仍朝画面左、表情平常。",
      "end_pose_description_only": "左掌可离开布尺下段，原半截尺自然垂回；右手全程仍握上端。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "左前臂向画面右明显展开、左掌托尺下段，双手分开，软尺形成可见浅弧且断端外露；不能仍托原右腕。",
      "pose_specific_sidedness": "人物右手画面左保持握上端；左手移到画面右托下段，尺仍从画面左腹前通向画面右，不换手。",
      "contact_and_support_checks": [
        "仍只有一条原半截尺，两手只接这一条，上端与毛边断端均可追踪。",
        "左掌托宽布面，毛边短端在掌外可见，不把尺拉长或拉成硬直线。",
        "右手不变成双手各持一条尺，围巾紧结原样、双脚稳定。"
      ],
      "prop_state_and_retention": [
        "唯一原半截软布尺的上端始终由人物右手（画面左）握住，右手留在腹前，不换手、不新增第二尺。保留母图原长度、宽度、暗色间隔线和毛边断端；左手仅按本张动作移动。尺只自然软弯，不伸长、不补齐、不拉成硬尺、不变现代卷尺；围巾仍紧结，发髻仍在画面右，衣装原样。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧表情左手只是托右腕、尺自由垂下，本张左手移开托尺下段并形成浅弧；是物件操作而非脸部微调。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/suier_lot/concept_v1/suier_lot_transparent.png"
      ],
      "reference_sha256": [
        "3983d4b3de284ebe2e48c818f5d587d68051fef615d1d27f4506523038400d25"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：绥珥 FX-LOT。四十来岁的成熟妇人，裁缝宅子亲属；母图棕发、画面右低髻、成熟略尖下颌，脸朝画面左。暗蓝灰围巾在颈前紧结，陶褐长袖长裙、米麻围裙和深棕闭口鞋完整保留。只用绥珥 FX-LOT / suier_lot，不是燧珥 FX-CP1 / suier。\n固定衣装与原物件：唯一原半截软布尺的上端始终由人物右手（画面左）握住，右手留在腹前，不换手、不新增第二尺。保留母图原长度、宽度、暗色间隔线和毛边断端；左手仅按本张动作移动。尺只自然软弯，不伸长、不补齐、不拉成硬尺、不变现代卷尺；围巾仍紧结，发髻仍在画面右，衣装原样。\n本张动作：双手托理半截布尺。双鞋稳站，右手仍在画面左的腹前握住原半截软布尺上端，握物手不换侧。左手从托右手腕的位置向画面右外移，左肘稍外开、左前臂展开，左掌朝上托住同一半截软布尺下半段的宽布面，让尺在两手之间自然形成一个浅软弧。毛边断端从左掌外侧短短垂出、保持可见；原尺长度不增加、不绷直、不修补。两手之间有清楚距离，动作是自己托理原物，不伸向画外、不测量任何东西。头脸仍朝画面左、表情平常。\n本张侧别：人物右手画面左保持握上端；左手移到画面右托下段，尺仍从画面左腹前通向画面右，不换手。\n必须明显可见：左前臂向画面右明显展开、左掌托尺下段，双手分开，软尺形成可见浅弧且断端外露；不能仍托原右腕。\n接触与支撑：仍只有一条原半截尺，两手只接这一条，上端与毛边断端均可追踪。；左掌托宽布面，毛边短端在掌外可见，不把尺拉长或拉成硬直线。；右手不变成双手各持一条尺，围巾紧结原样、双脚稳定。。\n",
      "prompt_sha256": "d794ebba9551695734f599af79b228aa3cd49615cc117218d29e1be3839a3cae",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/suier_lot_A1_support_half_cloth_tape_prompt.txt",
      "negative_constraints": [
        "只托理本人手中半截软布尺或抚本人围裙，不测量布匹、染缸或他人，不作交付、领取、修复或产权裁决。",
        "不作证、不认领他人财物、不替新主人说话、不确定丈夫去向，不画SQ03完成。",
        "绥珥suier_lot/FX-LOT与燧珥suier/FX-CP1严格分人；不能引用燧珥母图或动作。",
        "A1左掌接的是软尺下段宽面，右手仍握原上端；毛边断端要外露，不靠微小刻度读数作目标。",
        "A2左掌与布尺之间留清楚空隙，不能一手既托腕又抚围裙；尺仍保持原软弯和长度。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧表情左手只是托右腕、尺自由垂下，本张左手移开托尺下段并形成浅弧；是物件操作而非脸部微调。"
      }
    },
    {
      "key": "suier_lot_A2_smooth_left_apron_panel",
      "title_zh": "左掌下拂围裙",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "suier_lot_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "四十来岁的妇人，围巾结得紧"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-LOT／知情边界",
          "line_start": 732,
          "quote": "不替宅子新主人说话"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托篮/扶巾/理袖/扶腰/舒肩/半蹲/托尺/拂围裙是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图右手握尺、左手托右腕的站姿开始。",
      "pose": "双鞋分开稳站，躯干从髋部轻向前倾。右手仍在画面左腹前握原半截软布尺上端，尺按母图软弯向画面右下自然垂着、长度不变。左手完全离开原托右腕的位置，左臂向下伸，左掌自然并拢，平贴本人左腿膝上高度、米麻围裙画面右侧靠外的一大片布面，停在向下顺平围裙的一瞬。左掌与尺的毛边断端之间留清楚空隙，不同时托尺；围裙只轻折不掀高，长裙和鞋完整。头脸朝画面左、神态平常，紧结围巾不动。",
      "end_pose_description_only": "左掌可离开围裙放回身侧；布尺和衣装没有修补或交付结果。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "左臂明确低伸到膝上外侧围裙，左掌贴宽布面，躯干轻前倾；原右手仍腹前持尺。",
      "pose_specific_sidedness": "右手在画面左腹前握尺上端，尺仍向画面右下软垂；左掌在画面右更低更外侧的本人左腿前围裙，二者不接触。",
      "contact_and_support_checks": [
        "左掌贴围裙宽面，不抓尺、不托右腕、不掀裙，不能留下第三手。",
        "原半截尺保持一条、原长度及毛边断端，并与左掌有可读空隙。",
        "身体前倾由双脚支撑，围巾仍紧结，头发和双鞋完整。"
      ],
      "prop_state_and_retention": [
        "唯一原半截软布尺的上端始终由人物右手（画面左）握住，右手留在腹前，不换手、不新增第二尺。保留母图原长度、宽度、暗色间隔线和毛边断端；左手仅按本张动作移动。尺只自然软弯，不伸长、不补齐、不拉成硬尺、不变现代卷尺；围巾仍紧结，发髻仍在画面右，衣装原样。"
      ],
      "difference_from_mother_expression_and_batch": "旧母图/表情左手在腹前托右腕；本张左手低到膝上围裙并轻前倾，与双手托尺的展开手位区别明确。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/suier_lot/concept_v1/suier_lot_transparent.png"
      ],
      "reference_sha256": [
        "3983d4b3de284ebe2e48c818f5d587d68051fef615d1d27f4506523038400d25"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：绥珥 FX-LOT。四十来岁的成熟妇人，裁缝宅子亲属；母图棕发、画面右低髻、成熟略尖下颌，脸朝画面左。暗蓝灰围巾在颈前紧结，陶褐长袖长裙、米麻围裙和深棕闭口鞋完整保留。只用绥珥 FX-LOT / suier_lot，不是燧珥 FX-CP1 / suier。\n固定衣装与原物件：唯一原半截软布尺的上端始终由人物右手（画面左）握住，右手留在腹前，不换手、不新增第二尺。保留母图原长度、宽度、暗色间隔线和毛边断端；左手仅按本张动作移动。尺只自然软弯，不伸长、不补齐、不拉成硬尺、不变现代卷尺；围巾仍紧结，发髻仍在画面右，衣装原样。\n本张动作：左掌下拂围裙。双鞋分开稳站，躯干从髋部轻向前倾。右手仍在画面左腹前握原半截软布尺上端，尺按母图软弯向画面右下自然垂着、长度不变。左手完全离开原托右腕的位置，左臂向下伸，左掌自然并拢，平贴本人左腿膝上高度、米麻围裙画面右侧靠外的一大片布面，停在向下顺平围裙的一瞬。左掌与尺的毛边断端之间留清楚空隙，不同时托尺；围裙只轻折不掀高，长裙和鞋完整。头脸朝画面左、神态平常，紧结围巾不动。\n本张侧别：右手在画面左腹前握尺上端，尺仍向画面右下软垂；左掌在画面右更低更外侧的本人左腿前围裙，二者不接触。\n必须明显可见：左臂明确低伸到膝上外侧围裙，左掌贴宽布面，躯干轻前倾；原右手仍腹前持尺。\n接触与支撑：左掌贴围裙宽面，不抓尺、不托右腕、不掀裙，不能留下第三手。；原半截尺保持一条、原长度及毛边断端，并与左掌有可读空隙。；身体前倾由双脚支撑，围巾仍紧结，头发和双鞋完整。。\n",
      "prompt_sha256": "818ee8e3128fcc0f204c239aa8620d658b244eb246673c77f60f73532179c2d3",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/suier_lot_A2_smooth_left_apron_panel_prompt.txt",
      "negative_constraints": [
        "只托理本人手中半截软布尺或抚本人围裙，不测量布匹、染缸或他人，不作交付、领取、修复或产权裁决。",
        "不作证、不认领他人财物、不替新主人说话、不确定丈夫去向，不画SQ03完成。",
        "绥珥suier_lot/FX-LOT与燧珥suier/FX-CP1严格分人；不能引用燧珥母图或动作。",
        "A1左掌接的是软尺下段宽面，右手仍握原上端；毛边断端要外露，不靠微小刻度读数作目标。",
        "A2左掌与布尺之间留清楚空隙，不能一手既托腕又抚围裙；尺仍保持原软弯和长度。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "旧母图/表情左手在腹前托右腕；本张左手低到膝上围裙并轻前倾，与双手托尺的展开手位区别明确。"
      }
    }
  ]
}

只按本姿独立prompt调用。母图实比，不套数字。每姿1首稿，最多1次真硬错修订，安全block停止；内置imagegen负责人物，脚本只alpha≤8与隐藏RGB清理、整图nearest等比排版；保全返回payload与所有尝试。不动画、不游戏落地、不Git、不上传。
