# lodo 头像重绘候选

选中 `candidates/portrait_v2_74x100_candidate.png`。独立视觉QA选v2并保留候选备注；每人共2次内置imagegen，v1初稿、v2唯一必要修订，无第三轮。

`raw/`保存未修改原始PNG，`tool_returns/`保存完整工具回包，`prompts/`保存完整prompt及参数；`sources/`是现卡、母版、旧QA、四核心头像和相关台本的字节快照与SHA。

74×100为74×100整画布等比整图NEAREST缩放、MAXCOVERAGE无抖动32可见色上限量化及alpha阈值128得到的明示派生候选；没有程序重画几何或面部，不是原生逐像素终稿。`previews/`含1x、整数8x及三底色1x/4x。

复现：`python derive_portrait.py portrait_v2`；`python finalize_manifest.py portrait_v2 selected_candidate_with_limitations`。

独立终选备注：40多岁成熟宽鼻颧/圆方颌及偏侧接待浅笑清楚；头巾结离框，脸放大、颈领缩短。轻微发细线、肩领余量和小亮眼白保留候选备注。

旧图、现人物卡、代码均未修改，无commit/push，无游戏接入或runtime验收。
