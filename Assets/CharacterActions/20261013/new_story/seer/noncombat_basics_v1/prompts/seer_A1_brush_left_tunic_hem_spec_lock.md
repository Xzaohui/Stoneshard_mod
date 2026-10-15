# 当前独立动作制作锁

{
  "character": "seer",
  "action": "seer_A1_brush_left_tunic_hem",
  "label": "左手拂平左侧衣摆",
  "plan_gate_sha256": "d2c24d875355099356262e218e7a4cf8bc31b14b23131b8e3388b91aa505e917",
  "brief_sha256": "fd6e809c1ef8c7ccaad648b88542a8c87827d169f4380262c0d8fb32542af7ec",
  "reference": [
    "Assets/CharacterDesigns/20261013/expressive/new_story/seer/concept_v1/seer_transparent.png"
  ],
  "reference_sha256": [
    "b238b55b901eea014c66ba081c248f3c909b62c00f3d61a148b7921e71e154d3"
  ],
  "prompt_sha256": "b5413f2749d37dc7a72c5b60d9a7849b453450a48a2f4733309c34fa9893d25e",
  "canvas": "imagegen native output preserved; no forced fixed grid",
  "palette": "unchanged own mother palette; no quantization",
  "pose": "双靴分开平稳落地，身体轻向自己的左侧（画面右）侧倾。左臂从原胸腹外侧落下，左掌并拢平贴自己左侧大腿前的灰麻褂下摆，停在向下拂平布面的中段；左肘低垂，手掌与大面积衣面有清楚接触，衣边轻折但灰斑仍保留。右手继续在画面左腰旁握住原绳，绳的两端松垂。头保持朝画面左，仅微低，不改变基础脸型或情绪。",
  "fixed_props": [
    "人物右手（画面左）始终在右腰旁握住母图同一截浅色断绳，绳仍松垂且原两端完整，不展开、不抬绳、不换手。灰斑、衣带、翻袖和双靴保留。左手只按本张动作改变。"
  ],
  "checks": [
    "左掌与衣面广面接触，不是贴近但悬空。",
    "双脚全掌着地，侧倾仍在两脚支撑之间。",
    "绳无新结、无拉紧或微小尾端接点要求。"
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
