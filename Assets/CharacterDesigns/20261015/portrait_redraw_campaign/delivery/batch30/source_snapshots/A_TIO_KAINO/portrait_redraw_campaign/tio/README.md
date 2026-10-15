# 提奥·桶 / MNS-NPC-TIO

选用 v2_inset 带限制派生候选，可进入本批候选交付。

- 成功实质 image_gen 2 次（初稿＋唯一修订），停止，不出第三张。
- 当前图：candidates/portrait_v2_inset_74x100_candidate.png
- 二十多岁无须青年，栗棕乱短发、橄榄衫浅围裙可辨；第二次生图真正补回左右发轮廓，源层四边不再裁断。眼白较初稿缩小，鼻颧块面成立。
- 颈仍略长。
- 头发细线仍多于四核心风格。
- 同raw 72×98等比NN containment只建立2px成品边距，不是绘图修复或原生像素终稿。

## 技术和来源

74×100 RGBA，≤32可见RGB临时色，alpha仅0/255。全幅等比NEAREST缩放，透明阈值128、MAXCOVERAGE无抖动量化；不脚本绘制/变形脸或补头发。技术派生非原生逐像素终稿，未进游戏且未运行验收。

完整实际prompt/参数在prompts/，完整工具回包含image_url在tool_returns/，raw与回包逐字节相同；source_manifest存最新卡/母图/母QA/四核心/相关台本及来源SHA。1x/4x背景/8x整数预览在previews/。源卡相对旧历史有新增外观字段，已在spec_lock与source_manifest记优先规则。旧图、卡、代码与索引均未改；不commit/push。

## 复现

python derive_portrait.py portrait_v2 inset
python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations

qa/reproduction_check.json记录重跑候选逐字节一致；qa/source_hash_recheck.json验证当前来源与快照。SHA256SUMS覆盖本目录所有其他文件，manifest中列文件SHA。

另一次6参考图请求被工具参数校验立即拒绝，未生成图；完整请求与原错误在portrait_v2_rejected_request文件中，随后5参考图成功。成功生图仍是2次，API调用尝试为3次。
