# 《余烬与誓约》0.3.0剧情与场景重构

用户否决当前直白的文书查档任务和整屋复用。新控制器停止旧信使/仓务员/海关入口生成与旧任务推进，保留对象、函数、物品和房间索引，旧室内档可沿原门退出。旧EAO状态不清除，不伪造新完成。

NightQuest实现独立EAO_N1阶段：商队玛拉接取、两处实际现场观察、伊沃解释、执行前可改的两计划、暗渠撤离或公开交涉、不同人物状态与玛拉回访。4名人物及2处观察均沿用原生NPC点击/对白。NightRooms用自定26像素可走格构造3种1040×780布局，只借原控制器，不带海关整张背景；原生碰撞格和新落点先于玩家。所有门保留原生保存/转场，实际出发点在原门安排转场后记录，普通回程恢复原坐标。

NightArt将原创透明钟架PNG内嵌进DLL/.sml/data；读回时验证实际PNG字节。嵌入纹理显示名称不随资源包保存，后续更新必须从既有精灵引用找到纹理，不按临时名称另建未引用纹理；改变尺寸要分配版本化精灵。观察头像用原点0,0、37×50物件缩略图。先分配新房间、对象、精灵后编译；AddObject复用时显式赋Sprite/Parent/Visible。

87个匿名方法保持各父CODE/子CODE连续，并核对真实ParentEntry/SCRP/FUNCT。43项指令场景中10项是新剧情；8项旧房间兼容、5项地图传送、19项新故事/场景检查都需同候选SHA。新对白图边、可退出性、短中文、本地化、预览无副作用、三房间连通及全部门目标分别验证。完整设计与限制见design/10_技术预研/剧情重构与旧任务退役.md，实际部署与备份见artifacts/direct-deployment.json。

runtimeVerified仍为false。当前新章无金币/经验、原生日志、战斗波次、护送AI或大陆独立方块；灰堤后续尚未实现。地面和墙边为布局美术，人物借原生精灵，一件生成资产不表示整图已完成最终重绘。

# 《余烬与誓约》0.2.4海关入口可见性（历史）

用户已完成迟信并读抄本，海关一、二楼仍没有看到小门。入口位置原海关一楼351,428；原门Draw只画交互高亮，原背景没有这扇新门的门板，且约depth=-410在原ForegroundInstances=-1000之后。补自己的Draw用s_door原素材常驻绘制、黄色“封账仓入口”标签，自己的Step置depth=-1100，原Mouse/Other/Alarm仍全部继承，原房间/代码不改。

物理入口生成独立User_4在信使对白准备检查前执行，常驻且不重复生成；完成MQ01与读过抄本只解原门锁，不隐藏门。档案室在新增封账仓楼上，海关原二楼没有新增入口。本地HarborStore译名海关，抄本路线说明同步更正。部署需33项已编译场景、8项房间结构、5项传送接口检查匹配候选。运行可见性/点击/保存读档仍待反馈。

# 《余烬与誓约》0.2.3落点修复

用户实测0.2.2能传送，但落在地图外不能移动。原版地表User_15在加载末尾创建(-50,-50)的o_abstract_player，经Alarm_0、o_fastTurnController Alarm_1/0延迟创建正式玩家；没有通用global落点。0.2.3保留源地点保存→世界坐标提交→原生换图，使用NA与待落地标记。自己的End Step在原生成完成、下一帧正式玩家创建前，查询原newgrid，选地图内开放且有开放邻格、无原碰撞/地面标记的位置，只调整原生占位对象，正式玩家自行初始化。

当前格允许重新加载救回卡住角色；完全无落点则通过原scr_smoothRoomChange([10])与已归属EAO的坐标桥回到首次已保存的源位置。无玩家的失败目标不强行执行需要玩家的保存事件。不改原CODE/房间、不清输入锁、不写角色存档。部署需30项编译指令场景、7项房间、5项结构检查一致匹配候选SHA；新增5项生成/碰撞/占位对象/失败回退/同格恢复检查。真实移动、保存读档仍待用户新版本反馈。以下0.2.2描述保留为故障前历史。

# 《余烬与誓约》0.2.2测试方式（历史）

