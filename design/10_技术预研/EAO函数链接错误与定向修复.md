---
title: "EAO函数链接错误与定向修复"
id: TECH-007
type: implementation-record
status: draft
canon: mixed
baseline: "0.9.4.25-modbranch"
updated: 2026-10-11
tags: [stoneshard, implementation, debugging]
aliases: []
---

# EAO函数链接错误与定向修复

用户后续确认0.1.2已能看到人物，但无法互动；这只确认启动与人物出现，不能视为任务完成验证。0.1.3改鼠标交互，见 [[信使点击对话与输入锁]]。

来源S49：用户实际启动0.1.1时报告 `Error on load / Unable to find function eao_cn`。这推翻了“资源序列化成功即可启动”的假设；此前离线结果没有证明运行成功。关联 [[当前目录开发与回退]]、[[MSL重复事件打包错误与正确输入]]、[[首个开发包与离线验收]]、[[实施阶段与验证门槛]]、[[来源登记]]。

## 本地证据与修复

用安装内MSL0.13.2.0和UndertaleModLib0.6.1.0读取当前data：controller Create包含七个匿名方法，SCRP只有匿名名称，FUNCT却有裸名 `eao_cn/eao_ready/eao_eligible/eao_get/eao_set/eao_complete/eao_text`，对应指令为 `call.i eao_*`。匿名实例方法被编成无法解析的静态调用，包可读写但运行器加载失败。这个结论来自当前包，不依赖公开main与本机DLL完全相同的假设。

0.1.2将小样辅助逻辑移到对应事件内，语言选择使用局部变量和条件表达式，状态操作调用原生ds_map接口。移除旧七个匿名CODE/SCRP条目及错误函数条目，保留信使和 [[MQ01_营火旁的迟信]] 的五页面、状态键、两种选择与无金币奖励。未接取与已完成状态不能再次结算。尚未添加新地图或原生日志。

当前data与14:38的无EAO组合备份至少有一处非EAO代码差异，因此拒绝用旧组合覆盖。实际执行 `GameProbe --repair-eao`，只改三个controller事件；原loader及其余所有代码在内存和序列化重读后逐项反汇编比较一致。旧错误版本作为负例，新增链接检查确实拒绝七个裸名引用；新版在写出前及重读后通过同一检查。

## 部署与边界

2026-10-11 14:57完成当前安装部署：更新data.win与 `msl/Mods/EmbersAndOaths.sml`。备份目录 `backups/direct-20261011-145730-810` 包含修复前data、MSL设置、旧包和完整用户目录。原vanilla及130个用户文件哈希未变，没有恢复或修改角色存档；设置仅去重本Mod启用项，保留其他名称。证据为 `artifacts/direct-validation.json` 和 `direct-deployment.json`，仅本地保存，不上传个人数据与商业资源。

此时活动Mods目录只读观察只有EmbersAndOaths.sml，不能凭旧启用名称认定其他包仍在。定向修复保留当前data的其他代码；如以后从vanilla全量重建，先确认所需旧包实际存在。此前六包恢复是14:38的历史观察，不是持续状态保证。

本次修复输入已含EAO，不标成pre-EAO基线。部署记录使用targetedRepair及repairSourceData；后续构建对已识别的EAO小样更新三个事件，避免重复增加对象和日志。未知结构拒绝更新。

> [!warning] 验证范围
> 链接检查、包图标读取、资源写出重读和文件哈希通过；没有自动启动游戏。修复后的首次启动、任务交互、存读档、换角色仍待实际运行。`runtimeVerified`保持false，不用离线验收替代运行验收。
