# 赫珀（HIG-S01-NPC）肖像重绘

最终选择：candidates/portrait_v2_inset_74x100_candidate.png

SHA256：a95180b96ffa8cdae43fdfa4b4b42e0bb5d338fdc00b2c71ce7e08894df088be

状态：batch38独立终审允许有注记交付的NN技术派生候选。初稿与唯一imagegen修订全部留存，不再第三次生成。

## 来源与交付

- sources：最新独立人物卡、选定母图、母QA/manifest、当前剧情、Mara/Iwo/Leiya/Tore四核心参照；全部实读/实看，保留快照与源SHA。
- prompts：完整实参JSON及提示词；tool_returns：完整回包。两次成功产图，另一次6引用图的生图前参数校验拒绝无产图，改为草稿+四核心5图后成功；错误及原实参均保留。
- raw：完整回包的原始图像字节；candidates：74×100、32临时可见色、alpha0/255。
- previews：1x和4x/8x整数NN预览及浅/灰/深底。
- qa：作者目检、集中初审/终审反馈、来源复核、派生技术指标及独立源边缘证据。

## 边界与限制

二稿raw主轮廓完整，独立QA实看右缘3x浅深合成并多阈值核边确认真余量。直接74×100 NN采样贴边，不等于母图裁断；同raw全画布等比入72×98再置74×100的inset派生给出最终网格余量，未裁发耳、未脚本绘脸。

赫珀眼白仍偏亮、绿披和颈部仍比核心参照稍多，胡发簇仍有细碎。

NN/containment、alpha阈值与无抖动量化仅技术处理；不是原生像素手工终稿，不声明原生像素批准、代码接入或实机通过。未改旧母图/旧卡/代码/冻结索引，未commit/push。

## 复现

python derive_portrait.py portrait_v2 inset

python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations
