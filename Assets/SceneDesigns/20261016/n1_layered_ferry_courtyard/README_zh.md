# N1 旧渡口岸院 · 高分辨率分层美术候选

日期：2026-10-16。范围只含美术重绘、选区拆层、透明边缘整理与真实叠合。本目录没有游戏代码、校验器或接入改动；未部署、未进行游戏运行验收。

## 先看

- previews/COMPOSITE.png：五张交付图层按顺序真实叠合。
- previews/LAYER_OVERVIEW.png：各独立图层的棋盘底预览及真实叠合。
- previews/STACK_OVERVIEW.png：逐层累加过程。
- previews/COMPOSITE_without_bell.png：不含钟架的地面与岸线候选。
- previews/BEFORE_AFTER.png：旧图参照与新候选对照；旧图没有被覆盖。

## 五张独立 PNG

统一画布为 1536 × 1152，左上角原点。叠放顺序如下：

1. layers/01_water.png：完整、不透明水面；重新绘制，无旧镜像平铺操作。
2. layers/02_dry_floor.png：西宽平台、南窄堤、东平台的干地铺石。
3. layers/03_shore_edges.png：岸沿压顶、垂直岸墙、湿苔及两侧不相连的断桥残端。
4. layers/04_foreground.png：四组独特草石，仅在岸角与残端点缀，主通路留空。
5. layers/05_outdoor_bell.png：东平台北部的独立室外钟架；铜钟仍悬挂，短绳割断，地面保留一段绳头。复用同日钟房任务的独立新绘件，没有再绘第二座钟。

水面外，所有交付层均为二值透明背景。地面未烘焙水纹、建筑、钟架或前景草石；没有 A01 布林码头仓库或商业港口陈设。

## 分层方式与复原检查

水面与草石由 image_gen 分别绘制。岸地连续结构也由 image_gen 全新绘制，再以互补选区拆为干地和岸墙，保证两层相邻处来自同一母稿。它们不是将完整旧图重复覆盖，也不是分别生成两张难以对齐的岸线。

- 干地/岸墙 alpha 交集为 0。
- 二层重新叠合与整理后的岸地母稿逐像素比较 AE = 0。
- 所有层采用真实 source-over 合成；预览不另行生图。
- 完整选区坐标、缩放尺寸、平移与顺序见 TRANSFORMS.txt。
- 原稿未覆盖。三次本任务生成、零次重绘修订；另复用一个同伴新绘钟架。

上述检查只证明本候选的拆层复原与 alpha 状态，不能证明游戏内通行、交互或碰撞已经验收。

## 视觉与台本核对

保留 N1 的西平台、中央水渠、南侧窄堤、东侧室外钟架关系。断桥残端不跨水连通；唯一可见跨渠通路保持为南窄堤。平台中部没有人物、木箱等新障碍。割断的拉绳与仍悬挂的钟符合 N1-S02；未绘钟房建筑，也未把钟移到室内。

新石面、岸角和草石采用不相同的细节；未使用镜像、重复贴片或程序纹理绘制。水面为单张不重复的房间背景候选，尚未制作流动帧。

## 使用限制

这是高分辨率分层美术候选。构图保留台本拓扑，尚未逐格贴合 1040 × 780 原布局，未做 26 × 26 原生像素/调色板验收；不能直接宣称自动拼接瓦片、碰撞图、无缝地图块或运行成品。后续若进入接入阶段，门口、返回点、NPC 锚点、格尺寸与通行宽度都需另行对照。

## 来源

- sources/N1_map_readonly.md：design/02_世界与地图/旧渡口_场景与通路.md 只读副本。
- sources/N1_script_readonly.md：design/05_主线/台本/台本_N1_无钟之夜.md 只读副本。
- sources/old_yard_reference.png、old_water_reference.png：src/Art/hd2d_26x26_20261013/raw 的旧岸院、水面参考。
- sources/yard_plan_reference.png：同批 guides/r_eao_n1_yard_plan.png；用作拓扑参考，不声称当前像素与格网完全一致。
- sources/shared_outdoor_bell_trim.png、shared_outdoor_bell_prompt.txt 与 raw/05_shared_outdoor_bell_v1.png：同日 n1_layered_bellhouse 的户外钟架原稿/透明紧边件及提示词副本。
- prompts/：本任务全部完整提示词。
- generation_manifest.json、art_review.json、SHA256SUMS.txt：生成来源、视觉核对、文件指纹。