用户最新要求：撤掉测试向导，F8开关 → 地图左键点方块。默认关闭，地图显示状态；KeyPress_119在控制器处理。正常NPC交谈仍用鼠标。代码使用原GUI state=2聚焦事件、52×mapScale与mapOffset坐标规则，添加地图对象User_10桥接；其他交互走原User_15，关闭时恢复实例事件路由。使用原日志/地图退出流程，等原回合锁解除后创建scr_smoothRoomChange(target,[4,10],-1,true)。事件4先保存源地点，新增转场器User_10再提交目标世界格并用global落点。普通原事件和原房间不改；两个新增桥事件单独检查归属，其他Mod已占用则拒绝。

退役0.2.1向导资源若已存在保留ID并禁用，首次应用不分配向导；新的角色模式迁移先关闭，不自动推进任务或移动商队。测试目标是世界方块对应的地表房间，建筑/副本层继续用现有门。边界、无房间、战斗/地牢拒绝；F8取消待处理点击，进行中的原版转场不能打断。

验收仍为25项已编译指令场景（17项任务+8项地图）、7项房间、5项地图结构检查，匹配候选SHA再部署。原生函数为替身，不算游戏运行/碰撞/存读档验证。详见设计库“可选测试传送与返回点”。以下0.2.1为已被用户撤换的历史路线。

# 《余烬与誓约》0.2.1新增范围

新增TestTeleport、原生测试向导及控制器User_2。默认关闭，可点击开启、选择两个EAO房间、关闭或回程；不依赖任务门槛或快捷键。转场使用scr_smoothRoomChange(target,[4],-1,true)，保留原版地点/商队/迷雾保存。首次成功安排转场后保存原房间/坐标/世界格；跨测试房间保留锚点，关闭不丢弃回程。返回用scr_atr_set_simple(localX/localY)+NA，普通仓库出口包裹原版Alarm_7，只在测试旅程中改回程。向导用scr_locationRoomEntityInitSavable(id,false)排除房间实体保存。

EaoActionChecks共25项，包含开关、队列、战斗/地牢暂停、转场失败、首个锚点及关闭后返回。EaoTestTeleport检查编译对白图、动作预览、原版转场/坐标接口和入口门；独立报告test-teleport-validation.json。部署0.2.1必须三个报告均匹配候选SHA，且25/7/5项齐全。原生函数仍为替身，runtimeVerified=false，真实点击、转场、碰撞与存读档待验。游戏内使用见设计库“可选测试传送与返回点”。

## 0.2.0房间基础

用户确认0.1.6正常。NativeRooms用安装内港区商店建筑/地面/碰撞创建独立封账仓与档案室，剔除模板剧情/商人/旧出入口；原版房间元数据、图层和实例顺序指纹在写前与重读后验证不变。原生双向门沿用父类Alarm/输入/过渡/地点保存，资源必须先分配再编译；落点在abstract_player前创建。仓务员原生flow提供MQ02许可、阅读/携带/首次到场核验与文书补领。总计8种物品（背包和地面共16对象），2房间、4双向门及3落点，MQ01保持5回调，MQ02另4回调；EAO事件及子方法连续排列以防0.6.1读回错绑。

17项已编译回调检查使用原生库存替身；7项房间/门/对白结构检查。artifacts/document-action-validation.json与room-validation.json必须匹配候选SHA才允许部署。artifacts/warehouse-layout.html使用原图集显示实际房间布局；运行碰撞/光照/读档待验。无金币/经验奖励、犯罪战斗分支、MQ03/旧渠或新增世界格。部署与备份以direct-deployment.json为准。

以下为接口与历史记录：

# 《余烬与誓约》开发说明

2026-10-11，当前开发版0.2.2。用户最新明确要求“不隔离，直接在当前路径下开发”。下面的新流程取代0.1.0的隔离前置条件；大型扩展未完成。

0.1.5对白已获用户确认正常。0.1.6将avatar从地图精灵s_peasantmale_13改为同人物原生P头像（37×50、原点0,0）。四种文书各建o_inv_eao_*与o_loot_eao_*配对，前者继承o_inv_book，使用o_open_note阅读，后者继承o_consument_loot。Create在event_inherited前注册自己的consum/book数据，支持原生加载时重建；避开o_inv_note对序章read_diary的写入。

接取用scr_inventory_add_item关闭自动掉落，逐件原版放入，失败只销毁本轮新建物品；成功后才推进状态。阅读事件记录独立EAO_read_*，三件全读且携带时才允许登记；核对抄本能放入才完成。旧已接/已完成进度可补领缺失物品。价格0、阅读经验0，无金币，原件保留。对白仅短交接/提示。MQ02尚未实现。

