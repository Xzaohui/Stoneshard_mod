# Purple Crystal HD-2D — R01 Design Spec

## I. Project Information

布林外围Mod原创场景：灰堤工营、旧渠泵房与下层墓龛。角色仅预留空间。

## II. Canvas Specification

26×26格；工营40×30，旧渠52×34，墓室36×28。尺寸与独立精灵见spec_lock.md。

## III. Color Palette

BRY-R01-128，从既有布林Mod概念图提取128色，全HEX保存在spec_lock与palette JSON。

## IV. Art Style Definition

原作方向的正交斜俯视HD-2D，盐灰石、湿砖、褐木、低饱和水；左上基础光。

## V. Asset List

三幅场景母图、独立建筑与环境物件；地图、场景、结构、屋顶/前景分层导出。

## VI. Animation Specification

单帧静态；移动灯光与水/门动画不在本批。

## VII. Technical Constraints

几何为制作提案，源自台本约束；不改NPC、任务状态或安装包。固定门点与干地回程分别验收。

## VIII. Platform Export Notes

GameMaker RGBA PNG、原点、相对路径、占地和通路掩码；导入后仍需原生转场/相机/碰撞测试。
