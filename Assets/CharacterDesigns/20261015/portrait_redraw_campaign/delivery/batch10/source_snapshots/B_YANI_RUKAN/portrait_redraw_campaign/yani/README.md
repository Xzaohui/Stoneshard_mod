# 雅尼 紧脸头像重绘候选

选稿：candidates/portrait_v2_containment_mediancut_74x100_candidate.png
SHA256：5915dc8bf7adebb813844148392b296e96da1c21213154d8a93b57fb54b599dc
状态：独立视觉 QA 选定的候选，等待批次总哈希审计；不等于用户审美终审、原生逐像素成品或游戏内运行验收。

## 实际制作与复现

每人实际使用 built-in imagegen 一次初稿和一次针对性修订。完整精确 prompt、工具参数、原始 tool return、raw、来源 SHA 和 1×/整数 8×预览均保留。没有第3次生图。

最终技术导出从 v2 raw 全画布按原比例 fit 进 72×98 像素边界，取整数尺寸 72×97，Pillow NEAREST 缩放后以 (1,1) 居中放入 74×100 透明画布；alpha 阈值128，MEDIANCUT 无抖动，最终31可见色。它是机械派生，不是原生像素绘制。v1、v2直接导出和MAXCOVERAGE对照全部保留。

运行 python derive_portrait.py；python export_maxcoverage.py portrait_v1；python export_maxcoverage.py portrait_v2；python export_containment.py portrait_v2；python export_containment.py portrait_v2 MEDIANCUT；python finalize_manifest.py portrait_v2_containment_mediancut。生成模型无可用seed控制，不保证重新生成一致；技术导出已逐字节复现。

## 已知限制

- MEDIANCUT收暗亮白眼块，但面部/灰须层次偏平，窄领衣色向暖肤色合并。
- raw 的 alpha≥128 实体不触最外左右列，但边距小于1目标逻辑像素，直接NN缩小会贴目标边。没有依据断言raw已经裁发梢；原轮廓完整性也未获独立证明。
- containment只补透明画布边，没有补画、恢复发梢或改变角色几何；不把技术留边冒称原raw完全安全。
- 身体道具、姿态和其他裁幅外细节不由此头像证明。具体身份锁见 spec_lock.md，最终自审见 qa/visual_self_review.json，独立反馈见 qa/independent_feedback_record.json。

只在此新目录新增，旧图、人物卡与游戏代码未修改；未commit/push、未接入游戏。
