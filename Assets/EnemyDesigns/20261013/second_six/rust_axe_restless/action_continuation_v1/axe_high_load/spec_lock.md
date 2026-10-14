# 本轮关键姿态执行锁定

{
  "concept_id": "EAO-CONCEPT-ENEMY-009",
  "identity_lock": {
    "face_body": "新锚粗簇灰蜡肉脸、深眼窝、松张口与浅黄齿、露耳颈，锈裂盔仍有大缺损；塌肩前倾、缩短胸腹的紧凑亡卒。肉脸和肉腿仍清楚，不退回旧高频写实噪纹或换纯骷髅。",
    "clothing": "新锚大块锈褐/铁灰裂甲、画面左叠片肩护、画面右破赭布露肩；旧皮带与粗簇碎布裙、护腕膝片、裹踝残靴和露趾实体足。少量原有暗伤痕保留，不加新血。",
    "props_grip": "一柄巨大锈铁单侧宽刃长柄斧，斧头缺损/小凹口、长木杆和尾端金属箍；两手握住同一连续柄段，腕掌可信。原图画面左手靠头端，画面右手靠尾端，按自然持斧延续不另立H1前后规则。",
    "scale_lock": "长斧横跨躯干并伸出两侧，斧头为明显宽重级别；不缩成007单手斧或增加双刃。完整斧头及柄尾留边，可扩画布。 尺度只对新idle_style_v2身体归一化，不沿用旧idle_v1长身作比例标准。",
    "style_lock": "低魔中世纪组织性大块像素簇、硬边有限色阶，锈斑为稀疏成组块面；沿新锚紧凑体块，动作变化不恢复旧长腹或细密自然主义。"
  },
  "pose_mechanics": {
    "line_of_action": "保留亡卒塌肩和紧凑胸腹，胸廓微转、髋回到后脚上方；抬臂不变成活人士兵挺胸军姿或拉长腰身。",
    "arms_and_grips": "沿原图画面左侧近头端手、右侧近柄尾手的分工；双手均提高，近头端手至额侧上方，后手至上胸侧，双肘共同举起支撑。长柄从左上斧头连到右下柄尾，双拳分开且腕向可解释；允许自然握距小调，不颠倒承载顺序。",
    "support_and_contacts": "画面右后足整底承载更多，右膝屈、髋在两足基底之内；左前残靴/露趾足仍接触平面做平衡。两足分开，重斧不以头盔或肩甲硬托，不能单手悬举。",
    "prop_path": "整个斧头高于盔顶且偏左外空，宽刃、长柄和尾箍仍同一尺寸级别；柄不穿脸，斧头不靠裁切显示高度。",
    "readability_priority": "高斧、大幅双肘上提、后脚接重形成统一的蓄势；斧高于盔是易读证据，不以一个像素高度差替代动作。"
  },
  "pass_conditions": [
    "与axe_set并排能明确看见双手上提和重斧过盔高位，而非沿旧肩外姿微调。",
    "两手一柄、腕肘肩承载闭合，后脚支撑成立，完整斧刃与尾箍留边。",
    "保留idle_style_v2粗簇紧凑肉体和缺损甲，绝不回退旧idle_v1的长腹密纹。"
  ],
  "hard_fail_conditions": [
    "一手离柄、柄折断/穿头、斧头缩成007短斧，或两臂不可能承载高位。",
    "只提高斧头贴图、手臂/重心基本照抄axe_set，或者以裁切掩盖斧头与柄尾。"
  ],
  "format": "Native RGBA; entire subject and props fit with margin; canvas follows pose. No fixed runtime grid.",
  "processing": "Only alpha cleanup if visibly justified, and nearest-neighbor uniform display scaling. No body painting or stretching.",
  "budget": "One first draft; at most one documented hard-error revision.",
  "claims": "Independent keypose concept; animation anchors, exact palette, equipment integration and runtime unverified."
}
