# 当前独立动作制作锁

{
  "character": "seer",
  "action": "seer_A2_smooth_left_hair",
  "label": "抬左手轻理侧发",
  "plan_gate_sha256": "d2c24d875355099356262e218e7a4cf8bc31b14b23131b8e3388b91aa505e917",
  "brief_sha256": "fd6e809c1ef8c7ccaad648b88542a8c87827d169f4380262c0d8fb32542af7ec",
  "reference": [
    "Assets/CharacterDesigns/20261013/expressive/new_story/seer/concept_v1/seer_transparent.png"
  ],
  "reference_sha256": [
    "b238b55b901eea014c66ba081c248f3c909b62c00f3d61a148b7921e71e154d3"
  ],
  "prompt_sha256": "e83cd0bbda242cb50e53c740a09a318c516b37aa9a89f85bf15c1bb33e31a616",
  "canvas": "imagegen native output preserved; no forced fixed grid",
  "palette": "unchanged own mother palette; no quantization",
  "pose": "双靴仍平稳站立，躯干直立。左肘向画面右外抬至肩旁，左前臂向上弯，左掌和自然并拢指组轻贴自己左侧头顶外缘的原蓬发，停在顺平一小簇头发的瞬间；头发只轻微压合，原发型和发量保留。左手在头旁形成明显新轮廓，不盖眼睛、鼻子或嘴。右手在画面左腰旁照常握同一截绳，两端松垂。脸保持母图画面左朝向和原成熟特征。",
  "fixed_props": [
    "人物右手（画面左）始终在右腰旁握住母图同一截浅色断绳，绳仍松垂且原两端完整，不展开、不抬绳、不换手。灰斑、衣带、翻袖和双靴保留。左手只按本张动作改变。"
  ],
  "checks": [
    "左掌与发簇外缘接触，手不穿进头部、不遮脸。",
    "右手原绳保持完整，左手不接绳、不张指数数。",
    "双脚原位稳定，无退走或事件场景。"
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
