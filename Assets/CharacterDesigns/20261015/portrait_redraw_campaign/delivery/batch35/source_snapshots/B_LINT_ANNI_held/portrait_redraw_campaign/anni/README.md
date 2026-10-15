# 安妮 / ASH-NPC-ANNI 肖像重绘

状态：暂挂风格，不列选稿、不进入可交付候选计数。每人已完成初稿+唯一必要修订，共两次实质 image_gen；不再第三次。

无选定稿。仅作暂挂证据：candidates/portrait_v2_inset_74x100_candidate.png
SHA256：1e16522451cd110f00dfd96e835ffca630ecc55ce19f8973102ffcf377471125

V1右发被实际raw边界截断，V2已通过生成重绘补全；仍因大亮眼白、上眼线妆感和小鼻甜脸占主导暂挂。技术合格不抵消风格失败。

来源与复核：sources/保最新人物卡、原母图、原母QA/manifest、四核心参考与剧情快照；source_manifest.json保原路径与SHA；qa/source_hash_recheck.json复查所有源未漂移。实际查看了母图、四核心、v1/v2 raw及1×、整数NN和三底色预览。详见spec_lock.md及qa/author_visual_review.json、qa/independent_review_acceptance.json。

完整生成留档：prompts/portrait_v1.json和portrait_v2.json为真实实参，配完整.txt；tool_returns/保两次完整回包；raw/从完整回包无损解码，字节一致校验见metrics。旧稿未覆盖。

技术导出：74×100透明RGBA、32临时可见色、alpha仅0/255。全raw画布等比NEAREST、MAXCOVERAGE无抖动、alpha阈值128；inset使用72×98容纳盒再居中。只有技术派生，无脚本画脸、几何变形或裁切。raw真余量单列qa/raw_silhouette_margins.json。不可声称原生逐像素终稿或游戏接入。

复现全部候选：
- python derive_portrait.py portrait_v1
- python derive_portrait.py portrait_v2
- python derive_portrait.py portrait_v2 inset
- python finalize_manifest.py portrait_v2_inset held_not_delivery_eligible

qa/reproduction_verification.json验证保存raw可确定性重跑派生，图像生成本身不保证确定性重现。manifest和SHA256SUMS由脚本刷新。仅本目录写入，旧图、角色卡、代码与冻结索引不动，不commit/push。
