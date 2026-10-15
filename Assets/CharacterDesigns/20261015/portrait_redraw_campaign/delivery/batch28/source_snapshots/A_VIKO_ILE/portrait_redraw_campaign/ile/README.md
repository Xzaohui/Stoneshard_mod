# 伊蕾 肖像重绘候选

独立 QA28 已选 portrait_v2_inset，冻结为 deliverable_candidate_with_notes。每人两张成功 image_gen 实质稿，不再生成第三稿。选稿：candidates/portrait_v2_inset_74x100_candidate.png。

技术导出为整幅源图等比 NEAREST 适配72×98再置于74×100，alpha≥128二值化、MAXCOVERAGE至多32临时色、无抖动。该inset只避免74网格采样触边；不修缺发、不是额外生图。未脚本绘脸或局部变形。

验收限制：眼白仍偏亮，发束细节尚多，伊蕾头占略小。v2在alpha≥16四边均无触边；仍有极低透明边缘点（薇柯alpha≥5为1，伊蕾为20），不能声称全alpha无触边。右侧实质余量很小，未达到提示词4%目标。伊蕾v1的41个实心右触边已由v2实质重画修复。原始源图不变；此为可交付派生候选，并非原生逐像素终稿或游戏已接入验收。

prompts保存完整成功调用实参/提示词；tool_returns保存完整工具回包；raw为返回PNG逐字节副本。sources包含当前卡、母图/QA、四核心及剧情快照与SHA；qa保存指标、来源复核、独立反馈与验收。previews包含1x和整数NN预览。

复现：python derive_portrait.py portrait_v2 inset；python finalize_manifest.py portrait_v2_inset deliverable_candidate_with_notes。旧素材、人物卡、代码、冻结索引均不变，未commit/push。
