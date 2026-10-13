# 动作覆盖清单

## 当前进展（16:54 UTC）

最新已交补绘为16:15 Nell／Sel四张侧背；16人46态PDF／cover内容已通过16:17总览ZIP送达，Nisha／Doro三张职业静态姿态已于16:24交付，无GIF。此前各批送达记录保留。人物仍167；后续按具体缺口追加，不据此宣称全人物全动作完成。按角色可用资料、源包、新姿态与复用数见 [补绘总索引](MASTER_SUPPLEMENT_INDEX.md)。下文早期在制／暂停文字为当时快照，以随后发送记录及总索引为准。后续按具体缺口追加，当前新派工见末尾；自然步行、五个静态门槛及游戏落地仍未完成。

更新：2026-10-13 UTC。统计区分独立姿态、复用阶段和位置/效果采样，不把文件数量当成新增绘制数量。

## 07:52生产恢复历史（当前状态见页首总索引）

- 用户最新指令：“你先继续绘制人物基础动作和人物设定，先不管实际落地”（消息 `Sentinel_c1e6bea529c08191b60f78b312c44031`）。据此恢复基础动作概念与剩余人物设定生产，不以目标版实现契约或本地素材核查为前置。
- 原版部件／帧／遮罩／偏移（part／frame／mask／origin）及合成契约验证，移为 Stoneshard Mod 落地阶段待办；单体型替换部件小样也属于后续落地验证，不能阻塞本轮概念绘制。公开源码的尺寸与姿态数量仍不是目标版冻结规格。
- `archery_v1` 已恢复处理中，尚未完成交付。“仅3张身体原稿、未装备／合成／GIF／独审”的记录是恢复前快照，不再表示当前仍暂停；后续制作、审查与送达分别按实际证据更新。
- 既有作品、历史 QA 与交付事实保留。当前基础动作研究、未来自研完整动作研究与 Stoneshard Mod 的原版必需帧表分开，不将概念完成称作游戏落地通过。
- 人物人数仅按真实制作、审查和送达状态统计，不因恢复派工提前计入完成或交付。下方76／49／1／42／3／1如出现，属恢复前统计快照；新状态以实际队列与交付记录为准。

## 07:44生产门槛历史（概念暂停已由07:52新指令取代）

- 本表记录概念研究与真实交付，不是 Stoneshard 原版必需动作／帧表。既有作品、已交付事实和原 QA 结论全部保留。
- Stoneshard Mod 管线暂停新增整身动作及装备全组合的批量扩画。公开 StoneForge 源码支持预绘部件及必要姿态，并调用原版 `scr_playerSpriteUpdate` 合成角色精灵；见[合成器核实](../../CharacterDesigns/20261013/expressive/reference/STONESHARD_COMPOSITOR_VERIFICATION.md)。
- 当前授权 Mac 未找到原版安装或导出素材，目标 Windows 版本的原版函数体仍未核实；正在等待用户确认素材所在电脑／路径。这里只说明当前可用机器的查找结果，不代表游戏不存在。先核 part／frame／origin／mask 与合成契约，再做一个体型的替换部件小样；公开新版源码的画布尺寸和姿态数量均非目标版冻结规格。
- 下方完整动作与连续性缺口保留为概念研究问题。未来自研游戏若继续完整动作研究，应另定目标与验收，不直接转作 Stoneshard Mod 的扩帧任务。
- `archery_v1` 当前仅3张身体原稿，暂停于此；未制作装备、未合成、未制 GIF、未独审、未交付，不计完成。
- 本轮只调整生产门槛，不新增人物交付；人物统计保持已交76／通过未交49／研究1／暂停42／gate 3／Vian 1。

## 已交付

