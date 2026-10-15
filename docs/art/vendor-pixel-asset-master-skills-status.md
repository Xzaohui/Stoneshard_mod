# tools/vendor/pixel-asset-master-skills 状态（阶段 0 报告）

- 类型：gitlink（`160000`），记录的 commit：`33d891c421a9ad3608f5a09af97271388ca923af`
- 工作区：空目录（无 `.git`、无文件）。同级的 `ModShardLauncher` gitlink 同样为空。
- 仓库无 `.gitmodules`，`git submodule` 无法直接映射。
- 影响：`Validate-Hd2dBryCore/Outskirts`、`Validate-Hd2dR01`–`R06`、`R01Streets`、`SceneCueSync` 共 10 个脚本 import 失败。
- 阶段 0 **不**自行 vendor 第三方代码；请代码 / 小辉补齐子模块检出或改为普通树内依赖。
