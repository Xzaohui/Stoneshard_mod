# 坦瑟 / DEN-NPC-TANSER 肖像重绘

独立 QA27 选择 v2_inset 为附限制的候选。面部扩大、短颈、小暗眼与胡茬并块改善，旧缝痕和四十岁上下克制警觉保留。

每人共2次内置 image_gen 实质调用（初稿+唯一必要修订），没有第三次。

- 选中候选：`candidates/portrait_v2_inset_74x100_candidate.png`
- SHA-256：`bae249098163e729dbfc8b63a194ede2d06a2b34bc47b210cec88d1a655a87b2`
- 原图：`raw/portrait_v1_raw_imagegen.png`、`raw/portrait_v2_raw_imagegen.png`
- 完整原始回包：`tool_returns/portrait_v1.json`、`tool_returns/portrait_v2.json`；解码后与raw逐字节一致
- 完整prompt与实际实参：`prompts/portrait_v1.txt/.json`、`prompts/portrait_v2.txt/.json`
- 身份与来源：`spec_lock.md`、`sources/source_manifest.json`；当前卡优先与旧母图差异已记录
- 终审：`qa/independent_review_acceptance.json`；作者逐张实看：`qa/author_visual_review.json`
- 源边界：`qa/portrait_v1_raw_edges.json`、`qa/portrait_v2_raw_edges.json`
- 复现与原图回包同一性：`qa/reproducibility.json`；完整源SHA复核：`qa/source_hash_recheck.json`
- 1x及整数NN预览：`previews/`，含深灰/中灰/浅底

## 限制

- 源右边y717–729存在低alpha5–21羽边触边，alpha>=16有3像素；不能称所有alpha均留边。
- 独立灰底放大核实实心发尖在边前闭合；alpha>=128右侧真实余量10px，inset二值候选留2px侧边。
- 仍有平行发纹和局部细像素层次；不是原生逐像素终稿。
- 74×100、≤32临时色、二值alpha和等比NEAREST containment为技术派生候选，不是原生像素批准。
- 未替换母图、人物卡、代码或冻结索引，未导入游戏、未实机验证、未提交推送。

## 复现

在本目录运行：`python derive_portrait.py portrait_v1`、`python derive_portrait.py portrait_v2`、`python derive_portrait.py portrait_v2 inset`，最后 `python finalize_manifest.py`。派生环节已复跑且 candidates/previews/metrics SHA 完全一致。imagegen 本身不保证再次得到同一随机结果；工具未暴露 model/size/quality/seed，因此未虚构。

无脚本绘脸；全源等比 NEAREST、不裁剪、不重塑面部；alpha128阈值、MAXCOVERAGE无抖动≤32色只是技术适配。
