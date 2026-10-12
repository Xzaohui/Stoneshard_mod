---
title: "MSL重复事件打包错误与正确输入"
id: TECH-006
type: issue-record
status: reviewed
canon: original-local
baseline: "0.9.4.25-modbranch"
updated: 2026-10-11
tags: [stoneshard, testing, msl]
aliases: []
---

# MSL重复事件打包错误与正确输入

用户报告MSL打包失败：`Cannot add the event Create_0 in o_msl_timer since it already exists`。本地MSL0.13.2.0日志 `log_20261011_1433.txt` 确认加载了当前已打其他Mods的data.win，失败发生于LogUtils.InjectLog，在本Mod执行之前。没有据此修改角色保存、删除MSL对象或更新启动器DLL。

## 原因和验证

MSL界面调用PatchFile，先注入日志对象/事件，再执行勾选Mod。当前组合包已有o_msl_timer；重复添加Create_0抛出异常。报错或取消保存后，内存包可能已被部分修改，直接重复点击打包也不可靠。

通过GameProbe调用**本地DLL**的LogUtils.InjectLog：对当前data直接复现相同异常（未调用任何Mod）；对用户确认的原始vanilla注入成功。只在内存中测试，没有写入游戏数据。源码commit与本地DLL的设置字段名不同，本地反射确认字段为EnableMods，不按公开main字段名猜测设置键。

## 正确重建步骤

1. 关闭并重新打开MSL，确保重新扫描Mod文件与启用设置。不要继续使用已报错的内存包。
2. 加载游戏目录的原始vanilla.win，不加载已打补丁data。
3. 确认勾选AutoPathfinder_Modified、CaravanBackpack_F2、DetailedItems、Manual Save、全图交易、StableEnchant及EmbersAndOaths。
4. 打包并保存为当前游戏data.win，保留vanilla原文件。取消/失败后先重新加载vanilla，不能直接重复点击保存。

上述MSL重建与项目Build/Deploy的增量输入要求不同：项目工具只执行EAO补丁，不重复运行MSL日志注入，因此可对无EAO的现有组合增量；原生MSL需要原版输入并重建所有勾选Mod。此前说明未充分区分两条路径，已纠正根README与开发说明。

## 已完成的准备

在 `msl/Mods - 副本` 找到六个原有启用包，只复制这六个到活动Mods，不额外启用其他备用Mods；复制前后哈希相同。保留EAO0.1.1。记录 `artifacts/restored-msl-packages.json`。

提升权限确认游戏已退出，MSL仍在运行。重新备份当前data、设置、七个Mod包、完整用户目录；核对130个用户文件及data哈希一致。记录 `artifacts/msl-rebuild-backup.json`。没有覆盖data、强制关闭MSL或改动角色存档。

增加只读 `tools/Test-MslInput.ps1`，拒绝含MSL/EAO对象标记的输入。标记检查通过不等于独立发行版/来源校验通过；用户对vanilla来源的说明保持有效。

已复现问题并验证原版日志注入；**未宣称MSL界面七Mod最终保存或游戏内运行已通过**，这需后续实际结果。与 [[当前目录开发与回退]]、[[ModShardLauncher预研]]、[[首个开发包与离线验收]]、[[来源登记]] 关联。

## 图标提示补充

用户随后报告 `Cannot find the icon.png associated to EmbersAndOaths.sml`。这是读取包时缺图标的提示；公开FileReader捕获缺图标异常并保留包，界面提供默认图标，不等同于Create重复事件异常。

2026-10-11已加入自制矢量图标源 `src/EmbersAndOaths/Assets/icon.xaml`，打包时渲染128×128 PNG并嵌入 `EmbersAndOaths\icon.png`。本地MSL实际读出Icon共4922字节，与源PNG一致、解码成功；已更新指定Mods目录包并再次读入验证。备份旧包及当前资源/设置/用户数据；data和设置未变化。记录 `artifacts/icon-deployment.json`。剧情代码未改，版本仍为0.1.1；图标不属于原作美术。重开MSL刷新即可读取新图标。
