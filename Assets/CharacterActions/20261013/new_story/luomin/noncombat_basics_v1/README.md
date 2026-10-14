# 洛珉：非战斗基础动作 v1

两张独立全身关键姿势，以已审母图保持身份与衣装。

- 低位稳提油灯：`selected/luomin_A1_lantern_low_hold.png`
- 俯身稳放油灯：`selected/luomin_A2_lower_lantern_to_ground.png`

## 制作记录

内置 imagegen 逐张重绘，真实 prompt 与提交参数先落盘，原始结果及全部返修保留。每姿势首稿加最多一次硬错修订。`generation-log.json`、`source_hashes.json` 与 `manifest.json` 提供来源、输入、输出 SHA。

选稿只将原图 alpha≤8 的像素清为 RGBA 0；alpha>8 像素逐字节不变。`prepare_review.py` 仅做真实 alpha 合成、文字标注与等比 nearest 排版，不绘制或扭曲人体。

本批不主张连续动画、剧情已执行、交付/支付/同意、装备兼容或游戏运行通过。最终独审与冻结状态见 `FINAL_STATUS.json`。
