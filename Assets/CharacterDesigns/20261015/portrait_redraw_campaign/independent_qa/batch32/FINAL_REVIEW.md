# Batch32 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## ruya · candidate_with_limitations
选稿：`ruya/candidates/portrait_v2_74x100_candidate.png`
SHA256：`6d1ac8737309fcc958086a2208817372d2129bd93c1207a691037d6bba61844b`
限制：原始左右实体透明余量13/25px，仍较紧；74×100主体bbox(1,5,72,96)，窄边留存；头发及脸部仍有少量细碎量化色块，非原生逐像素人工终稿；NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。

## sujin · candidate_with_limitations
选稿：`sujin/candidates/portrait_v2_74x100_candidate.png`
SHA256：`5b196320ec4770973ba897c659e8bd35dbd187ace3449859373988d6e5127e08`
限制：原始左右实体透明余量10/18px，仍较紧；74×100主体bbox(1,7,73,89)，窄边留存；头巾体量偏大，裸颈仍略显长；作为带限制候选保留，不继续第三次生成；NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。

## suoya · candidate_with_limitations
选稿：`suoya/candidates/portrait_v2_74x100_candidate.png`
SHA256：`5e73bc68655674b727afb39acdfa107bab7ecf92dc3c03fe69c954b106444437`
限制：原始左右实体透明余量13/11px，仍较紧；74×100主体bbox(1,3,73,97)，不是源真裁断；眼白仍可更收敛，头发体量偏大；full优先脸部占比，已有inset只作未选技术派生；NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。

## ousha · held_style_not_deliverable
暂挂证据：`ousha/candidates/portrait_v2_74x100_candidate.png`
SHA256：`80cdadb272f181747fb6eca76f24e46d79c2f88bd74fabdf47b21188052c7251`
限制：核心风格未通过：两眼大亮白、偏卡通眼型与细长裸颈；不能因技术格式通过或大脸构图改善而列为可交付选稿；原始左右实体透明余量17/13px、底18px，轮廓完整但余量紧；full bbox(1,9,73,99)，inset不修复风格；selected为空、delivery_eligible=false；full v2和inset均只留研究审阅证据，不进入选稿交付清单；NN等比包含与32色量化为技术派生；未获用户审美终审，未集成或实机验证。

## 证据与边界
- 31份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 最新卡外观优先旧母图：芦雅30+深色布林式外褂、苏槿约50岁深绿磨旧工装、朔娅30+风雪纹左眉断口、欧莎30+低帽檐短斗篷；朔娅旧v3c是可核身份研究母图，不补写旧风格通过。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
