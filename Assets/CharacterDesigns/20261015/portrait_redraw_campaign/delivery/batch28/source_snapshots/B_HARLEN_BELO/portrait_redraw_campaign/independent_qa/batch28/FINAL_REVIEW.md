# Batch28 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## viko · deliverable_candidate_with_notes
选稿：`viko/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`eb30a2f311779a1cee39bffeebca45e1b3efac8ed23e672201c37e10375bba09`
限制：眼白与眼框仍比四核心稍亮大；不是严格小暗眼终稿；头发带状细节仍较多，非原生逐像素终稿；源alpha≥16右余4px、≥128右4px；仅一个alpha≥5弱点触右缘，未达4%目标。full网格x73触边，选同源72×98整幅等比inset，未补画源轮廓。

## ile · deliverable_candidate_with_notes
选稿：`ile/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`378f6ce15c03de6aacaeaf8dcdfe52e84a462fbb9ae4247e6f66e8fedb7658fb`
限制：眼白仍较亮、发带与颈部细节偏多，短颈/大脸目标仅部分达到；源alpha≥16右核心2px，≥128为3px，alpha≥5仍有20个极弱右缘点；未达4%余量目标，不声称全alpha无触边；full采样到目标x73属于NN网格贴边；选同源72×98整幅等比inset，不能把inset称作源裁断修复；原生像素与实机未经验证。

## harlen · deliverable_candidate_with_notes
选稿：`harlen/candidates/portrait_v2_74x100_candidate.png`
SHA256：`37e64b70711cfc88486b1c1ae1c9627eee72a452599acaa4c529aed190774ccb`
限制：发须仍有较多碎条与点，不是四核心同等简练像素组织；眼白仍可见，颈尚略长；作为带限制NN候选交付；源实心右余20px，小于约4%提示目标，但完整发/耳轮廓无实质裁断；alpha≥5四边0。

## belo · deliverable_candidate_with_notes
选稿：`belo/candidates/portrait_v2_74x100_candidate.png`
SHA256：`1010d438786069d51b0dc54a6365facb7d06c03220f4dd76c2d17c32ec90f432`
限制：眼白仍偏亮，颈段仍略长，发束仍多于四核心；顶空15px使头占较四核心偏小；完整源不裁剪、不脚本放大脸；源实心右余31px，小于约4%提示目标，但无发耳实质裁断；alpha≥5四边0。

## 证据与边界
- 30份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 最新卡外观优先旧母图遗漏；哈伦按当前卡读三十多岁及烟熏黄发，旧灰发灰须母图只保脸型与衣色身份，不回退老相。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
