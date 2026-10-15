# qiduo 肖像重绘候选

当前选用（带限制候选）：`candidates/portrait_v2_inset_74x100_candidate.png`。成功imagegen 2次：初稿＋唯一必要修订；不会第三次生成。

- 本轮为实质内置imagegen重绘，非旧母图裁切。
- `prompts/portrait_v1.json`、`portrait_v2.json`保留完整实参与引用路径；`tool_returns/`保留完整回包；`raw/`为回包字节解码原图。
- `sources/`保留当前卡、母图、母QA、母manifest、相关剧情、四核心及SHA。当前卡细描优先于旧母图外观读法，详见`spec_lock.md`。
- `derive_portrait.py`只做全画布等比NEAREST、MAXCOVERAGE≤32临时色无抖动量化、128阈值二值alpha；不脚本画脸。inset为同一v2原图在72×98框内全画布等比containment，绝非第三次生成或原生像素终稿。
- `previews/`包含1×、8×与三背景整数倍预览；技术检查不替代视觉验收。
- 视觉残余见`qa/author_visual_review.json`，来源真边界见`qa/source_boundary_checks.json`；batch34独立QA已选择此候选；完整限制及选定SHA见`qa/independent_review_acceptance.json`。
- 暂不是原生逐像素终稿，未导入游戏、未运行验收；旧图、源卡、代码及冻结索引未改，无commit/push。

复现全部候选：
`python derive_portrait.py portrait_v1`
`python derive_portrait.py portrait_v2`
`python derive_portrait.py portrait_v2 inset`
`python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`

保留限制：
- 唇颌仍有细点/锯齿须，灰尘短发部分平行细纹仍存。
- 眼白偏亮，眉较母QA描述略厚。
- alpha>=5主体四边无真裁断；alpha1低透明边缘杂点存在，不能称全部非零alpha都离边。
- 技术量化、二值alpha与containment不构成原生逐像素终稿。
