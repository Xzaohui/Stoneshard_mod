# 设计库协作规则

<!-- S62-RULE:BEGIN -->
2026-10-12 S62：当前任务须多种实际行动解法、人物跨任务弧光与有条件的后续影响。设计以网状叙事规范、交叉矩阵及各台本顶部R/X为准；S61旧选择停用、场次作有条件素材。16个DT为一次地方人物事件，普通运输、维修、清运不做玩家重复任务。角色获知须有限回执，死亡/缺席/拒绝/授权优先，先后次序重评未来行动而不回滚历史；伤害留痕、奖励去重、终局快照独立冻结。设计改后运行三项设计检查：Validate-StoryScripts.py、Validate-NarrativeNetwork.py、Test-DesignVault.ps1。自动检查不能证明对白质量或游戏运行，本轮不部署新包。
<!-- S62-RULE:END -->

2026-10-11 S61：当前先写全任务台本和区域理念。逐場稿在各方向的台本/子目录，统一从[[任务台本总索引]]和[[新区域设计与任务总表]]进入。主线使用N1—N18，证据用NE1—NE5；现行规则由[[当前任务依赖与状态字典]]和[[当前证据链与结局条件]]解释。历史MQ稿不静默覆盖或自动迁档，冲突明确以当前稿为准。台本必须含场面调度、实际对白、明确选项、执行出口、后果回访、关键证据恢复和奖励所有者；日常另写期限、失败与普通实例变体。角色知识有边界，长材料分存[[文书与现场文本台本]]，不把每章都写成收三份纸。draft仅代表第一版台本，N1新增对白也不能当已编入0.3.0。写文档不等于批准新部署，本轮不修改游戏与玩家数据。

2026-10-11叙事修订：当前文书查档开篇已被用户要求撤掉，新的[[开篇_无钟之夜]]及[[剧情重构与旧任务退役]]优先。旧MQ01/MQ02卡标记retired、旧18任务蓝图标记历史待重构；不要继续将其作为新开篇前置。每章需人物动机、现场矛盾、有限来源的反转、真实可执行选择及回访，不用统一“三份文书阅读交回”模板。新场景按用途分别布局，原创图像与碰撞职责分开；生成资产存源码目录，设计仅登记来源、规格与限制。

本目录是独立 Obsidian vault，仅存放调研摘要与设计，不存放Mod实现。用户已授权实现并明确“不隔离，直接在当前路径下开发”；遵循根目录AGENTS.md的当前安装开发和更新备份规则。

## 笔记规范

所有内容笔记用 UTF-8 Markdown，必须有 YAML 属性：title、id、type、status、canon、baseline、updated、tags、aliases。导航与规则文档可以按其用途简化。ID 不随标题修改；文件名在库内唯一。日期固定使用调查实际日期，不伪造后续核验。

内部关联用 Obsidian `[[笔记名]]`，外部来源用 Markdown URL。不要依赖 Dataview 或其他插件。每张实体卡应链接所属区域、相关势力/人物、任务或副本及对应方向索引；尽量让语义关系双方都链接。

`canon` 分为：original-local（本地观察）、original-source（外部资料）、mixed（逐项标识）、mod-original（原创）、unknown（未核验）。原作文本的存在仅证明包内定义，不证明当前存档可达。中文翻译与英文矛盾时记录差异，不推导额外真相。

## 逻辑要求

每个主线任务写明：前置、触发、目标、分支、状态变化、奖励、失败/中断恢复、关键物件替代、后续。支线每阶段也须有入口和出口。所有变量是设计变量，不得说它们已经是原作变量。

区域写明通路、服务、危险与回程。任务没有技能流派专属硬门槛；关键线索和物件不能被随机刷新永久删除；声望负值不得锁死主线。日常任务按游戏内时间与地方状态刷新，不使用现实签到。唯一奖励只能领一次，故事副本不能刷新关键 NPC 和证据。

事实修改先查来源登记和矛盾清单。设计修改同步影响：任务依赖表、证据链、区域、势力、结局条件、状态字典、内容清单与验收记录。

中文 Wiki 摘记从 [[中文Wiki参考与设计映射]] 进入。网页事实与原创设计决策分开，不复制整页；逐条保留来源、版本及未知路径。新机制建议同步到相关规则卡，不只收藏链接。

## 评审与阶段

draft 表示逻辑初稿，不代表对白全文、数值和美术完成。reviewed 需要记录评审证据。approved 仅在用户明确认可相应范围后使用。implemented 只在用户授权实现且有实际结果时使用。

实现已获授权；本目录只更新设计与证据，不存游戏实现文件。技术方向区分构建成功、离线补丁验证与游戏内运行验证。

用户已确认vanilla.win为原始data.WIN备份，当前data.win为加载现有Mods后的包；来源说明与独立校验分开记录。最新授权允许直接部署至`D:\SteamLibrary\steamapps\common\Stoneshard\msl\Mods`并更新现有游戏data.win；不抹掉现有Mod组合，不重复应用已存在的EAO补丁。

此前 [[隔离测试与正式存档保护]] 保留为历史/可选方案，当前执行用户“不隔离”选择。每次更新先保留资源/设置/用户数据备份，不自动回滚玩家档，不承诺Mod档无损回到原版。

直接使用现有安装和原作保存路径，不改引擎游戏名强制分离存档；无需创建测试账户或虚拟机。临时验收数据包只是部署前校验产物，不是独立运行环境。

开始阅读：[[设计总览]] → [[原作剧情进展]] → [[创作边界与待核验]] → [[剧情总纲]] → [[任务状态与依赖]]。

<!-- CITY-TASK-ART-S77:BEGIN -->
2026-10-12 S77：布林六处任务场所概念见design/12_美术参考/布林任务场所概念与台本映射.md，输出v1/v2与完整提示词、输入/输出哈希见research/brynn-task-space-art-s77.json。v2定向修改F空泊位，旧稿保留；A—F非任务顺序，图不定官方地理、NPC身份、门数、碰撞或库存。不覆盖十五城总览，不修改游戏包。后续修改按文字空间/台本核验并更新图文关联。
<!-- CITY-TASK-ART-S77:END -->

<!-- CITY-TASK-ART-20261012:BEGIN -->
2026-10-12：斯孔弗特／约斯特文各新增六面板任务场所概念，入口design/12_美术参考/原素材参考与城市概念图.md，逐项映射与原参考／提示词／候选SHA见research/city-task-art-20261012.json。保留原总览、YOS v1；人物、库存、排水、门与格尺寸须再制作核验。图只为原创草稿，不改变原回执、任务完成状态或游戏包。TaskArtLinks.py维持任务／聚落／空间双链；修改后跑原三项设计检查及图片来源检查。
<!-- CITY-TASK-ART-20261012:END -->

<!-- SHORE-VINE-TASK-ART-20261012:BEGIN -->
2026-10-12：丹布里／曼郡各新增六面板任务场所概念，逐项映射见design/12_美术参考/丹布里任务场所概念与台本映射.md与曼郡对应卡。完整提示词、原参考、v1/v2和输入输出哈希见research/shore-vine-task-art-20261012.json；不替十五总览或旧选稿。短宿两床、双名同桶、两对师徒及实际回程遵台本，坡面、容量和近景仍须制作；图不代表游戏交互。TaskArtLinks.py维持本批双链，运行Validate-ShoreVineTaskArt.py及既有设计检查。
<!-- SHORE-VINE-TASK-ART-20261012:END -->

<!-- CITY-ART-S74:BEGIN -->
2026-10-12 S74：参考用户stoneshard-assets-sample生成城市概念板，每板含城市核心与卫星ID构图；入口design/12_美术参考/原素材参考与城市概念图.md。初始/追加/编辑提示词、输入哈希和输出SHA分别存research/city-art-briefs.json、city-art-prompt-additions.json、city-art-manifest.json。参考原图只读，不复制图集；生成板是美术草稿，不作官方地理、最终精灵、碰撞或运行证据。新候选记录必须保留原提示词与版本，不覆盖旧选稿。
<!-- CITY-ART-S74:END -->

<!-- SPECIAL-NPC-NEXT-20261012:BEGIN -->
2026-10-12用户要求继续城市设计，完成后扩充各特殊地点与野外NPC对白；原版逐NPC中英文可只读核对，参考BG3／神界原罪的动机、分支与后果结构。后续范围及原版来源、文本／物件、地点／人物／任务交叉验收见design/11_管理/特殊地点与野外NPC对白扩展计划.md；城市稿与全局逻辑未收尾前不跳过该阶段。保持原版／当前组合输入分开、游戏与存档不改、原作来源摘要定位与必要短例入库，未读／未运行不称完成。
<!-- SPECIAL-NPC-NEXT-20261012:END -->

