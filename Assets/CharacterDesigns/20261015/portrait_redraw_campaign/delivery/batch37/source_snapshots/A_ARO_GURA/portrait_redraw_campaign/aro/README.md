# 艾萝·图 / HIG-NPC-ARO 肖像重绘候选

选择：`candidates/portrait_v2_74x100_candidate.png`，QA37接受为带限制候选。两次成功内置imagegen（初稿+唯一必要修订），原raw、完整回包、完整prompt实参均保留。一次6参考图参数预校验拒绝没有生成图，已记录，不计为第三张图。

74×100 RGBA、32个可见临时色、alpha只有0/255。ARO使用完整v2 raw等比NEAREST派生，发顶与耳侧完整，无裁切、无非等比拉伸。无抖动MAXCOVERAGE限色及alpha128阈值均仅技术派生，不是原生逐像素终稿，不代表游戏运行验收。

1x、8x整数最近邻预览和三背景1x/4x预览见previews；源卡、母图、母QA、母manifest、剧情与四核心风格见sources并带SHA。author_visual_review记录改善和残余。

复现：`python derive_portrait.py portrait_v2`；清单刷新：`python finalize_manifest.py portrait_v2 selected_candidate_with_limitations`。

旧图、卡、代码、冻结索引未改，不提交推送。停止生图，不做第三次。

独立QA残余：眉稍忧、颈稍长、发束仍平行。 原生像素与运行验收均未通过/未进行，不做相应声明。
