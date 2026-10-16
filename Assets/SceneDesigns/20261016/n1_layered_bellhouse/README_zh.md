# N1 无声钟房：高分辨率分层美术候选

2026-10-16。按 N1-S03 与旧渡口布局重绘，保留宽值房、后角铺盖、西南回程入口、东侧狭长通道和通道末端暗渠门。钟是屋外独立低钟架，没有钟塔，也没有套用 A01 码头大屋。

## 先看

- `previews/roof_off_on_actual_comparison.png`：左揭顶，右盖顶，由交付层真实 alpha 叠合。
- `previews/roof_off_actual.png` / `roof_on_actual.png`：各自的灰底大图。
- `previews/building_roof_off_transparent.png` / `building_roof_on_transparent.png`：仅建筑及室内的透明叠合。
- `previews/twelve_layers_separate_gray.png`：12 层按文件名排序的缩小分层预览。
- `previews/bedding_shoes_inspection.png`、`east_passage_inspection.png`、`front_eave_inspection.png`：关键物件与接合局部。

## 交付图层

全部是 **1536×1024 RGBA PNG**。左上角 (0,0) 对齐；以下位置是美术候选画布位置，不是游戏原点、碰撞格或已验证的接入锚点。

1. `layers/00_floor.png`：完整木地板和东侧石铺通道，墙下、铺盖下、桌下都已补全。
2. `layers/01_walls.png`：完整无顶石木墙体、南侧门洞与窗洞、东侧狭通道；室内透明。未添加会挡住路线的新隔间。
3. `layers/02_roof.png`：主屋瓦木顶与低通道顶，可整层隐藏。
4. `layers/03a_cot_adult_left.png`：左成人铺盖。
5. `layers/03b_cot_adult_right.png`：右成人铺盖。
6. `layers/03c_cot_child.png`：较短铺盖。
7. `layers/03d_small_shoes.png`：床边独立小鞋线索。
8. `layers/03e_watch_desk.png`：北侧值守桌、油灯、杯与凳。
9. `layers/04_outdoor_bell.png`：独立户外钟架、断绳及一段落地绳头。
10. `layers/05a_southwest_door.png`：西南入口门扇。
11. `layers/05b_east_passage_door.png`：东侧通道末端门扇。
12. `layers/05c_windows.png`：两个独立于墙体的窗件。

实际叠合顺序：地板 → 室内铺盖、小鞋和值守桌 → 墙 → 门窗 → 屋顶。户外钟架可独立叠放。盖顶/揭顶对照只改变屋顶层显隐，其余所有层保持原位。

对照图右上空白处的钟架是**独立件展示位**，不定义它在岸院地图上的真实坐标。钟应由岸院东平台候选决定场景落位；已提供相同钟架供岸院层复用。独立紧边透明件保留在 `work/bell_trim.png`，原图在 `raw/04_bell_v1.png`。

## 检查与制作

- 6 次内置 image_gen 初稿，0 次重绘。原稿完整保存在 `raw/`，完整提示词在 `prompts/`。
- 后处理仅用 ImageMagick 做 alpha 清理、图层选区、最近邻缩放、整数平移和 source-over 合成。没有用程序绘画或 Python 图像编辑。
- 地板为单独新绘，不是把整屋抠成背景。墙顶隐藏后，后墙及完整内部地板仍存在。
- 铺盖后角可读；小鞋是可独立移动/隐藏的道具。值守桌靠北，中央到东侧通道的路线保持空置。
- 屋顶覆盖主室及通道开口；前檐与墙顶有实接叠压。门窗没有重复画入地板或屋顶。
- 每张交付层的 alpha 均只有 0/255 两值；尺寸、抽查与限制见 `art_review.json`。这是美术检查，不是寻路、交互或运行验收。

## 来源与范围

`design/02_世界与地图/旧渡口_场景与通路.md` 的布局表（29–33 行）；`design/05_主线/台本/台本_N1_无钟之夜.md` 的 N1-S03（“钟在外头”、后角铺盖与小鞋）；旧 `n1-exterior-v1.png`、`n1-bellhouse-v1.png`、`r_eao_n1_bellhouse_plan.png`；2026-10-16 A01 仓棚的材质与分层方式。只读快照在 `sources/`。

本次仅称**高分辨率分层美术候选**。未声称原生像素、26px 网格、生产色限、碰撞/锚点适配或运行通过。没有修改旧资产、游戏代码、校验器、接入与游戏包，没有 push。
