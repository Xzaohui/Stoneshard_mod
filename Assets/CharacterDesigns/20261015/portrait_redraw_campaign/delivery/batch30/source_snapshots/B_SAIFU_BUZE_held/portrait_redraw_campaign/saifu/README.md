# 赛芙 / MNS-S01-NPC

暂挂（held_after_two_generations），v2仅作为未通过的审查证据；delivery_eligible=false。两稿均不计本轮紧脸达标交付。

- 成功实质 image_gen 2 次（初稿＋唯一修订），停止，不出第三张。
- 暂挂证据（selected=null）：candidates/portrait_v2_74x100_candidate.png
- 三十多岁试种人的短暗发/素锈红巾/蓝衣棕围裙可辨，无源层裁断；最新卡较浅肤色意图只部分达成。
- v2顶部空白减少，但裸颈、肩胸与衣领反而扩大，紧脸短颈未达标。
- 眼白仍偏亮，内侧抬眉仍显忧惧，谨慎自尊未充分传达。
- 肤色仍偏暖橙，未充分落实中性偏浅肤色。
- v1脸占幅不足且仍有眼白/暖色问题，不能回选掩盖未达标。

## 技术和来源

74×100 RGBA，≤32可见RGB临时色，alpha仅0/255。全幅等比NEAREST缩放，透明阈值128、MAXCOVERAGE无抖动量化；不脚本绘制/变形脸或补头发。技术派生非原生逐像素终稿，未进游戏且未运行验收。

完整实际prompt/参数在prompts/，完整工具回包含image_url在tool_returns/，raw与回包逐字节相同；source_manifest存最新卡/母图/母QA/四核心/相关台本及来源SHA。1x/4x背景/8x整数预览在previews/。源卡相对旧历史有新增外观字段，已在spec_lock与source_manifest记优先规则。旧图、卡、代码与索引均未改；不commit/push。

## 复现

python derive_portrait.py portrait_v2
python finalize_manifest.py portrait_v2 held_after_two_generations

qa/reproduction_check.json记录重跑候选逐字节一致；qa/source_hash_recheck.json验证当前来源与快照。SHA256SUMS覆盖本目录所有其他文件，manifest中列文件SHA。
