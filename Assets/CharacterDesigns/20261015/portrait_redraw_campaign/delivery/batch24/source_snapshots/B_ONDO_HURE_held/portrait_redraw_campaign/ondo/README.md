# 昂朵 肖像重绘

状态：pass_concept_with_notes

昂朵v2实看通过为带限制候选，锁标准portrait_v2_74x100_candidate；短颈显著改善、~50男与衣色/领口夹、小暗眼/发耳真留边成立。残留仍拧眉偏严肃，未完全达母图平静审慎；发须仍碎块，只记录不第三次。

选用 candidates/portrait_v2_74x100_candidate.png，为带限制概念候选。

实际生成：built-in image_gen，每人v1 + 一次必要v2；完整实参在prompts/portrait_v*.json，完整prompt在同名.txt，完整返回（含原图字节data URL）在tool_returns，raw为返回解码的逐字节同一原图。工具未暴露模型/seed/quality/size控制，未伪造。

复现：在本目录运行 python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python finalize_manifest.py。前两者为确定性技术导出；复跑SHA一致见qa/reproducibility.json。不能承诺重新生图字节可复现。

预览：previews/portrait_v2_1x.png、portrait_v2_8x.png、portrait_v2_1x_backgrounds.png及portrait_v2_4x_backgrounds.png，整数最近邻，无改脸。

来源：sources/source_manifest.json，源图母QA/最新卡与剧情均留SHA快照；qa/source_hash_recheck.json复核原件未变。限制与独立意见见qa/author_visual_review.json、qa/independent_review_acceptance.json。

- 眉眼仍拧紧、口角偏严肃，未完全达到母图平静审慎普通检查人的程度。
- 发束和短须仍有碎块，侧边余量不宽。
- 两次生图上限已到，不再修订。
- imagegen原图的像素风不等于原生逐像素绘制；74×100、32临时色与二值alpha仅技术派生。
- 未替换母图、角色卡、代码或游戏资源；未commit/push。

代词异常：旧卡/现卡正文“他”与母prompt adult man、男性母图一致。S91同一句“她只评普通适用性”复制入总表，按单源笔误延续成年男性，证据及原文行号见qa/identity_conflict_resolution.json；不改卡。
