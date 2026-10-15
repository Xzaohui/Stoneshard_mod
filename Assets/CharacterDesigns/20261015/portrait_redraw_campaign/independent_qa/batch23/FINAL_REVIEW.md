# Batch23 独立肖像QA

结论：3人可交带限制技术候选，1人保留为held证据。

## 范围与验证
- 已读AGENTS、当前roster与四张现卡、母QA和相关剧情；实际看母图、Mara/Iwo/Leiya/Tore四核心、四人两轮raw及1×/整数NN三背景。
- 原件/源快照SHA、完整回包base64与raw字节一致、74×100/≤32可见RGB/二值alpha/透明RGB归零，逐候选独立重构与复制已读脚本重放，候选和所有预览逐字节复现；manifest与SHA全覆盖通过。
- 每人2份成功图像。桑勒另有六参考超限请求，在生成前被拒绝，0图像，不算第三份成功图像。
- 四人身份与当前年龄/衣色成立；现卡明确外观优先于旧概念图。

## 各人结论

### 桑勒 / SKO-NPC-SALER
状态：pass_concept_with_notes；可交=True。
候选/held证据：`saler/candidates/portrait_v2_74x100_candidate.png`
SHA256：`4ff3a2b9c0185b31dcc25f80bdf9f25a4ae24759ea6471a9af897b5e435f5c99`
- 40岁松面笑纹、棕发薄须、梅帽兑筹缝记、梅外/黄褐里成立；最新卡外观更新优先。
- v2大脸与短颈改善，颌下仅窄领；警觉侧目和克制半笑可辨。
- 实际看raw与1×/8×浅深灰背景：完整帽顶、棕发和耳无切边；A>5 bbox[41,98,1049,1354]，源四边最高alpha1。
- 限制：眼白仍偏亮，不能说小暗眼风格已全验收。
- 限制：内眉仍略上抬，但没有丢失礼貌半笑。
- 限制：帽发占幅仍较大、局部发丝与皱纹较碎。

### 温诺 / SKO-NPC-WENNO
状态：pass_concept_with_notes；可交=True。
候选/held证据：`wenno/candidates/portrait_v2_containment_74x100_candidate.png`
SHA256：`fce8e52d5a59497c631c65b208c11ab6642b42018940a4919d57bf1619f380e2`
- 50岁净面、沙棕夹灰发与蓝/米白衣色保持；臂部烫伤未迁到脸上。
- v2裸颈收短、窄领贴下颌，蓝灰沉重布折提示湿布披肩；神情冷静专注而有轻微紧眉。
- 实际看raw、1×/8×与三背景，头发耳完整；A>5 bbox[30,91,1074,1393]/1079×1458，右发尖仍有真实5px高分辨率余量。
- 70×96完整画布等比NEAREST containment居中至74×100，未裁切、补画或修形。
- 限制：右发尖真实余量仅5px高分辨率像素，窄；containment增加目标画布余量不等于生成扩边。
- 限制：眼白仍有亮簇，发丝及局部皱纹偏碎。
- 限制：和四核心相比，头发仍较复杂；只接受带限制的技术候选。

### 布岚 / SKO-S01-NPC
状态：pass_concept_with_notes；可交=True。
候选/held证据：`buran/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`0cd388f2397e5ec024dd3ca0b155314b689bb1f179f722b88fae4bfe3c4a6763`
- 40多岁炭份保管人，厚实脸宽鼻、灰棕短须、暗帽/棕厚工装赭内衫成立。
- v2短颈、窄领、大脸及发须连通色块明显改善；眉变薄断续但仍有斟酌忧意。
- 实际看raw、1×/8×三背景，帽发耳完整；A>5 bbox[39,96,1068,1448]/1078×1459，右10px/底11px真实余量，源四边max alpha1。
- 限制：眼白仍偏亮；内眉残余忧意。
- 限制：眉虽变薄断续，炉火烤稀疏的辨识仍有限。
- 限制：帽发占幅偏大；源右10px和底11px高分辨率余量窄。

### 雷哈 / SKO-S02-NPC
状态：held_source_clipping；可交=False。
候选/held证据：`reha/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`f00a999d4e4fad8774b45061f8b696cfd6168d79fefc81c62a5d4d9da20b5e6c`
- 50多岁父亲、银灰发须、棕旧外套和绿内衫成立。
- v2较初稿颈短、窄领、大块发须改善；仍保较强内抬忧眉和亮眼白。
- 实际看raw右发卷撞画布截断；完整源头发留边失败。候选inset虽外有空白，不能补回缺失的源发尖。
- 限制：眼白偏亮且忧眉模板感仍较强。
- 限制：原raw左右余量不均，右发卷已真实裁切，不能列入可交候选。
- 限制：v1右发边也未达到完整安全留边，不能回选冒充通过；两次已用完，不第三次。
- 阻断：Raw1078×1459最右列x1077有16个alpha>=128像素，y531–546，最高alpha254；A>5 bbox[9,79,1078,1446]与A>=128 bbox[9,81,1078,1445]均到右边界。见reha_v2_right_edge_evidence.png与reha_v2_edge_pixels.json。

## 交付边界
仅桑勒、温诺、布岚进入可交候选。雷哈v2是锁定的失败证据，不回退不安全v1，也不进行第三次生成。
NN缩放、居中与临时量化是技术派生，inset/containment不会补回裁掉的源发尖；不是原生逐像素终稿，没有游戏内集成或实机验收。
仅写本QA目录。未修改旧图、源卡、代码，未commit/push。
交付具体路径及全SHA见FINAL_SELECTION.json、DELIVERY_CHECKLIST.json与SHA256SUMS.txt。
早期进度审计是在作者目录尚未冻结时运行，缺raw或清单不一致保留为历史；新加8×NN源在后续审计按派生预览验证。最终以final_technical_audit.json和frozen_verification.json为准。
