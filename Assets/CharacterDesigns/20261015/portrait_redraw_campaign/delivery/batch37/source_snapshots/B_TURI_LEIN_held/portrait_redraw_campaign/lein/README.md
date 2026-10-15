# 蕾因 / HIG-NPC-LEIN 紧脸肖像重绘

暂挂，不能交付：源轮廓/真实余量及风格门槛未通过。v2原raw最右列alpha最大47；alpha≥128边界像素为0，alpha≥16接边69像素（y769–847），alpha≥5接边108像素。近不透明主体到倒数第2列，但外缘缺真实透明余量，不能独立确认外层发廓完整。该证据不等于身份错误，也不能概括为全不透明主体裁断。inset仅增加技术画布空隙，不能恢复或证明源轮廓完整。 v1虽完整但大亮眼、忧眉、长颈未过风格。manifest selected_portrait 与 selected_sha256 均为null，delivery_eligible=false。仅保留 v2_inset 为 held 复核证据。

完成初稿与唯一一次必要 imagegen 修订，共2张成功图，禁止第三次生成。

## 证据与复现

- v1、v2 raw及同raw等比inset技术派生均保留
- 完整实参：prompts/portrait_v1.json、portrait_v2.json；完整提示词同名txt
- 完整回包：tool_returns/portrait_v1.json、portrait_v2.json；raw与回包字节一致
- 6参考图参数在预检被工具的5图上限拒绝，零成功图，失败记录保留；成功v2使用5图。四核心均已实际查看；v1引用全部四核心，v2沿用Mara、Leiya、Tore
- 当前卡/母版/母QA/故事定位、SHA及快照：sources/source_manifest.json
- 1x及整数NEAREST浅深底预览：previews/
- 独立选稿结论、作者review、技术指标、原raw右边界诊断：qa/

在本目录执行 python derive_portrait.py portrait_v2 inset，再执行 python finalize_manifest.py portrait_v2_inset held_source_contour_margin_and_style。完整回包/raw可确定复现技术派生；生成模型再调用不保证同图。

74×100 RGBA、≤32临时可见色、二值alpha仅是技术出口。imagegen实质重绘加等比NEAREST containment、无抖动量化与alpha阈值是派生候选，不是原生逐像素终稿。inset不改变五官，也不补全或证明raw外层轮廓完整；未修改旧图、角色卡或代码，未集成/运行验证，未commit/push。
