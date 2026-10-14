# 蔻珥 · 日常基础动作原始源

本目录保存2张独立全身关键姿态。内置imagegen首稿2次，定向硬错修订1次。只保留逐姿通过独审的图作为selected，见FINAL_STATUS.json和manifest.json。

- 双手低提原木桶：kouer_A1_low_lift_lime_bucket_v1
- 俯身扶稳落地桶沿：kouer_A2_grounded_bucket_rim_steady_v2

raw/保存所有原始PNG及完整工具返回（含image_url原图payload），prompts/保存调用前逐字提示词与实参，sources/保存来源原字节、SHA和实际处理脚本，review/保存作者及独立QA、真实浅深合成、母图对照合板与布局证据。

仅alpha≤8透明清理；alpha>8的原始像素逐字节保持。合板用同一0.47比例nearest缩放，不拉伸、不脚本绘人体。透明区域隐藏RGB不作为硬错。

蔻珥A2 v1出现中央第三鞋，已保留失败原稿与完整回执；唯一v2定向去除额外鞋后通过。v1不得作为selected，不再追加v3。

人物身份与道具以现行母图为锚。这是非战斗日常动作概念，不构成连续动画、不代表医疗演示或剧情结果，也未部署到游戏。

归档pixel skill已读取；其中引用的references/executor-pixel.md实际上不存在，没有杜撰该文件。当前生产沿用STYLE_DIRECTION及持续绘制授权。
