# 头像重绘第十九批：四人候选交付

日期：2026-10-15。四人均选择独立 QA 冻结的 v2：辛娅 XINYA（PAS-S01-NPC）、乌珀 WUPO（PAS-S02-NPC）、碧珞 BILUO（KOR-NPC-BILUO）、埃文·行 EVAN（KOR-NPC-EV）。身份以本批保存的当前人物卡和剧情快照为准。

## 文件与状态

交付七件：中文手机纵向总览一张（680×2184，74×100 原尺寸与4倍最近邻展示）、四张独立74×100透明PNG、两份各小于18MiB的普通源码ZIP。

- A_XINYA_WUPO：辛娅、乌珀完整制作目录。
- B_BILUO_EVAN：碧珞、埃文·行完整制作目录。
- 两个ZIP都带本批独立QA交付证据、交付总览、四张selected PNG、来源校验、交付冻结记录与便携复现脚本。

四人均为“带残留问题的生成/量化肖像候选”。本批无held。每人两份实际生图，v1未选与v2选中版本均原样保留。碧珞另有一次六参考图参数校验拒绝记录，该次没有生成图片，拒绝请求与回包均保留；成功成图仍为两份。交付阶段不重新生成、不补画、不修改角色源文件。

## 必须保留的限制

原始生图是高分辨率透明图。74×100候选由全画布同比例最近邻采样、alpha≥128二值化、无抖动调色板量化派生。它们不是原生74×100逐像素手工终稿，不代表用户美术终审、游戏集成或实机验收。32色是本轮临时技术上限，不是原作实测调色板规范。

- 辛娅：四十多岁量粮人，后梳高额、厚低眉宽钝鼻、赭衣棕围裙保留；v2缩短裸颈、提高领口肩线。仍有谨慎忧意，右眼白略亮。
- 乌珀：五十岁上下旁路石匠，宽额、粗灰眉、厚灰短须与褪棕系带衣旧围裙保留；v2压暗眼白、合并发须色块。低睑疲态仍强，局部颊纹细碎。
- 碧珞：三十多岁本案寄售人，长直鼻、宽颧菱下颌、后束波发、酒红衣灰披肩保留；v2短颈、半开短嘴更坦然。眼白仍偏亮，脸旁有一小段松散波发，但没有退回旧初稿整体近似脸。
- 埃文·行：三十多岁旅人，现行人物卡的低檐帽、早白鬓角优先于旧裸头母图；保留长略弯鼻、长方胡须、苔披风赭衣。仍带谨慎疲态，局部胡须色纹略碎。当前人物卡与历史母图的外观更新已有记录，不混作身份冲突。

四张选中v2的原始raw均无alpha≥128实色触边；发耳及帽形完整，留边来自真实源图余量。本批没有用padding或inset补回缺失内容，所有候选均使用74×100全画布fit。

## 源码追溯

每名角色目录内保留原始raw、完整工具回包（含原始base64）、完整提示词和参数、当前人物卡快照、身份母版、生成风格参考、剧情来源快照和SHA、未选v1、选中v2、预览、原始派生脚本、作者自检和清单。独立QA为independent_qa/batch19，冻结入口是freeze_manifest.json；交付以独立冻结而非仅作者自选为准。

未打包商业原作像素参考图或sprite图集。DELIVERY_EXCLUSIONS.json记录参考路径/SHA及不含像素声明；生成身份参考和已生成风格候选保留。原始记录中可能存在绝对路径，这是忠实的历史工具参数；便携复现使用包内相对路径，不需要那些工作区路径。

独立QA共97个文件，96条原始SHA256SUMS已完整核对；每个包保留其中81个文件，只省略16份完全重复的审计复跑raw与工具回包副本，未省略对应角色制作目录中的原始文件。省略项逐个列入freeze_gate.json与DELIVERY_EXCLUSIONS.json。原始QA的SHA256SUMS忠实保留，所以其中16条指向这些被省略的重复文件；解包校验应以本包PACKAGE_SHA256SUMS.txt和package_inventory.json为完整范围。QA复跑脚本、候选、预览、metrics与全部报告仍保留。

## 校验与复现

环境：Python 3.12.14、Pillow 12.3.0。图像派生使用确定性算法，无生图服务调用，无网络请求。四人所有历史候选均使用74×100全画布Pillow NEAREST整数尺寸同比例contain及MAXCOVERAGE量化，alpha阈值128、无抖动、透明像素归零。

1. 校验某ZIP：python verify_source_package.py batch19_source_A_XINYA_WUPO.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须不存在；脚本只写新输出，不改包内冻结文件。A、B分别复现所属两名角色的v1与v2，合计8张。
4. 脚本逐张比较RGBA像素及PNG完整字节与SHA；成功输出all_pass=true。
5. PACKAGE_SHA256SUMS.txt与package_inventory.json覆盖全部实质成员，校验清单自身由最终ZIP SHA锚定；verify_source_package.py检查全ZIP CRC、每成员SHA、大小、成员集合、重复路径与路径穿越。

交付前核对48项原源与快照、181个角色冻结文件、8份raw与完整回包字节，检查8份提示词文本与实参及所有参考输入。两个ZIP均实际解压，再由解压目录独立复现全部8张历史候选。手机总览与四张独立PNG实际查看，总览1x和4x区域验证来自完整selected原像素。各结论详见portable_reproduction_verification.json、production_source_verification.json、delivery_visual_QA.json及独立QA报告。

未改旧资产、人物卡或Mod代码；未commit/push；未集成或启动游戏。包内build_delivery.py和package_sources.py用于原仓库排版打包，依赖原仓库目录；面向独立解包使用的脚本为verify_source_package.py和reproduce_candidates.py。
