# 博赫·冷 肖像重绘候选

选择：`candidates/portrait_v2_inset_74x100_candidate.png`。

已用内置imagegen两次（首稿 + QA集中反馈后的唯一修订）。独立QA接受为带限制派生候选，非原生终稿；不再生成第三次。

候选74×100 RGBA，32个可见临时色、alpha仅0/255。v2同一raw整画布等比NEAREST缩入72×98再居中；无裁切、无几何或脸部脚本重画。alpha128阈值、MAXCOVERAGE无抖动限色与技术inset均明示为派生，不作为原生像素批准。

完整prompt实参、toolreturn（含完整图像数据）、字节一致raw、源卡/母图/母QA/母manifest/四核心/剧情快照与SHA均保留。`qa/generation_audit.json`记实际输入图SHA，`qa/raw_edge_audit.json`审原始边缘，不用padding掩盖裁切。

1x/8x：`previews/portrait_v2_inset_1x.png`、`previews/portrait_v2_inset_8x.png`，另附1x与整数NN4x三底预览。v1完整保留，v1/v2均可复现。

复现：`python derive_portrait.py portrait_v2 inset`；清单：`python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`。

视觉改善与残余见`qa/author_visual_review.json`；独立意见原文见`qa/independent_review_acceptance.json`。原图、角色卡、代码与全局冻结索引未改，无commit/push。未集成、未游戏运行验收。
