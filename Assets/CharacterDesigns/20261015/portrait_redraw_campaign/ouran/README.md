# 欧岚 / MAE-NPC-OURAN 头像重绘候选

选择：`candidates/portrait_v2_inset_74x100_candidate.png`。两次内置 imagegen（初稿 + 一次必要修订），保留全部 raw、完整 tool return、prompt 与实际参数。

候选为 74×100 RGBA，32 个可见临时色，alpha 仅 0/255。`portrait_v2_inset` 从同一 v2 raw 整图等比 NEAREST 缩入72×98框后居中，不裁头发、不重绘像素、不改变面部几何；无抖动 MAXCOVERAGE 限色和 alpha128阈值均明示为技术派生。不是原生逐像素终稿，不代表游戏运行验收。

预览：`previews/portrait_v2_inset_1x.png`、`portrait_v2_inset_8x.png` 与三背景1x/4x页。四核心风格仅作风格，不作为身份。源卡、母版、母版QA、母版manifest与剧情快照见 sources，并记录SHA与来源。

复现：`python derive_portrait.py portrait_v2 inset`；清单刷新：`python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`。

审查：`qa/author_visual_review.json` 记录改善与残余；独立QA接受冻结为带限制候选，见 `qa/independent_review_acceptance.json`，最终哈希复核由批次汇总引用。原图、角色卡和代码未变，未提交/推送。
