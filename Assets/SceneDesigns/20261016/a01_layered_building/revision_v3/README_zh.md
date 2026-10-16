# A01 主屋分层校准 v3

2026-10-16。已完成本次美术小样的分层位置校准与真实叠合检查。主体原图保持不变；屋顶与附件采用确定的图层缩放、平移和透明边缘清理。没有重新生图、扭曲、绘制新像素、修改游戏代码或push。

## 快速查看

- `previews/roof_off_on_actual_comparison.png`：左揭顶、右盖顶。同一主体、同一位置。
- `previews/three_layers_actual_stack.png`：灰底真实叠合。
- `previews/three_layers_actual_stack_transparent.png`：透明底真实叠合。
- `previews/three_layers_separate_gray.png`：主体、合并屋顶、附件三层。
- `previews/roof_sublayers_separate_gray.png`：主顶、左棚顶、右棚顶三个独立子层。

## 透明 PNG 图层

所有图层均为1536×1024，左上角(0,0)重叠即可使用本次位置关系，不需要额外移动。

- `layers/01_body_unchanged.png`：无屋顶主体与已补绘内部、门窗、石阶。逐字节保留第一版主体。
- `layers/02_roof_aligned.png`：三子顶的预合并版本，可整体揭顶。
- `layers/02a_main_roof.png`：独立主屋顶。
- `layers/02b_left_roof.png`：独立左棚顶。
- `layers/02c_right_roof.png`：独立右棚顶。
- `layers/03_foreground_aligned.png`：前景附件合并版本。
- `layers/03a_bench.png`：独立长凳。
- `layers/03b_barrel_crate.png`：独立桶箱。

屋顶组合顺序：左棚顶、右棚顶、主顶。完整组合顺序：主体、合并屋顶、合并附件。不要同时叠合“合并版本”和它的“子层”，以免重复。

## 实际检查结果

- 主屋后墙与左右棚房原先成条外露的内部区域已被覆盖。检查了整张真实叠合、左右檐口放大图和指定覆盖点。
- 前V覆盖山墙最高处；二层窗中心与中央门洞不被屋顶覆盖。
- 左右棚顶的剪切接缝放在主顶下面重叠，没有把整景程序抠图当作绘画。
- 长凳从v2精确下移14px，透明轮廓外框为(428,751)至(628,831)，最后不透明像素行y830。
- 桶箱从v2精确下移19px，外框为(1113,671)至(1290,800)，最后不透明像素行y799。
- 主体SHA-256仍为 `1dd79fb7bd2772f67984a69edc4644a16ff5886288b121323289e9f938660398`。
- 屋顶与附件alpha已整理为0/255；主体按要求不改，仍保留原半透明alpha。因此不能把整套说成已满足二值alpha生产标准。

覆盖点是抽样证据，不是全轮廓自动证明。最终细部风格/比例仍可进行美术评审。本次不宣称26px网格、≤128色、游戏碰撞/锚点、接入或运行验证已经完成。

## 来源与边界

绘画来源保持前两版：主屋主体与附件由image_gen独立绘制，主体补齐被屋顶遮住的内部。A01整景只作构图/材料参考。完整生成提示词及原始图在父目录和revision_v2中，未覆盖。

本轮使用ImageMagick 7.1.1-43，仅做选区分层、最近邻缩放、整数平移、alpha阈值清理和source-over合成。没有用Python编辑图像，也没有变形网格、透视变换或补画新纹理。技术选区与试稿在work/，不属于绘画交付层。

精确操作记录见 `TRANSFORMS.txt`；尺寸/alpha/检查点见 `alignment_review.json`；哈希见 `SHA256SUMS.txt`。
