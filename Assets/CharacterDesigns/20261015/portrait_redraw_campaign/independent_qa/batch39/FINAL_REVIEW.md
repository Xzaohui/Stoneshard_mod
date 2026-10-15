# Batch39 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## don · deliverable_with_notes
选稿：`don/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`b94d982a16588fa6bf8eddabb767dae4708a65c62b46d7a9a282d51350a06a1b`
限制：须发纹理仍比四核心细碎，年长面相略显苍老；这是概念提案而非精确年龄测量；仅74×100 NN等比缩放/32色无抖动/二值alpha技术派生候选，非原生逐像素终稿，未集成未实机验收。

## fuduo · deliverable_with_notes
选稿：`fuduo/candidates/portrait_v2_74x100_candidate.png`
SHA256：`98fa10d3e86f4d079020cb5a2d382aeef8b7fa256dd38301f5d966d213fa1a7e`
限制：高领仍偏厚且占底部面积，面貌仍略秀气；无儿童化硬冲突，但不是完全达到四核心窄领与粗块终稿；仅74×100 NN等比缩放/32色无抖动/二值alpha技术派生候选，非原生逐像素终稿，未集成未实机验收。

## kofu · deliverable_with_notes
选稿：`kofu/candidates/portrait_v2_74x100_candidate.png`
SHA256：`732211d8151026ce3bba0d24102220dca4de6df88f719f6db964e402847b97d6`
限制：颈仍稍长，眼白和上睫线仍偏亮强，领/围裙带有一定面积；可交带注候选，未达原生终稿；仅74×100 NN等比缩放/32色无抖动/二值alpha技术派生候选，非原生逐像素终稿，未集成未实机验收。

## lema · deliverable_with_notes
选稿：`lema/candidates/portrait_v2_74x100_candidate.png`
SHA256：`16508f00ec4a6c484189f7d4907d39a3f7836675ab95b3f850d39dde3d91bba9`
限制：眼白仍较亮，胡茬与发丝细点仍多于核心大块语法；属于有保留的NN候选而非原生逐像素完成；仅74×100 NN等比缩放/32色无抖动/二值alpha技术派生候选，非原生逐像素终稿，未集成未实机验收。

## 证据与边界
- 30份原始源/历史git证据独立快照与终检SHA一致；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；作者较早冻结状态awaiting_independent_qa真实保留，本次独立selection_lock为最终结论覆盖。只准交付selection_lock中的选稿文件与SHA。
- 多恩五十多岁父亲农夫、芙朵二十多岁佃农女儿、蔻芙二十多岁德娅女儿、雷玛三十多岁三篱邻户身份分明。当前S91软塌帽、自染头巾（蔻芙明确浅蓝）及洗白罩衫优先于旧概念遗漏。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
