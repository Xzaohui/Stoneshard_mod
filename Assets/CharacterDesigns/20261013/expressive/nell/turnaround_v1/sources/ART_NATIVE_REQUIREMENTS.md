# 原生人物素材接入要求：只读核验与最小试作

核验日期：2026-10-12。状态：技术调查；尚未制作、导入或运行原生人物精灵。

## 结论

现有概念图不能直接当作游戏人物帧。当前源码足以确定资源嵌入方式和已有 NPC 接口，但不足以确定 Sela 的正式画布、人体像素高度、原点、朝向序列及碰撞配置。应先做独立、可丢弃的单人单帧视觉试作；正式接入前补齐匹配版本的精灵元数据。不要把参考图大小、房间格子大小或生成图分辨率当成统一引擎规范。

本文件仅记录读到的源码及参考图属性；没有改变图片、项目嵌入项、GML、游戏包或存档，也没有执行构建、游戏或新工具。

## 已核实的项目事实

下列源码定位均相对仓库根目录。

- **图片不会因为放进 Assets 就自动入包。** `src/EmbersAndOaths/EmbersAndOaths.csproj:13` 仅显式嵌入 `Assets/night-bell-v1.png`，逻辑名为 `EAO.NightBell.png`；没有概念图通配嵌入规则。`tools/GameProbe/SmlPackage.cs:11–35` 打包一个启动器图标、GML 和程序集；图标并非游戏人物精灵。当前 ConceptDrafts 人物图没有对应的运行导入逻辑。
- **现成嵌入路径是钟道具专用实现。** `NightArt.cs:19–35` 读取程序集 PNG，写入 `UndertaleEmbeddedTexture`，创建纹理页项目并注册 `s_eao_n1_bell`；已有资源尺寸改变会拒绝，要求版本化精灵。它只有一个纹理帧，使用 `CreateSpriteNoCollisionMasks`。`64–2048` 的尺寸限制、中心 X／84% 高度原点均为此钟的代码，不能照搬到 NPC。
- **37×50 是这里创建的对话图标尺寸。** `NightArt.cs:37–46` 使用原点 `(0,0)` 创建图标。这不是场景人物尺寸。`NightQuest.cs:177–179` 又把钟按宽 104 绘制，说明资源像素尺寸和世界中绘制尺寸必须分开记录。
- **已实现 NPC 复用原生外观。** `NightQuest.cs:133–148` 使用 `s_peasantfemale_06`、`s_peasantmale_13`、`s_peasantfemale_03` 及对应 P 肖像，父对象为 `o_simple_NPC`。重复 `AddObject` 后显式设置 Sprite、ParentId、Visible；Prepare 阶段先分配资源再编译事件。尚没有 Sela 的运行对象或新人物图片导入器。
- **交互沿用原生接口。** `Codes/courier_create.gml:1–16` 先 `event_inherited()`，再调用 `scr_unit_interactive_init(sprite_index, sprite_index)`；Draw、Mouse 事件继承父对象。此仓库没有提供该原生函数和父对象的完整行为定义，不能仅凭这次调用断言新图的点击轮廓、占格或寻路会正确。画面 alpha 边界不等于世界碰撞边界。
- **26 是这组房间的布置格距。** `NightRooms.cs:14,44–45,59` 使用 `Tile=26`，通常在格心 `cx*26+13, cy*26+13` 放实例，墙碰撞另由 `o_hut_wall` 放置。它不是人物画布宽高，也不能证明脚部原点偏移。
- **预览关闭平滑不代表游戏关闭平滑。** `tools/GameProbe/Program.cs:78` 的 HTML 预览使用 `imageSmoothingEnabled=false` 和 `image-rendering:pixelated`；已检查的项目 `.cs`／`.gml` 未找到显式 GPU 纹理过滤设置。真实游戏继承渲染、相机缩放及过滤状态仍未核实。

## 单张 Verren 原参考实际能说明什么

文件：`references/original-characters/verren_npc_community_wiki.png`。本次实际查看图片，并用现有 Pillow 只读测量；未重存或修改。

