# 当前像素候选入口

本目录仅选择当前可审阅的原尺寸单帧，不表示最终美术、完整动画或游戏运行通过。原概念299张另存在 `src/EmbersAndOaths/Assets/ConceptDrafts/20261012`，不与本轮候选混计。


## 选择规则

只采用下列明确路径与SHA；独立QA必须与该图哈希匹配。文件出现、作者自检、旧版QA或较大的版本号都不能单独判完成。齐勒v2、洛妲v2已取得作者完成结果与独立QA后收录；保留原尺寸工具读形限制。

可见脚底行只是图片坐标，不是已证引擎origin。头身取可见颏界及容差，胡须下为区间；坐姿独立。追踪9个人物：8个仍为已审研究候选，瑟拉1个进入审美重设；另2个主道具。全部仍待最终风格、动画、场景与运行验收。

### 瑟拉 · sela — 审美重设中，暂无通过的当前native候选
- 身份：BRY-NPC-SELA。
- 最新状态：用户明确C仍丑，要求表情/情绪。C审美未获认可，不再标“待确认”或“当前主审推荐”；原独立QA的局部五官改善结论仅作历史技术证据，不能替代用户审美。
- 当前讨论方向：[G内置生成raw表情概念](sela_proportions/facial_refinement/redesign_G/sela_G_raw_imagegen.png)；[G制作说明](sela_proportions/facial_refinement/redesign_G/README.md)。raw SHA256：`c61337a497f4a6e6cdccb8d1cee8b8a49dba7aa9cfc13057678bce7e9fbc026a`。
- G raw正在准备交用户看表情概念方向；不是native像素成品、未获用户认可、未生产或运行验证。更有表情不等于风格或游戏通过。
- D/E/F手修未过内部审美，仅保留实验。G17px原生化/修整稿与70×88二倍工程稿均不列通过候选；尺寸、头身或颜色统计不是审美验收。
- C历史native仍在[sela_proportions/facial_refinement/c_reorganized/sela_face_C_native.png](sela_proportions/facial_refinement/c_reorganized/sela_face_C_native.png)，SHA `7176706fe53403dad1f8df41fc3da4c19488076380d06b2947d569620d6b39e2`；原冠4/肤颏20/足37及17:17证据保留，已不代表当前选稿。
- C来源仍见manifest-C.json及QA-independent-C.json；前17:17、A/B/C/D/E/F及G工程稿均保留，不覆盖。冻结v002仍含更早17:17稿，本次未改包或导新ZIP。

### 安菈 · anla
- 身份：BRY-NPC-ANLA
- 当前native：[anla/revision_1to1/anla_native_1to1.png](anla/revision_1to1/anla_native_1to1.png)
- SHA256：`e463e7ed23691e0d244930d35a16b3d98eeabe45fff9979bd6a9f36196012b73`
- 画布 [35, 44]；可见RGB色 15；不透明底行 y=37；bbox [8, 4, 28, 38]（右下半开）。
- 比例/QA：17:17；深色颏边计入则18:16。仅近1:1结构通过。
- 独立证据：`Assets/ReferenceAudit/20261013/remaining_head_body_ratio_review.json` / anla_revision_followup
- 防误用：anla_native_v1/v2/v3均为历史，v3不是当前头身版。

### 莉葵 · liqui
- 身份：TRADE-NPC-LIQUI
- 当前native：[liqui/revision_1to1/liqui_native_1to1.png](liqui/revision_1to1/liqui_native_1to1.png)
- SHA256：`c15f2d8995f2c0177a83b2130b92ab39fcf4ba074f37bcf855248956672fe72d`
- 画布 [35, 44]；可见RGB色 17；不透明底行 y=37；bbox [9, 4, 28, 38]（右下半开）。
- 比例/QA：主要颏端17:17，保守16:18；近1:1结构支持，脸型/色相/正面感仍待风格审查。
- 独立证据：`Assets/ReferenceAudit/20261013/remaining_head_body_ratio_review.json` / liqui_revision_followup
- 防误用：liqui_native_v1与v2/liqui_native_v2均非当前；不引用v2旧13:21作为现图比例。

