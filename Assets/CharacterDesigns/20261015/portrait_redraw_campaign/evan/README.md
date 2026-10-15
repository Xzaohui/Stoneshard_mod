# evan 头像重绘候选

独立QA终选并冻结：`candidates/portrait_v2_74x100_candidate.png`。2次成功内置imagegen：初稿+唯一集中修订；禁止第三次生成。

候选74×100 RGBA，≤32临时可见色，alpha0/255。全raw等比NEAREST到74×100、MAXCOVERAGE无抖动32色、alpha128阈值只是技术派生，没有裁边或脚本重画面部，不是原生逐像素终稿。raw本身真实四边留白，详见qa/author_visual_review.json。

复现：python derive_portrait.py portrait_v2
清单：python finalize_manifest.py portrait_v2 pass_derived_candidate_with_notes

源卡、母图、母QA、剧情及四核心参考均快照且SHA登记。Evan按当前卡补低檐帽与早白鬓角，历史卡缺S89细描的差异有证据。完整prompt/参数/工具回包/raw与1x和整数NN预览保存。源图卡与代码未改，未commit/push，未接入游戏。

独立审查：`qa/independent_review_acceptance.json`。保留限制：仍带谨慎疲态、局部胡须纹略碎。
