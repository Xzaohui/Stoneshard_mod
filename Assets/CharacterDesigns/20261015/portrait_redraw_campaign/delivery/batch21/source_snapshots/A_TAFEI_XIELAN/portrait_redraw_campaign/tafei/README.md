# tafei 肖像重绘候选

当前选择：candidates/portrait_v2_inset_74x100_candidate.png。状态：独立视觉终审通过，带注记派生候选；QA21继续独立字节审计。

这是内置imagegen实质重绘，74×100、32色、二值alpha版本是整画布等比NEAREST缩放、无抖动MAXCOVERAGE量化与alpha阈值128的技术派生；不是原生逐像素终稿，未运行整合或验收。

塔斐v2源轮廓没有实质alpha触边，但原生尺度右侧仅1源px，full NN映射会触目标右界；选定同raw 72×98包含派生以避免采样压边，非重绘或遮掩原始裁切。

已保留最新人物卡、剧情、母图与母QA、四核心参考、来源SHA、完整prompt/参数、完整工具回包、raw、1x与整数NN预览、作者QA、manifest和SHA。旧资产与剧情代码未改。

已完成初稿与唯一集中修订，共2次成功生图，不第三次生成。v2首个参数配置含6张参考，被工具在生成前拒绝；保留拒绝参数与错误记录，移除重复身份母图输入后正常生成，实际输入为v1编辑目标及四核心参考。

复现：python derive_portrait.py portrait_v2 inset；python finalize_manifest.py portrait_v2_inset pass_with_notes_derived_candidate。

终审限制：raw右侧极紧，仅1源px透明列；inset仅导出留边，并不修复源图。原raw右局部已独立实看，外轮廓闭合，未见发帽被切断。胡须和帽仍有条带。
