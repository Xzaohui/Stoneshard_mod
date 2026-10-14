# 忒曼：两种表情概念

FX-HNY / teman，五十来岁养蜂人。E1「说蜂会笑」与E2「亡巢敛笑」均为可逆表演提案。

- 使用 builtin image_gen.imagegen，两次首稿；无修订。
- prompts/ 保存真实逐字prompt，requests/ 保存实际调用参数，returns/ 保存工具返回值（含原image_url和原output_hint）；generation-log.json 绑定时间、路径与SHA。
- raw/ 保存全部原图；selected/为原图逐字节复制，保留生成alpha。原图alpha0下的隐藏RGB不能作为可见背景，qa/提供真实浅深合成。
- review/ 两块中文对照板仅做等比例展示合成；没有拉伸、量化或重绘身体。
- sources/含母图、当前卡/台本和brief快照、SHA索引。
- 作者已实际查看母图、两raw、两selected、浅深合成和中文浅深板；独审待回执。
- 本批不表示任务完成、关系变化或游戏落地，不封包、不上传、不提交git。

## 最终冻结

2026-10-14T02:36:49.503494+00:00：raw视觉与透明选稿/展示板独审均通过，作者完成终态冻结。两张均选v1，硬错修订0次。历史候审状态保留阶段记录；当前终态以FINAL_STATUS.json为准。
