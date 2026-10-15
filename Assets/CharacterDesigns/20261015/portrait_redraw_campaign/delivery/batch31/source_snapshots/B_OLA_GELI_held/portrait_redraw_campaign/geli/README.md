# 葛黎肖像重绘：未通过，保留证据

明确held，不回退v1充作完成。v2辫尾真实截底，alpha≥128底边36px接触（x1012–1047）、raw高1458；inset仅把截断尾巴缩进，不能补齐。v1源完整但亮大眼白/长颈未达集中修订目标。selected=null，delivery_eligible=false，保留v1/v2/inset为证据，无第三次。

无选稿，delivery_eligible=false。held证据：candidates/portrait_v2_74x100_candidate.png
SHA256：72213ea23c3c5760e481f31c37c31585fd98750991e435e3fde9840ead786ae9

raw/为实质imagegen源，tool_returns/为完整回包，prompts/为完整实际参数。两张成功输出，初稿加唯一必要修订；不再生成第三张。

全画布等比NEAREST、阈值128二值alpha、≤32临时色MAXCOVERAGE无抖动导出，仅为74×100技术候选；未原生逐像素验收，未运行整合。inset只容纳边缘，不能修复源裁切。

预览含真实1x与整数8x及三底色；sources/保存现卡、母图、母QA、母manifest、四核心及剧情快照，源哈希复核全部一致。

复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python derive_portrait.py portrait_v2 inset；python derive_portrait.py portrait_v1 inset；python finalize_manifest.py portrait_v2 held_not_delivery_eligible。

不改母图/人物卡/代码/冻结索引；不部署，不commit/push。