EaoDocuments检查实际继承、注册时序、原生阅读事件和资源配对；EaoInteraction拒绝长材料回到对白及错误结构体访问。EaoActionChecks解释本Mod已编译回调，并以库存函数替身验证交付事务、阅读/携带条件与旧进度；它不运行GameMaker引擎，不能验证GUI和实际存读档。命令：`dotnet tools/GameProbe/bin/Release/net10.0-windows/GameProbe.dll artifacts/direct-data.win --test-eao-actions`。报告为artifacts/document-action-validation.json。

0.1.4已被用户实测判定信使Create失败：异常对象索引2144440064。实际编译指令中，`_flow.Scripts.instruction_EAO_resume = eao_resume`在读取Scripts结构体后出现conv.v.i，随后将它作为stacktop对象写入；其他三个注册同样如此。该指令形态与报错吻合，尚无引擎逐指令运行证据。0.1.5采用原作DialogueSystem的显式variable_struct_get/set和array_get接口，移除自己的对白注册点赋值链。EaoInteraction新增字节码回归检查，已对旧部署0.1.4给出预期拒绝；新包写出前、重读后通过，非EAO代码保持不变。实际启动与对白仍待运行验证。

0.1.4撤回用户实测点击卡死的0.1.3自制面板。信使继承原生o_simple_NPC并先运行event_inherited初始化；Mouse_4/Draw沿用父类，User_13使用o_NPC原有接近、交谈门槛和scr_npc_interact_start_dialogue。注册原生flow及本地化行，原版scr_dialogue_start创建o_dialogue/o_dialogRender、按钮与退出生命周期。本Mod不再使用mouse_clear、自绘GUI或手动切换skill_can_cast/创建o_gui_no_click。

已有小样通过公开UpdatePrototype定向更新，仅改变EAO对象。EaoInteraction验证真实父类和原版事件调用、实际编译JSON的连通/文本/玩家选项/动作标签、移除旧输入锁。0.1.4/0.1.5有4个实例方法作为flow.Scripts回调，0.1.6增加补领回调，共5个；原生dialogue_eval_script重绑定至窗口并callv。EaoLinkage检查父子CODE顺序和SCRP/FUNCT链接，禁止裸名静态eao调用。退出和恢复操作由原生窗口负责。详见设计库“原生NPC对白接入与点击卡死修复”。

0.1.2修复运行器加载时 `Unable to find function eao_cn`。七个匿名实例辅助方法被编成裸名静态调用；现在事件内实现小样逻辑，不产生自定义函数依赖。`EaoLinkage.Validate`在0.1.2/0.1.3写出前与读回后拒绝裸名eao函数及嵌套EAO方法；0.1.4增加4个完整链接的原生对白回调白名单，旧坏包作为负例已被拒绝。这个约束针对当前原型，以后引入全局脚本时必须先扩展真实链接验收。

首次修复用 `GameProbe input --repair-eao package output --direct`；只更新三个EAO controller事件，并移除其旧子方法/脚本/函数，校验其他代码在写出前和重读后都不变。不能用旧组合备份覆盖用户MSL重建出的新组合。此时部署记录targetedRepair=true、preEaoInput=null，repairSourceData是含旧EAO的修复前资源备份；不能拿它当无EAO基线。后续Build自动识别此记录；若外部重新生成data，可使用 `./tools/Build-Mod.ps1 -RepairExistingEao -Deploy` 更新已识别小样。未知EAO结构会拒绝。

已更新正式data及.sml，vanilla与130个用户文件哈希未变。安装内包可读取图标、data通过函数链接校验；实际修复后游戏启动与MQ01交互仍待运行验证。详见设计库“EAO函数链接错误与定向修复”。后文六个旧包补回属于历史；14:57活动Mods只有本包，MSL全量重建时先确认其他所需包真实存在。

## 当前执行流程：原路径开发

> 2026-10-11修正：直接增量部署与MSL界面重建使用不同输入。MSL界面必须加载原始vanilla.win，当前data.win已经有MSL日志对象，不能再作为MSL打包输入。详细处理见设计库“MSL重复事件打包错误与正确输入”。

