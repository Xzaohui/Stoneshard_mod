# Spec lock: EAO-CONCEPT-ENEMY-007 / axe_forward_cut

Existing approved style continuation. New key-stage concept only. One first draft and at most one documented hard-error revision.

face_body: 浓眉、棕乱短发、近侧灰鬓和完整灰黑短胡、宽颧方颌暖肤成年男性；紧凑结实体格，不改幼脸或修长身。
clothing: 旧蓝灰短肩巾、灰褐菱格绗缝背心、米灰卷袖；画面右肩单铁肩甲，暗皮腰带方扣、褐裤、米色绑腿与双褐靴。
props_grip: 画面右侧盾臂支撑一面木圆盾，另一侧手持短单刃斧；圆盾竖木板、深边框、中央铁脐，斧为普通短柄铁头。盾背接臂可遮挡但不可悬空，斧刃不穿盾腿。
scale_lock: 盾直径约覆盖胸下至大腿上部的体量，不能膨成长盾；短斧明显短于躯干加腿的身体长度，保持单手短斧级别和原斧头/柄比例。

{
  "line_of_action": "面向画面左的轻三分之四保持，胸肩向左前转送，髋随之偏向前脚，头仍可见；不是只把斧贴图旋转。",
  "arms_and_grips": "延续画面左斧臂、右盾臂。斧手前送至胸下外前，肘展开但不锁死；短柄由拳斜向左下，斧头降到腰腹高度的空处，握拳后仍见短柄尾。盾收在近侧胸肋，前臂与盾背联系能解释。",
  "support_and_contacts": "画面左靴为前承重点，整底落在同一想象支撑平面，左膝屈向脚尖；右靴留后方，前掌至脚跟自然支撑形成宽基底。胸髋的前送由腿承接，不前倾到必然扑倒。武器、盾均不撑地。",
  "negative_space": "斧手和斧头在盾外左侧，斧刃不切进前腿；斧臂与身体形成明确前送空隙。脸在盾顶之上。",
  "readability_priority": "前送的肩肘链、前脚承重和向下斜切的短斧共同读成一阶段；不要求某一个像素坐标或盾脐点严格对齐。"
}

Canvas: native imagegen canvas, transparent RGBA; preserve full subject and props with margin. Do not rescale body or add runtime grid. Palette: inherit own selected mother muted brown/grey/blue-grey pixel clusters; no new palette quantization. Direction: left three-quarter. Count: one. Platform: original art concept for existing Stoneshard mod, not runtime integrated.
