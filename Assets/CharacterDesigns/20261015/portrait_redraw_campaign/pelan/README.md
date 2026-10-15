# 佩兰（BRY-NPC-PELAN）头像重绘候选

2026-10-15。属于全体头像重绘 batch08，单人独立目录。

## 当前状态

独立视觉QA终选 portrait_v2，candidate_pass_with_notes。首稿与一次必要修订已完成，生图冻结，不启第三稿。

终选：candidates/portrait_v2_74x100_candidate.png；预览：previews/portrait_v2_1x_8x.png。

保留非阻断备注：头发仍有条束。仍有少量明亮眼缝。颈还可再压。

## 证据与方法

- 精确当前人物卡、母版与四核心风格图快照在 sources/，原始路径、SHA在 source_manifest.json。
- 原始 imagegen prompt 和全部调用参数在 prompts/；完整工具返回在 tool_returns/，raw/保留完整生成图片。
- candidates/ 为74×100衍生候选，previews/为1×及整数8×最近邻预览。
- derive_portrait.py从工具返回原样恢复raw，整幅最近邻缩放，alpha阈值128二值化，MAXCOVERAGE≤32色无抖动量化。没有手绘或算法补画人物几何。
- 色数是本批临时上限；计数通过不等于色阶设计或审美已获终审。
- 这是 imagegen实际重绘后的NN/量化衍生概念候选，非原生74×100逐像素创作，未接入/验证游戏。
- 不改旧母版、人物卡或代码；不提交或push。

## 复现

python Assets/CharacterDesigns/20261015/portrait_redraw_campaign/pelan/derive_portrait.py Assets/CharacterDesigns/20261015/portrait_redraw_campaign/pelan portrait_v2

机械派生可复现，imagegen原始生成不承诺像素级复现。

## 调用边界

成功产图两次（v1/v2）。v2曾用6张参考图被输入校验拒绝，未产图；移除多余旧母版输入，保留v1编辑目标与四核心风格共5图后成功。拒绝参数和错误已保存在 prompts/portrait_v2_rejected_six_references.json 与 qa/v2_validation_retry.json，不把失败调用藏成额外图稿。
