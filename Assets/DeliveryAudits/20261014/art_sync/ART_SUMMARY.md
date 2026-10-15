# 当前美术素材汇总 · 2026-10-14

本次以提交 `86f630cd71ecfaea3e4a3920c3045477ac0e0ed4` 为归档基线，汇总当前工作树的新素材及相关索引。计数采用活索引与最终 FINAL/QA，旧图册和冻结文件作为当时快照保留。本文本身不证明远端推送成功，发布结果以本次 Git 核验为准。

## 一眼看清当前数量

| 类别 | 当前合格或已交范围 | 计数说明 |
|---|---:|---|
| 新剧情人物母图 | 44人／44张 | 11批；全部发送请求 accepted |
| 累计人物概念 | 211人 | 历史167＋新增44；旧范围5个未完另列 |
| 新44人的表情 | 87张 | 43人各2张，瑟珥仅E2；已含恩岱E2修复 |
| 新44人的职业动作 | 88张 | 44人各2张；原84＋4张补缺，当前制作缺项0 |
| 旧人物最新卡补绘 | 3张 | 布娅、雅尼、奥德；不增加人物数 |
| 敌人母图 | 12种／12张 | 独立于人物概念人数 |
| 敌人独立动作 | 35张 | 原24＋续姿11；002下挥仍缺 |
| 场景概念 | 2张v2 | 渡民岸井、退役营地避风棚；带风格保留意见 |
| 米娅摇头小样 | 2张新绘＋1张母图复用 | K1、K2通过；K0复用；K3缺项 |

人数、表情、动作和展示复用不可相加为“新增人物”。上述独立静态图、稀疏关键姿态均不是完整动画或可运行游戏资源。

## 素材入口

以下路径均相对仓库根目录：

- 人物当前母图入口：`Assets/CharacterDesigns/20261013/expressive/INDEX.md`
- 新44人及逐批核验：`Assets/CharacterDesigns/20261013/expressive/new_story/FINAL_DELIVERY_REPORT_44.md`
- 新人物表情活索引：`Assets/CharacterDesigns/20261013/expressive/new_story/EXPRESSION_DELIVERY_INDEX.md`
- 新人物动作活索引：`Assets/CharacterActions/20261013/new_story/ACTION_DELIVERY_INDEX.md`
- 历史具名人物侧背、表情、基础动作：`Assets/CharacterActions/20261013/MASTER_SUPPLEMENT_INDEX.md`；已在基线中的素材不重复算作本次新增。
- 三位旧人物最新卡修订：`Assets/CharacterDesigns/20261013/expressive/latest_card_alignment_delivery_v1/INDEX.md`
- 敌人：`Assets/EnemyDesigns/20261013/first_six/`、`second_six/`；各自 `INDEX.md` 与 `ACTION_CONTINUATION_DELIVERY_INDEX.md` 保留逐项选稿和失败来源。
- 两场景：`Assets/SceneDesigns/20261013/first_two_delivery_v1/INDEX.md`
- 米娅摇头：`Assets/CharacterActions/20261014/mia/headshake_pilot_v1/README.md`

## 已完成修复与剩余缺口

- 恩岱E2：`Assets/CharacterDesigns/20261013/expressive/new_story/endai/gap_repair_v2/`。新增1张已通过独审并补交；当前87表情已包含它。旧失败稿及旧图册均未覆盖。
- 图里、锉珥、苇珥、栎珥A1：各自 `Assets/CharacterActions/20261013/new_story/<角色>/gap_repair_v2/` 与 `character_gap_repair_v2_delivery/`。4张新选稿已通过并冻结；锉珥本轮失败首稿仍留存。当前88张已包括这4张，不能再加一次。
- 瑟珥E1：安全拦截，停止且不可重试；不计合格表情。旧Vian安全受阻项同样保留，不重试。
- 敌人002下挥：旧续姿轮和新补缺轮均未得到合格选稿。最新 `first_six/canal_club_brigand/gap_repair_v2/` 两张 FAILED 候选保留证据，`selected_output=null`；不把失败图加入35动作或图册选稿。
- 米娅K3收势：两版鞋形／脚距漂移，未通过固定双脚约束；K2首稿发缝／辫子镜像换边亦未收。2张新绘仅通过概念小样，仍有少量重绘位置漂移。
- 奥德左小指仍无法明确辨认，不能宣称已确认。
- 两景道具与地景的像素颗粒尚未完全对齐；SQ08闭合小包的内容不能凭外观认定为文书。