|角色 / 动作|实际内容|已验范围|仍有限制|
|---|---|---|---|
|齐勒 / 短步研究 walk_v1|3个逻辑阶段，原静站1图＋新绘2姿态|支撑、摆步、落脚的概念表现可辨|不是交替步行循环；W2后足接触未证明，无滑步未验；脸发有轻微漂移|
|齐勒 / 受惊回稳 startle_v1|2个独立主体图、3阶段；R2复用R0|受惊表演、身份与指示棒一致|不是受伤事实、受击技能或死亡动画|
|无身份成年训练样板 / 攻击|4个独立生成身体姿态：准备、抬剑、挥后、回收；geometry版复用1个固定木剑图层|固定剑几何、握点遮挡与透明安全导出通过概念审查|不是无缝循环；步轨连续性未验；剑像素块较粗，身段比齐勒更细长；装备系统未验|
|无身份成年训练样板 / 白闪|1个复用主体、3效果状态；H0=H2，H1=主体＋独立白闪层|分层合成与可见像素核验通过|不是3个新姿态；闪色时长为展示设定，命中事件和引擎参数未验|

|无身份成年训练样板 / 防御与侧撤|4个新身体姿态；两段各3阶段GIF及源包|06:43概念资料已发送|阶段复用不算新绘姿态；循环、动作事件、runtime与装备兼容未验|
|齐勒 / rigid_translation_v1|1个原主体、4个PNG检视位置、13个GIF位置采样、0新增姿态|刚性位移技术独审通过；06:43已发送|足底滑移明确保留，不是自然步态，不授齐勒冲刺技能|

|无身份成年训练样板 / interaction_v1|统一尺度3新身体图、4阶段、5 GIF显示帧|07:00概念资料已发送|显示帧与阶段不等于新增姿态；动作事件、runtime及换装未验|
|无身份成年训练样板 / rest_transition_v1|2新身体图＋复用I0、固定凳层、5阶段；起身反向复用|07:07概念资料已发送|反向复用不新增绘制；自然过渡、碰撞、runtime及换装未验|
|无身份成年训练样板 / shield_guard_v1|2新身体＋1局部手修＋1盾源；4阶段，S3复用S0|固定盾416px／木剑320px几何及遮挡概念QA通过；07:19已发送|局部手修和复用阶段不算新增完整身体；runtime及换装未验|
|无身份成年训练样板 / twohand_staff_v1|3独立身体＋1杖源；4阶段，T3复用T0|固定1000×36px杖／400px握距概念QA通过；07:34已发送|复用阶段不新增绘制；runtime及换装未验|

|无身份成年训练样板 / archery_v1|A0/A1/A2身体阶段，A3复用A0且不补回箭；固定弓与独立弦箭层|08:03三件概念资料已交付，QA记录握弓／箭尾弦中心和分层复合检查|精细钩弦手指及弓材像素统一仍属概念；离画箭是阶段省略，未制作连续飞行；runtime未验|

|无身份成年训练样板 / dialogue_gesture_v1|解释张手、收臂回稳；站姿复用I0|08:11检视板／GIF／源包真实发送，当前独审通过概念带注|无武器无剧情事件；不是对话系统、动作事件或runtime验收|

|无身份成年训练样板 / hit_recovery_v1|轻受击及回稳关键姿态检视、GIF与源包|08:18三件资料真实发送，独审概念通过|不是剧情受伤事实；连续运动、受击事件与runtime未验|

|无身份成年训练样板 / item_offer_v1|2新身体图、3阶段，末帧复用首帧；固定包与手前景遮挡|09:39冻结版本三件真实发送|底层含隐藏原包，非干净原生拆层；稀疏关键姿态概念，不证实收件人接收或runtime|

|Mia / blanket_adjust_v1|2新全身姿态，4阶段；首末复用同一批准站姿|10:11检视板／GIF／最终源包真实发送，独审与冻结hash核实|稀疏关键姿态，非完整动画；无痊愈或额外剧情事实，runtime未验|

|Sela / dialogue_gesture_v1|2新全身对话姿态，4阶段，G首末复用|10:20三件实际发送，FREEZE与独审SHA核实|稀疏关键姿态概念，非完整动画；0新人物，runtime未验|

|Mara／Ivo / dialogue_gesture_v1|各2新全身姿态、各4阶段，首末复用站姿|10:50两检视板／两GIF／联合源包实际发送|表情变化较弱、手势主导；稀疏阶段不是完整动画，runtime未验|

