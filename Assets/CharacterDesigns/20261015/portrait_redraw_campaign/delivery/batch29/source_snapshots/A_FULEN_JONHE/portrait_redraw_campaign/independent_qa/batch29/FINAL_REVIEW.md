# Batch29 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## fulen · selected_candidate_with_limitations
选稿：`fulen/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`b6e1a7a2ccf76396953d4434fd9f412324b093c558e15b168660faec7c0bef38`
限制：源左发真实余量仅5/1079源像素，安全余量不足仍保留；inset仅解决目标NN采样触边；眼白仍局部亮点，米白头巾占幅偏大，发纹需未来原生逐像素整理；仅为NN/32色技术派生候选，非原生逐像素终稿；未导入、未实机验证。

## jonhe · selected_candidate_with_notes
选稿：`jonhe/candidates/portrait_v2_74x100_candidate.png`
SHA256：`29e6b3336e876163259db831a7bbe4a0cae27c1a11527825d3c0195cbd843b36`
限制：眼白仍有局部较亮暖点；帽发与灰辫占幅偏大，顶端留白偏多，面部覆盖低于紧凑核心；浅色发丝量化后有细碎块；仍为生成图NN与32色技术派生，未逐像素原生整理；非原生逐像素终稿；未导入、未实机验证。

## moda · selected_candidate_with_limitations
选稿：`moda/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`ec29da9943e114082abacdf341675969facf069ce4ab6e183ae6cd53c42a5f0f`
限制：源右侧不透明轮廓仅2/1079源像素余量，极窄且边缘alpha残留触边；inset只避目标网格触边，不修复或提高源余量；眼白仍局部偏亮灰暖点，深棕卷发和巾皱纹略碎，面部整体像素组织未原生整理；仅为NN/32色技术派生候选，非原生逐像素终稿；未导入、未实机验证。

## rosa · selected_candidate_with_limitations
选稿：`rosa/candidates/portrait_v2_74x100_candidate.png`
SHA256：`2f63db5a677ad9e6f5a07f74eeb68feac575fe803ea0281ba5b54989578a52fb`
限制：灰缕发纹依然偏碎、眼部残留少量亮暖点；像素结构仍需原生逐点整理；仅为NN/32色技术派生候选，非原生逐像素终稿；未导入、未实机验证。

## 证据与边界
- 28份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 最新卡外观优先旧母图遗漏；芙伦护理素褂厚围裙，琼荷低帽檐葡园工作帽，墨达40+红鼻头，罗莎50岁深色围裙。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
