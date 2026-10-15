# Static concept execution contract
{
  "concept_id": "EAO-CONCEPT-ENEMY-003",
  "category": "僵尸",
  "working_name": "渠墓腐尸",
  "name_status": "可逆美术工作名，非新增剧情角色或原版兵种名",
  "status": "brief_ready_generation_not_started",
  "output_directory": "Assets/EnemyDesigns/20261013/first_six/canal_tomb_restless/idle_v1/",
  "planned_raw_image": "Assets/EnemyDesigns/20261013/first_six/canal_tomb_restless/idle_v1/canal_tomb_restless_idle_raw_imagegen.png",
  "reference_ids": [
    "R03",
    "R04"
  ],
  "project_source_keys": [
    "D02",
    "D07"
  ],
  "vanilla_evidence": [
    "R03官方Restless保留肉体并有塌肩伸臂；R04为混合亡灵陈列图，不可整图叫僵尸。"
  ],
  "existing_project_canon": [
    "D02亡者仅在明确墓龛战区；D07普通病人默认非敌对，不能由病态皮肤直接推成僵尸。"
  ],
  "original_proposal": {
    "silhouette": "扭曲斜C形、左肩下坠、头偏一侧；仍可读成人骨架但双臂不等高；拖后脚与弯膝形成非对称站姿。不是骷髅的轻细骨架。",
    "palette": {
      "base": [
        "灰橄榄死皮",
        "湿土褐"
      ],
      "secondary": [
        "旧麻灰",
        "黑褐阴影"
      ],
      "accent": "少量干暗红破损，不用鲜红喷血"
    },
    "clothing_and_surface_layers": [
      "保留大面积干瘪皮肉与小块斑驳组织；无袖残工作罩衣→破下摆→泥污绑腿；腐朽集中脸颊、前臂、袖边，不把全身画成白骨"
    ],
    "props": [
      "空手，不拿新武器；腰侧一小段断麻绳仅作旧衣物残留，无病人腕牌、护理器具"
    ],
    "face_and_emotion": "塌陷一侧脸颊、暗眼窝、松垂下颌、灰色薄唇；无漂亮红唇、大睫毛、温柔眉眼。面部迟钝空茫，腐朽不是人类微笑。",
    "static_idle_pose": "略偏三分之四，前脚平落、后脚拖步但仍与地面接触；一臂低垂另一臂稍抬，手指屈曲；单幅静止，无扑咬对象。",
    "future_action_direction_not_in_this_delivery": [
      "后续肩胯不同步拖步、慢速伸抓、受击塌肩、倒地；复活机制待后续实现核验"
    ]
  },
  "must_not_infer_or_draw": [
    "不复制D07病人或既有NPC面貌",
    "不画干净白骨骷髅",
    "不加临终剧情、身份揭示或已死NPC姓名"
  ],
  "unresolved_reversible_choices": [
    "来源与生前身份未定，暂不落具体墓主",
    "肤色与破衣样式可逆；不预设毒、传染或复活能力"
  ],
  "runtimeIntegrated": false,
  "runtimeVerified": false
}
Builtin imagegen; transparent_background=true; 1 static full-body original concept. Large organized hard pixel clusters. No fixed runtime dimensions, palette or animation promise. Retain raw. Cleanup only alpha<=8 and hidden RGB; proportional nearest-neighbor presentation only. Preserve wraith intentional partial alpha. First draft plus at most one hard-error revision.
