# 谟珥 第十一批基础动作锁定

{
  "slug": "moer_trs",
  "canonical_id": "FX-TRS",
  "name": "谟珥",
  "status": "planned_not_generated",
  "selection_status": "requested_candidate_retained_no_substitution",
  "current_card": {
    "path": "design/04_人物/野外人物/人物_FX-TRS_谟珥.md",
    "bytes": 1058,
    "sha256": "95c9799a2b546eaa3f4cf733170fd84425e28de858a174474df7a69b34e80f9e",
    "source_id": "moer_trs_card",
    "snapshot_path": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/files/design/04_人物/野外人物/人物_FX-TRS_谟珥.md"
  },
  "source_ids": [
    "moer_trs_card",
    "field_dialogue",
    "field_dialogue_registry",
    "N3",
    "moer_trs_mother_raw",
    "moer_trs_mother_transparent",
    "moer_trs_mother_manifest",
    "moer_trs_expression_final_status",
    "moer_trs_expressions_view"
  ],
  "mother_image": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/moer_trs/concept_v1/moer_trs_v2_raw_imagegen.png",
    "raw_sha256": "fe036b6b160d952f3bca7e5cd49e4a4a579c02c03edfdb331c090cc7ca2bc3f6",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/moer_trs/concept_v1/moer_trs_transparent.png",
    "transparent_sha256": "45f9ca7a50f6201e4d363d8a7a521fe20da81d5eb242a4e393151b7cf4a68793",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/moer_trs/concept_v1/manifest.json",
    "manifest_sha256": "149a8934db89da5e04478031e26ea62470761b951202042c873375194640c5b9",
    "independent_qa_source_id": "eleventh_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "分别实际查看本人v2 raw、透明母图与旧表情浅板：年轻成人深棕乱发、赭黄衣、米麻袖口、深灰裤及膝部原崖灰、棕靴附崖灰。唯一短铲斜背在身后：D形木柄露画面右肩后，铲刃露画面左腰后；人物左手（画面右）在肩旁握柄下部，右手（画面左）腰高半摊。旧传言兴起/问伴心虚保持背铲和腰高摊手，未屈膝低扶膝或抬手按发顶。",
    "fixed_sides": "唯一原短铲保持v2斜背在身后，D形木柄露画面右肩后、铲刃露画面左腰后；人物左手（画面右）始终握原柄下部，不换手、不卸铲、不挥铲、不把铲刃挪到身前，不新增背带。背铲可随躯干整体自然倾斜但不改原长度和相对背部位置。右手只按本张动作移动；原裤靴崖灰保留，无扬尘或洗净效果。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/moer_trs/expressions_v1/review/moer_trs_light_board.png"
  },
  "existing_expressions": {
    "status": "PASS_FROZEN_CONCEPT_ONLY",
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
    "普通可逆自理/暂歇，不挖土、不下崖、不带路、不指认宝藏、不新增同伴下落、传言证词、战斗或N3结果。",
    "源卡只有年轻成年人未明示性别，延续本人母图外观；严格使用moer_trs的已审v2背铲，不引用moer或废v1。"
  ],
  "risks": [
    "背铲必须仍有画面右肩后D柄和画面左腰后铲刃的同一斜向关系，左手不离原握点。",
    "屈膝动作是两靴完整支撑的浅暂歇；按发顶用掌贴头顶外缘，不遮眼、不抓脸、不摘发饰、不作头痛。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/moer_trs/noncombat_basics_v1",
  "plans": [
    {
      "key": "moer_trs_A1_shallow_crouch_right_palm_on_knee",
      "title_zh": "浅屈膝右掌扶膝",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "moer_trs_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "背着一把短铲，鞋上全是崖灰"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-TRS／拒绝，只限制不带路",
          "line_start": 840,
          "quote": "要我带路下崖？不去。"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托杯/理围裙/抬板/垂板/理外套/舒肩/扶膝/理发是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从v2母图左手肩旁握背铲、右手腰高半摊的站姿开始。",
      "pose": "双靴分开稳站并全掌支撑，双膝浅屈、髋部稍后下沉，躯干从髋部轻前倾。人物右手完全离开原腰高摊手的位置，右臂向画面左下伸，右掌平贴本人右膝上方的深灰裤面宽处，停在短暂扶膝的一瞬。人物左手仍在画面右肩旁握原铲柄下部，短铲整体随躯干轻倾但始终贴背：D柄仍露画面右肩后、原铲刃仍露画面左腰后。右掌落点低于铲刃，二者不相碰。头脸仍朝画面左、神态平常，原崖灰未清除。",
      "end_pose_description_only": "右掌可离膝、双腿自然伸直；背铲仍在背后，既不下崖也不挖掘。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "双膝可见浅屈、髋位降低，右掌由腰高摊手降到右膝上裤面；左手及背铲原关系保持。",
      "pose_specific_sidedness": "人物右掌在画面左的本人右膝上，左手画面右肩旁继续握柄；D柄画面右肩后、铲刃画面左腰后，不镜像。",
      "contact_and_support_checks": [
        "双膝和髋位真实改变，双靴全掌支撑，不只缩短人物或弯脖子。",
        "右掌只贴膝上裤布，不抓铲刃、不摸鞋；左手仍只有一只握原柄。",
        "短铲仍一把在背后，柄刃相对方向和原尺寸不变；不新增背带、扬尘、疼痛或跌倒。"
      ],
      "prop_state_and_retention": [
        "唯一原短铲保持v2斜背在身后，D形木柄露画面右肩后、铲刃露画面左腰后；人物左手（画面右）始终握原柄下部，不换手、不卸铲、不挥铲、不把铲刃挪到身前，不新增背带。背铲可随躯干整体自然倾斜但不改原长度和相对背部位置。右手只按本张动作移动；原裤靴崖灰保留，无扬尘或洗净效果。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧表情直立且右手腰高半摊，本张浅屈膝降髋、右掌低到膝上，区别由肢体支撑产生而非问伴情绪。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/moer_trs/concept_v1/moer_trs_transparent.png"
      ],
      "reference_sha256": [
        "45f9ca7a50f6201e4d363d8a7a521fe20da81d5eb242a4e393151b7cf4a68793"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：谟珥 FX-TRS。二十多岁的年轻成年人，堡垒寻宝者；源卡未明示性别，不另冻结性别。深棕蓬松波发、母图本人年轻成人脸朝画面左，赭黄外衣、米麻内衫与宽袖口、深灰裤及膝部原崖灰、棕腰带和沾崖灰的深棕靴保持。只用谟珥FX-TRS/moer_trs已审v2背铲母图，不用废v1，不是摩珥FX-WIL/moer。\n固定衣装与原物件：唯一原短铲保持v2斜背在身后，D形木柄露画面右肩后、铲刃露画面左腰后；人物左手（画面右）始终握原柄下部，不换手、不卸铲、不挥铲、不把铲刃挪到身前，不新增背带。背铲可随躯干整体自然倾斜但不改原长度和相对背部位置。右手只按本张动作移动；原裤靴崖灰保留，无扬尘或洗净效果。\n本张动作：浅屈膝右掌扶膝。双靴分开稳站并全掌支撑，双膝浅屈、髋部稍后下沉，躯干从髋部轻前倾。人物右手完全离开原腰高摊手的位置，右臂向画面左下伸，右掌平贴本人右膝上方的深灰裤面宽处，停在短暂扶膝的一瞬。人物左手仍在画面右肩旁握原铲柄下部，短铲整体随躯干轻倾但始终贴背：D柄仍露画面右肩后、原铲刃仍露画面左腰后。右掌落点低于铲刃，二者不相碰。头脸仍朝画面左、神态平常，原崖灰未清除。\n本张侧别：人物右掌在画面左的本人右膝上，左手画面右肩旁继续握柄；D柄画面右肩后、铲刃画面左腰后，不镜像。\n必须明显可见：双膝可见浅屈、髋位降低，右掌由腰高摊手降到右膝上裤面；左手及背铲原关系保持。\n接触与支撑：双膝和髋位真实改变，双靴全掌支撑，不只缩短人物或弯脖子。；右掌只贴膝上裤布，不抓铲刃、不摸鞋；左手仍只有一只握原柄。；短铲仍一把在背后，柄刃相对方向和原尺寸不变；不新增背带、扬尘、疼痛或跌倒。。\n",
      "prompt_sha256": "a080a300d12510acf00ac51960ad1e72a6b1c7ef950de1fa43f33074236a6b34",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/moer_trs_A1_shallow_crouch_right_palm_on_knee_prompt.txt",
      "negative_constraints": [
        "普通可逆自理/暂歇，不挖土、不下崖、不带路、不指认宝藏、不新增同伴下落、传言证词、战斗或N3结果。",
        "源卡只有年轻成年人未明示性别，延续本人母图外观；严格使用moer_trs的已审v2背铲，不引用moer或废v1。",
        "背铲必须仍有画面右肩后D柄和画面左腰后铲刃的同一斜向关系，左手不离原握点。",
        "屈膝动作是两靴完整支撑的浅暂歇；按发顶用掌贴头顶外缘，不遮眼、不抓脸、不摘发饰、不作头痛。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧表情直立且右手腰高半摊，本张浅屈膝降髋、右掌低到膝上，区别由肢体支撑产生而非问伴情绪。"
      }
    },
    {
      "key": "moer_trs_A2_rest_right_palm_on_hair_crown",
      "title_zh": "右掌轻按发顶",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "moer_trs_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "二十多岁的年轻人"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-TRS／知情边界",
          "line_start": 828,
          "quote": "不说同伴的下落"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托杯/理围裙/抬板/垂板/理外套/舒肩/扶膝/理发是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从v2母图左手肩旁握背铲、右手腰高半摊开始。",
      "pose": "双靴自然分开稳站、两腿伸直、躯干直立。人物右手完全离开原腰高半摊位置，右肘向画面左上方外抬，右前臂斜向上，右掌自然并拢轻贴本人头顶偏画面左的外层发面，停在顺理自己蓬发的一瞬。掌心接头顶外缘，指组沿发面自然放平，不遮眉眼、不抓头皮、不压扁或换发型。人物左手仍在画面右肩旁握原背铲柄下部，D柄仍在画面右肩后、铲刃仍在画面左腰后。脸朝画面左、神态平常，崖灰与衣装不变。",
      "end_pose_description_only": "右掌可从发顶自然放下，发型与背铲均保持原样；不新增头痛、伤病或情节。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "右肘抬到头侧、右掌到发顶外缘，原腰高摊手消失；两腿直立、左手保持背铲，是明显头上手位。",
      "pose_specific_sidedness": "人物右掌在画面左头顶外缘；左手保持画面右肩旁握柄，背铲D柄与铲刃仍原对角位置。",
      "contact_and_support_checks": [
        "右掌只轻贴发顶宽面，额头和眉眼清楚，不遮脸、不抓发或出现第三手。",
        "右臂高抬不碰背铲D柄，左手仍握原柄且铲身在背后。",
        "两靴全掌站稳、头与高肘留透明边，原发型和年轻成人比例保留。"
      ],
      "prop_state_and_retention": [
        "唯一原短铲保持v2斜背在身后，D形木柄露画面右肩后、铲刃露画面左腰后；人物左手（画面右）始终握原柄下部，不换手、不卸铲、不挥铲、不把铲刃挪到身前，不新增背带。背铲可随躯干整体自然倾斜但不改原长度和相对背部位置。右手只按本张动作移动；原裤靴崖灰保留，无扬尘或洗净效果。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧表情右手在腰高半摊，本张右手高到头顶、右肘外抬；与低扶膝在腿姿、躯干和手位上都显著不同。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/moer_trs/concept_v1/moer_trs_transparent.png"
      ],
      "reference_sha256": [
        "45f9ca7a50f6201e4d363d8a7a521fe20da81d5eb242a4e393151b7cf4a68793"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：谟珥 FX-TRS。二十多岁的年轻成年人，堡垒寻宝者；源卡未明示性别，不另冻结性别。深棕蓬松波发、母图本人年轻成人脸朝画面左，赭黄外衣、米麻内衫与宽袖口、深灰裤及膝部原崖灰、棕腰带和沾崖灰的深棕靴保持。只用谟珥FX-TRS/moer_trs已审v2背铲母图，不用废v1，不是摩珥FX-WIL/moer。\n固定衣装与原物件：唯一原短铲保持v2斜背在身后，D形木柄露画面右肩后、铲刃露画面左腰后；人物左手（画面右）始终握原柄下部，不换手、不卸铲、不挥铲、不把铲刃挪到身前，不新增背带。背铲可随躯干整体自然倾斜但不改原长度和相对背部位置。右手只按本张动作移动；原裤靴崖灰保留，无扬尘或洗净效果。\n本张动作：右掌轻按发顶。双靴自然分开稳站、两腿伸直、躯干直立。人物右手完全离开原腰高半摊位置，右肘向画面左上方外抬，右前臂斜向上，右掌自然并拢轻贴本人头顶偏画面左的外层发面，停在顺理自己蓬发的一瞬。掌心接头顶外缘，指组沿发面自然放平，不遮眉眼、不抓头皮、不压扁或换发型。人物左手仍在画面右肩旁握原背铲柄下部，D柄仍在画面右肩后、铲刃仍在画面左腰后。脸朝画面左、神态平常，崖灰与衣装不变。\n本张侧别：人物右掌在画面左头顶外缘；左手保持画面右肩旁握柄，背铲D柄与铲刃仍原对角位置。\n必须明显可见：右肘抬到头侧、右掌到发顶外缘，原腰高摊手消失；两腿直立、左手保持背铲，是明显头上手位。\n接触与支撑：右掌只轻贴发顶宽面，额头和眉眼清楚，不遮脸、不抓发或出现第三手。；右臂高抬不碰背铲D柄，左手仍握原柄且铲身在背后。；两靴全掌站稳、头与高肘留透明边，原发型和年轻成人比例保留。。\n",
      "prompt_sha256": "4ae7636b2d242054118f9d6d9bf57ed32721015931a40e611edfc6799f875d2f",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/moer_trs_A2_rest_right_palm_on_hair_crown_prompt.txt",
      "negative_constraints": [
        "普通可逆自理/暂歇，不挖土、不下崖、不带路、不指认宝藏、不新增同伴下落、传言证词、战斗或N3结果。",
        "源卡只有年轻成年人未明示性别，延续本人母图外观；严格使用moer_trs的已审v2背铲，不引用moer或废v1。",
        "背铲必须仍有画面右肩后D柄和画面左腰后铲刃的同一斜向关系，左手不离原握点。",
        "屈膝动作是两靴完整支撑的浅暂歇；按发顶用掌贴头顶外缘，不遮眼、不抓脸、不摘发饰、不作头痛。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧表情右手在腰高半摊，本张右手高到头顶、右肘外抬；与低扶膝在腿姿、躯干和手位上都显著不同。"
      }
    }
  ]
}

只按本姿独立prompt调用。母图实比，不套数字。每姿1首稿，最多1次真硬错修订，安全block停止；内置imagegen负责人物，脚本只alpha≤8与隐藏RGB清理、整图nearest等比排版；保全返回payload与所有尝试。不动画、不游戏落地、不Git、不上传。