### 莫伦·海 · morlen
- 身份：NPC12 / NPC-MORREN
- 当前native：[morlen/morlen_native_v1.png](morlen/morlen_native_v1.png)
- SHA256：`c0258a3839fe8ee95b0ec29d5a4f65c14711592f40f3b3493e40ac9546a41289`
- 画布 [35, 44]；可见RGB色 20；不透明底行 y=37；bbox [7, 4, 27, 38]（右下半开）。
- 比例/QA：胡须/围巾遮颏；推定14:20至16:18，精确解剖比例未证。不自动放大。
- 独立证据：`Assets/RedrawStudies/20261013/morlen/QA-independent.json`
- 防误用：structural_baseline与concept均不是当前native。

### 赫斯·白 · hers
- 身份：NPC10 / NPC-HERS
- 当前native：[hers/v2/hers_native_v2.png](hers/v2/hers_native_v2.png)
- SHA256：`0c8342b3dc02c4628ddbd5c7ccf29ae99cda310a1689d9c79408a7fd736a30ac`
- 画布 [35, 44]；可见RGB色 19；不透明底行 y=37；bbox [8, 4, 28, 38]（右下半开）。
- 比例/QA：短须/颏/领口边界不明；推定14:20至16:18，边界性候选，非精确1:1。
- 独立证据：`Assets/RedrawStudies/20261013/hers/v2/QA-independent.json`
- 防误用：hers_native_v1与preedit为历史；ledger是独立道具，不表示人物随身持账。

### 哈塞 · hase
- 身份：BRY-NPC-HASE
- 当前native：[hase/v1_1/hase_native_v1_1.png](hase/v1_1/hase_native_v1_1.png)
- SHA256：`614c628c28bcc78c588ee83e46a23a4e84559a057f39d6da7be2956b989803da`
- 画布 [35, 44]；可见RGB色 19；不透明底行 y=37；bbox [7, 4, 30, 38]（右下半开）。
- 比例/QA：胡须下颏推定y19–20：16:18至17:17；有条件近1:1，不认证精确解剖。
- 独立证据：`Assets/RedrawStudies/20261013/hase/v1_1/QA-independent.json`
- 防误用：native_base/nearest_base与concept_v1_unapproved不是完成native；v1额部孤立绿像素已在v1_1单像素修正；脸部对称性仍待艺术审查。

### 齐勒 · chiler
- 身份：ALD-NPC-CHILER
- 当前native：[chiler/chiler_native_v2.png](chiler/chiler_native_v2.png)
- SHA256：`6720bc83510e52d38629e5f09e67ce7c53d88fa11a533a9a404a63f97a4739e1`
- 画布 [35, 44]；可见RGB色 20；不透明底行 y=37；bbox [5, 4, 26, 38]（右下半开）。
- 比例/QA：可见肤颏y20、冠4、足37支持17:17；v2两处发孔修补经独立差分复核；1x小胡须仍不清。
- 独立证据：`Assets/RedrawStudies/20261013/chiler/QA-independent-v2.json`
- 防误用：v1、native_base与结构concept非当前；独立v1视觉证据加v2差分复核，不宣称额外视觉检查。

### 洛妲 · loda
- 身份：BRY-NPC-LODA
- 当前native：[loda/v2/loda_native_v2.png](loda/v2/loda_native_v2.png)
- SHA256：`0d1feb920af7ed8d225c7cf07dbceeef8eae615f91ab035e54529a992357c6b7`
- 画布 [35, 44]；可见RGB色 20；不透明底行 y=37；bbox [5, 4, 29, 38]（右下半开）。
- 比例/QA：可见肤颏y20、冠4、足37支持17:17；单绳环清楚；v2局部工具修订将锤头与手分开，1x具体种类仍受原尺寸限制。
- 独立证据：`Assets/RedrawStudies/20261013/loda/v2/QA-independent.json`
- 防误用：old_normalized只作旧稿比较，不是native。洛妲v1保留历史；v2仅工具/原遮挡手肤色局部修订，不宣称最终风格通过。