- PNG，RGBA，25×38，文件帧数 1；可见单一朝向。
- alpha 仅有 0 和 255；非透明颜色共 19 种。
- 非透明包围范围为 `[2,23) × [2,36)`，即 21×34 像素；最下可见像素行是 y=35（从 0 计）。这是图像内容包围范围，不能等同人体身高、脚底接地点或精灵原点。
- SHA-256：`ce4c5f8378fc3f537e534fd808618eb1b9897be4579658978561d270330b5d49`。
- 来源及版本说明见 `references/original-characters/metadata.json`、`coverage-original-reference-audit.json`。保存的来源页为 https://www.stoneshardwiki.com/en/people/verren/ ，记录称页面标注 0.9.4.25；尚未对照安装包。这里没有重新联网核验来源。

以上仅是此下载文件的属性，不构成全游戏 19 色限制、25×38 标准格或单方向动画规范。公开 PNG 不包含可验证的 GameMaker 原点、纹理裁切目标偏移、碰撞及状态帧映射。原参考仅供对照，不加入原创计数或打包进新 Mod。

## 最小试作建议（非已执行配置）

只选择 **Sela、一种已记录朝向、idle 的第 0 帧**，独立保存 v001，不覆盖旧概念选稿。朝向先用 `view01` 并附文字／图示说明，不在没有状态映射时冒称引擎 south、east 或数字方向。保持成人、发髻、青绿色披肩、浅色袖、灰褐裤与绳圈的识别特征。

可逆视觉试作可以明确选择 25×38 作为“与该参考同画布的实验”，使用透明背景、alpha 0/255 和有限色块；这些是试验约束而非正式规格。人物高度、颜色数量、脚点应按实际成图记录，不为凑 19 色、34 像素或 y=35 而扭曲人物，也不能靠缩小 1024 图直接通过验收。像素处理授权前不执行此步骤。

建议候选命名：`native-pilot/sela/v001/sela_idle_view01_f000.png`，配同名 JSON 记录角色 ID、来源候选与哈希、canvas、可见 bbox、alpha 值、palette、明确的 foot_anchor、origin、frame_index、朝向说明及 `runtime_verified: false`。未核实的 origin／collision 用 null 和待核说明，不写猜测值。不要自动生成其余朝向或整套动作。

## 正式导入前仍缺的最小输入

1. **匹配安装版本的少量 NPC 元数据。** 优先读取拟沿用的 `s_peasantfemale_06`／父对象，并用 Verren 或另一名成人校对：Width、Height、OriginX/Y、帧数、各帧 Source／Target 矩形及偏移、碰撞掩码／边界。现有 `tools/GameProbe/Program.cs:81–89` 的 `--asset-summary` 可以读尺寸、原点、帧数和对象父级，但不能单独覆盖所有这些字段。本次仓库查找未发现可用 `.win` 输入，未运行 probe。
2. **实际动画约定。** 只读查看目标原生父对象、Create／Step／Draw 及交互函数如何选帧、选朝向、翻转、缩放和确定深度；明确静止 NPC 是否真的只需一帧。没有此证据，不指定正式方向数、每动作帧数或 FPS。
3. **像素尺度与落地截图。** 在已知缩放和过滤设置下，将试作与至少两名原生成人同地面并排，核验脚点、遮挡、点击范围及邻格通行。截图和实测才补足源码中继承行为的未知；编译成功不代替此检查。

## 接入计划与验收门槛（待后续实现）

确认元数据后，采用独立的显式 `EmbeddedResource` 和稳定的 `s_eao_…` 名称，不加入全部 ConceptDrafts。以 `NightArt` 的嵌入／纹理注册模式为参考另写人物导入，不能复用钟的尺寸门槛、84% 原点或无掩码假设；根据核实后的裁切、原点和交互要求设置资源。资源先分配再编译事件，复用对象时显式更新属性，尺寸变更采用新版本名。

先验收单帧：透明边缘无灰底／软边，原尺寸及整数倍预览清楚，色块与轮廓稳定，脚点与原点分开记录。再做非部署的候选包读回，核对 PNG 哈希、尺寸、origin、帧数、纹理引用和重复导入是否新增垃圾资源。最后验证实际站位、遮挡、点击与通行；通过后再决定扩展朝向和动作。本轮没有创建候选包、执行游戏验收或部署。
