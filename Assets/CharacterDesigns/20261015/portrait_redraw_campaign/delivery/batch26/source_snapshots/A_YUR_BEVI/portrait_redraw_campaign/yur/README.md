# yur 肖像重绘候选

独立QA最终选择：candidates/portrait_v2_inset_74x100_candidate.png

状态：candidate_with_limits，可交研究候选。共2次内置 imagegen（首稿+唯一修订），已停止并冻结生图。v2脸量、短颈窄领与小暗眼改善，原图发耳/髻完整。

限制：稀胡茬仍偏碎；小眼点仍浅亮；尚非四核心逐像素控制，不作原生像素批准。74×100、32临时色、二值alpha为整张画布等比NN技术派生，不是原生逐像素终稿，不代表游戏运行验收。inset从同一v2 raw缩放进72×98并居中，非第三次生图，不裁绘、不补画。

完整prompt与参数、完整回包、raw、源快照和sourceSHA、1x/4x三底/8x预览、QA、manifest和SHA256SUMS保留。旧图/卡/代码/冻结索引未改，不提交推送。

复现：
- python derive_portrait.py portrait_v1
- python derive_portrait.py portrait_v2
- python derive_portrait.py portrait_v2 inset
- python finalize_manifest.py portrait_v2_inset candidate_with_limits

复现核查：3个候选按所存raw重跑后SHA一致；源快照SHA未变。
