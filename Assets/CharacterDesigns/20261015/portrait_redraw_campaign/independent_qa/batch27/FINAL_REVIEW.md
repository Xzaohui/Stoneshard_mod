# Batch27 独立QA终审

每人首稿后唯一一轮集中必要反馈，最多两份成功生图，无第三次。所有选稿仅为NN技术派生候选，非原生逐像素/实机终稿。

## noze · held_style_gap
选稿：`None`；暂挂证据：`noze/candidates/portrait_v2_inset_74x100_candidate.png`
SHA256：`68779c0072745d373f601ea19d96a461781bf14c146487d12a50c36e6a562447`
限制：长裸颈与发辫挤占脸幅仍明显，风格缺口未关闭。；原始发耳与辫尾完整，有真实边距；此次暂挂不是源裁断。；v2 inset仅同raw全画布NN技术派生，不解决风格缺口。；不再生成第三份，不替回首稿，不作原生/实机终稿。

## odo · conditional_technical_candidate
选稿：`odo/candidates/portrait_v2_inset_74x100_candidate.png`；暂挂证据：`None`
SHA256：`227c7a5cb993d59efa92e67ae7c99ce5e8bf4605e1219da0b63aacaaa00e46a2`
限制：眼白仍有少量浅色、发须块略粗，只作带注技术候选。；源右边真实留白仅4像素，已用同raw整画布inset避免目标边缘贴边。；NEAREST缩放/量化是技术派生，非原生逐像素、未集成或实机验收。

## sefin · held_source_clipping
选稿：`None`；暂挂证据：`sefin/candidates/portrait_v2_74x100_candidate.png`
SHA256：`84098c2068d8de4888d4aebe00f7244e29a9b3501cd8ab6168b09e1ba4783a76`
限制：真实源右发尖裁断；候选NN边距不能代替完整原始轮廓。；v1虽源完整但亮眼白/长颈风格缺口未关闭，不替回作为选稿。；两份成功图上限已用完，不第三次，不做padding掩盖。；只保研究证据，不交付selected，不作原生/实机终稿。

## tanser · conditional_technical_candidate
选稿：`tanser/candidates/portrait_v2_inset_74x100_candidate.png`；暂挂证据：`None`
SHA256：`bae249098163e729dbfc8b63a194ede2d06a2b34bc47b210cec88d1a655a87b2`
限制：源右低alpha5–21羽边触边（alpha>=16三像素），不能声称所有alpha都完整留边；实心发尖闭合且有10像素真边距。；眉间旧缝痕在74×100化为少量明暗像素，微细结构不等于原生逐像素精修。；发量略多但脸/短颈目标成立；仅条件技术候选，未集成或实机验收。

## 证据与边界
- 30份原始源文件独立快照与终检SHA不变；当前卡、母图/母QA、四核心与相关台本已读，母图及输出实际查看。
- 回包解码raw逐字节相等；74×100 RGBA、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；只准交付selection_lock中的选稿文件与SHA。
- 最新卡外观优先旧母图遗漏；欧铎读三十多岁、坦瑟眉间旧缝痕、瑟芬男性兄长身份不被旧文本混写改变。
- 未修改旧图、卡片、生产代码或冻结索引，未提交推送；未集成或运行验证。
