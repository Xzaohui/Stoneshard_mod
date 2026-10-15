# 缇安：非战斗基础动作

两张独立全身静态姿态概念，不构成先后或连续动画，未接入游戏。

- A1 · 将原钥匙半收入围裙袋：tian_A1_stow_key_at_pocket_v1
- A2 · 抬左肘向内查看空碗：tian_A2_tilt_bowl_toward_self_v1

## 来源与检查

- sources/files 保留本轮实际使用的母图原稿、透明母图、旧表情对照板、人物卡、台本边界、既有QA和风格来源的原字节快照。
- source_brief.json 是本人的动作规划快照；sources/third_new_character_actions_brief.json 保留整批规划原件，里面的 planning 状态是当时历史，不代表此包完成状态。
- prompts 每次先保存逐字提示词及实际工具参数，再调用内置 imagegen。
- raw 保留所有首稿和修订原图、完整工具返回（含 image_url）与参数/文件哈希。
- exports 保留所有透明处理结果，包括未选稿；最终选中只看 FINAL_STATUS.json。
- review 包含每稿浅深底、作者检查、独立视觉与板式QA、蕾因接点失败和修订证据。
- 处理仅为原A<=8的近零alpha背景RGBA清零；原A>8实体像素逐通道不变。provenance旧字段名 alpha_only_cleanup_threshold 仅指阈值，不声称RGB全图未动。没有脚本绘制人体、拉伸或强量化。
- 母图与旧表情只作参照，不计本批新增动作。

## 稿次

缇安A1/A2各一首稿，无修订。

## 限制

不新增道具、授权、交换、结案或剧情事实。原人物卡/台本未修改；未制作GIF、过渡帧、原生方向/锚点/装备兼容，未部署、未验证runtime。
