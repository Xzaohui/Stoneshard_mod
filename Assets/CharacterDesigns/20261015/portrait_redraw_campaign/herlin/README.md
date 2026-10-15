# 赫林 / Herlin 74×100 头像候选

独立视觉QA：candidate_pass_with_notes。选用portrait_v2，已冻结；完成首稿和唯一一次必要修订，共2次内置imagegen调用。不追加生图。

## 文件入口
- 身份：BRY-NPC-HERLIN
- 选用：`candidates/portrait_v2_74x100_candidate.png`
- 原尺寸＋整数8× nearest预览：`previews/portrait_v2_1x_8x.png`
- raw：`raw/portrait_v2_raw_imagegen.png`
- 两次实际参数：`prompts/portrait_v1.json`、`prompts/portrait_v2.json`
- 完整工具返回：`tool_returns/portrait_v1.json`、`tool_returns/portrait_v2.json`
- 先前未执行草案保留为`prompts/portrait_v2_proposed_not_executed.json`，实际执行的是另存v2参数
- 调用、输入、raw与返回SHA：`qa/generation_ledger.json`
- 独立取舍：`qa/independent_selection_summary.json`；当前选择：`selection.json`
- 来源快照／哈希：`sources/source_manifest.json`；未变校验：`qa/source_preservation.json`
- 派生逐字节复现核验：`qa/reproducibility.json`

## 身份与现卡
男性四十上下修铆工，削瘦角脸、灰黑短发、短胡茬。旧母版红衫与最新人物卡蓝灰短衫有冲突，本轮依最新卡改为蓝灰窄领＋棕皮围裙边。左耳小缺口仅弱可读，未伪称明确关闭。

## 保留问题
- 左耳缺口在raw可见，但74×100弱可读，不能声明明确关闭。
- 胡茬与边发仍偏细。

## 生产口径
内置imagegen实际绘画；保存高分辨率raw、完整toolreturn和所有参数。整画布nearest缩到74×100，alpha阈值128，可见采样RGB建立Pillow MAXCOVERAGE调色板，无抖动映射至最多32色、透明像素归零。未裁切、补画、变形或重绘像素几何。

这是从生成raw机械派生的概念候选，不是native_final、原生逐像素手工稿、用户审美终审或游戏运行验收。32色是本批临时上限，不是全项目硬限制。

## 复现
在仓库根执行`python Assets/CharacterDesigns/20261015/portrait_redraw_campaign/herlin/derive_portrait.py Assets/CharacterDesigns/20261015/portrait_redraw_campaign/herlin portrait_v2`。最后执行同目录`finalize_manifest.py`，从selection.json恢复已冻结选择与完整索引。所有已存raw到候选均已逐字节复核。生图本身不承诺确定性复现。

旧v1完整保留，旧母版／人物卡／台本／代码未改，未提交或push。
