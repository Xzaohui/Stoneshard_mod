# 瑟拉对话动作 · v1

已制作两张新姿态，批准G在序列首末复用。独立复核已通过关键姿态概念（带注明）；已整理最终包，上传与用户送达由主线程另记。

- sela_dialogue_review_zh.png：中文四阶段对照板
- sela_dialogue_once.gif：单次四关键帧预览，无循环扩展
- raw/：两张builtin imagegen原字节原稿
- 01_rest_G.png / 04_return_G.png：批准G原字节复用
- 02_open_palm.png / 03_serious_confirm.png：新姿态原字节副本
- *_aligned.png：共同0.50最近邻尺度、鞋底620、鞋中心280的透明展示图
- qa_white_background.png / qa_black_background.png：双底检视
- prompts/：完整提示词；sourcehash.json、manifest.json、QA-author.json：来源、操作、哈希与检查

所有身体像素来自builtin imagegen，build_review.py只排版。alpha>=128用于实体bbox定位，框内alpha保留。原稿透明背景有低alpha噪点；展示裁切不改变原稿。各图原生1118×1407，不是游戏原生精灵规格。高度存在约2.3%以内生成漂移。

瑟拉仅有限夜渡租船人。图中确认仅指对话神态；不写付款、签字、用途授权或任务完成。金环功能未设定。
