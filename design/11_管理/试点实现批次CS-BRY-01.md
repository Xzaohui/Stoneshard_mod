---
title: "试点实现批次CS-BRY-01"
id: MGMT-PILOT-BRY01-S156
type: guide
status: draft
canon: mod-original
baseline: "0.9.4.25-modbranch"
updated: 2026-10-13
tags: [stoneshard, S156, guide, implementation]
aliases: []
---

# 试点实现批次CS-BRY-01

[[试点实现批次N2]] 覆盖主章单案；本页是**系统层**试点：城市支线 `CS-BRY-01 一年之后`——含两条互斥路线、早到/晚到回执、拒绝/缺席、以及**服务班／信任档／闲谈池**三套系统的接线。仅排程与输入提取，不含实现代码、不部署；数据 `research/pilot-batch-cs-bry-01.json`。

## 输入（现场提取）

| 项 | 数量 | 明细 |
| --- | ---: | --- |
| 事件桩 | 14 | `evt_CS_BRY_01_entry`、`evt_CS_BRY_01_hub`、`evt_CS_BRY_01_route_continuity`、`evt_CS_BRY_01_route_exit`、`evt_CS_BRY_01_feedback_1_early`、`evt_CS_BRY_01_feedback_1_late`、`evt_CS_BRY_01_feedback_2_early`、`evt_CS_BRY_01_feedback_2_late`、`evt_CS_BRY_01_feedback_3_early`、`evt_CS_BRY_01_feedback_3_late`、`evt_CS_BRY_01_refusal`、`evt_CS_BRY_01_absent`、`evt_CS_BRY_01_before_city`、`evt_CS_BRY_01_after_city` |
| 状态键 | 10 | `encountered_CS_BRY_01`、`resolve_CS_BRY_01`、`callback_CS_BRY_01_continuity`、`consent_CS_BRY_01_continuity`、`paid_CS_BRY_01_continuity`、`callback_CS_BRY_01_exit`、`consent_CS_BRY_01_exit`、`paid_CS_BRY_01_exit`、`presence_CS_BRY_01`、`order_CS_BRY_01` |
| 条件流节点 | 14 | `entry`、`hub`、`route.continuity`、`route.exit`、`feedback.1.early`、`feedback.1.late`、`feedback.2.early`、`feedback.2.late`、`feedback.3.early`、`feedback.3.late`、`refusal`、`absent`、`before_city`、`after_city` |
| 解法（R） | 2 | `continuity：跨巷限定居住见证`、`exit：撤争议租约，独立短租与申诉` |
| X 边 | 0 | — |

## 系统层接线（与本案的关系）

- **服务班**：`SVC-BRY`「小批货样核验与运单誊写班」（经办 `米罗·账`），有限库存 样扣核验：每批3件、布样核验：每批2幅、运单誊写：每案1份；本案只走普通运单誊写，不触银行／海关／货栈账。
- **信任档**：布林五档只改范围与便利（−2 关闭／−1 限范围／0 基础／+1 一处小便利／+2 预约与转介）；本案结算不因档位改结论。
- **闲谈池**：城镇池（本案相关 4 条）与声望档池（2 条）**分池播放**；中间档不播档位池，闲谈不改任何结算。

## 落地顺序

1. **键落库**：先建 10 键——`encountered_CS_BRY_01`、`resolve_CS_BRY_01`（none/continuity/exit）、两条路线各自的 `callback_/consent_/paid_`、`presence_CS_BRY_01`（四态）、`order_CS_BRY_01`（early/late/unknown）。
2. **桩→事件**：14 桩一一对应（入口/枢纽/两条路线/三组早晚回执/拒绝/缺席/城前/城后）；回执桩读 `order_*` 决定早或晚。
3. **台词接线**：按 [[全库条件流投影]] 的 `refs` 逐字接入；`consent_*` 只在本人分项授权后写，`paid_*` 只在真实交付后写。
4. **系统接线**：服务班与闲谈池按上节规则落地；柜台句与街头反应分池，低档不删基本安全。
5. **验收**：见下节场景；编译侧须与候选包同一 SHA，运行按 [[试玩路线与检查单]] 记录。

## 验收场景

