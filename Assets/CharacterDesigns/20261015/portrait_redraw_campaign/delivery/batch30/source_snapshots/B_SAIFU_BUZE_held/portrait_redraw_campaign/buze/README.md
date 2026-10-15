# 布泽 紧脸重绘候选

未选稿，暂挂 style/composition，不入交付选稿。`candidates/portrait_v2_inset_74x100_candidate.png` 仅作 held evidence。QA30 认定 v1/v2 的浅眼块、忧眉下撇口和长颈衣领问题改善不足；不回选、不第三次生成。身份、来源完整性、技术校验均通过，不能误标为身份冲突或技术失败。manifest 的 selected_portrait/selected_sha256 均为 null，delivery_eligible=false。

- built-in imagegen 实质重绘，初稿及一次修订，共 2 张；不再第三次生成。
- 原始回包含完整 image_url：`tool_returns/portrait_v1.json`、`portrait_v2.json`；PNG 与回包逐字节一致。完整实际实参及文本在 `prompts/`。
- 当前卡、母图、母 QA、剧情与四核心来源快照/SHA 在 `sources/`；交付前原源逐项重验在 `qa/source_hash_recheck.json`。
- 候选 74×100 RGBA、32 临时可见色、0/255 alpha；1x、8x NN、三底预览齐全。
- inset 为整幅等比 NEAREST fit 72×98 后居中；full保留。量化 MAXCOVERAGE，关闭抖动，alpha阈值128。没有脚本绘脸、补发耳或非等比变形。
- 上述是技术派生候选，不是原生逐像素终稿/游戏导入或实机验收。旧图、卡、代码和总索引未改，不提交推送。

## 视觉保留问题
- v2眉心与下撇口仍有忧虑感，未完全达到谨慎说理的平静眉口目标。
- 浅眼白和较长裸颈仍在，衣领占幅略多；不得包装成四核心风格已充分达标。
- 两次实际生成已用尽；不再开第三张。

## 复现
`python derive_portrait.py portrait_v2 inset`

`python finalize_manifest.py portrait_v2_inset held_style_composition_after_two_generations`

最新卡“干瘦”优先于旧母图/母QA“壮实”；保留同人发须、鼻形与衣色，差异在 source_manifest/spec_lock 中显式记录。
