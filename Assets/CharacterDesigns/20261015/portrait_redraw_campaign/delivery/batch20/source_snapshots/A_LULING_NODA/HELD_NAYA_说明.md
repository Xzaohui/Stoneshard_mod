# 娜娅 NAYA 暂缓说明

本批独立终审为 `held_source_clipping`。娜娅没有选定可交付头像，`selected_portrait=null`；仅有两次生成后的历史和失败证据。不得把源包内候选作为成功头像计数或展示。

V2 原始图 `raw/portrait_v2_raw_imagegen.png` SHA256：f5e816e746fd35e5c548b93cacce370446d01809dbab12c8b4f6f4cbd031462d。左缘 x=0、y=523–534 连续12个 alpha≥128 像素，发束平截，源轮廓未闭合。技术 inset 透明留边未补回缺失头发。

V2 held证据 `candidates/portrait_v2_inset_74x100_candidate.png` SHA256：fb2b305dafd34a06be1fc03da9ecbd1aea1cd436dc6fcc4c5084d61120760777。

V1 `candidates/portrait_v1_inset_74x100_candidate.png` SHA256：5857a603b78da2ea22284ad156f3517836dbb7d572d14483d0899b20c5044ede。源轮廓虽完整，但长颈、亮眼和忧眉未达本轮要求，只保留历史记录，不回选、不计成功。

独立证据：`portrait_redraw_campaign/independent_qa/batch20/naya_source_boundary_evidence.json` 和 `naya_v2_left_boundary_4x.png`。技术格式与解包复现通过不能覆盖视觉暂缓。没有第三次生成。
