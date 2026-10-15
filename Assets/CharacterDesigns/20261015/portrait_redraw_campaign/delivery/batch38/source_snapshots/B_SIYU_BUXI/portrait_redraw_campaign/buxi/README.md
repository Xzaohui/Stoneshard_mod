# 布希：74×100 肖像重绘候选

本轮以 built-in image_gen 实质重绘，初稿加一次集中反馈修订，共两次。独立终审选择V2：`candidates/portrait_v2_74x100_candidate.png`。

四十岁上下女性，审慎估量的窄眼、窄长椭圆脸与颧骨、微方下巴、中分低髻；鼻粉与蓝衣/米白领/棕围裙肩带。

原母图、最新角色卡、剧情与四核心参考已实际阅读/查看，来源与 SHA 在 `sources/source_manifest.json`；布希代词歧义调查另见 `qa/identity_reconciliation.json`。现卡外观更新优先，源文件未修改。

完整 prompt 和实际参数：`prompts/portrait_v1.json`、`portrait_v2.json`；完整回包：`tool_returns/`；原始未修改图：`raw/`；74×100 候选、1x、4x 三底及8x整数NN预览分别在 `candidates/`、`previews/`。

## 派生与复现

`python derive_portrait.py portrait_v1`

`python derive_portrait.py portrait_v2`

`python finalize_manifest.py portrait_v2 selected_candidate_with_limitations`

整张raw等比NEAREST缩至74×100画布，alpha阈值128，MAXCOVERAGE无抖动≤32可见色；没有脚本画脸、局部变形或修补。`qa/portrait_v*_metrics.json`验证尺寸/临时色数/二值alpha/回包字节。生成本身非确定性；保存raw后的派生可逐字节复现。

这是带限制的技术派生候选，不是原生逐像素终稿。仍有浅眼白和细簇风格限制，未游戏接入/验收。旧图、角色卡、代码、冻结索引未改；不commit/push。
