# 头像重绘第十七批：四人候选交付

日期：2026-10-15。四名角色均选择独立 QA 冻结的 v2：缇弗 TIVER（MAE-S01-NPC）、薇榆 WEIYU（MAE-S02-NPC）、艾娜 ENA_COLDWINDOW（MAE-S03-NPC，冷窗驿）、礼昂 ELON（PAS-NPC-ELON）。冷窗艾娜与灰堤/主线 NPC-N-ENA 是不同身份；礼昂仍是一身份一身体的普通装卸工/患者，无军衔、无新增诊断，不代替 N7 配对的两名患者。

## 文件与状态

交付七件：中文手机纵向总览一张（680×2184，74×100 原尺寸与4倍最近邻展示）、四张独立74×100透明PNG、两份各小于18MiB的普通源码ZIP。

- A_TIVER_WEIYU：缇弗、薇榆完整制作目录。
- B_ENA_COLDWINDOW_ELON：冷窗艾娜、礼昂完整制作目录。
- 两个ZIP都带本批完整独立QA、交付总览、四张selected PNG、来源校验、交付冻结记录与便携复现脚本。

四人均为“带残留问题的生成/量化肖像候选”。本批无held。每人两次生图，v1未选与v2选中版本均原样保留。不重新生成，不补画，不修改角色源文件。

## 必须保留的限制

原始生图是高分辨率透明图。74×100候选由全画布同比例最近邻采样、alpha≥128二值化、无抖动调色板量化派生。它们不是原生74×100逐像素手工终稿，不代表用户美术终审、游戏集成或实机验收。32色是本轮临时技术上限，不是原作实测调色板规范。

- 缇弗：v2缩小头巾、缩短颈领，四十多岁照护工的宽颊方颌更清楚；发丝和头巾细褶仍偏碎，少量暖灰眼白仍在。
- 薇榆：沉眼睑、窄长脸与成熟颧面强化约五十岁抄写人身份；细发条和少量眼白仍在。
- 冷窗艾娜：低髻、芥黄领、深绿衣色与三十多岁外部接应人身份保留；眼白簇略宽，发面细条、轻微忧眉及较理想值偏长的颈段仍在。
- 礼昂：宽额方脸、短棕发近须、棕短褂与灰病号布边保留；下颌须纹及额头细线偏碎，肤色较暖。

## 源码追溯

每名角色目录内保留原始raw、完整工具回包（含原始base64）、完整提示词和参数、当前人物卡快照、身份母版、生成风格参考、剧情来源快照和SHA、未选v1、选中v2、预览、原始派生脚本、作者自检和清单。独立QA为independent_qa/batch17，冻结入口是freeze_manifest.json；交付以此而非作者自选为准。

未打包商业原作像素参考图或sprite图集。DELIVERY_EXCLUSIONS.json记录相关参考的路径/SHA及不含像素声明；本批生成身份参考和已生成风格候选保留。原始记录中可能存在绝对路径，这是忠实的历史工具参数；便携复现使用包内相对路径，不需要那些工作区路径。

## 校验与复现

依赖：Python 3.12、Pillow 12.3.0。图像本体使用确定性算法，无生图服务调用，无网络请求。缇弗/薇榆用单一比例逆像素中心最近邻和MAXCOVERAGE；冷窗艾娜/礼昂用72×98内部框的Pillow NEAREST整数尺寸同比例contain和MEDIANCUT。所有结果均alpha阈值128、无抖动、透明像素归零。

1. 校验某ZIP：python verify_source_package.py batch17_source_A_TIVER_WEIYU.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须不存在；脚本只写新输出，不改包内冻结文件。A、B分别复现所属两名角色的v1与v2，合计8张。
4. 脚本逐张比较RGBA像素及PNG完整字节与SHA；成功输出all_pass=true。
5. PACKAGE_SHA256SUMS.txt与package_inventory.json覆盖所有成员；verify_source_package.py还检查全ZIP CRC、成员SHA、大小、成员集合、重复路径与路径穿越。

交付前已核对55项原源与快照、167个角色冻结文件、8份raw与完整回包字节；两个ZIP都已实际解压，再由解压目录独立复现全部8张历史候选。手机总览与四张独立PNG已实际查看，总览1x和4x区域已验证来自完整selected原像素。各结论详见portable_reproduction_verification.json、production_source_verification.json、delivery_visual_QA.json及独立QA报告。

未改旧资产、人物卡或Mod代码；未commit/push；未集成或启动游戏。包内build_delivery.py和package_sources.py用于原仓库排版打包，依赖原仓库目录；面向独立解包使用的脚本为verify_source_package.py和reproduce_candidates.py。
