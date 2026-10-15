# 呼蕾 HURE：暂缓，不计成功

最终作者manifest：`selected_portrait=null`，`selected_sha256=null`，状态`held_composition_scale_eye_sclera`。独立QA状态`held_composition_scale_and_eye_sclera`。本批不提供第四张通过头像，不在通过画廊显示呼蕾；只在看板列出暂缓原因。

核心问题是构图缩小与亮眼白。V2原图1216×1293，74×100标准等比NN后alpha bbox[3,16,74,85]，头领仅69px高；宽侧髻压低脸占比。保全主体而只裁透明空白时，1159×1137包围框受74px宽约束，最大约73px高，仍未达到当前大脸竖幅目标。双眼白仍亮、神态偏忧。

早期切边怀疑已经纠正：灰底实际看源发髻轮廓闭合。V1/V2在alpha≥128下右侧真实余量为6/7源px，最右列最大alpha仅1/4。74宽NN后触右边属于窄余量问题，不是已证实真实裁断。没有用透明padding声称修好轮廓，没有裁主体、补画或拉伸。

源包B原样保留两版raw、完整回包、prompt实际参数、全部候选与预览、来源SHA、失败历史和作者QA；两包保留独立QA完整证据、灰底图、来源裁定及复现产物。技术复现通过不等于视觉验收。未回选V1，每人两份成功生图已用完，不追加第三份。

Held证据：`hure/candidates/portrait_v2_74x100_candidate.png`
SHA256：`497f9a849278b3c88bb1ce5c2f9e337934d6c35cd22d5dae90817369bcb625b0`

最终结论见独立QA `QA_summary.json`、`selection_lock.json`及`FINAL_REVIEW.md`。不计入本批3人或累计成功人数。
