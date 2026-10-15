# Batch09 独立QA冻结报告

冻结时间：2026-10-15T09:40:53.422526+00:00

结论：4/4 可交付带备注头像候选。未宣称原生像素手绘终稿、用户验收或游戏内运行完成。

## 选稿与视觉结论

### 瑟拉 / BRY-NPC-SELA
选稿：`sela/candidates/portrait_v1_maxcoverage_74x100_candidate.png`
SHA256：`1cb0cb01459333ac590270f04be5a9c3a2dd2e8094a8accad7b3fb522247d91b`
成熟侧目轻笑、高马尾和蓝绿双层工作衣成立，脸部大块连贯；保留v1避免不必要重绘。
保留意见：顶部留白7px，裸颈略多。；少量发纹仍较核心理想大面细。
技术：74×100，32种可见RGB，alpha仅0/255，bbox=[2, 7, 73, 99]。成功生成次数1。

### 塞芙 / BRY-NPC-SEV
选稿：`sev/candidates/portrait_v2_maxcoverage_74x100_candidate.png`
SHA256：`d3a562379715b63a94701b08f58d73f2fec6a78b912985624d14dfa7ab255464`
唯一v2修复右侧低髻触边，MAXCOVERAGE保住深蓝/米领；眉更平、暗米灰眼白更自然，鼻梁细横纹、成年审视与闭唇成立。
保留意见：裸颈仍略长，发丝分块较多。；保持戒备感，不把审视误作军官权威。
技术：74×100，32种可见RGB，alpha仅0/255，bbox=[1, 3, 73, 99]。成功生成次数2。

### 陶芮 / BRY-NPC-TAORI
选稿：`taori/candidates/portrait_v2_containment_74x100_candidate.png`
SHA256：`c31f72a9c6328139aafbadf1bb950bdad0f62f6dc9162899a624a1d6ffcd604f`
唯一v2显著降肤色饱和、半垂眼和平眉减忧，苍白疲惫与自主克制成立；灰紫粗布和旧毯窄边，没有康复笑或护理者身份。72×98整图NN后居中74×100保住全部发耳。
保留意见：鼻眉阴影略柔，仍不是逐像素原生手绘。；顶部留白5px；小幅技术留边使脸缩小约2.7%，可接受。
技术：74×100，32种可见RGB，alpha仅0/255，bbox=[2, 5, 73, 98]。成功生成次数2。

### 维松 / BRY-NPC-VIMON
选稿：`vimon/candidates/portrait_v2_74x100_candidate.png`
SHA256：`2a1c27c689a8748be03839e43050244350122c958966265e16e911da7e01273e`
唯一v2把短剃头皮与浅须从碎纹归并为大面，40多岁窄脸长鼻、平嘴与蓝灰/燕麦衣色保留；按当前卡替换旧束发，无领奖英雄/悔罪暗示。
保留意见：两处小眼白仍偏亮，裸颈仍略长。；头皮平面偏平整；作为候选保留，不追加第三稿。
技术：74×100，32种可见RGB，alpha仅0/255，bbox=[0, 5, 74, 100]。成功生成次数2。

## 独立核验

- 48条源文件/快照SHA逐一吻合；四角色当前roster、当前人物卡、所选母版及历史manifest核对通过。
- 7份raw逐字节匹配完整工具返回的image payload及保留的原始生成文件。
- 11个派生独立重跑，每个像素及PNG文件字节吻合；8x预览均为精确NEAREST。
- 作者manifest选稿SHA、完整文件清单的SHA/字节数、SHA256SUMS均已独立复核，无缺项或错误。
- 所有最终选稿符合74×100、≤32临时可见色、二值alpha；不以数字合规替代审美。
- 陶芮的containment仅把完整raw最近邻至72×98并放进74×100透明画布(1,1)，再alpha128与32色MEDIANCUT；没有裁切、补画或额外生成。
- 维松左右底边触边均为衣肩，发与耳保持完整。
- 前期initial_technical_audit与first_pair_frozen_audit是生产仍在写入时的检查快照，其中缺文件/生成数差异不是最终gate。最终以QA_GATE.json及final_technical_audit.json为准。

## 范围与交付

- 实际逐张查看旧母版、四核心、全部新raw及目标1x/8x预览。身份约束与首次集中修订意见见INITIAL_VISUAL_REVIEW.md。
- 只写independent_qa/batch09；未运行作者派生脚本写生产目录，未改人物卡/旧图/代码，不生图，不提交或推送。
- 来源、参数、原始返回、候选与预览由作者目录保留；本目录保留独立复现PNG、审计脚本/报告、冻结选择与对照预览。
