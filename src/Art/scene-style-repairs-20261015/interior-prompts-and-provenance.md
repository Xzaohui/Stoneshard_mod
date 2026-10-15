# 0.3.8 室内素材来源与提示词

内置 image_gen 生成，2026-10-15。用户授权持续修复素材、对齐当前游戏风格。本批不复制商业图集。

原始生成图保存在 `raw/interiors/`，生产图位于 `../native-n2-hd2d-v1/assets/`。导出器为 `tools/Export-N2InteriorStyleRepair.py`；完整重导出先运行 `Export-Hd2dNativeN2.py`，再运行本修复导出器，最后运行 `Validate-Hd2dNativeN2.py`。原始素材保存，生产图按用户替换修复授权更新。

新地面使用生成的完整材质图，最近邻降到 364×273 长周期画幅后铺到房间，避免原小裁块的重复大污渍；不是数学无缝纹理。二值 alpha、透明 RGB 归零，固定 R01 128 色板。碰撞遮罩来自 N2Quest，绘画不决定几何。

墙缘来自项目已有 R01 生成图的完整 26px 石墙段，不再只取 13px。雇工棚/侧间用深色切面背景，塌堤用已生成外院土地材质，水槽使用原 R01 水面片段，仅放在独立标定的非可走格。门框在地面绘制层装配，显示脚点是本格下沿，不改变门交互精灵的原生像素和 mask。

## wood-floor.png

原始工具文件：`C:/Users/83912/.codex/generated_images/01a13e01-c219-70b0-b2d5-46522e8a6302/exec-c9c5a271-a92d-488f-a183-1ab280107650.png`

Use case: stylized-concept. Asset type: production pixel-art wooden floor material for a top-down medieval RPG, to be displayed at native 26px movement cells with a roughly 26px tall actor. Generate a single flat orthographic floor texture covering the entire 1040x780 canvas edge to edge. Worn rough dark brown timber boards, muted desaturated umber and grey-brown, subtle age and dirt in seams, fine compact pixel clusters, restrained contrast, softly lit uniformly from above-left. Board width approximately 10-16 output pixels and varied lengths 45-100 output pixels; irregular staggered joints, long boards run vertically. The total floor is many varied boards, no repeated large motif. Crisp low-resolution hand-placed pixel style like a gritty 2D medieval RPG, not a polished 3D render. All geometry is floor-flat and walkable. No wall, roof, furniture, nails protruding, large planks, obstacles, objects, characters, symbols, text, borders, vignette, bevelled outer frame, perspective or tile grid. Do not depict a complete room. The texture must stay visually quiet behind characters. Opaque full canvas.

## stone-floor.png

原始工具文件：`C:/Users/83912/.codex/generated_images/01a13e01-c219-70b0-b2d5-46522e8a6302/exec-a7218729-d258-4fae-b724-2fdd39e04813.png`

Use case: stylized-concept. Asset type: production pixel-art stone floor material for a top-down medieval RPG, displayed at 26px movement cells with a roughly 26px tall actor. Generate a single flat orthographic worn flagstone floor texture covering the entire 1040x780 canvas edge to edge. Muted dark grey-brown slate, irregular small rectangular and polygonal flat paving stones, varied staggered joints and small repairs, tiny restrained chips and thin dirt/moss between stones. Each paving stone roughly 8-20 output pixels across, many hundreds across the whole image. Quiet low contrast, no large repeated motif, no cloned cracks or mirrored dirt shapes. Hand-authored crisp compact pixel clusters, limited desaturated palette, soft uniform light above-left, gritty medieval 2D RPG style rather than shiny 3D or painterly concept art. Every surface is flat walkable floor. No wall, roof, furniture, bricks stacked above the floor, large boulders, props, obstacles, characters, text, icons, shadows from offscreen objects, vignette, borders, perspective or visible movement grid. Do not depict a room. Opaque full canvas.

## doorway-arch-unused.png（首版未采用）

原始工具文件：`C:/Users/83912/.codex/generated_images/01a13e01-c219-70b0-b2d5-46522e8a6302/exec-a87a1c05-2d36-4822-9abf-c3796a5cce4d.png`

Use case: stylized-concept. Asset type: small production pixel-art doorway sprite for a gritty medieval top-down 2D RPG. A single recessed open doorway built into a SHORT wall section, viewed from above at the typical 3/4 RPG angle, front-facing. Thick worn desaturated grey-brown stone jambs and a timber lintel, a dark empty opening with the wooden door leaf held against the inside wall, a low worn stone threshold at the bottom. Two short low wall wings, compact silhouette. It must read as an opening in a wall, not a loose upright door slab on the floor. At final game scale the entire asset is 52x65 pixels, a character is about 26px tall, and the central opening spans roughly 24px. Bold readable compact pixel clusters, muted umber / grey stone / dark timber, limited palette, subtle upper-left lighting. No ornament, text, icon, UI, characters, vegetation, ground tile rectangle, cast shadow apron, checkerboard, outer outline or scene. Centered complete silhouette with padding on all sides. Truly transparent background outside the stone and timber structure and opening; keep the opening itself nearly black.

## 阶口定稿（替换竖门框预览）

首版竖门框保留为 `raw/interiors/doorway-arch-unused.png`，未部署。定稿来自 `exec-9a5e5106-f01d-4858-8ec2-bbfdc3cd3c57.png`，保存为 `raw/interiors/doorway.png`。这是检修阶口的视觉替换；转场仍是原生门生命周期，不引入攀爬、动画或新的楼层逻辑。水槽片段按原像素大小铺设，未拉长。提示词：

Use case: precise-object-edit. Edit target image 1: the isolated upright stone doorway. Replace it with a recessed FLOOR stairwell / maintenance hatch for the same gritty medieval top-down pixel RPG. The route must look embedded into the ground plane, not an upright arch or loose door. A small rectangular dark opening cut through the floor, five visible descending worn timber steps running from the bottom/front edge toward the top/back, thin low stone coping around three sides, a partly open wooden hatch leaf lying almost flat beside the opening. No tall lintel, no vertical pillars, no freestanding wall. Camera is orthographic 3/4 top-down as used for a 2D RPG floor hatch. Compact low silhouette, entire gameplay asset about 52px wide and 32px high, character about 26px tall. Preserve restrained grey-brown stone, dark aged timber, sharp readable low-resolution pixel clusters and upper-left lighting. Center complete asset with padding. Truly transparent outside the hatch assembly, opaque near-black dark cavity, no surrounding floor rectangle, no shadow apron, text, UI, characters, glow, checkerboard or scene.
