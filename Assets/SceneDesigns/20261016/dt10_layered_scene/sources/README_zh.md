# A01 布林码头小院：右侧仓棚分层美术小样

2026-10-16。依照 A01 整景右侧仓棚与主屋 v3 的材料/分层方式，新绘了三类独立透明图层。所有绘画由内置 image_gen 完成，共三次初稿，没有二次美术重绘。之后只用 ImageMagick 进行 alpha 边缘清理、最近邻缩放、整数平移和真实 source-over 合成。

## 先看

- `previews/three_layers_actual_stack.png`：灰底真实叠合。
- `previews/three_layers_actual_stack_transparent.png`：透明底真实叠合。
- `previews/roof_off_on_actual_comparison.png`：左侧揭顶、右侧盖顶，同一主体与货物位置。
- `previews/three_layers_separate_gray.png`：左主体、中屋顶、右货物。仅此排列图缩小为每格 768×512。
- `previews/left_eave_inspection.png`、`right_eave_inspection.png`：左右檐口与柱梁接合放大。
- `previews/cargo_ground_inspection.png`：货物落地与柱脚关系。

## 透明交付层

全部为 **1536×1024 RGBA PNG**，把左上角 (0,0) 对齐即可使用本次位置关系。所有交付层 alpha 均为 0/255。

1. `layers/01_body.png`：完整无顶主体，含柱梁、斜撑、背墙、侧向结构、石脚和浅抬高石地台。没有桶箱袋；屋顶下的背墙与结构已补画。
2. `layers/02_roof.png`：单独木板斜棚顶，可整层隐藏。没有柱、墙、地台或货物。
3. `layers/03_cargo.png`：两组桶箱袋的合并透明层，没有地台或建筑。
   - `layers/03a_cargo_left.png`：左侧一桶、一箱、两袋。
   - `layers/03b_cargo_right.png`：右侧一桶、一箱、一袋。

实际组合顺序：主体 → 货物 → 屋顶。揭顶时只隐藏屋顶。货物合并层和两个子层是替代用法，不要同时重复叠加。货物均摆在柱间，未覆盖前柱。

## 实际美术检查

- 棚顶后缘、两侧和前檐覆盖后排柱头及顶部框架；前檐与前柱/横梁接合，没有透明断带或悬空屋顶。
- 屋顶隐藏后，背墙和地台完整保留，不会出现由遮挡造成的空洞。
- 两组货物的底部接在可见地台石面上，没有落在地台外或遮住柱脚；主体没有重复货物。
- 屋顶三处前柱头与四处后柱头抽样像素为全不透明。抽样只辅助目视检查，不是全轮廓自动证明。
- 整张叠合与揭顶对比均由交付图层真实 alpha 合成，没有再次生图冒充叠合。

## 来源、记录与限制

- `raw/`：三张 image_gen 原始 PNG，保留未修改版。
- `prompts/`：三次完整提示词。
- `sources/`：A01 整景、右棚局部、主屋风格图、主屋分层方法与旧 spec_lock 的只读快照。局部参考由整景裁切，仅作参考，交付主体/屋顶/货物不是从整景程序抠图。
- `TRANSFORMS.txt`：可复现的缩放、定位、透明清理和叠合操作。
- `generation_manifest.json`：绘制来源和输出说明。
- `art_review.json`：尺寸、透明范围、抽样位置和人工检查结论。
- `SHA256SUMS.txt`：本次交付与源文件哈希。

本次是分层美术小样，不声称满足原生像素、26px 网格或 ≤128 色生产规格；没有新建或修改校验器，没有改代码、游戏包、碰撞/锚点或接入，没有运行游戏验收，没有 push。旧建筑 spec_lock 未修改。
