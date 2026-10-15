# 第二十八批头像重绘交付说明

日期：2026-10-15。薇柯、伊蕾、哈伦、贝洛共4人。独立审查冻结的带限制候选，不是原生逐像素终稿，也未集成或实机验证。

## 七件附件

1. batch28_四人头像总览_1x_4x.png：680×2184中文手机纵板；每人含74×100原尺寸及4倍最近邻展示。
2–5. VIKO_薇柯、ILE_伊蕾、HARLEN_哈伦、BELO_贝洛各一份74×100透明PNG。
6. batch28_source_A_VIKO_ILE.zip：薇柯与伊蕾完整制作来源。
7. batch28_source_B_HARLEN_BELO.zip：哈伦与贝洛完整制作来源。
两包均小于18 MiB，均附完整本批独立QA、总览、四张选中PNG及便携复现脚本。

## 冻结选稿与限制

### 薇柯（viko）
选稿：viko/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：eb30a2f311779a1cee39bffeebca45e1b3efac8ed23e672201c37e10375bba09
- 眼白与眼框仍比四核心稍亮大；不是严格小暗眼终稿。
- 头发带状细节仍较多，非原生逐像素终稿。
- 源alpha≥16右余4px、≥128右4px；仅一个alpha≥5弱点触右缘，未达4%目标。full网格x73触边，选同源72×98整幅等比inset，未补画源轮廓。

### 伊蕾（ile）
选稿：ile/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：378f6ce15c03de6aacaeaf8dcdfe52e84a462fbb9ae4247e6f66e8fedb7658fb
- 眼白仍较亮、发带与颈部细节偏多，短颈/大脸目标仅部分达到。
- 源alpha≥16右核心2px，≥128为3px，alpha≥5仍有20个极弱右缘点；未达4%余量目标，不声称全alpha无触边。
- full采样到目标x73属于NN网格贴边；选同源72×98整幅等比inset，不能把inset称作源裁断修复。
- 原生像素与实机未经验证。

### 哈伦（harlen）
选稿：harlen/candidates/portrait_v2_74x100_candidate.png
SHA256：37e64b70711cfc88486b1c1ae1c9627eee72a452599acaa4c529aed190774ccb
- 发须仍有较多碎条与点，不是四核心同等简练像素组织。
- 眼白仍可见，颈尚略长；作为带限制NN候选交付。
- 源实心右余20px，小于约4%提示目标，但完整发/耳轮廓无实质裁断；alpha≥5四边0。

### 贝洛（belo）
选稿：belo/candidates/portrait_v2_74x100_candidate.png
SHA256：1010d438786069d51b0dc54a6365facb7d06c03220f4dd76c2d17c32ec90f432
- 眼白仍偏亮，颈段仍略长，发束仍多于四核心。
- 顶空15px使头占较四核心偏小；完整源不裁剪、不脚本放大脸。
- 源实心右余31px，小于约4%提示目标，但无发耳实质裁断；alpha≥5四边0。

## 方法与历史边界

每人最多两份成功生图，未第三次重生。高分辨率生图使用整画布等比NEAREST缩放、取整输出尺寸、alpha阈值128、MAXCOVERAGE至多32可见色、无抖动、透明RGB归零。未手工补画、裁剪脸部或拼贴旧脸。32色只是临时技术上限，不等于原生像素美术认可。

薇柯与伊蕾选择同源v2的72×98 fit-box inset，置入74×100画布；原始v1、v2 full及inset全保留。inset只改善目标网格边缘接触，不补回未知源内容。伊蕾v1的实心源裁断问题已经由v2重画处理；v2仍有极弱边缘alpha及窄实心余量限制。哈伦与贝洛使用完整74×100 fit-box v2。哈伦年龄与烟熏黄发遵从最新人物卡，旧灰须母图只保留身份参考。

## 源包保留范围

角色制作目录全量快照共205文件：8张raw、8份完整工具回包、全部提示词txt与真实参数json、人物卡和剧情来源快照、身份母图/母QA/母manifest、四核心生成风格参考、10张历史候选、所有预览、metrics、作者自检、脚本、manifest与SHA256SUMS。薇柯v2预检错误回包也忠实保留，不能计作第三份成功生图。

独立QA完整94文件均进入两包，没有省略项，包含原始源独立快照、全部报告、复现图、作者证据、selection_lock.json、manifest.json和SHA256SUMS。唯一选图锁为independent_qa/batch28/selection_lock.json，选中PNG与SHA必须完全吻合。

核验48项作者原来源/快照及30项独立原来源/快照，所有原路径和SHA均保留。商业原作像素参考图与sprite图集不进入交付；DELIVERY_EXCLUSIONS.json只保留背景参考路径、SHA和不含像素声明。生成身份与风格参考完整保留。

原始提示词中的绝对路径忠实保留；便携复现使用包内相对路径，不依赖那些旧工作区路径。

## 校验与复现

验证环境：Python 3.12.14、Pillow 12.3.0。便携派生不调用生图服务、不访问网络。

1. 校验某ZIP：python verify_source_package.py batch28_source_A_VIKO_ILE.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在，脚本只写新输出，不改变冻结源文件。A包复现6张，B包复现4张，合计10张历史候选。
4. 逐张比较RGBA完整像素、PNG字节与SHA，成功输出all_pass=true。
5. verify_source_package.py核全ZIP CRC、所有成员SHA和字节大小、完整成员集合、重复路径及路径穿越。PACKAGE_SHA256SUMS.txt覆盖所有实质成员与package_inventory.json，清单自身由整个ZIP SHA锚定。

交付前已实际查看手机纵板与四张独立PNG，1x/4x的全部8个展示区域均逐像素验证。打包脚本实际解压每份ZIP，再从解压目录复现全部10张历史候选。证据位于portable_reproduction_verification.json、delivery_visual_QA.json、production_source_verification.json及完整独立QA。

未改源人物卡、旧资产或Mod代码；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py与verify_freeze.py为原仓库交付重建脚本，依赖仓库目录；便携解包复现使用verify_source_package.py与reproduce_candidates.py。
