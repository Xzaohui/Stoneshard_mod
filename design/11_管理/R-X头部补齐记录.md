---
title: "R-X头部补齐记录"
id: MGMT-RX-HEADERS-S141
type: review
status: draft
canon: mod-original
baseline: "0.9.4.25-modbranch"
updated: 2026-10-13
tags: [stoneshard, S141, review, screenplay]
aliases: []
---

# R-X头部补齐记录

按 S62「各台本顶部 R/X 为准」的口径核对城市稿：**79 篇**中 14 篇原有 R/X 头（`当前R/X` 或 `R：方法与提交`），**65 篇**带派生块。派生块只由脚本内既有内容生成——方法小节标题、`resolve_`／`paid_` 键与回访人物——不新增设定、不改动既有文字；插入前后逐篇比对，除新块外文本逐字相同。登记 `research/rx-headers.json`，工具 `research/tools/Write-RXHeaders.py`。

## 派生规则

- R（方法）：取「可执行方案与回访」小节内 `### 标签：名称` 标题，按原顺序列出；
- X（后续）：取全篇 `resolve_*`／`paid_*` 键（去重排序）与同节回访行的人物链接名；
- 块尾注明来源，便于后续维护者区分"原作文字"与"派生索引"。

## 逐篇登记

| 脚本 | 本轮插入 | 方法 | 写入键 | 回访人物 |
| --- | --- | --- | --- | --- |
| CM-ALD | 派生 | `open：匿名责任公开与独立支架复测` · `distributed：修护者共同保技术，逐户独立索赔` · `seal：由单一工艺赞助保全部记录` | `paid_CM_ALD`、`resolve_CM_ALD` | 赫莲·金、埃墨·衬、维安、芬珂、奈汀 |
| CM-ASH | 原有 | `localcare：留营与有限物资接续` · `distributedcare：本人自选分散安置` | `paid_CM_ASH`、`resolve_CM_ASH` | 米娅、琳汀·床、枯恩 |
| CM-BRY | 派生 | `civic：受害人主导的跨区有限听证` · `separate：分案处理，不组统一阵线` · `patron：接受单方赞助换受控救助` | `paid_CM_BRY`、`resolve_CM_BRY` | 赫林、奥辛·锤、米罗·账、阿薇、蕾娜·维尔、薇特·灰 |
| CM-DEN | 派生 | `shared：临时分住与共同修第二屋` · `leases：独立短租与驿站补位` | `paid_CM_DEN`、`resolve_CM_DEN` | 瑟芬·网、蓓薇、欧铎、卡蕾·棚 |
| CM-EED | 派生 | `oldstock：核旧材履约，限制搜家` · `localfirst：退部分城市预款，保林与本地用材` | `paid_CM_EED`、`resolve_CM_EED` | 奥菈·纹、芦雅、黎恩·岗 |
| CM-FOR | 派生 | `workerstop：工人自愿组与维护停井权` · `external：外部专业停井与限期工资托柜` | `paid_CM_FOR`、`resolve_CM_FOR` | 艾珀·风、祁铎、西婕、玛诺·灯 |
| CM-HIG | 原有 | `maintenance：共同维护边界与停工条款` · `minimal：固定图独行与有限专业委托` | `paid_CM_HIG`、`resolve_CM_HIG` | 古菈、艾萝·图、图里 |
| CM-KOR | 派生 | `limited：分用途取物证明与独立租住` · `custody：中立寄存争议物，先保障独立住所` | `paid_CM_KOR`、`resolve_CM_KOR` | 埃文·行、诺妲·门、塔斐 |
| CM-MAE | 派生 | `separate：三类记录分开保护与问责` · `evacuate：自愿迁藏与分散供给` · `control：接受地方动员者统一控制名册` | `paid_CM_MAE`、`resolve_CM_MAE` | 塞娜·里德、玛娅·禾、艾娜、莉德、古岚、尼芙 |
| CM-MNS | 派生 | `newlabel：用新年份与双来源售有限新酒` · `limited：旧家标只保来处，逐瓶注明新酿` | `paid_CM_MNS`、`resolve_CM_MNS` | 罗莎·藤、提奥·桶、墨达 |
| CM-OSB | 派生 | `seed：保留底种，有限共同过渡粮` · `advance：独立预购来年有限产出` | `paid_CM_OSB`、`resolve_CM_OSB` | 芙朵·谷、瓦森·磨、布希、德娅 |
| CM-PAS | 派生 | `joint：民军有限共同核查` · `neutral：中立分别复核与普通旁路` | `paid_CM_PAS`、`resolve_CM_PAS` | 雷奥·凯斯、莎帛、辛娅、莫伦·海 |
| CM-RAT | 派生 | `addendum：保英雄记述，补受害者独立附碑` · `family：各家独立记忆与赔付，不办统一纪念` | `paid_CM_RAT`、`resolve_CM_RAT` | 阿莉·铃、妮耶、伊默·栅、芬罗 |
| CM-SKO | 派生 | `repay：会计认挪款，缩产分期偿公款` · `sale：售非必需旧坯，先退公款` | `paid_CM_SKO`、`resolve_CM_SKO` | 妮莎·炉、博赫·冷、莉葵 |
| CM-YOS | 派生 | `sharedmark：来源分署，家纹仅代表工序` · `independent：分开工坊和家纹，徒弟独立接单` | `paid_CM_YOS`、`resolve_CM_YOS` | 塔雅·梭、缇娜·染 |
| CS-ALD-01 | 派生 | `a：限定署名` · `b：本人私存来源` | `paid_CS_ALD_01`、`resolve_CS_ALD_01` | 芬珂、科纳 |
| CS-ALD-02 | 派生 | `a：分仪式同补助` · `b：简葬封争议` | `paid_CS_ALD_02`、`resolve_CS_ALD_02` | 伊榕、司诺·庭、穆柯、萝铎 |
| CS-ALD-03 | 派生 | `a：纯赠与有限事实` · `b：拒礼普通替代` | `paid_CS_ALD_03`、`resolve_CS_ALD_03` | 索芮、奈汀、萝铎 |
| CS-ALD-04 | 派生 | `a：历史限范围` · `b：退虚标游约` | `paid_CS_ALD_04`、`resolve_CS_ALD_04` | 齐勒、布娅 |
| CS-ALD-05 | 派生 | `a：匿名工伤审查` · `b：独立代理索赔` | `paid_CS_ALD_05`、`resolve_CS_ALD_05` | 索芮、赫莲·金、维安 |
| CS-ALD-06 | 派生 | `a：如实限量申报` · `b：本地用旧件` | `paid_CS_ALD_06`、`resolve_CS_ALD_06` | 奇恩、萝铎、赫莲·金、维安 |
| CS-ASH-01 | 原有 | `a：有限安全取物` · `b：本人代取与争议封存` | `paid_CS_ASH_01`、`resolve_CS_ASH_01` | 妮蔻、缇安、安妮 |
| CS-ASH-02 | 原有 | `a：本人换护理` · `b：限期轮班` | `paid_CS_ASH_02`、`resolve_CS_ASH_02` | 奥娅、枯恩、安妮 |
| CS-ASH-03 | 原有 | `a：普通底量` · `b：停止本批观察` | `paid_CS_ASH_03`、`resolve_CS_ASH_03` | 枯恩、琳汀·床、苏奈、安妮 |
| CS-BRY-01 | 派生 | `continuity：跨巷限定居住见证` · `exit：撤争议租约，独立短租与申诉` | `paid_CS_BRY_01`、`resolve_CS_BRY_01` | 佩兰、蕾娜·维尔、麦勒 |
| CS-BRY-02 | 派生 | `dual：双见证保留分歧` · `private：各家私存，公共空间作安全住所` | `paid_CS_BRY_02`、`resolve_CS_BRY_02` | 伊芙、奥辛·锤、蕾娜·维尔 |
| CS-BRY-03 | 派生 | `shared：工艺分署与有限续作` · `leave：独立小棚与退未做订单` | `paid_CS_BRY_03`、`resolve_CS_BRY_03` | 安菈、沃伦 |
| CS-BRY-04 | 派生 | `publicnotice：有限公益版与分区事实核验` · `doorway：逐户限权通告，不强占印版` | `paid_CS_BRY_04`、`resolve_CS_BRY_04` | 乔彤、米罗·账、薇特·灰 |
| CS-BRY-05 | 派生 | `limit：限量交约并赔未授权部分` · `future：城镇知情预购未来有限份` | `paid_CS_BRY_05`、`resolve_CS_BRY_05` | 芮莎、米罗·账 |
| CS-BRY-06 | 派生 | `amend：本人限权补见证，不强领勋` · `record：私存见证并退错误个人功份` | `paid_CS_BRY_06`、`resolve_CS_BRY_06` | 薇特·灰、蕾娜·维尔、维松 |
| CS-BRY-07 | 派生 | `limited：限用途供观察，赔付不换沉默` · `refuse：拒出售用途，转中立有限护理` | `paid_CS_BRY_07`、`resolve_CS_BRY_07` | 陶芮、哈塞、米罗·账 |
| CS-BRY-08 | 派生 | `reserve：限期保物，航次席改为供给` · `release：退出航次约，独立存物与有限款清算` | `paid_CS_BRY_08`、`resolve_CS_BRY_08` | 米蕾、奥德、薇特·灰 |
| CS-BRY-09 | 派生 | `homes：先隔低屋风险，商业损失另赔` · `splitflow：有限临时两段分流` | `paid_CS_BRY_09`、`resolve_CS_BRY_09` | 洛妲、米罗·账、芮莎 |
| CS-BRY-10 | 派生 | `mandates：各群体有限授权席` · `separate：不同地点分案协商` | `paid_CS_BRY_10`、`resolve_CS_BRY_10` | 奥辛·锤、米蕾、米罗·账、蕾娜·维尔 |
| CS-BRY-11 | 原有 | — | `paid_CS_BRY_11`、`resolve_CS_BRY_11` | — |
| CS-BRY-12 | 原有 | — | `paid_CS_BRY_12`、`resolve_CS_BRY_12` | — |
| CS-BRY-13 | 原有 | — | `paid_CS_BRY_13`、`resolve_CS_BRY_13` | — |
| CS-BRY-14 | 原有 | — | `paid_CS_BRY_14`、`resolve_CS_BRY_14` | — |
| CS-BRY-15 | 原有 | — | `paid_CS_BRY_15`、`resolve_CS_BRY_15` | — |
| CS-BRY-16 | 原有 | — | `paid_CS_BRY_16`、`resolve_CS_BRY_16` | — |
| CS-DEN-01 | 派生 | `a：分船接应` · `b：同船但分授权` | `paid_CS_DEN_01`、`resolve_CS_DEN_01` | 欧铎、坦瑟、艾蕾、卡蕾·棚 |
| CS-DEN-02 | 派生 | `a：共用分权` · `b：各自有限网份` | `paid_CS_DEN_02`、`resolve_CS_DEN_02` | 娜泽、瑟芬·网、卡蕾·棚 |
| CS-DEN-03 | 派生 | `a：分开生活与仪式` · `b：独立侧屋租住` | `paid_CS_DEN_03`、`resolve_CS_DEN_03` | 伊蕾、薇柯 |
| CS-EED-01 | 派生 | `a：有限病伐` · `b：旧料替代` | `paid_CS_EED_01`、`resolve_CS_EED_01` | 苏槿、葛黎 |
| CS-EED-02 | 派生 | `a：先安置后有限拆` · `b：拒拆独立旧材` | `paid_CS_EED_02`、`resolve_CS_EED_02` | 岱里、布泽、芦雅 |
| CS-EED-03 | 派生 | `a：限林段通报` · `b：独立巡林点` | `paid_CS_EED_03`、`resolve_CS_EED_03` | 黎恩·岗、朔娅、欧莎 |
| CS-FOR-01 | 派生 | `a：历史限权展示` · `b：家内寄存` | `paid_CS_FOR_01`、`resolve_CS_FOR_01` | 艾钦、科蔚、祁铎 |
| CS-FOR-02 | 派生 | `a：赔付与排水分约` · `b：临停支流与外水` | `paid_CS_FOR_02`、`resolve_CS_FOR_02` | 蓓娜、科蔚、洛芙 |
| CS-FOR-03 | 派生 | `a：收益劳动拆开` · `b：售有限份退出` | `paid_CS_FOR_03`、`resolve_CS_FOR_03` | 艾钦、祁铎 |
| CS-HIG-01 | 原有 | `a：独立验段` · `b：保绕行不修` | `paid_CS_HIG_01`、`resolve_CS_HIG_01` | 图里、赫珀、蕾因 |
| CS-HIG-02 | 原有 | `a：保误差复测` · `b：换独立支架` | `paid_CS_HIG_02`、`resolve_CS_HIG_02` | 司榆、艾萝·图、维菈 |
| CS-HIG-03 | 原有 | `a：续约逐人` · `b：缩外段便利` | `paid_CS_HIG_03`、`resolve_CS_HIG_03` | 古菈、艾萝·图、赫珀 |
| CS-KOR-01 | 派生 | `a：按授权清租` · `b：封争议款保短宿` | `paid_CS_KOR_01`、`resolve_CS_KOR_01` | 玛迪、娜娅 |
| CS-KOR-02 | 派生 | `a：本人领物` · `b：代理分项` | `paid_CS_KOR_02`、`resolve_CS_KOR_02` | 赛洛、尤恩、卢绫 |
| CS-KOR-03 | 派生 | `a：未知如实售` · `b：留存开放核` | `paid_CS_KOR_03`、`resolve_CS_KOR_03` | 碧珞、榭兰、玛迪 |
| CS-MAE-01 | 派生 | `a：匿名限次售` · `b：保物独立救助` | `paid_CS_MAE_01`、`resolve_CS_MAE_01` | 维芮、多罗 |
| CS-MAE-02 | 派生 | `a：分箱` · `b：迁藏封柜` | `paid_CS_MAE_02`、`resolve_CS_MAE_02` | 欧岚、尼芙、薇榆 |
| CS-MAE-03 | 派生 | `a：照护与席位分开` · `b：中立接收班` | `paid_CS_MAE_03`、`resolve_CS_MAE_03` | 缇弗、玛娅·禾、贝诺 |
| CS-MAE-04 | 派生 | `a：有限续作` · `b：独立工棚` | `paid_CS_MAE_04`、`resolve_CS_MAE_04` | 扎禾、菲勒·火 |
| CS-MAE-05 | 派生 | `a：独立来源复核` · `b：技术保源私柜` | `paid_CS_MAE_05`、`resolve_CS_MAE_05` | 莉德、塞娜·里德、薇榆 |
| CS-MAE-06 | 派生 | `a：留城接续` · `b：自愿分批出城` | `paid_CS_MAE_06`、`resolve_CS_MAE_06` | 尼芙、艾娜、玛娅·禾 |
| CS-MNS-01 | 派生 | `a：护理优先退酒款` · `b：分量与替代` | `paid_CS_MNS_01`、`resolve_CS_MNS_01` | 凯诺、罗莎·藤、芙伦、贝洛 |
| CS-MNS-02 | 派生 | `a：双来源` · `b：独立小作` | `paid_CS_MNS_02`、`resolve_CS_MNS_02` | 凯诺、贝洛 |
| CS-MNS-03 | 派生 | `a：一季分收` · `b：补投入迁枝` | `paid_CS_MNS_03`、`resolve_CS_MNS_03` | 赛芙、琼荷、罗莎·藤 |
| CS-OSB-01 | 派生 | `a：本人限期工约` · `b：保村内独立学作` | `paid_CS_OSB_01`、`resolve_CS_OSB_01` | 芙朵·谷、多恩、洛珊 |
| CS-OSB-02 | 派生 | `a：开独立门` · `b：限期共围续约` | `paid_CS_OSB_02`、`resolve_CS_OSB_02` | 雷玛、沃达、芮茵 |
| CS-OSB-03 | 派生 | `a：婚与地分开` · `b：暂停婚约清礼` | `paid_CS_OSB_03`、`resolve_CS_OSB_03` | 蔻芙、雅铎、德娅 |
| CS-PAS-01 | 派生 | `a：工资托柜` · `b：旁路有限运量` | `paid_CS_PAS_01`、`resolve_CS_PAS_01` | 乌珀、沃汀、雷奥·凯斯 |
| CS-PAS-02 | 派生 | `a：编号分柜` · `b：本人有限实名` | `paid_CS_PAS_02`、`resolve_CS_PAS_02` | 礼昂、莎帛、辛娅 |
| CS-PAS-03 | 派生 | `a：有限家书` · `b：代理口信` | `paid_CS_PAS_03`、`resolve_CS_PAS_03` | 列梵、雷奥·凯斯、绮伦 |
| CS-RAT-01 | 派生 | `a：分两案` · `b：暂新护旧争` | `paid_CS_RAT_01`、`resolve_CS_RAT_01` | 芬罗、伊默·栅、瑟铎 |
| CS-RAT-02 | 派生 | `a：注明仿与退款` · `b：停售独立存原` | `paid_CS_RAT_02`、`resolve_CS_RAT_02` | 佩菈、米菈 |
| CS-RAT-03 | 派生 | `a：给付与仪式分开` · `b：各家小纪念` | `paid_CS_RAT_03`、`resolve_CS_RAT_03` | 阿莉·铃、伊默·栅、妮耶、佩菈 |
| CS-SKO-01 | 派生 | `a：封款拆用途` · `b：退单保工资` | `paid_CS_SKO_01`、`resolve_CS_SKO_01` | 古烈、妮莎·炉、布岚 |
| CS-SKO-02 | 派生 | `a：本人限权见证` · `b：安静归乡` | `paid_CS_SKO_02`、`resolve_CS_SKO_02` | 博赫·冷、雷哈 |
| CS-SKO-03 | 派生 | `a：限污染` · `b：停沟替水` | `paid_CS_SKO_03`、`resolve_CS_SKO_03` | 古烈、温诺、妮莎·炉 |
| CS-YOS-01 | 派生 | `a：底量限售` · `b：替代交换` | `paid_CS_YOS_01`、`resolve_CS_YOS_01` | 尤尔、呼蕾、莉葵 |
| CS-YOS-02 | 派生 | `a：离乡限款` · `b：自愿延期` | `paid_CS_YOS_02`、`resolve_CS_YOS_02` | 缇娜·染、塔雅·梭、梅蓓 |
| CS-YOS-03 | 派生 | `a：查班分流` · `b：停新管仲裁` | `paid_CS_YOS_03`、`resolve_CS_YOS_03` | 阿洛、溪悠、缇娜·染、昂朵 |

## 边界

- 派生块是索引，不是新设定；方法、键与回访名一律以脚本正文为准。
- 校验器逐篇重算：块内方法与正文小节一致、键来自正文、插入不改变既有文字。
- 主线／支线／日常／副本（`N`／`SQ`／`DT`／`D`）另有「可执行解法＋本任务影响的后事」与 `-R-` 键名体系，不属本次补齐范围。

[[质量守卫总表]] · [[逐角色稿完成度核对]] · [[任务台本总索引]] · [[逻辑验收记录]]
