# SQ05 / R02-well 渡民岸井：六层美术候选

2026-10-16。已按 SQ05-S01、SQ05-S03 和 R02 区域文本重绘六类独立素材。原稿全部由内置 image_gen 绘制，共六次初稿，未作二次生图修订。后期只用 ImageMagick 做透明边缘整理、矩形选区、最近邻缩放、整数平移与真实 source-over 合成。

## 查看顺序
- previews/sq05_actual_alpha_stack.png：真实叠合。
- previews/roof_off_on_actual.png：左揭顶、右盖顶，均来自交付层。
- previews/six_layers_separate.png：六类逐层灰底预览。
- previews/step_01_ground.png 至 step_06_roof_on.png：实际累积叠合步骤。
- previews/shelter_roof_off_detail.png：揭顶后完整背墙、柜顶与前梁间距、柜脚落点。
- previews/shelter_roof_and_cabinet_detail.png：棚檐与支柱接合。
- previews/three_sampling_landings_detail.png：三个取样点的干岸落地细节。
- previews/well_filter_footing_detail.png：井与独立过滤架。

## 六个主图层
所有主层与子层均为 1536×1024、8-bit RGBA PNG，共用左上角原点。底图为完整不透明地形；其余图层背景透明，整理后的 alpha 为 0/255。

1. layers/01_ground.png：河岸、干地回程、三处空取样落脚点、非交互草石前景。没有井、柜棚、屋顶、柜、过滤架、桶点。
2. layers/02_shelter_body.png：无顶木棚主体、完整背墙/短侧墙、柱梁、石脚与浅石平台。内部没有柜。
3. layers/03_roof.png：独立单坡木棚顶，可整层隐藏。
4. layers/04_well_filter.png：单井与分离的过滤架。过滤架底部是浅陶盆，不是额外取样桶。井中没有额外水桶。
5. layers/05_sampling_points.png：恰好三个岸边取样桶点，每处一个。
6. layers/06_closed_cabinets.png：关闭的分柜保管设施，空白小牌不公开姓名/编号。

实际叠合顺序：01 → 02 → 06 → 04 → 05 → 03。隐藏 03 即为揭顶。
04a/04b 为井与过滤架的独立子层；05a/05b/05c 为上、中、下三个桶点；06a/06b 为左右柜。
合并层和对应子层是替代用法，不能同时叠加，否则会重复显示。

## 画面检查与叙事边界
- 从左下入口经中部到岸边的干地视觉回路保留，三个取样点可分别抵近；这不是碰撞、可走格或游戏内导航验收。
- 三桶均在陆地，河面侧仅有自然石岸、芦苇。单井、独立过滤架与桶点没有重复烘焙到地形层。
- 屋顶隐藏后仍有完整棚体；柜顶已缩放/下移到前梁下，柜脚留在平台内。无顶与有顶使用相同柜层。
- 两柜是本次画面布局选择，台本要求分柜保存，不要求世界里恰好两柜。
- 画面不预设迁居/留营/分散安置选择，不证明水质已核验、井已修复、本人同意、匿名交接或任务已完成。闭柜不代表玩家取得全部钥匙。
- 重组图片与最终叠合的 ImageMagick AE 差异为 0；逐层图和对照图均为真实合成，没有再次生图伪装结果。

## 来源与限制
sources/ 保留台本、区域、协作约定只读快照，以及旧 SQ05 场景、同日 A01 仓棚与 DT03 场景参考。
raw/ 为六张未改动原始 PNG；prompts/ 为完整提示词；TRANSFORMS.txt 记录实际变换；generation_manifest.json 和 art_review.json 记录来源与核验；SHA256SUMS.txt 为文件哈希。
本次是高分辨率美术候选，不声称通过原生像素、26px 网格、≤128 色、碰撞或游戏内验收。未改代码、实现或游戏包，未接入、未 push。

