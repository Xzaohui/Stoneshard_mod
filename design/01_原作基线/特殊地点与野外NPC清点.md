---
title: "特殊地点与野外NPC清点"
id: SRC-SPECIAL-LOC-S92
type: source
status: draft
canon: mixed
baseline: "0.9.4.25-modbranch"
updated: 2026-10-13
tags: [stoneshard, S92, source, special-locations]
aliases: []
---

# 特殊地点与野外NPC清点

本页是[[特殊地点与野外NPC对白扩展计划]]第一步的只读清点结果：从本地原版包枚举世界地图区域、特殊地点候选与地形类型名，并登记对白族规模。数据源为只读扫描，**只保存键名、STRG序号、中文可用性与短地点名**，不保存对白全文、反编译源码或图集；逐NPC中英对读、野外遭遇映射与地点设计卡是后续步骤。

> [!info] 来源与指纹
> 文件 `D:\SteamLibrary\steamapps\common\Stoneshard\vanilla.win`；SHA-256 `99965AB8E26A07C9…`；160641056 字节；STRG 122200 条；清点日期 2026-10-13。
> 与 `research/local-baseline.json` 的候选基线指纹一致；当前 `data.win` 组合包不用于本清点。

方法：读取 STRG 字符串表；简体槽取首个含汉字且不含假名/谚文的字段。键存在不证明场景在游戏中可达；名字与游戏内显示不一致时以游戏为准。

## 世界地图区域（8）

|键|STRG|中文名|English|
|---|---|---|---|
|`map_abbey`|32468|修院周边地图|Map of the Abbey Surroundings|
|`map_brynn`|32471|布林城郊地图|Map of Brynn Outskirts|
|`map_freevalley`|32470|自由谷地图|Map of the Free Vale|
|`map_mannshire`|32472|曼郡村郊地图|Map of Mannshire Outskirts|
|`map_oldhomestead`|32467|老宅子周边地图|Map of the Old Homestead Surroundings|
|`map_osbrook`|32473|奥斯布鲁克村郊地图|Map of Osbrook Outskirts|
|`map_plaguevillage`|32466|阿尔内姆村郊地图|Map of Arnem Outskirts|
|`map_rottenwillow`|32469|烂柳周边地图|Map of the Rotten Willow Surroundings|

## 特殊地点候选（44）

地点名取自传闻条目的地点槽（中文与官方英文名并列）；`对白入口`为已配到的传闻对白条目数（本条只计数量，不存文本）。

