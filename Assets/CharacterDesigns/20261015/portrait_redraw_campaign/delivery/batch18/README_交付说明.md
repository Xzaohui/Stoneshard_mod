# 头像重绘第十八批：四人候选交付

日期：2026-10-15。四名角色均选择独立 QA 冻结的 v2：列梵 LEVAN（PAS-NPC-LEVAN）、绮伦 QILEN（PAS-NPC-QILEN）、莎帛 SHABO（PAS-NPC-SHABO）、沃汀 WOTIN（PAS-NPC-WOTIN）。身份以本批保存的当前人物卡和剧情快照为准；绮伦只称列梵成年亲属，不擅自确定亲属辈分；莎帛是普通护理当班人；沃汀左臂的疤不搬到脸上。

## 文件与状态

交付七件：中文手机纵向总览一张（680×2184，74×100 原尺寸与4倍最近邻展示）、四张独立74×100透明PNG、两份各小于18MiB的普通源码ZIP。

- A_LEVAN_QILEN：列梵、绮伦完整制作目录。
- B_SHABO_WOTIN：莎帛、沃汀完整制作目录。
- 两个ZIP都带本批完整独立QA交付证据、交付总览、四张selected PNG、来源校验、交付冻结记录与便携复现脚本。

四人均为“带残留问题的生成/量化肖像候选”。本批无held。每人两次生图，v1未选与v2选中版本均原样保留。不重新生成，不补画，不修改角色源文件。

## 必须保留的限制

原始生图是高分辨率透明图。74×100候选由全画布同比例最近邻采样、alpha≥128二值化、无抖动调色板量化派生。它们不是原生74×100逐像素手工终稿，不代表用户美术终审、游戏集成或实机验收。32色是本轮临时技术上限，不是原作实测调色板规范。

- 列梵：暗波发、二十多岁净面与克制闭唇保留；v2眼白压暗、裸颈缩短、锈衣领提高。眼白与发线仍有细亮点，左右约1目标像素留边。
- 绮伦：四十岁上下的宽下颊长圆脸、宽鼻及薄弧暖笑保留；米白头巾与高绿领忠实。眼内仍有亮点，米白巾较亮，右侧约1目标像素留边。
- 莎帛：三十多岁的宽短鼻、厚下唇、方短颌、短棕发及米白巾保留；高蓝领缩短颈段。眼白和头巾仍略亮，眉略严肃，右侧1目标像素留边。
- 沃汀：四十多岁的长矩脸、长鼻、暗八字胡、清下巴和小张口保留；低平暗眼与短颈高橄榄领改善。近眼小高光、细发线及少量硬折线仍在，右侧1目标像素留边。

四张选中v2的原始raw均无alpha≥128实色触边；留边是真实源图余量。此批没有用padding或inset补回缺失内容，所有候选均使用74×100全画布fit。

## 源码追溯

每名角色目录内保留原始raw、完整工具回包（含原始base64）、完整提示词和参数、当前人物卡快照、身份母版、生成风格参考、剧情来源快照和SHA、未选v1、选中v2、预览、原始派生脚本、作者自检和清单。独立QA为independent_qa/batch18，冻结入口是freeze_manifest.json；交付以此而非作者自选为准。

未打包商业原作像素参考图或sprite图集。DELIVERY_EXCLUSIONS.json记录相关参考的路径/SHA及不含像素声明；本批生成身份参考和已生成风格候选保留。原始记录中可能存在绝对路径，这是忠实的历史工具参数；便携复现使用包内相对路径，不需要那些工作区路径。独立QA重复运行所用的临时raw/工具回包副本不再次打包，原始内容已完整保存在对应角色目录；QA报告、运行日志、脚本及独立复现候选按冻结清单保留。

## 校验与复现

依赖：Python 3.12、Pillow 12.3.0。图像本体使用确定性算法，无生图服务调用，无网络请求。四人所有历史候选都用74×100全画布Pillow NEAREST整数尺寸同比例contain和MAXCOVERAGE量化。所有结果均alpha阈值128、无抖动、透明像素归零。

1. 校验某ZIP：python verify_source_package.py batch18_source_A_LEVAN_QILEN.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须不存在；脚本只写新输出，不改包内冻结文件。A、B分别复现所属两名角色的v1与v2，合计8张。
4. 脚本逐张比较RGBA像素及PNG完整字节与SHA；成功输出all_pass=true。
5. PACKAGE_SHA256SUMS.txt与package_inventory.json覆盖全部实质成员，校验清单本身由最终ZIP SHA锚定；verify_source_package.py检查全ZIP CRC、每成员SHA、大小、成员集合、重复路径与路径穿越。

交付前核对45项原源与快照、184个角色冻结文件、8份raw与完整回包字节；两个ZIP均实际解压，再由解压目录独立复现全部8张历史候选。手机总览与四张独立PNG实际查看，总览1x和4x区域验证来自完整selected原像素。各结论详见portable_reproduction_verification.json、production_source_verification.json、delivery_visual_QA.json及独立QA报告。

未改旧资产、人物卡或Mod代码；未commit/push；未集成或启动游戏。包内build_delivery.py和package_sources.py用于原仓库排版打包，依赖原仓库目录；面向独立解包使用的脚本为verify_source_package.py和reproduce_candidates.py。
