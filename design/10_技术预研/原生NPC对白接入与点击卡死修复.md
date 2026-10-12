---
title: "原生NPC对白接入与点击卡死修复"
id: TECH-009
type: implementation-record
status: draft
canon: mixed
baseline: "0.9.4.25-modbranch"
updated: 2026-10-11
tags: [stoneshard, implementation, dialogue]
aliases: []
---

# 原生NPC对白接入与点击卡死修复

最新S53反馈：用户确认0.1.5对白正常，仍有头像错位及长文书放在对白窗口的问题。0.1.6头像与背包文书改动见 [[信件物品与阅读驱动任务]]；不能把对白正常扩大成所有交互/存读档已通过。

> [!failure] 0.1.4运行失败，离线检查存在遗漏
> S52：用户实际运行在信使Create报告异常对象索引2144440064。下文0.1.4离线成功记录只代表当时已检查的项目，不能证明创建或对话成功；最新修复见本页0.1.5记录。

S51：用户实际点击0.1.3后卡住，没有对白窗口，并要求按原版做法修复。[[信使点击对话与输入锁]] 中自制面板路线判定运行失败，退出当前实现；不能将其离线验收记录当成互动已通过。关联 [[当前目录开发与回退]]、[[MQ01_营火旁的迟信]]、[[EAO函数链接错误与定向修复]]、[[来源登记]]。

## 本地原作接口证据

2026-10-11只读检查当前包0.9.4.25的指定事件和脚本，未导出原作源码全集。部分现代GML反编译器不能处理，改用原始指令核对，不能把反编译失败当成空函数。

- `o_simple_NPC` 继承 `o_unit`，Create完成单位、渲染、参数、技能映射及中立NPC字段初始化；Mouse_4通过 `event_perform_object(o_NPC, ev_mouse, ev_left_press)`复用原版左键，User_13同样调用原版NPC交互。
- `o_NPC.Mouse_4` 经GUI、行动、攻击模式等门槛，将玩家context_target_id指向人物，再触发User_13。User_13负责相邻距离、需要时的接近寻路、朝向和安全检查。
- `scr_npc_interact_start_dialogue()` → `scr_dialogue_start()`，使用当前NPC的字符串dialog_id。`scr_dialogue_context_create`装载数据，`scr_dialog_create`通过GUI容器创建真正的 `o_dialogue` 和 `o_dialogRender`，再由 `scr_dialogue_advance`推进节点。
- 原作数据含 `RootFragment / Monologue / Fragments / Speakers / Specs / Scripts`。Fragments表示下一节点或选项列表；Speakers是说话者到节点列表；instruction节点由Scripts方法执行。带action规范的动作在选项预览阶段不执行。
- 原生 `o_dialogue.Create`自行停止玩家、创建blockGUI和锁定输入；Destroy销毁自身blockGUI、解开玩家lock_movement并恢复镜头等原作流程。因此Mod不另建锁或手动接管退出。
- `scr_npc_dialogue_line_get_raw`从 `global.npc_lines_map`读取本地化行；上下文准备读取sex、occupation、playertype、faction、settlement等字段，然后按can_skip_checks决定筛选。Mod只注册自己的EAO键。

## 0.1.4实现

信使成为真正的 `o_simple_NPC` 子对象，Create先event_inherited初始化；保留原版Mouse、User_13、Draw、渲染更新和CleanUp。使用原生交互mask注册，停止日程AI，作为固定营地接信人。Controller只负责满足前置后生成、换图清理，不检测鼠标、不消费输入、不自绘面板。

新增 `eao_mq01` 原生对白数据，包含接信、比对、选择、登记和回看收条节点。中文/英文行在信使初始化时写入npc_lines_map；不修改原作对白表代码。原生窗口、选项按钮、自动接近和关闭行为由游戏处理，不再有自制右上关闭按钮或快捷键。

4个任务回调作为实例方法注册进该flow.Scripts；原生 `dialogue_eval_script`通过method/callv调用。它们不是裸名静态函数。链接验收要求4个匿名CODE方法都有SCRP/FUNCT记录，父条目先于子条目；继续拒绝0.1.1产生的裸名eao函数。状态变更仅放在action节点，避免显示选项时预先接任务或完成任务。

