# 沃汀 PAS-NPC-WOTIN 重绘候选

选择：candidates/portrait_v2_74x100_candidate.png。已完成初稿及独立 QA 指定的一次修订，共两次成功 image_gen，禁止第三次生成。独立 QA18 终审通过候选口径，已冻结当前v2。

- v2 保留身份，压小眼白、缩短颈部并提高衣领，增加脸部占比；完整母图、源卡、母 QA、剧情与四核心参考已实查。
- 此为 built-in image_gen 实质重绘后，整幅画布等比 NEAREST、alpha 128 二值化、MAXCOVERAGE ≤32色无抖动的技术派生候选。未脚本画脸、裁切或额外inset；不冒称原生像素终稿。
- 原raw具有真实四边余量；见 qa/author_visual_review.json，保留可见局限。独立验收记录见 qa/independent_review_acceptance.json。
- raw 与 tool_returns 保存完整返回并核对字节一致；prompts 保存每次实际参数与文本。
- previews 保留1x、8x整数NN，以及深中浅底1x和4x。
- 复现：python derive_portrait.py portrait_v2；python finalize_manifest.py portrait_v2 selected_candidate_with_limitations。qa/reproduction_check.json 证明重建SHA一致。
- 未改旧素材、人物卡、代码；未commit/push；未整合或实测游戏；独立QA不等于用户验收。
