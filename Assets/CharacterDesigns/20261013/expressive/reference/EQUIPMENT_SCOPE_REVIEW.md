# 装备范围证据复核

更新时间：2026-10-13T04:25:24.003247+00:00

19名新增独审人物＋1名用户认可瑟拉基准＋下一队列8人，共28人；不是172人普查。

## 当前队列结论

- 已生成20人 = 19名新增独审人物 + 瑟拉用户认可基准；下一队列8人独立计数。
- 28人源卡均未明确可入队、可控制或自由换装。实际机制分类全部为 **信息不足 / unknown**；没有完整换装生产名单。
- 源卡亦未声明永久固定服饰。下方固定外观/少量预设是可逆的制作建议，不能当作已证实游戏设定。
- 制作建议：固定外观23人、少量预设5人；可继续身份概念设计，但仍服从父任务派工暂停门槛。本报告不解除暂停。
- 托曼护路、伊沃离场、雷奥披甲、莉葵卖衣，均不能证明入队或换装。纳拉伤腿与坐姿必须保留，不能套站姿底模抹掉剧情事实。

## 证据规则

- 信息不足不等于不可换装；固定外观/少量预设是当前概念生产建议，不改人物设定。
- 本次源卡没有一人明确可入队、可控制或有装备选择机制，因此所有实际机制字段unknown，不提出完整换装角色名单。
- 源卡也未明确永久固定服饰，不能杜撰一组已证明永不换装人物。现有衣装brief只是单套外观美术提案。
- 如下一阶段出现明确队友证据，先按MODULAR-1决定实际范围，不倒推当前172人全部拆层。
- 仅新增本报告两文件；不改roster、剧情、既有图、dispatch_control、runtime或游戏包，不新生成图。

## 来源快照

- roster：`Assets/CharacterDesigns/20261013/expressive/roster.json`，SHA256 `0bc98becbab39e4ffcf5f13af99a2b14dd65868fbdfd24f8ba92ec1a53c52a2e`。
- `design/04_人物/人物弧光与关系转折.md`：[21, 21] 14组关系弧不是14个新同伴/可招募角色。
- `design/04_人物/人物_玛拉与伊沃.md`：[32, 32] 剧情确认离场不等于已实现护送AI。
- `Assets/CharacterDesigns/20261013/expressive/reference/MODULAR_CHARACTER_ART_DRAFT.md`：分层接口、头盔与特殊姿态、导出与引擎适配、最小试点与验收 
- `Assets/CharacterDesigns/20261013/expressive/reference/EQUIPMENT_COMPATIBILITY_AUDIT.md`：结论、原版Mod适配必须补核、最小验证与停止点 

## 分人物建议

### 齐勒（ALD-NPC-CHILER）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：旧墙讲述导者，经营讲述与退款边界。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_ALD-NPC-CHILER_齐勒.md:15–31`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 安菈（BRY-NPC-ANLA）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：成年卡扣学徒，留坊或离坊是劳动关系选择。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-ANLA_安菈.md:15–35`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 达兰（BRY-NPC-DARAN）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：亡者姐姐兼旧板材商，哀悼与私人注记的选择。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-DARAN_达兰.md:15–27`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_core_03.json`，`$.characters[?(@.id=='BRY-NPC-DARAN')].costume_props`；属于美术提案，不是换装机制证据。

### 艾伦（BRY-NPC-ELEN）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：成年装帧修复者；不是逃兵NPC-N-AREN。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-ELEN_艾伦.md:15–27`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_brynn_02.json`，`$.characters[?(@.id=='BRY-NPC-ELEN')].costume_props`；属于美术提案，不是换装机制证据。

### 哈塞（BRY-NPC-HASE）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：医药商品代理，有限营销用途与款项交易。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-HASE_哈塞.md:15–31`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 洛妲（BRY-NPC-LODA）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：有限水门维修班匠人，作业与赔付边界。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-LODA_洛妲.md:15–31`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 玛莉丝（BRY-NPC-MARIS）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：精灵扣件匠商；不是全族代表。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-MARIS_玛莉丝.md:15–27`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_brynn_02.json`，`$.characters[?(@.id=='BRY-NPC-MARIS')].costume_props`；属于美术提案，不是换装机制证据。

### 罗安（BRY-NPC-ROAN）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：成年本地装配匠，责任通过拆检判定。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-ROAN_罗安.md:15–27`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_brynn_02.json`，`$.characters[?(@.id=='BRY-NPC-ROAN')].costume_props`；属于美术提案，不是换装机制证据。

### 瑟拉（BRY-NPC-SELA）

