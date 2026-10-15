# 缇安 / ASH-NPC-TIAN

已完成imagegen初稿与唯一一次集中反馈修订；共2次生图，停止追加。独立QA已选portrait_v2_containment，pass_with_limitations；仅技术候选冻结。

- 候选：candidates/portrait_v2_containment_74x100_candidate.png
- 查看：previews/portrait_v2_containment_1x_backgrounds.png、portrait_v2_containment_8x.png
- 全部raw、完整生成参数/提示词与完整回包分别在raw/、prompts/、tool_returns/。
- 源卡、剧情、母图、母QA、四核心参考与源SHA：sources/；更新对账在qa/source_hash_recheck.json。
- 复现：python derive_portrait.py portrait_v2 containment；python finalize_manifest.py portrait_v2_containment selected_candidate_with_limitations
- 74×100、≤32临时可见色、二值alpha；整画布等比NEAREST containment、量化只作技术派生，不冒称原生逐像素终稿。
- 两次raw和技术候选均保留；源边缘审查qa/raw_v2_edge_audit.json。轮廓没有alpha>=5触源边，技术留白没有补画被裁断的头发。缇安原始右余量仍很紧，已如实记录。
- 视觉仍有限制：发丝分割偏多、眼白偏亮、颈与脸占比未完全达核心风格，详见qa/author_visual_review.json。
- 旧资产、角色卡、代码、冻结索引保持；不commit/push，不声称游戏集成或运行验收。

冻结依据：qa/independent_review_acceptance.json；不继续第三次生成或视觉修订。
