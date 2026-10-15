# 阿薇 BRY-NPC-AVI 头像重绘候选

最终选稿：`candidates/portrait_v2_74x100_candidate.png`。batch05 独立审核已选候选，各用首稿加唯一必要v2修订，不再生成。

## 文件与来源
- raw/：真实内置 imagegen 输出，按tool_returns/完整image_url原始字节保存，且已与工具原始落盘文件逐字节相等。
- prompts/：完整调用提示词和参数；sources/：当前人物卡、旧母版、历史QA、四风格参考及逐一来源SHA。
- candidates/：74×100技术派生，保留v1及所有导出；previews/：实际1×三底色与8×最近邻放大。
- qa/：技术指标、原始来源与重复导出一致性、作者审查、独立选稿摘要。综合独立QA在上级independent_qa/batch05单独维护。
- manifest.json、SHA256SUMS.txt：完整文件清单与SHA。

## 可复现
在本目录执行：
1. `python derive_portrait.py . portrait_v2`
2. `python finalize_manifest.py`

alpha≥128外接框裁切后，等比最近邻fit72×98居中于74×100；alpha128二值化；32色无抖动量化；透明RGB清零。最终使用MEDIANCUT，30个可见RGB色。
这是imagegen重绘衍生候选，非原生逐像素手工绘图，未游戏接入或运行验证；32色只是本批临时上限。

## 残留与边界
- 眉间仍稍蹙且蓝头巾占比偏宽；不继续生图。
- 此为imagegen衍生候选，未原生逐像素绘制、未接入游戏。
- 旧图、人物卡、源码未替换；未提交或推送。
