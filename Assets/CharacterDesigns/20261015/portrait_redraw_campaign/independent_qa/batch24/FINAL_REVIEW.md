# Batch24 独立肖像QA冻结结论

结论：莉葵、阿洛、昂朵为带限制的技术派生肖像候选；呼蕾held，不进入通过画廊。各人仅一次集中必要反馈、最多两份成功生图，没有第三次。

## 锁稿

- liqui: candidate_with_limits
  - 选稿：liqui/candidates/portrait_v2_inset_74x100_candidate.png
  - SHA256：b2b799491040e3edf06720bd87cd96db4b9f1bad5f340ac7b989c9657cffae90
- arlo: candidate_with_limits
  - 选稿：arlo/candidates/portrait_v2_inset_74x100_candidate.png
  - SHA256：534ab44e6cd93eb7d1d9b5ebe638d97e378f4f2c0a116027ebec76e02c853d84
- hure: held_composition_scale_and_eye_sclera
  - 选稿：无；仅保留held证据
  - SHA256：497f9a849278b3c88bb1ce5c2f9e337934d6c35cd22d5dae90817369bcb625b0
- ondo: candidate_with_limits
  - 选稿：ondo/candidates/portrait_v2_74x100_candidate.png
  - SHA256：c05334edfd54a2938e2e04afb448d34c35e8f625d89611e504f54615e19a6a2a

## 重要来源裁定

- 阿洛：最新人物卡明确20多岁、染缸蒸汽熏黄发，优先旧母图成熟灰须。v2落实年轻化并保宽钝鼻、蓝绿衣/棕围裙。
- 昂朵：旧卡与现卡正文第21行同一句“他”，母prompt明确adult man、实看母图男性；现卡第46行及总表第133行“她只评普通适用性”为同一S89/S91复制来源异常，不是两个独立身份重设证据。按已裁定成年男性和最新约50岁继续，不改卡。
- 呼蕾：初看切边说法已纠正。灰底实看轮廓闭合；v1/v2在alpha≥128下右侧真实余量6/7源px，最右列最大alpha仅1/4。74宽NN后触右边是余量不足，不写成已证实真实裁断。
- 呼蕾held主因构图与眼白：v2源1216×1293，目标alpha bbox[3,16,74,85]仅69px高，侧髻压低脸占比且双眼白仍亮。全保主体裁透明空白后，1159×1137包围框受宽度限制，最大约73px高，仍不适合当前大脸竖幅目标；不强行修复、不补像素、不拉伸。

## 独立技术验证

- 35份独立原路径/历史git来源快照，末次重新取值全SHA一致。母图、母QA、当前卡与四核心风格图实际查看。
- 8份成功raw逐字节等于完整工具回包；10份标准/inset派生逐字节复现。
- 所有派生74×100、≤32可见色、alpha仅0/255、透明RGB清零。1x、8x、三背景1x/4x预览逐字节复现，放大均整数NEAREST。
- 作者manifest全部文件SHA通过且无漏项：liqui55、arlo52、hure43、ondo49；作者SHA256SUMS对应56/53/44/50项全过。
- 脚本先读后独立实现复现，仅写本QA目录，不执行作者finalize、不改作者文件。

## 交付与限制

QA_summary.json 的 delivery_include 是三名可交付候选及预览清单；delivery_hold_evidence仅存呼蕾失败证据，不得混入通过画廊。selection_lock.json锁定SHA。selected_contact_4x_NN.png含显式HELD标签，仅供本批比较。

所有通过仅为Imagegen重绘后NN/减色/alpha技术派生候选。不是原生逐像素作者终稿，不是地图精灵，不代表已接入引擎或已实机验收。未改旧母图、人物卡、代码，未commit/push。
