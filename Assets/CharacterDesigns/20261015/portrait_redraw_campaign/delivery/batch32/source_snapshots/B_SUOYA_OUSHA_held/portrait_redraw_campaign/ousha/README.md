# 欧莎 2026-10-15 肖像重绘

本轮 held，不设选稿、不计可交付。full v2 仅作审阅证据：大亮眼白、卡通眼型和细长裸颈仍未达到四核心要求；inset不能解决这些问题。

- 版本：初稿 v1 与唯一一次 v2 修订；不再第三次生图。
- 审阅证据：candidates/portrait_v2_74x100_candidate.png
- SHA256：80cdadb272f181747fb6eca76f24e46d79c2f88bd74fabdf47b21188052c7251
- 原始生成：raw/；完整实际prompt参数：prompts/；完整工具回包：tool_returns/
- 1x 与整数放大/三背景预览：previews/
- 来源与哈希：sources/source_manifest.json；独立评审确认：qa/independent_review_acceptance.json
- 内置imagegen实质重绘后，全图等比NEAREST contain、≤32色量化和二值alpha仅技术派生，不是原生逐像素终稿；runtime未集成未验证。
- inset仅技术余量对照，不是另一次重绘，也不能修复源图裁切或核心风格。
- 可复现：python derive_portrait.py portrait_v2
- 重建清单：python finalize_manifest.py portrait_v2 held_after_single_revision
- 重算导出逐文件哈希一致，见qa/reproduction_check.json。旧资产、卡、代码与全局索引未改；未commit/push。