<!-- BRYNN-CONTINUATION-S85:BEGIN -->
2026-10-12 S85：用户追加布林续篇；research/brynn-continuation.json登记六案、18场/18方法、七原创人物、六场景、15组有限条件桥/45方法版本。入口design/00_导航/布林续篇任务与伏笔回收总表.md，原作复核另卡；原73篇/314单方法回执基线不删除，合计79篇、71逐角色草稿/8待深化；桥组与旧单方法回执分别计。官方2021正文经Steam API读，本地64命中只存定位/哈希/摘要，不存全文。夜船/旧市长谜底、原商店/地窖/领袖权限保留，礼昂与雅尼分人；空椅不作同意，N17不改/NE不加/奖去重。本轮不部署；Validate-BrynnContinuation.py＋原三项设计检查，数字/比例/游戏尚未验收。
<!-- BRYNN-CONTINUATION-S85:END -->

<!-- CITY-DRAMA-S86:BEGIN -->
2026-10-12 S86：寒凉盆地/修院山地八案由ashcare/highland的drama.json与feedback.json驱动，入口design/11_管理/寒凉盆地与修院山地人物演出审查.md。24场/16原方法/31旧回执/八新卡/六短文本；妮蔻与枯恩分别答、奥娅休息非弃人，真实普通护理不买研究/relief；支架非NE5，司榆补笔/赫斯旧控制留史；古菈旧工资独立、新班再问，缺必需交接保待办，N17不改。现73基线+六布林续篇=79逐角色初稿；全网数值/时间/比例/文学与游戏未验收。运行Validate-CareAndHighlandDrama.py及原三项设计检查，本轮不部署。
<!-- CITY-DRAMA-S86:END -->

<!-- TOWN-REPUTATION-S87:BEGIN -->
2026-10-12 S87：用户要求设计各城镇声望系统并中英对照。research/town-reputation.json定义三层分账（原作声誉/阵营承诺/城镇信任），十五地域各五档（−2..+2）、逐条写入来源、接收入口、受托解锁、听闻与边界。入口design/09_系统逻辑/城镇声望与信任系统.md与[[城镇声望系统中英对照]]；只能实际执行且最小核验写入，每来源一次，±1（重大伤害−1），上限±2；不洗罪、不解锁无限物资、不锁主线与回程，N17后冻结；跨城仅明列传递。运行Validate-TownReputation.py及原三项设计检查；未映射引擎、未部署。
<!-- TOWN-REPUTATION-S87:END -->

<!-- FORESHADOW-LEDGER-S87:BEGIN -->
2026-10-12 S87：用户要求持续埋伏笔并回收。research/foreshadow-ledger.json把主线74条X边、日常16条、副本18条并入线写成闭合丝线；布林续篇15桥与城镇解锁/听闻/回执各15处成组引用；夜船货物、旧市长责任、晶石全貌、全国政体为有意留白。入口design/09_系统逻辑/伏笔与回收台账.md，运行Validate-ForeshadowLedger.py及既有检查；不新增奖励/承诺/结局资格，不部署。
<!-- FORESHADOW-LEDGER-S87:END -->

<!-- TIMELINE-REGISTRY-S88:BEGIN -->
2026-10-12 S88：用户要求持续完善并收口全局逻辑。research/timeline-registry.json把主线18、支线8、日常16、副本9、城市73、续篇6的时序与奖励声明抽为单一审计视图（不新增数字）；入口design/09_系统逻辑/时序与奖励总表.md。全局口径：无隐藏倒计时、日常显式期限与状态机、最终确认后冻结、奖励一次键去重。对白独特性：修复布林续篇BC85-11—15五桥共用默认句、16个日常共用玩家句（源field＋writer模板）、CM-HIG说明文误入台词；Validate-DialogueDistinctiveness.py覆盖2962句源台词＋全库笔记层扫描（精确/规范化克隆、十笔记以上模板、12字短语跨5组、后台标识泄漏）。生成器可重跑：Write-StoryScripts/BrynnContinuation/Write-CityCampaign整篇重写时保留全部外部登记块（城市总写手另携带continuation_registries与dramatic_scope、复现CS-HIG-03入口文案并回写各哈希清单；隔离副本全量重跑后与主库逐字节一致）。另加Validate-CastRoster.py（158城市演员/89新卡/共享身份声明/条件引用/314回执接收者可解析）、奖励区间（N≤0.7B、SQ 0.2–0.3B、DT 0.15–0.3B）、“无限/永久免费”无界承诺、双语纯度与原文对白清点校验（1132条/72说话人槽）。运行新校验及既有检查；经济校准/比例地图/游戏运行未验收，不部署。
<!-- TIMELINE-REGISTRY-S88:END -->

<!-- FINE-DETAILS-S89:BEGIN -->
2026-10-12 S89：用户要求细粒度设计（NPC/物品/装备描述，贴合原作与新作风格）。research/item-registry.json（63条：文书26/信物30/工具7，名称中英＋风格描述＋处置规则＋14条原作术语对照）与research/npc-fine-details.json（172名Mod原创NPC：各城新增与『已有』演员、续篇演员、卫星住户与主线原创人物；体貌/衣着/随身/举止/风格守卫；含同名分人与共用身体说明；原作人物只续写剧情、不重画形象）。入口design/05_主线/原创物品与装备总表.md与design/04_人物/人物细描与随身物.md；描述按原作样例校准（1-2句、来源地/用途/行业视角），不复制原作文本。运行Validate-FineDetails.py及既有检查；数值、美术与游戏未验收，不部署。
<!-- FINE-DETAILS-S89:END -->

<!-- SERVICE-REGISTRY-S90:BEGIN -->
2026-10-12 S90：用户要求继续完成项目。research/service-registry.json登记十五城各一个普通有偿服务班（名称中英／经办人／职能／有限库存／档位便利／边界），落实「一批案件结束前不刷新库存」与「不刷新成玩家跑腿任务」；同一块挂到十五张城市页（服务/信任/人物细描三链）。入口design/09_系统逻辑/城市服务班与有限库存.md；档位便利与[[城镇声望与信任系统]]配套，只改范围与便利、不越授权、不无限供给。运行Validate-ServiceRegistry.py及既有检查；价格数值、美术与游戏未验收，不部署。
<!-- SERVICE-REGISTRY-S90:END -->

<!-- CITY-SPACES-S75:BEGIN -->
2026-10-12 S75：132室内用research/city-space-profiles.json逐街区空间替换通用工作间/侧室，58条CS触发/调查/回访用显式地点表，禁止重新按序号取模。入口design/11_管理/任务空间与地点关联审查.md。方案仅相对布局与互动，不是比例碰撞或运行房间；观察、私密授权、实际处置与奖励分记，新增室内不是全访前置。作者工具Write-CitySpaces.py保留备份差异与哈希，变更后额外运行Validate-CitySpaces.py及既有设计检查。
<!-- CITY-SPACES-S75:END -->

<!-- OFFICIAL-NAMES-S110:BEGIN -->
2026-10-13 S110：特殊地点的官方英文名接入（只读）。Probe-SpecialLocations.py 从同一 STRG 条目补 name_en：8 个世界地图区域、44 个传闻地点与 13 个地形类型全部有官方英文名（如 烂柳周边地图 = Map of the Rotten Willow Surroundings、渡鸦裂口 = Raven Cleft）；清点卡、六张地点卡与区域映射页改为中英并列。运行 Validate-SpecialLocationInventory/SpecialSiteCards/RegionContentMap 及既有检查；设计正文仍中文先行，未测量项不变，不部署游戏包。
<!-- OFFICIAL-NAMES-S110:END -->

<!-- NAV-ENTRY-S111:BEGIN -->
2026-10-13 S111：特殊地点阶段入口接入导航——设计总览加指向[[特殊地点与野外NPC阶段验收记录]]的句子，任务台本总索引与城市与聚落设计总索引加FIELD-STAGE-S111块（十一入口）。Write-CityIndexes.py 接入NotePreserve并在末尾回写全部清单（修复重跑触发续篇前置校验的问题）。运行Validate-FieldStage.py及既有检查；不部署游戏包。
<!-- NAV-ENTRY-S111:END -->

<!-- CITY-DRAMA-S76:BEGIN -->
2026-10-12 S76：布林主章＋10支线当前对白由research/brynn-drama.json、brynn-feedback.json驱动；stages只保S63地理骨架，dramatic_scenes是当前文本，不再输出三问模板或把患者/学徒话标在商户名下。20名演员包含13新增配角，56条旧回执分别写早到/晚到回应。入口design/11_管理/布林人物对白与网状演出审查.md。只增剧情细稿，不增新奖励、全巡前置、原作事实或游戏实现；实际签约/交接才提交，已结不改选，不克隆NPC。运行Validate-CityDrama.py及既有设计检查，尚余0篇城市对白与经济数值未终审。
<!-- CITY-DRAMA-S76:END -->

