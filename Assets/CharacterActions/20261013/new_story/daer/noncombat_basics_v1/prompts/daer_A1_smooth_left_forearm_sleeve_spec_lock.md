# 当前独立动作制作锁

{
  "character": "daer",
  "action": "daer_A1_smooth_left_forearm_sleeve",
  "label": "右掌抚平左前臂衣袖",
  "plan_gate_sha256": "d2c24d875355099356262e218e7a4cf8bc31b14b23131b8e3388b91aa505e917",
  "brief_sha256": "fd6e809c1ef8c7ccaad648b88542a8c87827d169f4380262c0d8fb32542af7ec",
  "reference": [
    "Assets/CharacterDesigns/20261013/expressive/new_story/daer/concept_v1/daer_transparent.png"
  ],
  "reference_sha256": [
    "8852643e1b657bc1bc36704bfb8a955579e8a4f494872ca097d0a14f856b1b93"
  ],
  "prompt_sha256": "8ee894d9c65ea56e32a319a1c7c767c763ec64b0d8699ae50c0dee2aa0fe91fa",
  "canvas": "imagegen native output preserved; no forced fixed grid",
  "palette": "unchanged own mother palette; no quantization",
  "pose": "双脚平稳分站。左肘向画面右稍外开，左前臂在身体前方接近水平伸出，手掌自然朝下，和胸口之间留出清楚间隙。右手从原搓手位置分开，右前臂斜穿腹前，右掌平贴左前臂外侧灰绿袖面，停在由肘下向腕部顺布的一瞬；接触点在扎紧袖口上方的一大片布面，不在细绳结。两手彼此分开，不扣掌。原两边袖口扎带仍完整扎好；原空袋继续瘪薄挂画面右腰后。脸朝画面左，目光轻落在袖面。",
  "fixed_props": [
    "同一只瘪薄灰麻空袋始终挂人物左侧（画面右腰后），原棕肩带由人物左肩（画面右）连接，不鼓胀、不移到对侧。两侧原袖口扎带都保持扎紧，数量和材质不变。左右手仅按本张独立手位。"
  ],
  "checks": [
    "掌对布面形成宽接触，不能两掌重新扣在一起。",
    "接触位置不覆盖、解开或重打袖口细结。",
    "空袋仍同侧瘪薄，双靴完整着地。"
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