|键|STRG|中文名|English|对白入口|已知所属城镇|
|---|---|---|---|---:|---|
|`rumor_abandonedQuarry1`|15331|石场|Quarry|1|待核|
|`rumor_abandonedWatermill1`|15316|水车磨坊|Watermill|1|待核|
|`rumor_abbey1`|15321|亵渎的修院|Defiled Monastery|1|待核|
|`rumor_banditRuins1`|15322|德·勒布朗的庄园|Der Lebron's Manor|1|待核|
|`rumor_bearHG1`|15351|熊的领地|Bear Territory|1|待核|
|`rumor_bearHG2`|15350|熊的领地|Bear Territory|1|待核|
|`rumor_camp1`|15338|土匪营地|Brigand Camp|1|待核|
|`rumor_camp2`|15337|荒废营地|Desolate Camp|1|待核|
|`rumor_camp3`|15336|营地|Encampment|1|待核|
|`rumor_camp4`|15335|兵营|Campsite|1|待核|
|`rumor_camp5`|15334|空地营帐|Camp on a Clearing|1|待核|
|`rumor_cave1`|15313|洞穴|Cave|1|待核|
|`rumor_cave2`|15312|洞穴|Cave|1|待核|
|`rumor_cave3`|15311|洞穴|Cave|1|待核|
|`rumor_cave4`|15310|洞穴|Cave|1|待核|
|`rumor_cave5`|15309|洞穴|Cave|1|待核|
|`rumor_cave6`|15308|洞穴|Cave|1|待核|
|`rumor_crawlerBurrow1`|15340|巨蛛洞|Crawler Burrow|1|待核|
|`rumor_ghoulDen1`|15343|食尸鬼巢穴|Ghoul Den|1|待核|
|`rumor_ghoulDen2`|15342|食尸鬼巢穴|Ghoul Den|1|待核|
|`rumor_grazingHG1`|15347|猎场|Hunting Grounds|1|待核|
|`rumor_grazingHG2`|15346|猎场|Hunting Grounds|1|待核|
|`rumor_grazingHG3`|15345|猎场|Hunting Grounds|1|待核|
|`rumor_harpyNest1`|15341|哈比窝|Harpies Nest|1|待核|
|`rumor_hermitHut1`|15330|药师家|Herbalist's House|1|Mannshire|
|`rumor_homestead1`|15324|安静的农宅|Quiet Homestead|1|待核|
|`rumor_homesteadAbandoned1`|15323|荒废的农宅|Abandoned Homestead|1|待核|
|`rumor_homesteadLooted1`|15328|裁缝宅子|Tailor's Homestead|1|待核|
|`rumor_hornetHive1`|15339|亡蜂巢|Deathstinger Hive|1|待核|
|`rumor_leprosy1`|15333|老麻风院|Old Leprosarium|1|待核|
|`rumor_mine1`|15315|矿洞|Mine|1|待核|
|`rumor_mine2`|15314|矿洞|Mine|1|待核|
|`rumor_mooseHG1`|15344|驼鹿的踪迹|Moose Trail|1|待核|
|`rumor_plagueVillage1`|15327|瘟村|Plague Village|1|待核|
|`rumor_ralphSons1`|15325|拉尔夫记旅馆|Albergue Ralph e Hijos|1|待核|
|`rumor_remoteBastion1`|15320|老城堡|Old Castle|1|待核|
|`rumor_remoteBastion2`|15319|固若金汤的堡垒|Impregnable Fort|1|Mannshire|
|`rumor_remoteCatacombs1`|15318|神圣的废墟|Sacred Ruins|1|待核|
|`rumor_remoteCrypt1`|15317|英雄陵墓|Hero's Mausoleum|1|待核|
|`rumor_rottenWillow1`|15326|烂柳酒馆|Rotten Willow Tavern|1|待核|
|`rumor_siegeCamp1`|15329|围城营地|Siege Camp|1|Brynn|
|`rumor_witchHut1`|15332|女巫|Witch|1|待核|
|`rumor_wolfHG1`|15349|狼的踪迹|Wolf Trail|1|待核|
|`rumor_wolfHG2`|15348|狼的踪迹|Wolf Trail|1|待核|

## 地形与类型名（13）

|键|STRG|中文名|English|
|---|---|---|---|
|`Area_Wilderness`|25852|区域野性|Area Wilderness|
|`Camp`|17606|营地|Camp|
|`Cave01`|17493|潮湿谷地|Damp Ravine|
|`Cave02`|17492|青苔断崖|Mossy Ledge|
|`Cave03`|17491|三刀会窝点|Three Knives Hideout|
|`Cave04`|17490|野兽洞穴|Beast Burrow|
|`Cave05`|17489|老梣树|Gnarly Ash|
|`Cave06`|17488|暴雨谷地|Storm Hollow|
|`Cave07`|17487|锈矿山|Rusty Mine|
|`Cave08`|17486|迷烟地道|Smoky Tunnel|
|`Cave09`|17485|渡鸦裂口|Raven Cleft|
|`Cave10`|17484|奥拉夫的巷道|Olaf's Shaft|
|`Field`|17697|原野|Field|

## 对白族规模

场景 326、问候 446、闲谈 125、NPC 227、随从 8；逐条键/序号/说话人槽见 `research/original-dialogue-inventory.json`，本页不重复。

## 未核与边界

- 键存在、有中文名都不证明玩家能到达、能触发对白或地点仍在当前版本使用；需按计划逐项做场景核对。
- 传闻地点名为通用名（如「洞穴」「矿洞」），同名地点可能多处；具体位置与原文语境需逐条读取对白后才能定。
- 只读扫描，未改游戏包、未触玩家存档；逐NPC中英对读、Mod原创特殊地点清点与地点设计卡见后续步骤。

[[特殊地点与野外NPC对白扩展计划]] · [[原作剧情与对话系统参照]] · [[来源登记]] · [[任务台本总索引]]