<!-- CITY-DRAMA-S78:BEGIN -->
2026-10-12 S78：奥尔德文主章＋六支线当前文本由research/aldwynn-drama.json与aldwynn-feedback.json驱动，独立dramatic_casts.ALD不混布林演员。21场、15方法、32旧回执；9新增配角卡，入口design/11_管理/奥尔德文人物对白与交叉演出审查.md。当前73篇逐角色稿，尚0篇待同等精修；stages为地理素材，S78 dramatic_scenes才是本城现行对白。保旧314边与NE/N17/奖励，拒伤像、共仪、赞助不取消基本出口，赠与撤回不得冒称交付。修改后运行Validate-AdditionalCityDrama.py和既有设计检查；数字经济、比例地图和游戏实现未经验证。
<!-- CITY-DRAMA-S78:END -->

<!-- CITY-DRAMA-S79:BEGIN -->
2026-10-12 S79：曼恩主章＋六支线逐角色稿由research/maen-drama.json与maen-feedback.json驱动，dramatic_casts.MAE独立。23场、15原方法、33旧回执；8补充角色卡含N10同一凯姆，不新增第二人生或回授旧认证。入口design/11_管理/曼恩人物对白与去留交叉审查.md。当前共73篇逐角色稿，其中三大城市25篇；0篇待同等深化；病例、住址、技术、物件、政治与去向授权分别核，焚毁/排斥/欠款留史，不强空城或正常学院重开。修改后运行Validate-MaenDrama.py及既有设计检查；数字经济、比例地图、最终对白和游戏运行尚未验收。
<!-- CITY-DRAMA-S79:END -->

<!-- CITY-DRAMA-S80:BEGIN -->
2026-10-12 S80：冶炼／羊毛两地八案作者源为research/skonfert-drama.json、yostwayne-drama.json及各feedback.json，入口design/11_管理/斯孔弗特与约斯特文人物演出审查.md。24场、16原方法、30旧回执；莉葵共一ID、卡、身体和有限款货，博赫不替妮莎未归弟弟归家，缇娜跨两案同人。当前73篇逐角色稿、0篇待深化。开门归包、信仰与护理、工钱／预款、冬料／外售分别核，拒未来不抹旧欠；晚到只改未来，不重奖／改N17。运行Validate-ForgeAndWoolDrama.py及既有设计检查；数值经济、时间轴、比例地图和游戏实现尚未验收。
<!-- CITY-DRAMA-S80:END -->

<!-- CITY-DRAMA-S81:BEGIN -->
2026-10-12 S81：丹布里／曼郡八案作者源由Author-ShoreAndVineDrama.py生成，两城各drama.json与feedback.json驱动。入口design/11_管理/丹布里与曼郡人物演出审查.md；24场、16原方法、30旧回执，10新卡。三户不从两空间造第三床，坦瑟第二场留原岸，家船三成年人逐人同意；提奥与贝洛分酿酒／箍桶，不替原NPC。当前73篇逐角色初稿、0篇待深化；床、船、护理、桶、枝、款和工班按实际单记，拒绝有独立出口，晚到不重奖／改N17。运行Validate-ShoreAndVineDrama.py及既有设计检查；数值、时间轴、比例图及游戏未验收。
<!-- CITY-DRAMA-S81:END -->

<!-- CITY-DRAMA-S82:BEGIN -->
2026-10-12 S82：伊德斯／佛尔霍特八案逐角色源为eeders／forholt的drama.json、feedback.json；入口design/11_管理/伊德斯与佛尔霍特人物演出审查.md。24场、16方法、29旧回执，10新卡；住梁未安置不拆，索名撤权不清旧泄露，救援立即执行、伤者真出井才演新句；矿份非金币，底薪／水款／检费／售款各真实占一次。当前73篇逐角色初稿、0篇待深化；旧314边、NE／奖励／N17保留，运行Validate-ForestAndMineDrama.py与既有检查，数值、比例地图和游戏未验收。
<!-- CITY-DRAMA-S82:END -->

<!-- CITY-DRAMA-S83:BEGIN -->
2026-10-12 S83：奥斯布鲁克／拉滕八案源为osbrook／ratten的drama.json与feedback.json，入口design/11_管理/奥斯布鲁克与拉滕人物演出审查.md。24场、16方法、29旧回执、11新卡；芙朵学艺／蔻芙婚事分户，种／饭、父债／路费、门钥／互助、婚／地各准；伪响不盖真风险，旧兽仍死，假章不判全部旧史，基本给付不买出席。当前73篇逐角色稿、0篇待深化，旧314边／NE／奖励／N17保，运行Validate-GrainAndMemoryDrama.py与既有检查；数值、比例地图和游戏未验收。
<!-- CITY-DRAMA-S83:END -->

<!-- CITY-DRAMA-S84:BEGIN -->
2026-10-12 S84：考德／柏石关八案源为korde／passgate各drama.json与feedback.json，入口design/11_管理/考德与柏石关人物演出审查.md；24场、16方法、28回执、12新卡、一封独立家书。考德物／房／代理分，族史unknown；埃文、兰衍、成年赛洛分人。雷奥莫伦同原身体，一床单占，N7／SQ02方法与CO真条件保，不二奖；原信送出不留原件、本人准副件可背包，口信不强纸。当前73篇逐角色稿、0篇待深化，运行Validate-NamesAndPassDrama.py及既有检查；数值、比例图与游戏未验收。
<!-- CITY-DRAMA-S84:END -->

<!-- FULL-REPLAY-S112:BEGIN -->
2026-10-13 S112：全链复跑演练（隔离副本重跑37写手/38校验器/vault并与主库逐文件比对）：design/ 597/598 逐字节一致（唯一差异为 design/AGENTS.md 块顺序，内容一致）、research/ 151/152 一致（唯一差异为副本内美术校验报告，环境项）；写手 34 直接通过、3 需参数或素材；校验器 35/38（3 美术为环境项）。演练暴露并修复：六篇城市演出审查陈旧句（“其它8篇”→“0篇”）、阶段验收记录陈旧计数（改为读校验报告）。副本位于 %TEMP%/eao-full-replay；不部署游戏包。
<!-- FULL-REPLAY-S112:END -->

<!-- FULL-REPLAY-S119:BEGIN -->
2026-10-13 S119：全链复跑第二轮（43写手/44校验器/vault，逐文件比对：design 602/603、research 168/169 一致，仅 AGENTS 块顺序与美术环境项不同）。修复阶段验收记录的内嵌计数漂移（三处硬编码改读实时报告）并给 Validate-FieldStage 加“计数＝实时报告”守卫；流程文档增“记录页在校验器之后重跑”规则。不部署游戏包。
<!-- FULL-REPLAY-S119:END -->

<!-- OFFICIAL-TERMS-S121:BEGIN -->
2026-10-13 S121：官方英文术语与服务班英文。Probe-OfficialTerms.py 只读 STRG 做中文段逐字匹配，6/14 条取得官方英文并纠正旧“含词定位”索引（保留为 official_index_contains）；服务班补 convenience_en/refresh_en；中英对照覆盖报告：用户可见文本 1272 组成对、中文单语 0。运行 Validate-FineDetails/ServiceRegistry/BilingualCoverage 及既有检查；不部署游戏包。
<!-- OFFICIAL-TERMS-S121:END -->

<!-- FULL-REPLAY-S126:BEGIN -->
2026-10-13 S126：全链复跑第三轮（45写手/50校验器/vault；design 608/609、research 185/186 一致，仅 AGENTS 块顺序与美术环境项不同）。暴露并修复：AGENTS 的 S124/S125 规则块陈旧（重跑写手）、brynn-continuation-integration 状态字典哈希陈旧（重跑续篇并加 integration-hash 守卫）。不部署游戏包。
<!-- FULL-REPLAY-S126:END -->

<!-- FIELD-NPC-S127:BEGIN -->
2026-10-13 S127：野外人物第二批八人（洞穴/野兽洞穴/老梣树/暴雨谷地/矿洞/食尸鬼巢穴/土匪营地/空地营帐），36人/504条中英对照；地点卡补链、迹象保留（合计覆盖44处）。联动：条件流36、状态键1393（presence150）、事件桩1807；独特性全库4376行/790组。运行Validate-FieldNpcDialogue/ModLocationCrosscheck/SpecialSiteCards/FieldSigns/FieldFlows/StateKeys/EventStubs及既有检查；不部署游戏包。
<!-- FIELD-NPC-S127:END -->

