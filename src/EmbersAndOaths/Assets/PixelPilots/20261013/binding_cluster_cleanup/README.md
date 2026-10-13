# 装订孔对齐：有限色簇清理实验

本目录独立于已经通过几何检查的 `../binding_alignment/native-study/`，旧目录只读，没有覆盖旧成品。仅一次重绘 A/B 固定图层的 RGB；不修改 alpha、纸张外轮廓、三个孔的坐标/尺寸、A 位置、B 刚体平移或下层露边。不是游戏运行验收或最终尺寸定稿。

## 美术处理与实际审图

- 原版整个纸面充满相邻近色及细碎单像素纹理；新候选改为平静的大底色、上左侧浅色块、阶梯式边角磨损及极少边缘色簇，不添加文字、符号或叙事证据。
- 共享不透明色（含背景）21 → 8；A 使用 4 色，B 使用 3 色，背景 1 色。是视觉分工结果，不以机械量化凑色数。
- A RGB 变更 11,263 像素，B 变更 8,572 像素。全部 alpha 和透明区 RGBA 变更为 0。
- 按同色四连通统计，A/B 单像素色簇 3,428/3,305 → 0/0；2–4 像素色簇 1,404/1,290 → 0/0。没有用删除 alpha 来消除合法边沿。
- 已实际查看原 sheet 和新旧 2x 对照。新稿纸面、三孔、对齐过程和最终右侧下层露边更容易辨认；整体更平、更图标化，纸纤维/旧化的写实感有所降低。这是有限色簇风格候选，不能仅凭低色数宣布美术最终通过。

## 文件

- `comparison_before_left_after_right.png` / `comparison_nearest_2x.png`：左旧右新，均按原 2×2 四帧顺序。
- `frame_00.png` 至 `frame_03.png`：256×256 四帧。
- `spritesheet.png`：512×512；`spritesheet_nearest_4x.png` 只用最近邻放大。
- `motion.gif`：四帧，1000/400/400/1600 ms；解码回读逐帧 RGB 完全一致。
- `layer_A.png`、`layer_B.png`、`mask_A.png`、`mask_B.png`：固定图层与原样掩码。
- `RGB_changes_A.png`、`RGB_changes_B.png`：仅 RGB 变更位置，白色表示改动。
- `manifest.json`：旧源树全文件 SHA-256、前后调色板、像素变更、色簇统计、逐帧位置与固定层哈希。
- `QA-readback.json`：独立脚本重新读取导出，验证源树、全部掩码、三孔、逐帧固定层重建、A/B/背景归属掩码、GIF 及 sheet。
- `QA-reproducibility.json`：临时目录重跑，17 个 PNG/GIF 与 manifest 共 18 文件逐字节一致。

## 复现

使用已安装 Pillow / NumPy / SciPy，不安装依赖。从本目录运行：

    python build_cleanup.py
    python verify_cleanup.py

也可 `python build_cleanup.py --out /tmp/binding-cluster-repro`，不会写入旧目录。未修改 runtime、全局设置、游戏包；无提交、推送或部署。
