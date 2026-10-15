# xielan 肖像重绘候选

当前选择：candidates/portrait_v2_74x100_candidate.png。状态：独立视觉终审通过，带注记派生候选；QA21继续独立字节审计。

这是内置imagegen实质重绘，74×100、32色、二值alpha版本是整画布等比NEAREST缩放、无抖动MAXCOVERAGE量化与alpha阈值128的技术派生；不是原生逐像素终稿，未运行整合或验收。

榭兰直接选择v2全画布等比派生，目标四边均留透明像素。

已保留最新人物卡、剧情、母图与母QA、四核心参考、来源SHA、完整prompt/参数、完整工具回包、raw、1x与整数NN预览、作者QA、manifest和SHA。旧资产与剧情代码未改。

已完成初稿与唯一集中修订，共2次成功生图，不第三次生成。v2首个参数配置含6张参考，被工具在生成前拒绝；保留拒绝参数与错误记录，移除重复身份母图输入后正常生成，实际输入为v1编辑目标及四核心参考。

复现：python derive_portrait.py portrait_v2；python finalize_manifest.py portrait_v2 pass_with_notes_derived_candidate。

终审限制：灰发仍有条带，神情略严肃；眼白已缩暗，眉间沟已减弱。