<!-- FULL-REPLAY-S131:BEGIN -->
2026-10-13 S131：全链复跑第四轮（48写手/53校验器/vault；design 619/620、research 194/195 一致，仅 AGENTS 块顺序与美术环境项不同）。暴露并修复：S129/S130 规则块由文档步骤写入、与写手措辞不同（重跑写手）；立“AGENTS 规则块由写手独占”的块归属规则。不部署游戏包。
<!-- FULL-REPLAY-S131:END -->

<!-- REP-BASE-LINK-S136:BEGIN -->
2026-10-13 S136：原作参照与城镇声望设计互链。两张原作参照卡（契据结构、声誉档位与地方状态）接入 [[城镇声望与信任系统]] 与 [[城镇声望系统中英对照]]，写明三层账对应与不照搬项（不写原版档位消息、不引入库存/价格/预支/外溢、折扣≤15%、不改通缉）；参照卡回链设计页。运行Validate-ReputationBaseLink.py及既有检查；不部署游戏包。
<!-- REP-BASE-LINK-S136:END -->

<!-- QUALITY-GUARDS-S142:BEGIN -->
2026-10-13 S142：质量守卫扩至七项。新增「方法数」（家族感知；低于2条方法的脚本0篇，S62多种解法成立）与「X边闭合」（矩阵74条、无引用0、悬空0）两项，连同结构覆盖/说话人闭合/对白去重/链接完整/占位扫描共七项，全部按实时重算渲染于 [[质量守卫总表]]。运行Validate-QualityGuards.py及既有检查；不部署游戏包。
<!-- QUALITY-GUARDS-S142:END -->

<!-- README-CLAIMS-S147:BEGIN -->
2026-10-13 S147：README活体状态对齐并加机检状态行。「设计库现状（2026-10-13）：台本131篇、城市任务79篇、逐角色稿待深化0篇、质量守卫7项」四项计数由 Validate-ReadmeClaims.py 现场重算核对；旧「71 篇逐角色初稿」「S86 工具未执行」「八篇待完成」口径已作废；第一版51篇保留为历史。只改活体文字，日期块不动。
<!-- README-CLAIMS-S147:END -->

<!-- OPEN-ITEMS-S149:BEGIN -->
2026-10-13 S149：待办登记刷新至15项。新增 OI-13（重建结构回归输入：broken/fixed .win 与记录哈希不匹配）、OI-14（验证快照不得清理：11份 backups/… 为保留性检查基线）、OI-15（按既有工程新建事件：0.3.0 包不含 S62+ 设计稿）；OI-11 补基线指针。入口design/11_管理/待办与已知缺口登记.md；运行Validate-OpenItems.py及既有检查；不部署游戏包。
<!-- OPEN-ITEMS-S149:END -->

<!-- NAV-STATUS-S148:BEGIN -->
2026-10-13 S148：三张导航页加入机检状态行。台本131篇（晶石51＋城市79＋野外1）、卫星聚落33篇、质量守卫7项；由 Validate-NavStatus.py 现场重算核对（家族计数、卫星笔记数、守卫行数），计数变化须重跑写手刷新。
<!-- NAV-STATUS-S148:END -->

<!-- CHAIN-ORDER-S150:BEGIN -->
2026-10-13 S150：链路顺序规则“清单即保护范围”。写手把写过的笔记记入各自 *note-hashes.json；BrynnContinuation.py 汇总全部清单并在写前逐个校验哈希，手工改过受保护笔记后必须先重跑拥有该条目的写手刷新清单再跑它，否则按设计拒绝并连锁 manifest-reconciled 失败。规则见 design/11_管理/设计库生成与校验流程.md 顺序约束节；不得直接改清单数值掩盖冲突。
<!-- CHAIN-ORDER-S150:END -->

<!-- CITY-S63:BEGIN -->
2026-10-12 S63：城市范围为十二命名聚落＋三原创地域，设计入口为design/00_导航/城市与聚落设计总索引.md。六区54节点仅早期连接场景，旧限制已被扩展纸面设计取代，不能据此缩回八城。N1—N18、NE与终局保持S62规则；CM地方篇章无全城游历前置，PAS/ASH/HIG为现有任务编排而非第二奖励。新版另用research/city-campaign.json管理城市/卫星/任务/条件回执，运行Validate-CityCampaign.py和原三项检查。通路SVG与概念板只作设计参考，房间美术/经济/运行未经验证不能称完成。
<!-- CITY-S63:END -->

<!-- FINE-DETAILS-S91:BEGIN -->
2026-10-13 S91：S89的172名人物细描已回灌各自人物卡（块标记FINE-DETAILS-CARD-S91，含体貌/衣着/随身/举止/风格守卫）；补建艾娜、纳拉、妮尔、塞尔四张主线配角卡，玛拉与伊沃共卡双块。十个整篇重写人物卡的生成器已接入NotePreserve保留外部登记块；Attach-FineDetails.py维护research/fine-details-card-note-hashes.json并回写各哈希清单。入口design/04_人物/人物细描与随身物.md；风格描述不替代美术终稿与运行验证。
<!-- FINE-DETAILS-S91:END -->

<!-- SPECIAL-LOC-S92:BEGIN -->
2026-10-13 S92：用户要求扩充特殊地点与野外NPC对白。research/special-location-inventory.json 只读清点原版特殊地点候选：8个世界地图区域、44个传闻地点、13个地形类型名与对白族规模（场景326/问候446/闲谈125/NPC227/随从8）；只存键名/STRG序号/中文可用性/短地点名，不存对白全文。入口design/01_原作基线/特殊地点与野外NPC清点.md；逐NPC中英对读、野外遭遇映射、Mod原创地点清点与地点设计卡仍待做。Probe-SpecialLocations.py与Write-SpecialLocationCard.py为作者工具，运行Validate-SpecialLocationInventory.py及既有设计检查；不部署游戏包。
<!-- SPECIAL-LOC-S92:END -->

<!-- NPC-READING-S93:BEGIN -->
2026-10-13 S93/S98：用户要求扩充特殊地点与野外NPC对白。research/original-npc-reading.json 把原版问候446/闲谈125按说话人槽归组（全槽覆盖）并逐组给口吻/主题/结构/短例定位；S98 增 npc 227 条行为槽分组（工具句、声望7档行为集、角色闲话标签、状态天气、商人变体）与场景族结论（scene 326 键可枚举、文本与分支在引擎侧）。入口design/01_原作基线/野外NPC口吻与闲谈参照.md。对白全文不入库、短例≤48字；不部署游戏包。
<!-- NPC-READING-S93:END -->

<!-- FIELD-NPC-S94:BEGIN -->
2026-10-13 S94/S97/S99/S106：用户要求扩充特殊地点与野外NPC对白（含中英对照）。research/field-npc-dialogue.json 登记 36 名Mod原创野外人物，覆盖S92地点类型中的28处（石场/磨坊/陵墓/废墟/修院/围城营地/麻风院/蛛洞/哈比巢/蜂巢/药师家/女巫邻居/老堡/荒宅/旅馆/猎场/疫村/食尸鬼巢穴/烂柳酒馆/三刀会窝点/矿洞/洞穴/裁缝宅子/废弃庄园/兵营/堡垒/荒废营地/安静农宅），每人含体貌、口吻、知情边界与中文先行对白（初次/复访/夜里、三条闲谈、到场/警告/拒绝），并有条件回访：任务进行中/完成后、先做或后做关联任务、本人缺席时旁人可代述的有限句；拒绝有替代出口，不新增奖励、不占原生服务、不做全巡前置。S106补28人×14槽英文稿（Mod原创新稿，不冒充原版译文，逐条与中文同槽）。入口design/02_世界与地图/特殊地点与野外NPC/台本_FX_野外人物对白.md与各人物卡；运行Validate-FieldNpcDialogue.py、Validate-DialogueDistinctiveness.py及既有检查；比例位置与引擎触发仍待做，不部署游戏包。
<!-- FIELD-NPC-S94:END -->

<!-- SITE-CARDS-S95:BEGIN -->
2026-10-13 S95：用户要求扩充特殊地点内容。44个传闻地点按6个地域拆成地点设计卡（入口/安全回程锚点、观察物、危险、服务=无、原作避让、逐地点关联），入口design/02_世界与地图/特殊地点与野外NPC/特殊地点设计卡总表.md。设计意图，未定比例/碰撞/运行房间；不新增服务与奖励、不新增前置。运行Validate-SpecialSiteCards.py及既有检查；不部署游戏包。
<!-- SITE-CARDS-S95:END -->

