# 本角色表情制作锁定

{
  "slug": "jier",
  "name": "蓟珥",
  "canonical_id": "FX-FRM",
  "brief_sha256": "eaf404168c49eb018ca4a202730db383ea97d25dc0508210fa09dca06f279bdf",
  "mother": {
    "directory": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1",
    "selected_raw": {
      "path": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/jier_v1_raw_imagegen.png",
      "sha256": "fecdbec699445ea31d17cffc6371814c620145d1e29304a91a1600554e12e3a5"
    },
    "transparent": {
      "path": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/jier_transparent.png",
      "sha256": "47c591b61400237112425f97f213b3663531eae495465c37bc067fbf1290d239"
    },
    "manifest": {
      "path": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/manifest.json",
      "sha256": "a73663227af6d4cd6ec2f318353d9bd794158ca5d9e3b8227a52ae92199f13b4"
    },
    "existing_review_status": "final_clean_and_presentation_pass",
    "raw_canvas": [
      1118,
      1407
    ],
    "transparent_canvas": [
      1118,
      1407
    ],
    "raw_mode": "RGBA",
    "transparent_mode": "RGBA",
    "actual_raw_and_transparent_viewed": true,
    "view_method": "2026-10-14本任务tools.view_image分别实际查看四人final raw与transparent，共8张；不以历史QA代替看图。",
    "hashes_verified_against_manifest_and_final_independent_qa": true,
    "manifest_entries_reverified": 21
  },
  "locks": [
    "四人的最终raw及transparent是各自唯一身份、服装、道具与实际比例母图；四人均选本人concept_v1中的v1，不以风格参考或他人图替代。",
    "画布意图：索妲1060×1484；珂琳、蓟珥、绥珥各1118×1407。单人纵向完整全身，保头发、双手、所有衣物道具、双鞋及合理留边；不强行统一比例或画布。",
    "年龄分别为四十多岁农妇、17–18岁姑娘、五十来岁男子、四十来岁妇人。珂琳保母图普通完整工作服与本人年轻面容，不幼化、不成人化、不性感化。",
    "八张情绪以眉眼嘴为主，微动作辅助。四人都保持本人原手位附近，索妲手仍在巾边与篮柄，珂琳手留袋旁和低垂，蓟珥手留腰前，绥珥握尺托腕；不使用全员抬掌。",
    "保留空篮、缝在围裙上的草药袋、两卷袖和土迹、半截软布尺及各自侧别；不借表情增加道具、抹痕、换服装、改头身或新伤。",
    "每组两图是可逆美术提案而非连续结局；本人存活、在场、愿谈且有相应有限见闻才适用。拒绝、缺席、逐项授权优先，不暗示任务完成、付款、治疗、康复、信任或关系改变。",
    "旧FX任务回访只作语气资料，不用来补全现行DT09署名、DT05有限分配、DT02配水或SQ03救济结果。地理关联不等于同一现场，不假定角色自动跨区到场。",
    "绥珥FX-LOT必须用suier_lot，严禁与燧珥FX-CP1/suier混同；所有工作slug都不作为官方英文名。",
    "沿用母图有组织的粗像素簇与低魔中世纪质感，不硬缩35px、不量化掩盖五官，不把概念声称为原生像素网格、part/frame/mask/origin、装备兼容、动画或runtime验证。"
  ],
  "prop_sides": [
    "两手始终在腰前原有低位，画面左手略高、画面右手略低，搓土时手指接触合理；可微停搓动，不能高抬开掌或指向画外院门。",
    "两袖卷起程度、米麻袖口和少量指端土色保持；土不是血，不添新伤，不把手洗净解释成劳作完成。",
    "不添加锄、桶、水碗、粮袋、账簿或武器；保持灰发灰须、五十来岁本人脸型及双脚承重，不年轻化或画衰弱倒地。"
  ],
  "budget": {
    "initial_images_per_expression": 1,
    "max_hard_error_revisions_per_expression": 1,
    "maximum_images": 16,
    "revision_allowed_for": [
      "身份/年龄/服装/比例明显偏离锁定母图",
      "肢体或手持接触明显不可能、关键轮廓被截断、必备道具丢失或换侧",
      "脸部不可读、所要求的情绪未形成或两幅几乎复制母图",
      "添加承诺/付款/治疗/续约/开闸等未发生结果或违反自主性"
    ],
    "not_revision_triggers": [
      "轻微自然表情差异",
      "合理遮挡、发丝、褶皱或掌指细节变化",
      "未达到臆定眉角、单像素位置或统一比例数字"
    ],
    "if_revision_still_fails": "保留首稿和唯一修订，标为待处理并报告具体硬错；不无限返工，不假称通过。",
    "planned_selected_images": 8
  },
  "expressions": [
    {
      "id": "E1",
      "key": "jier_E1_attentive_well_talk",
      "label_zh": "谈井专注",
      "scene_proposal": "话题转到院里哪口井还有水，他比平时多解释两句，只说自己有限见闻。",
      "face_changes": "原来压低的眉稍舒展，内眉微抬，双眼比母图略睁开但不扩大眼球，视线仍偏画面左；嘴形成清楚的小开口、唇角放松而不微笑，显出愿意认真说明熟悉事物的专注。保留灰须周围的成熟鼻唇。",
      "minimal_gesture": "上身仅极轻微倾向谈话，双手保持腰前原接触关系，搓土暂缓；不伸手指井、不拿水、不改变双脚承重。",
      "difference_from_static_and_pair": "母图低眉寡言，E1眉眼舒展与更清楚的小说话口形；E2眉压低、眼收、嘴合成平线。不得只把原嘴扩大或依赖手势。",
      "condition_and_limit": "只演谈井的投入，不保证饮水安全、井已恢复、水量足够、DT02配水完成或邻村无事；不出现品尝水、递水或无条件允许入院的动作，不公开粮量。",
      "story_support": {
        "path": "design/02_世界与地图/特殊地点与野外NPC/台本_FX_野外人物对白.md",
        "sha256": "f599af46e631f3dc9e80d20229d858b594aba754edd5c5e3e99015424ba67a3a",
        "locator": "L888体貌；L890口吻；L892知情范围；L896—897只限本人取水/缸位置；L910—914关联槽"
      },
      "research_support": {
        "path": "research/field-npc-dialogue.json",
        "sha256": "185900bb86b5b7fbe4586489d664584e28ccef2718c591841ab4a3f86ccd5b4d",
        "locator": "npcs[id=FX-FRM].voice/knows/not_knows/greetings"
      },
      "output_stem": "jier_E1_attentive_well_talk",
      "production_status": "not_generated",
      "prompt_status": "ready_text_not_executed"
    },
    {
      "id": "E2",
      "key": "jier_E2_quiet_no_lodging",
      "label_zh": "闭口谢客",
      "scene_proposal": "面对留宿的请求，简短拒绝后停下答话，仍留意院门方向。",
      "face_changes": "两眉压成较平的低线并轻聚，眼帘收一点、目光留在画面左的院门方向；嘴从母图微启变为完整短平闭唇，口角微下压。脸是沉静、有界限的谢客，不能画憎恨、威胁、恐慌或即将哭泣。",
      "minimal_gesture": "下巴轻收，头向院门方向略偏；双手仍在腰前，搓指动作停住但不握拳，两脚不动，不做赶人挥手。",
      "difference_from_static_and_pair": "母图微张嘴的短答变为完全闭口的静默；E1眉眼舒展并正说熟悉的井，E2低眉窄眼平唇，不用同一面孔加不同标签。",
      "condition_and_limit": "只表示这一请求被拒，不把人物定成敌对、不宣告以后永不接待或关系恶化；不画屋门关闭、留宿接受、存粮展示、院门通行权或DT02结案。",
      "story_support": {
        "path": "design/02_世界与地图/特殊地点与野外NPC/台本_FX_野外人物对白.md",
        "sha256": "f599af46e631f3dc9e80d20229d858b594aba754edd5c5e3e99015424ba67a3a",
        "locator": "L888说话先看院门；L890寡言；L898夜里不开门；L904拒绝留宿；L914本人缺席不自取水"
      },
      "research_support": {
        "path": "research/field-npc-dialogue.json",
        "sha256": "185900bb86b5b7fbe4586489d664584e28ccef2718c591841ab4a3f86ccd5b4d",
        "locator": "npcs[id=FX-FRM].look/voice/greetings[night]/site_lines[refusal]"
      },
      "output_stem": "jier_E2_quiet_no_lodging",
      "production_status": "not_generated",
      "prompt_status": "ready_text_not_executed"
    }
  ]
}
