# 欧铎 / DEN-NPC-ODO 肖像重绘

QA27通过带注技术候选：选择 portrait_v2_inset。v2脸加大、颈缩短、灰须减量；仍有轻微眼白和粗发块。源右侧实心轮廓真实余量4像素，未证实源裁断；同raw inset只解决派生边接触，目标右余量1像素。

- 当前候选：candidates/portrait_v2_inset_74x100_candidate.png
- SHA-256：227c7a5cb993d59efa92e67ae7c99ce5e8bf4605e1219da0b63aacaaa00e46a2
- 原始图：raw/portrait_v1_raw_imagegen.png、raw/portrait_v2_raw_imagegen.png
- 每轮完整实参及回包：prompts/portrait_v*.json、tool_returns/portrait_v*.json
- 1x与整数NN、三底预览：previews/
- 卡、母图/母QA、剧情和四核心源快照及SHA：sources/
- 作者复现和独立结论：qa/

内置 image_gen 实质重绘初稿＋唯一修订，共2次，已用尽额度；不进行第三次。v1与v2原稿均完整保留。74×100、32临时可见色、二值alpha为全画布等比NEAREST＋无抖动MAXCOVERAGE派生结果，inset将完整源画布放入72×98再居中，未裁切、未脚本画脸。它不是原生逐像素终稿。

复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python derive_portrait.py portrait_v2 inset；python finalize_manifest.py portrait_v2_inset pass_candidate_with_notes。作者重跑全部候选字节一致；独立QA在批次目录另存。

旧图、角色卡、代码、冻结索引不变，无commit/push；未接入游戏与运行验证。
