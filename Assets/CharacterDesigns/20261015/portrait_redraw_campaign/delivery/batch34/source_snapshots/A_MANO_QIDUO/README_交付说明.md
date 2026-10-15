# 第三十四批头像重绘交付说明

日期：2026-10-15。玛诺·灯、祁铎、西婕、艾钦共4人。独立审查冻结的带限制候选，不是原生逐像素终稿，也未集成或实机验证。

## 七件附件

1. batch34_四人头像总览_1x_4x.png：680×2184中文手机纵板；每人含74×100原尺寸及4倍最近邻展示。
2–5. MANO_玛诺·灯、QIDUO_祁铎、XIJIE_西婕、AIQIN_艾钦各一份74×100透明PNG。
6. batch34_source_A_MANO_QIDUO.zip：玛诺·灯与祁铎完整制作来源。
7. batch34_source_B_XIJIE_AIQIN.zip：西婕与艾钦完整制作来源。
两包均小于18 MiB，均附完整本批独立QA、总览、四张选中PNG及便携复现脚本。

## 冻结选稿与限制

### 玛诺·灯（mano）
选稿：mano/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：2bae88536962d009ebb40ed6476a4d1344e5d62d9e4ca6e75b71ae50a9fae7b6
- 内眉仍略带担忧；raw中少量亮眼点和平行帽发层未完全消除。
- 当前卡L17她/L40他孤立代词冲突原文与SHA完整保留；依父任务明确允许及母图母QA女性证据继续女性，不修改源卡。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

### 祁铎（qiduo）
选稿：qiduo/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：7be587908584abd2d86a77b7f6e8c41e94008429a94e6a935153eb35caa69a25
- 唇上与下颌仍有细点/锯齿胡茬，眼白偏亮、眉略厚于母QA薄平眉；不声称全部风格缺口清零。
- 伤与去留是台本条件，紧脸裁幅没有呈现护腕/腿伤不等于伤愈或同意复井。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

### 西婕（xijie）
选稿：xijie/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：423e64fb078e27cf10bef5712e6d6403899c874633e1034c58f10c40fd9d2a08
- 眼白仍偏亮、上眼线与平行发束比四核心粗簇目标更醒目；只准带限制候选。
- 最新卡旧皮护具覆盖历史橄榄衣短围裙，窄领不能展示全身皮护磨损、锤与记录板。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

### 艾钦（aiqin）
选稿：aiqin/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：a987c64d2f276a3bf4597934f6657d3fc165f57f7e0631048d353f6dd438c285
- 眉口仍略忧郁，原raw眼白不全暗、头发仍有平行层；没有宣称克制旧怒的表现已完美。
- 最新卡改小父亲旧工装覆盖历史蓝裙披巾，紧脸不表现手茧、卷袖、腰扳手或工作牌。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

## 方法与历史边界

每人两份成功生图，各一次集中必要反馈，未第三次重生。高分辨率生图使用整画布等比NEAREST缩放、取整输出尺寸、alpha阈值128、MAXCOVERAGE至多32可见色、无抖动、透明RGB归零。未手工补画、裁剪脸部或拼贴旧脸。32色只是临时技术上限，不等于原生像素美术认可。

四人均选择同源v2的72×98 fit-box inset，置入74×100画布。inset只调整目标网格边缘接触，不补回未知源内容、不增加原图安全余量。每人完整v1、v2、v2_inset历史派生均保留，未选历史派生不替代冻结选中PNG。

最新人物卡优先旧母图外观：玛诺约50岁女性班长，棕帽赭黄厚工衣，卡中L17她/L40他孤立代词冲突原文与SHA完整保留，按本轮授权及母图/母QA女性证据继续女性，不修改源卡。祁铎30多岁伤矿工，矿尘灰发灰棕工衣；伤与去留仍是台本条件，头像不显示伤处不等于伤愈或同意复井。西婕约40岁独立段检匠，橄榄内领棕旧皮护领覆盖历史橄榄衣短围裙。艾钦30多岁维护者之女、祁铎之妹，中分低辫、改小父亲褪蓝工装覆盖历史蓝裙披巾。紧脸头像不能呈现全身工具、护腕/腿伤、手茧等条件，不据此消除人物设定。

## 源包保留范围

角色制作目录全量快照共224文件：8张raw、8份完整成功工具回包、全部成功提示词txt与真实参数json、人物卡和剧情来源快照、身份母图/母QA/母manifest、四核心生成风格参考、12张历史候选、全部预览、metrics、作者自检、脚本、manifest与SHA256SUMS。西婕和艾钦各两份v2预检拒绝回包与原实参也忠实保留：一次相对路径、一次超过5张参考图，均未生成图像，不能计作第三份成功生图。4份失败实参保留完整prompt文本；原目录没有对应txt，交付不伪造原始txt或改写实参。

独立QA完整104文件均进入两包，无省略项，包含29份原始源独立快照、全部报告、历史/选中复现图、作者证据、selection_lock.json、manifest.json和SHA256SUMS。唯一选图锁为independent_qa/batch34/selection_lock.json，选中PNG与SHA必须完全吻合。

核验55项作者原来源/快照及29项独立原来源/快照，所有原路径和SHA均保留。商业原作像素参考图与sprite图集不进入交付；DELIVERY_EXCLUSIONS.json只保留背景参考路径、SHA和不含像素声明。生成身份与风格参考完整保留。

原始提示词中的绝对路径与失败的相对路径忠实保留；便携复现使用包内相对路径，不依赖旧工作区路径。

## 校验与复现

验证环境：Python 3.12.14、Pillow 12.3.0。便携派生不调用生图服务、不访问网络。

1. 校验某ZIP：python verify_source_package.py batch34_source_A_MANO_QIDUO.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在，脚本只写新输出，不改变冻结源文件。A包复现6张，B包复现6张，合计12张历史候选。
4. 逐张比较RGBA完整像素、PNG字节与SHA，成功输出all_pass=true。
5. verify_source_package.py核全ZIP CRC、所有成员SHA和字节大小、完整成员集合、重复路径及路径穿越。PACKAGE_SHA256SUMS.txt覆盖所有实质成员与package_inventory.json，清单自身由整个ZIP SHA锚定。

交付前实际查看手机纵板与四张独立PNG，1x/4x的全部8个展示区域逐像素验证。打包脚本实际解压每份ZIP，再从解压目录复现全部12张历史候选。证据位于portable_reproduction_verification.json、delivery_visual_QA.json、production_source_verification.json及完整独立QA。

未改源人物卡、旧资产或Mod代码；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py与verify_freeze.py为原仓库交付重建脚本，依赖仓库目录；便携解包复现使用verify_source_package.py与reproduce_candidates.py。
