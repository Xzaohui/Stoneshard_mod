# 布岚 / SKO-S01-NPC 肖像重绘候选

选择：`candidates/portrait_v2_inset_74x100_candidate.png`。独立视觉QA接受为带限制技术候选；两次内置 imagegen（初稿+唯一修订），完整prompt/实际参数、完整回包、未改raw、源快照与SHA齐全。

v2短颈、大脸、窄领、发须大色块明显改善；保四十多岁厚实脸、暗帽棕发灰须、棕工装赭内衫。仍有忧眉、偏亮眼白，眉虽变薄断续但炉烤稀疏感有限；源右10px/底11px主体余量窄。不得说原生风格已经验收。

74×100 RGBA、32可见临时色、二值alpha。全raw等比NEAREST缩入72×98框，无裁剪、无脚本绘脸；无抖动MAXCOVERAGE与alpha128阈值均为技术派生，不是原生逐像素终稿。1x、8x整数NN及三背景预览在previews。

复现：`python derive_portrait.py portrait_v2 inset`。清单刷新：`python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`。

两次预算已用尽，不做第三稿。不改旧图卡代码或冻结索引，不提交推送，未游戏集成/验收。
