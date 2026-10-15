# 呼蕾 肖像重绘

状态：held_composition_scale_eye_sclera

呼蕾维持held，准确gate为composition/scale + eye_sclera，不是source_clipping；灰底闭合及6/7px源边证据已复核。

无已选通过肖像；保留v2为held best-effort证据并排除交付通过画廊。

实际生成：built-in image_gen，每人v1 + 一次必要v2；完整实参在prompts/portrait_v*.json，完整prompt在同名.txt，完整返回（含原图字节data URL）在tool_returns，raw为返回解码的逐字节同一原图。工具未暴露模型/seed/quality/size控制，未伪造。

复现：在本目录运行 python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python finalize_manifest.py。前两者为确定性技术导出；复跑SHA一致见qa/reproducibility.json。不能承诺重新生图字节可复现。

预览：previews/portrait_v2_1x.png、portrait_v2_8x.png、portrait_v2_1x_backgrounds.png及portrait_v2_4x_backgrounds.png，整数最近邻，无改脸。

来源：sources/source_manifest.json，源图母QA/最新卡与剧情均留SHA快照；qa/source_hash_recheck.json复核原件未变。限制与独立意见见qa/author_visual_review.json、qa/independent_review_acceptance.json。

- held：近方源画幅1216×1293，全幅等比74×100后主体仅69px高，上下空白明显，侧髻占宽抑制脸占比。
- 源有效右边余量极窄（v1 6px / v2 7px），目标NN触右边；实际灰底复核轮廓闭合，不称已证实裁断。
- 眼白仍亮，未达到小暗眼目标；眉仍带忧愁倾向，发纹较密。
- 两次生图上限已到，不再修订；不进入通过肖像画廊。
- imagegen原图的像素风不等于原生逐像素绘制；74×100、32临时色与二值alpha仅技术派生。
- 未替换母图、角色卡、代码或游戏资源；未commit/push。

勘误：v2真实prompt保留了初看时“裁边”的担忧，这是历史实参，不删改。后续alpha与灰底审查证明轮廓闭合；准确问题为源余量不足造成目标触边，加构图缩小和亮眼白，不认定源图已裁断。详见qa/raw_margin_audit.json。
