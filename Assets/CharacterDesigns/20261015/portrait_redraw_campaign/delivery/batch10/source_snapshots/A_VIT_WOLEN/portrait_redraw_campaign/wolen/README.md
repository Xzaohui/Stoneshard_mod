# 沃伦 / Wolen portrait redraw

独立QA选择v2：candidate pass with notes。不是原生逐像素终稿或游戏内验收。

- 角色ID：BRY-NPC-WOLEN
- 已选：candidates/portrait_v2_74x100_candidate.png
- 原始绘制：built-in imagegen各初稿和一次必要修订。完整参数在prompts，完整工具返回在tool_returns，未改原图在raw。
- 派生：74×100 whole-canvas NEAREST + MEDIANCUT最多32色无抖动 + alpha阈值128；透明像素RGB归零，不画改人物几何。
- 对照：previews/portrait_v2_1x_8x.png，含1x深/灰/亮底与整数8x最近邻及四核心2x参考。
- 来源：sources/source_manifest.json记录源路径、快照、SHA；qa/source_hash_verification.json核现源与快照一致。
- 修订：合并发须、缩眼白/颈段，薇特加清楚年龄块面，沃伦眉轴调平。保留初稿，不继续第三次生成。
- 备注：少量发须细亮条、单像素过渡；左右1px安全余量未触边。临时32色上限不代表设计色阶已最终核准。
- 复现：python derive_portrait.py portrait_v2；之后python finalize_manifest.py恢复选稿记录与最终校验清单。使用Pillow，未安装新软件。
- 保留全部旧图、人物卡和代码；未集成游戏、未commit/push。
