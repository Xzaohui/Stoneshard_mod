# 当前独立动作制作锁

{
  "character": "daer",
  "action": "daer_A2_grip_left_bag_strap",
  "label": "左手上提扶稳空袋背带",
  "plan_gate_sha256": "d2c24d875355099356262e218e7a4cf8bc31b14b23131b8e3388b91aa505e917",
  "brief_sha256": "fd6e809c1ef8c7ccaad648b88542a8c87827d169f4380262c0d8fb32542af7ec",
  "reference": [
    "Assets/CharacterDesigns/20261013/expressive/new_story/daer/concept_v1/daer_transparent.png"
  ],
  "reference_sha256": [
    "8852643e1b657bc1bc36704bfb8a955579e8a4f494872ca097d0a14f856b1b93"
  ],
  "prompt_sha256": "a57731ccf82d0dfd9ab10fc33235bdaa3eda50fba87a66eebf67603f8421fe52",
  "canvas": "imagegen native output preserved; no forced fixed grid",
  "palette": "unchanged own mother palette; no quantization",
  "pose": "双脚分开站稳、躯干基本直立。左肘抬到画面右胸侧，左手在自己左肩前、锁骨下握住原棕肩带，掌指绕带形成可辨的抓握，轻轻向上扶稳；肩带在手的上下两段连续，原灰麻空袋仍挂画面右腰后且保持瘪薄，只随肩带略收近身体。右臂完全离开搓手位，自然向画面左身侧下垂，右手松弛可见。脸仍朝画面左，平静看前侧。",
  "fixed_props": [
    "同一只瘪薄灰麻空袋始终挂人物左侧（画面右腰后），原棕肩带由人物左肩（画面右）连接，不鼓胀、不移到对侧。两侧原袖口扎带都保持扎紧，数量和材质不变。左右手仅按本张独立手位。"
  ],
  "checks": [
    "原肩带连续经过左掌，不凭空新增第二带。",
    "空袋保持瘪薄，不改内容、侧别或悬挂方向。",
    "右手不残留与左手相扣或按袖的状态。"
  ],
  "limits": {
    "initial": 1,
    "max_hard_error_revisions": 1,
    "revision_only_for": "真实、明确且可定位的身份、人体、原物数量/侧别、目标动作、接触支撑、比例、裁切或透明硬错。",
    "after_failed_revision": "全部尝试保留，失败标缺项；不得第三稿、脚本修人体或改动作名继续。",
    "safety_blocked": "立即停止该动作，记录tool返回；不重试、不换工具、不改写规避。"
  },
  "allowed_postprocessing": "only alpha<=8 zero and hiddenRGB cleanup; full image aspect-preserving nearest composition"
}