<!-- MOD-LOC-XCHECK-S96:BEGIN -->
2026-10-13 S96：按计划第5步交叉核对Mod特殊地点与人物。research/mod-location-crosscheck.json：9个副本各归R01—R06并只由唯一任务结算、6个布林续篇场景归布林、16名野外人物无重名无重复挂点；入口design/11_管理/Mod特殊地点与人物交叉核对.md。运行Validate-ModLocationCrosscheck.py及既有检查；坐标、实际排布与英文稿仍待做，不部署游戏包。
<!-- MOD-LOC-XCHECK-S96:END -->

<!-- FIELD-DOCS-S100:BEGIN -->
2026-10-13 S100：用户要求扩充特殊地点内容。research/field-docs.json 登记 12 份Mod原创野外地点短文书（原件/副件/残件分记，绑S94/S99人物与S92地点），入口design/02_世界与地图/特殊地点与野外NPC/文书_FX_野外地点短稿.md。阅读只给信息：不完成任务、不发奖励、不替代当事人同意；不设收集式门槛。运行Validate-FieldDocs.py及既有检查；摆放与交互脚本仍待做，不部署游戏包。
<!-- FIELD-DOCS-S100:END -->

<!-- FIELD-SIGNS-S101:BEGIN -->
2026-10-13 S101：用户要求扩充各特殊地点。research/field-signs.json 为剩余16处地点补“迹象与观察”（观察/判定提示/危险退路），入口design/02_世界与地图/特殊地点与野外NPC/野外迹象与观察.md；44处传闻地点至此全部有落点（28人物＋16迹象）。迹象只给信息：不发奖励、不完成任务、不替代同意；判定不含数值掉落。运行Validate-FieldSigns.py及既有检查；生成点与比例仍待制作，不部署游戏包。
<!-- FIELD-SIGNS-S101:END -->

<!-- BRANCH-COVERAGE-S103:BEGIN -->
2026-10-13 S103：按计划剩余项「对白分支」做结构审计。research/branch-coverage.json 覆盖 130 个脚本（城市73/续篇6/主线·支线·后章·副本/日常16）：多方法、逐方法先做后做、早晚回执、拒绝或缺席替代、知识守卫与中断恢复齐备，不合口径无。入口design/11_管理/对白分支覆盖审计.md；只审字段结构，不评文学、不证明运行；运行Validate-BranchCoverage.py及既有检查；不部署游戏包。
<!-- BRANCH-COVERAGE-S103:END -->

<!-- REGION-MAP-S104:BEGIN -->
2026-10-13 S104：用户要求扩充各特殊地点。research/region-content-map.json 把8个原作世界地图区域映射到Mod地域/地点卡/野外人物，入口design/02_世界与地图/特殊地点与野外NPC/原作地图区域与Mod内容映射.md；只做映射与避让口径：不占区域、不改原作地图与任务、不新增服务；比例与生成点仍待做。运行Validate-RegionContentMap.py及既有检查；不部署游戏包。
<!-- REGION-MAP-S104:END -->

<!-- FIELD-FLOWS-S105:BEGIN -->
2026-10-13 S105：把28名野外人物的对白投影成实现可用的条件流。research/field-scene-flows.json 含固定条件词表与逐人节点图（初遇/夜里/复访、任务进行中/完成后、先做/后做、拒绝出口、缺席替代），节点只引用登记台词；入口design/02_世界与地图/特殊地点与野外NPC/野外对白条件流.md。不新增奖励与结算、不改台本状态；引擎侧触发距离与生成点仍待做。运行Validate-FieldFlows.py及既有检查；不部署游戏包。
<!-- FIELD-FLOWS-S105:END -->

<!-- PROD-PROTOCOL-S108:BEGIN -->
2026-10-13 S108：特殊地点阶段剩余四项（经济数值、比例与生成点、运行验证、引擎侧触发）出制作与校准规程。research/production-protocol.json 定义测量对象/记录字段/采样/通过条件/禁止清单；入口design/11_管理/特殊地点阶段制作与校准规程.md。不含实测数字，未测量不得补值；运行与数值仍待实机。运行Validate-ProdProtocol.py及既有检查；不部署游戏包。
<!-- PROD-PROTOCOL-S108:END -->

<!-- RULE-AUDIT-S109:BEGIN -->
2026-10-13 S109：野外内容规则一致性审计。research/rule-audit.json 重算 14 项（无奖励/前置/重复任务字段、拒绝与缺席出口、知情边界、中英对齐、服务不新增、44地点落点），入口design/11_管理/野外内容规则一致性审计.md。只验规则与结构；运行、数值与生成点见制作规程。运行Validate-RuleAudit.py及既有检查；不部署游戏包。
<!-- RULE-AUDIT-S109:END -->

<!-- CORPUS-FLOWS-S113:BEGIN -->
2026-10-13 S113：全库条件流投影（实现桥）。research/corpus-flows.json 把 130 个脚本（城市73/续篇6/主线·支线·后章·副本/日常16）投影成固定词表条件图，refs 逐条回指源原句、notes 载守卫与例外；入口design/11_管理/全库条件流投影.md。投影不新写台词、不含奖励/结算字段、不改台本；运行Validate-CorpusFlows.py及既有检查；引擎触发与部署仍待实现阶段。
<!-- CORPUS-FLOWS-S113:END -->

<!-- STATE-KEYS-S114:BEGIN -->
2026-10-13 S114：状态键映射（实现桥）。research/state-keys.json 由源确定性推导 1393 个实现用状态键（encounter/resolve/callback/consent/paid/order/presence＋329 个跨任务回执）；键名 ID 中 `-` 换 `_`，resolve 结算前 none、结算后唯一取值，回执只记已播。入口design/09_系统逻辑/状态键映射总表.md；条件流 when 的映射见页内。不迁移旧存档、不含奖励语义；运行Validate-StateKeys.py及既有检查；不部署游戏包。
<!-- STATE-KEYS-S114:END -->

<!-- AMBIENT-GOSSIP-S115:BEGIN -->
2026-10-13 S115：地区闲谈池（原创，中英对照）。research/ambient-gossip.json 六地域 30 条，条件词表 any/night/band:+1/band:-1/after:<台本>；只谈本区生活与旧事，不发奖励、不推进任务、不写状态键。入口design/02_世界与地图/特殊地点与野外NPC/地区闲谈池.md；运行Validate-AmbientGossip.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。
<!-- AMBIENT-GOSSIP-S115:END -->

<!-- TOWN-GOSSIP-S116:BEGIN -->
2026-10-13 S116：城镇闲谈池（原创，中英对照）。research/town-gossip.json 十五城镇各4条共 60 条，条件 any/night/after:<主章台本>；城镇内说行当与街面、城外见地区闲谈池；不发奖励、不推进任务、不写状态键。入口design/02_世界与地图/特殊地点与野外NPC/城镇闲谈池.md；运行Validate-TownGossip.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。
<!-- TOWN-GOSSIP-S116:END -->

<!-- BAND-GOSSIP-S117:BEGIN -->
2026-10-13 S117：声望档街头反应（原创，中英对照）。research/band-gossip.json 十五城镇与六地域各2条冷/热档口气（band:-1 / band:+2）共 42 条；只写口气与场面，不承诺服务、不发物品、不给情报，且与柜台台词不重复。入口design/02_世界与地图/特殊地点与野外NPC/声望档街头反应.md；运行Validate-BandGossip.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。
<!-- BAND-GOSSIP-S117:END -->

<!-- EVENT-STUBS-S118:BEGIN -->
2026-10-13 S118：事件桩映射（实现桥末端）。research/event-stubs.json 把条件流每个节点映射成事件桩（共 1807 个：命名/触发/读写状态键/冷却），读写键必须在状态键表内；不声明真实引擎事件号。入口design/09_系统逻辑/事件桩映射总表.md；运行Validate-EventStubs.py及既有检查；引擎号、触发距离与存档字段仍待实现阶段。
<!-- EVENT-STUBS-S118:END -->

<!-- BILINGUAL-COVERAGE-S120:BEGIN -->
2026-10-13 S120：中英对照覆盖报告。research/bilingual-coverage.json 逐登记重算：用户可见文本 1384 组成对、中文单语 0 条（目标0）；内部散文中文先行不计缺口；英文均为Mod原创。入口design/11_管理/中英对照覆盖报告.md；运行Validate-BilingualCoverage.py及既有检查；不部署游戏包。
<!-- BILINGUAL-COVERAGE-S120:END -->

<!-- KEY-NAMES-S123:BEGIN -->
2026-10-13 S123：键名口径对账。research/key-naming-reconciliation.json 把S62旧族级字段名映射到S114按脚本/按路线键；[[状态键映射总表]]为唯一权威，旧名只作阅读别名、不双写；两篇旧文加提示块。入口design/09_系统逻辑/键名口径对账.md；运行Validate-KeyNaming.py及既有检查；引擎字段与旧档迁移仍待实现。
<!-- KEY-NAMES-S123:END -->

