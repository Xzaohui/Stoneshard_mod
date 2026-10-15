# 第三十三批头像重绘交付说明

日期：2026-10-15。岱里、艾珀·风、科蔚、洛芙共4人。独立审查冻结的带限制候选，不是原生逐像素终稿，也未集成或实机验证。

## 七件附件

1. batch33_四人头像总览_1x_4x.png：680×2184中文手机纵板；每人含74×100原尺寸及4倍最近邻展示。
2–5. DAILI_岱里、APE_艾珀·风、KEWEI_科蔚、LUOFU_洛芙各一份74×100透明PNG。
6. batch33_source_A_DAILI_APE.zip：岱里与艾珀·风完整制作来源。
7. batch33_source_B_KEWEI_LUOFU.zip：科蔚与洛芙完整制作来源。
两包均小于18 MiB，均附完整本批独立QA、总览、四张选中PNG及便携复现脚本。

## 冻结选稿与限制

### 岱里（daili）
选稿：daili/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：b97465b3e5e64f50dc5839316e8fcf09cad880609dd4d4cd3f3f5b7c726f5f89
- 发巾卷发仍占较多幅面，颈仍有小段；未再开新生图。
- 年龄与紧绷情绪为块面概念表达，非逐像素原生精修。
- NN技术派生候选，未集成或实机验证。

### 艾珀·风（ape）
选稿：ape/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：6190add257fc41f31e2f18bac095316ab8eb0ec453d08d419d3e729b87677f89
- 须发仍有一定细纹，颈段虽短仍未达到极简。
- 年龄读法风霜偏重，保留母图灰发疲态，不声称精确年龄写实肖像。
- NN技术派生候选，未集成或实机验证。

### 科蔚（kewei）
选稿：kewei/candidates/portrait_v2_inset_74x100_candidate.png
SHA256：08599118ea63d7ec78ec3501c32aac4f89e23123384c6dd0b08dcb2f4aaf647c
- 须部仍留一些细纹与插值观感，仅为粗块风格候选。
- NN技术派生候选，未逐像素原生精修、未集成或实机验证。

### 洛芙（luofu）
选稿：luofu/candidates/portrait_v2_74x100_candidate.png
SHA256：7c9983c5bd9621243d81b0ad49ec1a667702170e78d0940bc82a86fb571d7bd2
- 颈与衣区仍比核心多，白巾仍带细条；只作带注候选，不宣称严格最终风格验收。
- 头巾所占上部较多；没有第三次生成或脚本改脸。
- NN技术派生候选，未逐像素原生精修、未集成或实机验证。

## 方法与历史边界

每人两份成功生图，各一次集中必要反馈，未第三次重生。高分辨率生图使用整画布等比NEAREST缩放、取整输出尺寸、alpha阈值128、MAXCOVERAGE至多32可见色、无抖动、透明RGB归零。未手工补画、裁剪脸部或拼贴旧脸。32色只是临时技术上限，不等于原生像素美术认可。

岱里、艾珀·风、科蔚选择同源v2的72×98 fit-box inset，置入74×100画布；洛芙选择74×100 fit-box v2。inset只调整目标网格边缘接触，不补回未知源内容、不增加原图安全余量。每人的完整v1/v2及历史inset均保留，未选历史派生不替代冻结选中PNG。

最新人物卡优先旧母图外观：岱里约60岁女性看屋人，白巾灰缕橄榄厚衣；艾珀约40岁男性本段通风维护者，灰褐短须发褪蓝罩衣；科蔚约50岁男性有限出资者，整齐灰发短尖胡与深外套；洛芙30多岁女性水渠维护者，扎紧白巾橄榄罩衣。不修改人物卡或身份母图。

## 源包保留范围

角色制作目录全量快照共252文件：8张raw、8份完整成功工具回包、全部提示词txt与真实参数json、人物卡和剧情来源快照、身份母图/母QA/母manifest、四核心生成风格参考、14张历史候选、所有预览、metrics、作者自检、脚本、manifest与SHA256SUMS。岱里v2的超过5张参考图预检拒绝回包和原实参也忠实保留，该回包无生成图片，不能计作第三份成功生图。

独立QA完整114文件均进入两包，没有省略项，包含36份原始源独立快照、全部报告、历史/选中复现图、作者证据、selection_lock.json、manifest.json和SHA256SUMS。唯一选图锁为independent_qa/batch33/selection_lock.json，选中PNG与SHA必须完全吻合。

核验59项作者原来源/快照及36项独立原来源/快照，所有原路径和SHA均保留。商业原作像素参考图与sprite图集不进入交付；DELIVERY_EXCLUSIONS.json只保留背景参考路径、SHA和不含像素声明。生成身份与风格参考完整保留。

原始提示词中的绝对路径忠实保留；便携复现使用包内相对路径，不依赖那些旧工作区路径。

## 校验与复现

验证环境：Python 3.12.14、Pillow 12.3.0。便携派生不调用生图服务、不访问网络。

1. 校验某ZIP：python verify_source_package.py batch33_source_A_DAILI_APE.zip
2. 解压后在包目录运行：python reproduce_candidates.py --output /path/to/new-empty-output
3. 输出目录必须尚不存在，脚本只写新输出，不改变冻结源文件。A包复现8张，B包复现6张，合计14张历史候选。
4. 逐张比较RGBA完整像素、PNG字节与SHA，成功输出all_pass=true。
5. verify_source_package.py核全ZIP CRC、所有成员SHA和字节大小、完整成员集合、重复路径及路径穿越。PACKAGE_SHA256SUMS.txt覆盖所有实质成员与package_inventory.json，清单自身由整个ZIP SHA锚定。

交付前实际查看手机纵板与四张独立PNG，1x/4x的全部8个展示区域逐像素验证。打包脚本实际解压每份ZIP，再从解压目录复现全部14张历史候选。证据位于portable_reproduction_verification.json、delivery_visual_QA.json、production_source_verification.json及完整独立QA。

未改源人物卡、旧资产或Mod代码；未commit/push；未集成或启动游戏。build_delivery.py、package_sources.py与verify_freeze.py为原仓库交付重建脚本，依赖仓库目录；便携解包复现使用verify_source_package.py与reproduce_candidates.py。