## 图册范围，避免误读旧数字

1. 新人物图册v1：`Assets/CharacterDesigns/20261013/expressive/new_story/catalog_v1/output/pdf/新增剧情人物44人_概念与表情图册_v1.pdf`，24页，44母图＋86表情＝130张不同选图。它早于恩岱E2补交，仍有当时的两处缺项占位；当前表情库存是87，不能拿该旧册反推当前缺项。图册也不包含88张职业动作。
2. 敌人图册v2：`Assets/EnemyDesigns/20261013/catalog_v2/enemy_design_catalog_v2.pdf`，14页，12母图＋35动作＝47张不同选图；002缺项用文字标明，未收入失败稿。
3. 新人物基础动作图册v1：`Assets/CharacterActions/20261013/new_story/catalog_v1/output/pdf/新增剧情人物44人_基础动作图册_v1.pdf`，24页，44母图＋84动作＝128张不同源图。它早于图里、锉珥、苇珥、栎珥4张A1修复，保留当时四处文字缺项；当前库存是88动作，修复入口见上一节，旧册不重写。该册未收人物表情。
4. 图册、浅深板、缩略图和浏览副本不算新增原创选稿。图册制作ZIP仅包含其声明的排版与核验资料，不等于完整素材源包。

## 源档与审计的保留口径

归档应保留对应完整源树及源ZIP：原始PNG、通过选稿、失败候选、真实提示词与已有参数记录、生成返回（其中图像payload属于绘图来源证据）、来源哈希、作者QA、独审、最终状态及冻结清单。缺失的历史参数不补造。ZIP与散文件存在重复，不代表新增素材。

部分“普通ZIP”按容量拆成多包，需要按其各自说明解压到同一目录；它们不是二进制分卷，单包可能不完整。按人物独立封包的源档则分别解到独立目录，避免根部同名清单覆盖。

补充记录 `Assets/DeliveryAudits/20261013/delivery_addendum_v1/` 保留第十一批两份最终状态补交的闭环；它不新增人物、姿势或图片。`research/story-network-validation.json`、`research/story-script-validation.json` 是叙事校验报告，不是新增美术数量或游戏实测证明。具体纳入发布范围由本次归档清单决定。

## 发送状态与制作状态分开

88张职业姿态全部制作通过并保存在素材树中，其中80张对应发送请求已接受，另8张属于瑟珥／达珥、索妲／珂琳两组，附件发送结果不确定。两组素材及源包已经保存，发送不确定不意味着素材丢失，不阻止本次Git归档，也不授权重发旧消息。accepted只说明请求已接受，不能证明已送达、已读或用户逐项审美认可。

## 本汇总的核对深度与使用边界

机器清单见同目录 `ART_SUMMARY.json`：记录当前数量、44份人物动作FINAL的逐人84＋4＝88对账、活索引与QA的SHA-256，以及184张指定选稿的当前文件字节数和SHA-256。184张是核对样本范围：旧人物图册130＋恩岱E2 1＋敌人47＋米娅2＋动作修复4；不是全库存总图数。原84张动作在本汇总按44份FINAL计数并绑定状态文件哈希，不宣称本轮重新逐图视觉验收。

仍未完成：原生像素网格及统一比例制作、装备兼容、完整连续动画／循环、场景碰撞与交互、游戏集成及实机验收。现有概念稿的QA或文件完整性核验不能替代这些工作；本次汇总与Git归档不构建或部署游戏包。
