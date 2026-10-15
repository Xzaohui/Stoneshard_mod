# 莉葵 / liqui / batch24 肖像重绘

## 选稿与边界

独立QA核过后锁定带限制肖像候选：`candidates/portrait_v2_inset_74x100_candidate.png`。
SHA256：`b2b799491040e3edf06720bd87cd96db4b9f1bad5f340ac7b989c9657cffae90`。

30多岁成年长脸、栗棕低辫、单侧挑眉/自信微笑、绿赭两层旅行领保留。

- 眼部仍有浅米白点
- 发量偏满
- 仍是技术派生候选，非原生逐像素终稿，未接入/验证游戏

## 来源与版本

- `sources/`：现卡、母图、母版QA/manifest、四核心风格、相关剧情与AGENTS快照；`source_manifest.json`保存原路径与SHA，`qa/source_hash_recheck.json`复核一致。
- `prompts/portrait_v1.json`、`portrait_v2.json`是完整准确的实际生成参数；同名txt为提示词。
- `tool_returns/portrait_v1.json`、`portrait_v2.json`为完整工具回包（包含原图数据）；`raw/`原图经逐字节比对一致。
- 六参考预备参数保留，实际成功v2用了支持的5参考。调用与校验失败情况见`qa/generation_ledger.json`，不作第三次产图。
- `candidates/`保留v1、v2全幅及v2 inset；`previews/`包含1x、整数8x最近邻及三种底色1x/4x预览。
- `qa/`包含v1作者意见、v2作者审美、独立QA锁稿、技术指标、原始边界、源码SHA和确定性复现。

## 技术复现

完整原图画布等比缩至72×98容器后居中于74×100，NEAREST无插值；alpha阈值128；MAXCOVERAGE至多32可见色、无抖动，透明像素RGB归零。未裁发耳、未变形、未脚本绘制五官。

`python derive_portrait.py portrait_v1`
`python derive_portrait.py portrait_v2`
`python derive_portrait.py portrait_v2 inset`
`python finalize_manifest.py portrait_v2_inset selected_candidate_with_limitations`

32色为临时工作上限；上述均为生图后的技术派生，不能冒称原生逐像素终稿或游戏内验收。每人实际2张生图，初稿+唯一必要修订，剩余缺陷如实保留，不第三次。旧图、角色卡、代码与公共冻结索引未改，无commit/push。
