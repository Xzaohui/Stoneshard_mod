# 艾蕾 / DEN-NPC-ELE：带限制肖像候选

独立QA选 `candidates/portrait_v2_inset_74x100_candidate.png`，状态 candidate_with_limits。SHA256：`f0814e54d8b13e363a89496df7eda9b8a9f27d14db1b3570b853f15999dba64c`。两次内置imagegen实质重绘，最终稿由v2原图整体等比NN缩入72×98容框，再置于74×100透明画布，无局部改脸或补画。32可见色，二值alpha，目标实心bbox(3,5,73,96)。

二十岁上下成年女性、晒健康肤、紧棕辫与独立平嘴神态成立；赭内衣、浅米窄巾和灰蓝旧围裙窄边保留。源辫轮廓闭合，四边实体为0；但原图右余仅1源像素，不能说已修成宽裕源留白，技术inset只有1px目标右余。

已知限制：浅眼点、部分鼻颧碎块仍在，裸颈仍有、发冠偏满；未达四核心原生逐像素控制。色数/尺寸/alpha通过只代表技术格式，既不是原生像素终稿，也不是装备兼容、引擎整合或运行验收。

保留v1/v2完整提示参数、完整工具回包、原始图、派生候选、1x/4x/8x整数预览、来源快照与SHA、源边界审计、作者QA和独立反馈。没有脚本画脸，没有改旧图/卡/代码，没有commit/push。

复现技术派生：`python derive_portrait.py portrait_v1`、`python derive_portrait.py portrait_v2`、`python derive_portrait.py portrait_v2 inset`。重建清单：`python finalize_manifest.py portrait_v2_inset candidate_with_limits`。原始PNG可从完整工具回包image_url逐字节解码；生图重跑不保证相同图。
