# 黎恩·岗 / EED-NPC-LIN 肖像重绘候选

已完成两次内置 imagegen 实质重绘，独立QA31锁定 candidates/portrait_v2_74x100_candidate.png。选稿 SHA256：24fa414638fce73b0884b8060b48b880b1e79cf674ae5fd4121fcb4f86178490。

有保留通过：身份为三十多岁清瘦长鼻净面护林者；最新卡低帽檐优先，旧母版的棕发、苔绿短披与棕衣保持。脸幅/颈领比首稿改善，源帽发耳完整。保留顶空13px、眼白稍亮、颈侧略长；导出右余量1px而源实际19px，不用inset再缩脸。不称完全达到四核心紧脸标准。

74×100 RGBA、32可见色、二值alpha为临时技术规范。完整画布等比NEAREST缩放、无抖动MAXCOVERAGE量化和alpha阈值仅为技术派生，不是原生逐像素终稿。无脚本画脸、局部几何改形、游戏整合或运行验收。旧图/卡/代码/冻结索引均未改，无commit/push。

复现：python reproduce.py。所有prompt实参在prompts；完整回包在tool_returns；raw字节与回包一致；sources保存来源及SHA；qa记录独立/作者检查；previews含1×及整数NN。一次六参考参数校验在生图前被拒，证据单列；仅两份成功生成图，没有第三次实质生图。
