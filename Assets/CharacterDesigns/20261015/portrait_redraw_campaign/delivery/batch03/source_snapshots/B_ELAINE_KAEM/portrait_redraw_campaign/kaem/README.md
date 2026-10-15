# 凯姆（MAE-NPC-KAEM；NPC-N-KAEM同人别名）｜74×100头像重绘候选

最终候选：`candidates/portrait_v2_74x100_candidate.png`。独立视觉QA选择v2 MEDIANCUT，通过概念候选并保留非阻断余项。

## 身份与来源

现行人物卡与台词优先于旧母版。完整源快照与SHA见`sources/source_manifest.json`。原图和人物卡均未修改。四张风格参照为Mara v2、Ivo v1、Leiya v2 maxcoverage、Tor v1；只承接硬边大块与紧脸构图，不复制其人物身份或忧眉表情。

凯姆为同一四十多岁男性副馆员，按现卡明确早花白发与轻微前探姿态；旧侧分、轻胡茬、炭灰米领仍沿用。旧母版偏年轻全棕发已被当前卡的年龄/灰发设定取代，不是新增人物或复权剧情。

## 生成与派生，不能混称

- 采用内置imagegen实质重绘：v1初稿，v2唯一必要修订；每人共2次调用，未使用CLI fallback。
- `prompts/`含每次完整prompt与实际参数；`tool_returns/`保留完整返回JSON，`raw/`逐字节解码保存返回图像。
- 生成raw约1079×1458（伊莲v2为1079×1457），并非原生74×100逐像素绘制。
- 导出使用Pillow 12.3.0整幅NEAREST缩到74×100，无裁切；alpha>=128转255、否则0。可见RGB样本建MEDIANCUT 32色palette，无抖动，全RGB映射至palette，透明像素RGB清零。脚本：`derive_portrait.py`。
- v1另留MAXCOVERAGE比较稿，它保米领/眼白但肤面碎阶梯较多；v2选MEDIANCUT。32是本批临时上限，不代表全项目最终色板已锁定。
- `previews/portrait_v2_8x.png`为严格8×整数最近邻放大；`previews/portrait_v2_1x_8x.png`含三底色1x和8x对照，供实际视觉检查。

## QA边界

技术统计见`qa/*_metrics.json`，作者视觉记录见`qa/author_visual_review.json`。独立选择摘要见`qa/independent_selection_summary.json`；独立原始报告在本批统一QA目录由审核者维护。尺寸、色数、alpha通过不等于审美原生像素验收。未接入运行时、未验证引擎、未提交或推送、未替换旧图或人物卡。
