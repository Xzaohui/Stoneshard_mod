# Batch19 独立审计冻结

冻结时间：2026-10-15T11:15:44.770679+00:00

四人均终选 v2，状态为 pass_derived_candidate_with_notes。每人 2 份实际 imagegen 回包，1 轮集中反馈；没有第三次生图。

## 选择与完整 SHA-256

- 辛娅（xinya）：xinya/candidates/portrait_v2_74x100_candidate.png
  SHA-256：8f5bb00c58dbe1afaa05486dad1c44e5ee9083d4faf1b661a4baa1c59b81d214
- 乌珀（wupo）：wupo/candidates/portrait_v2_74x100_candidate.png
  SHA-256：35e76b0d510136ae88d7730f547dc2cac9d546f589e5320bee45feff814859b2
- 碧珞（biluo）：biluo/candidates/portrait_v2_74x100_candidate.png
  SHA-256：a16086b8120ec168d73d3aa4b0f8e59275f10ebafbe1c1ebfd8947562f321ac7
- 埃文·行（evan）：evan/candidates/portrait_v2_74x100_candidate.png
  SHA-256：1ff0423c76cc3749e6b8c069ec46be9b41a18a24e11605edeb645b1b1f25ced0

## 独立核验

- 准确当前人物卡、roster、选定母图、母图 QA、认可四核心均已核对；母图与候选真实打开查看。
- 所有 source snapshot 与原文件 SHA-256 相同，冻结时再次核对原卡/母图/母 QA/母清单未变。
- 完整工具回包图片字节与 raw 一致，并核对工具保存的原始文件。
- 先完整阅读作者脚本，再在本 QA 目录副本复跑；8 版候选、1x、8x、三底预览和 metrics 逐字节相同。
- 额外独立实现重新生成候选，74×100、最多32个可见RGB色、二值alpha和8x最近邻预览通过。
- raw 与候选分别检验真实边界；四个选定 raw 都保完整发耳，不以透明 padding 伪装裁边修复。
- 作者 manifest 全文件 SHA 与字节数、SHA256SUMS 完整覆盖均通过；freeze_manifest.json 列出全部交付文件哈希。

## 保留限制

- 辛娅：仍有谨慎忧意，右眼白略亮。；高分辨率生图经NN缩小和32色量化的派生候选，非原生像素终稿；未接入、未实机验证。
- 乌珀：低睑疲态仍强，局部颊纹细碎。；高分辨率生图经NN缩小和32色量化的派生候选，非原生像素终稿；未接入、未实机验证。
- 碧珞：眼白仍偏亮。；脸旁重新出现一小段松散波发，仍与独立长鼻宽颧面形并存，未退回初稿整体近似脸。；高分辨率生图经NN缩小和32色量化的派生候选，非原生像素终稿；未接入、未实机验证。
- 埃文·行：仍带谨慎疲态。；局部胡须色纹略碎。；高分辨率生图经NN缩小和32色量化的派生候选，非原生像素终稿；未接入、未实机验证。
- 埃文现行卡的低檐帽/早白鬓角优先于旧卡时期裸头母图；已记录差异，保母图独立面形和苔披风赭衣。
- 这些是高分辨率重绘经最近邻缩小、阈值alpha和32色量化的派生候选。规格检查不能证明原生像素终稿。
- 未替换任何生产旧图、人物卡或游戏代码；未接入游戏、未实机验证；未 commit/push。

## 交付清单

- 四个角色目录各含 sources、prompts、完整 tool_returns、raw、两版 candidates、1x/8x/三底 previews、QA、spec lock、manifest、SHA256SUMS、可复跑导出脚本。
- 本审计目录含来源核对、集中反馈、终选视觉评审、最终技术审计、脚本副本逐字节复跑证据、独立生成候选、四人1x/4x对照、四核心参考、冻结清单和全目录SHA256SUMS。
- 碧珞另有一次6参考图参数校验拒绝记录，未生成图片；成功成图仍为2份。无第三份成图。
- replay/ 为独立审计副本，不是新的生图调用。
