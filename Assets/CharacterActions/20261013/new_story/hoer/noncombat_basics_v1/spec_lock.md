# 本轮独立非战斗关键姿态执行锁

只生产本人物2个独立全身动作概念，不制作动画、GIF、装备或runtime素材。首稿每姿态1次，至多1次硬错修订，安全blocked即停，不绕过。builtin imagegen为唯一绘图工具。脚本仅alpha清理及等比最近邻排版，不画身体、不拉伸、不强量化。完整真实prompt、工具原返回和SHA独立保存。已读取当前卡、STYLE_DIRECTION及raw和透明母图。

{
  "slug": "hoer",
  "canonical_id": "FX-MIL",
  "name": "霍珥",
  "status": "planned_only_not_generated",
  "selection_status": "requested_candidate_suitable_retained",
  "source_card_hash_matches_roster44": true,
  "source_ids": [
    "hoer_card",
    "hoer_manifest",
    "hoer_spec_lock",
    "hoer_character_brief",
    "hoer_expression_manifest",
    "hoer_expression_board",
    "hoer_raw",
    "hoer_anchor",
    "qa_first",
    "field_dialogue",
    "field_script"
  ],
  "mother_image": {
    "path": "Assets/CharacterDesigns/20261013/expressive/new_story/hoer/concept_v1/hoer_transparent.png",
    "sha256": "2ad7fad3d48561ccefe04f1363c0f382d7eb8f4393cfa5acd9d8c62147680718",
    "raw_path": "Assets/CharacterDesigns/20261013/expressive/new_story/hoer/concept_v1/hoer_v1_raw_imagegen.png",
    "raw_sha256": "2e978cb06e5e71dc342946d2ff2255ae32716afb47ca67be8d95aa7ac365f189",
    "size": [
      1049,
      1499
    ],
    "mode": "RGBA",
    "raw_and_transparent_actually_viewed": true,
    "viewed_utc": "2026-10-14T03:03:55Z",
    "hashes_match_manifest_and_independent_qa": true,
    "existing_expression_board_actually_viewed": true,
    "old_pose": "直站，右掌举起制止，左手侧落。表情E1降掌闲谈；E2右手近胸压声，均非双手接触或下肢支撑变化。",
    "identity_lock": "三十来岁成年男子，棕短发、粗眉、短须和结实脸；蓝灰工褂袖至肘，棕腰带与腰围布、深褐裤、旧棕靴；不与瓦森合人，不添工具。",
    "side_lock": "腰带垂尾保留人物左側（画面右）；左耳后旧疤按卡保留其侧，但母图区域被耳廓/发际遮挡，容许继续遮挡，不凭空在右脸或耳前补大疤。人物右手原在画面左。"
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
    "不开闸放水、不替上游人家作证、不推定修路完成、不掌握军需船期。",
    "不磨面、不垫粮、不捞上游物品；本人安全在场才可用，未授权事仍未发生。"
  ],
  "risks": [
    "母图无磨杆、闸轮或水桶，不能用职业常识补一件已持工具。",
    "虎口色块非新伤诊断；轻揉是日常手部动作设计，不画伤口、包扎或康复。",
    "听水只推导姿态，无具体听到的事件或指认对象；不画临水险站。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/hoer/noncombat_basics_v1",
  "plans": [
    {
      "key": "hoer_A1_press_workworn_palm",
      "title_zh": "收手轻揉虎口",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "hoer_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "虎口有磨杆磨出的厚皮"
        },
        {
          "source_id": "hoer_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "袖子永远卷到手肘"
        }
      ],
      "art_inference": "源文支持身份、物件或习惯；手位、重心、起止姿势及所选瞬间为可逆动作设计，不冒充台本中已经发生的事件。",
      "start_pose_description_only": "两脚稳站，原制止右手收至肚腹前，右腕转为掌心朝自身斜上；左手接近。",
      "pose": "双脚仍稳站，双肘收于腰两侧。右手在腹前低位半张，掌心斜向自身；左手从下托右掌，左拇指轻压右手拇指与食指根部的虎口厚皮，右手其余手指自然微曲放松。头稍低看两手，左右手接触点明确，脸不痛苦。两只袖口仍卷在肘部，绝不补磨杆或夹持空气。",
      "end_pose_description_only": "左拇指松开，双手自然分开回到近身垂落；不改变厚皮，不宣称治疗或伤愈。",
      "transition_scope": "起止仅供未来动画设计参考，本轮仅计划中间所述一张姿态；未画起止/过渡，不能声称连续或循环。",
      "contact_and_support_checks": [
        "两足同平面，骨盆居中",
        "左手托右掌但不穿掌，左拇指接触虎口；不画额外拇指",
        "手位低于胸口、不呈举掌说话或心口作证手势"
      ],
      "prop_state_and_retention": [
        "母图无手持物，本张仍零工具",
        "腰带、左侧垂尾、腰围布、双靴保留；袖不重新展开"
      ],
      "difference_from_mother_expression_and_batch": "不同于母图单掌制止与E2右手靠胸；本图双手相触并有局部压力动作。避免已存在的理袖模板。",
      "risk_level": "medium",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/hoer/concept_v1/hoer_transparent.png"
      ],
      "reference_sha256": [
        "2ad7fad3d48561ccefe04f1363c0f382d7eb8f4393cfa5acd9d8c62147680718"
      ],
      "prompt": "以所附该人物已审定透明全身母图为唯一人物身份、比例、衣装及已有工具造型锚，重新绘制一张独立非战斗全身动作关键姿态。保持同一脸、年龄、身材、头身比例、发型、服装层次、配色磨损与有组织的粗像素簇；成熟大头紧凑成年人，不幼化、不拉成长身、不套四人统一脸。不镜像，左右以人物自身解剖侧为准并对照画面侧说明。必须有真实手部/身体动作与明确接触，不能只改表情或平移母图。头发、双手、双靴和所有道具完整，四周留透明边距。纯alpha透明背景；除本张明确写出的接触物外，无背景、地板、阴影、光晕、文字、数字、边框、UI或第二个人。只画一个瞬间，不画动作残影、多格、箭头或连播。人体由生图重绘，禁止脚本旋转肢体、变形、拼接、插值或强量化掩盖错误。同一物件恰好一件，从原挂位取出后该位置必须空。动作不宣布任务完成、授权、付款、同意、修复、合格、康复或任何新剧情事实。\n人物：霍珥 / FX-MIL。三十来岁成年男子，棕短发、粗眉、短须和结实脸；蓝灰工褂袖至肘，棕腰带与腰围布、深褐裤、旧棕靴；不与瓦森合人，不添工具。\n固定侧别：腰带垂尾保留人物左側（画面右）；左耳后旧疤按卡保留其侧，但母图区域被耳廓/发际遮挡，容许继续遮挡，不凭空在右脸或耳前补大疤。人物右手原在画面左。\n本张动作：收手轻揉虎口。双脚仍稳站，双肘收于腰两侧。右手在腹前低位半张，掌心斜向自身；左手从下托右掌，左拇指轻压右手拇指与食指根部的虎口厚皮，右手其余手指自然微曲放松。头稍低看两手，左右手接触点明确，脸不痛苦。两只袖口仍卷在肘部，绝不补磨杆或夹持空气。\n支撑与接触：两足同平面，骨盆居中；左手托右掌但不穿掌，左拇指接触虎口；不画额外拇指；手位低于胸口、不呈举掌说话或心口作证手势。\n道具保留：母图无手持物，本张仍零工具；腰带、左侧垂尾、腰围布、双靴保留；袖不重新展开。\n附加约束：只是日常舒展劳作手部的可逆提案，无受伤诊断、流血、绷带、药物或治愈表现。\n剧情边界：不开闸放水、不替上游人家作证、不推定修路完成、不掌握军需船期。；不磨面、不垫粮、不捞上游物品；本人安全在场才可用，未授权事仍未发生。",
      "prompt_sha256": "64c2c7e4cc33667c7d4d5732dbd5c8b5202c5c802dc0fe270ca6ee945cf1145c",
      "negative_constraints": [
        "母图无磨杆、闸轮或水桶，不能用职业常识补一件已持工具。",
        "虎口色块非新伤诊断；轻揉是日常手部动作设计，不画伤口、包扎或康复。",
        "听水只推导姿态，无具体听到的事件或指认对象；不画临水险站。",
        "不开闸放水、不替上游人家作证、不推定修路完成、不掌握军需船期。",
        "不磨面、不垫粮、不捞上游物品；本人安全在场才可用，未授权事仍未发生。"
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
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/second_new_character_actions_sources/hoer_A1_press_workworn_palm_prompt.txt"
    },
    {
      "key": "hoer_A2_brace_thighs_listen",
      "title_zh": "双手稳膝，俯身听水",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "field_dialogue",
          "locator": "FX-MIL / greetings[night]",
          "line_start": 127,
          "quote": "夜里水声大，出什么事都听不见。你也是来听水的？"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-MIL / site_lines[warning]",
          "line_start": 142,
          "quote": "水口那圈石头是滑的，上个月有人在那摔断了腿。"
        }
      ],
      "art_inference": "源文支持身份、物件或习惯；手位、重心、起止姿势及所选瞬间为可逆动作设计，不冒充台本中已经发生的事件。",
      "start_pose_description_only": "在安全干燥的平处站稳，双手向自己膝上移；两靴保持分开，不朝水口踏出。",
      "pose": "双膝轻屈、髋向后折，上身有明显前倾，两只掌心分别撑在自己左右大腿的膝上方；肘有自然弯曲。头在保持母图可识別脸朝向的前提下轻偏向画面左的听声方向，侧耳凝听，目光不指认任何人。双靴均完整着地，姿态像在安全位置停下辨听，不是伸手捞水、眩晕或喘病。",
      "end_pose_description_only": "双腿伸直，双手离开大腿回到直立；没有开闸、移动到滑石或听出结论。",
      "transition_scope": "起止仅供未来动画设计参考，本轮仅计划中间所述一张姿态；未画起止/过渡，不能声称连续或循环。",
      "contact_and_support_checks": [
        "掌根各自实贴大腿膝上，不直接锁压膝盖；两臂不能悬空当撑杖",
        "骨盆后移抵消前倾，重心仍在双足间；不踮脚、跨步或站在水石上",
        "身体倾斜和双手接触必须明显区别于仅侧头的表情图"
      ],
      "prop_state_and_retention": [
        "零新增道具；原腰围与左侧腰带尾自然垂落",
        "不画水、石、闸、麦袋、第二人或气泡音效"
      ],
      "difference_from_mother_expression_and_batch": "不同于旧静听表情：全身髋膝屈曲与双手支撑改变；德茹浅蹲是单掌撑腿＋拢裙，本图双手撑腿、无拢衣。",
      "risk_level": "medium_high",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/hoer/concept_v1/hoer_transparent.png"
      ],
      "reference_sha256": [
        "2ad7fad3d48561ccefe04f1363c0f382d7eb8f4393cfa5acd9d8c62147680718"
      ],
      "prompt": "以所附该人物已审定透明全身母图为唯一人物身份、比例、衣装及已有工具造型锚，重新绘制一张独立非战斗全身动作关键姿态。保持同一脸、年龄、身材、头身比例、发型、服装层次、配色磨损与有组织的粗像素簇；成熟大头紧凑成年人，不幼化、不拉成长身、不套四人统一脸。不镜像，左右以人物自身解剖侧为准并对照画面侧说明。必须有真实手部/身体动作与明确接触，不能只改表情或平移母图。头发、双手、双靴和所有道具完整，四周留透明边距。纯alpha透明背景；除本张明确写出的接触物外，无背景、地板、阴影、光晕、文字、数字、边框、UI或第二个人。只画一个瞬间，不画动作残影、多格、箭头或连播。人体由生图重绘，禁止脚本旋转肢体、变形、拼接、插值或强量化掩盖错误。同一物件恰好一件，从原挂位取出后该位置必须空。动作不宣布任务完成、授权、付款、同意、修复、合格、康复或任何新剧情事实。\n人物：霍珥 / FX-MIL。三十来岁成年男子，棕短发、粗眉、短须和结实脸；蓝灰工褂袖至肘，棕腰带与腰围布、深褐裤、旧棕靴；不与瓦森合人，不添工具。\n固定侧别：腰带垂尾保留人物左側（画面右）；左耳后旧疤按卡保留其侧，但母图区域被耳廓/发际遮挡，容许继续遮挡，不凭空在右脸或耳前补大疤。人物右手原在画面左。\n本张动作：双手稳膝，俯身听水。双膝轻屈、髋向后折，上身有明显前倾，两只掌心分别撑在自己左右大腿的膝上方；肘有自然弯曲。头在保持母图可识別脸朝向的前提下轻偏向画面左的听声方向，侧耳凝听，目光不指认任何人。双靴均完整着地，姿态像在安全位置停下辨听，不是伸手捞水、眩晕或喘病。\n支撑与接触：掌根各自实贴大腿膝上，不直接锁压膝盖；两臂不能悬空当撑杖；骨盆后移抵消前倾，重心仍在双足间；不踮脚、跨步或站在水石上；身体倾斜和双手接触必须明显区别于仅侧头的表情图。\n道具保留：零新增道具；原腰围与左侧腰带尾自然垂落；不画水、石、闸、麦袋、第二人或气泡音效。\n附加约束：听水是由对白推导的身体演出，不表明听见事故、证人或上游秘密。\n剧情边界：不开闸放水、不替上游人家作证、不推定修路完成、不掌握军需船期。；不磨面、不垫粮、不捞上游物品；本人安全在场才可用，未授权事仍未发生。",
      "prompt_sha256": "784c91697bff0ae1cc4e335187223f87ca2d72bf2dbf851aea20766bacd0dfa2",
      "negative_constraints": [
        "母图无磨杆、闸轮或水桶，不能用职业常识补一件已持工具。",
        "虎口色块非新伤诊断；轻揉是日常手部动作设计，不画伤口、包扎或康复。",
        "听水只推导姿态，无具体听到的事件或指认对象；不画临水险站。",
        "不开闸放水、不替上游人家作证、不推定修路完成、不掌握军需船期。",
        "不磨面、不垫粮、不捞上游物品；本人安全在场才可用，未授权事仍未发生。"
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
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/second_new_character_actions_sources/hoer_A2_brace_thighs_listen_prompt.txt"
    }
  ]
}