- 范围：approved_baseline_1；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：独立夜渡船租船人，只能承诺一趟实际船运。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-SELA_瑟拉.md:15–27`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 雅尼（BRY-NPC-YANI）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**少量预设**（推断）。
- 源卡身份：带未合适义肢回城的成年退役者，伤残不代表战斗队友。
- 理由：义肢/支具与姿态需独立适配；只留已确认状态，不能自造康复或更换义肢分支。
- 验收：PRESET-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_BRY-NPC-YANI_雅尼.md:15–27`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 凯姆（MAE-NPC-KAEM）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：与N10同人的副馆员，失印与责任共用。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_MAE-NPC-KAEM_凯姆.md:15–34`。
- 角色来源：`design/04_人物/台本新增人物与知识边界.md:47–51`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_core_01.json`，`$.characters[?(@.id=='MAE-NPC-KAEM')].costume_props`；属于美术提案，不是换装机制证据。

### 赫斯·白（NPC-HERS）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：装置控制者；卡中拒绝正常可加入洗白线，但不是换装机制定义。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_NPC-HERS_赫斯·白.md:15–25`。
- 角色来源：`design/04_人物/人物_赫斯·白.md:21–39`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 莉德（NPC-LYD）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：来源抄写者，保护去向与作证须本人同意。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_NPC-LYD_莉德.md:15–27`。
- 角色来源：`design/04_人物/台本新增人物与知识边界.md:53–57`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_core_01.json`，`$.characters[?(@.id=='NPC-LYD')].costume_props`；属于美术提案，不是换装机制证据。

### 玛娅·禾（NPC-MAYA）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：地方民粮代理，非全阵营领袖。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_NPC-MAYA_玛娅·禾.md:15–27`。
- 角色来源：`design/04_人物/人物_玛娅·禾.md:21–39`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_routes_04.json`，`$.characters[?(@.id=='NPC-MAYA')].costume_props`；属于美术提案，不是换装机制证据。

### 米娅（NPC-MIA）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**少量预设**（推断）。
- 源卡身份：本地疫所患者，想先坐到门外且不一定迁村。
- 理由：坐姿/站姿与披肩、普通叠毯可作为有依据的表现预设；不是痊愈或自由换装。
- 验收：PRESET-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_NPC-MIA_米娅.md:15–25`。
- 角色来源：`design/04_人物/台本新增人物与知识边界.md:59–63`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_core_01.json`，`$.characters[?(@.id=='NPC-MIA')].costume_props`；属于美术提案，不是换装机制证据。

### 莫伦·海（NPC-MORREN）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：退役军医，病例与伤患保护职责。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_NPC-MORREN_莫伦·海.md:15–27`。
- 角色来源：`design/04_人物/人物_莫伦·海.md:21–39`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 雷奥·凯斯（NPC-REY）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：地方军需代理；衬垫旅行甲是美术提案，不证明可换甲。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_NPC-REY_雷奥·凯斯.md:15–27`。
- 角色来源：`design/04_人物/人物_雷奥·凯斯.md:21–39`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_core_03.json`，`$.characters[?(@.id=='NPC-REY')].costume_props`；属于美术提案，不是换装机制证据。

### 塞娜·里德（NPC-SENA）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：藏档人，资料比对与有限抄本职责。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_NPC-SENA_塞娜·里德.md:15–27`。
- 角色来源：`design/04_人物/人物_塞娜·里德.md:21–39`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_core_03.json`，`$.characters[?(@.id=='NPC-SENA')].costume_props`；属于美术提案，不是换装机制证据。

### 莉葵（TRADE-NPC-LIQUI）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：跨两地衣料采购人；换衣/冬衣库存交易不是本人穿脱装备接口。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/城市人物/人物_TRADE-NPC-LIQUI_莉葵.md:15–35`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 托曼·索（NPC07）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：护路契约人与路线提供者；护路资格不等于可控制队友。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/人物_托曼·索.md:21–39`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_routes_04.json`，`$.characters[?(@.id=='NPC07')].costume_props`；属于美术提案，不是换装机制证据。

### 欧达·苇（NPC09）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：守水源与水路互助者；迁居帮助不等于入队。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/人物_欧达·苇.md:21–39`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_routes_04.json`，`$.characters[?(@.id=='NPC09')].costume_props`；属于美术提案，不是换装机制证据。

### 艾娜（NPC-N-ENA）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**少量预设**（推断）。
- 源卡身份：受欠薪困扰的工人妻子，折叠外套是场面物件。
- 理由：本人衣服与怀抱外套分开保留，便于静态手持预设；不要把外套当她可自由穿脱的装备。
- 验收：PRESET-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/台本新增人物与知识边界.md:23–27`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_labor_06.json`，`$.characters[?(@.id=='NPC-N-ENA')].costume_props`；属于美术提案，不是换装机制证据。

