# 缄声执铃者 / bell_outward_swing

{
  "identity_lock": {
    "face_body": "新锚低炭灰圆帽、额际短棕卷发、成熟方窄颌与浓眉长鼻、闭嘴侧眼；头较大而胸腹腿紧凑，仍是成年脸。不得回退旧012约7头身修长自然主义，也不幼化；近似风格对齐而非精确1:1.5。",
    "clothing": "炭灰圆领宽袖膝袍、浅领口，污白斜肩带由画面左肩至右腰结/短穗，棕皮带方扣、短棕裤与双旧靴；保留新锚简洁大块衣褶，避免细密布料噪点。",
    "props_grip": "原画面左手持一只暗铜铃，木柄/握拳/钟肩/钟口内单铃舌连续；另一手在胸腹斜带附近，可自然移位但不新增书卷。",
    "scale_lock": "铜钟体约半前臂长度级别、完整柄使总长增加；保持小手铃，不缩成挂坠或变大香炉/链球。钟口向下或自然小倾，不以复制第二铃表达摇动。 尺度只对新idle_style_v2身体归一化，不沿用旧idle_v1长身作比例标准。",
    "style_lock": "沿新锚粗簇、成熟大头短身与有限明暗色阶，和007/008相邻观看时应属于同系列；不强迫所有成人完全同一模板。"
  },
  "pose_mechanics": {
    "line_of_action": "胸廓稍向持铃侧转，左前脚接重、另一脚后稳，肩线跟随外摆但头仍朝左三分之四。",
    "arms_and_grips": "原画面左手继续包握同一木柄，肩肘向外展开，手位于身体左侧、胸腹之间；肘比raise明显展开但不锁死。铃柄与手腕同向自然斜转，钟体在手的左下外侧，钟口斜下，原单铃舌可自然偏而不增殖。空手在右胸腹斜带附近，不触铃。",
    "support_and_contacts": "画面左前靴整底落地、膝微屈接住侧前重量；右后靴同样稳触平面，站距略开而非settle收步。不需要跨步夸张扭腰或双脚腾空。",
    "negative_space": "持铃手腕必须从袖口连续伸出，铃与袍、脸、膝有清楚空隙，完整木柄和钟体同一轴系，不将手铃改为链坠。",
    "readability_priority": "外展的肩肘链、斜下钟体和前脚接重一起读成外摆端点；单独改变铃口几个像素或微表情不算新动作。"
  },
  "pass_conditions": [
    "与raise弯肘高提、settle低垂收铃形成第三种明确外伸姿，整个手臂与铃的轮廓在缩小后仍可读。",
    "袖口—腕—握拳—木柄—钟肩连续，单手小铃体量不漂移；另一手保持空手。",
    "沿idle_style_v2大头短身与成熟五官，不回退旧长身；低帽、污白左肩至右腰斜带和双靴一致。"
  ],
  "hard_fail_conditions": [
    "重画高提或低收，只换眼神/铃口倾角；外摆没有肩肘与承重变化。",
    "铃改手/脱柄/增加链条、复制第二铃或铃舌，或袖口断腕，钟体粘脸腿。"
  ],
  "palette": "沿本次三张锁定参考；不新定色板",
  "canvas": "按主体完整性自然画幅，原生透明，概念PNG，无精确像素规格保证",
  "budget": "1 first draft + max 1 independently documented hard-error revision",
  "scope": "New key-stage concept; no continuous animation, anchor, equipment or runtime verification",
  "review_gate": "Independent planning gate passed by review_second_enemy_continuations 2026-10-14T04:20Z. 011双趾按双足解释，不改母图爪趾拓扑。"
}
