# 头像重绘第二十一批：四人候选交付

日期：2026-10-15。终选严格采用独立 QA 冻结：塔斐 TAFEI（KOR-NPC-TAFEI）v2_inset、榭兰 XIELAN（KOR-NPC-XIELAN）v2、尤恩 YUEN（KOR-NPC-YUEN）v2_inset、阿霖 ARLIN（KOR-S01-NPC）v2_inset。身份以本批保存的当前人物卡和剧情快照为准。

## 文件与状态

交付七件：中文手机纵向总览一张（680×2184，74×100 原尺寸与4倍最近邻展示）、四张独立74×100透明PNG、两份各小于18MiB的普通源码ZIP。

- A_TAFEI_XIELAN：塔斐、榭兰完整制作目录。
- B_YUEN_ARLIN：尤恩、阿霖完整制作目录。
- 两个ZIP都带本批独立QA交付证据、交付总览、四张selected PNG、来源校验、交付冻结记录与便携复现脚本。

四人均为带残留问题的NN技术派生候选。本批无held。每人两份实际生图，合计8份；所有v1、v2与技术inset候选均保留，共11张。每人另有一次六参考图参数校验拒绝记录，该次没有生成图片；拒绝请求和回包保留，成功成图数仍为两份。交付阶段不重新生成、不补画、不修改角色源文件。

## 必须保留的限制

原始生图是高分辨率透明图。74×100候选由全画布同比例最近邻采样、alpha≥128二值化、无抖动MAXCOVERAGE调色板量化派生。full导出使用74×100 fit，inset导出使用72×98 fit后居中放入74×100画布；inset沿用同一raw，不是额外生图，也不是缺失内容补绘。它们不是原生74×100逐像素手工终稿，不代表用户美术终审、游戏集成或实机验收。32色是本轮临时技术上限，不是原作实测调色板规范。

- 塔斐：四十多岁，现卡低帽檐与早白鬓角优先旧裸头棕鬓母图；保留宽颊圆鼻、浅棕八字胡清下巴、褪蓝行脚衣灰披边与担忧解释。原raw右侧仅1源像素透明留边，余量极紧；full NN候选采样到右画框。所选72×98 containment仅是技术导出留边，不能声称修复源图裁切。发须和帽褶仍有平行条带；小眼白残余偏亮。
- 榭兰：约50岁男性购画人，长窄脸、直鼻、灰短胡、深蓝衣与窄朴素棕披边，审慎侧目。灰发短胡仍有重复条带、细碎像素；表情仍略严肃；底部只1候选像素透明留边，构图余量偏紧。
- 尤恩：约60岁，全白发、旧式长褂、窄围巾与旧徽遵循当前卡；保留低睑、下垂长鼻和犹疑难过。额眉皱纹线仍稍多，白发有少量连续条带，眼白保留小亮块。原raw右侧余量15源像素，selected inset提供更稳候选留边，不是源图修复。
- 阿霖：四十多岁修门人，左眉旧伤疤遵循当前卡，保留深褐发须、粗眉宽脸与木工衣边。小眼白仍比四核心略亮；深发仍为条状大分组，少量暗色合并仍存在。full版本把部分褐发胡须合成橄榄调，selected inset已明显减轻；32色压缩的细微色差损失保留为限制。

四份选中候选对应的v2 raw均无alpha≥128实色触边；这不抹去塔斐极紧的真实边界，也不把技术padding当成源图修复。源边界特写与独立审计均随包提供。

## 源码追溯

每名角色目录内保留原始raw、完整工具回包（含原始base64）、完整提示词和实际参数、当前人物卡快照、身份母版、生成风格参考、剧情来源快照和SHA、所有未选历史版与技术派生、整数预览、原始派生脚本、作者自检和清单。独立QA为independent_qa/batch21，冻结入口是freeze_manifest.json；交付以独立冻结而非仅作者自选为准。

未打包商业原作像素参考图或sprite图集。DELIVERY_EXCLUSIONS.json记录参考路径/SHA及不含像素声明；生成身份参考和已生成风格候选保留。原始记录中的绝对路径是忠实的历史工具参数；便携复现使用包内相对路径，不需要那些工作区路径。

独立QA共148个文件，147条原始SHA256SUMS完整核对；每个包保留其中132个文件，只省略16份完全重复的审计复跑raw与工具回包副本。对应角色制作目录中的原始文件没有省略。省略项逐个列入freeze_gate.json与DELIVERY_EXCLUSIONS.json，包含原QA路径、字节数、SHA、保留的制作路径与所属A/B包。原始QA的SHA256SUMS忠实保留，其中16条指向这些省略副本；完整解包校验以本包PACKAGE_SHA256SUMS.txt和package_inventory.json为准。QA复跑脚本、候选、预览、metrics与全部报告仍保留。

## 校验与复现

环境：Python 3.12.14、Pillow 12.3.0。图像派生使用确定性算法，无生图服务调用，无网络请求。所有候选使用Pillow NEAREST同比例contain、整数尺寸四舍五入、MAXCOVERAGE 32色量化、alpha阈值128、无抖动与透明RGB归零。

1. 校验某ZIP：python verify_source_package.py batch21_source_A_TAFEI_XIELAN.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须不存在；脚本只写新输出，不改包内冻结文件。A复现塔斐3张和榭兰2张，B复现尤恩3张和阿霖3张，合计11张。
4. 脚本逐张解码完整回包与raw比较，独立复现候选并比较RGBA像素、PNG完整字节与SHA；成功输出all_pass=true。
5. PACKAGE_SHA256SUMS.txt与package_inventory.json覆盖全部实质成员，校验清单自身由最终ZIP SHA锚定；verify_source_package.py检查全ZIP CRC、每成员SHA、大小、成员集合、重复路径与路径穿越。

交付前核对46项原源与快照、202个角色冻结文件、8份raw与完整回包字节，检查8份成功提示词文本与实参及参考输入。两个ZIP实际解压，再由解压目录独立复现全部11张历史候选。手机总览与四张独立PNG实际查看，总览1x和4x区域验证来自完整selected原像素。结论详见portable_reproduction_verification.json、production_source_verification.json、delivery_visual_QA.json及独立QA报告。

未改旧资产、人物卡或Mod代码；未commit/push；未集成或启动游戏。包内verify_freeze.py、build_delivery.py和package_sources.py用于原仓库核验、排版与打包，依赖原仓库目录；面向独立解包使用的是verify_source_package.py和reproduce_candidates.py。
