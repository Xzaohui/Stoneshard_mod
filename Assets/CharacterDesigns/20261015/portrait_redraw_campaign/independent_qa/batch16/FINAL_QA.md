# Batch16 独立 QA：3 人冻结候选，1 人 held

审计时间：2026-10-15T10:50:10.207949+00:00

## 结论

- 可交付：尼芙 niv v2_inset、欧岚 ouran v2_inset、扎禾 zaho v2。三人源轮廓完整，保留个别审美残留备注。
- 暂扣：维芮 vere v2。源图右发束真实裁边，父确认本批 held，不回选 v1、不追加生图。
- 四人的 PNG 技术与来源链校验通过，不等于四人轮廓通过。均非原生逐像素终稿，未做游戏整合或运行验收。

## 技术证据

- 46 份来源记录：当前原件、快照与所记 SHA 全匹配；四人的现卡、母版、旧 QA 与 manifest 也独立匹配 campaign roster。
- 8 份 imagegen 回包：base64 解码、保存 raw 与工具保存原文件逐字节相同；每人恰为初稿加一次修订。
- 10 份派生候选：独立执行整幅 NEAREST、MAXCOVERAGE≤32 色、alpha 128 二值化，输出 PNG 字节复现一致；8x 预览与严格 NN 一致。
- 4 目录 manifest、选中 SHA、全文件清单、SHA256SUMS 均完整通过；详见 final_technical_audit.json。
- 最终目标均为 74×100 RGBA、32 个可见 RGB 色、alpha仅0/255；透明像素 RGB 为0。

## 独立目检

### niv：frozen_deliverable_candidate_with_minor_notes
- 文件：`niv/candidates/portrait_v2_inset_74x100_candidate.png`
- SHA256：`0dd02407beb6b2473447e7201e7fba317c0583db9e9b33d1196070937f5eba0a`
- 身份：二十多岁成年女性、浅肤棕松卷、暖棕衣米领暗绿边。独立表达边界的警醒侧目成立。
- 改善：v2缩短裸颈、眼白收敛；完整轮廓与透明安全边关闭v1触边问题。
- 残留／阻塞：睫眼仍稍大，平行发束高光未完全合并；当前是重绘派生候选。

### ouran：frozen_deliverable_candidate_with_minor_notes
- 文件：`ouran/candidates/portrait_v2_inset_74x100_candidate.png`
- SHA256：`a522f895617a4fe50f7fa853dbf5826771ea7d4c42a69fadf2ca0500481134b2`
- 身份：四十多岁男性、灰褐乱短发短须、灰外层暖棕内领。警戒侧目与成熟面骨可读，未误读为银发老者。
- 改善：v2眼更窄暗、口线更平、颈缩短；inset确保完整轮廓透明边。
- 残留／阻塞：眉根仍有忧虑、顶部发量和条状高光偏多；保留审慎不安而非声称完全去忧眉。

### zaho：frozen_deliverable_candidate_with_minor_notes
- 文件：`zaho/candidates/portrait_v2_74x100_candidate.png`
- SHA256：`7ac438e5a85ed4f6dd0aeda758cdcdf60b4f5dbb40a532630cec6440957d8756`
- 身份：三十多岁成年女性、较宽成熟颌面、暗短发低小束、蓝染工作窄领。轻微不对称闭口保留自尊与记恩。
- 改善：v2显著短颈，嘴角微抬与维芮区分，发块略合并，源轮廓完整。
- 残留／阻塞：小块浅眼白、平行发束和较多顶部透明留白仍留备注；不改变全幅等比派生。

### vere：held_review_candidate_source_edge_clipping
- 文件：`vere/candidates/portrait_v2_74x100_candidate.png`
- SHA256：`48290922217c2e214b1cdb5d0b7165ca38923a21934f2b9038a680a4dedf2eff`
- 身份：三十多岁女性、棕色松侧辫与尖颌、现卡灰学院袍改制窄领。身份没有新增矛盾。
- 改善：v2短颈和灰领明显优于v1。
- 残留／阻塞：真实源图右侧发束裁边：x1078、y989–1053共65像素alpha>=128。外框padding不修复原始源轮廓。仍有忧眉和眼白/发束细条。

## 扎禾身份文字不一致

卡的弧线与当前两份台本多处使用“她”，与已审成年女性母版一致；卡末风格守卫单独写“他”。已独立核验并保留证据，依父明确确认按成年女性绘制。现卡蓝染工装优先旧锈红衣领；未改生产人物卡或母版。

## 维芮裁边证据与交付边界

- `vere_v2_source_edge_blocker.json`：原始源图 SHA、逐像素边界数据、连续65像素alpha≥128。
- `vere_v2_source_edge_evidence.png`：原图边界4x NN诊断，不是修补稿。
- `final_1x_4x_contact.png`：三人可交付与维芮held明确分栏。
- `freeze_manifest.json`：各目录所有文件冻结SHA及选中路径。后续打包应保持这些字节；维芮不得计入成功人数。
- 独立审计仅写本 batch16 目录；未生图、未修改生产卡/代码/旧资产、未提交推送。
