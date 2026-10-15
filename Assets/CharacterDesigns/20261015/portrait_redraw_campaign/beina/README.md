# 蓓娜 / FOR-S02-NPC 肖像重绘

状态：独立QA允许带限制候选。每人已完成初稿+唯一必要修订，共两次实质 image_gen；不再第三次。

锁定候选：candidates/portrait_v2_inset_74x100_candidate.png
SHA256：9ee071b9643c6305e982e9d163c2035c07c6cbfc55c6009f541e238f0674d4de

保留40岁成熟质疑脸、蓝巾棕发灰罩衣锈内领。仍有忧眉、偏亮眼白、巾发平行细分和脸占比保守的局限。

来源与复核：sources/保最新人物卡、原母图、原母QA/manifest、四核心参考与剧情快照；source_manifest.json保原路径与SHA；qa/source_hash_recheck.json复查所有源未漂移。实际查看了母图、四核心、v1/v2 raw及1×、整数NN和三底色预览。详见spec_lock.md及qa/author_visual_review.json、qa/independent_review_acceptance.json。

完整生成留档：prompts/portrait_v1.json和portrait_v2.json为真实实参，配完整.txt；tool_returns/保两次完整回包；raw/从完整回包无损解码，字节一致校验见metrics。旧稿未覆盖。

技术导出：74×100透明RGBA、32临时可见色、alpha仅0/255。全raw画布等比NEAREST、MAXCOVERAGE无抖动、alpha阈值128；inset使用72×98容纳盒再居中。只有技术派生，无脚本画脸、几何变形或裁切。raw真余量单列qa/raw_silhouette_margins.json。不可声称原生逐像素终稿或游戏接入。

复现全部候选：
- python derive_portrait.py portrait_v1
- python derive_portrait.py portrait_v2
- python derive_portrait.py portrait_v2 inset
- python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations

qa/reproduction_verification.json验证保存raw可确定性重跑派生，图像生成本身不保证确定性重现。manifest和SHA256SUMS由脚本刷新。仅本目录写入，旧图、角色卡、代码与冻结索引不动，不commit/push。