前述受惊、攻击与白闪使用delivery_safe中的透明RGB安全版本。原imagegen结果保留，历史剑长不一致研究明确标历史，不作为当前几何版。

## 当前研究

- 齐勒待机 idle_v1：I0、I1两个不同文件，I2复用I0。微小变化无法形成可读呼吸，作为静站保持/微变化研究，不认定已完成呼吸循环。
- 齐勒交替步行 walk_cycle_v2、v3_rig、v4_guided：停在半步研究，未形成完整循环。生成鞋长变化、固定腿段接缝与细腿问题、两轮局部重绘仍未解决的支撑重心及远腿路径问题均保留。已停止继续扩帧；不以插值或凑齐6张替代验收。
- 已交付的刚性位移仅为平移研究；其送达不改变自然步行v2/v3/v4未形成完整循环的结论。
- archery_v1：08:03已交概念资料（Sentinel_d62690a01e748191bffab034ea593046）；连续动作、离弦后箭轨迹及游戏事件仍未验证，不再列为待交。

## 缺口

1. 可读待机呼吸或其他自然待机循环。
2. 自然、连续、左右交替且循环接缝可接受的步行；稳定鞋形、腿长、支撑重心与逐脚接触轨迹。
3. 攻击脚步与身体连续运动、最终木剑像素画质、动作事件时间线。
4. archery_v1、持盾、双手杖、防御／侧撤、俯身检查及坐起过渡的连续性与游戏事件仍待生产验证。上述概念资料已交付；archery_v1于08:03完成概念送达，不再将制作、独审或发送列为当前未交缺口。
5. 全部动作的原生方向、origin、速度、裁切、碰撞、事件、游戏内播放和完整装备遮挡/换装验证。

1536×1536、root工作点和预览时间均是本轮创作/检视约定，不是从Stoneshard提取的原生参数。官方GIF提供表现参考，不提供这些原创姿态的原帧证明。

## 最新送达记录

2026-10-13 06:43UTC共7件资料真实发送（root确认）：
- 防御／侧撤：Sentinel_da0abbc081c081918157dd62cc51548f。
- 刚性位移：Sentinel_c4dd63312f848191814711f95f1ec148。

文件件数、身体姿态数、阶段数和位置采样数分别统计，不新增人物交付人数。

2026-10-13后续概念交付（root确认）：
- 07:00 interaction_v1：Sentinel_f09276ee107c81918ba7ed68aca9fa0c。3新身体图、4阶段、5 GIF显示帧。
- 07:07 rest_transition_v1：Sentinel_58a82d1d4c5c81919a82c056b2ca7680。2新身体图＋复用I0、固定凳层、5阶段，起身反向复用。
- 07:19 shield_guard_v1：Sentinel_8f64f45c2f408191b642abdf3fb56247。2新身体＋1局部手修＋1盾源；4阶段，S3复用S0；固定盾416px／木剑320px几何遮挡概念QA通过。
- 07:34 twohand_staff_v1：Sentinel_aadb130ec0648191b778b4a7804f63d6。3独立身体＋1杖源；4阶段，T3复用T0；固定1000×36px杖／400px握距概念QA通过。

以上不改变自然步行未闭环与runtime／换装未验的结论。

08:03 archery_v1三件真实发送：Sentinel_d62690a01e748191bffab034ea593046。精确Library IDs与文件SHA见人物roster的action_animation_branch.deliveries；独审位于adult_training_dummy/archery_v1/QA-independent.json。自然步行未闭环结论不变。

08:11对话手势三件已发送：Sentinel_fda6a8f468b48191a8ba42bd88240d2d。精确文件SHA与Library IDs见roster动作交付台账。

08:18轻受击回稳三件已发送：Sentinel_f03b4c4a1e4881919b277257926426bb。准确Library IDs与文件SHA见roster动作台账。

## 08:29新增步行研究

basic_walk_v1独审确认交替不通过：W1支撑侧、W2前后腿遮挡不连续。研究停止；原稿只可参考单姿态，不交动画、无GIF、不计完成。自然步行未闭环结论不变。

