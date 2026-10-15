# saler 肖像重绘候选

最终选择（独审通过，带限制）：`candidates/portrait_v2_74x100_candidate.png`。已完成初稿及唯一必要v2，实质生成2次，不再第三次。

## 来源与绘制

- 实读当前卡、相关台本、母QA与manifest；母图及Mara/Iwo/Leiya/Tore四核心已实看。
- 当前卡年龄/帽与披肩更新优先；源快照和SHA在`sources/source_manifest.json`，细则在`spec_lock.md`。
- 内置imagegen实质绘制；`prompts/portrait_v1.json`与`portrait_v2.json`保存完整参数，`tool_returns/`保存完整返回，`raw/`是返回图像原样解码。
- 候选为完整原始画布等比NEAREST缩小居中；MAXCOVERAGE无抖动≤32临时色、alpha阈值128二值化。不是原生逐像素终稿。
- 桑勒v2完整原始画布导出74×100，保持源帽发耳真实余量。初次v2请求六参考超工具上限而在生图前拒绝，修正为五参考后正常完成唯一v2；失败记录另存。

## 复现

`python derive_portrait.py portrait_v2`

`python finalize_manifest.py portrait_v2 selected_candidate_with_limitations`

1×、1×三底色、4×三底色、8×整数NEAREST在`previews/`。作者实看与独审集中反馈在`qa/`，独立视觉复审已接受本选择，技术复验由batch23独审另存。眼白仍略亮、局部发丝较细作为限制保留，不以量化冒充原生审定。

未改旧图、人物卡、代码或冻结索引，未集成或游戏内验证，未commit/push。
