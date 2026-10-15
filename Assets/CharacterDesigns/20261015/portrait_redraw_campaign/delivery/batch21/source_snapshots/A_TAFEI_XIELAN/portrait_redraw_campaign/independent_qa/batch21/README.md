# Batch21 独立审计冻结

冻结时间：2026-10-15T11:34:42.611410+00:00

四人状态：带注记的 NN 技术派生候选。没有原生像素或实机终稿批准。

## 终选与完整 SHA-256

- 塔斐（tafei）：tafei/candidates/portrait_v2_inset_74x100_candidate.png
  SHA-256：fdc0757e51e56e41a1684625b9346df19e176fe4801de8949507abc5d269b95a
- 榭兰（xielan）：xielan/candidates/portrait_v2_74x100_candidate.png
  SHA-256：81c343d0fce4935936d320bc9ca7d401c25806055fdf9a7134a35952d2a27143
- 尤恩（yuen）：yuen/candidates/portrait_v2_inset_74x100_candidate.png
  SHA-256：6a71b2e1db1b5bb27fa0bbe5ebaf9c20352fa2073c29dfa1b5fd3baf987b7313
- 阿霖（arlin）：arlin/candidates/portrait_v2_inset_74x100_candidate.png
  SHA-256：8b9a508ee332c9ee39c6d43248ef12ceadc135e57e5fa68e27c91c8a9215eb79

## 独立核验

- 当前人物卡、roster、母图、母 QA、母清单与四核心已核；真实打开图像核身份、年龄、衣色和个性。
- 当前源与快照 SHA 一致，冻结时再次确认源卡/母图/母 QA/清单未漂移。
- 完整 imagegen 回包解码字节与 raw 一致；每人成功成图至多2份，无第三份成图。
- 先读作者派生脚本并锁 SHA，再仅在本 QA 目录内复跑。所有候选、1x、8x、三底预览与 metrics 逐字节复现。
- 额外独立实现复验 PNG 字节、74×100、≤32可见RGB色、二值alpha、透明RGB为0、整数NN预览。
- 原raw与候选分别检查实质边界，不用技术padding把真实裁边洗成通过。
- 作者 manifest 和 SHA256SUMS 全文件覆盖核验通过；freeze_manifest 列四角色完整交付文件 SHA。

## 保留限制

- 塔斐：原raw右侧仅1源像素透明留边，余量极紧；full NN候选采样到右画框，所选72×98 containment仅是技术导出留边，不能声称修复源图裁切。；发须和帽褶仍有平行条带；小眼白残余偏亮，但明显好于v1。
- 榭兰：灰发和短胡仍保留一些重复条带、细碎像素；表情仍略严肃。；底部只1候选像素透明留边，构图余量偏紧。
- 尤恩：额眉皱纹线仍稍多，白发仍有少量连续条带；眼白保留小亮块。；原raw右侧余量15源像素，selected inset提供更稳候选留边，不是源图修复。
- 阿霖：小眼白仍比四核心略亮；深发仍为条状大分组，少量暗色合并仍存在。；full版本把部分褐发胡须合成橄榄调，selected inset已明显减轻；32色压缩的细微色差损失保留为限制。
- 塔斐低帽檐/早白鬓角、尤恩全白发/围巾旧徽、阿霖左眉疤按当前卡更新旧母图外观。
- 塔斐raw右边仅1源像素透明列，暗外轮廓仍闭合。v2_inset只改变等比技术containment，不代表源图修复。
- 全部是高分辨率生图后NN缩小、阈值alpha与量化导出的候选，非原生逐像素定稿。
- 未替换生产旧图、人物卡、游戏代码，未接入游戏或实机验证，未commit/push。

## 交付清单

- 每角色目录保留来源、规格锁、提示词、完整工具回包、raw、所有候选/技术派生、整数预览、作者QA、manifest、SHA及复跑脚本。
- 本目录含来源预检、每人唯一集中反馈、终选视觉评审、最终技术审计、逐字节复跑、独立复现、四人对照、四核心、源边界特写、冻结清单与全目录SHA。
- 参数校验未生成图片的记录与成功图片回包分开统计。replay/只是审计副本，不增加生图计数。
