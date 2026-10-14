# 珥兰 第九批基础动作锁定

{
  "slug": "erlan",
  "canonical_id": "FX-HNT",
  "name": "珥兰",
  "status": "planned_not_generated",
  "selection_status": "requested_candidate_retained_no_substitution",
  "current_card": {
    "path": "design/04_人物/野外人物/人物_FX-HNT_珥兰.md",
    "bytes": 1047,
    "sha256": "1b19806af5b5347c5ef0d8d1a52a6672d0f096933e48f53f749b2cd771b3b322",
    "source_id": "erlan_card",
    "snapshot_path": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/files/design/04_人物/野外人物/人物_FX-HNT_珥兰.md"
  },
  "source_ids": [
    "erlan_card",
    "field_dialogue",
    "field_dialogue_registry",
    "DT10",
    "erlan_mother_raw",
    "erlan_mother_transparent",
    "erlan_mother_manifest",
    "erlan_expression_final_status",
    "erlan_expressions_view"
  ],
  "mother_image": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/erlan/concept_v1/raw/erlan_v1_raw_imagegen.png",
    "raw_sha256": "fde8c78def44fb5cb156bb364a2e97ef61c638465b5b428190122f242c0205cd",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/erlan/concept_v1/erlan_transparent.png",
    "transparent_sha256": "271db0a9cb3502210225ae26d0d8b645369cc691d52f65e51723f9bd674d011d",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/erlan/concept_v1/manifest.json",
    "manifest_sha256": "b631090ed5fd222818b2b7dd0f9a2260194d702dd39d02d05d8791448922147d",
    "independent_qa_source_id": "ninth_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "实际查看raw、透明母图及旧表情板：灰绿短褂成年女子，棕长辫在画面右侧。人物右臂画面左低伸指向脚边，左臂画面右低垂；双腿略错步，皮护带扣可见。三根尖木桩一起插在人物左侧后腰、可见为画面右腰髋带袋。旧E1谈猎与E2冷拒主要改脸/低手，未有扶护片或横胸贴上袖。",
    "fixed_sides": "腰后恰好三根母图削尖木桩仍一起收在人物左侧后腰（画面右腰髋）的原带袋内，三个尖头清楚、不拔出、不增减、不换侧；不把带袋移到腹前。原棕辫留在画面右肩后，双腿皮护的数量、绑带、扣和双靴不变。双手只按本张动作改变。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/erlan/expressions_v1/review/erlan_expressions_review_zh_light.png"
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
    "只整理本人皮护外表或衣袖，不解扣、不重新绑带、不插桩、不设陷或撤陷。",
    "不画猎物、牲口、草皮、陷阱、夜岗清剿或DT10完成；不重复指地提醒/谈猎和冷拒表情。"
  ],
  "risks": [
    "A1以掌贴整块护片和明显降髋屈膝验收，不以细扣是否扣上判断。",
    "三桩保持原腰后收纳；抬臂不遮三尖头或把它们变成手中道具。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/erlan/noncombat_basics_v1",
  "plans": [
    {
      "key": "erlan_A1_half_crouch_smooth_right_leg_guard",
      "title_zh": "半蹲抚平右腿皮护",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "erlan_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "腿绑皮护"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-HNT／体貌",
          "line_start": 504,
          "quote": "腰后插着三根削尖的木桩"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体理披/拂衣/抚护片/理袖/扶帽/拢襟/舒展是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图略错步、右手指地姿势开始。",
      "pose": "双脚从母图轻错步改为稳定分站，两膝明显弯曲，臀部向后下方沉到浅半蹲，躯干由髋部前倾。右手不再指地，右掌并拢、广面贴在自己右腿膝下的原皮护前上半片，停在顺平皮护表面的一瞬；不摸小扣，不解任何绑带。左掌平贴本人左大腿膝上裤面作轻扶，左肘朝画面右外开。两靴全掌着地，头随躯干降低而保持原成熟脸和画面左朝向，视线轻落右护片。三木桩始终插在原画面右后腰带袋，三个尖头清楚。",
      "end_pose_description_only": "右掌可离开护片、双腿伸直回站姿；没有扣带开合或装备更换。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "明显屈膝降髋，右掌落在右腿宽皮护片，左掌扶左大腿；必须改变双臂和支撑轮廓。",
      "pose_specific_sidedness": "右掌在画面左的本人右腿皮护，左掌在画面右的本人左大腿；三桩仍画面右后腰。",
      "contact_and_support_checks": [
        "右掌贴一大片原皮护外面，皮护绑带和扣仍闭合。",
        "双膝自然弯、双靴全掌着地，不能跪地、踮脚或画成只弯腰。",
        "左掌轻扶左大腿而不伸进三桩带袋，三尖头保留。"
      ],
      "prop_state_and_retention": [
        "腰后恰好三根母图削尖木桩仍一起收在人物左侧后腰（画面右腰髋）的原带袋内，三个尖头清楚、不拔出、不增减、不换侧；不把带袋移到腹前。原棕辫留在画面右肩后，双腿皮护的数量、绑带、扣和双靴不变。双手只按本张动作改变。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧表情为站立低指或低垂，本张屈膝降髋并两掌分别落到护片/大腿，显著区别。不是插桩、撤陷或绑紧小扣。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/erlan/concept_v1/erlan_transparent.png"
      ],
      "reference_sha256": [
        "271db0a9cb3502210225ae26d0d8b645369cc691d52f65e51723f9bd674d011d"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图紧凑而成熟的成年身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：珥兰 FX-HNT。三十多岁的成年女子；母图棕发长辫在画面右肩后垂下，脸仍朝画面左。灰绿短褂、浅麻翻袖领边、棕腰带、深褐裤、两腿绑带皮护和棕靴完整保留。\n固定衣装与原物件：腰后恰好三根母图削尖木桩仍一起收在人物左侧后腰（画面右腰髋）的原带袋内，三个尖头清楚、不拔出、不增减、不换侧；不把带袋移到腹前。原棕辫留在画面右肩后，双腿皮护的数量、绑带、扣和双靴不变。双手只按本张动作改变。\n本张动作：半蹲抚平右腿皮护。双脚从母图轻错步改为稳定分站，两膝明显弯曲，臀部向后下方沉到浅半蹲，躯干由髋部前倾。右手不再指地，右掌并拢、广面贴在自己右腿膝下的原皮护前上半片，停在顺平皮护表面的一瞬；不摸小扣，不解任何绑带。左掌平贴本人左大腿膝上裤面作轻扶，左肘朝画面右外开。两靴全掌着地，头随躯干降低而保持原成熟脸和画面左朝向，视线轻落右护片。三木桩始终插在原画面右后腰带袋，三个尖头清楚。\n本张侧别：右掌在画面左的本人右腿皮护，左掌在画面右的本人左大腿；三桩仍画面右后腰。\n必须明显可见：明显屈膝降髋，右掌落在右腿宽皮护片，左掌扶左大腿；必须改变双臂和支撑轮廓。\n接触与支撑：右掌贴一大片原皮护外面，皮护绑带和扣仍闭合。；双膝自然弯、双靴全掌着地，不能跪地、踮脚或画成只弯腰。；左掌轻扶左大腿而不伸进三桩带袋，三尖头保留。。\n",
      "prompt_sha256": "94f84fdebb2cd28eddcd9fbf87910cb9659ede16f1c7281bf6add344cea954cf",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/erlan_A1_half_crouch_smooth_right_leg_guard_prompt.txt",
      "negative_constraints": [
        "只整理本人皮护外表或衣袖，不解扣、不重新绑带、不插桩、不设陷或撤陷。",
        "不画猎物、牲口、草皮、陷阱、夜岗清剿或DT10完成；不重复指地提醒/谈猎和冷拒表情。",
        "A1以掌贴整块护片和明显降髋屈膝验收，不以细扣是否扣上判断。",
        "三桩保持原腰后收纳；抬臂不遮三尖头或把它们变成手中道具。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧表情为站立低指或低垂，本张屈膝降髋并两掌分别落到护片/大腿，显著区别。不是插桩、撤陷或绑紧小扣。"
      }
    },
    {
      "key": "erlan_A2_smooth_left_upper_sleeve",
      "title_zh": "右掌横胸理左上袖",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "erlan_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "三十多岁的女子"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-HNT／知情边界",
          "line_start": 508,
          "quote": "不替牧场主看牲口"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体理披/拂衣/抚护片/理袖/扶帽/拢襟/舒展是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图右臂低伸指地的站姿开始。",
      "pose": "双靴自然分开稳站，躯干直立，头仍朝画面左。右臂从原低指位置抬起，右肘离开画面左腰侧，右前臂横过胸前，右掌并拢平贴自己左侧肩下的灰绿上袖外面，停在向下顺平衣袖的一瞬。左臂低垂，左手在画面右腿外可见，远离后腰木桩；掌只接触袖布，不接皮带。原长辫仍落在画面右肩后，三桩完整可见。",
      "end_pose_description_only": "右手可离袖落回身侧，左袖保持原样。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "右前臂完整横胸、右掌清楚落在对侧上袖的大面积布面；左臂保持低垂，和屈膝扶腿姿态不同。",
      "pose_specific_sidedness": "右手从画面左横胸到画面右的本人左上臂；左手画面右低垂，三桩仍同侧后腰。",
      "contact_and_support_checks": [
        "右掌在肩下上袖，不停在胸口、发辫或袖口细扣。",
        "左右肩肘腕各连续，左手低垂清楚，避免第三手。",
        "三桩没有被右手拿出或增加；双脚稳站。"
      ],
      "prop_state_and_retention": [
        "腰后恰好三根母图削尖木桩仍一起收在人物左侧后腰（画面右腰髋）的原带袋内，三个尖头清楚、不拔出、不增减、不换侧；不把带袋移到腹前。原棕辫留在画面右肩后，双腿皮护的数量、绑带、扣和双靴不变。双手只按本张动作改变。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧E1/E2都没有横胸贴上袖；本张站立高位理袖，与半蹲低位护片接触不同。与其他人物理袖属普通动作大类，不声称全库首次。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/erlan/concept_v1/erlan_transparent.png"
      ],
      "reference_sha256": [
        "271db0a9cb3502210225ae26d0d8b645369cc691d52f65e51723f9bd674d011d"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图紧凑而成熟的成年身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：珥兰 FX-HNT。三十多岁的成年女子；母图棕发长辫在画面右肩后垂下，脸仍朝画面左。灰绿短褂、浅麻翻袖领边、棕腰带、深褐裤、两腿绑带皮护和棕靴完整保留。\n固定衣装与原物件：腰后恰好三根母图削尖木桩仍一起收在人物左侧后腰（画面右腰髋）的原带袋内，三个尖头清楚、不拔出、不增减、不换侧；不把带袋移到腹前。原棕辫留在画面右肩后，双腿皮护的数量、绑带、扣和双靴不变。双手只按本张动作改变。\n本张动作：右掌横胸理左上袖。双靴自然分开稳站，躯干直立，头仍朝画面左。右臂从原低指位置抬起，右肘离开画面左腰侧，右前臂横过胸前，右掌并拢平贴自己左侧肩下的灰绿上袖外面，停在向下顺平衣袖的一瞬。左臂低垂，左手在画面右腿外可见，远离后腰木桩；掌只接触袖布，不接皮带。原长辫仍落在画面右肩后，三桩完整可见。\n本张侧别：右手从画面左横胸到画面右的本人左上臂；左手画面右低垂，三桩仍同侧后腰。\n必须明显可见：右前臂完整横胸、右掌清楚落在对侧上袖的大面积布面；左臂保持低垂，和屈膝扶腿姿态不同。\n接触与支撑：右掌在肩下上袖，不停在胸口、发辫或袖口细扣。；左右肩肘腕各连续，左手低垂清楚，避免第三手。；三桩没有被右手拿出或增加；双脚稳站。。\n",
      "prompt_sha256": "9284e8e41c52f8bb218c690966deeedfd99857b9a31ffccc1290de936005a743",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/erlan_A2_smooth_left_upper_sleeve_prompt.txt",
      "negative_constraints": [
        "只整理本人皮护外表或衣袖，不解扣、不重新绑带、不插桩、不设陷或撤陷。",
        "不画猎物、牲口、草皮、陷阱、夜岗清剿或DT10完成；不重复指地提醒/谈猎和冷拒表情。",
        "A1以掌贴整块护片和明显降髋屈膝验收，不以细扣是否扣上判断。",
        "三桩保持原腰后收纳；抬臂不遮三尖头或把它们变成手中道具。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/ninth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧E1/E2都没有横胸贴上袖；本张站立高位理袖，与半蹲低位护片接触不同。与其他人物理袖属普通动作大类，不声称全库首次。"
      }
    }
  ]
}

只按本姿独立prompt调用。母图实比，不套数字。每姿1首稿，最多1次真硬错修订，安全block停止；内置imagegen负责人物，脚本只alpha≤8与隐藏RGB清理、整图nearest等比排版；保全返回payload与所有尝试。不动画、不游戏落地、不Git、不上传。
