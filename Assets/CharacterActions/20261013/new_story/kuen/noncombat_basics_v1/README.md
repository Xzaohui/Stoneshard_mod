# 枯恩：两种独立非战斗基础动作

选稿以 asset_catalog.json 的 selected 字段为准：均为 exports/*_transparent_clean.png。exports/*_transparent.png 是保留原字节的未清理历史副本，不能作为另一个动作计数。

每个姿态均通过 builtin imagegen 独立生成，首稿各一次，未用修订。raw/ 保留原图、完整原工具返回（包含原始图像数据）、原始receipt及alpha处理记录；prompts/保留调用前落盘的真实逐字提示词与完整参数。sources/ 保留母图、人物卡、既有表情、关联台本、规则与brief来源快照及哈希。

透明清理仅把原alpha≥128设255、其余设0；RGB、画布尺寸与像素位置完全不变，不画人体、不拉伸、不拼接或强量化。浅深板使用真实RGBA alpha_composite及最近邻等比缩放。

同目录旧production_brief/spec_lock中的planned/pending字样是调用前原始计划快照，不代表终态。最终选稿与冻结结论以FINAL_STATUS.json、manifest.json及QA-independent.json为准。

四姿彼此独立，没有连续动画、过渡、循环、装备组合、原生尺寸/方向/origin或游戏运行验收。动作不证明任何治疗、授权、交接、付款或任务完成。
