# 雷哈 REHA：暂缓，不计成功

独立 QA 与作者最终 manifest 一致：`selected_portrait=null`，`status=held_source_clipping`。本批看板仅列暂缓原因，不展示雷哈为通过头像，不提供第四张单独通过候选附件。

V2 原始图为1078×1459；最右列 x=1077、y=531–546 有16个 alpha≥128 像素，最高254。右发卷撞画布真实截断。候选虽然使用72×98等比 NN inset居中到74×100产生透明留边，也不能补回原始发尖。V1同样未获本轮批准，不回选；每人两份成功生图已用完，不生成第三份。

源包 B 原样保留雷哈完整目录：两份 raw、生图完整回包、prompt实际参数、所有候选和预览、来源与 SHA、失败历史及作者 QA。两包独立 QA 中保留 `reha_v2_right_edge_evidence.png` 与 `reha_v2_edge_pixels.json`。独立重构及重放可复现失败候选，技术复现通过不构成视觉验收。

Held evidence：`reha/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`f00a999d4e4fad8774b45061f8b696cfd6168d79fefc81c62a5d4d9da20b5e6c`

完整冻结结论见独立 QA `FINAL_SELECTION.json` 与 `FINAL_REVIEW.md`。不计入本批3人，不计入累计93人。
