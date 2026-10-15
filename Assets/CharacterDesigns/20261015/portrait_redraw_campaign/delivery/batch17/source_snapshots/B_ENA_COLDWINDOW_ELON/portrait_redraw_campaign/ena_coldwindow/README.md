# 艾娜 · MAE-S03-NPC · batch17

当前候选：`candidates/portrait_v2_74x100_candidate.png`
SHA-256：`50c39a2e4ba0bc8a42fff4b2804b2635496e26fa7fc9f44d0ecd872acc6000ad`

v2 保留冷窗驿 MAE-S03-NPC 三十多岁女性、棕低髻与芥黄/深绿衣色。短卷收整，颈比初稿更短，鼻翼颧骨有成面硬块，成年卵圆脸清楚。

冷窗艾娜 MAE-S03-NPC，不是灰堤/主线 NPC-N-ENA。无围裙持外套等另一艾娜线索。

## 查看

- `previews/portrait_v2_1x.png`：准确1×透明目标
- `previews/portrait_v2_8x.png`：整数8× nearest-neighbor
- `previews/portrait_v2_1x_8x.png`：暗/中灰/浅底1×、8×和四核心风格对照
- `raw/portrait_v1_raw_imagegen.png`、`raw/portrait_v2_raw_imagegen.png`：内置 imagegen 原始返回，保留未缩放图

## 方法与复现

内置 imagegen 真实重绘，初稿+一次集中修订，共2张。完整调用参数和提示词在 `prompts/portrait_v1.json`、`prompts/portrait_v2.json`；完整 tool return 含原图 data URL，存于同名 `tool_returns/`。

执行：`python derive_portrait.py portrait_v2`。Pillow 使用全画布等比 contain 到72×98内框，居中于74×100；仅 NEAREST，无裁切/局部几何修饰；alpha 128阈值二值化；可见采样色 MEDIANCUT ≤32色、无抖动。整数栅格尺寸的round已记录于metrics。不得称作原生74×100手工像素。

## 来源与验收

当前卡、精确母版、旧选版QA、旧manifest、四核心参考与关联台本快照均在 `sources/`。来源及hash见 `sources/source_manifest.json`；制作后逐项重核为13项原文件和快照未变。

技术结果见 `qa/portrait_v2_metrics.json`；作者视觉记录及未完全解决的细节见 `qa/author_visual_QA.json`；独立QA已通过视觉与逐字节复现，接受v2为有细节备注的候选；报告为 `../independent_qa/batch17/v2_visual_reviews.json` 和 `../independent_qa/batch17/final_technical_audit.json`。

本目录为未接入游戏的候选；旧图、人物卡和代码未改，不commit/push。
