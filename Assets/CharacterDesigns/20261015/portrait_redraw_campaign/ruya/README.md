# ruya portrait redraw

独立复审已选带限制 v2：candidates/portrait_v2_74x100_candidate.png。v1 保留。

- 两次实际 imagegen 生成（初稿＋唯一修订）。v2六参考实参在生成前被工具五张上限拒绝，失败实参与错误另存；移除冗余母图后使用v1＋四核心参考成功，无第三张生成。
- 身份母图、当前卡、母QA、剧情及四核心来源已实际核对并保留快照与SHA；最新卡衣色优先。
- 原始PNG与完整回包逐字节相同。源发耳/头巾完整，但左右余量仍窄，详见作者QA；不以padding冒称修复源图。
- 技术派生为整画布等比最近邻包含，二值alpha，MAXCOVERAGE≤32临时工作色，无抖动、无脚本绘脸。
- 1×、8×整数NN与三底色预览在 previews。
- 非原生像素终稿，未游戏集成或运行验收；不改旧母图/人物卡/代码/总索引，未commit/push。

复现：
1. python recover_raw.py portrait_v2
2. python derive_portrait.py portrait_v2
3. python finalize_manifest.py portrait_v2 selected_candidate_with_limitations

QA32确认直接选full v2，不加inset。左右余量偏紧但不是裁断；苏槿仍有颈稍长/头巾偏大的限制。
