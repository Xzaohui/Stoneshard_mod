# 贝洛 肖像重绘候选

选定：candidates/portrait_v2_74x100_candidate.png

- 独立QA结论：deliverable_candidate_with_notes。
- 黑短发冠已收，二十多岁无须成年脸和石板灰领成立；眼白仍偏亮、颈仍略长、顶空15像素使整体头占偏小。源发耳完整，无实质裁断。
- 74×100、32个临时可见色、二值alpha；四边源图实心像素为0。
- 实际image_gen生成v1与唯一v2各一次，之后不第三次。一项6参考图请求在参数层被拒绝，未生成图像；失败实参和原错误保存在prompts/及tool_returns/。
- raw是完整原回包字节解码，原始母图与源卡保留；来源SHA见sources/source_manifest.json，终检见qa/source_hash_recheck.json。
- 1x预览：previews/portrait_v2_1x_backgrounds.png；整数放大：previews/portrait_v2_8x.png。

这是实质image_gen重绘后的整画布等比NEAREST containment、alpha阈值128及无抖动32色量化派生候选。没有裁剪、脚本绘脸或几何补画。临时色数合格不等于原生像素终稿；未集成游戏或完成运行验收。

复现：
python derive_portrait.py portrait_v2
python finalize_manifest.py portrait_v2 selected_candidate_with_limitations

完整生成提示词和实参在prompts/，完整原始回包在tool_returns/，逐版raw、技术指标、独立反馈和来源快照均保留。
