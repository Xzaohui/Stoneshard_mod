# 艾娜 / NPC-N-ENA 头像重绘候选

本目录只制作74×100对话头像。权威为2026-10-13独立人物卡，快照见sources/character_card.md；旧v2只参考衣着、发色、头巾/胡须身份，未继承旧Q版比例或大眼睛。

## 当前结果

- v1与唯一一次定向v2均保留；独立QA选用v2候选，已停止生图。
- candidates/portrait_v2_74x100_candidate.png为已选1×可审候选。
- previews/portrait_v2_8x.png为已选整数8×透明放大；portrait_v2_1x_8x.png含暗/灰/浅三底1×及8×与风格母版。
- 来源、参数、完整工具返回、未改动raw及校验分别在sources、prompts、tool_returns、raw、qa目录。

## 生成和导出

实质绘图使用内置imagegen。raw按工具返回原样存储。导出仅整幅NEAREST缩至74×100、alpha阈值128转0/255、MEDIANCUT最多32色且不抖动；没有手绘补像素、重画轮廓或机械裁脸。32色是本批临时上限，不是全项目永久标准。

这是imagegen高分辨率raw的最近邻缩图及量化派生，不能称原生逐像素绘制、官方工具完整通过或游戏内验证。未改旧图、人物卡、代码或游戏包，也未提交/推送。

## 复现

python derive_portrait.py <本目录路径> portrait_v2
python finalize_manifest.py <本目录路径> portrait_v2

衍生导出脚本来自同仓库已核验的Tore头像生产脚本，复制到本目录后仅改角色ID/名称。技术通过不代表审美或剧情通过。

## 独立QA已选v2，但保留局限

- 亮眼白和上抬忧眉仍较强。
- 头巾纵褶仍偏多。
- 8连通检查有3像素侧发断簇，位置(3,74)、(3,75)、(4,75)；保留原生图派生，不补画。

选稿 SHA-256：86c117a0e4d938cd0a817c97f5f4d6d105dbd725d25dac2cd25eb13190f98a5c

正式独立复核位于上级 independent_qa/batch01；本目录 qa/independent_selection_summary.json 保存选稿结论。候选通过不等于原生逐像素终稿或用户最终审美认可。
