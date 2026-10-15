# 卢绫 / KOR-NPC-LULING 肖像重绘候选

选择：`candidates/portrait_v2_safe_74x100_candidate.png`。独立 QA20 结论 `pass_concept_with_notes`。初稿加一次必要修订，共2次实质 imagegen；另一次输入参数数量校验在生图前失败，详见qa记录，不计作生成。未进行第三次。

短颈窄领、大脸成熟宽颌改善，保浅巾深发；现卡深色外褂与暖赭内衬已对齐。残余：亮眼白、强眉间折、发巾平行细条；raw右仅3px但轮廓完整、四边alpha128均清。

74×100 RGBA，32个临时可见色，alpha0/255。safe从完整v2 raw等比NEAREST缩入70×96框再居中，目标bbox[3,5,72,94]。无抖动MAXCOVERAGE量化、alpha128及containment均只是技术派生，不代表原生逐像素终稿，也没有修复或伪造源图内容。

复现：`python derive_portrait.py portrait_v2 safe`；`python finalize_manifest.py portrait_v2_safe pass_concept_with_notes`。全部prompt/参数/完整返回/raw/sourceSHA/重放及1x与整数预览已保留，重放字节一致。源卡、旧素材、代码、索引不变；未commit/push，未集成或运行验收。
