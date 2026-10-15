# qilen 头像重绘候选

独立QA以带限制的候选口径通过，选定portrait_v2；初稿v1完整保留。每人内建image_gen两次（初稿+独立QA后唯一一次修订），不再生图。

- 候选：candidates/portrait_v2_74x100_candidate.png
- SHA256：c4f5799a547826db579cd55524605b29ad98cbf19384f17ca997a9620294bb01
- 74×100、32可见色、alpha仅0/255；1x、8x整数NN及三底预览在previews。
- prompt/参数在prompts；完整工具返回在tool_returns；原始图原字节保存在raw，已与完整返回解码核对。
- 来源快照与原路径/SHA在sources/source_manifest.json，作者检查与源边界审计在qa。
- 实质绘制全部使用image_gen；技术导出仅整图等比NEAREST到74×100、32色MAXCOVERAGE无抖动量化、alpha阈值128；无裁剪或脚本画脸，无局部变形。
- 复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python finalize_manifest.py portrait_v2 pass_candidate_with_notes。重跑候选及全部预览已逐字节复现。
- 是技术派生候选，不是已批准原生像素终稿，未导入或运行游戏。旧素材、人物卡、代码未修改。

## 留存限制
- 唯一一次修订后，绿领明显提高、裸颈缩短；宽下颊长圆脸、低宽鼻、米色包发巾与薄弧暖笑保住。
- 眼白收低，但仍有浅色眼白/反光和右侧1px级巾结余量，属于当前候选局限；未第三次生图。
- 原始v2四边alpha>=128实色触边数均为0，没有真实裁边；未用padding或inset宣称修复。

## 独立QA结论

绮伦v2终审视觉通过候选口径：高绿领显著收短裸颈，暖薄弧笑、宽下颊/长圆脸及40岁上下感仍在，眼已收低；源raw alpha>=128 bbox=(65,162,1071,1310)，四边实色触边0，头巾与耳形完整。冻结当前v2即可，不加inset、不再生图。保留眼内仍有少量亮点、右侧仅1目标px余量和头巾块面稍亮的限制。
