# 当前基础动作制作约束

{
  "character": "miloer",
  "name": "米洛珥",
  "brief_sha256": "ee5505e87bba25bac7d0ae7d978d4ea8e3507257a068f33a1c189792321ad11e",
  "status": "plan_gate_passed_generation_pending",
  "palette_size_style": "严格延续本人当前母图的配色、成熟紧凑头身与粗像素簇；高分辨率概念尺寸由内置生成决定，非游戏规格。",
  "mother": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/miloer/concept_v1/miloer_v1_raw_imagegen.png",
    "raw_sha256": "669f8424bd7b5b99f822edd12f9da19c48186887df0c3677ce2877251506396f",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/miloer/concept_v1/miloer_transparent.png",
    "transparent_sha256": "c1c10e6f1dc19bebb89493b8c0e9a32616272f4fea7f1b5c70c8252b11d47275",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/miloer/concept_v1/manifest.json",
    "manifest_sha256": "37862a490a93abaeb2aeb75f2a10bfd9d53039886239708774e0c5ba7c54c646",
    "independent_qa_source_id": "fourth_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "已逐张查看raw与transparent：四十来岁成年男子，厚下颌、深棕发夹灰鬓及短须，米麻衫双袖有麻绳结，灰绿围裙。左手（画面右）托红棕小陶罐，浅棕圆盖及颈部绳结完整；右手（画面左）向下展开。E1/E2右臂下垂、左手仍托罐，没有右手碰盖或跨身理左袖的接触。",
    "fixed_sides": "同一小陶油膏罐固定由左掌（画面右）承托，原盖与颈绳结始终封合；不得开盖或换成现代旋盖瓶。双袖麻绳结各留本侧。A1右指组触盖顶；A2右手跨到左袖布褶、不得穿过持罐左腕或陶罐。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/miloer/expressions_v1/review/miloer_expressions_light_zh.png"
  },
  "plans": [
    {
      "key": "miloer_A1_touch_closed_jar_lid",
      "title_zh": "托罐轻按原盖",
      "pose": "左肘（画面右）保持弯曲，左掌从下托住同一小陶罐，罐移到左下胸前以看清原盖。右臂（画面左）弯向身体中线，右手拇指留在盖侧，另外并拢的指腹轻压原浅棕圆盖上面，形成看得清的盖顶接点。罐体保持竖直、盖完全贴合原罐口、颈绳结保持原样；两手分工清楚，一手托底、一手轻按盖。头略看自己的手，双足原位站稳。",
      "contact_and_support_checks": [
        "左掌托底、右指腹在盖顶，两个手腕与各自袖口连续",
        "盖和罐口间不出现开口或露膏，颈绳原结不断",
        "双脚落地、两肘不高过肩，罐不悬浮不翻倒"
      ],
      "prop_state_and_retention": [
        "一只原红棕陶罐、一片原盖、一条原颈绳；没有复制到腰侧的第二罐",
        "两袖绑绳与围裙全保留"
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
      "key": "miloer_A2_smooth_left_tied_cuff",
      "title_zh": "持罐按平左袖褶",
      "pose": "左肘（画面右）弯曲，左前臂近水平向前，左掌向上稳定托住同一竖直封罐，罐保持在左腹前并略离衣身。右手（画面左）从腹前横伸到左袖口外侧，右掌与并拢指组轻压左袖原麻绳结下方的米白布褶，让褶边贴回左腕上方。右手接触的是布料，不抓绳尾、不解绳结、不触陶罐。右前臂从腹前横过但不穿过左腕，两袖原绳结仍可读，头只略低看手，双脚原位站稳。",
      "contact_and_support_checks": [
        "左手持续托底，罐和盖不倾斜；右手在左袖外侧而非压罐",
        "左袖绳结上方仍清楚，右指组只按结下方布褶，不把结变成散绳",
        "双手与袖口解剖连续，前臂交叠有清楚前后关系，不生第三手"
      ],
      "prop_state_and_retention": [
        "原封罐、盖和颈绳不动用；左手不能空手",
        "双袖各一原麻绳结，右袖结也保留可见线索"
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
