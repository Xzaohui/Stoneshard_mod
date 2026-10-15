# 玛娅·禾 / Maya He 头像重绘候选

选择：`candidates/portrait_v2_74x100_candidate.png`。

- 实际 imagegen 生成两次：v1 初稿 + 一次必要的 v2 修订，已停止追加生成。
- 全部 raw、完整工具返回、逐次 prompt/参数与来源卡/旧母版/历史 QA/风格锚点快照保留。
- 当前候选为 74×100，二值 alpha，最多 32 可见工作色；该上限为本批临时工作预算。
- `previews/portrait_v2_1x_8x.png` 提供黑/灰/浅底 1× 与 8× NN 放大；`previews/portrait_v2_8x.png` 为独立放大预览。
- 来源卡与原母版已逐项核 SHA。旧图、人物卡、源码均不覆盖。

## 独立选择

v2 MEDIANCUT 优于同 raw MAXCOVERAGE，鼻颧大平面更连贯，后者额/颊/下巴有碎斑；v2脸部放大、露颈收紧、灰巾大折改善，温厚闭口轻笑与稳眉保住，四十多岁可读。

非阻断备注：眼白与皮肤略同色。；局部轮廓偏柔。；紧裁切让围裙不入镜。

正式 QA：`../independent_qa/batch04/QA_REPORT.md`、`selection.json`、`independent_measurements.json`。本角色汇总见 `qa/independent_selection_summary.json`。

## 复现

依赖 Python + Pillow。按顺序执行：

```
python derive_portrait.py
python export_maxcoverage.py portrait_v2
python finalize_manifest.py portrait_v2
```

`derive_portrait.py` 将完整 tool return 的图像字节原样还原为 raw；对整幅画布做 NEAREST 74×100、alpha>=128 二值化、可见 RGB 的 MEDIANCUT 32 色无抖动量化。`export_maxcoverage.py` 对相同 raw 做 MAXCOVERAGE 对照；没有新画人物几何或手工补脸。再生成 1×/8× 预览及指标。

## 限定

这是 imagegen 重绘的像素风头像研究候选和明示技术派生，不是原生逐像素手绘终稿，不以色数合格代替视觉批准。未导入游戏、未进行运行验收，无装备层/动作适配声明。保留未选版本供溯源；不提交、不 push。