<!-- INTERIOR-AMBIENT-S124:BEGIN -->
2026-10-13 S124：副本与日常氛围句（原创，中英对照）。research/interior-ambient.json 9副本×3现场观察＋16日常×2周边口气共 59 条；不推进任务、不写状态键、不揭未核真相，after 只改未来口气。入口design/02_世界与地图/特殊地点与野外NPC/副本与日常氛围句.md；运行Validate-InteriorAmbient.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。
<!-- INTERIOR-AMBIENT-S124:END -->

<!-- CONTENT-INVENTORY-S125:BEGIN -->
2026-10-13 S125：叙事内容清单。research/content-inventory.json 一页列全叙事资产与桥接层（用户可见文本约 870 个单元）；入口design/00_导航/叙事内容清单.md；计数取自源、重跑刷新。只做索引与计数；运行Validate-ContentInventory.py及既有检查；不部署游戏包。
<!-- CONTENT-INVENTORY-S125:END -->

<!-- PLAYTEST-S128:BEGIN -->
2026-10-13 S128：试玩路线与检查单。research/playtest-walkthrough.json 十一试玩段（步骤/观察点/证据项），由既有设计派生；入口design/11_管理/试玩路线与检查单.md。不新增设计内容；实现后按规程记录运行证据。运行Validate-Playtest.py及既有检查；不部署游戏包。
<!-- PLAYTEST-S128:END -->

<!-- DISTRICT-AMBIENT-S129:BEGIN -->
2026-10-13 S129：街区氛围句（原创，中英对照）。research/district-ambient.json 十五城 66 街区各1条，按街区功能写；与四套闲谈池不重复、不发奖励、不推进任务、不写状态键。入口design/02_世界与地图/特殊地点与野外NPC/街区氛围句.md；运行Validate-DistrictAmbient.py、Validate-DialogueDistinctiveness.py及既有检查；触发与配音待实现。
<!-- DISTRICT-AMBIENT-S129:END -->

<!-- AMBIENT-REVIEW-S130:BEGIN -->
2026-10-13 S130：氛围层总览与冻结建议。research/ambient-review.json 清点九层共 936 个可播单元并给出冻结口径（只有新增地点/聚落/派系时才加句；不新增室内级逐间台词）；入口design/11_管理/氛围层总览与冻结建议.md。只做清点与口径；运行Validate-AmbientReview.py及既有检查；触发与配音待实现。
<!-- AMBIENT-REVIEW-S130:END -->

<!-- NAME-COLLISION-S132:BEGIN -->
2026-10-13 S132：原作名与原创名碰撞核对（只读）。Probe-NameCollisions.py 扫 7 类原创专名对 STRG 简体槽：精确同名 1（「玛拉」命中程序化女名池 14956—14971，保留并标注同形不同人）、近似 4（仅前缀巧合）；物品/街区/室内/场景 0 命中。入口design/01_原作基线/原作名与原创名碰撞核对.md；新增专名后重跑扫描。运行Validate-NameCollision.py及既有检查；不部署游戏包。
<!-- NAME-COLLISION-S132:END -->

<!-- CONTRACT-REF-S134:BEGIN -->
2026-10-13 S134：原作契据任务与声誉结构参照（只读探针）。6设置项（时限/可领数/按地牢类型声誉收益）、5信息流（%town_name%/%contract_name%/%rep_amount%）、144契据键、60行巨魔契据状态化对白、667标识符名；对照口径：不用「契据」名、地方信任与原版声望分开、不做重复任务、不引入预支/外溢/竞争。入口design/01_原作基线/原作契据任务与声誉结构参照.md；片段≤46字。运行Validate-ContractReference.py及既有检查；不部署游戏包。
<!-- CONTRACT-REF-S134:END -->

<!-- REP-REF-S135:BEGIN -->
2026-10-13 S135：原作声誉档位与地方状态参照（只读探针）。10信息流（村落/阵营/全域+界面）、20来源（任务/贸易/犯罪等，均带[声誉%rep_amount%]）、20档位（特殊任务/特色商品/赏金预付/库存±10..50%/交易±5..30%/本地公敌）、两档通缉、15地方状态；对照口径：地方信任与原版声望分开、信任档只改范围与便利、不照搬数值、不写地方状态修正、不改通缉。入口design/01_原作基线/原作声誉档位与地方状态参照.md；片段≤46字。运行Validate-ReputationReference.py及既有检查；不部署游戏包。
<!-- REP-REF-S135:END -->

<!-- DIALOGUE-COVERAGE-S137:BEGIN -->
2026-10-13 S137：逐角色稿完成度核对（结构重算）。131篇台本逐篇核对对话树/场次节、场次标记、说话人行数与版本标记：130篇有对话节（例外为野外人物对白卡格式）；城市稿ASH/HIG各3篇已于S86深化、布林续篇六篇各有场1—3，当前待深化0篇；旧「各四篇/8篇待深化」保留为S84/S85历史记录，计划页旧句改为指向本页。入口design/11_管理/逐角色稿完成度核对.md；运行Validate-DialogueCoverage.py及既有检查；不部署游戏包。
<!-- DIALOGUE-COVERAGE-S137:END -->

<!-- SPEAKER-CLOSURE-S138:BEGIN -->
2026-10-13 S138：说话人与人物卡闭合核对。逐行取说话人 232 位全部归类（玩家/人物卡精确/前缀/提及/通用称谓/标记），未闭合 0 位；白名单research/speaker-allowlist.json（通用称谓与标记不建卡）；新增说话人未列入白名单时校验报错。入口design/11_管理/说话人与人物卡闭合核对.md；运行Validate-SpeakerClosure.py及既有检查；不部署游戏包。
<!-- SPEAKER-CLOSURE-S138:END -->

<!-- DIALOGUE-DISTINCT-S139:BEGIN -->
2026-10-13 S139：对白去重与独特性核对（整句完全匹配）。逐行抽取2717行、去重2699条；完全重复18组，全部为主章—副本配对（同一人物跨N/D，有意一致），待复核0组。新增重复不属配对时校验报错，须改写或登记理由。入口design/11_管理/对白去重与独特性核对.md；运行Validate-DialogueDistinctiveness.py及既有检查；不部署游戏包。
<!-- DIALOGUE-DISTINCT-S139:END -->

<!-- RX-HEADERS-S141:BEGIN -->
2026-10-13 S141：R/X头部补齐。城市稿79篇中14篇原有R/X头、65篇带派生块（仅用脚本内既有方法小节、resolve_/paid_键与回访名，不新增设定、不改既有文字，逐篇比对保证只增块）。N/SQ/DT/D另用「可执行解法＋本任务影响的后事」与-R-键名，不在本次范围。入口design/11_管理/R-X头部补齐记录.md；运行Validate-RXHeaders.py及既有检查；不部署游戏包。
<!-- RX-HEADERS-S141:END -->

<!-- VERIFY-RECORD-S151:BEGIN -->
2026-10-13 S151：验收记录补记与连续性守卫。补 S101（野外迹象与观察16处）与 S120（中英对照覆盖：成对1384组、用户可见中文单列0）两段补记块；Validate-VerificationRecord.py 断言 S 编号块 BEGIN/END 成对且区间无缺口（当前64块、S87—S150），新增记录不得留空号。
<!-- VERIFY-RECORD-S151:END -->

<!-- PILOT-N2-SCEN-S154:BEGIN -->
2026-10-13 S154：试点批次验收场景N2。6条场景覆盖N2全部5键（encountered/resolve/callback×2/presence），期望写入逐条对照取值集合校验，含拒绝、已结案回访与存读档顺序场景；仅场景清单与口径，不含实现代码、不部署。入口design/11_管理/试点批次验收场景N2.md；运行Validate-PilotScenarios.py及既有检查。
<!-- PILOT-N2-SCEN-S154:END -->

<!-- PILOT-N2-S153:BEGIN -->
2026-10-13 S153：试点实现批次N2。把实现交接六步收敛为首个可验收切片（N2）：5桩、5键、5流节点、3解法、X边5条；给出落地顺序、建议GML文件与验收项；仅排程与输入提取，不含实现代码、不分配事件号、不部署。入口design/11_管理/试点实现批次N2.md；运行Validate-PilotBatch.py及既有检查。
<!-- PILOT-N2-S153:END -->

<!-- PILOT-BRY01-S156:BEGIN -->
2026-10-13 S156：试点实现批次CS-BRY-01（系统层）。14桩、10键、14流节点、2解法；含服务班（SVC-BRY）/信任档/闲谈池（城镇4条、档位2条）接线与7条验收场景（早到晚到、拒绝缺席、服务档位、闲谈分池）。键名口径同S155；仅排程与输入提取，不含实现代码、不部署。入口design/11_管理/试点实现批次CS-BRY-01.md；运行Validate-PilotBry01.py及既有检查。
<!-- PILOT-BRY01-S156:END -->

