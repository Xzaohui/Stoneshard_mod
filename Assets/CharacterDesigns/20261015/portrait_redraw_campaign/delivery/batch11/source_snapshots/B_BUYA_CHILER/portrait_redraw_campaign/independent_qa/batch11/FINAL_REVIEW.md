# Batch 11 最终独立 QA

冻结复核时间：2026-10-15T09:59:52.382769+00:00

结论：四位可交付为带明确备注的头像候选。不是原生逐像素终稿、用户审美验收或游戏运行验收。

## 选稿与限制

### 芮莎 / BRY-S02-NPC / 五十岁上下镇粮保管人

选稿：`risha/candidates/portrait_v2_containment_74x100_candidate.png`

v2 脸更饱满、宽颊钝鼻和年龄感成立，颈与围裙边收紧；保暗红头巾、深棕发、橄榄/浅围裙身份。Containment留出目标框安全边。

- 内眉上扬和亮眼白仍在，不能称忧眉全部修复。
- 侧卷/头巾折线仍细于理想硬块风格。
- 技术安全边只增加透明画布，不恢复或绘制内容。

- 候选 SHA256：`9c02704cb60cb51ff67c2c4fcc4d2d3d532f553bf7517ee7659da9b806372564`
- Manifest SHA256：`03a4dbd9b9da329b2ed5a645a37c9803c3752e975753a9d6d5ceb32b0f77d09b`

### 米蕾 / BRY-S03-NPC / 三十多岁未归水手的姐姐

选稿：`milei/candidates/portrait_v2_containment_74x100_candidate.png`

v2 紧拢发髻、短颈和窄灰蓝领明显改善，长卵成人脸、淡眼下影与坚定闭嘴成立；未表现弟弟死亡、救回、葬礼或放弃等待。

- 亮眼白和轻微眉间紧张仍有，不能称完全中性眉。
- 所选v2 raw右缘alpha128实体贴边78行；安全边不证明恢复潜在缺失轮廓。
- Containment为同raw整幅保比NN技术派生，非第三次重绘。

- 候选 SHA256：`f0df0f02e328e38e6d467e2ed339e762971079db48dd7b32518cf2fda20422de`
- Manifest SHA256：`f27d83dca6abd93e129e5d3efc5c65d2ac03f8eb4485ad873d53665632a77cd3`

### 布娅 / ALD-NPC-BUYA / 三十多岁付费访客

选稿：`buya/candidates/portrait_v2_maxcoverage_74x100_candidate.png`

v2 修复右发/辫触框并稍放平内眉；成人鼻颧、棕辫和梅紫/灰绿身份保留，略张口为礼貌追问。母版使用latest_card_alignment_v1。

- 亮眼白、细发带、笑意偏弱和颈领稍多仍在。
- 此头像不验证右手套/左手裸、手腕白痕、披风内衬或随身物；裁幅内无手。

- 候选 SHA256：`64818682ce48b600c6b2ca69a5c89229a7973baa7e309119ebe1b5017fcf0ebb`
- Manifest SHA256：`583da040fce128ad4895cbbea782fa92f9e9ecd34202ad8c58f84fe67981c8ce`

### 齐勒 / ALD-NPC-CHILER / 六十岁上下旧墙讲述导者

选稿：`chiler/candidates/portrait_v1_maxcoverage_74x100_candidate.png`

v1 已有约六十岁灰鬓/年纹，长鼻、翘须和短山羊须、细粉笔帽檐、芥末/灰绿成立；张口讲述/斟酌有个性。选MAXCOVERAGE保中性灰须/粉笔，不用无必要v2。

- 亮眼白与少量细须为非阻断候选备注。
- 不由普通讲述表情认定新围城为事实或退款/剧情完成。

- 候选 SHA256：`c439b3ac7d3b4fab9d14e4dc0ce7131e3e9a12555712ee16cb14f1d36774ed38`
- Manifest SHA256：`792ab9001d87c2a53e024591d741109ac4174f25bed910f8e0053bbb4c04f3c6`

## 技术复核

- 4 个唯一身份，成功生图 7 次：芮莎2、米蕾2、布娅2、齐勒1。每人初稿加最多一次必要修订。
- 18 份候选导出独立重新实现；像素和 PNG 字节逐一完全相同，8x 均精确最近邻。
- 4 份选稿均 74×100、32 可见 RGB 色、0/255 二值 alpha、透明 RGB 清零；四条目标画布边均透明。
- 50 条 source 清单记录的原源/快照/声明 SHA 全部相同；现卡/精确母版/旧 QA 与 roster 另行核过。
- 原始 imagegen 大图与完整工具返回解码字节一致，工具原始输出文件亦核对。
- 全部生产 manifest 选稿 SHA、生成数、source 清单、文件清单或 SHA256SUMS 覆盖与散列均通过；没有未完成项。芮莎/米蕾使用 SHA256SUMS 作为完整文件清单，其 manifest 采用 generation_calls_completed 字段。
- 两份六参考参数拒绝记录无图像 payload；成功结果仍各两张，不重复计作第三次生图。
- 技术导出增加的透明边不等于恢复原始缺失图像。米蕾 raw 右边缘贴边限制保留在最终选择和生产 README/manifest 中。

全部审查产物限于本目录；未改生产卡、旧图或代码，未生成图、提交或推送。
