# 首六敌人动作补缺交付索引

记录日期：2026-10-14（UTC）。

## 本轮结果

- 六个拟补阶段中，5 个新增独立关键姿势通过：001 v2、003 v1、004 v1、005 v1、006 v1。
- 002 下挥中段的 v1、v2 均未通过。单次硬修订额度已用尽，仍缺 1 个阶段；两版只保留在完整失败源包中，不计合格动作、不交付选稿 PNG。
- 实际生成共 8 次：6 次首稿 + 2 次硬错误修订。
- 三组共 14 附件：5 张新增合格透明 PNG、3 张浅深背景相邻阶段对照板、6 个完整源 ZIP（含 002 失败档案）。
- 14 件已保存 Library 并回读；逐件 SHA-256 与字节数与冻结原件一致。6 ZIP 共 346 个成员的 CRC、SHA、字节与完整源树通过。

## 发送记录

### 001 / 002

- 001长矛手收矛回重心v2通过；002劫道者下挥中段v1/v2失败，不交付选稿PNG，仅保留失败源档案。
- 4 附件；消息 Sentinel_5c2473f6eb488191be153affad93771c；2026-10-14T04:11:45.946482+00:00。
- 状态：sent_accepted_not_read。发送请求已接受，不代表已送达或已阅读。
- [交付回执](continuation_001_002_delivery_v1/DELIVERY_RECEIPT.json) · [冻结清单](continuation_001_002_delivery_v1/delivery_manifest.json) · [独立封包审查](continuation_001_002_delivery_v1/independent_package_audit.json)

### 003 / 004

- 003渠墓腐尸前压扣抓末端、004墓龛游魂探手回束各新增一个独立关键姿势。
- 5 附件；消息 Sentinel_b7a60e5fa55881919c89b50d7cb43c11；2026-10-14T04:11:59.839332+00:00。
- 状态：sent_accepted_not_read。发送请求已接受，不代表已送达或已阅读。
- [交付回执](continuation_003_004_delivery_v1/DELIVERY_RECEIPT.json) · [冻结清单](continuation_003_004_delivery_v1/delivery_manifest.json) · [独立封包审查](continuation_003_004_delivery_v1/independent_package_audit.json)

### 005 / 006

- 005饥血潜行体回爪后承重、006债契仪式看守侧移换重心各新增一个独立关键姿势。
- 5 附件；消息 Sentinel_f24551a66550819191427ca88e419e13；2026-10-14T04:12:12.852976+00:00。
- 状态：sent_accepted_not_read。发送请求已接受，不代表已送达或已阅读。
- [交付回执](continuation_005_006_delivery_v1/DELIVERY_RECEIPT.json) · [冻结清单](continuation_005_006_delivery_v1/delivery_manifest.json) · [独立封包审查](continuation_005_006_delivery_v1/independent_package_audit.json)

## 计数边界

- 首六敌人：原有 12 个已交付独立关键姿势 + 本轮 5 个 = 17 个；6 张静态概念另计。
- 全部 12 敌人：原有 24 个已交付独立关键姿势 + 本轮 5 个 = 29 个；12 张静态概念另计。
- 对照板中的旧相邻姿势只作参考，不能再次计作新增。本轮没有修改原 24 姿态的冻结索引、旧回执或旧 ZIP。
- 001、003、004、005、006 现在各有 3 个独立阶段；002 仍是原有 2 个合格姿势，新增阶段缺项。

## 制作状态

- 三阶段不等于连续动画；没有完成动画循环、补间、精确锚点注册或帧间一致性验收。
- runtimeIntegrated=false；runtimeVerified=false。装备组合、碰撞与实机表现未验证。
- 004 保留原审定半透明；005 / 006 保留生成原始 alpha。
- 本轮未 git commit、未 push；冻结文件与旧记录保持不变。

## 原交付入口

- [首六原静态与动作交付](INDEX.md)
- [第二组六敌人原交付](../second_six/INDEX.md)
- [十二敌人原目录](../catalog_v1/INDEX.md)

## 2026-10-14 再修记录｜002 gap_repair_v2（未补齐）

- 本轮1次新首稿＋1次硬错误修订，共2次生成；v1、v2均失败，selected_output=null，新增合格姿态0。
- v1棍头高于拳；v2棍头降至腰带及以下，均未满足完整下挥胸腹中弧。两稿保留失败标记，不作选稿交付。
- 本轮不改变已有首六17姿、002已有2姿及全部敌人的合格姿态计数；上文29姿为首六补缺批次的历史时点总数，后续批次应另见第二组六敌人索引。
- [本轮失败最终状态](canal_club_brigand/gap_repair_v2/FINAL_STATUS.json) · [独审](canal_club_brigand/gap_repair_v2/independent_QA.json)；旧失败记录、冻结包与回执均保留。
