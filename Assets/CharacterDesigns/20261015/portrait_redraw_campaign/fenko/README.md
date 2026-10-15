# fenko 头像重绘候选

选中 `candidates/portrait_v2_inset_74x100_candidate.png`。独立视觉QA选v2并保留候选备注；每人共2次内置imagegen，v1初稿、v2唯一必要修订，无第三轮。

`raw/`保存未修改原始PNG，`tool_returns/`保存完整工具回包，`prompts/`保存完整prompt及参数；`sources/`是现卡、母版、旧QA、四核心头像和相关台本的字节快照与SHA。

74×100为72×98容纳框，实际72×97等比整图NEAREST缩放、MAXCOVERAGE无抖动32可见色上限量化及alpha阈值128得到的明示派生候选；没有程序重画几何或面部，不是原生逐像素终稿。`previews/`含1x、整数8x及三底色1x/4x。

复现：`python derive_portrait.py portrait_v2 inset`；`python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`。

独立终选备注：30多岁的长角脸和克制自尊抿嘴保留；面部放大、颈领明显缩短。颈领仍比理想略多，眼白小亮块、发帽细线保留候选备注。v2原图完整，alpha≥128 bbox(11,81,1077,1425)，右侧无实际截断；72×98整图等比NN技术inset仅留边。

旧图、现人物卡、代码均未修改，无commit/push，无游戏接入或runtime验收。
