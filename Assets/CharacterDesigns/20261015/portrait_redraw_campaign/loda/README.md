# 洛妲 / loda / batch06

当前作者选择：candidates/portrait_v2_maxcoverage_74x100_candidate.png。每人2次内置imagegen（初稿＋唯一修订），已用完本轮额度，保留v1。待独立QA确认；不能称艺术终审或入游验收。

修订后短颈窄领口与脸部占比已改善。保三十多岁成年女性、宽方下颌、深棕后低束发、深蓝工装领；按最新卡加入低帽与浅粉灰粉线。

选MAXCOVERAGE原因：v2 MAXCOVERAGE保眼白/虹膜分离与淡粉灰帽线，MEDIANCUT将其并成肤橘色，不选。

仍需披露：帽体虽压低仍偏软。；顶部留白略多。；眼白仍有小亮片。；个别脸颊亮色孤点。

- 完整输入参数与提示：prompts/portrait_v1.json、prompts/portrait_v2.json
- 原图与完整工具返回：raw/、tool_returns/
- 最新卡、母版、既有QA、剧情和四张认可风格参考的字节快照及SHA：sources/source_manifest.json
- 74×100 RGBA透明派生：candidates/
- 1x黑/灰/浅底与整数8x预览：previews/
- 技术统计、作者视觉自检、复现验证：qa/
- 全部逐文件校验：SHA256SUMS；身份及范围：spec_lock.md

每张raw由内置imagegen实质绘制。脚本只整图NEAREST缩小、alpha二值阈值128、最多32色无抖动量化及预览排版；没有代码绘脸或手工像素修补。MEDIANCUT与MAXCOVERAGE是同一raw的技术派生，不能称原生逐像素终稿。颜色上限为临时工作限制，非最终原生调色板证据。旧图、人物卡和代码未改；未commit/push。

复现：python derive_portrait.py；python export_maxcoverage.py portrait_v1；python export_maxcoverage.py portrait_v2；python finalize_manifest.py portrait_v2_maxcoverage。完整参数可重发imagegen，但生成非确定性；已有raw至候选的转换已逐字节验证。
