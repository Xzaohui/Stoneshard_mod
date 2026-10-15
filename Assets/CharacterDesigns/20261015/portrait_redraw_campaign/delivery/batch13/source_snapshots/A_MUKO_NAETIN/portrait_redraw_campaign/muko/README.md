# muko 头像重绘候选

选中：`candidates/portrait_v1_inset_74x100_candidate.png`。独立视觉QA通过并保留候选备注；共1次 imagegen。

raw 保存 imagegen 原始字节，tool_returns 保存完整工具回包，prompts 保存完整输入参数。candidates 为 74×100 透明画布，使用72×98容纳框等比整图NEAREST缩放（实际72×97），无抖动32色上限、二值 alpha 的明示派生候选；previews 提供 1x、8x 和三底色校验。derive_portrait.py 可离线重做技术导出，manifest.json 记选中版本、来源与全部产物，SHA256SUMS 核验全部文件。

残余：眼白仍略亮，发须仍有少量细纹。；颈侧块面不足以确认旧烫痕细节；不将面部阴影写成伤疤事实。

未覆盖旧图，未修改人物卡/代码，未提交推送；未原生逐像素验收或接入游戏。
