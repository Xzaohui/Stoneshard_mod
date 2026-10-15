# 0.3.7 门交互锚点与建筑接地修复

2026-10-15，Windows Codex /root，main 工作区。延续用户“继续开发、computer use、截图待办、持续对齐原作风格”的授权；0.3.6 全部未提交改动保留。本批不是 OI-10 完整剧情回归。

## 已核对的本机接口

输入为已装 0.3.6，data SHA-256 为 `73A0AFD2DC6BD62BA30355699CBD7224567A93898FB4568BE15F712B07A8BAEC`。只读核对了门的 Create、User 0、Alarm 7 及其继承链，不保存原作完整源码。

- `o_Doors_all_small → o_villageDoorsEnter → o_preset_transition → o_transition_hl_only → o_transitions_door`。
- `s_doors_all_small` 为 64×90、原点 (32,32)、32 帧；此前用于常驻绘制的 `s_door` 是另一个 28×52、原点 (1,27) 的精灵。不能把绘制脚点修正当成交互格已修正。
- `gml_Object_o_transitions_door_Create_0` 按精灵中心计算逻辑 grid，再登记原生 barrier。对放在 `(cell*26+13)` 的门，原精灵的 Y 中心与原点相差 13，逻辑 grid 会比摆放格多一行。
- 原生 User 0 和 Alarm 7 仍负责回合锁、战斗、对话、距离、overlay、地点事件 4 保存与转场。本批不能绕过这些条件或直接写玩家位置。

`SceneDoorAnchor.cs` 新增 EAO 专属精灵资源，复用原图帧与碰撞 mask，原点设为 (32,45)。只用于 SceneAssembly 管辖的门；原精灵、原门及旧 D01 坐标不变。GameProbe 核对帧、mask、尺寸、中心原点及门的原生继承。实机是否解决 ART-036-12 仍须现场复测，不能由这条公式直接认定。

开发面板追加只读诊断：门摆放格、实际 grid、锁状态、Alarm 7、玩家回合锁数量与目标 tag。诊断不调用门、不修改输入锁、不写任务状态。

## 建筑素材

三座建筑的棋盘状底条存在于各自 PNG，`n2site__structure` 是空层，因此应修 PNG。内置 imagegen 分别编辑三张原图，原始输出保留于 `src/Art/scene-style-repairs-20261015/raw/facades/`，提示词及来源见同目录上级 `prompt-and-provenance.md`。

导出采用生产版 4df549ad 的主体边界、现有 canvas 与 origin；不能使用 R01 源图的不同透明留白去推导生产构图。`Export-SceneFacadeRepair.py` 固定这些边界，记录基线 PNG SHA、原图/成品 SHA，做最近邻缩放、固定色板和 alpha 规范化。碰撞继续来自 `layout.json`。

完整外院重导出顺序：基础 `Export-N2SceneAssembly.py` → 地面 `Export-ForecourtStyleRepair.py` → 建筑 `Export-SceneFacadeRepair.py` → `Validate-N2SceneAssembly.py`。最后仍须通过候选嵌入字节及实机显示校验。

## 本批验收清单

- [x] 候选构建、原作房间/非 EAO 代码读回一致、五份报告同 SHA。
- [x] 备份部署到当前组合，保留 vanilla 与完整用户数据。
- [x] 外院三座建筑底条已消除，主体沿用原边界；实机可见。较大的零星碎石和建筑矩形地脚仍须细修。
- [x] 外院经普通鼠标门进入绞盘室，再经灰堤外院门返回专用 marker (26,16)。
- [ ] 门摆放格与实时 grid 一致，人物在门格及相邻格均不会被无响应门困住。
- [x] 从原生出发点巡览和返程后保存、正常退出；不把场景抽查扩大成剧情/存档全回归。

尚未完成的其他场景风格问题继续见 [0.3.6 待办](art-runtime-todo-20261015.md)。完整项目开发目标仍未达成。

## 候选与部署记录

17:01 部署到当前安装，备份 `backups/direct-20261015-170113-239`，部署阶段 vanilla 及 133 个用户文件保持原哈希。候选通过 43 指令场景、8 房间、5 地图传送、59 剧情结构、272 开发/嵌入素材检查，共 387 项；图像检查 2038 项。报告留存于 `artifacts/scene-runtime-037-20261015/`，这些报告均不代替运行验收。

- data.win SHA-256：`C78FA5BE4450D5C952BA7436F6FC691215706C9517797D9B61DB6E7858D67942`
- .sml SHA-256：`02EE18467C433B2603CC92AE37B50B4ED6B6006D433C94142272A6A025A8C88C`

## 实机结果与限制

24 张本机窗口截图保存在 `artifacts/scene-runtime-037-20261015/`，运行摘要为 `artifacts/scene-runtime-037-20261015.json`。截图文件名中 entry/result 也包含尝试，只有下列对应画面证明实际到达。

- [三处立面接地](../artifacts/scene-runtime-037-20261015/03-facades-clean-apron.jpg)：黑色棋盘底条消失。雇工棚全景见 [返程画面](../artifacts/scene-runtime-037-20261015/09-camp-native-return-observer-off.jpg)。不能据此称整个外院风格完成。
- [外院绞盘门](../artifacts/scene-runtime-037-20261015/04-winch-entrance-anchor.jpg) 为摆放 (26,14) / grid (26,14)，[室内返程门](../artifacts/scene-runtime-037-20261015/15-winch-return-anchor-diagnostic.jpg) 为摆放 (31,23) / grid (31,23)，均 lock=0、玩家回合锁=0。
- [实际进入绞盘室](../artifacts/scene-runtime-037-20261015/11-winch-native-entered.jpg)，沿通道行走后经原生返程门 [回到外院 (26,16)](../artifacts/scene-runtime-037-20261015/16-winch-native-return-confirmed.jpg)。返程成功时观察器开启，因此早先“关闭观察器后成功”的先后关系不能认作观察器阻挡输入的原因。
- 雇工棚 (7,24) 普通返程成功。旧渠入口 (42,14) / grid (42,14) 一致，[实际进入侧间](../artifacts/scene-runtime-037-20261015/20-canal-native-entered.jpg)，随后沿原室内门返回绞盘室；新增侧间 (8,22) 外院返程门本次未到场验证。
- 人物走到门格后，中心点击多次没有转场；右键中心出现人物菜单。改变点击位置后绞盘及旧渠成功。现有证据不能区分人物与门重叠、原生点击选择、自动输入时序各自影响；保留 ART-037-13，不把一次成功写成每次可靠。
- 岸院及钟屋等未纳入 SceneAssembly 的旧门仍观察到 grid 比摆放多一行，例如岸院 (7,24) / grid (7,25)。本批没有扩展到这些门，登记 ART-037-14。
- Shift+F11 返回本次原生野外出发点，观察器按现有规则关闭；[游戏菜单保存后回到标题](../artifacts/scene-runtime-037-20261015/23-saved-to-title.jpg)，随后 Alt+F4 正常关闭，窗口清单确认游戏已退出。未恢复、删除角色或写入任务阶段。

本批仅关闭“未观察到绞盘返程成功”这一失败记录；门格重叠的可用性、旧渠新增外院出口、室内铺装/墙口/门名、岸线接缝及完整剧情与存档回归仍未完成。
