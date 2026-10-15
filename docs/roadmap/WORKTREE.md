# 稀疏工作树方案（2026-10-16）

磁盘曾因 6 个完整工作树各复制约 9.3G 的 `Assets/` 而占满。此后并行开发必须用稀疏检出，只拉归属目录。

## 现成工作树

| 路径 | 分支 | 助手 | 典型体积 | 含 `Assets/`？ |
|---|---|---|---|---|
| `/workspace/projects/Stoneshard_mod` | `main` | 协调、合并、实机构建 | ~全量（含 Assets） | 是 |
| `/workspace/projects/wt-code` | `work/code` | 代码 | ~0.8G | 否（含 `src/EmbersAndOaths/Assets` 嵌入资源） |
| `/workspace/projects/wt-story` | `work/story` | 文案 | ~20M | 否（且不含 `design/12_美术参考`） |
| `/workspace/projects/wt-art` | `work/art` | 绘图 | ~11G | 是（全库唯一的第二份 Assets） |

`/workspace/projects/map-plan`（`code/map-plan`）为临时代办，推完大地图方案后移除。

## 新建配方

```bash
# 代码（示例）
git worktree add --no-checkout /workspace/projects/wt-code -b work/code main
cd /workspace/projects/wt-code
git sparse-checkout init --cone
git sparse-checkout set \
  src/EmbersAndOaths tools research/tools research \
  docs/roadmap WORK-CLAIMS.md README.md AGENTS.md CHANGELOG.md
git checkout

# 文案（非 cone，排除美术参考与 Assets）
git worktree add --no-checkout /workspace/projects/wt-story -b work/story main
cd /workspace/projects/wt-story
git sparse-checkout init --no-cone
git sparse-checkout set \
  '/*' '!/Assets/' '!/Assets/**' '!/src/' '!/src/**' '!/output/' '!/output/**' \
  '!/tools/' '!/tools/**' '!/design/12_美术参考/' '!/design/12_美术参考/**' \
  '/design/' '/research/' '/docs/' \
  '/README.md' '/AGENTS.md' '/CHANGELOG.md' '/WORK-CLAIMS.md'
git checkout

# 绘图（必须含 Assets，全库只此一份副本）
git worktree add --no-checkout /workspace/projects/wt-art -b work/art main
cd /workspace/projects/wt-art
git sparse-checkout init --cone
git sparse-checkout set \
  Assets src/Art src/EmbersAndOaths/Assets output design/12_美术参考 \
  research docs/art docs/roadmap README.md AGENTS.md CHANGELOG.md WORK-CLAIMS.md
git checkout
```

## 规则

1. 禁止再为非绘图任务检出完整 `Assets/`。
2. 合并、推送前在各自分支提交，再经 main 快进或 PR；不要在 main 工作树上直接改功能。
3. 构建：MSL/`data.win` 在 main 或 wt-code 完成；根目录 `Assets/` 是美术参考，嵌入资源在 `src/EmbersAndOaths/Assets/`。
4. 用完临时工作树：`git worktree remove --force <路径>`，并删除对应本地分支。
