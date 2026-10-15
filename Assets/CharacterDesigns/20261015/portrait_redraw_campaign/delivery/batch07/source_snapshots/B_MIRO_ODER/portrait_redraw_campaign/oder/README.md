# 奥德头像重绘候选

本目录属于2026-10-15全体头像重绘batch07。已完成v1和唯一必要定向修订v2；独立实看已选v2为可交候选，生成预算用完并冻结，不再追加v3。

## 来源与身份

最新角色卡、实际查看的已选母版、旧独立QA及四个风格锚均在sources，原路径与SHA-256见sources/source_manifest.json。本轮最新文字卡优先。奥德准确ID为BRY-NPC-ODER，五十余岁的靠泊席位船主；采用latest_card_alignment_v1母版，不混同欧达或工艺人。左手缺半截小指在头像外，不作已核验声明。

## 文件与复现

- prompts/portrait_vN.json：实际内置imagegen调用的完整参数和提示词。
- tool_returns/portrait_vN.json：完整返回，含原图data URL。
- raw/portrait_vN_raw_imagegen.png：从返回无损解码的原始PNG。
- candidates/portrait_vN_74x100_candidate.png：整张画布Pillow NEAREST到74×100，MEDIANCUT 32色上限，无抖动，alpha阈值128，透明RGB置零。
- previews/：真实1x、8x整数最近邻及四个核心风格锚对照；预览背景不进入透明PNG。
- qa/：技术统计、作者/独立实看结果、来源检查与复现验证。
- manifest.json与SHA256SUMS.txt：选稿和文件哈希。

复现导出：python derive_portrait.py。重建清单：python finalize_manifest.py portrait_v2。要求Python3和Pillow，版本记录在manifest。imagegen本身不承诺字节确定性；完整工具返回保证可重现当前派生品。

## 限制

74×100为明示NN缩放与量化派生候选，不是原生网格绘制终稿，数值过关不代表审美或用户认可。本批32色仅临时上限；尚未导入游戏、验证装备或运行。旧图、旧QA、角色卡和代码均不覆盖；未commit/push。

## 本轮修订

v1独审要求收紧脸部构图、压短颈领；米罗另需减轻严虑，增强礼貌眼笑与成熟周正脸；奥德保留身份神态，仅收颈与组织发须块。v2完整保留。另有一次引用图数量超过5的参数校验失败，没有生成图片，记录单列，不计为第三张作品。

## 冻结选稿

选稿：candidates/portrait_v2_74x100_candidate.png。独立结论摘要见qa/independent_selection_summary.json，正式入口为上级independent_qa/batch07/FINAL_SELECTION.json与technical_audit.json。保留原始v1/v2及全部参数。非阻断备注：奥德胡须仍有少量细条。
