# 奥娅 / ASH-S02-NPC 肖像重绘保留证据

最终gate：`held_composition_scale_and_eye_sclera`。`delivery_eligible=false`，`selected_portrait=null`、`selected_sha256=null`，不进入通过肖像画廊。

保留证据：`candidates/portrait_v2_74x100_candidate.png`，SHA256 `2ce259d0b712ab6848fcca0222f7112d5e6086c89ef88277744d0183463bacc9`。raw：`raw/portrait_v2_raw_imagegen.png`。初稿＋唯一必要修订共2次内置imagegen已结束，不第三次生成、不再派生。

独立QA初步pass以相对v1改善判断过宽；随后与呼蕾/溪悠/梅蓓held案例同尺度复核，最终纠正为held。头领主体仅72px高，脸焦点偏小，浅眼白仍显著；收颈窄领和面部减皱/整块改善不足以跨过同一门槛。对比板：`../independent_qa/batch36/comparison_with_held_gate_4x_NN.png`；独立终审：`../independent_qa/batch36/oya_final_visual_review.json`。

技术检查通过不等于视觉通过：74×100 RGBA、32个可见临时色、alpha仅0/255，raw与完整回包逐字节一致。整图等比NEAREST containment、无抖动MAXCOVERAGE限色、alpha128阈值仅技术派生，不是原生逐像素终稿。源发耳/结髻完整，无证实裁断，不以padding补画轮廓。

其余限制：头巾/发束仍细，v2近方raw导致上下较空。厚围裙只在小领边可见，未验收全身围裙或卷袖。 未集成游戏、未实机或装备兼容性验收。

初/修两版原图、prompt实际参数、完整工具回包、源卡/母图/母QA/剧情/四核心快照及源SHA全部保留。最新卡三十多岁与外观要求优先，已记录差异；身份未被剧情结局替代。

预览（只作held证据）：`previews/portrait_v2_1x.png`、`portrait_v2_8x.png`、`portrait_v2_1x_backgrounds.png`、`portrait_v2_4x_backgrounds.png`。

复现方法（已核两版哈希一致，无需继续派生）：`python derive_portrait.py portrait_v2`；清单复现：`python finalize_manifest.py portrait_v2 held_composition_scale_and_eye_sclera`。见 `qa/generation_provenance.json`、`qa/author_visual_review.json`、`qa/independent_review_acceptance.json`。

原图、角色卡、代码和冻结索引不变；未commit/push。
