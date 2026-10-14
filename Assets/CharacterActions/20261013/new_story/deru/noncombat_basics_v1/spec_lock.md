# 本轮独立非战斗关键姿态执行锁

只生产本人物2个独立全身动作概念，不制作动画、GIF、装备或runtime素材。首稿每姿态1次，至多1次硬错修订，安全blocked即停，不绕过。builtin imagegen为唯一绘图工具。脚本仅alpha清理及等比最近邻排版，不画身体、不拉伸、不强量化。完整真实prompt、工具原返回和SHA独立保存。已读取当前卡、STYLE_DIRECTION及raw和透明母图。

{
  "slug": "deru",
  "canonical_id": "FX-QRY",
  "name": "德茹",
  "status": "planned_only_not_generated",
  "selection_status": "requested_candidate_suitable_retained",
  "source_card_hash_matches_roster44": true,
  "source_ids": [
    "deru_card",
    "deru_manifest",
    "deru_spec_lock",
    "deru_character_brief",
    "deru_expression_manifest",
    "deru_expression_board",
    "deru_raw",
    "deru_anchor",
    "qa_first",
    "field_dialogue",
    "field_script"
  ],
  "mother_image": {
    "path": "Assets/CharacterDesigns/20261013/expressive/new_story/deru/concept_v1/deru_transparent.png",
    "sha256": "9a335a68915943a6c2c01b8aa30c6a49248b3a5c3e837d39076b6c3c57ec5f8c",
    "raw_path": "Assets/CharacterDesigns/20261013/expressive/new_story/deru/concept_v1/deru_v2_raw_imagegen.png",
    "raw_sha256": "0dfc9b5caa66f636ca853b76c9a1a46c597862c64d59d2b2fbe0372e2b21c8e3",
    "size": [
      1118,
      1407
    ],
    "mode": "RGBA",
    "raw_and_transparent_actually_viewed": true,
    "viewed_utc": "2026-10-14T03:03:55Z",
    "hashes_match_manifest_and_independent_qa": true,
    "existing_expression_board_actually_viewed": true,
    "old_pose": "直站，右手向画面左下示意，左手近左围裙凿子。表情E1收下右手，E2腰下摊右掌，凿子均未取出。",
    "identity_lock": "约五十岁的女石工，灰白夹深发后束、熟龄厚下颌、粗指节、结实紧凑成年身体；灰粗布衣、赭棕长围裙、棕靴。人物右肩（画面左）略低于左肩，保留自然旧姿态，不画疼痛或新伤。",
    "side_lock": "唯一磨秃凿子平时别在人物左侧围裙（画面右）；左右按人物解剖侧，不镜像。只有A1左手取用该凿；A2原位收好。"
  },
  "duplicate_check": {
    "own_existing_branches": [
      "concept_v1",
      "expressions_v1"
    ],
    "own_action_directories_found": [],
    "non_source_action_metadata_matches": [],
    "existing_expressions_actually_viewed": true,
    "do_not_recount": [
      "concept_v1母图",
      "expressions_v1情绪与小手势",
      "复制source/交付包内的母图",
      "仅表情或不改变接触/手脚结构的小变化"
    ]
  },
  "story_boundaries": [
    "不下坑探路、不复工、不宣布欠薪清偿、不替石场主认领人或石料；不知道军务调动。",
    "仅日常自有工具与衣物动作；查凿不等于磨锋利，低蹲不指向任何已发现证据。"
  ],
  "risks": [
    "高龄不能幼化成灰发少女；保持粗指节与自然右低肩。",
    "凿子取用后原挂位必须为空；不增锤、磨石、石料或修磨火花。",
    "拢裙不是掀衣暴露、下坑许可或越塌方线；双靴和内层灰衣保持完整。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/deru/noncombat_basics_v1",
  "plans": [
    {
      "key": "deru_A1_check_blunt_chisel",
      "title_zh": "双手近身查看钝凿",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "deru_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "围裙上别着一把磨秃的凿子。"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-QRY / chats[1]",
          "line_start": 44,
          "quote": "凿子钝了能磨，人手散了磨不回来。"
        }
      ],
      "art_inference": "源文支持身份、物件或习惯；手位、重心、起止姿势及所选瞬间为可逆动作设计，不冒充台本中已经发生的事件。",
      "start_pose_description_only": "稳站，凿子仍别在人物左侧围裙，双臂收近；左手先握柄取出，右手随后托稳工具中部。",
      "pose": "双脚原地分开稳立，左肘贴近肋侧，左手从原左侧围裙取出同一磨秃凿子并握住木柄，在腰上方斜横持；右手从下托住钝凿的中部厚实杆身，不碰刃口。凿头朝画面左上且低于胸口，头略前低看钝端，两手之间留出可读工具轮廓；围裙原挂位清楚为空。",
      "end_pose_description_only": "右手松开托持，左手把同一凿子回到原左围裙挂位；双脚不走动。此结束态不另出图。",
      "transition_scope": "起止仅供未来动画设计参考，本轮仅计划中间所述一张姿态；未画起止/过渡，不能声称连续或循环。",
      "contact_and_support_checks": [
        "重心在两靴之间，两脚全掌落在同一隐含平面",
        "左手握木柄、右手托非刃中段，左右腕无反折，钝端不指向身体",
        "右低肩保持，手臂收近形成不同于原向下示意的轮廓"
      ],
      "prop_state_and_retention": [
        "一把原凿，原围裙挂位空",
        "不添磨石/小锤/新石块，钝端保持磨秃，不变亮刃"
      ],
      "difference_from_mother_expression_and_batch": "母图及E1/E2均未取凿；此图两手共同承托原凿，区别维菈规贴样品及旧递物动作。",
      "risk_level": "medium",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/deru/concept_v1/deru_transparent.png"
      ],
      "reference_sha256": [
        "9a335a68915943a6c2c01b8aa30c6a49248b3a5c3e837d39076b6c3c57ec5f8c"
      ],
      "prompt": "以所附该人物已审定透明全身母图为唯一人物身份、比例、衣装及已有工具造型锚，重新绘制一张独立非战斗全身动作关键姿态。保持同一脸、年龄、身材、头身比例、发型、服装层次、配色磨损与有组织的粗像素簇；成熟大头紧凑成年人，不幼化、不拉成长身、不套四人统一脸。不镜像，左右以人物自身解剖侧为准并对照画面侧说明。必须有真实手部/身体动作与明确接触，不能只改表情或平移母图。头发、双手、双靴和所有道具完整，四周留透明边距。纯alpha透明背景；除本张明确写出的接触物外，无背景、地板、阴影、光晕、文字、数字、边框、UI或第二个人。只画一个瞬间，不画动作残影、多格、箭头或连播。人体由生图重绘，禁止脚本旋转肢体、变形、拼接、插值或强量化掩盖错误。同一物件恰好一件，从原挂位取出后该位置必须空。动作不宣布任务完成、授权、付款、同意、修复、合格、康复或任何新剧情事实。\n人物：德茹 / FX-QRY。约五十岁的女石工，灰白夹深发后束、熟龄厚下颌、粗指节、结实紧凑成年身体；灰粗布衣、赭棕长围裙、棕靴。人物右肩（画面左）略低于左肩，保留自然旧姿态，不画疼痛或新伤。\n固定侧别：唯一磨秃凿子平时别在人物左侧围裙（画面右）；左右按人物解剖侧，不镜像。只有A1左手取用该凿；A2原位收好。\n本张动作：双手近身查看钝凿。双脚原地分开稳立，左肘贴近肋侧，左手从原左侧围裙取出同一磨秃凿子并握住木柄，在腰上方斜横持；右手从下托住钝凿的中部厚实杆身，不碰刃口。凿头朝画面左上且低于胸口，头略前低看钝端，两手之间留出可读工具轮廓；围裙原挂位清楚为空。\n支撑与接触：重心在两靴之间，两脚全掌落在同一隐含平面；左手握木柄、右手托非刃中段，左右腕无反折，钝端不指向身体；右低肩保持，手臂收近形成不同于原向下示意的轮廓。\n道具保留：一把原凿，原围裙挂位空；不添磨石/小锤/新石块，钝端保持磨秃，不变亮刃。\n附加约束：不做举凿威胁、磨凿工序或向画外递出。\n剧情边界：不下坑探路、不复工、不宣布欠薪清偿、不替石场主认领人或石料；不知道军务调动。；仅日常自有工具与衣物动作；查凿不等于磨锋利，低蹲不指向任何已发现证据。",
      "prompt_sha256": "184150ad9a02afd74e203646228eba712b034b3ee72e5e86fd966638fe2bdae7",
      "negative_constraints": [
        "高龄不能幼化成灰发少女；保持粗指节与自然右低肩。",
        "凿子取用后原挂位必须为空；不增锤、磨石、石料或修磨火花。",
        "拢裙不是掀衣暴露、下坑许可或越塌方线；双靴和内层灰衣保持完整。",
        "不下坑探路、不复工、不宣布欠薪清偿、不替石场主认领人或石料；不知道军务调动。",
        "仅日常自有工具与衣物动作；查凿不等于磨锋利，低蹲不指向任何已发现证据。"
      ],
      "new_contact_prop": null,
      "animation_claim": false,
      "sequence_required": false,
      "new_story_fact": false,
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "safety_blocked": "stop; no circumvention, prompt laundering or alternate generator"
      },
      "review_status": "planning_author_checked; independent_plan_review_pending",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/second_new_character_actions_sources/deru_A1_check_blunt_chisel_prompt.txt"
    },
    {
      "key": "deru_A2_gather_apron_crouch",
      "title_zh": "拢住围裙，稳身低蹲",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "deru_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "五十岁上下的女石工，指节粗大，右肩比左肩低；围裙上别着一把磨秃的凿子。"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-QRY / knows[1]",
          "line_start": 22,
          "quote": "哪一段岩壁在渗水"
        }
      ],
      "art_inference": "源文支持身份、物件或习惯；手位、重心、起止姿势及所选瞬间为可逆动作设计，不冒充台本中已经发生的事件。",
      "start_pose_description_only": "在安全平地双靴分开，凿子已在左围裙原位；右手先捏住自己右侧围裙下摆，左手准备撑左大腿。",
      "pose": "人物保持原三分之四朝向，双膝明显弯曲、髋后移成浅蹲，上身随髋略前倾而非仅低头。右手（画面左）把自己右侧赭棕围裙下缘拢起少许、停在右膝外侧，左掌实贴左大腿膝上作辅助支撑。视线向近脚前下方；两靴完整着地。内层灰衣与裤腿仍遮蔽身体，左围裙凿子仍挂稳，不能变成取凿。",
      "end_pose_description_only": "凭双腿伸膝回到稳站，再松开围裙；不迈步、不下坑、不拾得物件。",
      "transition_scope": "起止仅供未来动画设计参考，本轮仅计划中间所述一张姿态；未画起止/过渡，不能声称连续或循环。",
      "contact_and_support_checks": [
        "双靴脚掌着地、膝朝脚尖方向，髋部重心落在双足支撑区",
        "左掌压自己大腿不是压空气，右手有明确布料捏持点与褶皱",
        "围裙只收少量长度避免拦膝，不改衣装层次或露出不该出现的肌肤"
      ],
      "prop_state_and_retention": [
        "原凿一件保留人物左围裙原挂位，不能随围裙收边消失",
        "无石块、坑沿、白线、背景或新检查结果"
      ],
      "difference_from_mother_expression_and_batch": "母图和表情都直站；A1站立持凿，本图下肢/髋位改变并接触自有衣物。不是瓦森拂围裙，也不是洛珉放灯。",
      "risk_level": "medium_high",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/deru/concept_v1/deru_transparent.png"
      ],
      "reference_sha256": [
        "9a335a68915943a6c2c01b8aa30c6a49248b3a5c3e837d39076b6c3c57ec5f8c"
      ],
      "prompt": "以所附该人物已审定透明全身母图为唯一人物身份、比例、衣装及已有工具造型锚，重新绘制一张独立非战斗全身动作关键姿态。保持同一脸、年龄、身材、头身比例、发型、服装层次、配色磨损与有组织的粗像素簇；成熟大头紧凑成年人，不幼化、不拉成长身、不套四人统一脸。不镜像，左右以人物自身解剖侧为准并对照画面侧说明。必须有真实手部/身体动作与明确接触，不能只改表情或平移母图。头发、双手、双靴和所有道具完整，四周留透明边距。纯alpha透明背景；除本张明确写出的接触物外，无背景、地板、阴影、光晕、文字、数字、边框、UI或第二个人。只画一个瞬间，不画动作残影、多格、箭头或连播。人体由生图重绘，禁止脚本旋转肢体、变形、拼接、插值或强量化掩盖错误。同一物件恰好一件，从原挂位取出后该位置必须空。动作不宣布任务完成、授权、付款、同意、修复、合格、康复或任何新剧情事实。\n人物：德茹 / FX-QRY。约五十岁的女石工，灰白夹深发后束、熟龄厚下颌、粗指节、结实紧凑成年身体；灰粗布衣、赭棕长围裙、棕靴。人物右肩（画面左）略低于左肩，保留自然旧姿态，不画疼痛或新伤。\n固定侧别：唯一磨秃凿子平时别在人物左侧围裙（画面右）；左右按人物解剖侧，不镜像。只有A1左手取用该凿；A2原位收好。\n本张动作：拢住围裙，稳身低蹲。人物保持原三分之四朝向，双膝明显弯曲、髋后移成浅蹲，上身随髋略前倾而非仅低头。右手（画面左）把自己右侧赭棕围裙下缘拢起少许、停在右膝外侧，左掌实贴左大腿膝上作辅助支撑。视线向近脚前下方；两靴完整着地。内层灰衣与裤腿仍遮蔽身体，左围裙凿子仍挂稳，不能变成取凿。\n支撑与接触：双靴脚掌着地、膝朝脚尖方向，髋部重心落在双足支撑区；左掌压自己大腿不是压空气，右手有明确布料捏持点与褶皱；围裙只收少量长度避免拦膝，不改衣装层次或露出不该出现的肌肤。\n道具保留：原凿一件保留人物左围裙原挂位，不能随围裙收边消失；无石块、坑沿、白线、背景或新检查结果。\n附加约束：只是在安全平处为低位观察作准备；不得画已跨线下坑。\n剧情边界：不下坑探路、不复工、不宣布欠薪清偿、不替石场主认领人或石料；不知道军务调动。；仅日常自有工具与衣物动作；查凿不等于磨锋利，低蹲不指向任何已发现证据。",
      "prompt_sha256": "4e415e1cc0f16040e305152af7a23b01476b413cd4381115ca00ffa41ff2b8cf",
      "negative_constraints": [
        "高龄不能幼化成灰发少女；保持粗指节与自然右低肩。",
        "凿子取用后原挂位必须为空；不增锤、磨石、石料或修磨火花。",
        "拢裙不是掀衣暴露、下坑许可或越塌方线；双靴和内层灰衣保持完整。",
        "不下坑探路、不复工、不宣布欠薪清偿、不替石场主认领人或石料；不知道军务调动。",
        "仅日常自有工具与衣物动作；查凿不等于磨锋利，低蹲不指向任何已发现证据。"
      ],
      "new_contact_prop": null,
      "animation_claim": false,
      "sequence_required": false,
      "new_story_fact": false,
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "safety_blocked": "stop; no circumvention, prompt laundering or alternate generator"
      },
      "review_status": "planning_author_checked; independent_plan_review_pending",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/second_new_character_actions_sources/deru_A2_gather_apron_crouch_prompt.txt"
    }
  ]
}
