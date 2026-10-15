# Batch08 独立 QA 终审

日期：2026-10-15 UTC。范围：奥辛、佩兰、蕾娜、罗安。状态：四张已选定并冻结的带限制概念候选；技术审计通过，视觉目标并非全部满足。不是原生逐像素终稿，不代表用户认可或游戏内验收。

## 终选

- 奥辛：osin/candidates/portrait_v2_74x100_candidate.png。40多岁秃顶宽脸男班长、皮围裙铆钉和橄榄领口保持；v2连须大块、短颈窄领较v1改善。仍有较宽赭灰眼白、局部额颧细点，右侧余量仅1像素。
- 佩兰：pelan/candidates/portrait_v2_74x100_candidate.png。约50岁女住客、发髻、灰褐挺领保持；v2平眉闭嘴和重眼睑更自持。仍有条束头发、少量亮眼缝，颈可再压，右侧2像素余量。
- 蕾娜：rena/candidates/portrait_v2_maxcoverage_74x100_candidate.png。40多岁女记录员、米白头巾和深绿罩衣边保持；颈领收紧，克制愧意符合身份。MAXCOVERAGE比MEDIANCUT保住深绿衣色。左发轮廓在x=0、y=41/42仍有2像素触框，右侧余量1像素；安全边目标尚未完全达到。亮眼缝和条状发纹仍存。
- 罗安：roan/candidates/portrait_v2_maxcoverage_74x100_candidate.png。30多岁男装配匠、深短发厚须、赭衣棕围裙保持；v2怒V趋平压眉、脸更大颈更短，固执防备可辨。MAXCOVERAGE保住眼/衣色分层，但眼白仍偏亮，须发有细碎纹，右侧余量仅1像素。

各人均只有初稿和一次成功修订，没有第三稿。奥辛/佩兰v2最初一次六参考输入被参数校验拒绝，没有产图；改为v1加四核心的五参考调用后成功。失败参数和工具错误另存，未计为成功产图，也未隐去记录。

## 实际查看与判断依据

逐一阅读当前角色卡与适用规则、核对roster、查看四张历史身份母版和四个认可风格锚点；查看各v1/v2的1×及8×最近邻预览，最后查看独立1×/4×横向对比板。当前卡的年龄、服色优先于历史图。奥辛/罗安维持成年劳动者面骨；佩兰与蕾娜按新卡补足成熟年龄，分别采用自持和克制愧意，避免整批同款忧眉。

四张都保留紧脸方向、大块鼻颧明暗和有限服装边缘，没有增加工具、手、职业徽章或预演和解/签署/代表全城等剧情结果。仅蕾娜仍有明确左侧接框；不能因技术尺寸合格就说所有裁边要求已通过。

## 冻结后的独立技术审计

2026-10-15 09:29:40 UTC 后从作者已声明冻结的目录重新读取：

- 17项当前卡/选定母版/历史QA/历史manifest与campaign roster哈希一致。
- 39项作者来源快照与仓库原文件逐字节及SHA一致。
- 8份raw与完整工具返回base64解码字节一致；保留的工具原始PNG同样逐份比对。
- 12份候选由独立脚本从raw重建，像素和PNG文件字节均完全一致。脚本只做整画布NEAREST到74×100、alpha阈值128、可见RGB的32色MEDIANCUT或MAXCOVERAGE无抖动量化及透明RGB清零，不绘制角色几何。
- 全部候选均74×100、32可见RGB色、alpha仅0/255；透明RGB为零；8×预览为精确最近邻放大。
- 163项manifest文件记录、167项SHA256SUMS记录全匹配；选定SHA、generation_calls=2、文件集闭合及非原生/非运行边界全匹配。
- 冻结审计0错误、0待办。早期审计包含作者正在修订时的临时manifest陈旧状态，最终以frozen_technical_audit.json为准。

## 交付文件

- FINAL_SELECTION.json：终选路径、选定SHA、测量与逐人残留。
- frozen_technical_audit.json：来源、工具payload、独立复现、manifest和SHA明细。
- frozen_verification.json：冻结manifest、SHA清单与选图指纹及计数。
- selected_candidates_1x_4x.png：四人终选与四个风格锚点；只做最近邻展示，无角色编辑。
- comparison_manifest.json：对比板输入和输出指纹。
- INITIAL_VISUAL_REVIEW.md：初稿问题与一次集中修订记录。
- preflight_source_checks.json、review_basis.json：roster/风格依据。
- audit_batch08.py、finalize_review.py、build_comparison.py：独立复现与归档脚本。

本QA只写入independent_qa/batch08；没有改生产角色目录、旧资产、人物卡、代码或提交推送。美术生产下一阶段仍须人工逐像素处理眼白、发须簇、色阶及安全边，再做原生目标和游戏接入验收；本批没有自动进入该阶段。
