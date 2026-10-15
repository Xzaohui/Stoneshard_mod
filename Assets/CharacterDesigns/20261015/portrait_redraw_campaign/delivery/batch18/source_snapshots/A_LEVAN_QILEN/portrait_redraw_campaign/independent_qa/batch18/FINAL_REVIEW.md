# Batch18 独立审计终报

冻结：2026-10-15T11:05:32.466539+00:00

## 结论

四人均选 v2，状态为“对白头像候选通过，保留限制”；无 held。四人各仅初稿＋一次修订，已明确禁止第三次生图。
全部仍是图像生成后技术派生候选，非原生逐像素终稿，未集成游戏、未做运行或装备兼容验证。

## 选稿与字节锁定

### 列梵 / PAS-NPC-LEVAN
- 源根：Assets/CharacterDesigns/20261015/portrait_redraw_campaign/levan
- 选稿：candidates/portrait_v2_74x100_candidate.png
- SHA-256：62c19f78afd75315ae5be7b79e804995844fa8ccc971c424e054593db559f0be
- 原始 v2 SHA-256：146c7197dc9ccc614f0e586c80ebd65e1b91b7d48b41b4ba01bc4c9a117c8cad
- 目标 alpha bbox：[1, 5, 73, 97]；原始 alpha≥128 bbox：[15, 71, 1070, 1419]
- 净面暗波发、20多岁和克制想家闭唇仍辨。
- 眼白收低压暗、裸颈缩短，锈衣领抬升；大块脸部和发团比初稿更一致。
- 源发耳轮廓完整，raw实色四边0；无需inset。
- 限制：左右约1目标px留边。 眼白及发线仍有少量细亮点；不是原生逐像素终稿。

### 绮伦 / PAS-NPC-QILEN
- 源根：Assets/CharacterDesigns/20261015/portrait_redraw_campaign/qilen
- 选稿：candidates/portrait_v2_74x100_candidate.png
- SHA-256：c4f5799a547826db579cd55524605b29ad98cbf19384f17ca997a9620294bb01
- 原始 v2 SHA-256：63559dccaba7ffe68e15bb0f520a830efefe21c20502c5159617f1b62237e739
- 目标 alpha bbox：[4, 11, 73, 90]；原始 alpha≥128 bbox：[65, 162, 1071, 1310]
- 成熟宽下颊长圆脸、宽鼻、薄弧暖笑保住，约40岁与列梵明显不同。
- 米白束发巾和高绿领忠实；裸颈明显缩短，笑眼收低。
- 耳、发巾、右侧结完整，raw实色四边0；无需inset。
- 限制：右侧约1目标px留边。 眼内仍有少量亮点，米白头巾块面比四核心更明亮。

### 莎帛 / PAS-NPC-SHABO
- 源根：Assets/CharacterDesigns/20261015/portrait_redraw_campaign/shabo
- 选稿：candidates/portrait_v2_74x100_candidate.png
- SHA-256：deb83ce13b4368c7f04154fe403b073ca8fbfeb37fc3c736500c19367dacadc8
- 原始 v2 SHA-256：7683dd6eeec0872dec1a5318ba3dab68053856a5c274a849bd51037830b5df7c
- 目标 alpha bbox：[2, 7, 73, 95]；原始 alpha≥128 bbox：[22, 97, 1062, 1383]
- 30多岁宽短鼻、厚下唇、方短颌与稳定专注神态成立。
- 米白头巾及短棕发保留，高蓝领显著缩短颈段、衣物压成底部窄条。
- 完整耳发头巾，源raw四边实色0；无需inset。
- 限制：右侧1目标px留边。 眼白仍略亮，米白头巾较四核心明亮；眉形仍略严肃。

### 沃汀 / PAS-NPC-WOTIN
- 源根：Assets/CharacterDesigns/20261015/portrait_redraw_campaign/wotin
- 选稿：candidates/portrait_v2_74x100_candidate.png
- SHA-256：c9345185e01b0d2af3e10a634d05080082f62ccac5fee7032b19001134e57f89
- 原始 v2 SHA-256：dc62ee3e14c9263bf659180740a58956988d753fabb9dbdfbd874a17cbebb996
- 目标 alpha bbox：[2, 5, 73, 98]；原始 alpha≥128 bbox：[35, 66, 1067, 1430]
- 40多岁长矩脸长鼻、暗八字胡、清下巴及欲辩小张口保住。
- 低平小暗眼和短颈高橄榄领改善明显，灰披只占底部窄条，脸部占比提高。
- 发耳完整，raw实色四边0；无需inset。
- 限制：右侧1目标px留边。 近眼仍有小米色高光，少量硬折线；非原生逐像素终稿。

## 独立核验

- 已读项目 AGENTS、名册四项、现卡、母版选择 QA/manifest 与相关剧情；实际查看四份母图、四核心参考、初稿与修订 raw、目标1x及整数放大、最终深灰浅底对照。
- 四人现卡与名册快照相符。历史母版记录的旧卡 SHA 与现卡不同，已重读现卡而未自动判冲突；共45项来源原件与快照逐字节/登记SHA匹配。
- 绮伦是列梵自愿选择的成年亲属，未擅定母亲/配偶。莎帛现卡短发与头巾相容，未推断长发。沃汀厚身与长矩脸不冲突；左臂疤未移至脸部。
- 8份成功图像返回的base64原始PNG字节均等于raw，output_hint所列原始文件亦匹配；莎帛另有一次超过5参考图的参数校验失败记录，无对应生成图片，不计成功图像。
- 全部8份候选均为74×100 RGBA、32种可见RGB色、alpha仅0/255，透明RGB清零；目标四边透明。
- 独立实现派生算法复现PNG字节一致。先阅读全文并锁定SHA的作者脚本复制至本审计目录再运行，8个版本的候选、1x、8x、三底1x/4x及metrics共48件结果逐字节复现。未在作者目录运行写脚本。
- 1x与候选字节一致，8x为精确NEAREST放大；背景预览也经重放逐字节核验。
- 四份最终manifest、其文件尺寸/哈希、完整SHA256SUMS与所选文件均核对通过，无遗漏、无硬错误、无待核项。冻结清单另锁manifest与SHA256SUMS文件自身SHA。
- 源raw实际视觉检查和alpha≥128边缘检查均未发现发耳/头巾截断；极低alpha残屑不当作实体裁切。四人均用full全画布等比采样，没有inset/padding选稿，不把量化或透明留边称为源图修复。

## 证据入口

- FINAL_SELECTION.json：交付worker选稿、源根与SHA锁
- final_technical_audit.json：来源、原始字节、派生、预览、manifest/SHA明细
- final_derivation_replay.json：已读SHA锁脚本隔离重放，48件逐字节比对
- preflight_source_checks.json：名册、现卡、母图母QA预检
- v1_visual_feedback.json / v2_visual_reviews.json：唯一反馈与终审限制
- selected_v2_four_character_contact.png：四人1x/4x对照
- selected_v2_background_comparison.png：四人深/灰/浅三底4x

审计只写 independent_qa/batch18；旧源资产、人物卡、作者目录未改；未 commit/push。

## 交付边界

仅打包本审计目录根级文件。replay/ 是隔离执行用的重复 raw、base64 回包与重放输出，留本地而不交付；各角色完整制作目录保留唯一原始输入证据。final_derivation_replay.json 保留48件逐字节比对结果，8张独立复现PNG在根级，足以配合作者目录重新核验。freeze_manifest.json 和 SHA256SUMS.txt 仅锁需交付根级文件，不要求打包 replay/。
