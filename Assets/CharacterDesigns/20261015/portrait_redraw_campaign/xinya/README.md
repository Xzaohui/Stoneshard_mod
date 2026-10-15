# 辛娅 / PAS-S01-NPC 头像重绘

终选：candidates/portrait_v2_74x100_candidate.png。独立QA：pass_derived_candidate_with_notes。两次imagegen已用完，冻结v2。

修订：缩短裸颈、提高领口、大脸更紧凑；后梳高额、宽钝鼻、赭衣棕围裙保留。限制：神情仍稍谨慎忧虑，右眼白略亮。

1x、8x最近邻预览及三底比较见previews；完整提示词/实参见prompts；两次完整回包见tool_returns，raw逐字节匹配解码。源卡/母图/母QA/剧情/四核心与来源SHA见sources；作者及独立QA见qa；全文件清单见manifest.json和SHA256SUMS。

这是imagegen实质重绘后，整画布等比NEAREST containment、alpha阈值128与MAXCOVERAGE无抖动≤32色的技术派生。不是原生逐像素终稿，未用户单人终稿验收、未接入或实机验证。未改旧素材、卡、代码、全局索引，无commit/push。

复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python finalize_manifest.py portrait_v2 selected_candidate_with_limitations。
