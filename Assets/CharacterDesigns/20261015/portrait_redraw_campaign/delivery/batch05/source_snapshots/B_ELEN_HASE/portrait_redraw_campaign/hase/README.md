# hase 头像重绘候选

当前候选：`candidates/portrait_v1_74x100_candidate.png`。独立QA候选级通过（含限制），冻结v1；不是用户终审或原生像素验收。

- 实质绘图：内建 imagegen，原始完整结果见 `tool_returns/portrait_v1.json`，原始PNG见 `raw/`。
- 导出：整画布NEAREST到74×100；alpha阈值128；MEDIANCUT可见色32色临时上限，无抖动；透明RGB归零。
- 这是高分辨率imagegen原稿的NN/量化派生，不是原生74×100逐像素绘制；色数达标不代替造型和审美验收。
- 复现：在已装Pillow的Python环境运行 `python derive_portrait.py portrait_v1`。PNG导出无需重新生图。
- 预览：`previews/portrait_v1_1x_8x.png` 含三底色1x和整数8x，四核心参考为整数2x。
- 身份与来源：`sources/source_manifest.json`、`sources/roster_entry.json`、`spec_lock.md`，含源卡/母版/旧QA/场景台本及SHA。
- 最多2次imagegen，初稿及一次必要修订；当前只用初稿，独审认为无需修订。
- 仅新增此角色目录，不改人物卡、旧图、游戏代码；未提交、未push、未集成运行。