<!-- PILOT-FX-S157:BEGIN -->
2026-10-13 S157：试点实现批次FX野外层。以 FX-QRY 为例覆盖野外层（存在性四态/条件回访/文书只给信息/迹象判定/三池闲谈 地区30／城镇60／声望档42 条），5条验收场景；与 N2（主章）、CS-BRY-01（城市系统）合起来覆盖实现交接六步的全部接线类型；仅排程，不含实现代码、不部署。入口design/11_管理/试点实现批次FX野外层.md；运行Validate-PilotFx.py及既有检查。
<!-- PILOT-FX-S157:END -->

<!-- PILOT-INDEX-S158:BEGIN -->
2026-10-13 S158：试点批次总表（实现轮单一入口）。三批合计 19桩／15键／28流节点／5解法／18验收场景，覆盖实现六步全部接线类型；共享键名口径（EAO_＋登记键名）、前置（OI-02/OI-03）与验收方式（同候选SHA＋按规程记录）；建议顺序 P1→P2→P3。入口design/11_管理/试点批次总表.md；运行Validate-PilotIndex.py及既有检查。
<!-- PILOT-INDEX-S158:END -->

<!-- HANDOFF-LINKS-S159:BEGIN -->
2026-10-13 S159：交接↔试点互链。实现交接总表加首批执行说明（按试点批次总表 P1→P2→P3），OI-01 指向试点总表，试点总表回链交接总表；Validate-HandoffLinks.py 断言三向互链与链接解析。入口三页见 design/11_管理/。
<!-- HANDOFF-LINKS-S159:END -->

<!-- TOOLCHAIN-S162:BEGIN -->
2026-10-13 S162：结构回归输入复核。GameProbe --assert-eao-struct-access 复跑：direct-data.win 通过（可作fixed输入）、repeat-data.win 属另一失败模式（Courier InvalidDataException）、vanilla-0.2.0.win 通过；仅缺故意损坏的broken输入，OI-13已更新。入口design/11_管理/工具链离线自检记录.md；运行Validate-ToolchainChecks.py及既有检查；不构建、不部署。
<!-- TOOLCHAIN-S162:END -->

<!-- EVT-NUM-S163:BEGIN -->
2026-10-13 S163：事件号分配方案。1,807桩按家族基址（N10000/SQ20000/DT30000/D40000/CS50000/CM60000/FX70000）＋脚本64对齐块确定性预分配，一桩一号不复用，退役不转号；引擎号实现时分配并回写事件桩映射总表；纸面方案，原生事件号空间未读取。入口design/11_管理/事件号分配方案.md；运行Validate-EventNumbers.py及既有检查。
<!-- EVT-NUM-S163:END -->

<!-- NAV-BLOCK-S164:BEGIN -->
2026-10-13 S164：设计总览导航块扩容至S125—S163。按四组（清点与交接/原作参照/质量守卫/实现准备）列28个入口，含三批试点、引擎键、N1键语义与事件号方案；Validate-NavBlock.py 断言目标笔记全部存在且链接解析。只改导航与生成模板。
<!-- NAV-BLOCK-S164:END -->

<!-- OPEN-ITEMS-S133:BEGIN -->
2026-10-13 S133：待办与已知缺口登记。research/open-items.json 汇总 12 项（实现5/制作3/实机3/设计可选1/口径1），标明负责方、前置与证据；设计总览补最新入口块。入口design/11_管理/待办与已知缺口登记.md；只汇总不改门槛。运行Validate-OpenItems.py及既有检查；不部署游戏包。
<!-- OPEN-ITEMS-S133:END -->

<!-- TOOLCHAIN-S166:BEGIN -->
2026-10-13 S166：结构回归关闭（OI-13）。broken输入取自backups/direct-20261011-155606-160/data.win（67B2D55E…），fixed改用当前构建artifacts/direct-data.win（4D863960…，旧fixed文件已不满足更严linkage检查）；复跑通过、记录已按今日重写。修好两处工具缺陷（预期stderr终止脚本→局部Continue；utf8NoBOM→WriteAllText，兼容PS5.1）；待办登记15→14项。入口design/11_管理/工具链离线自检记录.md；运行Validate-ToolchainChecks.py及既有检查；不构建、不部署。
<!-- TOOLCHAIN-S166:END -->

