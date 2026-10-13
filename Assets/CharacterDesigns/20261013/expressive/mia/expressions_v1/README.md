# 米娅 · 三表情胸上概念

本组只新增3张表情，不增加人物人数，不改批准正面或已过审turnaround。当前状态：独审通过（pass_expression_concepts_with_notes），root已实看比较板通过；尚未记录实际上传或用户认可。manifest与作者QA保持独审时原字节，属于审查前快照；最新结论见QA-independent.json及FINAL_STATUS.json。

- 关切询问：内眉抬起、微开口，保留疲惫的半垂眼睑。
- 认真倾听：眉眼集中、嘴闭合，不以怒意取代专注。
- 温和鼓励：闭口浅笑，谨慎表达关怀，不暗示米娅康复、成为护理者或任务完成。

## 产物

- `raw/`：3次builtin image_gen原稿，1254×1254 RGBA，逐张生成，每张一次，无定点重绘。
- `prompts/`：3份实际生成提示词。询问只引用批准正面；另两张引用批准正面为身份锚、询问图为统一构图参考。
- `mia_*.png`：3张统一860×1075透明胸上单图。
- `mia_expressions_review_zh.png`：1600×950中文比较板。
- `manifest.json` / `sourcehash.json` / `QA.json`：来源、哈希、尺寸、作者自查和限制。
- `build_review.py`：可复现裁切和比较板。只将alpha≤5近透明噪点设为0，统一裁切[190,65,1050,1140]，全组共同0.55最近邻排版（整数目标473×591）；未直接绘制或修改五官，未调色量化。

基准：`../ratio_1_to_1_5/mia_ratio_1_to_1_5_v2_raw_imagegen.png`，SHA256 `3f2060ae7a0e1694995540c51160fd515a72c8013e548d2e9313cee857d493fd`。实际查看批准正面、turnaround比较板、源卡与既有QA。新图轻微头发/服褶色簇漂移如实保留，不冒充逐帧对齐、原生精灵或引擎验证。
