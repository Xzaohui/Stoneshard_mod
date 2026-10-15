# Batch37 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## aro · deliverable_as_NN_derived_candidate_with_notes
选稿：`aro/candidates/portrait_v2_74x100_candidate.png`
SHA256：`e5a2cf8486261fff5a28f6106615891c67c39f0e9dea024780f4b29e646cb164`
限制：内眉仍略忧、颈部稍长，未达到完全沉静短颈的理想；发束仍有平行层，1x个别皮肤折面小碎点；不以32色格式宣称风格零缺口；仅74×100 NN技术派生候选，非原生逐像素终稿；未集成游戏、未实机验证。

## gura · deliverable_as_NN_derived_candidate_with_notes
选稿：`gura/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`1626640c4a14b9e39306b817f95e94dc2298315c4f5c0b9b3e32fe239e19e8d5`
限制：内眉仍略V形、发丝平行层仍可见；raw左右余量仅16/10源像素，源边距偏窄；inset增加目标透明格不代表满足原提示词的宽源边距要求；仅74×100 NN技术派生候选，非原生逐像素终稿；未集成游戏、未实机验证。

## lein · held_source_contour_margin_and_style
暂挂证据：`lein/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`7e1d2ba859c3656cd812b6e3f318665b4faf295c8cc14c422f113aa63a4298a6`
限制：源轮廓/真实余量门槛未过，selected=null，v2_inset仅保留审查证据，禁止进入交付选稿；眼白仍不全暗、上眼线和发层仍强；风格改善不能抵消源边界风险；仅74×100 NN技术派生候选，非原生逐像素终稿；未集成游戏、未实机验证。

## turi · deliverable_as_NN_derived_candidate_with_notes
选稿：`turi/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`995312565126d56e0fa4dc9d57e1741eadcaaf3277e7f53c4a8b8478290a1d2f`
限制：眼白仍偏浅、内眉稍忧，未完全达到小暗眼白目标；发与灰鬓仍有平行长层，短须局部碎点；只作带限制候选；仅74×100 NN技术派生候选，非原生逐像素终稿；未集成游戏、未实机验证。

## 证据与边界
- 28份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 当前卡外观优先：艾萝约40岁深色保管者长衣，旧橄榄短披不沿用；古菈30多岁本班维护工灰厚褂；蕾因30多岁女向导，棕软帽粉笔与绿披；图里约40岁精瘦男检查匠，灰鬓短须橄榄披。蕾因源边缘未保真实透明余量，α≥128右界计数0不等于全阈值透明；保留多阈值及3x边界证据，不简单声称全opaque裁断。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
