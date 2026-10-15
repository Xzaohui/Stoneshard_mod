# 朔娅 2026-10-15 肖像重绘

选 full v2 带限制候选。面部下半与短颈窄领改善，成熟风雪纹及左眉缺口保留。源左右13/11像素余量偏紧但主体未真裁断；不选inset。

- 版本：初稿 v1 与唯一一次 v2 修订；不再第三次生图。
- 选中候选：candidates/portrait_v2_74x100_candidate.png
- SHA256：5e73bc68655674b727afb39acdfa107bab7ecf92dc3c03fe69c954b106444437
- 原始生成：raw/；完整实际prompt参数：prompts/；完整工具回包：tool_returns/
- 1x 与整数放大/三背景预览：previews/
- 来源与哈希：sources/source_manifest.json；独立评审确认：qa/independent_review_acceptance.json
- 内置imagegen实质重绘后，全图等比NEAREST contain、≤32色量化和二值alpha仅技术派生，不是原生逐像素终稿；runtime未集成未验证。
- inset仅技术余量对照，不是另一次重绘，也不能修复源图裁切或核心风格。
- 可复现：python derive_portrait.py portrait_v2
- 重建清单：python finalize_manifest.py portrait_v2 selected_candidate_with_limitations
- 重算导出逐文件哈希一致，见qa/reproduction_check.json。旧资产、卡、代码与全局索引未改；未commit/push。
