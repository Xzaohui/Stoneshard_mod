# 0.3.9 水槽与铺盖来源

2026-10-15，内置 image_gen。用户持续修复素材与对齐游戏风格授权。原图保留在生成目录并复制进项目，不依赖外部绝对路径。现有资产按修复授权替换，原始 R01 生成图不改。

## drain-basin-v1.png

原始工具图：`C:/Users/83912/.codex/generated_images/01a13e01-c219-70b0-b2d5-46522e8a6302/exec-5ed787ce-c0ee-400d-9e50-b65690b57977.png`

项目原图：`raw/interiors/drain-basin-v1.png`。整段缩放至既有三处 104×260 / 130×260 非可走水槽；不再小块纵向平铺。岸沿也是生成图的一部分，碰撞仍以 N2Quest 为准。

最终提示词：

Use case: stylized-concept. Asset type: production pixel-art drainage basin for a gritty top-down medieval RPG using 26px movement tiles and 26px tall characters. Generate ONE long narrow vertical rectangular sunken canal basin, exact overhead orthographic top-down view, length twice its width, filling a portrait 1:2 canvas edge to edge. It will be reduced to 130x260 native pixels. A continuous narrow worn grey-brown small-stone coping rim around all four edges, with a little irregular dark damp earth and moss on the outside corners; rim thickness around 6 native pixels, no high vertical walls. Center is quiet dark desaturated blue-green water with many tiny subtle irregular short ripples, compact crisp pixel clusters and very low contrast. No periodic motifs or obvious repeated patches, no broad bands or checker patterns; avoid fish, leaves, floating trash, foam, reflections of objects, bright glints, waves, ornaments or symbols. Basin is full length and entire canvas is painted, opaque, no margins, no transparent background. Uniform soft upper-left lighting; restrained charcoal, umber, grey stone and dull teal water palette. Small stone joints and water detail consistent in scale with Stoneshard-like 2D game environments, not isometric, not a painting or 3D render. No characters, no items, no text, no UI, no perspective convergence. This is one complete basin with end caps, not a texture tile or a room.

## bedroll-topdown-v1.png

原始工具图：`C:/Users/83912/.codex/generated_images/01a13e01-c219-70b0-b2d5-46522e8a6302/exec-28af1c37-5085-4be6-8abe-c9f6890e23e8.png`

项目原图：`raw/interiors/bedroll-topdown-v1.png`。保留真 alpha，二值化后裁透明边，最近邻约束到 24×44 可见框并放进原 52×52 画布；精灵原点 (26,43)、三个原有实例的位置与非阻挡语义不变。

最终提示词：

Use case: stylized-concept. Asset type: ONE production transparent pixel-art bedroll sprite for a gritty top-down medieval RPG with 26px tall characters. Primary request: an unoccupied laborer's thin straw sleeping mat with a worn dark desaturated brown-grey wool blanket spread flat, small rolled cloth pillow at the NORTH/top end, uneven frayed fabric edges. Camera is exactly overhead orthographic, long axis exactly vertical with parallel edges and no diagonal tilt, no isometric projection, no side view, no raised mattress, no wooden frame or feet. This must read as a flat floor cloth a character could walk across. Intended native visible footprint about 24px wide by 44px long, centered on a 52x52 transparent canvas. Compact restrained pixel clusters, clear plain silhouette, muted umber wool and grey-tan straw, subtle short folds along length, light upper-left. It should look simple and used, consistent with the fine but readable pixel style of Stoneshard-like 2D game props. No person, no body under the blanket, no tools, no shoes, no floor, no drop shadow beyond a tiny contact rim, no box, coffin, planks, straps crossing like a crate, no metal fasteners, no text, no UI or border. Transparent background including corners and all outside the single narrow mat. Keep generous transparent margins to the left and right.

## 生产导出

`tools/Export-N2InteriorStyleRepair.py` 同时导出 N2 四层和 `native-n2-built-v1/assets/n2site_r01_shelter_bedroll.png`，固定 R01 128 色、最近邻、无抖动、二值 alpha、透明 RGB 归零。生产 PNG 内嵌 .sml。完整从基础图重建时，顺序为 N2 基础导出、外院基础导出、外院地面与立面修复、最后本修复导出器；单独执行旧基础导出会回到旧派生版本。

实际显示与剩余问题独立记录于 `research/art-water-bedroll-039-20261015.md`，图像检查不等于实机验收。
