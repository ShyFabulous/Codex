---
type: troubleshooting
project: Knowledge Base Operations
status: resolved
date: 2026-07-02
tags:
  - topic/obsidian
  - topic/github
  - topic/git
  - topic/sync
  - issue/resolved
---

# Obsidian Git Upstream Branch Issue

## 问题现象

安装 Obsidian Git 插件后，频繁弹出：

```text
Aborted. No upstream-branch is set!
No commits to push
Pull: Everything is up-to-date
```

## 信息解读

其中：

- `No commits to push`：正常提示，表示没有需要推送的提交。
- `Pull: Everything is up-to-date`：正常提示，表示远程和本地已同步。
- `No upstream-branch is set!`：需要修复，表示插件没有正确识别本地分支对应的远程分支。

## 根本原因

Obsidian Git 插件在执行自动 pull / push 时，需要知道当前本地分支追踪哪个远程分支。

如果插件读取不到 tracking branch，就会尝试让用户选择 upstream branch；如果选择流程被取消或插件状态没刷新，就会弹出：

```text
Aborted. No upstream-branch is set!
```

虽然命令行后续可能已经显示：

```text
main...origin/main
```

但插件仍可能保留旧状态，或在自动同步周期中继续弹出历史提示。

## 最终解决方案

### Step 1：显式设置 upstream branch

```bash
cd "/Users/shy/Desktop/Obsidian Basement/Codex"
git branch --set-upstream-to=origin/main main
```

### Step 2：设置 Git 自动建立远程追踪关系

```bash
git config push.autoSetupRemote true
```

### Step 3：验证追踪关系

```bash
git branch -vv
git rev-parse --abbrev-ref --symbolic-full-name @{u}
```

期望结果：

```text
main [origin/main]
origin/main
```

### Step 4：减少 Obsidian Git 无意义弹窗

插件配置文件：

```text
.obsidian/plugins/obsidian-git/data.json
```

加入：

```json
"disablePopupsForNoChanges": true,
"showErrorNotices": true
```

保留真正错误提示，但减少“没有变化”“已经最新”这类正常提示。

## 当前验证结果

当前本地分支状态：

```text
main...origin/main
```

当前 upstream：

```text
origin/main
```

说明本地 `main` 已正确追踪远程 `origin/main`。

## 如果再次出现

按顺序处理：

1. 重启 Obsidian，或关闭再启用 Obsidian Git 插件。
2. 在命令行执行：

```bash
git branch -vv
git status --short --branch
```

3. 如果 upstream 丢失，重新执行：

```bash
git branch --set-upstream-to=origin/main main
```

4. 如果出现认证问题，参考 [[GitHub Token Authentication Issue]]。

## 长期建议

- 保持本地分支固定为 `main`。
- 不要频繁删除 `.git/config` 或切换远程地址。
- Obsidian Git 自动同步成功后，日常主要通过插件备份；重大结构调整后手动检查一次 `git status`。

