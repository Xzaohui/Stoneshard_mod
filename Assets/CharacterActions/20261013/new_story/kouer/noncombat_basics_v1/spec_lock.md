# 当前基础动作制作约束

{
  "character": "kouer",
  "name": "蔻珥",
  "brief_sha256": "ee5505e87bba25bac7d0ae7d978d4ea8e3507257a068f33a1c189792321ad11e",
  "status": "plan_gate_passed_generation_pending",
  "palette_size_style": "严格延续本人当前母图的配色、成熟紧凑头身与粗像素簇；高分辨率概念尺寸由内置生成决定，非游戏规格。",
  "mother": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/kouer/concept_v1/kouer_v1_raw_imagegen.png",
    "raw_sha256": "b58f27d1de28aaeab1f14a003633587680edeb7012127e804593d147ffdb183e",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/kouer/concept_v1/kouer_transparent.png",
    "transparent_sha256": "30b2b6ec4a29139a8520b5de382cd93e3cb002a9d94241a0502698a79e385500",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/kouer/concept_v1/manifest.json",
    "manifest_sha256": "72529a2d05f1073c4b627c1d0f767fceee5264a159cc506157487d7d4bcfe8e8",
    "independent_qa_source_id": "fourth_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "已逐张查看raw与transparent：灰蓝外头巾与米白内头巾、暗褐长衣、米白袖裙边和棕鞋。单个木桶在身前偏人物右侧（画面左）落地，两手并排握弧形提把顶段。桶内原白石灰小堆和两道铁箍清楚；E1/E2仍同样两手搭把、桶底落地，仅脸部变化。",
    "fixed_sides": "桶始终是母图那一个，位于身前偏人物右侧（画面左）；两道铁箍、弧形原提把与内部白石灰堆保持。A1双手各握原把顶段并排上提；A2右手（画面左）握原把顶部，左手（画面右）触桶口外缘，绝不碰石灰。双头巾外灰蓝内米白，不镜像。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/kouer/expressions_v1/review/kouer_expressions_light_zh.png"
  },
  "plans": [
    {
      "key": "kouer_A1_low_lift_lime_bucket",
      "title_zh": "双手低提原木桶",
      "pose": "双手仍并排握同一弧形提把顶部，两肘从原下垂姿略弯，将原桶整体平稳提起一小段。桶仍在身前偏人物右侧（画面左），竖直不倾斜，桶底离双鞋共同落地基线约半个鞋面高度，留出清楚透明间隙，不挪到膝上或胸前。双臂与肩部有自然向上的提力关系，肩平、躯干站直，双脚原位全掌着地。原灰堆保持静止不扬起，面部保持克制日常神情。",
      "contact_and_support_checks": [
        "双手真正握同一把顶部、指组包住把，原把两端接桶耳",
        "桶底与原足底基线间有可见间隙，不能仍落地冒称提起，也不能漂浮脱手",
        "双脚全掌原位，桶不歪、石灰不离桶"
      ],
      "prop_state_and_retention": [
        "原木桶、弧形提把、两道铁箍及原石灰量都保留",
        "两层头巾和裙摆保持完整；不新增移动工具"
      ],
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "revision_only_for": "明确可定位的身份、人体、接触支撑、道具数量或侧别、裁切与透明硬错；不作无限审美迭代。",
        "after_failed_revision": "保留所有原稿并标缺项；不得加第三稿或转脚本修人体。",
        "safety_blocked": "stop; no circumvention, prompt laundering or alternate generator"
      }
    },
    {
      "key": "kouer_A2_grounded_bucket_rim_steady",
      "title_zh": "俯身扶稳落地桶沿",
      "pose": "原桶底完全落在母图的隐含地面基线、位置不移，人物双膝小幅弯曲并从髋部温和前倾。右手（画面左）仍握同一弧形提把顶部，手腕顺着把自然下垂；左手（画面右）松开把，向下伸至桶口画面右侧的外缘，掌根贴外侧木桶沿，指组向外下方弯在桶壁上。左手及指尖始终留在桶口外面，不伸进白灰、不压灰堆。两臂高度与接点清楚不同，桶靠自身底面承重，双脚原位稳定，头略随上身看桶沿。",
      "contact_and_support_checks": [
        "桶底贴原隐含地面，右手握把顶、左掌扶外木缘，接点分离可读",
        "左指组全部在桶口外缘外侧，不接触白灰；不能用灰堆托住手",
        "双脚全掌原位、双膝不触地；桶体竖直，提把两端仍接原桶耳"
      ],
      "prop_state_and_retention": [
        "同桶同灰、桶体不变形，不出现第二把或第三只手",
        "原衣裙、双头巾和两鞋全保留，不加地板、封条或场景"
      ],
      "generation_budget": {
        "initial": 1,
        "max_hard_error_revisions": 1,
        "revision_only_for": "明确可定位的身份、人体、接触支撑、道具数量或侧别、裁切与透明硬错；不作无限审美迭代。",
        "after_failed_revision": "保留所有原稿并标缺项；不得加第三稿或转脚本修人体。",
        "safety_blocked": "stop; no circumvention, prompt laundering or alternate generator"
      }
    }
  ],
  "processing": "仅alpha≤8透明清理、nearest等比展示；不重画人体、不拉伸。",
  "pipeline_note": "读取真实归档pixel skill。references/executor-pixel.md不存在，不杜撰。延续STYLE_DIRECTION与用户持续基础动作授权。"
}
