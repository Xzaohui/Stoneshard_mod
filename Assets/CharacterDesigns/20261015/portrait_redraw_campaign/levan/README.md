# levan 头像重绘候选

独立QA以带限制的候选口径通过，选定portrait_v2；初稿v1完整保留。每人内建image_gen两次（初稿+独立QA后唯一一次修订），不再生图。

- 候选：candidates/portrait_v2_74x100_candidate.png
- SHA256：62c19f78afd75315ae5be7b79e804995844fa8ccc971c424e054593db559f0be
- 74×100、32可见色、alpha仅0/255；1x、8x整数NN及三底预览在previews。
- prompt/参数在prompts；完整工具返回在tool_returns；原始图原字节保存在raw，已与完整返回解码核对。
- 来源快照与原路径/SHA在sources/source_manifest.json，作者检查与源边界审计在qa。
- 实质绘制全部使用image_gen；技术导出仅整图等比NEAREST到74×100、32色MAXCOVERAGE无抖动量化、alpha阈值128；无裁剪或脚本画脸，无局部变形。
- 复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python finalize_manifest.py portrait_v2 pass_candidate_with_notes。重跑候选及全部预览已逐字节复现。
- 是技术派生候选，不是已批准原生像素终稿，未导入或运行游戏。旧素材、人物卡、代码未修改。

## 留存限制
- 唯一一次修订后，眼白变低平且压暗；裸颈明显缩短，锈衣领口提高，年轻成人净面与克制闭唇保住。
- 暗波发大块与鼻/颧骨色面可读，与四核心粗簇方向接近；仍有少量较亮眼白、两侧约1px余量，属于候选限制。
- 原始v2四边alpha>=128实色触边数均为0，没有真实裁边；未用padding或inset宣称修复。

## 独立QA结论

列梵v2已实际看raw/1x/8x：眼白收低压暗、裸颈缩短有效，二十多岁净面与克制闭唇保住，较v1更贴四核心。源raw alpha>=128 bbox=(15,71,1070,1419)，四边实色触边0；无真实裁边，不需加inset反复采样。可冻结当前v2候选，记左右约1px留边及仍有少量明眼白为候选限制，不再生图。
