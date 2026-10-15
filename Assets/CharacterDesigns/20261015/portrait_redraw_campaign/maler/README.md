# 六十余岁男性房主 · maler 头像重绘候选

当前选稿：`candidates/portrait_v1_maxcoverage_74x100_candidate.png`。原图来自built-in imagegen实质重绘，仅一次v1调用；独立视觉QA通过为带非阻断备注的候选，批次最终技术审计待完成。

- `raw/portrait_v1_raw_imagegen.png`：完整工具返回解码，1079×1458，保留原始内容。
- `prompts/portrait_v1.json` 与 `tool_returns/portrait_v1.json`：完整调用参数与返回，包括原始image_url。
- `sources/`：当前卡、旧母版/QA/manifest、当前关联台本、四核心参考及SHA。
- `spec_lock.md`：人物锁定与最新细节优先理由。
- `candidates/`：74×100整幅最近邻缩放、alpha 128阈值、最多32色无抖动派生；MEDIANCUT为对照，MAXCOVERAGE为候选。
- `previews/`：独立8x整数放大与黑/灰/浅底1x、四核心同屏。
- `qa/`：技术指标与作者实际目视备注，独立QA另附。

复现：在本目录运行 `python derive_portrait.py`，然后 `python export_maxcoverage.py portrait_v1`，再 `python finalize_manifest.py portrait_v1_maxcoverage`。生图结果不可确定性重演，工具回执解码和派生可复现；调用不含工具未提供的seed或尺寸参数。

32色是暂定工作上限。不是原生手工像素终稿，不代表用户美术批准、游戏接入或运行验证。旧母版、人物卡及代码均未改动；未提交或推送。

独立视觉QA传回意见见 `qa/independent_feedback_record.json`。最终批次选稿入口为 `../independent_qa/batch07/FINAL_SELECTION.json`，技术审计为同目录 `technical_audit.json`；冻结时尚待审查者落盘，不虚构其哈希。源卡/旧图哈希和raw工具字节一致性已核；在独立临时目录实跑派生并逐PNG字节一致，见 `qa/reproducibility_and_source_integrity.json`。
