# 锉珥：非战斗基础动作 v1

计划2项，目前仅A2选稿通过，A1未通过。首稿和唯一硬错修订全部保留。

## 选稿

- A2：屈膝用闭钳轻敲轨顶，唯一选稿位于 selected/cuoer_A2_crouch_tap_rail_transparent.png。
- A1：未通过，不计入成品。A1唯一修订后仍是新木握柄、直鼻钳口，原母图圆弧裸金属短钳造型未恢复。修订预算已用完，不再追加生成。

## 包含内容

- raw：全部4张内置imagegen原始输出，未改。
- candidate_previews：全部4张仅作alpha清理的候选预览；此目录不表示获选。
- selected：仅A2通过透明PNG，不含失败A1。
- review：每个候选的浅/深正确RGBA合成板。
- receipts：每次调用前保存的完整参数JSON和工具原始完整返回JSON（含原始图像data URL），互不覆盖。
- prompts：首稿、修订文字及从完整调用JSON解出的逐字实际提交文本。精确SHA见generation-log.json。
- sources：母图raw/透明、当前卡、关联来源快照与哈希。
- QA-author、QA-independent、alpha_report、manifest与FINAL_STATUS：验收与冻结记录。

人体、手和道具均由内置imagegen生成；脚本仅alpha≤8清零，透明像素隐藏RGB清零，等比nearest排版和正确RGBA合成；不画身体，不拉伸。

仅独立静态关键姿态；起止文字是未来动作参考，不代表已画连续动画、循环、GIF或游戏运行验证。动作不宣布任务完成、合格、许可、薪酬、修复或新剧情事实。
