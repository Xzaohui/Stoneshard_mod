# 蓟珥 第十批基础动作锁定

{
  "slug": "jier",
  "canonical_id": "FX-FRM",
  "name": "蓟珥",
  "status": "planned_not_generated",
  "selection_status": "requested_candidate_retained_no_substitution",
  "current_card": {
    "path": "design/04_人物/野外人物/人物_FX-FRM_蓟珥.md",
    "bytes": 1029,
    "sha256": "7c22bfa2d44acf4dcea2e44f0f8da5b06483a1fe4798031e553c083974f1d83c",
    "source_id": "jier_card",
    "snapshot_path": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/files/design/04_人物/野外人物/人物_FX-FRM_蓟珥.md"
  },
  "source_ids": [
    "jier_card",
    "field_dialogue",
    "field_dialogue_registry",
    "DT02",
    "jier_mother_raw",
    "jier_mother_transparent",
    "jier_mother_manifest",
    "jier_expression_final_status",
    "jier_expressions_view"
  ],
  "mother_image": {
    "raw": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/jier_v1_raw_imagegen.png",
    "raw_sha256": "fecdbec699445ea31d17cffc6371814c620145d1e29304a91a1600554e12e3a5",
    "transparent": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/jier_transparent.png",
    "transparent_sha256": "47c591b61400237112425f97f213b3663531eae495465c37bc067fbf1290d239",
    "manifest": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/manifest.json",
    "manifest_sha256": "a73663227af6d4cd6ec2f318353d9bd794158ca5d9e3b8227a52ae92199f13b4",
    "independent_qa_source_id": "tenth_mother_qa",
    "independent_qa_selected_status": "final_clean_and_presentation_pass",
    "actual_visual_observation": "本任务分别实际查看raw、透明母图与旧表情浅板：五十来岁男性农人，灰发灰须、灰蓝粗衫、两袖卷起，棕腰带褐裤、深棕绑腿鞋靴。双手在腰前，人物右手画面左略高，左手画面右略低，正在轻搓手指；有少量土色但不作逐甲缝复原声明。旧谈井专注/闭口谢客保留腰前手位，未见两臂展开或半蹲双掌扶膝。",
    "fixed_sides": "没有手持物，不添加工具、桶碗、粮袋或家具。母图两只袖口继续卷在原高度，米麻袖缘、腰带和双靴保留；指端原少量土迹仍是土，不改成血、不宣称洗净。灰发灰须与真实五十来岁脸保持；双手按本张动作移动。",
    "raw_and_transparent_actually_viewed": true,
    "expression_board_actually_viewed": "Assets/CharacterDesigns/20261013/expressive/new_story/jier/expressions_v1/review/jier_expressions_light.png"
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
    "普通舒肩或短暂半蹲自理姿态，不增加疲病、受伤、康复或体能恢复设定。",
    "不舀水、不引人入院、不留宿、不认证井水、不暴露存粮、不替邻村作保、不画DT02配给结果。"
  ],
  "risks": [
    "展开双臂不能变招手、拦路、拥抱或施法；动作以整臂轮廓而非改脸判断。",
    "半蹲要明显降髋屈膝、两掌分别贴两腿裤面，双靴平稳支撑，不跪地、不画跌倒。"
  ],
  "proposed_output_directory": "Assets/CharacterActions/20261013/new_story/jier/noncombat_basics_v1",
  "plans": [
    {
      "key": "jier_A1_open_arms_low_shoulder_stretch",
      "title_zh": "双臂侧下舒肩",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "jier_card",
          "locator": "体貌与随身",
          "line_start": 17,
          "quote": "五十来岁的男人，袖口卷起"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-FRM／闲谈1，仅支持普通劳作背景",
          "line_start": 899,
          "quote": "地还在种。种得少，够吃就行。"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托篮/扶巾/理袖/扶腰/舒肩/半蹲/托尺/拂围裙是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图双手腰前轻搓手指开始。",
      "pose": "双靴自然分站、全掌着地，躯干维持原长度自然直立。双手从原腰前搓指位置完全分开，两上臂向身体两侧展开，双肘轻弯，两前臂斜向侧下伸展，让两只放松的手分别远离左右腰线、落在下胸至腰部高度。右臂延伸到画面左外侧，左臂延伸到画面右外侧；手掌自然朝内下，指组松弛，不指人、不握拳。两肩轻舒展、头脸朝画面左，表情平常。原两只卷袖和指端少量土色保留。",
      "end_pose_description_only": "双臂可自然收回放下；不把舒展解释为体能恢复或劳作完成。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "两条手臂同时离开身前向侧下展开，两手各远离躯干侧线至少一个掌宽，形成明显宽轮廓；不是只分开几根手指。",
      "pose_specific_sidedness": "人物右臂向画面左、左臂向画面右舒展；不镜像面向，左右靴保持各自原侧。",
      "contact_and_support_checks": [
        "双肩肘腕连贯，两手分离可见，原卷袖随手臂但不滑脱。",
        "没有接触他人或空气中的物体，不绘招手、拦路、施法或残影。",
        "身体不拉长、不后仰失衡，双靴支撑完整，指端土色不变成飞尘。"
      ],
      "prop_state_and_retention": [
        "没有手持物，不添加工具、桶碗、粮袋或家具。母图两只袖口继续卷在原高度，米麻袖缘、腰带和双靴保留；指端原少量土迹仍是土，不改成血、不宣称洗净。灰发灰须与真实五十来岁脸保持；双手按本张动作移动。"
      ],
      "difference_from_mother_expression_and_batch": "母图/表情两手腰前相近，本张整臂左右展开；与双掌扶膝的低位半蹲在手位、支撑和轮廓上均不同。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/jier_transparent.png"
      ],
      "reference_sha256": [
        "47c591b61400237112425f97f213b3663531eae495465c37bc067fbf1290d239"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：蓟珥 FX-FRM。五十来岁的农宅男性住户，母图灰棕短发、灰须、宽额与方实成熟脸，脸朝画面左。旧灰蓝粗衫、米麻领边与两只原卷袖、棕腰带、褐裤和深棕绑腿鞋靴完整保留。\n固定衣装与原物件：没有手持物，不添加工具、桶碗、粮袋或家具。母图两只袖口继续卷在原高度，米麻袖缘、腰带和双靴保留；指端原少量土迹仍是土，不改成血、不宣称洗净。灰发灰须与真实五十来岁脸保持；双手按本张动作移动。\n本张动作：双臂侧下舒肩。双靴自然分站、全掌着地，躯干维持原长度自然直立。双手从原腰前搓指位置完全分开，两上臂向身体两侧展开，双肘轻弯，两前臂斜向侧下伸展，让两只放松的手分别远离左右腰线、落在下胸至腰部高度。右臂延伸到画面左外侧，左臂延伸到画面右外侧；手掌自然朝内下，指组松弛，不指人、不握拳。两肩轻舒展、头脸朝画面左，表情平常。原两只卷袖和指端少量土色保留。\n本张侧别：人物右臂向画面左、左臂向画面右舒展；不镜像面向，左右靴保持各自原侧。\n必须明显可见：两条手臂同时离开身前向侧下展开，两手各远离躯干侧线至少一个掌宽，形成明显宽轮廓；不是只分开几根手指。\n接触与支撑：双肩肘腕连贯，两手分离可见，原卷袖随手臂但不滑脱。；没有接触他人或空气中的物体，不绘招手、拦路、施法或残影。；身体不拉长、不后仰失衡，双靴支撑完整，指端土色不变成飞尘。。\n",
      "prompt_sha256": "cede895d2f7e2e99f6beef35e6f0a4b3e9ef252df78147acdd38a7c432f56cb8",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/jier_A1_open_arms_low_shoulder_stretch_prompt.txt",
      "negative_constraints": [
        "普通舒肩或短暂半蹲自理姿态，不增加疲病、受伤、康复或体能恢复设定。",
        "不舀水、不引人入院、不留宿、不认证井水、不暴露存粮、不替邻村作保、不画DT02配给结果。",
        "展开双臂不能变招手、拦路、拥抱或施法；动作以整臂轮廓而非改脸判断。",
        "半蹲要明显降髋屈膝、两掌分别贴两腿裤面，双靴平稳支撑，不跪地、不画跌倒。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/表情两手腰前相近，本张整臂左右展开；与双掌扶膝的低位半蹲在手位、支撑和轮廓上均不同。"
      }
    },
    {
      "key": "jier_A2_half_crouch_palms_on_knees",
      "title_zh": "半蹲双掌扶膝",
      "status": "planned_not_generated",
      "output_count": 1,
      "kind": "independent_full_body_noncombat_keypose",
      "evidence": [
        {
          "source_id": "jier_card",
          "locator": "体貌与随身，仅保原土迹",
          "line_start": 17,
          "quote": "指甲缝里是土"
        },
        {
          "source_id": "field_dialogue",
          "locator": "FX-FRM／知情边界",
          "line_start": 892,
          "quote": "不说自家存粮"
        }
      ],
      "art_inference": "源卡与对白只支持身份、原随身物、习惯及边界；具体托篮/扶巾/理袖/扶腰/舒肩/半蹲/托尺/拂围裙是本轮可逆美术提案，台本未记载这些动作已经发生。",
      "start_pose_description_only": "独立从母图双手在腰前、双腿站直的姿势开始。",
      "pose": "双靴分开到稳定站距，双膝明显弯曲，髋部向后下方沉为浅半蹲，躯干从髋部轻前倾。双手不再搓指，右掌平贴本人右腿膝盖上方的褐色裤面，左掌平贴本人左腿膝盖上方的褐色裤面，两手左右分开、双肘各向侧边稍开。手掌是宽面轻扶，不抓绑腿或小扣；原裤、两卷袖和双靴保持。头随躯干降低但仍朝画面左，眉眼平常，不表现疼痛或跌倒。",
      "end_pose_description_only": "双掌可离膝、两腿自然伸直回站姿；没有新增伤病或休息结算。",
      "transition_scope": "起止仅文字；只生成pose所述一帧。A1/A2无顺序依赖，不引用另一姿作为参考。",
      "visible_stage_target": "明显降髋屈双膝，双掌各自落在一条腿的膝上裤面，两手不再腰前相搓。",
      "pose_specific_sidedness": "右掌画面左贴本人右膝上裤面，左掌画面右贴本人左膝上裤面；两脚各在同侧支撑。",
      "contact_and_support_checks": [
        "双膝真实弯曲、髋位降低，不只缩短整个人或只弯脖子。",
        "两掌各贴一腿裤面，手腿之间接触清楚，原绑腿和鞋完整。",
        "双靴全掌着地、重心在两脚间，不跪、不坐地、不加座具。"
      ],
      "prop_state_and_retention": [
        "没有手持物，不添加工具、桶碗、粮袋或家具。母图两只袖口继续卷在原高度，米麻袖缘、腰带和双靴保留；指端原少量土迹仍是土，不改成血、不宣称洗净。灰发灰须与真实五十来岁脸保持；双手按本张动作移动。"
      ],
      "difference_from_mother_expression_and_batch": "母图/旧表情为直立腰前搓指，本张双膝弯曲、双掌低到两腿；不是谈井或谢客的表情变体。",
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
        "Assets/CharacterDesigns/20261013/expressive/new_story/jier/concept_v1/jier_transparent.png"
      ],
      "reference_sha256": [
        "47c591b61400237112425f97f213b3663531eae495465c37bc067fbf1290d239"
      ],
      "prompt": "以所附本人的已审透明全身母图为唯一身份、年龄、实际体态比例、衣装配色与原物件造型锚，绘制一张独立、普通日常的全身基础动作像素概念。延续母图真实年龄与紧凑身体、自然短颈、本人五官和有组织的粗像素簇；不幼化、不拉成长身、不统一套用头身数字。禁止镜像，左右均按人物自身解剖侧并核对注明的画面侧。必须真实改变下述肢体和接触，不能只改眉眼或头姿。完整头发、双手、双脚及全部原物件，四周保留透明余量。一人、一个瞬间、纯alpha透明背景，无地板、地面投影、光晕、烟雾、文字、UI、箭头、边框、残影或第二人。不新增环境、工具、战斗、魔法或剧情结果。只画本张动作，不画起止或连续帧。\n人物：蓟珥 FX-FRM。五十来岁的农宅男性住户，母图灰棕短发、灰须、宽额与方实成熟脸，脸朝画面左。旧灰蓝粗衫、米麻领边与两只原卷袖、棕腰带、褐裤和深棕绑腿鞋靴完整保留。\n固定衣装与原物件：没有手持物，不添加工具、桶碗、粮袋或家具。母图两只袖口继续卷在原高度，米麻袖缘、腰带和双靴保留；指端原少量土迹仍是土，不改成血、不宣称洗净。灰发灰须与真实五十来岁脸保持；双手按本张动作移动。\n本张动作：半蹲双掌扶膝。双靴分开到稳定站距，双膝明显弯曲，髋部向后下方沉为浅半蹲，躯干从髋部轻前倾。双手不再搓指，右掌平贴本人右腿膝盖上方的褐色裤面，左掌平贴本人左腿膝盖上方的褐色裤面，两手左右分开、双肘各向侧边稍开。手掌是宽面轻扶，不抓绑腿或小扣；原裤、两卷袖和双靴保持。头随躯干降低但仍朝画面左，眉眼平常，不表现疼痛或跌倒。\n本张侧别：右掌画面左贴本人右膝上裤面，左掌画面右贴本人左膝上裤面；两脚各在同侧支撑。\n必须明显可见：明显降髋屈双膝，双掌各自落在一条腿的膝上裤面，两手不再腰前相搓。\n接触与支撑：双膝真实弯曲、髋位降低，不只缩短整个人或只弯脖子。；两掌各贴一腿裤面，手腿之间接触清楚，原绑腿和鞋完整。；双靴全掌着地、重心在两脚间，不跪、不坐地、不加座具。。\n",
      "prompt_sha256": "fa2ca095f23b1db5c2beb384a9f49960238fda57c8c4bdc54a5c1f5adfed4f7c",
      "prompt_file": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/jier_A2_half_crouch_palms_on_knees_prompt.txt",
      "negative_constraints": [
        "普通舒肩或短暂半蹲自理姿态，不增加疲病、受伤、康复或体能恢复设定。",
        "不舀水、不引人入院、不留宿、不认证井水、不暴露存粮、不替邻村作保、不画DT02配给结果。",
        "展开双臂不能变招手、拦路、拥抱或施法；动作以整臂轮廓而非改脸判断。",
        "半蹲要明显降髋屈膝、两掌分别贴两腿裤面，双靴平稳支撑，不跪地、不画跌倒。"
      ],
      "existing_asset_check": {
        "own_action_directory_count": 0,
        "prior_action_found": false,
        "expression_board_actually_viewed": true,
        "scan": "Assets/CharacterDesigns/20261013/expressive/new_story_audit/tenth_new_character_actions_sources/action_tree_scan.json",
        "semantic_comparison": "母图/旧表情为直立腰前搓指，本张双膝弯曲、双掌低到两腿；不是谈井或谢客的表情变体。"
      }
    }
  ]
}

只按本姿独立prompt调用。母图实比，不套数字。每姿1首稿，最多1次真硬错修订，安全block停止；内置imagegen负责人物，脚本只alpha≤8与隐藏RGB清理、整图nearest等比排版；保全返回payload与所有尝试。不动画、不游戏落地、不Git、不上传。
