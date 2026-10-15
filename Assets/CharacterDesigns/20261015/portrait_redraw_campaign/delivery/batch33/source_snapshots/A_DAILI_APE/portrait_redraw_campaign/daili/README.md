# 岱里 / EED-S02-NPC

状态：selected_candidate_with_limitations。batch33独立审查带注选v2，已停止生图，每人仅两份成功图。

所选：`candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`b97465b3e5e64f50dc5839316e8fcf09cad880609dd4d4cd3f3f5b7c726f5f89`

v2眼袋/鼻唇/下颊已支持约60岁、颈明显缩短，1x眼白已压暗。raw alpha≥16右侧仍有3px、alpha≥128有4px真实间隙，轮廓完整；源alpha1散点接边不算真裁断。保留发巾仍稍占幅、颈尚有小段的限制。

74×100 RGBA、32临时色、alpha 0/255。完整原始回包与原样raw、两轮完整prompt/实参、源卡/母图/母QA/剧情/四核心快照、1x与整数NN预览、机器指标及审查记录全部保留。

技术流程：整张raw等比NEAREST包含至72×98盒，再居中置于74×100透明画布；alpha阈值128；MAXCOVERAGE至多32色且无抖动。没有脚本画脸、补发耳或拉伸几何。此为技术派生概念候选，不是原生逐像素终稿，不是运行验收。旧图、人物卡、代码和冻结索引未改，无commit/push。

复现：在本目录运行 `python derive_portrait.py portrait_v2 inset`；再运行 `python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`。四核心8x参照可由 `python make_style_previews.py` 重建。以上技术输出可确定性复现；重新调用imagegen不保证逐字节一致。

另保留一次6参照参数校验失败记录，失败未产图，成功图仍为两份。
