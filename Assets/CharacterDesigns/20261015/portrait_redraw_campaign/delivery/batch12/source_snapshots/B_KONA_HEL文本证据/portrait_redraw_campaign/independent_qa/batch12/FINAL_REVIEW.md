# Batch12 独立终审

结论：3张可交付候选，1人身份冲突暂挂。全部仍为非原生终稿的对白头像候选，未入游戏验收。

## 选稿

- 埃墨·衬（ALD-NPC-EMO）：`emo/candidates/portrait_v2_maxcoverage_74x100_candidate.png`。32色，SHA256 `b1e73ec1f7fe10a842f0772a9c7d2d5e61fd0ae2b4506c51641a44a6786c1849`。少量约2px眼白、帽部细纹仍可见；已保暖棕肤、卷发亚麻帽、成熟清瘦脸及蓝灰窄领。
- 奇恩（ALD-NPC-KIEN）：`kien/candidates/portrait_v2_74x100_candidate.png`。32色，SHA256 `0f2832c722d560640d35ff63ae30296a717ae9911d4529a60c9802748a55973d`。沙发仍有少量平行细簇、嘴角偏急；宽厚下颌与短颈已显著改善，符合现卡40岁敦实成年。
- 科纳（ALD-NPC-KONA）：`kona/candidates/portrait_v2_74x100_candidate.png`。30色，SHA256 `8a1a2530fa2a7fbba9943de3ac2b4334bf63603f9b37200ca27bfbcef8f9f442`。谨慎眉势与颈部斜亮面仍略突出；平内眉、短颈窄领改善，30多暗波发短须及深蓝领成立。

三张已实际查看原图、74×100及1×/8×最近邻预览，并与四核心风格锚比较。均为紧脸、短颈窄领、整齐鼻颧骨块面，帽/发/耳未因放大被裁。三人面型、发色、帽/胡须与表情可区分。当前卡的年龄体貌服装优先于旧视觉假设：埃墨40多、奇恩40敦实、科纳30多深蓝短褂。初稿问题均集中反馈，每人仅一次生图修订。

## 赫莲·金暂挂

ALD-NPC-HEL：现卡“她的尺只量本件”与所锁历史短须成年男性母版/历史QA构成真实冲突；来源SHA相符，非文件误配。保持blocked_source_conflict，生图0、候选0，不计合格。等待父任务/用户身份决定。没有重画、改卡或覆盖旧图。这是来源身份冲突，并非安全阻断。

## 独立技术检查

- 当前卡、母版、历史QA/manifest、四核心与脚本来源共43份源快照的原件/快照/SHA相符；另核名册锁定身份源。
- 6份成功工具返回与raw逐字节相等，工具输出原文件仍在且相等；每人恰好2次，赫莲0次。
- 独立从raw重建全部7份74×100候选，像素与保存后的PNG字节均一致；所有8×预览确为NEAREST。
- 所选埃墨32色、奇恩32色、科纳30色；alpha均仅0/255，无框边不透明像素，无透明RGB污染。
- 埃墨v2使用72×98安全域等比例NN并MAXCOVERAGE无抖动32色，保蓝灰小领。奇恩v2使用整图74×100 NN fit并MEDIANCUT；科纳v2使用72×98安全域等比例NN及MEDIANCUT，保留完整发耳。没有剪裁/拉伸/局部手绘。
- 全部作者manifest文件、明确选稿SHA与SHA256SUMS再次核验通过。赫莲冻结包全SHA通过，生成与候选计数均为0。

## 边界

≤32色是临时候选色数上限，不是全局锁定调色板。统计通过不代替上述视觉判断。未证明原生逐像素作者工作、装备兼容、运行导入或用户终稿批准。独审只写本batch12目录，未修改人物生产文件、故事卡、旧资产或代码，未提交/推送。

证据入口：`FINAL_SELECTION.json`、`frozen_technical_audit.json`、`preflight_source_checks.json`、`hel_frozen_held_verification.json`及`selected_candidates_1x_4x.png`。
