# 雷奥·凯斯 / NPC-REY 对白头像候选

当前：独立视觉QA选v2 candidate，资产与元数据已冻结，待独立最终SHA/清单/RGBA复核；不等于用户最终认可。

- 目标与1×文件：candidates/portrait_v2_74x100_candidate.png
- 1×三底色与8×最近邻预览：previews/portrait_v2_1x_8x.png
- 独立8×：previews/portrait_v2_8x.png
- 原图：raw/portrait_v1_raw_imagegen.png 与 portrait_v2_raw_imagegen.png
- 完整生图返回：tool_returns/portrait_v1.json 与 portrait_v2.json
- 完整参数/最终提示词：prompts/portrait_v1.json 与 portrait_v2.json
- 身份/剧情/风格来源与SHA：sources/source_manifest.json；当前读取快照保存在sources/
- 作者目测：qa/author_visual_review.json；非独立结论
- 再现：python derive_portrait.py <本目录> portrait_v2；元数据封装：python finalize_manifest.py <本目录>

制作方式：built-in imagegen负责人物实质重绘；raw是高分辨率生成图（真实尺寸见metrics）。候选是Pillow NEAREST整张降到74×100、alpha≥128二值化、可见采样色MEDIANCUT≤32色且无抖动的派生图。两张v2实测各31可见RGB色。没有用代码绘制人物或手修像素。不能称原生逐像素制作、量化=美术验收或已接入游戏。本批32色上限为临时工作预算。每人已完成初稿+一次定向修订，保留旧版本作对照。

旧图、人物卡和实现代码未修改；未提交、未推送。
