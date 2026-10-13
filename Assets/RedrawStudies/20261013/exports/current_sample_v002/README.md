# 当前像素重绘导出小样

仅稳定可审阅候选：9个人物、2个主道具；稳定不是最终风格或生产批准。

原尺寸见native/；1x/8x预览仅用于审阅，不计新美术。坐姿与道具单列。可见脚底/画布不是引擎origin。

本包不是完整离线重绘流程，不含作者脚本、全部源输入及外部生成输入，也不是游戏mod。完整制作源、日志与历史版本仍在项目。无旧失败版本，仅收录已完成独立候选审查的齐勒v2/洛妲v2，洛妲小锤保留原尺寸识别限制，无商业原版PNG或原版对照图片。

current_candidates.json记录精确来源、SHA、测量、比例和QA范围；sample_native_path是包内相对路径，repository_path/native_path是原项目定位，不保证包内存在。SOURCES.json列原版参考来源、版权与用途；independent_qa/为独立报告或修订跟进段的来源标注副本，临时绝对路径省略。审核证据只证明所述范围，所有候选style/production/runtime均未批准。

FILE_MANIFEST.json含其余每一文件的SHA256与CRC32，不自引用；外部ZIP验证报告另含归档哈希、CRC全检与源native逐字节核对。

- 瑟拉 (BRY-NPC-SELA): native/sela/sela_structural_idle_view01_f000.png
  17:17；深色颏边计入则18:16。近1:1结构通过，风格未验收。
- 安菈 (BRY-NPC-ANLA): native/anla/anla_native_1to1.png
  17:17；深色颏边计入则18:16。仅近1:1结构通过。
- 莉葵 (TRADE-NPC-LIQUI): native/liqui/liqui_native_1to1.png
  主要颏端17:17，保守16:18；近1:1结构支持，脸型/色相/正面感仍待风格审查。
- 莫伦·海 (NPC12 / NPC-MORREN): native/morlen/morlen_native_v1.png
  胡须/围巾遮颏；推定14:20至16:18，精确解剖比例未证。不自动放大。
- 赫斯·白 (NPC10 / NPC-HERS): native/hers/hers_native_v2.png
  短须/颏/领口边界不明；推定14:20至16:18，边界性候选，非精确1:1。
- 哈塞 (BRY-NPC-HASE): native/hase/hase_native_v1_1.png
  胡须下颏推定y19–20：16:18至17:17；有条件近1:1，不认证精确解剖。
- 齐勒 (ALD-NPC-CHILER): native/chiler/chiler_native_v2.png
  可见肤颏y20、冠4、足37支持17:17；v2两处发孔修补经独立差分复核；1x小胡须仍不清。
- 洛妲 (BRY-NPC-LODA): native/loda/loda_native_v2.png
  可见肤颏y20、冠4、足37支持17:17；单绳环清楚；v2局部工具修订将锤头与手分开，1x具体种类仍受原尺寸限制。
- 雅尼 (BRY-NPC-YANI): native/yani/native.png
  坐姿独立审查；不可套站姿17+17，胡须遮颏，缺少同姿原版参照。
- 布盖桶 (prop): native/cloth_barrel/candidate_water_container_native.png
  道具不适用头身比；布木箍区分候选通过，真实场景暗轮廓待核。
- 白带系泊桩 (prop): native/whiteband_mooring_post/native_32x48.png
  道具不适用头身比；42px可见高须真实岸边尺度/遮挡复核，非已定矮系泊桩。
