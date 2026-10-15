# 调色板锁登记（阶段 0）

日期：2026-10-15。分支 `art/stage0`。

## 现状
| 批次 | 锁文件 | 校验器读取路径 | 状态 |
|---|---|---|---|
| N1 | `src/Art/hd2d_26x26_20261013/palettes/den_n1_128.json` | `tools/Validate-Hd2dN1.py` | 已用 |
| R01 | `batches/R01-*/palettes/bry_r01_128.json` + `spec_lock.md` | `Validate-Hd2dR01*.py`；N2 组装校验读 `R01-camp-canal-v2/spec_lock.md` | 已用 |
| R02–R06 / BRY | 各 `batches/*/palettes/*.json` + `spec_lock.md` | 对应 `Validate-Hd2dR0x.py` / `Validate-Hd2dBry*.py` | **批次内已有 128 色锁**；校验器因 `tools/vendor/pixel-asset-master-skills` 空目录目前跑不起来 |
| N2（built / hd2d） | 本阶段新增 `src/Art/native-n2-*/spec_lock.md` 与 `palettes/den_n2_128.json` | **仍读 R01 spec_lock**（见下） | 艺术侧已登记；校验器未改路径 |

## 本阶段做了什么
1. 从已验收的 R01-camp-canal-v2 锁复制为：
   - `src/Art/native-n2-built-v1/spec_lock.md`
   - `src/Art/native-n2-hd2d-v1/spec_lock.md`
   - `src/Art/hd2d_26x26_20261013/palettes/den_n2_128.json` / `.gpl`
2. **未改** `tools/Validate-N2SceneAssembly.py`：它仍从 R01 的 `spec_lock.md` 取色。两份内容当前一致，行为不变。
3. R0x / BRY 的锁文件本来就在各 batch 目录里，无需再造一份；缺的是 vendor 子模块内容，不是锁本身。

## 需要代码配合（不在本分支改）
1. 可选：把 `Validate-N2SceneAssembly.py` 的 palette 路径改到 `native-n2-built-v1/spec_lock.md`，让 N2 批次自包含。
2. 修复 `tools/vendor/pixel-asset-master-skills` 与 `ModShardLauncher` 两个 gitlink（当前为空目录，commit `33d891c4…` / `368dfb06…` 未检出）。10 个 Bry/R0x 校验器依赖其中的 `asset_validator.py`。艺术侧不应自行 vendor 第三方代码。

## 验收
- Stage 0 场景修复仍以 `Validate-Hd2dN1`、`Validate-N2SceneAssembly`、`Validate-Hd2dNativeN2`、`Verify-Hd2dPackages` 为准。
