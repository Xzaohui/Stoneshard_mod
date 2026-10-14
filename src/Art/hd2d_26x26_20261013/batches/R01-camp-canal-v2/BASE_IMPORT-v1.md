# 灰堤工营与旧渠场景美术 v1

本批负责场景绘制。NPC 图像、对白与任务事件由另一模型负责。
已输出40张生产PNG、9个独立建筑/环境物件、3张局部地图；对应5项原清单视图。381项静态检查通过。
这是一批可导入素材，几何为台本约束下的制作提案，尚未装配或验证为原生游戏房间。

打开 preview.html 可离线切换场景、平面图、物件、屋顶、26格网、通行掩码和门点。
所有路径相对本目录；原图在 raw/，生产导入使用 assets/，不要导入生图原稿。

| 场景 | 画布 | 格数 | 用途 |
|---|---|---|---|
| r01_camp | 1040×780 | 40×30 | N2灰堤工营：空棺、雇工棚、拆轴工地 |
| r01_canal_pump | 1352×884 | 52×34 | D02泵房、双水槽、桥、维护梯与干燥侧间 |
| r01_canal_tomb | 936×728 | 36×28 | D02下层墓龛环道与干燥平台 |

导入比例为1像素＝1房间像素；关闭平滑和mipmap。场景层原点(0,0)，保留透明画布，不能自动裁边。
draw order：backing → floor → structure → 按脚底Y排序的独立物件/建筑body与原生人物 → foreground → 可关闭roof。
建筑full/body/roof三版本使用相同尺寸和原点；body与roof不重叠，可精确重组full。
props_preview、environment、working_space和overview是预览/拼版；实际交互物件使用items中的独立PNG。
两个overview均为1352×1638、保持两层1:1比例的上下拼版，不能当一间可走房间。

物件位置公式：左上角=(cellX*26+13,cellY*26+13)-sprite.origin。
独立物件的实际底沿对准originY；foot_anchor与interaction_hint供后续对象校准，不能直接把alpha当碰撞。
layouts.json中的可走格、阻挡矩形、门点与预留格是本批空间接口；NPC模型按各场景空位接入人物，不需要把人物烘焙进背景。
各房间所有可走格连通；初始入口和维护返程不靠人物授权解锁。原生转场、保存与犯罪/碰撞行为仍须后续安装测试。

工营棺内只放旧外套，不表示确认死亡；轴座为空，不表示本人已经回营。
泵房生活侧间有两格宽维护开口，铺盖和水壶只作独立环境图；下层墓室没有住户床位。
闸轮是中性静态图，没有烘焙所选放水方法；灯光、机关、水位变化与文字由引擎独立绘制。
旧渠入口为独立建筑图，户外地形位置及门洞接入尚待装配。

完整提示词、输入/输出哈希：generation-log.json；裁切与量化：manifest.json；静态证据：validation.json。
材料来自本项目AI生成母图与既有Mod概念图，未复制商业图集。
重建：python tools/Prepare-Hd2dR01.py → python tools/Export-Hd2dR01.py → python tools/Validate-Hd2dR01.py → python tools/Package-Hd2dR01.py。
泵房初始生图输入已归档为guides/r01_canal_pump_generation_v1.png；生活侧间边墙在制作几何中另行补齐。
