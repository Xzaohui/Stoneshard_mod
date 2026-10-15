# 枯恩（ASH-NPC-KUEN）肖像重绘候选

当前候选：`candidates/portrait_v2_inset_74x100_candidate.png`。独审已锁定为可交付、带限制的技术派生候选。

## 来源与范围

- 最新角色卡、母图、母QA、母manifest、相关剧情与四核心参照均已读取；身份母图与四参考已实际查看。源文件快照、SHA及复核见 `sources/source_manifest.json` 与 `qa/source_hash_recheck.json`。
- 内建 image_gen 实质重绘两次：v1初稿、v2唯一必要修订；不做第三次。完整实参/完整提示词位于 `prompts/`，完整工具回包位于 `tool_returns/`，原字节图位于 `raw/`。
- 原始v2图已经具备完整发耳真实透明边距；alpha多阈值边缘检测见 `qa/raw_containment_metrics.json`。

## 候选规格

74×100 RGBA，32种可见临时工作色，alpha仅0/255。`inset` 为同一v2原图整画布等比NEAREST缩入72×98再置于74×100、阈值alpha≥128和MAXCOVERAGE无抖动量化；没有画脸、改五官或拉伸。full/inset都是技术派生，绝非原生像素终稿。

原图、full和inset均保留。1×、整数8×NN、多底1×/4×预览在 `previews/`。

## 视觉限制

- 大脸、短颈、窄披肩领相较v1已实质改善。
- 三十多岁成年男性、棕乱发、稀胡茬、病号灰蓝内领及灰褐厚披肩身份保持。
- 眼白仍偏亮，内眉略忧，脸/胡茬仍有细碎簇；不声称已解决。

不表示原生像素批准、游戏集成、运行验收、痊愈、研究同意、迁居或已接班。不改旧图、角色卡、代码或冻结索引，不commit/push。

## 复现

`python derive_portrait.py portrait_v1`

`python derive_portrait.py portrait_v2`

`python derive_portrait.py portrait_v2 inset`

技术指标在 `qa/portrait*_metrics.json`，最终文件绑定见 `manifest.json` 与 `SHA256SUMS`。

选定SHA256：`f5789504824665242a16f5a30ce6bf533168a0b6146dccec3d72449aed2c68c8`。
