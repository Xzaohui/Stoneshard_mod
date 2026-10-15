# Batch22 独立 QA 终审

冻结时间：2026-10-15T11:39:24.896681+00:00

结论：4张v2带备注概念候选可交付，0 held。仅74×100 NN/二值alpha/≤32可见色量化派生候选，非原生像素终稿，未集成或实机验收。

## 证据与技术验收

- 当前人物卡、指定母图、母图QA、mara/iwo/leiya/tore四核心均已读取并实际看图；49项来源/快照SHA全部一致，最终复核无漂移。
- 各2份成功生图，共8份完整toolreturn的image_url解码与raw逐字节一致。古烈另有一次六参照参数预检拒绝，无图返回，实参/错误均保留，不计第三份生图。
- 8候选均74×100、≤32可见RGB色、二值alpha；独立算法复算PNG逐字节一致。
- 完整读取并SHA锁定导出脚本后，只在本QA目录重放；8版本共48个候选/1x/8x/三底1x/4x/metrics文件逐字节一致。没有在作者目录重跑。
- 最终作者manifest共181文件项、SHA256SUMS共185文件项全匹配，全部文件已覆盖，selected SHA一致。
- 四个所选源的发、巾、耳完整；raw alpha>=5四边均清。madi/boh的inset为全画布技术缩放，不补回任何缺失轮廓。妮莎v1贴框风险由v2真实重画内收解决。
- 本审计不改变vere/naya的既有held裁边判断，不以透明padding洗掉源裁边。

## 冻结选择

### madi
- 候选：`madi/candidates/portrait_v2_inset_74x100_candidate.png`
- SHA256：`cb42e379fdb9cb3a6343b32766cc610abd7a1b5ce73ee8d089fd78ac5718c9f1`
- 约50岁长鼻成熟窄脸，口周/下睑纹理、灰缕浅巾、暗锈衣深罩衣成立。
- 脸体量提升，露颈明显缩短、窄领贴下颌，眉眼灰暗且保持温和坚持/忧疑。
- 头巾、巾结、发梢和耳完整。alpha>=128 bbox[9,112,1072,1408]；左右仅alpha1–2散点、>=5四边清。真实左右余量窄但未见截断；技术inset不用于弥补缺失形体。
- 眼内残留小亮簇
- 头巾占幅仍较大
- 源左右真实余量9/7px偏窄

### boh
- 候选：`boh/candidates/portrait_v2_inset_74x100_candidate.png`
- SHA256：`3af0c70c1da36a528d048bc421753fbe32f4b24f1f96eec3f4a8b86aa4bd0c50`
- 30多岁偏瘦男性，暗棕短胡发，灰蓝新工装/棕背心，自持警觉。非妮莎弟弟；赎回不代表家族所有。
- 较v1明显短颈、V领贴下颌；大脸窄肩底条、眼白灰暗、脸型保持瘦。
- 发冠、发梢、耳和肩完整；alpha>=128 bbox[55,71,1060,1298]，源四边有效轮廓不触边。
- 眼内小亮簇仍在
- 头发部分细碎
- 候选底部13px空白偏多，未擅自裁切放大

### goren
- 候选：`goren/candidates/portrait_v2_74x100_candidate.png`
- SHA256：`e084b4fc8a5914c9617f5b8781e5cc71cf2448139be99d86df71ebcba437fbc1`
- 使用rework_v2母图，30多岁男性炭工；厚下颌宽鼻棕短胡发与炭灰领，和博赫瘦脸可区分。护符可在本头颈画幅外，不增魔法或护理改信含义。
- 眼缩为小横向侧目、眼白压暗，显著短颈窄领；厚脸大面块保持疲倦坚守。
- 发冠发梢及耳完整；alpha>=128 bbox[24,114,1070,1409]，源边缘最高alpha3、>=5四边清。
- 发胡仍略碎
- 眼内少量浅簇
- 发冠仍占幅偏大
- 源右侧9px透明余量窄

### nisha
- 候选：`nisha/candidates/portrait_v2_74x100_candidate.png`
- SHA256：`dcfcd95f05ce3dea8b67c8241345a721c253c2daf84ef80b0651ea0cf7817d87`
- 40多岁女性会计，伏案红痕/口周纹、棕发锈红巾，深罩衣领与少量暗绿肩边。焦虑愧疚、分栏原则；不表示弟弟已归，也不把博赫画成弟弟。
- 短颈窄深领明显落实；发梢、巾结巾尾重新内收，左发及右巾轮廓完整。
- alpha>=128 bbox[48,194,1061,1342]，四边最高alpha1；源真实留边恢复，非技术padding掩裁。
- 眼白仍偏亮且比本批另三张更显眼，不等于小暗眼风格完全验收
- 头发/锈红巾占幅仍大
- 源右侧18px余量较窄
- 顶空13px、底空8px造成头像有效占高较少

## 交付入口与限制

- `FINAL_SELECTION.json`：唯一冻结选图/哈希/交付标记；`DELIVERY_CHECKLIST.json`：48项交付证据清单。
- `final_technical_audit.json`、`frozen_verification.json`、`full_derivation_replay.json`：最终证据；`selected_v2_1x_4x.png`：不插值1x/4x总览。
- `v1_visual_feedback.json`保存每人唯一集中反馈；`v2_visual_reviews.json`保存终审。中途initial/prefreeze报告保留历史，其中未冻结时的manifest待项已被final_technical_audit全部关闭。
- 仍有亮眼簇、发/巾细纹和头部留白差异，妮莎眼白较明显；需后续原生像素制作与游戏内可读性/透明边缘/定位验收。不能以本技术通过替代这些验收。
- 本独立QA全部写入仅限`independent_qa/batch22`，未改生产角色文件、旧图、人物卡、代码，未commit/push。
