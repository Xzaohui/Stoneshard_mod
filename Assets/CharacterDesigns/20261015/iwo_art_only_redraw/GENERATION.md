# 生成记录

- 工具：内置 `image_gen`；未使用 CLI、外部付费 API 或新增软件。
- v1：`prompts/iwo_map_v1.txt`，五张引用依次为身份头像、Bert、Frid、Jurg、hers_native_v2。`transparent_background=false`。返回文件 `generated_images/exec-3cc96c6c-e81f-4f3b-986c-6c936016b166.png`。原始尺寸1119×1406 RGB。SHA256：3af6aa5df8909aa110e44bea7d986e76b1a797cf827c6c6d75885adabe79c81a。
- v2：`prompts/iwo_map_v2.txt`，三张引用依次为本轮v1、Bert、Jurg。`transparent_background=false`。只要求简化格数与紧凑比例，同时保留身份和静立姿态。返回文件 `generated_images/exec-2fdae47a-eb41-4195-a2b8-5f8861183923.png`。原始尺寸1119×1406 RGB。SHA256：39029bc8bfb8ab33c9839af4d3de2050acb78a12a083cc60623417b1f0a3bb80。
- 展示候选是v2原字节复制，不是缩小、取格、抠底或重绘派生。
- 两张原始输出及最终落盘展示候选均已实际查看。达到本轮最多一次修订上限后停止；35×44原生像素目标尚未达成。
