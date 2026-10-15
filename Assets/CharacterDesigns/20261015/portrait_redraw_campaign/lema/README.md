# 肖像重绘候选封档

当前暂定 portrait_v2，状态 awaiting_independent_qa：已按 batch39 集中反馈完成唯一必要修订；封档时尚未收到独立 QA 的最终采用/保留结论。每人两份成功生图已全部收回，无运行中的调用，不再生成第三次。

完整生图实参见 prompts/portrait_v1.json 与 portrait_v2.json；完整原始回包见 tool_returns/，raw 为回包原样解码。源卡、身份母图、母 QA、剧情与四核心参考快照及 SHA 见 sources/。

74×100 输出由整画布等比 NEAREST 缩放、alpha≥128二值化、MAXCOVERAGE ≤32色无抖动产生；仅技术派生候选，不是原生逐像素终稿，不代表游戏接入。预览含1×和4×/8×整数倍及三底。作者保留问题见 qa/author_visual_review.json。

复现：python derive_portrait.py portrait_v1；python derive_portrait.py portrait_v2；python finalize_manifest.py portrait_v2 awaiting_independent_qa。

旧图、卡、代码和冻结索引均未改；本作者未提交或推送。