### 纳拉（NPC-N-NARA）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**少量预设**（推断）。
- 源卡身份：伤腿绞盘维修工，不能因画站姿而默认为痊愈。
- 理由：优先坐姿、伤腿支撑与工具收纳预设；不先扩通用站立底模。
- 验收：PRESET-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/台本新增人物与知识边界.md:29–33`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_labor_06.json`，`$.characters[?(@.id=='NPC-N-NARA')].costume_props`；属于美术提案，不是换装机制证据。

### 妮尔（NPC-N-NELL）

- 范围：independently_reviewed_19；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：原创劳务书记；非原作尼尔，租屋/听审为情境变化。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/台本新增人物与知识边界.md:35–39`。
- 当前没有在本次所读batch brief中找到服饰条目；现有图可作视觉参考，不据图推机制。

### 塞尔（NPC-N-SEL）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：器具工坊师傅，炉与劳动债务是剧情对象。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/台本新增人物与知识边界.md:41–45`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_labor_06.json`，`$.characters[?(@.id=='NPC-N-SEL')].costume_props`；属于美术提案，不是换装机制证据。

### 玛拉（n1_mara）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**少量预设**（推断）。
- 源卡身份：绳匠与伊沃姐姐；围巾是剧情关联物。
- 理由：围巾或工作小道具有明确情境，可保单套衣服并有限切换道具；状态触发须另查台本。
- 验收：PRESET-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/人物_玛拉与伊沃.md:25–25`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_opening_05.json`，`$.characters[?(@.id=='n1_mara')].costume_props`；属于美术提案，不是换装机制证据。

### 伊沃（n1_ivo）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：守夜人；逃离/听审分支不是入队机制。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/人物_玛拉与伊沃.md:26–26`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_opening_05.json`，`$.characters[?(@.id=='n1_ivo')].costume_props`；属于美术提案，不是换装机制证据。

### 托雷（n1_tor）

- 范围：next_queue_8；机制证据：**unknown**；概念制作建议：**固定外观**（推断）。
- 源卡身份：私人债务追索者；撤票/失踪分支不是装备界面。
- 理由：现有来源约束职业、身份、关系或任务职责，未规定装备选择机制。可继续单套身份外观概念，不能把制作建议写成永久不可换装的剧情事实。
- 验收：FIXED-1；若后续证实可入队/可换装，转MODULAR-1核定范围。
- 角色来源：`design/04_人物/人物_玛拉与伊沃.md:27–27`。
- 单套服饰提案：`Assets/CharacterDesigns/20261013/expressive/briefs/batch_next_opening_05.json`，`$.characters[?(@.id=='n1_tor')].costume_props`；属于美术提案，不是换装机制证据。

## 验收门槛

### FIXED-1

- 源卡身份、同人归并和所处状态一致；衣装注明美术提案，不新增王冠/军徽/武器等设定。
- 固定外观概念仍需原生尺度重制；正式画布、方向、动作、原点、碰撞、点击和深度待核。
- 保留原始概念、透明边界、来源与版本；单张PNG不能冒充已拆层母版。

### PRESET-1

- 先列少数确实需要的情境/姿态与触发证据；未证实状态不生成，不自动编造伤愈或入队。
- 身体与固定衣装可整身制作，道具、毯、支撑或围巾按真实遮挡需要分开；是否运行时分层另定。
- 坐姿需独立检查腿、衣摆、座面、支撑与脚点，不能压缩站姿或取消既有伤腿。

### MODULAR-1

- 先补角色专属可入队/可控制/换装机制证据并明确具体可见装备范围；只有入队一项仍不能证明支持任意装备。
- 冻结实际body_profile与同一逻辑画布、foot_anchor、方向/动作/帧ID；engine_origin、碰撞和点击单独核实。
- 交付可编辑干净身体与真实衣甲/头发/头盔/手持源层，被遮挡区域完整；不将整身PNG机械裁块算底模完成。
- 试点空手、单手+盾、双手武器；检查左右握点、方向相关遮挡和副手互斥。
- 试点无盔/两顶盔，检查发型隐藏区/蒙版与脸部；试点一套衣甲穿脱还原完整底图。
- 坐姿等特殊姿态单独验收；特殊体型或支具声明兼容边界与明确回退预设，不能承诺全装备通用。
- PNG/图集+JSON保逻辑画布、trim_offset、anchors、draw_order、hide_masks、支持组合及版本；运行适配另核。
- 正式运行验收穿脱、切武器组、过图、存读档、原生并排尺度与点击/通行；未运行一律runtime_verified=false。

## 验证边界

本次逐张读取roster所指源角色卡及相关具名角色段，引用按角色身份定位；未把roster aliases中的跨页链接当同人证明。未核验原版游戏接口，未运行游戏，未增改角色机制。JSON保存各来源行段、原文摘录及当前SHA256，支持复核。源卡变动或明确玩法决策出现后需重新审查；本报告不以资料缺项阻止无关的概念设计。