<!-- PS-PORTABILITY-S167:BEGIN -->
2026-10-13 S167：PowerShell 兼容性排查。tools/*.ps1 中 6 处 PS7 专有 -Encoding utf8NoBOM（Deploy-Mod 4／Prepare-TestEnvironment 2／Check-FormalEnvironment 1）改为 [IO.File]::WriteAllText + UTF8Encoding(false)；六个脚本解析器静态检查 parse_errors=0；Validate-PsPortability.py 断言无 PS7 专有构造。未构建、未部署。
<!-- PS-PORTABILITY-S167:END -->

<!-- BUILD-CHAIN-S169:BEGIN -->
2026-10-13 S169：构建输入链核对（只读）。部署记录分支=--repair-eao（定向修复）、当前data.win与记录一致（4D863960…）、修复源backups/direct-20261011-202449-265/data.win存在（143A9697…）、回滚备份含data.win/before.json/旧包/Settings.json/userdata。若data.win与记录不一致，构建脚本改用当前文件作新输入（已含EAO补丁会被拒绝）。入口design/11_管理/构建前置核对.md；运行Validate-BuildReadiness.py及既有检查。
<!-- BUILD-CHAIN-S169:END -->

<!-- BUILD-RUN-S170:BEGIN -->
2026-10-13 S170：本地构建（未部署）。tools/Build-Mod.ps1（无 -Deploy）跑通：新包 FF5D90F7…、新候选 direct-data.win 2F669A1C…，输入当前组合（定向修复）；重复补丁拒绝/非EAO原代码未改/链接通过/原身份保留；四套离线套件执行；runtimeVerified=false。本地候选≠已部署副本（旧3B3EF27A…）——实现侧现状页如实报告"候选较新，部署待放行（OI-11）"；未部署、未改游戏目录。入口design/11_管理/构建前置核对.md；运行Validate-ImplState.py与Validate-BuildReadiness.py及既有检查。
<!-- BUILD-RUN-S170:END -->

<!-- HOOK-MAP-S171:BEGIN -->
2026-10-13 S171：触发器接线点映射（只读）。1807桩的8种触发逐一接到小样原生钩子（characterDataMap/__dialogue_flow_data/instance_create_depth/event_user/scr_quest_get_complete），附证据行号与口径；实现轮照此接线并逐桩回写；不改源码、不构建、不部署。入口design/11_管理/触发器接线点映射.md；运行Validate-HookMapping.py及既有检查。
<!-- HOOK-MAP-S171:END -->

<!-- REF-GAMES-S172:BEGIN -->
2026-10-13 S172：参考游戏对照页守卫。Validate-ReferenceGames.py 断言四款点名游戏（BG3/DOS1/DOS2/Drova）各有机制行与教训、取舍映射表覆盖四款并回链设计页、引用全部为URL、保持外部研究与未验证边界。入口design/11_管理/参考游戏叙事与声望机制对照.md；只读守卫，未改页面。
<!-- REF-GAMES-S172:END -->

<!-- ASK-TRACE-S173:BEGIN -->
2026-10-13 S173：用户要求与交付对照。12行逐条对应“要求→交付页→守卫→状态”（背景/台词/任务/声望/中英对照/参照游戏/网状/伏笔/NPC/原作参照/设计参考/阶段规则），交付页33个全部存在、守卫工具存在；done不表示游戏内已实现；未完成项指向待办登记。入口design/11_管理/用户要求与交付对照.md；运行Validate-AskTraceability.py及既有检查。
<!-- ASK-TRACE-S173:END -->

<!-- USER-SIDE-S175:BEGIN -->
2026-10-13 S175：用户侧前置状态（只读）。MSL Settings.json 合法且 EnableMods 含 EmbersAndOaths（共7项，其余为玩家自装，部署只追加不删除）；用户数据文件133个与记录 userFilesChecked 一致（自2026-10-11未变）。并入design/11_管理/部署与回滚运行手册.md；运行Validate-RollbackRunbook.py及既有检查；本轮未部署。
<!-- USER-SIDE-S175:END -->

<!-- TEXT-INJECT-S176:BEGIN -->
2026-10-13 S176：文本注入与本地化口径（只读提取）。证据：__dialogue_flow_data+npc_lines_map以json_parse注入（NativeDialogue.cs:114/130）、语言槽索引0=EN/1=CN（global.language==3取CN，:129）、文书走NativeDocuments原语；不改STRG、不依赖外部文件。本Mod台本对白2717行等将走同一机制；未接线、未构建、未部署。入口design/11_管理/文本注入与本地化口径.md；运行Validate-TextInjection.py及既有检查。
<!-- TEXT-INJECT-S176:END -->

<!-- NARRATIVE-DEPTH-S177:BEGIN -->
2026-10-13 S177：网状叙事深度审计（只读计算）。按BG3/DOS经验量化反应性：条件节点/先后槽/缺席槽/路线/入出向X边/说话人；城市稿73/73有early+absent；缺口：无先后槽57篇、无缺席槽57篇、无入向边102篇、无出向边81篇、节点≤4共16篇；附三条优化提案。入口design/11_管理/网状叙事深度审计.md；运行Validate-NarrativeDepth.py及既有检查；不改内容。
<!-- NARRATIVE-DEPTH-S177:END -->

<!-- BASELINE-REG-S146:BEGIN -->
2026-10-13 S146：验证快照依赖登记。工具源码中 11 份 backups/… 快照（城市/戏剧类保留性检查的“变更前”基线）逐份登记大小/哈希/用途，另 1 条为非依赖说明；缺任一份对应校验器无法运行，改动或替换由 Validate-PreservationBaselines.py 报错。入口design/11_管理/验证快照依赖登记.md；不复制、不修改、不删除备份。
<!-- BASELINE-REG-S146:END -->

<!-- REPLAY-S145:BEGIN -->
2026-10-13 S145：第五轮全链复跑演练。主库按生成链顺序重跑写手：通过54、需素材跳过6、失败0；重跑后65校验器与Test-DesignVault全通过。最小副本（design/research/tools/src）重跑同序：写手46通过/8中止（缺backups与artifacts输入，下游保留守卫按设计连锁）、校验器49通过/16失败（戏剧城市类读backups、美术类读素材、计数页读已中止写手结果）。结论：主库链路自洽、顺序敏感、环境依赖已清点；未声明整树字节一致。入口design/11_管理/全链复跑演练S145.md；不构建、不部署。
<!-- REPLAY-S145:END -->

<!-- IMPL-STATE-S143:BEGIN -->
2026-10-13 S143：实现侧现状核对（只读哈希）。构建包与MSL副本同哈希、data.win与部署记录一致、vanilla与基线一致；0.3.1完整验收runtimeVerified=false，开发观察实测独立登记；GML代码28个、构建/部署/检查脚本Build-Mod/Check-FormalEnvironment/Deploy-Mod/Prepare-TestEnvironment/Test-EaoStructRegression/Test-MslInput；S62—S143设计稿尚未进包，OI-01须在现有工程上新建事件。重建包后须重跑本页与校验器。入口design/11_管理/实现侧现状核对.md；运行Validate-ImplState.py及既有检查；不构建、不部署。
<!-- IMPL-STATE-S143:END -->

<!-- BUILD-READY-S168:BEGIN -->
2026-10-13 S168：构建前置核对（只读，不构建）。dotnet 10.0.401、构建脚本解析 errors=0、NuGet包 3/3 就位、MSL程序集 4/4 就位；构建会重写 .sml 与 direct-data.win，构建轮须一并重跑实现侧现状与收束核对页。入口design/11_管理/构建前置核对.md；运行Validate-BuildReadiness.py及既有检查。
<!-- BUILD-READY-S168:END -->

<!-- TOOLCHAIN-S144:BEGIN -->
2026-10-13 S144：工具链离线自检（只读）。Test-MslInput 正对照通过（vanilla.win：34189代码条目/9663对象/1067房间，无已知MSL/EAO标记）、负对照按预期拒绝（组合data.win）；Check-FormalEnvironment属隔离期已停用（快照指向已移除备份）；结构回归输入不在库中暂不可复跑；GameProbe已构建。入口design/11_管理/工具链离线自检记录.md；运行Validate-ToolchainChecks.py及既有检查；不构建、不部署。
<!-- TOOLCHAIN-S144:END -->

<!-- N1-KEYS-S161:BEGIN -->
2026-10-13 S161：N1小样键语义与迁移建议（只读扫描）。扫描EAO_N1_*共22处用法：EAO_N1_stage无任何写入点（静态结论，运行时未验证）；建议入口门槛改挂encountered_N1、解法用resolve_N1、stage仅作旧档读取垫片；origin族语义清楚可保留。供OI-03决策；不改源码、不改存档、不部署。入口design/11_管理/N1小样键语义与迁移建议.md；运行Validate-N1Keys.py及既有检查。
<!-- N1-KEYS-S161:END -->

<!-- ROLLBACK-S174:BEGIN -->
2026-10-13 S174：部署与回滚运行手册。部署五步（退出→构建验收→备份与替换→记录→部署后核对）与回滚六步（定位备份集→校验→还原data.win→还原设置与旧包→复核→留痕）按脚本实际行为写成；当前备份集 direct-20261013-155030-418 哈希已核对；不保证无损卸载、用户数据不动。本轮未执行部署或回滚。入口design/11_管理/部署与回滚运行手册.md；运行Validate-RollbackRunbook.py及既有检查。
<!-- ROLLBACK-S174:END -->

<!-- ENGINE-KEYS-S155:BEGIN -->
2026-10-13 S155：引擎键名前缀与遗留键登记。口径＝引擎键 `EAO_`＋登记键名；扫描已实现GML得33个EAO_键，全部为0.3.0期遗留（测试传送/N1小样/旧任务），映射登记键0个；小样EAO_N1_stage与登记resolve_N1须二选一（属OI-03）。只读扫描，不改源码与存档。入口design/11_管理/引擎键名前缀与遗留键登记.md；运行Validate-EngineKeys.py及既有检查。
<!-- ENGINE-KEYS-S155:END -->

<!-- REG-COVERAGE-S152:BEGIN -->
2026-10-13 S152：登记文件覆盖分类。research/ 下 127 份登记按覆盖方式分类：校验器直接 92、间接 24、工具产物 5、调查记录 4、共享输入 2；未归类 0。新增活输入须进前两类，工具产物须由已登记工具生成，调查记录须被设计页引用；出现未归类即报错。入口design/11_管理/登记文件覆盖分类.md；运行Validate-RegistryCoverage.py及既有检查。
<!-- REG-COVERAGE-S152:END -->

<!-- PHASE-CLOSE-S160:BEGIN -->
2026-10-13 S160：设计阶段收束核对。现场证据：649篇笔记、两份AGENTS（208规则块）、90校验器/134948项检查、131台本、三张原作参照、声望中英（成对1384、可见中文单列0）、74边闭合、28个GML、.sml与MSL副本同哈希、试点3批/18场景；历史待办共14项；用户已授权当前安装开发测试，0.3.1开发观察已构建部署，实测证据单列，完整扩展尚未验收。入口design/11_管理/设计阶段收束核对.md；运行Validate-PhaseClose.py及既有检查。
<!-- PHASE-CLOSE-S160:END -->

<!-- FIELD-STAGE-S102:BEGIN -->
2026-10-13 S102：特殊地点与野外NPC阶段收口。入口design/11_管理/特殊地点与野外NPC阶段验收记录.md：清点8区域/44地点/13类型、阅读72槽/17组+npc行为槽与场景族结论、28名野外人物（392条含条件回访）、44地点卡、16迹象、12文书、Mod交叉核对与伏笔台账引用组FS-33..36；剩余经济数值、比例与生成点、运行验证、英文稿与逐地点交互脚本。运行Validate-FieldStage.py及既有检查；不部署游戏包。
<!-- FIELD-STAGE-S102:END -->

<!-- IMPL-HANDOFF-S122:BEGIN -->
2026-10-13 S122：实现交接总表。research/impl-handoff.json 列输入清单 18 项、实现顺序 6 步（含每步验收）、不变门槛与尚未确定项；入口design/11_管理/实现交接总表.md；计数取自实时校验报告。不新增设计内容；运行Validate-ImplHandoff.py及既有检查；实现与运行验证仍待进行，不部署游戏包。
<!-- IMPL-HANDOFF-S122:END -->

<!-- QUALITY-GUARDS-S140:BEGIN -->
2026-10-13 S140：质量守卫总表与两项新守卫。链接完整：13548条双链、未解析0（行内代码段除外）；占位扫描：命中5处且全部登记于research/placeholder-allowlist.json；连同S137结构覆盖、S138说话人闭合、S139对白去重共五项守卫。入口design/11_管理/质量守卫总表.md；运行Validate-LinkIntegrity.py与Validate-PlaceholderScan.py及既有检查；不部署游戏包。
<!-- QUALITY-GUARDS-S140:END -->
