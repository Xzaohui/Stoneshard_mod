---
title: "ModShardLauncher预研"
id: TECH-001
type: research
status: draft
canon: mixed
baseline: "0.9.4.25-modbranch"
updated: 2026-10-11
tags: [stoneshard, research]
aliases: []
---

# ModShardLauncher预研

当前方式已按用户最新选择改为现有目录直接开发，0.1.1使用原作保存路径；最新部署/组合更新规则见 [[当前目录开发与回退]]。下文隔离部署限制只描述此前选择，已不作为前置。

## 用户指定工具

[ModShardTeam/ModShardLauncher](https://github.com/ModShardTeam/ModShardLauncher) 已登记。工具以补丁形式处理Stoneshard数据；本地文件版本0.13.2.0。实现授权后已取得固定commit源码并使用本地DLL构建小样、离线打补丁；没有更新正式工具或启动MSL界面。当前证据见 [[首个开发包与离线验收]]。

[入门文档](https://modshardteam.github.io/ModShardLauncher/guides/start-modding.html)说明C# Mod、数据补丁及.sml分发流程。现已生成实际.sml并通过本地读取，尚未完成游戏内运行验收。

## 用户确认的输入与部署位置

S43：`vanilla.win`为原始`data.WIN`备份，当前`data.win`为现有Mods加载后的游戏资源包。默认新Mod构建以vanilla的冻结副本作为输入，当前data的副本用于组合兼容性研究；除非核验构建流程确有需要，不在当前已加载包上重复套用全部Mods。

用户指定实现后的加载目录为`D:\SteamLibrary\steamapps\common\Stoneshard\msl\Mods`，2026-10-11只读确认目录存在。未来交付.sml先保存到项目的产物目录并通过隔离验证，再复制到该Mods目录交由MSL加载。.sml是加载输入，MSL生成的data.win是补丁结果，vanilla是原版备份；三者不混为同类文件。

记录部署目录不等于打开正式MSL、改变现有启用列表或重建正式data.win。当前产物只复制到项目内启动器Mods；正式部署待完成 [[隔离测试与正式存档保护]] 与运行验收。

## 能力证据与未决问题

| 设计需求 | 文档中相关能力 | 尚未验证 |
| --- | --- | --- |
| 新NPC与实体 | AddObject、AddNewEvent | AI、对话、犯罪及日程衔接 |
| 任务和文本 | 代码/字符串/表操作 | 日志UI、真实任务状态接口 |
| 副本房间 | AddRoom、AddRoomJson、房间图层和实例 | 全球地图注册、边界、碰撞和重载 |
| 新敌人与奖励 | 敌人/装备表注入、掉落表 | 版本字段、平衡与动画 |
| 精准修改 | Load/Match/Act/Save链式补丁 | 本地脚本匹配和其他Mod顺序 |
| 持久化 | 需要代码/原作接口研究 | 没有确认安全存档扩展API |

依据：[API文档](https://modshardteam.github.io/ModShardLauncher/guides/api.html)。页面自述WIP且最后版本v0.11.1.0，早于本地0.13.2.0；不能直接把示例方法签名当本地已验证接口。AddRoom不等于自动扩大世界地图。

## 本地现状与风险

日志显示UTMT v0.6.1.0；已有ExportRoom.csx和若干物品表导出，但这些只证明本地工具文件存在。vanilla.win来源由用户确认，历史工具校验警告及其限制见 [[本地安装与证据]]。

需未来重点核对：原作调查结案和商队接口、全球地图生成/路径规划、剧情实体生命周期、存档、日常模板和本地化显示。

已有启用Mod：自动寻路（新地图/出口）、商队背包（容器/任务物）、物品详情（新物件标签）、手动存档（保存/恢复）、全图交易（经济）、稳定附魔（装备收益）。每类都有需验证的交叉点，不在本轮停用或修复。

后续进入实现时先固定干净游戏副本、启动器版本与源码commit，再做小范围验证。见 [[实施阶段与验证门槛]]。

公开DataLoader源码的文件选择与保存路径核对见 [[隔离测试与正式存档保护]]：可选择独立输入/输出不等于自动保护正式目录，保存会替换选中目标。源码已固定commit，实际编译/读取使用本地DLL；未证明源码与本地二进制逐字相同。
