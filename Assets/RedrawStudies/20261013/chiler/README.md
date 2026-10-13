# 齐勒：单站姿近1:1结构研究 v1

本轮仅 ALD-NPC-CHILER 齐勒。旧板与布娅未修改，未扩朝向、安装、修改 global/runtime 或 push。

## 当前可审阅结果

- `chiler_concept_v1.png`：built-in image_gen 新概念，完整提示词见 `prompt.txt`。仅用Bert/Jurg原生参考的最近邻放大作风格输入；旧齐勒板实际查看后仅用文字限定身份，避免继承细长插画比例。
- `chiler_native_v1.png` / `chiler_native_v1_1x.png`：35×44透明研究图；`chiler_native_v1_8x.png`为严格最近邻8倍。画布大小不是引擎规范。
- `comparison_landmarks_8x.png`：新齐勒与Gunda/Bert同尺度标线；`chiler_landmarks_20x.png`附每行/列坐标；`old_new_refs_comparison.png`保留旧身份对照。
- `native_base.png`为整理前采样中间稿；`native_base_20x.png`与`sampling_probe.png`仅早期诊断，后者显示不能直接使用含微弱透明噪点的总bbox裁切，绝非候选。

## 坐标与视觉判断

零基、闭区间。头发顶 y4；真实肤色颏 y20，下面 y21 为短胡茬/领口暗边，不把胡须垂尾计头长；足底 y37。肤色颏口径17头+17余身，暗边口径18+16，±1px边界差异保留。颅部宽 x9..24 共16px；披肩约 x9..24，未把指示杆或手掌算肩宽。颈没有独立长柱，颏下直接接领。

保留偏瘦成年导者、芥黄短披肩、橄榄短衣、棕斜包、蓬松棕发、小胡须。双手放下闭合；单朴素指示杆斜向下，不是法杖/武器。与原生NPC相比，头块、短颈与紧凑腰腿已接近本次目标；仍是原创研究候选，面部与杆语义需独立视觉QA/用户审阅，不能由20色或17/17数字判定完成。

未画警报、武装领袖、魔法、访客相信或退款。其他朝向、动画、碰撞、引擎透视、运行及本地vanilla版本均未验收；社区原生图只作参考。

## 复现与溯源

运行 `python Assets/RedrawStudies/20261013/chiler/build_native.py --out /tmp/chiler-check`。脚本只读concept/reference及卡，写指定输出，不改输入。默认输出当前研究目录，重跑同名派生物为确定性结果。imagegen本身不承诺逐字节重现，保留原始生成PNG。

`pixel_edits.json`记录alpha阈值、裁切/采样、材料palette及全部10次局部坐标编辑前后色值；不是拿缩小限色替代结构重绘。`manifest.json`记录prompt、全部输入和产出SHA256、脚本SHA及未修改范围。已在独立/tmp目录重跑，manifest逐字节一致。

## 独立QA后的v2局部修整

`QA-independent.json`支持17/17结构及单指示杆，但指出v1的x11,y7与x12,y18透明针孔。v1原样保留，`build_native_v2.py`仅额外填这两处发簇针孔，生成`chiler_native_v2.png`及对应1x/8x、`comparison_landmarks_8x_v2.png`和v2日志/清单；没有再调比例或增加脸部细节。v1日志10条操作实际8处颜色改变+2处no-op；v2共12条操作、10处实际改变。v2完整manifest在独立/tmp/chiler-reproduce-v2重跑一致。

独立审阅限制：1x下小胡须与嘴/暗颏不完全可分辨，作为稀疏像素语义保留，不能夸大为细节完全通过。当前推荐审阅v2，仍非最终生产验收。
