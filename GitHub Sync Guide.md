---
type: guide
system: sync
tags:
  - workflow/github-sync
  - topic/github
---

# GitHub Sync Guide

## 当前配置

- 本地 Git 仓库：已初始化
- 远程仓库：`https://github.com/ShyFabulous/Codex.git`
- 分支：`main`
- Obsidian Git 插件配置：已预置到 `.obsidian/plugins/obsidian-git/data.json`

## 安全规则

不要把 GitHub token、API key、账号密码写入笔记、脚本或 Git 配置。

你已经在聊天里暴露了一个 GitHub token。请在 GitHub 后台撤销它，并重新生成一个只用于 Git 操作的最小权限 token。

## 手动认证建议

优先方案：安装 GitHub CLI 后登录。

```bash
brew install gh
gh auth login
```

备选方案：使用 Obsidian Git 插件或 Git Credential Manager 保存凭据。

## 常用命令

```bash
git pull --rebase origin main
git add .
git commit -m "vault backup"
git push origin main
```

如果远程仓库已有内容，第一次同步前先执行 pull，避免覆盖远程历史。

