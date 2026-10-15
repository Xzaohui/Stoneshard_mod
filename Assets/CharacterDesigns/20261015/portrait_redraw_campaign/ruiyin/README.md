# ruiyin 肖像重绘：冻结待修订稿

v1 已实质 imagegen 生成并完成技术派生。集中 QA 要求一次必要修订；v2 提示词已准备，但未发起调用。因用户要求合并推送当前变更而停止新增生图，本包冻结为 `draft_needs_revision_frozen_for_publication`。无正在运行的生成。

无通过终审的 selected portrait，`delivery_eligible=false`。保留的 v1 草稿：`candidates/portrait_v1_74x100_candidate.png`；它不是已通过终稿。一次必要修订额度尚未使用。

完整 prompt 实参、完整工具回包、逐字节相同 raw、来源 SHA、1x 与整数 NN 多底预览、技术指标和集中反馈均已保存。`prompts/portrait_v2.*` 仅为未执行计划，执行记录见 `qa/generation_execution_ledger.json`。

复现 v1：`python derive_portrait.py portrait_v1`；随后 `python finalize_manifest.py portrait_v1 draft_needs_revision_frozen_for_publication`。Python 3.12.14 / Pillow 12.3.0。

NN 等比 containment、二值 alpha 和 ≤32 色仅是技术派生，非原生像素终稿或运行验收。没有脚本绘脸、旧图/卡/代码/冻结索引改写、commit 或 push。