| 场景 | 名称 | 期望写入 | 不得发生 |
| --- | --- | --- | --- |
| BRY01-T01 | 接取与首见 | `encountered_CS_BRY_01`＝`true` | resolve 保持 none；不写 consent/paid |
| BRY01-T02 | continuity 路线结算 | `resolve_CS_BRY_01`＝`continuity`；`callback_CS_BRY_01_continuity`＝`true`；`consent_CS_BRY_01_continuity`＝`true`；`paid_CS_BRY_01_continuity`＝`true` | exit 组键不写；未二次确认保持 pending |
| BRY01-T03 | exit 路线结算 | `resolve_CS_BRY_01`＝`exit`；`callback_CS_BRY_01_exit`＝`true`；`consent_CS_BRY_01_exit`＝`true`；`paid_CS_BRY_01_exit`＝`true` | continuity 组键不写；两路线互斥 |
| BRY01-T04 | 拒绝与缺席 | `presence_CS_BRY_01`＝`refused` | resolve 保持 none；缺席时只播代理句 |
| BRY01-T05 | 早到/晚到回执 | `order_CS_BRY_01`＝`early`；`order_CS_BRY_01`＝`late` | 两种顺序只改未来台词；不回滚已结案；不重复结算 |
| BRY01-T06 | 服务班档位 | 无写入 | 0 档按基础范围与正常价；+1 档只多一处小便利；不越权、不无限供给 |
| BRY01-T07 | 闲谈池分离 | 无写入 | 城镇池与声望档池不串；中间档不播档位池；闲谈不改任何结算 |

写入矩阵逐条对照 [[状态键映射总表]] 取值集合校验（登记 `research/pilot-batch-cs-bry-01.json`）：

| 场景 | 键 | 取值 | 类型 |
| --- | --- | --- | --- |
| BRY01-T01 | `encountered_CS_BRY_01` | `true` | encounter |
| BRY01-T02 | `resolve_CS_BRY_01` | `continuity` | resolve |
| BRY01-T02 | `callback_CS_BRY_01_continuity` | `true` | callback |
| BRY01-T02 | `consent_CS_BRY_01_continuity` | `true` | consent |
| BRY01-T02 | `paid_CS_BRY_01_continuity` | `true` | paid |
| BRY01-T03 | `resolve_CS_BRY_01` | `exit` | resolve |
| BRY01-T03 | `callback_CS_BRY_01_exit` | `true` | callback |
| BRY01-T03 | `consent_CS_BRY_01_exit` | `true` | consent |
| BRY01-T03 | `paid_CS_BRY_01_exit` | `true` | paid |
| BRY01-T04 | `presence_CS_BRY_01` | `refused` | presence |
| BRY01-T05 | `order_CS_BRY_01` | `early` | order |
| BRY01-T05 | `order_CS_BRY_01` | `late` | order |

## 建议新增文件（沿用既有命名）

- `src/EmbersAndOaths/Codes/cs_bry_01_entry.gml`（on_first_interaction／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_hub.gml`（on_interaction／repeatable）
- `src/EmbersAndOaths/Codes/cs_bry_01_route_continuity.gml`（on_route_selected／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_route_exit.gml`（on_route_selected／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_feedback_1_early.gml`（on_state_change／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_feedback_1_late.gml`（on_state_read／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_feedback_2_early.gml`（on_state_change／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_feedback_2_late.gml`（on_state_read／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_feedback_3_early.gml`（on_state_change／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_feedback_3_late.gml`（on_state_read／once）
- `src/EmbersAndOaths/Codes/cs_bry_01_refusal.gml`（on_refusal／repeatable）
- `src/EmbersAndOaths/Codes/cs_bry_01_absent.gml`（on_presence_check／repeatable）
- `src/EmbersAndOaths/Codes/cs_bry_01_before_city.gml`（on_state_read／repeatable）
- `src/EmbersAndOaths/Codes/cs_bry_01_after_city.gml`（on_state_read／repeatable）

## 边界

- 键名口径：引擎键＝`EAO_`＋登记键名（见 [[引擎键名前缀与遗留键登记]]）。
- 前置同 N2：OI-02（事件号）、OI-03（存档字段与迁移）；经济数值、比例与触发距离仍待实机。
- 本页**不含实现代码、不分配事件号、不写数值、不部署**；未跑过的运行项不得标"已验证"。

[[试点实现批次N2]] · [[试点批次验收场景N2]] · [[城市服务班与有限库存]] · [[城镇声望与信任系统]] · [[全库条件流投影]] · [[实现交接总表]]