继续使用EAO_schema=1、EAO_MQ01=0/1/2等原有标量键。入口resume动作选择未接、已接、已完成对白，暂缓不丢进度；两个提交回调仅在MQ01=1时写入完成状态。选项标记technical，已看过的暂缓/回看选项不被原版去重隐藏。没有金币发放、背包新增物品或原生日志接入；[[MQ02_盐封的货单]]及外港地图尚未实现。

## 验证与运行边界

已完成0.1.4编译、实际MSL包读取、写出及重读。验证实际编译后的JSON可解析、所有边指向存在节点或原生终点、中文未被转义破坏、文本/说话者对应、任务动作具有action标签、选项可重复、方法真实链接，以及Controller不再包含旧输入锁。其他原有代码逐项反汇编比较不变，保存身份保留StoneShard。

0.1.4已收到用户实际创建失败反馈，尚未通过游戏内点击。需要验证：点击人物自动接近并出现原版窗口、全部选项、暂缓重开、两种提交、已完成回看、离开后移动/技能恢复、切房间和正常存读档。当前工具没有可用的原生桌面控制面，未自动启动游戏，不把离线通过写成运行通过。S51、S52的失败是实际反馈；新版本的预期行为与验收分开。

部署前保存当前资源、旧包、设置及完整用户目录，原vanilla保留；实际部署/备份路径和哈希以 `artifacts/direct-deployment.json` 为准。不恢复旧档覆盖最新进度。

2026-10-11 15:42已将0.1.4更新到当前data.win及msl/Mods/EmbersAndOaths.sml。备份 `backups/direct-20261011-154205-955` 包含修复前0.1.3资源、本Mod旧包、设置和完整用户目录；本次130个用户文件部署前后哈希不变，vanilla不变。用户目录数量较上次变化来自部署前现场，未回滚或覆盖任何玩家文件。实际弹窗仍待运行验证。

补充验收：对0.1.4候选包再执行一次定向更新，写出、重读、回调和其他代码一致性检查已通过，记录 `artifacts/repeat-validation.json`。该检查发现并修正工具对旧匿名方法的父对象ChildEntries引用清理顺序：重编前同时清理旧CODE/SCRP/FUNCT和父条目子引用，避免重读后出现残留子方法。本次重复更新只生成项目内验收产物，没有再次覆盖已部署资源或用户数据。

## 0.1.5：信使Create异常对象索引修复

S52用户报错为Create中的“Unable to find any instance for object index 2144440064”，调用方为Controller.BeginStep。已部署0.1.4反汇编显示：读取_flow.Scripts结构体后，四条instruction回调赋值均先conv.v.i，再pop到stacktop对象字段。这是把结构体接收者转为整数实例索引的错误指令路径，与报错吻合；尚未在游戏引擎逐指令追踪，因此不宣称已经证明异常具体发生地址。

本地原版 `gml_Script_scr_dialogue_context_create` 使用variable_struct_get/set及array_get操作上下文、节点和文本。0.1.5采用相同显式接口注册自己的4个回调和本地化行，移除自己的点赋值链；原版NPC父类、点击、接近和o_dialogue流程保留。资料：[GameMaker结构体写入](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Variable_Functions/variable_struct_set.htm)、[读取](https://manual.gamemaker.io/monthly/en/GameMaker_Language/GML_Reference/Variable_Functions/variable_struct_get.htm)。月度文档改用struct_get/set名称，本地接口按实际原版指令采用variable_struct_get/set。

编译0警告/0错误，实际MSL读取0.1.5包、写出重读、4回调链接、对白JSON图和非EAO代码一致性通过。新增EaoInteraction字节码检查拒绝conv.v.i后直接以stacktop为接收者的写入；自己的注册代码必须包含13个显式结构体写入与3个数组读取。`tools/Test-EaoStructRegression.ps1`对备份0.1.4给出预期拒绝，对已部署0.1.5通过；证据 `artifacts/struct-access-regression.json`。该检查针对这次实际编译回归，不等价于引擎运行测试。

2026-10-11 15:56已更新当前data.win及msl/Mods/EmbersAndOaths.sml。更新前备份 `backups/direct-20261011-155606-160` 保存0.1.4资源、旧包、MSL设置和完整用户目录。130个用户文件部署前后哈希不变，原vanilla不变。部署资源SHA256为 `2B78DD7141E69E3AC356D21CD7C3CC6BB933FE11BF2CCF789241F1D3F512A668`，最新记录见 `artifacts/direct-deployment.json`。实际启动、信使生成、点击、关闭与存读档仍待运行验证。