09:39递包三件已发送：Sentinel_7ea6d5488bc88191b6826d76f3b68d33。选稿与SHA以adult_training_dummy/item_offer_v1/DELIVERY_FREEZE.json冻结清单为准，已核实际字节；Library IDs存人物roster动作台账与delivery_item_offer_receipt.json。

## 10:10具名人物动作状态（未交付）

- Mia / blanket_adjust_v1：2新全身整理叠毯关键帧已独审通过，QA SHA `4f1a9f459390effc2c5a9c906503cb6464f1baf156f5c5a9ce4bbbc2af8fcf35`已核。最终包已于10:11:45.641250 UTC随检视板／GIF实际发送；见下方送达记录。
- Sela / dialogue_gesture_v1：2新全身对话姿态，4阶段、批准G首末复用，已独审并于10:20:12.611768 UTC交付。路径`sela/dialogue_gesture_v1/`。
- 两项仅概念，0新人物；167已交人物计数不变。

10:11:45.641250 UTC Mia理毯三件已发送：Sentinel_882daa1a058c8191ac6da90eb6516aa8。最终源包CRC及FREEZE全部成员hash已核，精确Library IDs见delivery_mia_blanket_adjust_receipt.json。0新人物，已交167不变。

10:20:12.611768 UTC Sela对话检视／GIF／源包已发送：Sentinel_df28c422812c819194184cc6689ed1b9。三文件冻结SHA、独审SHA与ZIP CRC已核。玛拉与伊沃各3表情已于10:29:55.255824 UTC交付，不新增人物。

## 10:29静态表情与转面范围

玛拉／伊沃6张新胸像静态表情、两检视板及联合ZIP共9件已发送：Sentinel_ea5b67b57f248191b1c3b5d56c4b702d。属于静态表情，不计动画姿态或新人物。两人各侧背turnaround_v1共4新图已独审并于10:41交付；侧面带展示角、背结构为推定。人物仍167已交。

10:41:10.921815 UTC 玛拉／伊沃转面7件已发送：Sentinel_ad62594fbbb081918cb82f1733ea519c。4新视图、0新人物，不是动画。冻结hash、ZIP CRC及所发PNG成员已核。两人dialogue_gesture_v1各2新全身姿态、4阶段首末站姿复用已独审，于10:50交付；已交人数167不变。

10:50:38.373685 UTC 玛拉／伊沃对话5件已发送：Sentinel_1b1099d8d6cc81919effc510927d8408。FREEZE五附件、双独审及ZIP全部成员hash已核。4新姿态、0新人物，167不变。Tor period_costume_v2衣领时代修订在制，未审未交，当前人物选稿不自动替换。


10:56:50.673655 UTC Tor衣装修订三件已发送：Sentinel_d87a6cd0c8588191ac5b0d924c7e28df。当前选稿已按独审切至period_costume_v2透明稿，旧发送历史保留，0新人物。

11:11:49.718551 UTC Tor／Rhea表情9件已发送：Sentinel_ba1bd8b839ac8191be31d6b9ddb4aa77。6新静态胸像、0新人物；九附件及双QA hash、ZIP CRC和八PNG成员hash已核，详见delivery_tor_rhea_expressions_receipt.json。Tor使用新衣装锚。两人turnaround_v1各侧背2图正在制作，尚未独审或交付；人物已交167不变。


11:20:38.905321 UTC Tor／Rhea转面7件已发送：Sentinel_a652563743dc819182ef4e9bea9825ef。4新侧背、0新人物；七附件、双独审hash与ZIP CRC／六PNG成员已核，见delivery_tor_rhea_turnaround_receipt.json。Tor背高+5.69%、非精密正交，Rhea持物背结构推定备注保留。两人dialogue_gesture_v1各2新全身姿态、4阶段正在制作，未审未交；人物已交167不变。


11:28:04.023950 UTC Tor／Rhea对话5件已发送：Sentinel_12191b7615d481919839e44f920d62af。4新姿态、各4展示阶段、首末站姿复用；五冻结附件及双独审hash、ZIP CRC已核。详见delivery_tor_rhea_dialogue_receipt.json。0新人物，167不变，稀疏概念关键姿态。

