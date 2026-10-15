# 莉德 74×100对白头像重绘

当前候选：`candidates/portrait_v2_74x100_candidate.png`。
1×三底色与8×整数最近邻对照：`previews/portrait_v2_1x_8x.png`；独立透明8×：`previews/portrait_v2_8x.png`。

## 身份和生成

冻结派工 `../batch_02_next.json` revision 2；实际阅读当前卡并查看旧母版后，使用内置 imagegen 实质重绘。完整prompt及实际参数在 `prompts/`；完整工具返回在 `tool_returns/`；返回原图在 `raw/`。来源快照、SHA和优先级见 `sources/source_manifest.json`。

## 技术派生

74×100为整幅nearest-neighbor缩放、alpha≥128二值化、Pillow MAXCOVERAGE无抖动量化的派生候选，不称原生74×100逐像素绘制。32可见RGB色只为本批临时上限，不是全项目标准。没有手绘补像素或几何修补。脚本 `derive_portrait.py` 可复现；各轮尺寸、色数、alpha、palette及SHA见 `qa/*_metrics.json`。

## 审查与范围

独立审查主记录：`../independent_qa/batch02/QA_REPORT.md`，独立机械复现：`../independent_qa/batch02/independent_measurements.json`。本目录保留作者自评与独立意见摘要。所有旧图原样保留；本轮未改人物卡、代码，未集成游戏，未提交/推送；candidate不代表用户已认可终稿或运行验证。

## 所选版本与非阻断余项

- 眉态更克制，下压嘴角与戒备侧望成立；缩颈减肩并保留高束识别。
- 三十多岁身份、锈褐罩衣与灰围领保留。
- 非阻断余项：眼白仍略亮，发髻仍偏大；两次限额已用，不再生成。

已依独立目视与机械复现冻结所选候选，不继续生图。
