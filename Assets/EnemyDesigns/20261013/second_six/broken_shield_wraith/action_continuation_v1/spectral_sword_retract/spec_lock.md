# 本轮关键姿态执行锁定

{
  "concept_id": "EAO-CONCEPT-ENEMY-010",
  "identity_lock": {
    "face_body": "冷蓝灰面腔和清楚颧鼻、暗眼窝，破盔低顶；宽肩倒梯形幽体，不变暖肉或命名死者肖像。",
    "clothing": "同色冷蓝灰盔、肩甲、胸前碎布与层叠袍；腰下两条短钝碎尾，中间透空，绝无靴足、腿部承重或拖地长袍。",
    "props_grip": "画面右持一面大缺口窄长尖底盾影，原大缺口在盾外上侧，裂面保留组织；另一侧一把短直剑，剑身护手柄与拳连续。盾后前臂接合可解释，不把盾当第三臂。",
    "scale_lock": "长盾近于肩至短尾末端的大体量，剑为单手直剑且比盾短；不缩成007圆盾、不把剑变长枪。双尾锁选定v2短长度级别，尾碎簇可自然变化。"
  },
  "pose_mechanics": {
    "line_of_action": "脸仍朝左三分之四；胸廓从前探转为小幅向右后收，肩与腰关系改变而不是整图位移。",
    "arms_and_grips": "原画面左剑臂肘折回身旁，剑拳回到左侧胸肋，短直剑由拳指向左上外空，与脸留缝；原右盾臂保持盾背连接，长盾仍护近侧胸腹。剑柄、拳、护手、剑身链连续。",
    "support_and_contacts": "无脚、无地面接触。两条短钝分叉尾由同一个腰下幽体相连，尾端可轻向左滞留而胸肩向右收；保持选中母图的短尾级别及中间透空，不画长飘带、第三尾或实体落地腿。",
    "negative_space": "回收剑仍在身体左外侧，斜上剑身不得穿过脸/盔/盾；盾的外上缺口和尖底保持可辨。",
    "readability_priority": "折肘、举剑回收、胸廓后收共同读阶段；尾的轻偏只辅助，不以加光雾或大幅尾旋转制造动作。"
  },
  "pass_conditions": [
    "可见probe伸肘到新稿折肘的明确功能变化，剑从平探转为胸侧斜上回收。",
    "冷色成熟面腔、破盔肩甲、同一缺口长盾及短直剑一致；两短尾自然接腰且无落地足。",
    "真实alpha浅深底合成可读；透明像素的隐藏RGB不作为可见光晕证据。"
  ],
  "hard_fail_conditions": [
    "仍画低剑guard，或只将probe整体平移，回收核心不存在。",
    "回收剑穿脸/盾、变长剑或掉握；增脚或第三尾、两尾变扫地长袍。"
  ],
  "format": "Native RGBA; entire subject and props fit with margin; canvas follows pose. No fixed runtime grid.",
  "processing": "Only alpha cleanup if visibly justified, and nearest-neighbor uniform display scaling. No body painting or stretching.",
  "budget": "One first draft; at most one documented hard-error revision.",
  "claims": "Independent keypose concept; animation anchors, exact palette, equipment integration and runtime unverified."
}
