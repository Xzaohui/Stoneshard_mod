# 娜泽 / DEN-NPC-NOZE 肖像重绘

暂留，不进入所选交付。QA27判定 held_style_gap：长裸颈、发辫挤占脸幅，修订后眉更紧，紧脸主目标仍未收足。selected_portrait=null，delivery_eligible=false。v2 inset仅作为留档证据，不把v1替回已通过。

- 留档证据：candidates/portrait_v2_inset_74x100_candidate.png
- SHA-256：68779c0072745d373f601ea19d96a461781bf14c146487d12a50c36e6a562447
- 原始图：raw/portrait_v1_raw_imagegen.png、raw/portrait_v2_raw_imagegen.png
- 每轮完整实参及回包：prompts/portrait_v*.json、tool_returns/portrait_v*.json
- 1x与整数NN、三底预览：previews/
- 卡、母图/母QA、剧情和四核心源快照及SHA：sources/
- 作者复现和独立结论：qa/

内置 image_gen 实质重绘初稿＋唯一修订，共2次，已用尽额度；不进行第三次。v1与v2原稿均完整保留。74×100、32临时可见色、二值alpha为全画布等比NEAREST＋无抖动MAXCOVERAGE派生结果，inset将完整源画布放入72×98再居中，未裁切、未脚本画脸。它不是原生逐像素终稿。

复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python derive_portrait.py portrait_v2 inset；python finalize_manifest.py portrait_v2_inset held_style_gap。作者重跑全部候选字节一致；独立QA在批次目录另存。

旧图、角色卡、代码、冻结索引不变，无commit/push；未接入游戏与运行验证。
