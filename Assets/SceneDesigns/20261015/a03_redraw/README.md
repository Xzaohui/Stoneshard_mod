# A03 / DT10 夜岗林缘重绘候选（2026-10-15）

选稿：`a03_dt10_night_watch_candidate_v2.png`，1448 × 1086、RGB PNG，和 v2 原始输出逐字节一致。采用内置 image_gen 完成初稿与一次必要收尾修订；未做程序绘画、缩放、量化或像素重采样。

## 题材与构图依据

- `docs/roadmap/绘图-迭代规划-20261015.md:58`：明确“A03”对应“夜岗林缘 DT10”。旧原图未取得，本批为重新绘画。
- `design/07_日常任务/台本/台本_DT10_别让狼靠近夜岗.md:22,45–46,153`：肉商弃血引来野兽；核验血槽与足迹；两条方法分别约束弃血、有限驱护。不按旧日常委托模板画循环屠狼任务。
- `design/02_世界与地图/区域_R03_曼恩边地.md:34,55,66–67`：R03-watch 夜岗林缘；冷灰石、湿黑木、旧蓝布；连接民田与风雪驿道。
- `Assets/SceneDesigns/20261013/new_scene_gap_audit.json` 的 `SCENE-GAP-DT10-R03-WATCH`：暮色、普通弃血槽、克制暗褐旧痕、可追踪足迹、可见夜路与退路；岗亭规格尚无剧情依据，因此本图只用简单遮雨棚。采用空景，不替剧情确定人物、狼群、清运、付费或结案。

相对方位、树丛、棚形与路面属于本次构图提案，不是新增剧情事实或可运行房间布局。原审计中保存的DT10旧SHA已不等于当前台本，本次实际阅读当前台本；见下方当前SHA。

## 已实际查看的系列与原版参考

- `Assets/SceneDesigns/20261015/a01_redraw/a01_brynn_dockyard_candidate_v2.png`：延续灰石、湿木、克制暖色、可读空地与固定俯斜游戏视角；本图降低小尺度表面噪点。
- `Assets/SceneDesigns/20261015/a01_redraw/references/Dockside_Store_outside.png`：本地保存的原作环境参考，观察建筑轮廓、材质色块和前向立面关系。
- `Assets/ReferenceAudit/20261013/originals/Frid_environ.png` 与 `prop_scene_reference_sheet.png`：本地保存的原作地面、木栏和草丛参考，观察疏密关系；其社区来源记录在 `original-reference-metadata.json`。未将这些原作参考复制进本批或当作新增作品。

## 输出与选稿

- `raw/a03_dt10_night_watch_v1_raw.png`：内置 image_gen 初次输出；构图完整，但足迹偏图标化、地面纹理细碎。
- `raw/a03_dt10_night_watch_v2_raw.png`：以内置 image_gen 编辑初稿，仅一次修订；缩小、减淡足迹并减轻细碎纹理，保留场景和叙事关系。
- `prompt_v1.txt`、`prompt_v2.txt`：两次调用的完整实际提示词。初稿未附输入图；参考图已由作者实际查看并转为文字规范。第二次输入为初稿原图。
- `a03_dt10_night_watch_candidate_v2.png`：v2选稿副本，供直接审阅与附件交付。

视觉检查：棚顶完整，夜路贯通，足迹与血槽分区清楚，无人物、动物、尸体、魔法、文字或UI。仍有生成概念画的细节与程式化足迹，不能称为已对齐原生像素精度；本次不拆层、不改代码或校验器、不接入、不运行、不提交或推送，不覆盖旧资产。

## 来源及输出校验值

- 绘图roadmap：`3bb1ab3eaf7ce11c63d1ce3a377815a4ae36405a9cabf59e6b6d5ff399f7985f`
- 当前DT10台本：`229a5fd7350499044e5acaaea369c413c8f60cff14ea6dbe06d8583a0bd0f619`
- R03区域：`d556b66a0834fe34f02eaad2fe47336ee683c73035c533800c37b1586367ede1`
- 场景审计：`ef807defdb2a348043b70f2a557bf5f2cec32f1b01198c11a9bc67e60fcd7246`
- v1原图：`19c59a77946cfbe6bba595985217a9cc994bc55f458f8242d1fbbc355e908c5d`
- v2原图及选稿：`885bc0465a470dc0e63ce85c921f7a76d4604be2a9a57f46bebf1f50695aa3b9`

原始生成输出均保留原位。本目录仅保存非破坏性副本与本批提示词、说明。
