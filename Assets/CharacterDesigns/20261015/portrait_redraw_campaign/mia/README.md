# 米娅头像重绘候选（2026-10-15）

## 当前状态

独立视觉 QA 已选择 v2 MAXCOVERAGE，作为 candidate 冻结；不代表 native_final。最终文件为 candidates/portrait_v2_maxcoverage_74x100_candidate.png，1x/8x 检查图为 previews/portrait_v2_maxcoverage_1x_8x.png。仅人物对话头像，不包含地图站姿、全身或旧 1:1.5 概念图变更。

## 身份

NPC-MIA，三十多岁、独立说话的成年患者。棕色低辫、蓝青披肩与米白病号布衣沿用既有母版。不是护士、治愈者或患者群体代言人。权威人物卡与来源快照见 sources/。

## 输出与复现

- raw/：imagegen 输出原字节；完整返回见 tool_returns/，完整提示词与参数见 prompts/。
- candidates/：74×100 RGBA 候选；previews/：1x 三底色检查与8x整数最近邻预览。
- derive_portrait.py：初稿/修订的整幅 NEAREST 采样、alpha 128 阈值、32 色 MEDIANCUT 无抖动量化。
- derive_maxcoverage.py：v2 同采样同alpha的 MAXCOVERAGE 机械备选，保留小面积蓝青领口；不绘制、修形、补色或重画人物。
- finalize_manifest.py：独立候选选择后更新冻结信息与最终清单。复现顺序为 derive_portrait.py → derive_maxcoverage.py → finalize_manifest.py。
- qa/：机械指标及作者/独立QA记录；manifest.json 与 SHA256SUMS.txt：可追溯文件清单。

## 必须保留的限制

所有实质绘图由内置 imagegen 完成。生成 raw 的实际尺寸为工具输出；74×100 是明确标注的最近邻与无抖动量化派生，不是原生逐像素手工绘制或原生目标尺寸保证。32 色只是本轮工作上限，数字合格不代表调色板层次与像素簇已达到终稿标准。尚未接入游戏、未做游戏运行验证、未提交或推送。旧图与权威人物卡未修改。

## 独立评审结论

v2 的紧脸、压低眼睑与疲惫感、棕低辫及蓝青/米白身份成立。候选残余：眼白仍稍亮、顶发仍有平行纹、材质色阶由量化产生而非手工设计。两次 raw 均与完整工具返回及原生成路径字节一致；v1、v2 MEDIANCUT、v2 MAXCOVERAGE 均由独立审查者逐 RGBA 复现一致。已用初稿与一次修订，不再生图。
