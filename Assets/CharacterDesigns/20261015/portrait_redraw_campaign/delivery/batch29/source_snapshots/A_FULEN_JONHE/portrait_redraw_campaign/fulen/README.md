# fulen 肖像重绘候选

选用：`candidates/portrait_v2_inset_74x100_candidate.png`

SHA-256：`b6e1a7a2ccf76396953d4434fd9f412324b093c558e15b168660faec7c0bef38`

状态：selected_candidate_with_limitations。芙伦：米白头巾、小后结、耳后短发、三十多岁宽颧长鼻、护理素褂与厚围裙窄上缘。眼白缩暗、颈领压缩；原图左侧真实余量偏小，无发丝实际裁断。inset仅改善74×100目标采样触边，不冒充补回内容。

已完成初稿1次+集中QA后唯一修订1次；共2/2次实质 built-in image_gen，不再第三次。完整实际实参在 `prompts/portrait_v1.json` 和 `portrait_v2.json`，全文提示词在同名 `.txt`；完整含图回包在 `tool_returns/`；原始PNG在 `raw/`，与相应回包base64解码逐字节一致。母图、当前卡、母QA、母manifest、四核心及剧情快照与源SHA在 `sources/`。

复现：`python derive_portrait.py portrait_v2 inset`；然后 `python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`。仅整画布等比NEAREST、alpha阈值128与MAXCOVERAGE无抖动≤32临时色；不裁剪、不几何重绘、不脚本绘脸。`previews/`提供1×、整数8×和三背景整数4×预览。

这是技术派生候选，不是原生逐像素终稿、装备兼容或游戏运行验收。独立复核记录见 `qa/independent_review_acceptance.json`，作者限制见 `qa/author_visual_review.json`，源边界实测在 `qa/portrait_v2_source_edges.json`。旧图、角色卡、代码及冻结索引未改；未commit/push。
