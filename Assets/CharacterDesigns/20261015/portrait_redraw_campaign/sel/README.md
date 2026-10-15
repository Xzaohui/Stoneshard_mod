# 塞尔 / Sel 头像重绘候选

选定：`candidates/portrait_v2_mediancut_74x100_candidate.png`。预览：`previews/portrait_v2_mediancut_1x_8x.png`（三背景1x、8x最近邻与MAXCOVERAGE对照）。

独立人物卡（2026-10-13细描）优先。约50岁的工坊经手人；厚眉、较厚脸、宽鼻颧颌、灰短全须，锈红工作衫和炭灰围裙带保留。肩因劳作稍前倾，表现疲惫和盘算说明，不画冷血债主、武器或已签债票/卖炉结案。账尺、票夹、袖补丁与手茧在紧头像之外，不为身份强塞道具。

共两次内置imagegen实质绘画，第二次依独立QA集中反馈减少碎发须、缩颈、缓和眉眼。v1/v2原图、完整返回、prompt参数、来源快照与哈希均保留。生图冻结。

机械导出：整画布最近邻74×100；alpha128二值化；32色无抖动。原先MAXCOVERAGE保留小面积服色，但v2皮肤出现离群亮斑，因此依QA做一次MEDIANCUT对照并选定。两个v2导出alpha逐像素相同，无裁切、涂色、改形或手工补轮廓。旧MAXCOVERAGE候选保留。

原始v1为1079×1458、v2为1079×1457；这是生成图的机械缩采样候选，非原生74×100逐像素绘制。32色仅本轮临时上限，不等于手工设计色阶。独立QA选v2 MEDIANCUT，剩余眉口略严厉、眼白对比略高、自动近似色及发须台阶。

未改旧图、人物卡、代码；未提交推送；未集成或实机验证。

复现：`python derive_portrait.py <本目录> portrait_v2`，再`python derive_mediancut_comparison.py <本目录>`，最后`python finalize_manifest.py <本目录>`恢复选版和哈希清单。