| 操作 | 输入 | 输出 |
| --- | --- | --- |
| 本项目Build/Deploy工具，直接调用本Mod补丁 | 当前组合data，或部署前无EAO组合备份 | 暂存校验后部署data |
| 原生MSL界面，自动注入日志并应用勾选Mods | 原始vanilla.win，每次失败后重新读取 | 保存到游戏data.win；不要覆盖vanilla |

原生MSL的LogUtils.InjectLog发生在本Mod之前；不能用本Mod代码绕过已经发生的重复事件异常，也不能靠关闭日志显示开关解决。失败或取消保存后，内存中的输入可能已经被打过补丁，下一次保存前重新加载原始输入。

六个旧包已从 `msl/Mods - 副本` 补回活动Mods目录，现有data和完整用户数据已做游戏退出后的新备份。MSL重新打开后确认原六项和EmbersAndOaths均勾选；运行中的MSL可能尚未刷新文件列表/勾选状态。读入vanilla时的历史校验警告仍单独记录，不据此否定用户确认的来源。

图标提示也已修复：源码 `src/EmbersAndOaths/Assets/icon.xaml` 是自制矢量图，打包时渲染为128×128的icon.png，并以 `EmbersAndOaths\icon.png` 嵌入.sml。打包校验要求本地MSL读出的Icon字节与原PNG一致且可解码，图标缺失会导致构建拒绝交付。已替换加载目录内开发包并核验；结果 `artifacts/icon-deployment.json`。这次只更新包内图标，剧情DLL和三份GML未改。

```powershell
# 只读检查是否含已打补丁的MSL/EAO标记；不能代替原版来源验证
./tools/Test-MslInput.ps1
```

源码继续在本项目，编译引用现有安装的MSL0.13.2.0。保留游戏名称、引擎FileName和原作AppData保存位置，已移除独立存档名与提前退出守卫。现有角色正常保存时会携带EAO新增状态；保存兼容仍需游戏内验证。

```powershell
# 构建、读取.sml、补丁编译、临时包重读；没有目录副本/新账户前置
./tools/Build-Mod.ps1

# 同样验收后，直接部署现有安装；游戏与MSL须已退出
./tools/Build-Mod.ps1 -Deploy
```

部署目标 `D:\SteamLibrary\steamapps\common\Stoneshard\msl\Mods\EmbersAndOaths.sml`；同时更新当前 `data.win` 并追加MSL Settings.json中 `EnableMods` 的 `EmbersAndOaths` 条目，保留其余启用项。使用当前已含其他Mods的包作为输入，仅加入EAO，避免用单独的vanilla补丁覆盖已有组合。Mod列表扫描以.sml文件名为ID，中文显示名不是设置键。

每次部署前保存当前data、Settings、本Mod旧包和完整StoneShard用户数据到 `backups/direct-时间戳`，验证备份哈希。候选包在 `artifacts/direct-data.win` 编译/重读成功后才放到游戏目录，哈希一致再替换data。候选文件只是原路径部署前的临时产物，不是隔离运行环境。原vanilla不改；不自动恢复玩家存档。游戏或MSL在运行时拒绝更新，不能强制结束程序。

第一次部署保存EAO加入之前的组合包；后续若当前data哈希仍等于上次部署结果，构建自动使用该组合备份重建EAO。外部工具改过data时以新输入处理，但若新包已含EAO则拒绝重复叠加。需要先建立明确的无EAO组合输入，不能随意删除已有Mod对象。

实际结果 `artifacts/direct-validation.json` 和 `artifacts/direct-deployment.json`；runtimeVerified仍由真实运行决定。之前两份离线报告是0.1.0历史结果。原 `Check-FormalEnvironment.ps1` 只对旧快照检查，部署后data和MSL设置有授权变动，不能再把旧快照差异当成意外损坏。

历史0.1.1首次部署时游戏仍在运行，完整data部署被拒绝。已执行 `Deploy-Mod.ps1 -PackageOnly`，仅部署.sml并登记MSL启用项，data未改、没有停止游戏；记录 `artifacts/package-deployment.json`。这不会热加载到当前游戏。当时需退出后执行上述 `Build-Mod.ps1 -Deploy` 完成资源更新；最新0.1.4完整部署已完成。需要避免重复构建时，也可用已验收包执行 `./tools/Deploy-Mod.ps1 -ValidatedInput 'D:\SteamLibrary\steamapps\common\Stoneshard\data.win'`；工具会重核全部哈希，变化时拒绝部署。

