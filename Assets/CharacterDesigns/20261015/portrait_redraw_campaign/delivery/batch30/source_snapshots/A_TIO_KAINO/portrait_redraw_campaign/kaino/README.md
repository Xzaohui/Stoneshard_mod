# 凯诺 紧脸重绘候选

选稿：`candidates/portrait_v2_safe_74x100_candidate.png`；QA30 已确认选为带限制候选。

- built-in imagegen 实质重绘，初稿及一次修订，共 2 张；不再第三次生成。
- 原始回包含完整 image_url：`tool_returns/portrait_v1.json`、`portrait_v2.json`；PNG 与回包逐字节一致。完整实际实参及文本在 `prompts/`。
- 当前卡、母图、母 QA、剧情与四核心来源快照/SHA 在 `sources/`；交付前原源逐项重验在 `qa/source_hash_recheck.json`。
- 候选 74×100 RGBA、32 临时可见色、0/255 alpha；1x、8x NN、三底预览齐全。
- safe 为整幅等比 NEAREST fit 70×96 后居中；full 与72×98 inset保留。量化 MAXCOVERAGE，关闭抖动，alpha阈值128。没有脚本绘脸、补发耳或非等比变形。
- 上述是技术派生候选，不是原生逐像素终稿/游戏导入或实机验收。旧图、卡、代码和总索引未改，不提交推送。

## 视觉保留问题
- 肤色相对四核心略暖。
- 裸颈仍略多于四核心最紧脸标准；眼白尚有灰浅小块。
- 面部部分色阶仍带生成式细像素质感，灰发少量条带仍在，不是原生逐像素终稿。
- 两次实际生成已用尽；不再开第三张。

## 复现
`python derive_portrait.py portrait_v2 safe`

`python finalize_manifest.py portrait_v2_safe selected_candidate_with_limitations`

一次 6 个输入的工具参数在生成前被拒绝，错误与错误实参已保留；实际使用 5 个输入生成 v2，生成图仍为 2 张。
