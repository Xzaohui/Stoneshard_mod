# 缇娜·染 肖像重绘候选

选稿：`candidates/portrait_v2_inset_74x100_candidate.png`，独立QA锁为带限制候选。成功生成两张（初稿＋一次必要修订），没有第三张。一次六参考参数提交被工具验证拒绝、没有图像；已保留失败实参与错误，随后同一v2改用五参考。完整成功回包、精确prompt实参、未改raw均存档。

最新卡二十多岁成人徒弟兼移居染工；保棕辫、方颌、直眉平嘴与蓝旧罩衣；闭嘴时不强制露笑时虎牙。v2 raw右透明余量11px，辫尾完整但接近右边。

74×100 RGBA，32个可见色，alpha仅0/255。色数仅临时工作上限。v2 inset从同一raw整画布等比NEAREST缩入72×98框后居中，再alpha128阈值与MAXCOVERAGE无抖动限色；不裁图、不脚本改脸、不拉伸、不补发耳。inset是技术留边，不能恢复不存在的源轮廓。不是原生逐像素终稿，未整合或实测游戏。

相较初稿，颈领缩短、鼻颧块面更明确；年龄及衣色成立。残余限制：眼白仍浅、发带细分较多，脸颈比例未完全达到四核心目标。

预览：`previews/portrait_v2_inset_1x.png`、`portrait_v2_inset_8x.png`及三背景1x/4x页。来源：sources下最新卡、母图、母QA、manifest、剧情、四核心风格参照及SHA。四核心均实看，仅提供风格。

复现：`python derive_portrait.py portrait_v2 inset`。清单：`python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`。v1/v2的full/inset及所有预览重跑逐字节一致，见`qa/author_reproduction_check.json`。

审查：`qa/author_visual_review.json`、`qa/independent_final_visual_review.json`及`qa/independent_review_acceptance.json`。完整清单与SHA见manifest和SHA256SUMS。原素材、卡、代码、冻结索引未改；未commit/push。
