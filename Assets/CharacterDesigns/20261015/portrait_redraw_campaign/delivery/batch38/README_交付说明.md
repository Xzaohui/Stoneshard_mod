# 第三十八批头像重绘交付说明

日期：2026-10-15。维菈、赫珀、司榆、布希共4人。独立审查冻结的带限制候选，不是原生逐像素终稿，也未集成或实机验证。

## 七件附件

1. batch38_四人头像总览_1x_4x.png：680×2184中文手机纵板；每人含74×100原尺寸及4倍最近邻展示。
2–5. VILA_维菈、HEPO_赫珀、SIYU_司榆、BUXI_布希各一份74×100透明PNG。
6. batch38_source_A_VILA_HEPO.zip：维菈与赫珀完整制作来源。
7. batch38_source_B_SIYU_BUXI.zip：司榆与布希完整制作来源。
两包均小于18 MiB，均附完整本批独立QA、总览、四张选中PNG及便携复现脚本。

## 冻结选稿与限制

### 维菈（vila）
选稿：vila/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：49f48179cf94d2aaef4db5e5362b0c752a64a861573ef9acb43ef8b620949627
- 性别仍未定，不据中性外观冻结身份canon。
- 夹镜边及眼白仍较亮，面部仍有imagegen细簇；仅有注记NN派生候选。
- 源边余量偏窄；inset不是重绘或原生像素验收。
- 未逐像素原生绘制，未集成或实机验收。

### 赫珀（hepo）
选稿：hepo/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：a95180b96ffa8cdae43fdfa4b4b42e0bb5d338fdc00b2c71ce7e08894df088be
- 白眼仍偏浅，绿披及下颈占比仍略大于核心；仅有注记NN派生候选。
- 源右边只留很窄的主要轮廓余量，边缘alpha5噪点仍记录；不把inset说成裁断修复。
- 未逐像素原生绘制，未集成或实机验收。

### 司榆（siyu）
选稿：siyu/candidates/portrait_v2_74x100_candidate.png
SHA256：b1fb37e69591762d7d868b20e9367b29f6a0abe49618decfd8871d3645fe696d
- 末S91他与正文她的代词不一致留痕，沿正文及女性母图，不修改源卡。
- 眼白仍偏浅，额部有细碎簇；仅有注记NN派生候选。
- 未逐像素原生绘制，未集成或实机验收。

### 布希（buxi）
选稿：buxi/candidates/portrait_v2_74x100_candidate.png
SHA256：f9b70515f015f28b7fa4b004d14abab888b245287c5ac572aec7b54171879ddd
- 现卡S91孤立他与旧女性母设定歧义，经git/brief/prompt及剧情核对后协调保女性继续，未改源卡。
- 少量眼白及鼻粉仍浅、面簇偏柔；仅有注记NN派生候选。
- 未逐像素原生绘制，未集成或实机验收。

## 方法与历史边界

每人两份成功生图，各一次集中必要反馈，未第三次重生。高分辨率生图使用整画布等比NEAREST缩放、取整输出尺寸、alpha阈值128、MAXCOVERAGE至多32可见色、无抖动、透明RGB归零。未手工补画、裁剪脸部或拼贴旧脸。32色只是临时技术上限，不等于原生像素美术认可。

维菈与赫珀选择同源v2的72×98 fit-box inset，置入74×100画布；司榆与布希选择74×100 full fit-box v2。inset只调整目标网格边缘接触，不补回未知源内容、不增加原图安全余量。赫珀raw右边缘最大alpha为5，主要发束在原画布内闭合，窄源边余量与透明噪点完整留证；不称作裁断修复。维菈与赫珀完整v1、v2、v2_inset，以及司榆与布希完整v1、v2历史派生均保留，未选历史派生不替代冻结选中PNG。

维菈约40岁，中性外观是可逆提案，性别未定；透明放大夹保持人物左眼／画面右眼。赫珀四十多岁，山风粗红皮肤、厚褂与母版绿短披兼容，不把近景描画当作山路检查完成。司榆正文女性与母图、母prompt一致，S91末段单个“他”记录为歧义，源文不改。布希旧卡无男性设定，母brief与prompt明确女性；现卡S91唯一“他”和细描总表同句镜像，不构成第二份独立证据。沿已验女性母身份继续，旧卡be19635、现卡09216ad、brief、prompt、台本与独立核对证据全部保留，不改源卡。最新细描年龄、衣装、鼻粉仍优先；紧脸头像未呈现手部、工具、服装全貌或剧情条件，不据此消除设定。

## 源包保留范围

角色制作目录全量快照共202文件：8张raw、8份完整成功工具回包、全部成功提示词txt与真实参数json、人物卡和剧情来源快照、身份母图/母QA/母manifest、四核心生成风格参考、10张历史候选、全部预览、metrics、作者自检、脚本、manifest与SHA256SUMS。维菈和赫珀各1份v2预检拒绝回包与原实参也忠实保留：超过5张参考图的参数校验拒绝，未生成图像，不能计作第三份成功生图。失败实参保留完整prompt文本；原目录没有对应txt，交付不伪造原始txt或改写实参。

独立QA完整111文件均进入两包，无省略项，包含31份最初原始源与4份补充源/历史git独立快照（合计35）、全部报告、历史/选中复现图、作者证据、selection_lock.json、manifest.json和SHA256SUMS。唯一选图锁为independent_qa/batch38/selection_lock.json，选中PNG与SHA必须完全吻合。

核验50项作者原来源/快照及35项独立原来源/快照，含实际git show历史字节与当前源字节核对；所有原路径和SHA均保留。商业原作像素参考图与sprite图集不进入交付；DELIVERY_EXCLUSIONS.json只保留背景参考路径、SHA和不含像素声明。生成身份与风格参考完整保留。

原始提示词中的绝对路径及历史参数忠实保留；便携复现使用包内相对路径，不依赖旧工作区路径。

## 校验与复现

验证环境：Python 3.12.14、Pillow 12.3.0。便携派生不调用生图服务、不访问网络。

1. 校验某ZIP：python verify_source_package.py batch38_source_A_VILA_HEPO.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在，脚本只写新输出，不改变冻结源文件。A包复现6张，B包复现4张，合计10张历史候选。
4. 逐张比较RGBA完整像素、PNG字节与SHA，成功输出all_pass=true。
5. verify_source_package.py核全ZIP CRC、所有成员SHA和字节大小、完整成员集合、重复路径及路径穿越。PACKAGE_SHA256SUMS.txt覆盖所有实质成员与package_inventory.json，清单自身由整个ZIP SHA锚定。

交付前实际查看手机纵板与四张独立PNG，1x/4x的全部8个展示区域逐像素验证。打包脚本实际解压每份ZIP，再从解压目录复现全部10张历史候选。证据位于portable_reproduction_verification.json、delivery_visual_QA.json、production_source_verification.json及完整独立QA。

未改源人物卡、旧资产或Mod代码；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py与verify_freeze.py为原仓库交付重建脚本，依赖仓库目录；便携解包复现使用verify_source_package.py与reproduce_candidates.py。
