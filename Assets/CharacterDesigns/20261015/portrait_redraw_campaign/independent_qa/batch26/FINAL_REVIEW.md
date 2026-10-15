# Batch26 独立QA终审

四人各完成首稿＋一次集中反馈后的修订，均不得第三次生图。技术通过不等于原生逐像素或游戏内验收。

## yur · candidate_with_limits
选稿：`yur/candidates/portrait_v2_inset_74x100_candidate.png`；暂挂证据：`None`
SHA256：`5351b9dceaa6738ddbbaa175cf6a68a50c39ac20ead3e86500ec52f3ae8fccc6`
限制：小眼点仍偏浅亮，未达四核心完全小暗眼控制。；下颌稀胡茬仍有碎格，裸颈仍有少量。

## bevi · candidate_with_limits
选稿：`bevi/candidates/portrait_v2_inset_74x100_candidate.png`；暂挂证据：`None`
SHA256：`f5f8bf6a6adc4cdf6d7baff77fffe03895affd3980c9224f6445e487feaf378b`
限制：发帽仍偏满，脸量尚未完全达到四核心。；小眼点和裸颈仍略显，表情偏忧但符合来源。

## ele · candidate_with_limits
选稿：`ele/candidates/portrait_v2_inset_74x100_candidate.png`；暂挂证据：`None`
SHA256：`f0814e54d8b13e363a89496df7eda9b8a9f27d14db1b3570b853f15999dba64c`
限制：原图右侧实心外余量仅1px，灰底实看轮廓闭合、边界实体0；inset不代表源留白已修宽，须如实保留此限制。；浅眼点与部分鼻颧小碎格仍在，颈部仍略长、发冠偏满。；仅NN/量化派生候选，未达到四核心原生逐像素控制。

## kare · held_source_clipping_and_style
选稿：`None`；暂挂证据：`kare/candidates/portrait_v2_74x100_candidate.png`
SHA256：`c4e4e2a516d297ee4d4a2e665875a636dd7f8cc0ffb4e0fdf35dc103c843c1c5`
限制：v2原始1079×1458画布右侧x1078、y606–687连续82个alpha≥128实体像素，头巾真实源留边失败；灰底实看确认，不是仅NN贴边。；v2眼白与微启嘴亮牙仍显，颈领尚多。；v1虽无源实体触边，却保留明显亮眼白与长颈宽领，不能为交付数回退。

## 证据与边界
- 33份原始源文件独立快照与终检SHA不变；卡、母图/母QA、四核心与相关台本已读，母图与输出实际查看。
- 所有成功回包解码字节与raw相等；74×100、≤32可见色、二值alpha、透明RGB归零、逐字节导出和整数NN预览独立复现。
- 作者manifest/全SHA覆盖完整；selected只允许selection_lock列出的文件及哈希。
- 蓓薇兄/姐文本差异仅记录；最新卡衣装优先旧母图；不改卡、旧图、生产代码或提交推送。
- inset为同raw整画布等比NN技术派生；非新生图、非原生像素终稿，未集成或实机验证。
