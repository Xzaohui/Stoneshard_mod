# A01 主屋分层绘制小样（2026-10-16）

状态：已完成三张独立绘制层；同画布，未对齐，不能直接作为注册合格的组合建筑使用。

本轮只做主屋分层绘画，没有修改代码、校验器、游戏接入或旧素材，没有 push。没有把整景程序抠图当作重绘。

## 看图入口

- `previews/roof_off_on_actual_comparison.png`：左为主体+附件，右为主体+屋顶+附件；直接使用源 PNG 原位叠合。
- `previews/three_layers_actual_stack.png`：三层原位叠合，灰底便于看错位。
- `previews/three_layers_separate_gray.png`：从左到右为主体、屋顶、前景附件，均保持原始尺寸。
- `previews/old_workshop_layer_evidence.png`：旧 workshop 完整图、body、roof 的灰底只读检视。

## 三层内容

1. `layers/01_body.png`：无屋顶主屋。含连续后墙、内侧木地板、前墙、山墙、左右侧室的完整可见结构，中央门洞、门框、石阶和窗户。屋顶移除后不是透明大洞。门窗没有再画进附件层。
2. `layers/02_roof_candidate.png`：主屋瓦顶、两侧矮屋顶、厚檐、烟囱。选用屋顶 v2，仍注册失败，不能当正式覆盖层。
3. `layers/03_foreground.png`：门左长凳、右廊木箱和木桶。独立于主体，可移除查看身后的墙面。

三层均为 image_gen 原始输出的逐字节副本，1536×1024 RGBA。没有缩放、平移、裁剪、调色、抠图或阈值化。纯 alpha 合成只用于预览。透明叠合预览另存于 `previews/three_layers_actual_stack_transparent.png`。

## 明确问题

- “同画布”只描述像素尺寸，绝不表示已对齐。
- 屋顶 v2 的前 V 顶约 (768,400)，主体山墙顶约 (780,342)，约偏左 12、偏下 58 像素。坐标为目视近似定位，不是逐像素测绘。
- 主屋屋顶左右檐约 x310、x1215；主体墙顶约 x420、x1140。超出约左 110、右 75 像素，侧檐存在悬空，不能用“正常出檐”解释全部误差。
- 长凳脚在 y790 左右，而主墙石基底部在 y800 左右，长凳落地关系未通过。
- 原提示词要求门阶锚点 (768,900)，实际主体门阶下缘中心约 (780,854)，未达提示定位要求。可用 (780,854) 作为本次观察参考点；它不是已验证的游戏原点。
- 三层有真实透明 alpha，但 alpha 为 0—254，存在大量半透明像素和很低 alpha 的边缘杂点；不是旧规范要求的二值 alpha。
- 这是高分辨率纹理绘画小样，未达成 26px 网格、每精灵 ≤128 色、生产级硬像素边缘和游戏锚点要求。未运行游戏，不宣称部署或运行通过。

`art_review.json` 保存尺寸、alpha、SHA-256 与问题记录。

## 旧素材的实际证据

已读取 `src/Art/hd2d_26x26_20261013/spec_lock.md` 和 BRY-core 的 `spec_lock.md`、`manifest.json`，并实际查看：

- `bry_workshop_house.png` / `bry_workshop_house__body.png` / `bry_workshop_house__roof.png`：均 364×234，原点 (182,216)，对应 body/roof 独立层。
- 旧 workshop 的 body 只是把屋顶区域挖成透明，没有补齐屋内。这是旧素材的不足，本轮没有照搬。
- `bry_blocked_old_door.png`：独立门件证据。旧房间级素材另有 structure / foreground / roof。
- `r02_tax_house__body.png` / `__roof.png`：另一套屋顶/主体分离样本。

当前副本未找到原始 `stoneshard-assets-sample` 图集。`research/city-art-reference-catalog.json` 中 s_brynn_03_house22 的 433×239、原点 (140,220) 是历史原版索引记录，本轮没有声称已重新打开该原版图集。旧原创 Mod 素材与原版素材证据已区分。

## 生成来源与取舍

- A01 整景 `Assets/SceneDesigns/20261015/a01_redraw/a01_brynn_dockyard_candidate_v2.png` 仅用于主屋构图、灰石/木梁/瓦顶材料参考。
- 旧 `bry_workshop_house.png` 仅用于第一层的材质和硬块面风格参考，没有程序复制它的像素。
- 使用内置 image_gen，共五次：主体 v1、屋顶 v1、屋顶 v2、屋顶注册试验 v3、附件 v1。
- v3 试验试图在主体上绘制屋顶来寻找注册关系，但生成器改变了主体尺度。该图明确拒用，保留为 `raw/02_roof_v3_registration_failed.png`，绝没有拿它冒充三层合成图。
- 完整提示词在 `prompts/`，逐次输入、原始返回路径和 SHA-256 在 `generation_manifest.json`。所有原图留在 `raw/`。

后续应先解决注册和透明边缘，再考虑生产画布；本次没有扩大到整院、更多建筑或游戏代码。
