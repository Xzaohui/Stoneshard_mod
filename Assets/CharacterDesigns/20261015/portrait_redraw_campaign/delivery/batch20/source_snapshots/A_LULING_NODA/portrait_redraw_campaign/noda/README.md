# 诺妲·门／KOR-NPC-NOD 头像重绘候选

独立QA结论：pass_concept_with_notes。选择 candidates/portrait_v2_74x100_candidate.png。

- 实质绘制：内置 image_gen，初稿+唯一一次集中反馈修订，各2张生成raw。参数超5参考图的请求在校验层被拒，未生成额外图。
- 最终候选：74×100 RGBA，32个可见RGB色，alpha仅0/255；选定SHA256：499af7c3c1543222b2d3ba6bdabaf096a71783a9598ff41893e60ba6ba86eab5。
- 同v2 raw的inset仅留作等比技术采样备选；独审选择full以保面部采样。
- 原卡、母图、旧资源及索引不改；未提交、推送或接入游戏。

## 实看与限制

- 40+成熟宽颊、宽鼻低髻、深灰罩衣领与谨慎抿嘴成立。
- v2短颈窄领明显改善，完整髻与耳轮廓可读。
- raw bbox(34,102,1068,1379)，alpha≥128四边均0，完整源轮廓不是padding遮裁边。
- 残余：眼白仍亮、发丝条纹细、内眉仍微忧；不作为原生逐像素终稿。

NN整图等比containment、调色板量化与alpha阈值只是技术派生，没有脚本重画脸。此概念候选不是原生逐像素终稿，暂定32色上限也不是原生验收；runtime未验证。

## 追溯与复现

完整原始tool return与raw、prompt文本及参数、来源快照与SHA、作者及独立QA、1x及整数倍预览均在本目录。来源快照完成末次hash复核。tool_return_integrity另外核对完整原始image_url的长度与CRC32、原始output_hint及解码PNG逐字节一致。

从本目录执行：

python derive_portrait.py portrait_v1
python derive_portrait.py portrait_v2
python derive_portrait.py portrait_v2 inset
python finalize_manifest.py portrait_v2 pass_concept_with_notes

完整SHA256SUMS覆盖清单与全部文件。身份与最新卡衣装更新详见spec_lock.md。
