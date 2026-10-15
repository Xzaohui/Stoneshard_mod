# Batch35 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## beina · deliverable_as_NN_derived_candidate_with_notes
选稿：`beina/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`9ee071b9643c6305e982e9d163c2035c07c6cbfc55c6009f541e238f0674d4de`
限制：内眉仍略忧惧、嘴角略低，神态未完全改成平稳坚定；眼白不全暗，发巾仍有平行层；头上透明余量较大，未宣称风格缺口全部清零；仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

## anni · held_style_not_clipping
暂挂证据：`anni/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`1e16522451cd110f00dfd96e835ffca630ecc55ce19f8973102ffcf377471125`
限制：风格暂挂：大亮眼白、妆感上眼线、小鼻甜脸仍主导，未通过四核心系列风格gate；v2真源裁断已修好；不靠inset或padding掩盖裁断。保留完整新raw和inset作证据，不列入交付选稿；仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

## kuen · deliverable_as_NN_derived_candidate_with_notes
选稿：`kuen/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`f5789504824665242a16f5a30ce6bf533168a0b6146dccec3d72449aed2c68c8`
限制：眼白仍偏亮、内眉仍略提，未完全达到小暗眼白/平稳眉口目标；胡茬仍有细碎点和锯齿，平行发束仍偏密；仅带限制候选，不能以技术格式宣称纯原生手绘；仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

## lint · deliverable_as_NN_derived_candidate_with_notes
选稿：`lint/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`466434bdc2e245be6716f902080e607ceb2323aefdd2f75686a491600e9d557a`
限制：内眉仍略忧、眼白偏亮及上眼线较强，平稳利落表现未完全满足理想；头发仍有平行层和皮肤小折面；窄领不能证明完整护理褂袖扣/随身物已制作；仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

## 证据与边界
- 34份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 最新卡外观优先旧母图：蓓娜约40岁洗砂住户，蓝巾灰罩衣锈内领；安妮20多岁普通当班护理者，棕低髻素护理褂；枯恩30多岁苍白自主患者，棕乱发稀胡茬及厚灰褐披肩灰蓝内领；琳汀30多岁护理接收员，短发别耳后素护理褂优先旧高髻赭裙。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
