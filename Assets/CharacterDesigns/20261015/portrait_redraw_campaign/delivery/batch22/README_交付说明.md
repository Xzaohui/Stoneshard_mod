# 头像重绘第二十二批：四人候选交付

日期：2026-10-15。四人均选择独立 QA 冻结的 v2：玛迪 MADI（KOR-S02-NPC）、博赫·冷 BOH（SKO-NPC-BOH）、古烈 GOREN（SKO-NPC-GOREN）、妮莎·炉 NISHA（SKO-NPC-NIS）。身份以本批保存的当前人物卡和剧情快照为准。

## 文件与状态

交付七件：中文手机纵向总览一张（680×2184，74×100原尺寸与4倍最近邻展示）、四张独立74×100透明PNG、两份各小于18MiB的普通源码ZIP。

- A_MADI_BOH：玛迪、博赫·冷完整制作目录。
- B_GOREN_NISHA：古烈、妮莎·炉完整制作目录。
- 两个ZIP均带完整独立QA交付证据（仅映射省略重复replay输入）、交付总览、四张selected PNG、来源校验、冻结记录及便携复现脚本。

四人均为“带残留问题的生成/量化肖像候选”，本批无held。每人两份实际生图，未选v1与选中v2均原样保留。古烈另有一次六参考图参数预检拒绝，该次未生成图片，请求与错误回包保留，不计第三份生图。交付阶段不重新生成、不补画、不修改角色源文件。

## 必须保留的限制

原始生图为高分辨率透明图。74×100候选由整画布同比例最近邻采样、alpha≥128二值化、无抖动MAXCOVERAGE量化派生。它们不是原生74×100逐像素手工终稿，不代表用户美术终审、游戏集成或实机验收。32色为临时技术上限，不是原作实测调色板规范。

- 玛迪：约五十岁女性守灯人，成熟窄脸、大长鼻、下睑口周纹、灰缕深发浅米巾、深罩衣暗锈衣保留。v2缩短露颈、窄领贴下颌；仍有眼内小亮簇、头巾占幅大，raw真实左右余量仅9/7px。
- 博赫·冷：三十多岁瘦男性归乡工匠，暗棕短胡发、灰蓝新工装与棕背心，自持警觉。新衣设定优先旧补丁背心，不是妮莎弟弟；赎回不代表家族所有。v2短颈V领贴下颌，仍有眼内小亮簇、细碎头发，候选底部13px空白偏多，未擅自裁切放大。
- 古烈：三十多岁男性炭工，使用rework_v2身份母图，厚下颌宽鼻、棕短胡发与炭灰窄领，与博赫瘦脸可分。护符可在本头像画幅外，不新增魔法或护理改信含义。v2眼缩为小横向侧目、短颈窄领；仍有浅眼簇、碎发胡与偏大发冠，raw右侧真实余量9px。
- 妮莎·炉：四十多岁女性会计，眼下伏案红痕/口周纹、棕发锈红巾、深罩衣窄领与少量暗绿肩边。保留焦虑愧疚和分栏原则，不表示弟弟已归。v2短颈窄领且发巾轮廓真实内收；眼白仍明显偏亮，比本批另三张更显眼，不代表小暗眼风格完全验收。发巾占幅大，raw右侧18px余量较窄，候选顶空13px/底空8px使有效占高较少。

四张选中v2原始raw的alpha≥5实色均不触边，发巾耳轮廓完整。玛迪/博赫的v1与v2使用72×98 fit box后居中于74×100，是完整画布技术inset，不能恢复任何被裁内容。古烈/妮莎两版使用74×100全画布fit。妮莎v1贴框风险由v2真实重画内收解决，未用padding掩盖源裁边。

## 源码追溯

每人制作目录保留原始raw、完整工具返回（含原始base64）、完整提示词及实参、当前人物卡快照、身份母版、生成风格参考、剧情来源快照及SHA、未选v1、选中v2、预览、原始派生脚本、作者自检与完整清单。独立QA在independent_qa/batch22，其唯一冻结选图入口为FINAL_SELECTION.json，另有FINAL_REVIEW.md、DELIVERY_CHECKLIST.json、final_technical_audit.json和frozen_verification.json。以独立冻结而非仅作者自选为准。

未打包商业原作像素参考图或sprite图集。DELIVERY_EXCLUSIONS.json保存参考路径、SHA和不含像素声明；生成身份参考及生成风格候选保留。原始工具记录中的绝对路径忠实保留，便携复现使用包内相对路径，不依赖那些旧工作区路径。

独立QA共153文件，152条原始SHA256SUMS.txt完整核对；每个包保留其中137文件，仅省略16份完全重复的审计replay raw/工具回包副本，对应原始文件仍完整保留于角色制作目录。每一省略项均在freeze_gate.json和DELIVERY_EXCLUSIONS.json记录源路径、SHA、保留目标与所属包。原始QA的SHA256SUMS.txt、QA_FILE_INVENTORY.json忠实保留，因此含有指向省略副本的条目；解包完整范围应以PACKAGE_SHA256SUMS.txt和package_inventory.json为准。QA的全部脚本、候选、预览、metrics和报告仍保留。

## 校验与复现

环境：Python 3.12.14、Pillow 12.3.0。图像派生为确定性算法，无生图服务调用、无网络请求。Pillow NEAREST对整画布等比contain并取整输出尺寸，alpha阈值128、MAXCOVERAGE≤32色、无抖动、透明RGB归零；fit box按上文分别为72×98或74×100。

1. 校验某ZIP：python verify_source_package.py batch22_source_A_MADI_BOH.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在；脚本只写新输出，不改包内冻结文件。A、B分别复现所属两人的v1与v2，合计8张历史候选。
4. 脚本逐张比较RGBA像素、PNG完整字节和SHA；成功输出all_pass=true。
5. PACKAGE_SHA256SUMS.txt与package_inventory.json覆盖全部实质成员；清单自身由最终ZIP SHA锚定。verify_source_package.py检查全ZIP CRC、各成员SHA/大小、完整成员集合、重复路径和路径穿越。

交付前核对49项原来源与快照、189个角色冻结文件、8份raw和完整回包逐字节一致，并验证8份成功提示词文本/实参及全部实际参考。两个ZIP均实际解压，再从解压目录复现全部8张历史候选；独立QA另已重放8版本共48个候选/预览/metrics文件。手机总览和四张独立PNG实际查看，总览1x与4x区域均校验为完整selected原像素。详见portable_reproduction_verification.json、production_source_verification.json、delivery_visual_QA.json及独立QA报告。

未改旧资产、人物卡或Mod代码；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py与verify_freeze.py用于原仓库排版与打包，依赖原仓库目录；独立解包使用verify_source_package.py、reproduce_candidates.py。
