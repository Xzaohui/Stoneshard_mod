# 卡蕾·棚 / DEN-NPC-KAR：本轮暂挂

状态：held_source_clipping_and_style。没有获选肖像，manifest 的 selected_portrait 和 selected_sha256 均为 null。两次内置 imagegen 实质重绘已用完，不做第三次。

v2仅作暂挂证据：`candidates/portrait_v2_74x100_candidate.png`，SHA256 `c4e4e2a516d297ee4d4a2e665875a636dd7f8cc0ffb4e0fdf35dc103c843c1c5`。原始v2右侧砖红头巾实体触画布，边界y606–687连续82个alpha≥128像素，触边部位是头巾外缘，巾尾本身尚闭合，不能靠缩小加边伪称修复；v1原始轮廓完整，但亮大眼白、长裸颈及宽领仍未通过风格门槛，不能当合格备用稿。

保留两版完整提示参数、完整工具回包、原始图、74×100派生、1x/4x/8x整数预览、来源快照与SHA、独立反馈、作者QA和原图边界审计。色数≤32、二值alpha是临时技术上限，不是原生逐像素终稿、装备兼容或游戏运行验收。没有脚本画脸、没有改旧资产/人物卡/代码，没有commit或push。

复现技术派生：`python derive_portrait.py portrait_v1`、`python derive_portrait.py portrait_v2`。重建清单：`python finalize_manifest.py portrait_v2 held_source_clipping_and_style`。原始PNG可从完整工具回包image_url逐字节解码，生图重跑不保证相同图。
