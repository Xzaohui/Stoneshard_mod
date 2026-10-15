# 洛芙肖像重绘候选

独立QA选择：`candidates/portrait_v2_74x100_candidate.png`
SHA256：`7c9983c5bd9621243d81b0ad49ec1a667702170e78d0940bc82a86fb571d7bd2`
状态：`selected_candidate_with_limitations`。每人内置imagegen首次实质重绘＋一次集中必要修订，共2次，已停止生成。

## 结果与限制

颈衣区域仍偏多，白巾折纹仍偏细。v2源图已完整生成巾结及双尾，alpha≥5右余量15px、≥16右余量17px，未接边；最终full导出右1列、下1行透明。inset作为未选技术备选保留，不用其掩盖源轮廓问题。

74×100 RGBA，32个可见临时色，二值alpha。原图是imagegen重绘；等比NEAREST、MAXCOVERAGE无抖动量化与alpha128阈值是技术派生，不能称原生逐像素终稿。未整合游戏，未运行验证。

## 证据与复现

- raw/：完整生成原图；tool_returns/：完整工具回包；二者逐字节匹配验证
- prompts/：每次完整提示词及准确实参；qa/generation_provenance.json：输入SHA、工具回包SHA及可复现边界
- candidates/：v1、v2 full与v2 inset均保留，以上路径是唯一选稿
- previews/：每版实际1x透明图、1x三背景及最近邻4x/8x
- sources/：最新角色卡、母图、母版QA、剧情、四核心风格参考的只读快照及SHA
- qa/：身份预检、源图边缘审计、作者实际查看记录、集中反馈、终审选择、技术复现
- manifest.json：选稿、输入、产物与SHA；SHA256SUMS：全文件校验表

复现选稿：`python derive_portrait.py portrait_v2`
复现清单：`python finalize_manifest.py portrait_v2 selected_candidate_with_limitations`
技术产物重复运行后候选、所有预览及metrics逐字节匹配。imagegen无种子参数，重新生成不保证相同，但原始回包与完整实参已保存。

旧图、角色卡、代码及冻结总索引不变；未commit、push。
