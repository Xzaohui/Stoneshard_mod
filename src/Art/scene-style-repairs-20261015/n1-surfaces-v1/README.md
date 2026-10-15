# N1 连续地面修复 0.3.13

针对 0.3.12 截图中地面重复、镜像碎屑、巨型木板接头与墙沿拼接，使用内置 image_gen 生成两张完整地面材质。完整提示词和参考用途见 [prompts-and-provenance.json](prompts-and-provenance.json)，原始输出保留在 [raw](raw/)。参考图也是此前本项目的原创生成素材；未导入商业图集。

首版在实际人物旁仍显得颗粒太大，保留首轮候选/截图后使用内置 image_gen 编辑两张源图，得到 v2。最终选择由 `layout.json` 的文件名明确指定，修订提示词见 [density-revision-prompts.json](density-revision-prompts.json)；v1 原图未覆盖。没有通过缩小后复制平铺来伪造连续细材质。

生产导出运行 `tools/Export-N1SurfaceRepair.py`，在基础 `Export-Hd2dN1.py` 之后运行。整张源图最近邻采样为 1040×780，再量化到既有 DEN-N1-128；地面不再使用重复或镜像拼贴。钟房石廊保留原 26..35 / 16..19 材质分界，墙沿只从已有原创 R01 石墙条裁取。二值透明与透明 RGB 清理沿用原约定。

实际碰撞仍由 `NightRooms.cs` 唯一决定；三处 floor alpha 必须与原掩膜逐像素一致，墙沿不得进入可走区。导出更新生产层、计划图、环境合成与预览，原图和原始导出脚本保留。原有门口与道具只出现在预览中，不烘焙到生产地面。脚本、布局、两张原图、色板、墙条和 NightRooms 来源哈希保存在主 manifest 的 `n1_surface_repair`。

N1 素材接入普通模式，F6 开发观察中的 F10 仍保留原开发底图对照；石场开关保持。当前修复不意味着陈设、建筑体量、交互热点、剧情或存档已完整验收；运行覆盖另记于 `research/art-n1-surfaces-0313-20261015.md`。
