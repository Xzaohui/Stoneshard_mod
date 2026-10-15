# 罗莎·藤 肖像重绘候选

内置 image_gen 实质重绘初稿加唯一一次集中修订已完成，独立QA已选为selected_candidate_with_limitations，终审反馈见qa/independent_review_acceptance.json。

- 终审选定候选：candidates/portrait_v2_74x100_candidate.png
- 原始图：raw/portrait_v1_raw_imagegen.png、raw/portrait_v2_raw_imagegen.png，与各完整tool_returns回包PNG字节一致。
- 精确实参与完整提示：prompts/portrait_v1.json、portrait_v2.json及同名txt。
- 74×100一倍、8倍NN、三底色一倍和4倍预览均在previews。
- 来源/当前卡更新与身份锁：sources/source_manifest.json、spec_lock.md。
- 四核心8倍NN输入的复现：python prepare_revision_refs.py；不改变参考像素。
- v1独立反馈：qa/independent_v1_feedback.json；作者v2目视与源边界限制：qa/author_visual_review.json。
- 技术派生为整画布等比NEAREST containment、alpha>=128、MAXCOVERAGE最多32可见色且无抖动；没有脚本绘脸或几何修补。
- 罗莎v2源alpha>=128左右余量21/26px，完整发耳；选普通v2，inset仅保留对照。
- 本次是可审技术派生候选，不是原生像素终稿、像素制作批准或游戏运行验收。旧素材、人物卡、代码与冻结总索引均未改；无commit/push。

复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python derive_portrait.py portrait_v2 inset；python finalize_manifest.py portrait_v2 selected_candidate_with_limitations。

终审共同保留：局部眼亮点与发纹略碎；技术达标不等于原生像素终稿。
