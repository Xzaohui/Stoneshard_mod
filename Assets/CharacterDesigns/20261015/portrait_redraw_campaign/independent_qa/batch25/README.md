# Batch25 独立 QA

最终结论：塔雅、缇娜为带限制 NN 派生候选；溪悠、梅蓓 held，不进入交付。

仅 selection_lock.json 的 delivery_allowlist 两条精确路径/SHA 有效。held 的 selected_path 与 selected_sha256 为 null，仅保 held_candidate_path / SHA 用于追溯。各成功生成2张、初稿集中反馈1轮；无第三次成功生成。六参照参数校验失败未产图，独立于成功生成数。

已核：最新卡与母图/母QA、四核心、源快照和SHA、完整工具回包与raw逐字节一致、74×100不超过32色二值alpha、全部派生与1×/整数NN/三底预览复现、作者manifest全量文件SHA和SHA256SUMS。技术通过不替代视觉gate。

塔雅/缇娜保留眼白仍浅、发带偏多与真实右余量较窄的限制。溪悠/梅蓓保身份与短颈改善，但白巾/横向发量挤小脸、眼白明显；与此前held呼蕾同倍率对照后继续held。原始轮廓未证实裁断，技术inset不能宣称修复构图或补回源轮廓。

查看 final_audit_summary.json、selection_lock.json、四份 final_visual_review.json、四份 technical_audit.json。comparison_with_held_hure_4x_NN.png为五张同倍率比较；selected_contact_4x_NN.png仅含两位可交候选。

这些都是整幅imagegen输出经NN等比缩小、阈值alpha和限色的派生候选，非原生像素终稿，也未集成/实机验证。未修改生产旧图、人物卡或代码，未commit/push。
