# 采石场地面第二版

2026-10-15，Windows Codex，imagegen 内置工具。原始输出完整保留于 `raw/quarry-floor-v2.png`，导出脚本为 `tools/Export-QuarryStyleRepair.py`，裁切坐标、源图及成品哈希见 `quarry-export.json`。

输入一为原 `r_eao_fx_quarry__floor.png`；输入二为本机原生野外实机截图 `artifacts/art-runtime-20261015/00-native-style-baseline.jpg`，仅用于像素尺度和色调参考，不入商业资源包。

提示词：

> Use case: precise-object-edit. Asset type: 2D RPG quarry walkable ground layer. Edit IMAGE 1 only. IMAGE 2 is a style and pixel-scale reference from the installed game. Keep IMAGE 1's 4:3 canvas composition and exact hard stair-step silhouette of the connected three walkable areas, all other regions truly transparent. Replace ONLY the existing visible ground material: remove the huge rectangular pale paving slabs, all tall rock columns, tool handles and cliff faces from this ground layer, and replace these with low compact brown-grey quarry earth, fine stone grit, sparse small broken chips and subtle boot-worn trails. The whole opaque area must read as flat, traversable ground, with no objects or obstacles. Match the reference game's crisp hand-placed pixel clusters, modest warm/cool hue shifts, dark neutral outlines, subdued saturation and small native pixel scale: one 26px cell is one character-foot width, each small rock chip only 2–6 native pixels, surface not large bricks. Muted warm grey-brown ground, low contrast variation, avoid pale beige sheet-like areas, avoid uniform checkerboard, avoid repeated mirrored patches, avoid random white-noise texture, avoid smooth painting and antialiasing. Flat orthographic ground seen from above with no global lighting or vignette. No people, text, UI, doors or additional props. Preserve the silhouette and overall framing exactly. Deliver one production ground layer with actual transparency.

生成图并未精确保持原轮廓，且透明边缘有零散像素。因此只取三处内侧材质矩形，用最近邻缩放、DEN-N1-128 调色板、无抖动和既有原生可走遮罩导出。透明像素 RGB 归零。碰撞与路径几何不从生图推算。原始素材版本仍可由 Git 恢复，不覆盖生成原图。

验收范围：PNG 尺寸、哈希、调色板、遮罩和候选嵌入检查；运行结果单独登记在 `research/art-runtime-todo-20261015.md`。不以生成图或离线报告代替实机验收。

## 外院细颗粒暗土第二版

同日使用内置 imagegen 从描述生成一张连续平面材质，不输入原作素材。原图为 `raw/forecourt-earth-v2.png`（1446×1087）；第一候选实机截图 `26-036-forecourt.jpg` 用于人工判断碎石比例过大，没有作为工具输入。导出脚本 `tools/Export-ForecourtStyleRepair.py` 按既有 layout 和调色板生成 1352×988 地面，保留原可走遮罩与三个建筑占地孔洞，不改碰撞。源图及成品 SHA-256 见 `forecourt-export.json`。

提示词：

> Use case: stylized-concept. Asset type: production flat ground texture for a 2D top-down medieval pixel RPG, covering a 1352 by 988 room canvas. Paint one continuous rectangular expanse of compact desaturated dark brown-grey earth with a few scattered fine gravel chips, worn tiny fragments of old cobble and subtle low-contrast foot traffic wear. Native game scale: a human's feet occupy a 26 by 26 pixel cell; every loose pebble is only 2 to 5 pixels across and all cobble fragments are under 10 pixels. Strict fine hand-placed pixel clusters, sharp hard edges, one source pixel per game pixel, subdued old low-resolution RPG texture. The ground must be visually quieter than characters and buildings. Most area is compact flat dirt, only sparse gravel. Muted earthy browns and greys with restrained hue shifts, almost no saturation, modest contrast and no pale slabs. Image should look like Stoneshard's natural compact dirt ground at native resolution. Absolutely no large stones, no boulders, no cliff faces, no regular tiling grids, no repeated mirrored patches, no broad decorative paths, no directional lighting, no shadows cast by offscreen buildings, no large contrast patches or beige paving. Fully opaque flat orthographic surface fills entire 4:3 image edge to edge with no holes, margin, props, scenery, text, labels, figures or UI. No blur, photorealism, glossy highlights or noisy stippling. Do not depict a scene or perspective camera: this is only the small-scale material of walkable ground.

生产导出使用最近邻缩放、R01 固定 128 色、无抖动，透明 RGB 归零。建筑黑色接地条、孤立门板和背景交界另列待办，不能以这张地面通过替代整个场景验收。

## 0.3.7 三座建筑去除烘焙底条

2026-10-15 使用内置 imagegen，分别输入当时生产版的 `n2site_r01_worker_shed.png`、`n2site_r01_winch_shed.png`、`n2site_r01_canal_entry.png` 为编辑目标，各执行一次相同提示词。原始输出保留于 `raw/facades/worker_shed.png`、`raw/facades/winch_shed.png`、`raw/facades/canal_entry.png`。

共同提示词：

> Use case: precise-object-edit. Asset type: production medieval pixel RPG building sprite. Edit the supplied image only. Remove ONLY the artificial long horizontal black/brown rectangular stripe and checkerboard apron running underneath the entire building at the very bottom. Make those apron pixels truly transparent, including the stripe beyond the walls at left and right. Keep the building itself, its stone foundation blocks and thresholds, the roof, all walls, beams, equipment, shapes, framing and exact pixel artwork unchanged. No new background, terrain, cast shadow, props or details. Preserve the original sprite silhouette except for removing that bottom apron. This is a tiny low-resolution native-game asset: preserve the existing hard pixel clusters and muted brown-grey palette; do not reinterpret, redraw, smooth or upscale the amount of detail. Keep the structure at the same location and size within the same canvas aspect ratio, with true alpha transparency around it. The result must be the SAME building cutout with the bottom horizontal rectangular apron erased, suitable for compositing directly onto the game's dirt ground. No text or UI.

模型结果保留了主要外观，但并非逐像素相同。`tools/Export-SceneFacadeRepair.py` 仅做原图 body bbox 配准、最近邻缩放、R01 固定色板量化和二值 alpha 导出；采用模型给出的去底条轮廓，不用程序绘制替代建筑。尺寸及 sprite origin 均沿用既有合同，可走格与建筑占地不从 alpha 推算。源/成品哈希、配准边界与被移除底条的起始行由脚本写入 `facade-export.json`。

完整外院再导出的顺序为 `Export-N2SceneAssembly.py`、`Export-ForecourtStyleRepair.py`、`Export-SceneFacadeRepair.py`，随后运行 `Validate-N2SceneAssembly.py`；只运行最早的基础导出会恢复历史贴图，不能据此覆盖当前生产版。
