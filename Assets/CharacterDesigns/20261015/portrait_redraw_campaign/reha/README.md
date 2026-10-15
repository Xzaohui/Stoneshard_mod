# 雷哈 / SKO-S02-NPC 肖像重绘保留证据（held）

没有可交付选稿。`candidates/portrait_v2_inset_74x100_candidate.png`仅保留为失败修订证据；v1也不回退为通过。独立视觉QA确认v2源图右发卷触边截断：raw1078×1459，x1077、y531–546共16个A≥128像素，max alpha254；A>5和A≥128包围框均到右界1078。技术inset/padding不能补回源发轮廓。

v2短颈窄领与银灰发须大块有改善，保五十多岁父亲、棕外绿内衣色，但内抬苦情眉/偏亮眼白仍存。两次内置imagegen预算耗尽，不做第三稿。

证据候选74×100 RGBA、32可见临时色、alpha仅0/255，只证明技术格式合规。全raw等比NEAREST缩入72×98、无抖动MAXCOVERAGE限色、alpha128阈值都是技术派生；不脚本补发、不掩盖裁切，不是原生逐像素终稿。

完整prompt/实际参数、完整回包、未改raw、源快照与SHA、1x/8x整数NN/三背景预览齐全。复现：`python derive_portrait.py portrait_v2 inset`。清单刷新：`python finalize_manifest.py portrait_v2_inset held_source_clipping`。

旧图卡代码和冻结索引未改，未提交推送，未游戏集成或验收。
