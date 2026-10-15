# Batch 14 独立冻结审查

结论：4/4 可交付为带备注的重绘头像候选。没有原生逐像素批准，也没有游戏内验证。

## 冻结选稿

- 伊榕（ALD-NPC-YIRONG）：`yirong/candidates/portrait_v2_74x100_candidate.png`
  - SHA256：`64c84285c9229cf905d2f0981e9c2fbb54f23be31f5a5c47c408bc8d074afb2a`
  - 50多银低髻、素黑窄领与疲惫追问成立；v2删掉长垂碎发并简化发块、缩短颈领。中央眉势仍轻微偏忧，少量眼白和细簇留作候选备注。
- 泊恩（ALD-S01-NPC）：`poen/candidates/portrait_v2_74x100_candidate.png`
  - SHA256：`dfee127c4b43badb78367b34bfb432840b380acd50d8a5da175a6b9aa4edd903`
  - 约60瘦颧、灰卷发宽胡须、审视眯眼和短颈窄领成立；v2关闭原图发卷真实撞边与宽胸领问题。须发少量细簇、眼白和MEDIANCUT使极窄赭领偏棕保留备注。职业是旧料回收匠，非领班。
- 芬珂（ALD-S02-NPC）：`fenko/candidates/portrait_v2_inset_74x100_candidate.png`
  - SHA256：`b27191815699dfe4edd4d0cd902f3b5957e720e72d5b452922767fa1c5ae3ef5`
  - 30多长角脸、克制自尊抿嘴，亚麻帽棕发及绿/炭窄领成立；v2放大脸并显著缩短裸颈锁骨，同raw整图等比NN inset关闭导出右帽尾贴框。少量眼白、细发簇及颈领余量保留备注。
- 萝铎（ALD-S03-NPC）：`lodo/candidates/portrait_v2_74x100_candidate.png`
  - SHA256：`fa33c5ef610d4e0e7629f85668677f1b2ab7ba701007d21053478f5c64db3fe9`
  - 40多宽鼻颧和成熟宽脸、偏侧专业接待小笑成立；v2缩短颈领并完整收进右巾结，暗锈/蓝灰领可辨，与芬珂瘦直嘴区分。少量发线、颈肩余量与眼白保留备注。

## 来源、原始回包与导出复现

- 已读现卡、关键关联台本、旧QA及母版manifest；实际看四身份母版、四核心风格参考、四首稿与四修订图。
- 年龄和伊榕黑衣按现卡优先。泊恩职业为旧料回收匠；父交接“领班”已澄清，生产prompt未采用错误身份。
- 每人两次成功生图，共8张raw；逐张独立比对完整tool image payload、归档raw和可访问generated original。全部字节一致。
- 四人所有来源snapshot与原来源及记录SHA一致；原人物卡和旧母版未改。
- 所有74×100候选均独立复现导出像素与PNG文件字节，并校验≤32可见色、二值alpha、透明RGB归零、8x严格最近邻。
- 4个终选四边透明。芬珂inset前的raw本来轮廓完整；仅通过等比整图NN留边避免采样后贴框，没有画补边或第三次生图。
- 完整生产manifest files、SHA256SUMS及所选SHA逐一实核通过。
- 初稿或生产收尾过程中记录的清单缺项/暂时哈希差异均在冻结审计关闭；以frozen_technical_audit.json为最终技术结论。

## 边界

- 限色是临时候选导出预算；生成图经最近邻、alpha阈值和无抖动量化，不是原生74×100手工逐像素绘制。
- 仍有少量亮眼白、细簇及个别眉势/颈领余量，已作为非阻断候选备注，不得转述为毫无问题的原生终稿。
- 本QA仅写independent_qa/batch14；没有改生产图、人物卡或代码，没有提交或推送。
