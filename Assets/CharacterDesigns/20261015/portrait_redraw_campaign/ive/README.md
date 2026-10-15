# 伊芙 / Ive 74×100 头像候选

独立视觉QA：candidate_pass_with_notes。选用portrait_v2_mediancut，已冻结；完成首稿和唯一一次必要修订，共2次内置imagegen调用。不追加生图。

## 文件入口
- 身份：BRY-NPC-IVE
- 选用：`candidates/portrait_v2_mediancut_74x100_candidate.png`
- 原尺寸＋整数8× nearest预览：`previews/portrait_v2_mediancut_1x_8x.png`
- raw：`raw/portrait_v2_raw_imagegen.png`
- 两次实际参数：`prompts/portrait_v1.json`、`prompts/portrait_v2.json`
- 完整工具返回：`tool_returns/portrait_v1.json`、`tool_returns/portrait_v2.json`
- 先前未执行草案保留为`prompts/portrait_v2_proposed_not_executed.json`，实际执行的是另存v2参数
- 调用、输入、raw与返回SHA：`qa/generation_ledger.json`
- 独立取舍：`qa/independent_selection_summary.json`；当前选择：`selection.json`
- 来源快照／哈希：`sources/source_manifest.json`；未变校验：`qa/source_preservation.json`
- 派生逐字节复现核验：`qa/reproducibility.json`

## 身份与现卡
二十多岁女性，深棕发夹灰缕与低侧辫、棕两圈围巾／炭衣。保年轻成人脸；灰缕不等于老年。低平紧眉与侧目表达安静持续怒意；陶灯与门牌不入紧脸裁幅，不演和解或复仇。

## 保留问题
- 灰缕与眼白仍稍亮。
- 围巾带仍略厚。

## 生产口径
内置imagegen实际绘画；保存高分辨率raw、完整toolreturn和所有参数。整画布nearest缩到74×100，alpha阈值128，可见采样RGB建立Pillow MEDIANCUT调色板，无抖动映射至最多32色、透明像素归零。未裁切、补画、变形或重绘像素几何。

另存同v2 raw的MEDIANCUT无抖动机械导出，以减少MAXCOVERAGE产生的额头碎色岛；无新增生图或补画。

这是从生成raw机械派生的概念候选，不是native_final、原生逐像素手工稿、用户审美终审或游戏运行验收。32色是本批临时上限，不是全项目硬限制。

## 复现
在仓库根执行`python Assets/CharacterDesigns/20261015/portrait_redraw_campaign/ive/derive_portrait.py Assets/CharacterDesigns/20261015/portrait_redraw_campaign/ive portrait_v2`。然后执行同目录`export_v2_mediancut.py`。最后执行同目录`finalize_manifest.py`，从selection.json恢复已冻结选择与完整索引。所有已存raw到候选均已逐字节复核。生图本身不承诺确定性复现。

旧v1完整保留，旧母版／人物卡／台本／代码未改，未提交或push。
