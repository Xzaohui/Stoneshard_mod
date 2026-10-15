# sena 对白头像重绘审阅候选

独立视觉QA选择 portrait_v2 为 candidate，本角色生成已停止。这是待用户审阅的候选，不是用户终稿认可。

## 当前选定

- candidates/portrait_v2_74x100_candidate.png
- SHA256：e0cb364a66995a8a43cb234516179352fb1549f499b16bb709bc1a2797a1c4b9
- 非阻断余项：围巾约底部16px仍略厚；非阻断。

## 制作与审查

- 目标74×100 RGBA；本批临时预算≤32可见RGB色，alpha 0/255。
- 实质绘画由内置image_gen.imagegen完成。raw为工具返回PNG字节原样存档，tool_returns保存完整结果，prompts保存实际工具参数及完整prompt。
- candidates为整幅NEAREST缩放、alpha≥128阈值和无抖动MEDIANCUT量化的技术派生。没有程序代画人物或局部修像素，不宣称原生逐像素完成的74×100作品。
- previews提供1x三底色与8x整数最近邻检视；qa含作者观察、技术指标和独立结论记录，独立审计报告位于../independent_qa/batch02/QA_REPORT.md。
- sources含当前人物卡、旧身份母版及QA、风格参考、冻结派工revision2与来源SHA；初始派工快照只作历史溯源，年龄以revision2和最新卡优先。
- 未覆盖旧图、人物卡、代码或其他角色；未入游戏、未提交或推送。

## 生成次数

2次。v1保留；唯一v2针对脸占比、短颈、眼白与成熟年龄进行imagegen修订。
