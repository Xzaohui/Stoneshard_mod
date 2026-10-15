# 奥菈·纹 / EED-NPC-OLA 肖像重绘候选

已完成两次内置 imagegen 实质重绘，独立QA31锁定 candidates/portrait_v2_74x100_candidate.png。选稿 SHA256：3ad917cfd8888927ed4d124c936e5efeb84b182c135a538dd376e9b44e0bac84。

有保留通过：四十多岁成熟锯工骨相与棕发髻锈衫身份保持；颈胸、大围裙扣明显减少，脸幅增大。源发髻耳完整，raw右11px真实余量。保留顶空11px/下空8px、眼白稍亮、眉心稍忧惧；肩皮/围裙处在紧脸画幅外。不要用inset继续缩脸。不称完全达到四核心紧脸标准。

74×100 RGBA、32可见色、二值alpha为临时技术规范。完整画布等比NEAREST缩放、无抖动MAXCOVERAGE量化和alpha阈值仅为技术派生，不是原生逐像素终稿。无脚本画脸、局部几何改形、游戏整合或运行验收。旧图/卡/代码/冻结索引均未改，无commit/push。

复现：python reproduce.py。所有prompt实参在prompts；完整回包在tool_returns；raw字节与回包一致；sources保存来源及SHA；qa记录独立/作者检查；previews含1×及整数NN。仅两份成功生成图，没有第三次。
