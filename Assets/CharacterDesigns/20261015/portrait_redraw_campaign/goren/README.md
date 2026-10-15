# 古烈（SKO-NPC-GOREN）对话肖像候选

## 当前选稿

- 选用：`candidates/portrait_v2_74x100_candidate.png`
- SHA256：`e084b4fc8a5914c9617f5b8781e5cc71cf2448139be99d86df71ebcba437fbc1`
- 74×100 RGBA；32个可见RGB颜色；alpha仅0/255。
- 两次成功image_gen：初稿与独立QA集中反馈后的唯一修订。预检失败1次，未产生图片；不再生成第三稿。
- 独立QA：带限制候选可冻结，见`qa/independent_review_acceptance.json`。

## 来源与身份

当前人物卡、选定母图/母QA/manifest、三篇剧情人物段、Mara/Iwo/Leiya/Tore四核心参照均已核对与实际看图。完整来源快照及SHA见`sources/source_manifest.json`，外观差异取舍见`spec_lock.md`。结尾重查全部来源哈希未变。

## 限制

残余发胡碎点、少量浅眼簇、发冠偏大；原始右侧9px余量窄，但独立实看发耳完整且未裁。

这是image_gen实质重绘后，经整张画布等比NEAREST containment、alpha128二值化、MAXCOVERAGE最多32色且无抖动的技术派生候选。未用脚本绘脸、局部重画或变形；未做inset。32色为临时工作上限，不证明原生像素质量；不是原生作者终稿，也未接入或验证游戏。旧图、旧卡、代码与冻结索引未改，无commit/push。

## 复现与审计

1. `python derive_portrait.py portrait_v1`
2. `python derive_portrait.py portrait_v2`
3. `python finalize_manifest.py portrait_v2 selected_candidate_with_limitations`
4. `sha256sum -c SHA256SUMS`

完整实参/纯文本提示词在`prompts/`；完整tool回包在`tool_returns/`，解码原图在`raw/`；两次技术派生重跑逐字节一致见`qa/reproduction_check.json`。图像生成本身不声称可重复出相同像素。原始alpha边缘只读核验见`qa/silhouette_edge_audit.json`，1x与整数NN放大、深灰/中灰/浅色底预览均在`previews/`。
