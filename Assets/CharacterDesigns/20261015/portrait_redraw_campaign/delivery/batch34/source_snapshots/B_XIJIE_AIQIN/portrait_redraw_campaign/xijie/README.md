# xijie 头像重绘候选

选稿：candidates/portrait_v2_inset_74x100_candidate.png，独立QA已选定为带限制候选，见qa/independent_review_acceptance.json。两份成功内置imagegen图：初稿+唯一必要修订，不第三次。v2之前两次实参校验失败未产出图（相对路径、参考图超5），失败实参和原始错误另存，可与两份完整成功回包区分。

原始图在raw，完整回包在tool_returns，完整prompt和真实实参在prompts。qa/author_visual_review.json记录改善与保留问题；集中QA反馈在qa/independent_v1_feedback.json。

选稿为74×100 RGBA，32个可见临时色，alpha仅0/255。同一v2原始整张画布等比NEAREST置入72×98框再居中，不裁切、不改脸形、不脚本绘脸；MAXCOVERAGE无抖动量化与alpha128阈值均为技术派生，不是原生逐像素终稿。原始耳、发顶、辫端确有余量，containment仅增加输出画布余量，不代表修补裁断。各阈值实测见qa/portrait_v2_raw_margins.json。

源卡、母图、母图QA/manifest、四核心及剧情快照/SHA在sources。现卡衣着更新优先口径已明确写入spec_lock和source_manifest，不静默跟随过期旧衣。1x与整数8x预览、三背景1x/4x页在previews。

复现：python derive_portrait.py portrait_v2 inset。清单刷新：python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations。

保留限制：眼白仍亮、发束平行细纹偏多、皮肤仍有细小阴影。

旧图、卡、代码不变，未提交/推送，未游戏集成或运行验收。
