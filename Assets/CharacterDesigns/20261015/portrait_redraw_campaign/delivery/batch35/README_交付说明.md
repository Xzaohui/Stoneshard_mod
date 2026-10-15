# 第三十五批头像重绘交付说明

日期：2026-10-15。蓓娜、枯恩、琳汀·床共3名带限制候选；安妮风格暂缓，selected=null，不回退历史版本。所有结果仅为高分辨率生图的74×100最近邻技术派生候选，非原生手工逐像素终稿、未集成游戏、未实机验证。

## 六件附件

1. batch35_三人头像总览_1x_4x.png：680×1898中文手机纵板；每人含74×100原尺寸及4倍最近邻展示。安妮仅显示暂缓文字，不展示成功头像。
2–4. BEINA_蓓娜、KUEN_枯恩、LINT_琳汀·床各一张74×100透明PNG。
5. batch35_source_A_BEINA_KUEN.zip：蓓娜、枯恩完整制作来源。
6. batch35_source_B_LINT_ANNI_held.zip：琳汀·床完整制作来源与安妮完整暂缓证据。
两包均小于18 MiB，每包均附完整独立QA、三人总览、3张选稿及便携复现脚本。

## 冻结选稿与限制

### 蓓娜（beina）
选稿：beina/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：9ee071b9643c6305e982e9d163c2035c07c6cbfc55c6009f541e238f0674d4de
- 内眉仍略忧惧、嘴角略低，神态未完全改成平稳坚定。
- 眼白不全暗，发巾仍有平行层；头上透明余量较大，未宣称风格缺口全部清零。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

### 安妮（anni）
状态：风格暂缓，selected=null，不计成功。
证据：anni/candidates/portrait_v2_inset_74x100_candidate.png
证据SHA256：1e16522451cd110f00dfd96e835ffca630ecc55ce19f8973102ffcf377471125
- 风格暂挂：大亮眼白、妆感上眼线、小鼻甜脸仍主导，未通过四核心系列风格gate。
- v2真源裁断已修好；不靠inset或padding掩盖裁断。保留完整新raw和inset作证据，不列入交付选稿。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

### 枯恩（kuen）
选稿：kuen/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：f5789504824665242a16f5a30ce6bf533168a0b6146dccec3d72449aed2c68c8
- 眼白仍偏亮、内眉仍略提，未完全达到小暗眼白/平稳眉口目标。
- 胡茬仍有细碎点和锯齿，平行发束仍偏密；仅带限制候选，不能以技术格式宣称纯原生手绘。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

### 琳汀·床（lint）
选稿：lint/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：466434bdc2e245be6716f902080e607ceb2323aefdd2f75686a491600e9d557a
- 内眉仍略忧、眼白偏亮及上眼线较强，平稳利落表现未完全满足理想。
- 头发仍有平行层和皮肤小折面；窄领不能证明完整护理褂袖扣/随身物已制作。
- 仅74×100 NN技术派生候选，非原生逐像素终稿、未集成游戏、未实机验证。

## 方法与身份边界

四人各有两份成功生图、一次集中必要反馈，未第三次重生。采用整画布等比NEAREST缩放、取整输出尺寸、alpha阈值128、MAXCOVERAGE至多32可见色、无抖动、透明RGB归零。未手工补画、裁脸、几何重绘或拼贴旧脸。32色只是临时技术上限，不代表原生像素美术认可。

三人均选择同源v2的72×98 fit-box inset，置入74×100透明画布。inset只调整目标网格边缘接触，不能修复真正源裁断、不补未知头发耳朵；安妮v1真实裁边由v2重新生成修复，当前只因风格暂缓。保留每人的v1、v2、v2_inset全部历史派生；未选历史图不能冒充冻结选中头像。

最新人物卡优先旧母图：蓓娜约40岁洗砂住户，严包蓝头巾、灰旧罩衣、锈色内领，不写成受气包；枯恩30多岁苍白自主患者，棕乱发稀胡茬、厚灰褐披肩与灰蓝内领，不将照护需要写成爱情考题；琳汀30多岁护理接收员，短发别耳后及素护理褂优先旧高髻赭裙，只接当班；安妮20多岁普通当班护理者，棕低髻与素护理褂，只签这一班。紧脸头像不能展示手部痕迹、扣袖与随身物，不能据此宣称设定已完整制作。

## 源包保留范围

四人制作目录全量211文件：8张raw、8份完整成功工具回包、8份成功提示词txt与8份真实参数json、12张历史候选、人物卡与剧情来源快照、身份母图/母QA/母manifest、四核心生成风格参考、全部预览、metrics、作者自检和反馈、脚本、manifest与SHA256SUMS。没有遗漏安妮held的raw/回包/提示词/参数/历史QA。

独立QA完整109文件均进入两包，无省略项，包含34份原始源独立快照、完整技术/视觉报告、历史和选中复现图、源终检、selection_lock.json、manifest.json与SHA256SUMS（107清单项、108 SHA项）。唯一选稿锁是independent_qa/batch35/selection_lock.json，SHA256 ca07cfc6fab66999a44c8a08bf3b69db2ff31e27a5bb5a52345dad28b007ae6e。所有角色原来源与快照SHA、独立34份原来源与快照SHA在冻结和打包前重新核对。

商业原作像素参考图和sprite图集不进入交付；DELIVERY_EXCLUSIONS.json仅保留背景参考路径、SHA和不含像素声明。生成的身份与四核心风格参考完整保留。原始提示词的绝对路径忠实保留；便携复现使用包内相对路径，不依赖旧工作区路径。

## 校验与复现

验证环境：Python 3.12.14、Pillow 12.3.0。便携派生无需生图服务或网络。

1. 校验ZIP：python verify_source_package.py batch35_source_A_BEINA_KUEN.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在。脚本只写新输出，不改冻结源文件。A包复现6张、B包复现6张，合计12张历史候选，包括安妮的3张仅作证据派生。
4. 逐张比较RGBA完整像素、PNG字节和SHA，成功输出all_pass=true。
5. verify_source_package.py核全ZIP CRC、所有成员SHA/字节大小、完整成员集合、重复路径和路径穿越。PACKAGE_SHA256SUMS.txt覆盖所有实质成员与package_inventory.json，清单自身由整个ZIP SHA锚定。

交付前实际查看手机纵板与三张独立PNG，1×/4×全部6个展示区域逐像素验证。打包后实际解压两份ZIP，从解压目录重新复现全部12张历史候选。证据见portable_reproduction_verification.json、delivery_visual_QA.json、production_source_verification.json与完整独立QA。

仅写delivery/batch35，未改源人物卡、旧资产、制作源目录或Mod代码；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py、make_freeze_gate.py为原仓库交付重建脚本，依赖原仓库目录；解包后的便携校验使用verify_source_package.py和reproduce_candidates.py。
