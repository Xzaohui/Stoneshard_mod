# 娜娅 / KOR-NPC-NAYA 肖像重绘记录：暂缓

独立 QA20 结论 `held_source_clipping`。本目录没有选定可交付肖像，manifest selected_portrait=null。v2仅为held证据：`candidates/portrait_v2_inset_74x100_candidate.png`。v2 raw左缘x=0,y523–534连续12个不透明像素，发束轮廓平截且未闭合。缩小留边不能修复源头发。

v1完整留存为历史fallback：`candidates/portrait_v1_inset_74x100_candidate.png`，但长颈/亮眼/忧眉未达本轮要求，不能代替通过。v2短颈虽改善，仍有亮眼白/忧眉/繁复团辫残余。成年20+窄脸直鼻、棕披肩蓝领身份一致。

两次imagegen（初稿加唯一修订）预算已用完，不第三次。74×100、32临时色、alpha0/255等技术指标通过只代表派生格式，不是原生终稿或美术通过。完整raw、返回、参数、源哈希、重放脚本与1x整数预览都保留；重放字节一致。

复现：`python derive_portrait.py portrait_v2 inset`；`python finalize_manifest.py portrait_v2_inset held_source_clipping`。旧素材、卡片、代码、索引不变；未commit/push，未集成或运行验收。
