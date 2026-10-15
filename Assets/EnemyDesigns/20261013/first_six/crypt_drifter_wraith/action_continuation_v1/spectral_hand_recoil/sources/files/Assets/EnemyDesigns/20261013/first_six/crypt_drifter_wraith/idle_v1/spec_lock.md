# Static concept execution contract
{
  "concept_id": "EAO-CONCEPT-ENEMY-004",
  "category": "幽灵",
  "working_name": "墓龛游魂",
  "name_status": "可逆美术工作名，非新增剧情角色或原版兵种名",
  "status": "brief_ready_generation_not_started",
  "output_directory": "Assets/EnemyDesigns/20261013/first_six/crypt_drifter_wraith/idle_v1/",
  "planned_raw_image": "Assets/EnemyDesigns/20261013/first_six/crypt_drifter_wraith/idle_v1/crypt_drifter_wraith_idle_raw_imagegen.png",
  "reference_ids": [
    "R05"
  ],
  "project_source_keys": [
    "D09",
    "BRY14"
  ],
  "vanilla_evidence": [
    "R05官方Wraith陈列保留兜帽/武器职业形、暗眼窝与冷青碎尾，无落地靴；图不证明运行时alpha实现。"
  ],
  "existing_project_canon": [
    "D09回声仅有来源的感知干扰，无死者明确签名；CS-BRY-14禁止把弟弟幽灵搬进场景。"
  ],
  "original_proposal": {
    "silhouette": "窄上宽下的破伞形罩袍；肩线几乎水平、头略埋；下半身分两长一短的碎烟尾，尾端之间留透明缺口，完全不露实脚。",
    "palette": {
      "base": [
        "深灰青",
        "黯蓝绿"
      ],
      "secondary": [
        "灰冷青"
      ],
      "accent": "仅额边与手背用浅青小簇提亮，不做白色全身光晕"
    },
    "clothing_and_surface_layers": [
      "朽旧兜帽与短肩披仍有布料折角；胸部暗层向下渐碎成硬边烟尾；用大块像素簇表达消散，不用柔焦雾球"
    ],
    "props": [
      "不持武器，单只骨感手从披衣伸出；无钥匙、签名书、灵魂锁链或墓主信物"
    ],
    "face_and_emotion": "深暗眼窝与窄颅面残影，眉鼻结构只留简化冷色棱面；空茫、无直视式卖萌，无可识别死者脸。",
    "static_idle_pose": "轻三分之四朝画面左，双肩安静，伸手只比腰稍高；漂浮下缘完整，透明背景不带墓地/大烟雾/阴影地板。",
    "future_action_direction_not_in_this_delivery": [
      "后续微幅上下漂移、手伸展、尾部离散与重聚；本轮不承诺透明渲染、穿墙或召唤能力"
    ]
  },
  "must_not_infer_or_draw": [
    "不把D09回声视为真魂",
    "不画CS-BRY-14弟弟或任何既有死者面貌",
    "不发出证明事实的文字或遗言"
  ],
  "unresolved_reversible_choices": [
    "具体出现地点、历史、与回声关系均未定",
    "冷青色阶与尾形为可逆概念，不预设魔法机制"
  ],
  "runtimeIntegrated": false,
  "runtimeVerified": false
}
Builtin imagegen; transparent_background=true; 1 static full-body original concept. Large organized hard pixel clusters. No fixed runtime dimensions, palette or animation promise. Retain raw. Cleanup only alpha<=8 and hidden RGB; proportional nearest-neighbor presentation only. Preserve wraith intentional partial alpha. First draft plus at most one hard-error revision.
