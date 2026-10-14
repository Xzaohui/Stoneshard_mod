# Third batch independent noncombat action spec

Approved continuation of locked adult expressive coarse-pixel mother. Each pose is independent static concept, not animation or runtime. One first draft and at most one hard-error revision per pose. Builtin imagegen only for anatomy; no procedural body edits. Preserve character-specific palette and proportions, real alpha, all props and story boundaries.

{
  "slug": "kuen",
  "canonical_id": "ASH-NPC-KUEN",
  "name": "枯恩",
  "status": "selected_planned_not_generated",
  "selection_status": "requested_candidate_kept",
  "source_card_hash_matches_roster44": true,
  "source_ids": [
    "kuen_card",
    "kuen_mother_manifest",
    "kuen_mother_spec",
    "kuen_expression_manifest",
    "kuen_expression_qa"
  ],
  "mother_image": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/kuen/concept_v1/kuen_v1_raw_imagegen.png",
    "raw_sha256": "c69e688038a5e806bb5609f0a141351f8cd6f167bfcc3b8805711b702caf93f1",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/kuen/concept_v1/kuen_transparent.png",
    "transparent_sha256": "18f4a8f8b77e25529edee1c0d0055d063a22584bf7b625dc1f9660bb5eacdd61",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/kuen/concept_v1/manifest.json",
    "manifest_sha256": "50ccdc72b34ef769256f14cded7d9724ce34f9c5ee6853e236d6f9dc272c2370",
    "independent_qa_source_id": "mother_qa",
    "actual_visual_observation": "母图右手（画面左）摊掌说明，左手（画面右）有旧青并落左膝。低木椅有靠背，布卷位于背部并在画面右露卷端；单独矮木凳、温水杯及无字布条在人物右侧（画面左）。E1双手低放，E2右掌举起拒绝，均未操作披肩或侧转靠椅。",
    "fixed_sides": "旧青固定人物左手背（画面右），不得改侧或新增病灶。木椅、背部布卷、双脚原落点不挪；右侧（画面左）小凳、杯、布条原位不动，杯始终未触碰、未端起。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/kuen/expressions_v1/review/kuen_expressions_light.png"
  },
  "duplicate_check": {
    "own_existing_branches": [
      "concept_v1",
      "expressions_v1"
    ],
    "own_action_directories_found": [],
    "existing_expressions_actually_viewed": true,
    "do_not_recount": [
      "母图与表情小手势",
      "sources内复用图",
      "重复展示板/源ZIP成员",
      "只有表情或头姿的变化"
    ]
  },
  "story_boundaries": [
    "成年自主表达不等于身体能力改变；当前卡写喝水要人扶，当前CS-ASH-02-S1-needs还写这个时段帮起身，故两姿保持臀部坐实、脚原位，不推起、不自行饮水。",
    "不画治疗/医疗操作、康复、迁居、护理替换成立、观察同意或对伴侣的要求；坐姿变化只是可逆日常演出推断。",
    "原手背旧青只保留，不展示现代针管、留置针、输液或新诊断；杯水和需求布条不变成可读数据。"
  ],
  "risks": [
    "A1要操作正在披着的同一披肩，不变成独立毯子或增加一件衣物。",
    "A2只旋转肩胸，不移动椅、抬臀、拔出布卷或呈站起势；手掌轻搭椅面而非撑体起立。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/kuen/noncombat_basics_v1",
  "plans": [
    {
      "key": "kuen_A1_draw_shawl_edges_in",
      "title_zh": "坐稳合拢胸前披肩",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "kuen_card",
          "locator": "衣着与磨损",
          "line_start": 38,
          "quote": "病号布衫外披厚披肩，是奥娅织的"
        },
        {
          "source_id": "kuen_card",
          "locator": "体貌",
          "line_start": 36,
          "quote": "坐时背垫着布卷"
        }
      ],
      "art_inference": "源文只支持人物、物件与边界；本具体手位、物件朝向和重心是可逆日常动作提案，不冒充台本已发生的事件或医学建议。",
      "start_pose_description_only": "臀部坐实原椅，背仍靠布卷；两手从说明/落膝位置移向自己披肩两前缘，杯与凳不动。",
      "pose": "两肘收近身体，右手（画面左）捏住同一披肩右前缘在下胸处向中线轻拉；左手（画面右）托住并捏稳左前缘，位置略低于右手。两条仍连着肩背的前缘在胸腹中央形成清楚的小重叠与受牵折褶，两个手腕与指组各有真实布料接点。肩胸仍朝母图方向，头稍低看自己的手；臀部全落原椅面、背后布卷不滑出，双脚原落地。",
      "end_pose_description_only": "放松捏握，让同一披肩仍披在肩背并垂回膝前；不增脱衣、起身、取水或照护步骤。",
      "transition_scope": "起止只是文字供以后制作参考；本轮只计划pose描述的一张独立静态关键姿态，未制作起止帧、过渡或连续循环。A1/A2不构成默认先后顺序。",
      "contact_and_support_checks": [
        "两手各捏同一披肩一条前缘，布料从两肩连续到接点，不浮空、不互穿",
        "双肘有弯曲与袖口相接，左手背旧青不移到右手",
        "臀部在椅面、后背布卷与双脚构成原坐姿支撑，椅凳杯布条仍全可见"
      ],
      "prop_state_and_retention": [
        "同一披肩仍穿披于身上，只合拢前缘；不新增独立毯子",
        "椅、布卷、小凳、杯水、布条保持母图位置和数量"
      ],
      "difference_from_mother_expression_and_batch": "相对母图及E1/E2，两手均转为捏衣接触，披肩前缘重叠可读；与Mia站立抚平独立叠毯不同，也不是Osin袖口或Vasen围裙整理。",
      "risk_level": "medium",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/kuen/concept_v1/kuen_transparent.png"
      ],
      "reference_sha256": [
        "18f4a8f8b77e25529edee1c0d0055d063a22584bf7b625dc1f9660bb5eacdd61"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一人物身份、脸型、年龄、比例、衣装、配色及已有器物造型锚，用内置imagegen重新绘制一张独立非战斗全身动作关键姿态。保留母图成熟大头、短自然颈、紧凑成年身体与有组织的粗像素簇，不幼化、不拉成长身、不统一四人的脸。不镜像；下文左右均为人物自身解剖侧，并附画面侧。必须有真实手臂、身体或原道具接触变化，不能只改表情、低头或平移母图。完整头发、双手、双脚和全部保留器物，四周留透明边距。单人、单个瞬间、纯alpha透明背景，无背景、地板、投影、光晕、文字、数字、图标、边框、UI、第二个人、箭头、残影或多格。所有原物件只保一件，取出后原位置不再复制同件。不用脚本绘制人体、旋转肢体、插值、拉伸、拼接或强量化修错。没有动作结果、治疗、康复、付款、授权、所有权转移、任务结案或新剧情事实。\n人物：三十多岁成年男性、清醒能自主表达的患者；深棕短乱发、少量胡茬、烟灰蓝布衫、厚暖灰褐织披肩、深灰褐裤、松袜口与软便鞋。\n原侧别与锚定：旧青固定人物左手背（画面右），不得改侧或新增病灶。木椅、背部布卷、双脚原落点不挪；右侧（画面左）小凳、杯、布条原位不动，杯始终未触碰、未端起。\n本张动作：坐稳合拢胸前披肩。两肘收近身体，右手（画面左）捏住同一披肩右前缘在下胸处向中线轻拉；左手（画面右）托住并捏稳左前缘，位置略低于右手。两条仍连着肩背的前缘在胸腹中央形成清楚的小重叠与受牵折褶，两个手腕与指组各有真实布料接点。肩胸仍朝母图方向，头稍低看自己的手；臀部全落原椅面、背后布卷不滑出，双脚原落地。\n接触与重心：两手各捏同一披肩一条前缘，布料从两肩连续到接点，不浮空、不互穿；双肘有弯曲与袖口相接，左手背旧青不移到右手；臀部在椅面、后背布卷与双脚构成原坐姿支撑，椅凳杯布条仍全可见。\n物件保留：同一披肩仍穿披于身上，只合拢前缘；不新增独立毯子；椅、布卷、小凳、杯水、布条保持母图位置和数量。\n剧情边界：成年自主表达不等于身体能力改变；当前卡写喝水要人扶，当前CS-ASH-02-S1-needs还写这个时段帮起身，故两姿保持臀部坐实、脚原位，不推起、不自行饮水。；不画治疗/医疗操作、康复、迁居、护理替换成立、观察同意或对伴侣的要求；坐姿变化只是可逆日常演出推断。；原手背旧青只保留，不展示现代针管、留置针、输液或新诊断；杯水和需求布条不变成可读数据。。\n硬约束：A1要操作正在披着的同一披肩，不变成独立毯子或增加一件衣物。；A2只旋转肩胸，不移动椅、抬臀、拔出布卷或呈站起势；手掌轻搭椅面而非撑体起立。。只画上述一个瞬间，不画文字说明的起止姿态。",
      "prompt_sha256": "227116cb9a2e6c10c31a9495f9eb594c9b8d093511e9388c76d20d2553e815c3",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/third_new_character_actions_sources/kuen_A1_draw_shawl_edges_in_prompt.txt",
      "negative_constraints": [
        "A1要操作正在披着的同一披肩，不变成独立毯子或增加一件衣物。",
        "A2只旋转肩胸，不移动椅、抬臀、拔出布卷或呈站起势；手掌轻搭椅面而非撑体起立。",
        "成年自主表达不等于身体能力改变；当前卡写喝水要人扶，当前CS-ASH-02-S1-needs还写这个时段帮起身，故两姿保持臀部坐实、脚原位，不推起、不自行饮水。",
        "不画治疗/医疗操作、康复、迁居、护理替换成立、观察同意或对伴侣的要求；坐姿变化只是可逆日常演出推断。",
        "原手背旧青只保留，不展示现代针管、留置针、输液或新诊断；杯水和需求布条不变成可读数据。"
      ],
      "new_contact_prop": null,
      "animation_claim": false,
      "sequence_required": false,
      "new_story_fact": false,
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "revision_only_for": "明确可定位的人体/接触/道具数目侧别/身份等硬错；不是无止境美感迭代",
        "safety_blocked": "stop; no circumvention, prompt laundering or alternate generator"
      },
      "review_status": "planning_author_checked; independent_plan_review_pending"
    },
    {
      "key": "kuen_A2_seated_turn_with_seat_contact",
      "title_zh": "坐稳轻侧转并搭椅沿",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "kuen_card",
          "locator": "举止",
          "line_start": 42,
          "quote": "喝水要人扶，翻身不用"
        },
        {
          "source_id": "kuen_card",
          "locator": "体貌",
          "line_start": 36,
          "quote": "坐时背垫着布卷"
        },
        {
          "source_id": "care02",
          "locator": "CS-ASH-02-S1-needs",
          "line_start": 47,
          "quote": "这个时段帮我起身和准备普通水。"
        }
      ],
      "art_inference": "源文只支持人物、物件与边界；本具体手位、物件朝向和重心是可逆日常动作提案，不冒充台本已发生的事件或医学建议。",
      "start_pose_description_only": "仍在原椅上坐稳，双脚和臀部不移动；右手准备落右大腿，左手准备轻搭左侧椅面边缘。",
      "pose": "保持原臀部落点和双脚地面接触，肩胸小幅向人物左侧（画面右、远离水杯）转约十五至二十度，头跟随看向左前方，不能只转头。右掌（画面左）实贴自己的右大腿膝上；左掌（画面右）从左膝移到左髋旁原木椅座面的外缘轻搭，手指沿座面边向下自然弯，左肘仍弯曲而不锁直推撑。肩线因侧转可读地改变，但臀部不抬、躯干不前冲，后腰仍与原布卷保持支撑接触，布卷不抽出也不移位。衣摆随小幅转体自然跟随。",
      "end_pose_description_only": "肩胸可回母图朝向、左手可回左大腿；这只是文字，不补转回帧，不表示可以自行起立。",
      "transition_scope": "起止只是文字供以后制作参考；本轮只计划pose描述的一张独立静态关键姿态，未制作起止帧、过渡或连续循环。A1/A2不构成默认先后顺序。",
      "contact_and_support_checks": [
        "臀部整个承重区仍贴椅面，不露离座空隙，双脚完全留在原落点",
        "右掌贴右大腿，左掌接原左侧椅座外缘；不造扶手、不抓椅背、不锁肘撑起",
        "后腰与布卷接触未断，重心留在椅座支撑区；椅凳腿和杯不挪动"
      ],
      "prop_state_and_retention": [
        "厚披肩仍覆肩背、前缘自然落膝，不新增动作道具",
        "杯、凳、布条不触碰；左手旧青仍只在原侧"
      ],
      "difference_from_mother_expression_and_batch": "上身真正侧转，加左手与椅座的新接点；区别本人E1落膝/E2拒绝抬掌及Nara坐姿对话、训练样板起坐/地坐/侧卧。",
      "risk_level": "high_seated_support",
      "reference_image_paths": [
        "Assets/CharacterDesigns/20261013/expressive/new_story/kuen/concept_v1/kuen_transparent.png"
      ],
      "reference_sha256": [
        "18f4a8f8b77e25529edee1c0d0055d063a22584bf7b625dc1f9660bb5eacdd61"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一人物身份、脸型、年龄、比例、衣装、配色及已有器物造型锚，用内置imagegen重新绘制一张独立非战斗全身动作关键姿态。保留母图成熟大头、短自然颈、紧凑成年身体与有组织的粗像素簇，不幼化、不拉成长身、不统一四人的脸。不镜像；下文左右均为人物自身解剖侧，并附画面侧。必须有真实手臂、身体或原道具接触变化，不能只改表情、低头或平移母图。完整头发、双手、双脚和全部保留器物，四周留透明边距。单人、单个瞬间、纯alpha透明背景，无背景、地板、投影、光晕、文字、数字、图标、边框、UI、第二个人、箭头、残影或多格。所有原物件只保一件，取出后原位置不再复制同件。不用脚本绘制人体、旋转肢体、插值、拉伸、拼接或强量化修错。没有动作结果、治疗、康复、付款、授权、所有权转移、任务结案或新剧情事实。\n人物：三十多岁成年男性、清醒能自主表达的患者；深棕短乱发、少量胡茬、烟灰蓝布衫、厚暖灰褐织披肩、深灰褐裤、松袜口与软便鞋。\n原侧别与锚定：旧青固定人物左手背（画面右），不得改侧或新增病灶。木椅、背部布卷、双脚原落点不挪；右侧（画面左）小凳、杯、布条原位不动，杯始终未触碰、未端起。\n本张动作：坐稳轻侧转并搭椅沿。保持原臀部落点和双脚地面接触，肩胸小幅向人物左侧（画面右、远离水杯）转约十五至二十度，头跟随看向左前方，不能只转头。右掌（画面左）实贴自己的右大腿膝上；左掌（画面右）从左膝移到左髋旁原木椅座面的外缘轻搭，手指沿座面边向下自然弯，左肘仍弯曲而不锁直推撑。肩线因侧转可读地改变，但臀部不抬、躯干不前冲，后腰仍与原布卷保持支撑接触，布卷不抽出也不移位。衣摆随小幅转体自然跟随。\n接触与重心：臀部整个承重区仍贴椅面，不露离座空隙，双脚完全留在原落点；右掌贴右大腿，左掌接原左侧椅座外缘；不造扶手、不抓椅背、不锁肘撑起；后腰与布卷接触未断，重心留在椅座支撑区；椅凳腿和杯不挪动。\n物件保留：厚披肩仍覆肩背、前缘自然落膝，不新增动作道具；杯、凳、布条不触碰；左手旧青仍只在原侧。\n剧情边界：成年自主表达不等于身体能力改变；当前卡写喝水要人扶，当前CS-ASH-02-S1-needs还写这个时段帮起身，故两姿保持臀部坐实、脚原位，不推起、不自行饮水。；不画治疗/医疗操作、康复、迁居、护理替换成立、观察同意或对伴侣的要求；坐姿变化只是可逆日常演出推断。；原手背旧青只保留，不展示现代针管、留置针、输液或新诊断；杯水和需求布条不变成可读数据。。\n硬约束：A1要操作正在披着的同一披肩，不变成独立毯子或增加一件衣物。；A2只旋转肩胸，不移动椅、抬臀、拔出布卷或呈站起势；手掌轻搭椅面而非撑体起立。。只画上述一个瞬间，不画文字说明的起止姿态。",
      "prompt_sha256": "ba952fa1b213794d3fd7548b81839d543f200f60e2fa125e04e102866c389677",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/third_new_character_actions_sources/kuen_A2_seated_turn_with_seat_contact_prompt.txt",
      "negative_constraints": [
        "A1要操作正在披着的同一披肩，不变成独立毯子或增加一件衣物。",
        "A2只旋转肩胸，不移动椅、抬臀、拔出布卷或呈站起势；手掌轻搭椅面而非撑体起立。",
        "成年自主表达不等于身体能力改变；当前卡写喝水要人扶，当前CS-ASH-02-S1-needs还写这个时段帮起身，故两姿保持臀部坐实、脚原位，不推起、不自行饮水。",
        "不画治疗/医疗操作、康复、迁居、护理替换成立、观察同意或对伴侣的要求；坐姿变化只是可逆日常演出推断。",
        "原手背旧青只保留，不展示现代针管、留置针、输液或新诊断；杯水和需求布条不变成可读数据。"
      ],
      "new_contact_prop": null,
      "animation_claim": false,
      "sequence_required": false,
      "new_story_fact": false,
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "revision_only_for": "明确可定位的人体/接触/道具数目侧别/身份等硬错；不是无止境美感迭代",
        "safety_blocked": "stop; no circumvention, prompt laundering or alternate generator"
      },
      "review_status": "planning_author_checked; independent_plan_review_pending"
    }
  ]
}
