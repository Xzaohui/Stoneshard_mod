# 首批五人头像重绘交付

2026-10-15｜米娅 MIA、艾娜 ENA、纳拉 NARA、妮尔 NELL、塞尔 SEL。

## 使用与状态

- 5 张独立 PNG 为最终冻结的 candidate，74×100、RGBA、二值 alpha，逐字节复制选稿。
- 中文总览为每人 1×原尺寸＋4×最近邻；只做排版，没有补画、重绘或改色。
- 来源为高分辨率生图，经全画布最近邻缩小、alpha 阈值 128、无抖动量化派生；不是原生手工逐像素终稿。
- 尚未接入游戏、未做实机验证，也不代表用户已经认可这批新稿。≤32 色仅本批临时上限。
- MIA 最终使用 v2 MAXCOVERAGE 保住暗青披肩；SEL 使用 v2 MEDIANCUT 减少皮肤盐斑；两者均为同 raw 的机械量化对照，没有增加生图。
- ENA 保留 3 像素独立侧发簇 (3,74)、(3,75)、(4,75)。其余亮眼白、平行发带、自动近似色等局限见逐人 QA。

## 源包

三个文件是彼此独立的普通 ZIP，不是分卷压缩包：
1. source_A_MIA_ENA.zip：MIA、ENA 完整过程与来源。
2. source_B_NARA_NELL.zip：NARA、NELL 完整过程与来源。
3. source_C_SEL.zip：SEL 完整过程与来源。
每包都含同一份全组独立 QA、中文总览及五张选稿、交付清单和核验脚本。每个角色保留全部 raw、提示词、完整工具返回、候选、导出脚本、预览、来源、作者 QA 与清单；旧候选仅供追溯。

商业原生参考图像不随包分发；其来源路径与哈希保留在原始来源清单及 DELIVERY_EXCLUSIONS.json 中。生成的旧身份图与自有风格参考可随包收录。生产清单 SHA256SUMS.txt 未改写，因此会包含被主动排除的商业参考项；验收实际源包请使用 package_inventory.json / PACKAGE_SHA256SUMS.txt。

各包可独立解压查看。若要拼回完整工作副本，将三包解压到同一空目录，重叠公共文件字节一致。历史脚本原样保留，可能依赖原仓库路径与 Pillow 版本；请先阅读后在副本内运行，避免覆盖已冻结成果。完整派生算法与独立逐 RGBA 复现结果见 independent_qa/batch01。

## 核验

运行 python3 verify_source_package.py <源包.zip> 可检查所有 ZIP CRC 和清单内每项 SHA-256。交付前已对每个条目检查 CRC、包内 hash 与快照源文件 hash；选稿、中文板和源包关联见 selected_delivery_manifest.json。
