# 岱珥 第十一批基础动作锁定

{
  "slug": "daier",
  "canonical_id": "FX-MAN",
  "name": "岱珥",
  "status": "planned_not_generated",
  "selection_status": "requested_candidate_retained_no_substitution",
  "current_card": {
    "path": "design/04_人物/野外人物/人物_FX-MAN_岱珥.md",
    "bytes": 1061,
    "sha256": "92ca69d13c523fc51686400e3a55e68456877b3325f19add44be9e3864ca8786",
    "source_id": "daier_card",
    "snapshot_path": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/files/design/04_人物/野外人物/人物_FX-MAN_岱珥.md"
  },
  "source_ids": [
    "daier_card",
    "field_dialogue",
    "field_dialogue_registry",
    "DT07",
    "daier_mother_raw",
    "daier_mother_transparent",
    "daier_mother_manifest",
    "daier_expression_final_status",
    "daier_expressions_view"
  ],
  "mother_image": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/daier/concept_v1/daier_v1_raw_imagegen.png",
    "raw_sha256": "89a6879812d2a3830ec9a073c350bc85149f890084c1e8e54bdd2f62cae3915a",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/daier/concept_v1/daier_transparent.png",
    "transparent_sha256": "cfc6697b7aeb2abfd199ff69e560e4913afaca5966382dd83318331ff463cfc8",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/daier/concept_v1/manifest.json",
    "manifest_sha256": "33e591614b422bccf47083646fe0dcf97dbd938b31f7cf36114a32c6ccf72c53",
    "independent_qa_source_id": "eleventh_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "分别实际查看本人raw、透明母图与旧表情浅板：五十来岁灰鬓看守，灰紫补丁长外套，画面右上臂和两侧衣摆原棕补丁，米麻衫与袖口。人物左臂从画面右横在身前，左手轻搭画面左的本人右前臂袖布；右臂向画面左下伸。旧钥匙串在画面右腰前，两鞋站地。旧过客冷嘲/危处警告保留这组理袖姿态。",
    "fixed_sides": "原灰紫旧外套、棕补丁位置、米麻内衫/袖口、腰带和双鞋保持；不新增现代西装翻领或纽扣。唯一原旧钥匙串保持挂在画面右腰前，数量和造型照母图，两手均不拿钥匙。钥匙仍是原没用的旧钥匙，不暗示开门；两手只按本张动作移动。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/daier/expressions_v1/review/daier_light_board.png"
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
    "只理本人外套或舒展双臂，不掸环境门廊、不加扫帚/门/家具，不开锁、不递钥匙、不作庄园归属/通行承诺，不画DT07结果。",
    "五十来岁成熟年龄照母图，不年轻化；岱珥daier/FX-MAN与达珥daer为不同人物。"
  ],
  "risks": [
    "不能复画母图左手搭右袖；两手必须各自离开原接点，形成明确的双手分开或双臂展开。",
    "钥匙串必须仍在画面右腰可读，双手理衣只触钥匙上方的外套宽面；不拉开外套露出新内容。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/daier/noncombat_basics_v1",
  "plans": [
    {
      "key": "daier_A1_smooth_both_coat_fronts",
      "title_zh": "双掌顺平外套前片",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "daier_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "披着补过的旧外套"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-MAN／闲谈1，只保旧钥匙边界",
          "line_start": 771,
          "quote": "钥匙串是旧的。锁早换了。"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托杯/理围裙/抬板/垂板/理外套/舒肩/扶膝/理发是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图左手横身搭右袖、右臂向下的站姿开始。",
      "pose": "两鞋分开稳站，躯干直立。人物左手完全离开原右前臂袖布、右手从画面左低位抬起，两手各自分开到同侧胸腹之间，左右掌心各平贴本人同侧的一片灰紫外套前片宽布面，位置在腰带和钥匙串上方。两肘自然向外打开，双前臂各形成短斜线，停在向下顺平自己外套的一瞬。两掌不交叉、不抓衣领、不拉开外套，原补丁与米麻内衫不改。钥匙仍挂画面右腰前并完整可见。头脸朝画面右、神态平常。",
      "end_pose_description_only": "两掌可离开外套前片自然放下；不脱衣、不变钥匙状态。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "原左手横身搭右袖的接点解除，两掌左右分开、各贴一侧胸腹外套前片，两肘外开；钥匙在两手下方。",
      "pose_specific_sidedness": "人物右掌在画面左贴本人右前片，左掌画面右贴本人左前片；原钥匙串仍画面右腰前，双手都在其上方。",
      "contact_and_support_checks": [
        "每掌仅贴一侧衣布，不交叉搭袖、不拿钥匙、不抓细小扣结。",
        "外套前片只轻折、不脱落或翻开，原棕补丁保持原部位。",
        "双手、腰钥匙与鞋都可读，身体比例和成熟年龄不变。"
      ],
      "prop_state_and_retention": [
        "原灰紫旧外套、棕补丁位置、米麻内衫/袖口、腰带和双鞋保持；不新增现代西装翻领或纽扣。唯一原旧钥匙串保持挂在画面右腰前，数量和造型照母图，两手均不拿钥匙。钥匙仍是原没用的旧钥匙，不暗示开门；两手只按本张动作移动。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧表情左手搭对侧右袖、右手低垂；本张两掌分别回到各自前片，双肘外开，是真实双臂接触改变。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/daier/concept_v1/daier_transparent.png"
      ],
      "reference_sha256": [
        "cfc6697b7aeb2abfd199ff69e560e4913afaca5966382dd83318331ff463cfc8"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：岱珥 FX-MAN。五十来岁的男庄园看守，深灰褐头发带明显白鬓、无须成熟长面，脸朝画面右。灰紫旧长外套、原棕补丁、米麻内衫及袖口、棕腰带、褐裤和深棕鞋靴完整保留。只用岱珥FX-MAN/daier，不是达珥daer。\n固定衣装与原物件：原灰紫旧外套、棕补丁位置、米麻内衫/袖口、腰带和双鞋保持；不新增现代西装翻领或纽扣。唯一原旧钥匙串保持挂在画面右腰前，数量和造型照母图，两手均不拿钥匙。钥匙仍是原没用的旧钥匙，不暗示开门；两手只按本张动作移动。\n本张动作：双掌顺平外套前片。两鞋分开稳站，躯干直立。人物左手完全离开原右前臂袖布、右手从画面左低位抬起，两手各自分开到同侧胸腹之间，左右掌心各平贴本人同侧的一片灰紫外套前片宽布面，位置在腰带和钥匙串上方。两肘自然向外打开，双前臂各形成短斜线，停在向下顺平自己外套的一瞬。两掌不交叉、不抓衣领、不拉开外套，原补丁与米麻内衫不改。钥匙仍挂画面右腰前并完整可见。头脸朝画面右、神态平常。\n本张侧别：人物右掌在画面左贴本人右前片，左掌画面右贴本人左前片；原钥匙串仍画面右腰前，双手都在其上方。\n必须明显可见：原左手横身搭右袖的接点解除，两掌左右分开、各贴一侧胸腹外套前片，两肘外开；钥匙在两手下方。\n接触与支撑：每掌仅贴一侧衣布，不交叉搭袖、不拿钥匙、不抓细小扣结。；外套前片只轻折、不脱落或翻开，原棕补丁保持原部位。；双手、腰钥匙与鞋都可读，身体比例和成熟年龄不变。。\n",
      "prompt_sha256": "dff91b8c154533887c9733885648ef7f5a0fb466cc2b2933021349a94b19e730",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/daier_A1_smooth_both_coat_fronts_prompt.txt",
      "negative_constraints": [
        "只理本人外套或舒展双臂，不掸环境门廊、不加扫帚/门/家具，不开锁、不递钥匙、不作庄园归属/通行承诺，不画DT07结果。",
        "五十来岁成熟年龄照母图，不年轻化；岱珥daier/FX-MAN与达珥daer为不同人物。",
        "不能复画母图左手搭右袖；两手必须各自离开原接点，形成明确的双手分开或双臂展开。",
        "钥匙串必须仍在画面右腰可读，双手理衣只触钥匙上方的外套宽面；不拉开外套露出新内容。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧表情左手搭对侧右袖、右手低垂；本张两掌分别回到各自前片，双肘外开，是真实双臂接触改变。"
      }
    },
    {
      "key": "daier_A2_open_arms_low_shoulder_stretch",
      "title_zh": "双臂侧下舒肩",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "daier_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "五十来岁的男人"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-MAN／知情边界",
          "line_start": 764,
          "quote": "不替旧主人认领庄园"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托杯/理围裙/抬板/垂板/理外套/舒肩/扶膝/理发是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图左手搭右袖、右臂低伸开始。",
      "pose": "两鞋约肩宽全掌稳站，躯干自然直立。双手完全离开原理袖位置，两上臂向各自侧下方展开，两肘轻弯，右前臂伸向画面左外侧、左前臂伸向画面右外侧，双手松弛地落在腰高附近且各离开身体侧线至少一个掌宽。掌心朝内下，手指自然并拢微弯，不对人摊掌、不招手。原灰紫长外套随手臂自然舒开但不脱落，钥匙仍低挂画面右腰前。头脸朝画面右、神态平常。",
      "end_pose_description_only": "两臂可自然放回身侧；不把舒展解释为康复或体力回复。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "两只手都离开身前，双臂同时侧下展开形成明显宽轮廓；原搭袖接点消失，钥匙仍无人触碰。",
      "pose_specific_sidedness": "人物右臂向画面左展开、左臂向画面右展开；钥匙固定画面右腰前，面朝仍向画面右。",
      "contact_and_support_checks": [
        "两肩肘腕自然连贯、双手可见且不多手，不把手留在另一条袖上。",
        "双手松弛朝内下，不读成阻拦、发令、招手、施法或迎客承诺。",
        "两脚完整支撑，外套补丁与钥匙仍可见，头身不拉长。"
      ],
      "prop_state_and_retention": [
        "原灰紫旧外套、棕补丁位置、米麻内衫/袖口、腰带和双鞋保持；不新增现代西装翻领或纽扣。唯一原旧钥匙串保持挂在画面右腰前，数量和造型照母图，两手均不拿钥匙。钥匙仍是原没用的旧钥匙，不暗示开门；两手只按本张动作移动。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧表情是一手横身搭袖，本张双臂离身向两侧展开；与A1双掌贴前片的收拢手位相反，轮廓区别大。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/daier/concept_v1/daier_transparent.png"
      ],
      "reference_sha256": [
        "cfc6697b7aeb2abfd199ff69e560e4913afaca5966382dd83318331ff463cfc8"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：岱珥 FX-MAN。五十来岁的男庄园看守，深灰褐头发带明显白鬓、无须成熟长面，脸朝画面右。灰紫旧长外套、原棕补丁、米麻内衫及袖口、棕腰带、褐裤和深棕鞋靴完整保留。只用岱珥FX-MAN/daier，不是达珥daer。\n固定衣装与原物件：原灰紫旧外套、棕补丁位置、米麻内衫/袖口、腰带和双鞋保持；不新增现代西装翻领或纽扣。唯一原旧钥匙串保持挂在画面右腰前，数量和造型照母图，两手均不拿钥匙。钥匙仍是原没用的旧钥匙，不暗示开门；两手只按本张动作移动。\n本张动作：双臂侧下舒肩。两鞋约肩宽全掌稳站，躯干自然直立。双手完全离开原理袖位置，两上臂向各自侧下方展开，两肘轻弯，右前臂伸向画面左外侧、左前臂伸向画面右外侧，双手松弛地落在腰高附近且各离开身体侧线至少一个掌宽。掌心朝内下，手指自然并拢微弯，不对人摊掌、不招手。原灰紫长外套随手臂自然舒开但不脱落，钥匙仍低挂画面右腰前。头脸朝画面右、神态平常。\n本张侧别：人物右臂向画面左展开、左臂向画面右展开；钥匙固定画面右腰前，面朝仍向画面右。\n必须明显可见：两只手都离开身前，双臂同时侧下展开形成明显宽轮廓；原搭袖接点消失，钥匙仍无人触碰。\n接触与支撑：两肩肘腕自然连贯、双手可见且不多手，不把手留在另一条袖上。；双手松弛朝内下，不读成阻拦、发令、招手、施法或迎客承诺。；两脚完整支撑，外套补丁与钥匙仍可见，头身不拉长。。\n",
      "prompt_sha256": "8b1f46c07ee71b61523a0b778d42b639bbbe5d113509a31443cc27f9f4f50e1d",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/daier_A2_open_arms_low_shoulder_stretch_prompt.txt",
      "negative_constraints": [
        "只理本人外套或舒展双臂，不掸环境门廊、不加扫帚/门/家具，不开锁、不递钥匙、不作庄园归属/通行承诺，不画DT07结果。",
        "五十来岁成熟年龄照母图，不年轻化；岱珥daier/FX-MAN与达珥daer为不同人物。",
        "不能复画母图左手搭右袖；两手必须各自离开原接点，形成明确的双手分开或双臂展开。",
        "钥匙串必须仍在画面右腰可读，双手理衣只触钥匙上方的外套宽面；不拉开外套露出新内容。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/eleventh_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧表情是一手横身搭袖，本张双臂离身向两侧展开；与A1双掌贴前片的收拢手位相反，轮廓区别大。"
      }
    }
  ]
}

只按本姿独立prompt调用。母图实比，不套数字。每姿1首稿，最多1次真硬错修订，安全block停止；内置imagegen负责人物，脚本只alpha≤8与隐藏RGB清理、整图nearest等比排版；保全返回payload与所有尝试。不动画、不游戏落地、不Git、不上传。
