# 埃墨·衬 / ALD-NPC-EMO：头像重绘候选

选择 portrait_v2_maxcoverage，SHA256：b1e73ec1f7fe10a842f0772a9c7d2d5e61fd0ae2b4506c51641a44a6786c1849。

- 最终候选：candidates/portrait_v2_maxcoverage_74x100_candidate.png
- 1×＋8×近邻预览及四核心风格对照：previews/portrait_v2_maxcoverage_1x_8x.png
- 身份、现卡及历史母版/QA快照：sources/source_manifest.json、spec_lock.md
- 完整生图prompt/工具参数：prompts/portrait_v1.json、prompts/portrait_v2.json
- 完整tool return含原始图payload：tool_returns/portrait_v1.json、tool_returns/portrait_v2.json
- 原图：raw/portrait_v1_raw_imagegen.png、raw/portrait_v2_raw_imagegen.png
- 复现：运行 python derive_portrait.py portrait_v2_maxcoverage

使用built-in image_gen实际重绘。v1后按自检与独立QA只作一次必要v2修订，缩短颈、加大脸、平稳眉嘴。最终为同一v2原图的等比例全画布NEAREST缩小，置入74×100透明画布，alpha≥128二值化，再MAXCOVERAGE≤32临时色无抖动量化。没有局部描改、补眼、拼接或拉伸；保留MEDIANCUT对照版本。

本稿为衍生候选，不是原生像素手绘终稿，不是用户审美认可或运行集成验收。眼白仍约2px，记录为候选备注；蓝灰领口保留但极窄。旧图、人物卡、代码未改，未commit/push。
