# Batch 20 独立终审

## 结论

3 人可交付概念候选，1 人 held。所有图像均为 imagegen 实质重绘后技术派生，不是原生逐像素终稿；未入游戏、未做运行或装备兼容验证。

- 卢绫：通过并带限制，锁 portrait_v2_safe。成熟宽颊厚颌、浅巾与深褂赭衬对齐，短颈改善。源巾耳轮廓完整，但 raw 最窄右余量仅 3px；safe 只增加技术留边。眼白仍亮、眉间折仍强，发巾细条偏多。
- 娜娅：held_source_clipping，无交付选定图。v2 左源发束 y523–534 连续 12 个 alpha≥128 像素与源边相交，放大可见横向平截，轮廓未闭合。inset 不能修补缺失源轮廓。v1 仅历史记录，不回选、不计成功，不作第三次生成。v2 虽缩颈，但亮眼白、忧眉和团块双辫仍需记录。
- 诺妲：通过并带限制，锁 portrait_v2 full。40+ 成熟宽颊、低髻、深灰窄领与谨慎抿嘴成立，髻耳轮廓完整，短颈改善。仍有亮眼白、微忧内眉与细发纹。
- 赛洛：通过并带限制，锁 portrait_v2 full。20 岁上下成年清瘦、直鼻方颌、深棕短发、暗绿领与棕灰拼布成立。发尖耳轮廓完整、短颈改善，仍有偏紧眉、亮眼白和漫画感。不能幼化或与埃文并为同人。

## 来源与视觉证据

已阅读根/设计 AGENTS、四人 roster 条目、当前人物卡、认可身份母图的历史 QA/manifest 及相关台词/演出约束；实际查看四人完整身份母图和 Mara/Iwo/Leiya/Tore 四核心。现卡增补导致历史卡 SHA 不同，不等于身份冲突；当前卡明确年龄、深色罩衣/外褂、双绕辫和错色拼布优先于旧概念服饰提案。独立源快照与逐项 SHA 在 preflight_source_checks.json、source_snapshots/。

实际查看各人的 v1/v2 raw、目标 8x，以及有输出的 inset/safe 技术备选；结论以完整源轮廓和 74×100 的可读性共同判断。娜娅左源边 4x NN 放大与精确像素坐标见 naya_source_boundary_evidence.json 和 naya_v2_left_boundary_4x.png。

## 独立技术核验

- 原始工具返回的 base64 解码字节逐一等于 raw PNG；每人恰好 2 张实质生成图，共 8 张。参数超出 5 参考图的校验拒绝未生成图，作者记录单列，不算第三张。
- 每份候选 74×100、可见 RGB≤32 色、alpha 仅 0/255，透明像素 RGB 归零。1x 原样、8x 和多底 4x 为整数 NN。
- 作者脚本先全文通读并锁定 SHA，再只在本 QA/replay 目录执行。raw、工具返回和脚本复制为只读来源；派生候选、所有预览、metrics JSON 逐字节复现一致。
- 另有独立实现重建各候选 PNG，逐像素及 PNG 文件字节均一致。作者四目录 manifest 库存与 SHA 全文件核验完整，无漏项或不匹配。
- 技术完整性通过不覆盖视觉 hold：娜娅导出的格式与字节复现正确，但源轮廓不完整，仍不交付。

统计：{"source_copies_checked": 49, "raw_tool_payloads_checked": 8, "candidate_exports_checked": 11, "replay_artifacts_byte_identical": 66, "manifest_inventory_checks": 198, "source_SHA_checks": 202}。

## 冻结与交付清单

- FINAL_SELECTION.json：逐人唯一选定版本、完整 SHA、held 排除与残余限制
- FINAL_REVIEW.md：本终审完整口径
- frozen_technical_audit.json、derivation_replay.json、frozen_verification.json：最终技术证据
- v1_visual_feedback.json、v2_visual_reviews.json：每人唯一一次集中反馈与终审
- preflight_source_checks.json、source_snapshots/：独立来源快照
- selected_candidates_1x_4x.png、v1_v2_comparison_4x.png、comparison_manifest.json：整数 NN 审核板（娜娅明确标 held）
- naya_source_boundary_evidence.json、naya_v2_left_boundary_4x.png：held 原因证据
- QA_FILE_INVENTORY.json、SHA256SUMS.txt：本 QA 全文件库存与哈希；库存不自哈希，SHA 清单不自哈希以避免循环

只写 independent_qa/batch20；未改源卡、旧母图、代码或作者资产，未 commit/push。过程中的 initial/inflight/prefreeze 文件是未冻结时的时点证据，最终状态以 frozen_* 为准。
