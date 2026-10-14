# 俉珥与库奇：基础动作完整源包

本批只新增两位既有人物各2张全身静态动作，共4张；4次内置imagegen首稿，0次修订。4张逐稿独审均通过。母图和既有表情仅作身份、体态与动作去重参照，不计本批新图。

- 俉珥 FX-CV3：右手横胸拂平左上袖；屈膝半蹲右掌扶腿
- 库奇 FX-BUR：右手握稳肩前钩杆背带；左掌低托腰间旧绳卷

## 内容

wuer_kuqi_mother_actions_light.png 与 dark.png 为中文联合母图对照板。board_layout.json 记录原图SHA与精确坐标；只用完整画布等比nearest显示。
selected_files.json 指向四张通过PNG。两个人物noncombat_basics_v1目录保留原始raw、完整工具返回含image_url数据、逐字prompt和实际参数、唯一母图SHA、透明清理、真浅深复合、作者与独立QA及生成记录。
planning_sources完整保留本批规划来源快照和SHA；现行卡和旧冻结图均不改动。俉珥仅继承母图短截状指端，不推定具体哪指。库奇原钩杆保持斜背，绳圈仍挂原腰处。

每份ZIP是可单独打开的普通ZIP；全部分包合在一起才是完整源档。包内PACKAGE_CONTENTS.json与包外package_manifest.json记录成员SHA。所有尝试已保留，本组没有废稿或安全阻断。

本批为可逆美术提案，不是连续动画、原版像素网格、装备兼容、碰撞或游戏运行验收。未改游戏、存档或剧情，未Git、未上传。最终冻结状态以作者sole-writer FINAL_STATUS及外部包审计为准。
