# 多罗 / doro 头像重绘候选

2026-10-15。当前只交头像美术候选，未覆盖原图、人物卡或游戏代码，未接入运行包，不 commit/push。身份预检见 spec_lock.md 与 qa/identity_preflight.json；全部输入来源与 SHA 见 sources/source_manifest.json。

## 生成与派生

使用内置 image_gen.imagegen 实质重绘，一人一张首稿，最多一张针对性修订。prompts 保存完整调用参数；tool_returns 保存原始完整返回；raw 是返回图像数据原字节保存。身份母版和四核心风格图均先实际查看；四核心只作为像素块面/构图风格，不复制其脸。

74×100 是技术派生：对 raw 整幅画布等比缩放，Pillow NEAREST 取样，必要时居中透明补边；alpha 阈值128；从可见目标像素取 MEDIANCUT 调色板，32色上限、无抖动，透明像素清零。未局部扭曲、补画、删簇、裁头或改变几何；尺寸整数量化带来的小于一像素舍入会明确记录。不能将这套派生称作原生74×100逐像素绘制，32色仅本批临时上限。

## 复现

环境：Python 3，Pillow 12.3.0。在任意工作目录运行 python 此目录/derive_portrait.py portrait_v1（若最终选择v2，则改为portrait_v2）。该脚本直接从保存的tool_returns重新生成raw、candidates、previews、技术QA、manifest与SHA256SUMS。生成模型不提供可复现随机种子；归档的精确提示词、输入图和原始返回可复现技术导出，不能保证重新生图字节一致。

1x预览为原尺寸；8x是整数nearest-neighbor，1x_8x审阅板含深灰/中灰/浅底和四核心2x。最终选稿与独立QA状态以manifest为准，数值合格不代表审美或游戏验收。

## 最终技术安全留边

独立QA终选 v2，同一raw等比NN缩放到72×98内框（整数采样结果72×97），居中放74×100，完整保留四边透明边。原v1/v2技术导出均保留，新增安全版不计第三次生图。最终 selected 为 candidates/portrait_v2_safe_74x100_candidate.png。

复现最终结果依次运行：python derive_portrait.py portrait_v2；python derive_safe_portrait.py；python finalize_manifest.py。最后一项只刷新清单与SHA，不改图像。剩余风格限制见manifest和独立QA；并未由量化变成原生像素手工稿。