首次调查时活动Mods目录没有其他.sml，Settings保留六个旧启用项，现有data已含这些Mods。此次已从 `Mods - 副本` 找到并补回全部六个旧包，校验复制前后哈希；MSL重建时须确实勾选它们。其余备用包没有加入或启用。

当前运行：按原有入口启动。原作调查结案且与商队处于同一世界格时，左键点击信使，沿用原版接近交谈及窗口选项；选暂缓/关闭结束对白，不依赖F8。0.1.4保留EAO已有进度，地图、MQ02和原生日志仍未实现。离线验收已通过，游戏内弹窗、关闭及存读档仍待测；部署结果与最新备份以artifacts/direct-deployment.json为准。

## 0.1.0历史记录（以下隔离路线已被用户最新选择取代）

## 已写入的内容

`src/EmbersAndOaths` 是真正的MSL C#工程，包含三份GML资源，输出 `artifacts/EmbersAndOaths.sml`。包格式经过本地MSL `FileReader.Read` 实际读取，不是把DLL改扩展名。

新增持久控制对象和信使对象。原作 `questGuinnelAnswers` 完成、商队位置有效、玩家与商队处于同一世界格时提供入口。靠近信使按F8，数字1/2/3选择，Esc关闭。允许暂缓并回来；比对迟信与收条后选择交维伦核对或先抄录，完成后可再看收条。信使是复用原作精灵的接口实体，尚无原生NPC日程、碰撞、商店或完整对话系统。

EAO状态写入原作 `global.characterDataMap` 的独立标量键：

| 键 | 意义 |
| --- | --- |
| EAO_schema | 1；小样状态版本 |
| EAO_MQ01 | 不存在/0未接，1已接，2完成 |
| EAO_E01 | copied；信与收条抄录 |
| EAO_register_lead | outer_harbor；外港线索 |
| EAO_MQ01_choice | verren或copy_first；两种处理选择 |
| EAO_MQ01_reward | 1；完成登记，MQ01没有金币奖励 |

这些键不是原作任务ID。本版自带记录面板，尚未注册原生任务日志、实际物品和后续入口。维伦分支目前只登记意向，没有新维伦对白。正常保存逻辑预计携带这些键，但退出重读未实测，不能宣称已验证持久化。没有任意位置保存功能。未完成的地图、势力、支线、日常、副本没有占位冒充交付。

## 输入、产物与备份

| 路径 | 用途 |
| --- | --- |
| test-env/baseline/game | 用户确认的原始vanilla备份作为data.win及运行依赖；禁止补丁输出 |
| test-env/work/game | 唯一干净小样工作游戏；构建覆盖其data.win |
| test-env/work/launcher | 本地0.13.2.0启动器的独立副本；没有启用正式Mods |
| test-env/work/compat/data.win | 当前既有Mod组合加本小样的离线兼容输出；单独数据包，不能当完整游戏启动目录 |
| test-env/backups/时间戳 | 原始vanilla、既有组合data和完整正式StoneShard用户数据备份 |
| test-env/manifests | 私有文件清单、哈希、备份/正式环境检查 |
| artifacts | .sml与两组离线验收JSON |

`test-env`、`artifacts`、工具依赖、bin/obj被忽略；个人备份和商业游戏资源只留本地。不要上传完整项目目录。备份不自动恢复，游戏更新或正常游玩导致比较失败时应调查，不能覆盖玩家的新进度。

## 构建

使用PowerShell 7与本机.NET SDK10；Mod面向net6.0-windows以匹配本地MSL，离线核验器运行在net10.0-windows。MSL/UndertaleModLib引用来自本地副本，不改正式工具。首次构建需官方NuGet依赖；开发依赖包保存在 `tools/packages`。

```powershell
# 仅首次，游戏已退出且不存在test-env时；不会启动游戏
./tools/Prepare-TestEnvironment.ps1

# 日常构建：原版离线补丁 + 当前组合离线补丁 + 正式环境比较
./tools/Build-Mod.ps1 -CompatibilityCheck

# 单独复核正式资源、用户数据与备份
./tools/Check-FormalEnvironment.ps1
```

