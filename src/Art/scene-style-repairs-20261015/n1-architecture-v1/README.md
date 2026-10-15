# N1 墙面与暗渠边缘 0.3.14

接续 0.3.13 的普通模式实机图：薄石条让钟房、暗渠缺少建筑差异，暗渠旧 backing 水纹碎片沿墙外露出。本批使用内置 image_gen 生成木构墙面和潮湿石墙，原图见 `raw/`，完整提示词/参考用途见 [prompts-and-provenance.json](prompts-and-provenance.json)。参考都是本项目已有原创生成素材或其合成预览；不拷贝商业图集。

`tools/Export-N1Architecture.py` 在 `Export-N1SurfaceRepair.py` 后运行：按 `layout.json` 的透明边界裁取，最近邻缩到 312×52，量化 DEN-N1-128，作为可重复的建筑墙段。木厅、石廊和暗渠使用各自材料；北墙高 52，前沿 13，侧柱 9 像素，最终 alpha 裁在旧地面 mask 之外。暗渠 blocked backing 改为不带水纹碎片的统一深色。

地面像素不变，不新增家具/碰撞/交互，不修改门坐标、NPC、剧情锁、奖励或保存代码。原有 N1 51 张 HD2D 集合中的背景层更新，生产 PNG 继续内嵌 `.sml`；不增加绝对路径依赖。几何/字节检查不能证明墙体风格完成，须用人物同框和普通门口实机图另行观察。

部署与运行记录见 `research/art-n1-architecture-0314-20261015.md`。
