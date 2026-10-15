# Batch33 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## daili · accepted_candidate_with_notes
选稿：`daili/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`b97465b3e5e64f50dc5839316e8fcf09cad880609dd4d4cd3f3f5b7c726f5f89`
限制：发巾卷发仍占较多幅面，颈仍有小段；未再开新生图；年龄与紧绷情绪为块面概念表达，非逐像素原生精修；NN技术派生候选，未集成或实机验证。

## ape · accepted_candidate_with_notes
选稿：`ape/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`6190add257fc41f31e2f18bac095316ab8eb0ec453d08d419d3e729b87677f89`
限制：须发仍有一定细纹，颈段虽短仍未达到极简；年龄读法风霜偏重，保留母图灰发疲态，不声称精确年龄写实肖像；NN技术派生候选，未集成或实机验证。

## kewei · accepted_candidate_with_notes
选稿：`kewei/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`08599118ea63d7ec78ec3501c32aac4f89e23123384c6dd0b08dcb2f4aaf647c`
限制：须部仍留一些细纹与插值观感，仅为粗块风格候选；NN技术派生候选，未逐像素原生精修、未集成或实机验证。

## luofu · accepted_candidate_with_notes
选稿：`luofu/candidates/portrait_v2_74x100_candidate.png`
SHA256：`7c9983c5bd9621243d81b0ad49ec1a667702170e78d0940bc82a86fb571d7bd2`
限制：颈与衣区仍比核心多，白巾仍带细条；只作带注候选，不宣称严格最终风格验收；头巾所占上部较多；没有第三次生成或脚本改脸；NN技术派生候选，未逐像素原生精修、未集成或实机验证。

## 证据与边界
- 36份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 最新卡外观优先旧母图：岱里约60岁女性看屋人，白巾灰缕橄榄厚衣；艾珀约40岁男性本段通风维护者，灰褐短须发褪蓝罩衣；科蔚约50岁男性有限出资者，整齐灰发短尖胡与深外套；洛芙30多岁女性水渠维护者，扎紧白巾橄榄罩衣。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
