# 芮莎 / BRY-S02-NPC

选稿：candidates/portrait_v2_containment_74x100_candidate.png
SHA-256：9c02704cb60cb51ff67c2c4fcc4d2d3d532f553bf7517ee7659da9b806372564

本目录为全人物对白头像重绘新候选。保留原始生图、两个完整工具返回、准确参数、来源快照及SHA、首稿与唯一修订、两种技术量化对照和透明边导出。先实看现卡、旧母版与四核心风格；现卡年龄/收发/衣色优先。

方法：内置imagegen实质绘制；NN、二值alpha及≤32临时工作色是明示技术派生，不是原生逐像素作者稿。未集成或验证游戏运行，不覆盖旧素材。

重现：
python derive_portrait.py
python export_maxcoverage.py portrait_v1
python export_maxcoverage.py portrait_v2
python export_containment.py portrait_v2
python export_containment.py portrait_v2 MEDIANCUT
python finalize_manifest.py portrait_v2_containment

四边透明安全框只增加留边，不补画原图外内容。独立最终批次QA见manifest链接。

视觉备注：50岁、暗红头巾/橄榄衣与浅围裙边成立，但忧眉、亮眼白及细卷仍有；只称候选带备注通过，不称全部修复。
