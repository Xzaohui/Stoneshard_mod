# 罗安 / BRY-NPC-ROAN

候选 v2：`candidates/portrait_v2_maxcoverage_74x100_candidate.png`，74×100，32临时色，二值 alpha。独立 QA 定级：selected_candidate_with_limitations。

实际 imagegen 初稿＋一次必要修订，完整 prompt / tool return / raw / 来源 SHA / 导出脚本 / 1x和8x检查图均归档。`python derive_portrait.py`、`python export_maxcoverage.py portrait_v1`、`python export_maxcoverage.py portrait_v2`、`python finalize_manifest.py portrait_v2_maxcoverage` 可复现派生与清单。非原生逐像素终稿，未入运行时，不替换旧图。

v2改善短颈/窄领与眉势，但局部眼白偏亮及安全边偏窄仍保留限制；不以技术32色证明审美终审。

具体残留：
- Eye-white blocks remain brighter than requested.
- Some fine beard/hair texture remains rather than only broad unified clusters.
- Right silhouette has only one pixel of transparent clearance.
