# 图里 / HIG-NPC-TURI 紧脸肖像重绘

独立QA选取带限制NN技术候选：candidates/portrait_v2_inset_74x100_candidate.png。SHA256：995312565126d56e0fa4dc9d57e1741eadcaaf3277e7f53c4a8b8478290a1d2f。颈领、成熟灰鬓与鼻颧已改善；眼白仍浅、眉稍忧、平行发层残留。

完成初稿与唯一一次必要 imagegen 修订，共2张成功图，禁止第三次生成。

## 证据与复现

- v1、v2 raw及同raw等比inset技术派生均保留
- 完整实参：prompts/portrait_v1.json、portrait_v2.json；完整提示词同名txt
- 完整回包：tool_returns/portrait_v1.json、portrait_v2.json；raw与回包字节一致
- 6参考图参数在预检被工具的5图上限拒绝，零成功图，失败记录保留；成功v2使用5图。四核心均已实际查看；v1引用全部四核心，v2沿用Mara、Leiya、Tore
- 当前卡/母版/母QA/故事定位、SHA及快照：sources/source_manifest.json
- 1x及整数NEAREST浅深底预览：previews/
- 独立选稿结论、作者review、技术指标、原raw右边界诊断：qa/

在本目录执行 python derive_portrait.py portrait_v2 inset，再执行 python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations。完整回包/raw可确定复现技术派生；生成模型再调用不保证同图。

74×100 RGBA、≤32临时可见色、二值alpha仅是技术出口。imagegen实质重绘加等比NEAREST containment、无抖动量化与alpha阈值是派生候选，不是原生逐像素终稿。inset不修复raw裁切或五官；未修改旧图、角色卡或代码，未集成/运行验证，未commit/push。
