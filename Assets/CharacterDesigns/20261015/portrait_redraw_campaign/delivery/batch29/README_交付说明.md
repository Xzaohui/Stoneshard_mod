# 第二十九批头像重绘交付说明

日期：2026-10-15。芙伦、琼荷、墨达、罗莎·藤共4人。独立审查冻结的带限制候选，不是原生逐像素终稿，也未集成或实机验证。

## 七件附件

1. batch29_四人头像总览_1x_4x.png：680×2184中文手机纵板；每人含74×100原尺寸及4倍最近邻展示。
2–5. FULEN_芙伦、JONHE_琼荷、MODA_墨达、ROSA_罗莎·藤各一份74×100透明PNG。
6. batch29_source_A_FULEN_JONHE.zip：芙伦与琼荷完整制作来源。
7. batch29_source_B_MODA_ROSA.zip：墨达与罗莎·藤完整制作来源。
两包均小于18 MiB，均附完整本批独立QA、总览、四张选中PNG及便携复现脚本。

## 冻结选稿与限制

### 芙伦（fulen）
选稿：fulen/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：b6e1a7a2ccf76396953d4434fd9f412324b093c558e15b168660faec7c0bef38
- 源左发真实余量仅5/1079源像素，安全余量不足仍保留；inset仅解决目标NN采样触边。
- 眼白仍局部亮点，米白头巾占幅偏大，发纹需未来原生逐像素整理。
- 仅为NN/32色技术派生候选，非原生逐像素终稿；未导入、未实机验证。

### 琼荷（jonhe）
选稿：jonhe/candidates/portrait_v2_74x100_candidate.png
SHA256：29e6b3336e876163259db831a7bbe4a0cae27c1a11527825d3c0195cbd843b36
- 眼白仍有局部较亮暖点；帽发与灰辫占幅偏大，顶端留白偏多，面部覆盖低于紧凑核心。
- 浅色发丝量化后有细碎块；仍为生成图NN与32色技术派生，未逐像素原生整理。
- 非原生逐像素终稿；未导入、未实机验证。

### 墨达（moda）
选稿：moda/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：ec29da9943e114082abacdf341675969facf069ce4ab6e183ae6cd53c42a5f0f
- 源右侧不透明轮廓仅2/1079源像素余量，极窄且边缘alpha残留触边；inset只避目标网格触边，不修复或提高源余量。
- 眼白仍局部偏亮灰暖点，深棕卷发和巾皱纹略碎，面部整体像素组织未原生整理。
- 仅为NN/32色技术派生候选，非原生逐像素终稿；未导入、未实机验证。

### 罗莎·藤（rosa）
选稿：rosa/candidates/portrait_v2_74x100_candidate.png
SHA256：2f63db5a677ad9e6f5a07f74eeb68feac575fe803ea0281ba5b54989578a52fb
- 灰缕发纹依然偏碎、眼部残留少量亮暖点；像素结构仍需原生逐点整理。
- 仅为NN/32色技术派生候选，非原生逐像素终稿；未导入、未实机验证。

## 方法与历史边界

每人两份成功生图，未第三次重生。高分辨率生图使用整画布等比NEAREST缩放、取整输出尺寸、alpha阈值128、MAXCOVERAGE至多32可见色、无抖动、透明RGB归零。未手工补画、裁剪脸部或拼贴旧脸。32色只是临时技术上限，不等于原生像素美术认可。

芙伦与墨达选择同源v2的72×98 fit-box inset，置入74×100画布；原始v1、v2 full及inset全保留。inset只改善目标网格边缘接触，不补回未知源内容、不增加原图安全余量。芙伦原图左发真实余量仅5/1079像素；墨达原图右侧不透明轮廓仅2/1079像素余量且有低alpha边缘残留；独立审查实际看过原图外轮廓，仍须保留安全余量不足的限制。

琼荷和罗莎·藤选完整74×100 fit-box v2。罗莎同源inset属于未选历史派生，完整保留但不替代选中PNG。琼荷低檐帽与工作褂、芙伦短发与护理衣着、墨达四十多岁及红鼻头、罗莎深色酿酒围裙均按当前人物卡校准，不改身份母图、人物卡或旧资产。

## 源包保留范围

角色制作目录全量快照共210文件：8张raw、8份完整成功工具回包、全部提示词txt与真实参数json、人物卡和剧情来源快照、身份母图/母QA/母manifest、四核心生成风格参考、11张历史候选、所有预览、metrics、作者自检、脚本、manifest与SHA256SUMS。墨达v2的超过5张参考图预检拒绝回包也忠实保留，该回包无生成图片，不能计作第三份成功生图。

独立QA完整99文件均进入两包，没有省略项，包含28份原始源独立快照、全部报告、历史/选中复现图、作者证据、selection_lock.json、manifest.json和SHA256SUMS。唯一选图锁为independent_qa/batch29/selection_lock.json，选中PNG与SHA必须完全吻合。

核验45项作者原来源/快照及28项独立原来源/快照，所有原路径和SHA均保留。商业原作像素参考图与sprite图集不进入交付；DELIVERY_EXCLUSIONS.json只保留背景参考路径、SHA和不含像素声明。生成身份与风格参考完整保留。

原始提示词中的绝对路径忠实保留；便携复现使用包内相对路径，不依赖那些旧工作区路径。

## 校验与复现

验证环境：Python 3.12.14、Pillow 12.3.0。便携派生不调用生图服务、不访问网络。

1. 校验某ZIP：python verify_source_package.py batch29_source_A_FULEN_JONHE.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在，脚本只写新输出，不改变冻结源文件。A包复现5张，B包复现6张，合计11张历史候选。
4. 逐张比较RGBA完整像素、PNG字节与SHA，成功输出all_pass=true。
5. verify_source_package.py核全ZIP CRC、所有成员SHA和字节大小、完整成员集合、重复路径及路径穿越。PACKAGE_SHA256SUMS.txt覆盖所有实质成员与package_inventory.json，清单自身由整个ZIP SHA锚定。

交付前已实际查看手机纵板与四张独立PNG，1x/4x的全部8个展示区域均逐像素验证。打包脚本实际解压每份ZIP，再从解压目录复现全部11张历史候选。证据位于portable_reproduction_verification.json、delivery_visual_QA.json、production_source_verification.json及完整独立QA。

未改源人物卡、旧资产或Mod代码；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py与verify_freeze.py为原仓库交付重建脚本，依赖仓库目录；便携解包复现使用verify_source_package.py与reproduce_candidates.py。
