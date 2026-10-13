# D/E：表情探索稿，未选定

用户否定C的美感并要求情绪表达后，重新整理面颊、眉眼和嘴线。D意图为温和但警觉；E意图为略倔强。此为意图，不代表表情已经成功。

共通修改：嘴由C的y19上提至y18，y19恢复连续肤面；鼻下不再用一枚深点作为器官，面部主明面连成较完整的暖肤色块。新增三枚低饱和暖过渡色：中间肤#dca074、阴影#b87857、短嘴色#9d6854，保原亮肤#efbb82、原身体和手肤。没有整体变白、眼白大亮点、浓口红或高分辨率纹理。

初版实际眼色为deep_brown #35271f，但实际观察仍像淡眼窝/闭眼，根审看和两位独立审看均不认为表情成立。因此v2将近眼改为outline+hair_dark，远眼outline，并让E眉眼之间保一行完整肤色。不用结构QA代替审美结论。

查看：
- `comparison_CDE_1x.png` / `comparison_CDE_8x.png`：C/D/E/Gunda同尺度。
- `face_CDE_closeups_10x.png`：同顺序整头10倍。
- `face_CDE_review_v2_10x.png`与`comparison_CDE_review_v2_1x.png`：v2稳定快照，内容与当前正式预览相同。
- 两张`native`与`8x`透明图。

本目录所有改动基于原1:1 Before独立编辑，C/A/B不变。允许面部范围x10..18/y11..19，范围外逐像素相同；y20颏及以下、头顶、外发髻、身体衣装手脚均保留。沿用C的两像素鼻边内收，其余alpha保持。

`pixel_edits.json`记录所有前后RGBA与功能理由，`face_allowed_envelope.png`与各mask提供范围；QA仅证明范围和可重复性，不能证明漂亮或用户认可。

复现：

    python Assets/RedrawStudies/20261013/sela_proportions/facial_refinement/de_expressions/build_de.py /tmp/sela-face-de-reproduce

只用已有Pillow/NumPy显式像素工具，无imagegen、无新软件、无运行资源或其他演员修改。等待根审看及独立比较后选择，不自动交付为成品。

## 最终审看状态：冻结为探索，未通过

根审看与独立审看复看v2后认为：D/E主眼比初版更聚焦，D嘴略温和而E嘴平直，但原尺寸情绪差异很弱；E未能明确表达倔强。纵长平脸、大面积空面和迟钝感没有根治，不值得再单独交给用户一轮。停止D/E逐像素补丁，保留实验记录，不发用户为成品。初版“眼色太浅”的技术归因已纠正：实际RGB确为深棕，问题在暗簇与邻色组织。
