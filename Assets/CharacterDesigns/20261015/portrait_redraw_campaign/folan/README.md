# 佛兰肖像重绘：有限通过候选

选full v2：短颈窄领改善明显，40+与发须衣色成立，full眼白比inset更克制；源完整、导出bbox[5,5,72,97]。限制为灰发须仍细碎、眉心略忧，作为NN候选可交付。

选稿：candidates/portrait_v2_74x100_candidate.png
SHA256：a8efb17508770bd5babfa28f295038a725418b4068e962df94b3b47fbcabcfdc

raw/为实质imagegen源，tool_returns/为完整回包，prompts/为完整实际参数。两张成功输出，初稿加唯一必要修订；不再生成第三张。一次6引用参数校验失败无生图，完整错误及尝试参数另存；实际v2为5引用。

全画布等比NEAREST、阈值128二值alpha、≤32临时色MAXCOVERAGE无抖动导出，仅为74×100技术候选；未原生逐像素验收，未运行整合。inset只容纳边缘，不能修复源裁切。

预览含真实1x与整数8x及三底色；sources/保存现卡、母图、母QA、母manifest、四核心及剧情快照，源哈希复核全部一致。

复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python derive_portrait.py portrait_v2 inset；python finalize_manifest.py portrait_v2 selected_candidate_with_limitations。

不改母图/人物卡/代码/冻结索引；不部署，不commit/push。