后续限定范围见人物briefs/next_main_cast_supplements.json：纳拉／灰堤艾娜、妮尔／塞尔各2张story_gesture_v1剧情姿态在制，未独审未交；塞娜／凯姆待排未开画。仅这六人剧情姿态，不自动扩展侧背或胸像；自然步行研究停止结论不变。


11:40:58.467915 UTC Nara／灰堤Ena剧情姿态6件已发送：Sentinel_64da94784fd481919202d3a6d5eb8c13。4新姿态、各4阶段首末锚复用，0新人物，167不变。六冻结附件、双QA及两ZIP全部成员hash/CRC已核，见delivery_nara_ena_story_receipt.json。Nara凳/靴接地点漂移、Ena D2高+5.66%保留备注。

11:41状态：Nell／Sel两份story_gesture_v1实际QA均已落盘通过，准确图稿hash已核，尚未交付；Sena／Kaem已开画在制未审未交。仅限定剧情姿态，不扩展侧背胸像。


11:42:54.815381 UTC Nell／Sel剧情姿态5件已发送：Sentinel_46b882354760819193fc5f807b20eec6。4新姿态，各4阶段、锚首末复用，0新人物；Nell表情差较小，以手势为主。五附件、双QA、联合ZIP全部成员hash及CRC已核，见delivery_nell_sel_story_receipt.json。Sena／Kaem仍在制未审未交，人物已交167不变。


11:47:36.516151 UTC Sena／Kaem剧情姿态5件已发送：Sentinel_5745719924dc81918dcc78c4ae572f3c。4新姿态、各4阶段锚首末复用，0新人物；Kaem第二姿态接近锚，幅度较小如实保留。五附件、双QA及ZIP全部59成员hash/CRC已核，见delivery_sena_kaem_story_receipt.json。

本轮六名既有人物共12新剧情姿态已交齐，人物仍167已交。下一轮brief02为最多4人8姿态规划，尚未派生图，不列在制或通过。


11:51 brief02已派画未审未交：Toman/NPC07与Morlen/NPC-MORREN由draw_toman_morren_story_keyframes制作；Leo/NPC-REY与Lyd/NPC-LYD由draw_rey_lyd_story_keyframes制作，各story_gesture_v1两张新姿态，最多8新图。Lyd新空白双联纸原锚没有，因此原锚仅参考栏，动作使用新1→新2→新1或两帧，禁止纸突然出现的原锚衔接；其余允许4阶段首末锚复用。静态选稿未改，0新人物，167不变。本批之后先核实际缺口，不机械扩展全员。


12:02 brief02四人8新姿态已交齐，0新人物，167不变：
- Leo／Lyd五件12:02:42.959368 UTC发送，Sentinel_0866b1b5118c81918715cf4d12bcf706。Lyd为新1→新2→新1三帧，无纸原锚独立参考；Leo匣厚生成漂移保留备注。
- Toman／Morlen五件12:02:59.696431 UTC发送，Sentinel_0f09c9d4a9cc8191a87778f4056b225f。各4阶段首末锚复用，Toman杖长/握点漂移保留备注。
- 两组附件、四QA与两ZIP全部成员hash/CRC已核，见人物清单delivery_leo_lyd_story_receipt.json及delivery_toman_morlen_story_receipt.json。
- brief03只在核N8/N11等实际缺口，尚未派工，不列生图在制。


12:07 brief03最终派工：draw_oda_rowen_story_keyframes制作Oda/NPC09两姿（4阶段锚首末复用）及Rowen/NPC11一姿（锚→新→锚3阶段），共3新图，在制未审未交。brief SHA b7b93b8c18486253ad327a8ce5f20c64b7744b29326d8c47c25cdb60cfd8d3d5已核。N17 Hers仅源证据核查，未派画；静态选稿及167已交人数不变。


12:08 Hers证据核查后已另派draw_hers_branch_pose_studies，hers/branch_pose_studies_v1在制未审未交：N17-R-defection条件下转身准备逃离、N17-R-shutdown条件下断源后空手戒备，两张条件替代静态姿态。没有GIF或默认先后连播，不表示已逃脱；双手空、钥匙挂腰，不加武器。准确静态锚hash已核；不将N17战术或装置动画记为已覆盖，0新人物，167不变。