### 雅尼 · yani
- 身份：BRY-NPC-YANI
- 当前native：[yani_seated/style_reset/native.png](yani_seated/style_reset/native.png)
- SHA256：`a558c5c2a6b28ac4e902425a1b2da894065000ccd8c07321bbc7fc74f5b344a4`
- 画布 [35, 44]；可见RGB色 18；不透明底行 y=37；bbox [7, 9, 28, 38]（右下半开）。
- 比例/QA：坐姿独立审查；不可套站姿17+17，胡须遮颏，缺少同姿原版参照。
- 独立证据：`Assets/RedrawStudies/20261013/yani_seated/style_reset/QA-independent.json`
- 防误用：yani_seated根目录与v2均为历史，不误选较旧坐姿。

### 布盖桶 · cloth_barrel
- 身份：原创道具，无角色ID
- 当前native：[cloth_barrel/v2/candidate_water_container_native.png](cloth_barrel/v2/candidate_water_container_native.png)
- SHA256：`e0872127fcb256463f1e0a78e9911f6599549ed5368b99022a236561ccdd80d7`
- 画布 [32, 32]；可见RGB色 17；不透明底行 y=28；bbox [3, 3, 30, 29]（右下半开）。
- 比例/QA：道具不适用头身比；布木箍区分候选通过，真实场景暗轮廓待核。
- 独立证据：`Assets/RedrawStudies/20261013/cloth_barrel/v2/QA-independent.json`
- 防误用：cloth_barrel根目录v1、initial_quantized及concept不是当前。

### 白带系泊桩 · whiteband_mooring_post
- 身份：原创道具，无角色ID
- 当前native：[whiteband_mooring_post/native_32x48.png](whiteband_mooring_post/native_32x48.png)
- SHA256：`7db3957918dc0cba6ef32601d825f00e21b281bd2db8f774cb1a52c461dcaf58`
- 画布 [32, 48]；可见RGB色 13；不透明底行 y=44；bbox [7, 3, 24, 45]（右下半开）。
- 比例/QA：道具不适用头身比；42px可见高须真实岸边尺度/遮挡复核，非已定矮系泊桩。
- 独立证据：`Assets/RedrawStudies/20261013/whiteband_mooring_post/QA-independent.json`
- 防误用：native_before_edits与concept不是当前；无同物原版匹配。

## 已收录但未决
- 瑟拉：C审美未获用户认可，G表情概念方向准备交用户看；没有新通过的native。
- 洛妲v2：工具局部修订，1x具体器具识别仍受原尺寸限制。
- 所有角色：只有单帧研究候选，最终风格、多方向/动画与游戏运行均未验收。

## 冻结审阅小样（不等于实时当前入口）
- 已冻结历史导出：[current_sample_v002](exports/current_sample_v002/README.md)；[ZIP](exports/current_sample_v002.zip)。历史导出不覆盖。
- v002的1×/8×同地面预览按站姿、坐姿、道具分开；展示冻结时的候选，未包含后续瑟拉C/G；C已未获用户审美认可，G仅概念，不嵌入商业原版。预览是审阅辅助，新增美术计数0。
- 本次仅更新目录入口与来源/状态，不改冻结v002 ZIP或目录、不导新ZIP、不上传。瑟拉已进入G表情概念重设；上方G raw仅讨论方向，不能当native成品。
- 原版来源及用途见小样SOURCES.json；原图不入包。
- Hers独立账簿v2不在本次十一候选清单，仍保存在hers/v2；不当人物随身物或新人物计数。
- 导出小样不含作者脚本/全部输入，不是完整离线重绘流程，也不是可安装游戏mod。全流程仍保存在项目。
- 导出文件逐项SHA256及CRC32见FILE_MANIFEST.json，ZIP与源图核对见exports下同名验证报告。
