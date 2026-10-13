# 布林外港街区场景素材 v1

本批继续负责场景绘制。68张生产PNG、13个独立建筑与道具、5张局部场景，加1张区域连接总览；对应原清单9项视图。691项静态检查通过。
本批为可导入美术和空间制作提案，尚未安装为原生游戏房间。NPC图像、对白和行为由另一模型负责。

打开preview.html，切换场景、平面图、屋顶、26格、通行掩码及出口点。它在解压目录离线可用。

| ID | 场景 | 像素 | 格数 |
|---|---|---|---|
| r01_port | 港街复核亭 | 1040×780 | 40×30 |
| r01_hearing | 听审棚与熄灯租屋外巷 | 1040×780 | 40×30 |
| r01_workshop | 堤外器具工坊与弃置驿站 | 1040×780 | 40×30 |
| r01_salt | 盐车道 | 1040×780 | 40×30 |
| r01_rental | 熄灯租屋工作间 | 624×520 | 24×20 |

区域图r01_region__plan为1664×1248的连接示意图；六个节点、七条双向边与R01设计一致，显示锚点不等于世界格坐标。区域图标缩为1/2，只用于地图显示；不得作为实际房间尺寸或碰撞。

**导入**：使用assets/的RGBA PNG，关闭平滑与mipmap，保持透明画布。场景层1像素＝1房间像素，原点(0,0)。
层次：backing→floor→structure→按脚底Y排序的独立body/道具与原生人物→foreground→可关闭roof。
建筑full/body/roof共用相同画布与原点，body和roof不重叠、可以逐像素重组full。roof隐藏只影响视觉，不替代室内房间或权限。
物件左上角=(cellX×26+13,cellY×26+13)-sprite.origin。脚底已经对齐originY，保留画布，禁止自动裁边。
props_preview、environment、working_space是检查图，实际交互使用items中的单独PNG。NPC不能烘焙进这些层。

**空间接口**：manifest.json登记尺寸、原点、相对路径和SHA；layouts.json登记地面与阻挡提案；manifest.scenes另含门边开口。
各场景所有可走格连通，出口和预留点可达。碰撞采用显式格方案，经原生引擎测试后接入，不能从PNG透明度推测。
听审公共通路与私租屋入口分开。租屋只含工作桌、晾纸架和冷炉，没有新造床位；进入授权、纸张内容及冷炉证据状态由任务逻辑处理。
工坊大炉、普通修理台与压印台为独立对象，停大炉或处分资产时仍可保留基础修理。
公示栏和纸张不含文字；使用引擎字体和对应状态。寄存箱只表示外观，不声明容量或库存。灯光、火焰、处置后变化须独立绘制。

**来源和重建**：原始母图在raw/，完整提示词与输入/输出SHA在generation-log.json，裁切/最近邻组装见manifest.crop_operations；未复制商业图集。
指定Pixel Asset Master skill commit：33d891c421a9ad3608f5a09af97271388ca923af。实际调用其finalize_assets.py量化/清理与asset_validator.py验收。
raw母图保持不变；港街最早输入中的蓝色基础已在导出时换为干地。建筑占地与出口开口在生产几何中校正，生图时输入另存guides/*_generation_v1.png。
重建顺序：Prepare-Hd2dR01Streets.py→Prepare-Hd2dR01Region.py→Export-Hd2dR01Streets.py→Validate-Hd2dR01Streets.py→Package-Hd2dR01Streets.py。
本批不修改游戏包、角色存档或NPC源码。原生门、保存、镜头、碰撞、人物遮挡与动态灯光仍需游戏装配验收。
