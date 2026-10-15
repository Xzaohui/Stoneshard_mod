# 多恩 肖像重绘候选

状态：awaiting_independent_qa。两张成功image_gen及技术导出已经完成，等待batch39独立QA最终分级；当前选图仅为待审候选。

当前候选：candidates/portrait_v2_inset_74x100_candidate.png。

眼白及长颈较初稿已压低，但忧眉、灰须细碎仍有保留。源轮廓完整，等比inset仅改善最终画布余量。

每人一次初稿加一次集中反馈后的修订，已达到两张成功图上限，不再新生图。Don曾有一次6引用即时参数拒绝，无图片生成，错误与原始参数单独保留。

使用内置image_gen实质重绘。完整prompt实参、完整回包、逐字节raw、源卡/母图/母QA/剧情与四核心参考的快照和SHA均已保存。最新卡帽/头巾更新优先于旧母图；身份、年龄和衣色保持。

74×100、32色临时预算、二值alpha及NEAREST等比containment仅技术派生，非原生逐像素终稿。未接入运行、未实机验收，旧图/人物卡/代码/冻结索引未修改。

复现技术导出：python derive_portrait.py portrait_v2 inset；python finalize_manifest.py portrait_v2_inset awaiting_independent_qa。qa/reproduction_check.json记录全部候选逐字节复现一致。图像生成本身是随机过程，完整参数及回包用于审计，不声称可重新生成相同图。