`GameProbe`限定补丁输出只能在项目 `test-env/work`，打包输出只能在 `artifacts`；拒绝正式安装、baseline、越界和联接输出。数据包先写临时文件、重新读入验证，成功才替换工作包；不允许原地修改输入。小样重复应用会拒绝，必须从冻结输入重建。

源码接口参考固定于ModShardLauncher commit `368dfb0602945ea88ef675204d7e4ed10497de64`，克隆放在 `tools/vendor/ModShardLauncher`；这不证明源码与本地DLL逐字相同。实际包读取、编译/补丁调用使用本地DLL。

## 离线验收的含义

实际编译GML、生成.sml、通过MSL读取、对vanilla和既有组合分别打补丁、序列化并再次读入，检查新增对象及启动保护。原有所有代码条目中只有 `o_gameLoader` Create允许变动，其余逐项反汇编比较。父方法先于嵌套方法写入CODE，避免本地UTMT反序列化失败。验证重复应用会被拒绝，原作初始化前存在路径守卫。

这证明包结构和补丁流程成立；不证明不同Mod的运行输入、渲染、NPC位置、玩家存读档或卸载兼容。现有组合的离线验收不等于所有加载顺序和所有存档都兼容。JSON中 `runtimeVerified` 必须保持false，直到实际运行验收。

## 0.1.0首次运行的历史待办

小样把引擎GeneralInfo Name/FileName改为 `StoneShard_EAO_Dev`，使用新的字符串资源，避免改动原资源池。原作slots/settings初始化之前检查 `game_save_id` 含此标识，否则结束。预期写入 `%LOCALAPPDATA%\StoneShard_EAO_Dev`；这是依据GameMaker官方保存区文档的推断，还不是本机观察。守卫没有日志写入，也不代替OS权限限制。

本地Steam扩展包含 `SteamAPI_RestartAppIfNecessary` 名称，尚未证明是否调用。它可能在GML守卫之前把进程转到正式安装。Steam Cloud也未查清，不在本轮修改Steam设置。不能据此启动当前账户副本并承诺安全。

推荐下一步使用独立普通Windows测试账户，先审查该账户不能写正式游戏/正式用户目录的权限，确认Steam登录、合法使用权与Cloud边界；不能简单给整个磁盘Everyone写权限。账户创建和Steam配置需要另行明确授权。若本机Steam仍切回正式安装，再用独立虚拟机。新档和测试数据进入测试账户，正式角色不导入。

运行验收按以下实际顺序记录：

1. 未打补丁副本启动路径、数据写入位置、Cloud边界；创建空白新档、正常保存、退出重读。
2. 小样首次启动；实测独立保存区和guard失败时无正式用户写入；比较正式文件哈希。
3. 原作任务未完成不出现入口，完成且商队有效才出现；离营地/换房间/换角色不残留信使或界面。
4. 接取、暂缓、两种选择、按键与游戏暂停/热键、中文/英文及多分辨率布局；实体不能堵路。必要时改用原生对话。
5. 已接/已完成分别正常存读档，抄本可回看、重复互动无重复结算；原作任务/声望/物品未误改。
6. 干净小样通过后再验既有Mod组合。原生任务日志与实际房间入口完成并通过后才能称P2完成，之后进入R01/MQ02–04。

尚未复制到用户指定正式 `D:\SteamLibrary\steamapps\common\Stoneshard\msl\Mods`，尚未启用MSL、启动副本或加载正式档。本开发版不承诺旧档迁移、无损卸载或直接回原版。

关联设计库：`design/10_技术预研/首个开发包与离线验收.md`、`隔离测试与正式存档保护.md`、`MQ01_营火旁的迟信.md`。

依据：[GameMaker文件系统](https://manual.gamemaker.io/lts/en/Additional_Information/The_File_System.htm)、[game_save_id](https://manual.gamemaker.io/lts/en/GameMaker_Language/GML_Reference/General_Game_Control/game_save_id.htm)、[Steam启动接口](https://partner.steamgames.com/doc/api/steam_api#SteamAPI_RestartAppIfNecessary)。




0.1.4重复定向更新已验证：重编前从父CODE的ChildEntries移除旧回调，并清理旧SCRP/FUNCT，随后生成新回调。再次写出重读、真实链接和其他代码比较通过（artifacts/repeat-validation.json）；重复验收产物不自动部署，当前15:42已部署资源仍以direct-deployment.json为准。