12:17:26.707463 UTC Oda／Rowen五件已送：Sentinel_a445795577808191895822ee4ed32e3a。Oda两新姿4阶段，Rowen一新姿3阶段，首末锚复用，共3新姿、0新人物。

12:19:03.252208 UTC Hers四件已送：Sentinel_13295160ef188191bb83ff6f01e93084。两张条件替代静态姿态，无GIF、无默认先后连播；拒绝稿不计。当前已派任务交齐，167已交人物不变；自然步行与五个静态门槛仍未完成，不自动扩产。


12:28 城镇职业动作小批01已派，在制未审未交：Emo衬边检查2姿／4阶段、Geli木票检查1姿／3阶段（draw_emo_geli_work_poses）；Belo箍边检查1姿／3阶段、Kien样品箱换握2姿／4阶段（draw_belo_kien_work_poses）。合4人6新姿计划，原物件连续不新增工具，持物连续性通过才制GIF。brief SHA546964caa17a7907cb658b795b4ea048d64ebd4b4109aa04d641c9ff1ab2813e已核；0新人物，静态167不变。


12:39:41.818571 UTC Emo／Geli职业动作5件已发送：Sentinel_d4feb87f2c648191af95fac3e96bb0e2。Emo两新姿4阶段，Geli一新姿3阶段，首末锚复用。五附件、双QA当前图稿hash及ZIP CRC核实，见delivery_emo_geli_work_receipt.json。0新人物，167不变。12:40实际最新QA：Belo与Kien最后GIF增量均已通过，尚未实际交付。


12:53:27.633149 UTC Belo／Kien职业动作五件已送：Sentinel_34bec6f0ea788191956d731bd5edc4cb。Belo一新姿3阶段，Kien两新姿4阶段；共3新姿、0新人，167不变。Belo仅称检查箍缘，Kien箱尺寸轻漂保留。五附件、双当前QA及50成员ZIP CRC已核，见delivery_belo_kien_work_receipt.json。职业小批01四人六姿已交齐。新sideview_contact_pilot_v1仅S0生成研究，未通过未交付，不解决自然步行缺口。


13:01 sideview_contact_pilot_v1最终为research_only：3/3原稿完成，S0仅历史单姿门槛通过；S1卷翘长靴改变设计、S2腰扣漂至后侧，接触未证明完整周期。最终独审SHA76502bac946e7917777c3e80fc4ef335ce9897edbda028569640b2a23fbb5387已核。原稿与失败检视板保存在项目，不计通过动作套组或新角色，不交GIF／成功包；自然步行仍未完成。


13:20:14.700628 UTC Toman／Leo转面7件已送：Sentinel_d020fe4a7db48191a4a4d026e636fce3。4新静态侧背，0新人物，167不变。七冻结附件、双QA图稿hash及42成员ZIP CRC／六PNG成员hash已核，见delivery_toman_leo_turnaround_receipt.json。背结构推定；旧比例已有背面，本批为当前比例补充。Leo匣厚和固定朝向未冻结，不计方向动画通过。


13:38:27.456012 UTC Nell／Sel表情9件已送：Sentinel_9b17849682148191b14cadcc3db1d777。6新增静态胸像、0新人物，167不变。九冻结附件、双QA及ZIP全部42成员hash/CRC已核，见delivery_nell_sel_expressions_receipt.json。Nell前两张头姿近；Sel第三张为忧虑侧望而非明显低头。原图及manifest未改。


13:58:40.324261 UTC Sena／Kaem表情10件已送：Sentinel_710f22c8e1a48191a236406e2698cd97。6新胸像、0新人，167不变。十冻结附件、当前正式manifest与双QA匹配，两ZIP CRC及所发PNG成员hash已核，见delivery_sena_kaem_expressions_receipt.json。各条件场景非连续悔改／认罪；Sena3柔圆眼、Kaem3不满克制备注保留。不宣称Kaem旧新差集已独立验证，图与manifest未改。


