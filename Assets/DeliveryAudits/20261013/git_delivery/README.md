# 当前美术资源 Git 归档（2026-10-13）

按既有目录全量归档当前资源，原图、原稿、源包、制作提示词、清单、QA、交付回执和历史候选均保留。此目录是独立的 Git 交付说明，不修改任何既有冻结清单或包内哈希。

## 范围

- `src/EmbersAndOaths/Assets/ConceptDrafts/20261012/`：既有概念批次与制作来源。
- `src/EmbersAndOaths/Assets/PixelPilots/20261013/`：像素试点。
- `output/pixel-production/`：本项目的制作 brief、批次脚本和审计脚本，作为相关源资料保留。
- `Assets/CharacterDesigns/`：人物概念、表情、转面、原始候选与源包。
- `Assets/CharacterActions/`：动作／姿态候选、来源、交付包、QA 与历史状态记录。
- `Assets/RedrawStudies/`、`Assets/ReferenceAudit/`、`Assets/DeliveryAudits/`：重绘研究、参考审计、完整性记录。

原有资源共 6,001 文件，2,676,809,481 字节，其中 83 个 ZIP 共 655,118,042 字节。本说明和新增逐文件清单不计入原资源数量。仅忽略 Python 字节码缓存；不删除本地文件。原先通用 `*.zip` 忽略保持，83 个已审查项目源包显式加入 Git。未引入 Git LFS 或新服务配置。

## 合并与来源

云端原 checkout 基线：`39a466fac4024282a23b30ddbc357d80fc773a9e`。
先拉取并 fast-forward 纳入远端的九个已有提交至 `ad1b49c347a340a0b12a6c7a19205b6e0ce17fee`；远端更新与待归档资源没有同路径冲突。远端代码、剧情、人物卡和资源变更完整保留。

艺术目录里的 `sources/`、创作提示词、manifest 与 QA 来源 SHA 属于创作时快照。它们不随最新故事／人物卡改写；每份资源的来源以原清单为准。归档不改变已交付图、ZIP、回执或冻结记录的字节。Git 不存储文件系统 xattr，Library 身份元数据未另行导出。

## 验证与限制

`asset_bytes_manifest.json` 登记原有每份文件的路径、字节数与 SHA-256，供本地和 Git blob 校验。克隆后可运行 `python Assets/DeliveryAudits/20261013/git_delivery/verify_archive.py`，只读重算全部 6,001 份资源；本次归档前复核零差异。归档前检查常见密钥、凭据、带认证 URL 和签名下载地址模式，并对所有 ZIP 成员作内容扫描；无命中。83 个 ZIP 全部成员读取成功。

概念、表情和动作图仍是各原交付记录所标注的状态。167 人物概念与 16 人／46 表情不等于完成最终运行精灵；走路／呼吸连续性、静态五闸与游戏运行情况继续按原报告，不因提交成功升级验收状态。本次仅保存和远端归档，不执行生图、重新制作、游戏构建、部署或实机验收。

分四批普通提交与推送：概念／像素试点与源稿、人物设计、人物动作、审计／重绘与此交付清单。每批原文件总量低于 2 GiB，不使用 force push。