14:17:04.978116 UTC Nara／Ena表情10件已送：Sentinel_ecf023337a40819199609eafe36069b0。6新静态胸像、0新人，167不变。十冻结附件、双QA及两ZIP CRC／所发PNG和QA成员hash已核，见delivery_nara_ena_expressions_receipt.json。Nara2短横气口非纵口，Ena3旧工衣裁切露出／颈巾轻漂；非伤愈或剧情结果。审定图与manifest未改。


14:38:02.350915 UTC Morlen／Leo表情9件已送：Sentinel_185f1eca4a4c819186bb1ab1ebdead79。6新胸像、每人1次修订、8张raw保留；0新人，167不变。九附件、双QA及两ZIP全部成员hash/CRC已核，见delivery_morlen_leo_expressions_receipt.json。保留概念轻漂及条件限制。Lyd／Hers各2胸像已派在制未交，图与manifest未改。


14:48:59.498090 UTC Lyd／Hers表情6件已送：Sentinel_5d0e7f11976481918375f6263f6d9e7d。4新胸像、0修订、0新人，167不变。六附件、双QA及ZIP全部成员hash/CRC已核，见delivery_lyd_hers_expressions_receipt.json。Hers E2短横暗缝，条件非连续剧情。审定图与manifest未改。


16:15:00.827503 UTC Nell／Sel转面6件首次实际已送：Sentinel_7fdfdd0b9df081918ab674ab463cfbf0。4新静态侧背、0新人，167不变。六附件、双QA及ZIP CRC／所发PNG与QA成员hash已核。Sel唯一侧视修订，背结构推定，各图等比fit并非共同倍率。总览PDF／cover截至16:14无Library条目，不记已交；Nisha／Doro职业3姿已派在制，见town_work_pose_candidates_02.json。


16:17:10.063714 UTC 表情总览ZIP已实际送达：Sentinel_61c2e445b9448191950a7223dd758792，Library libfile_36645437938881919a53b3862fe382bc。5页16人46态，五成员均匹配本地原文件，ZIP SHA及CRC已核；PDF原字节不变。单独PDF／cover上传状态不确定，但内容ZIP交付已闭环，无需盲查或重复create。0新图、0新人，167不变。


16:24:07.591490 UTC Nisha／Doro职业静态姿态6件已送：Sentinel_f651f9db0ba0819181f91b6beedfafd7。3新姿、0修订、0新人，无GIF，167不变。六冻结附件、双QA及ZIP CRC／所发PNG和QA成员hash已核，见delivery_nisha_doro_work_receipt.json。书宽厚／碗椭圆轻漂保留，非物件精确冻结或剧情结果。审定文件未改。


16:37:17.013899 UTC Osin／Vasen五件已送：Sentinel_f3a8dbf69cd081919d8caf88936c6ae5。2新静态、0新人、无GIF，167不变。五附件、双QA及ZIP CRC／所发PNG和QA成员hash已核，见delivery_osin_vasen_work_receipt.json。Osin同倍率占高约+8%；Vasen同动作左右手对调合理，修订未选不计第二姿。审定图和manifest未改。下一dummy单膝短歇仅brief准备，未派图。


16:46:03.600099 UTC dummy单膝静态三件已送：Sentinel_508b5bcc837c8191ab0c16684005d513。1新图、0新人，无GIF，I0/I2/R2仅复用参考。三附件、独审及ZIP全部24成员hash/CRC已核，见delivery_dummy_single_knee_rest_receipt.json。头帽−6.1%及后踝遮挡限度保留，未证明骨长或完整动画。167人不变，审定文件未改。


16:54:55.373208 UTC dummy侧卧R1三件已送：Sentinel_52987ee43bdc819182dc692d1695f5bc。1新静态、0新人、无GIF，167不变。三附件、独审及ZIP全部成员hash/CRC已核，见delivery_dummy_reclined_rest_receipt.json。远靴遮挡不证骨长／鞋形完整追踪；掌侧折臂托头是前臂平枕的等价构图，保留差异限制。审定payload未改。
