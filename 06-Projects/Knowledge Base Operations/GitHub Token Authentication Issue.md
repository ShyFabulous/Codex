---
type: troubleshooting
project: Knowledge Base Operations
status: resolved
date: 2026-07-02
tags:
  - topic/github
  - topic/git
  - topic/authentication
  - issue/resolved
---

# GitHub Token Authentication Issue

## 问题现象

在将 Obsidian Vault 推送到 GitHub 时，出现认证失败：

```text
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/ShyFabulous/Codex.git/'
```

随后又出现网络层错误：

```text
fatal: unable to access 'https://github.com/ShyFabulous/Codex.git/': Error in the HTTP2 framing layer
```

## 根本原因

### 1. GitHub 不再支持账号密码推送

GitHub 的 HTTPS Git 操作不能使用 GitHub 登录密码作为 password，必须使用 Personal Access Token、GitHub CLI、SSH key 或其他受支持的凭据方式。

### 2. 新 token 最初没有仓库权限

截图显示：

```text
This token does not have access to any repositories.
This token does not have any repository permissions.
```

这说明 token 是“空权限 token”，不能访问 `ShyFabulous/Codex`，因此 push 会失败。

### 3. macOS 钥匙串可能缓存旧 token

本机 Git 使用：

```text
credential.helper=osxkeychain
```

如果旧 token 已撤销但钥匙串仍缓存旧凭据，Git 可能继续使用旧 token 导致认证失败。

### 4. HTTP/2 链路异常

`Error in the HTTP2 framing layer` 属于 Git 与 GitHub 之间的 HTTP/2 网络/兼容性问题，常见于代理、VPN、网络链路或 Git/libcurl 组合。

## 最终解决方案

### Step 1：撤销已暴露旧 token

旧 token 一旦出现在聊天、截图、日志或网页中，应按已泄露处理，必须 revoke。

### Step 2：重新生成 fine-grained token

权限最小化：

- Repository access：只选择 `ShyFabulous/Codex`
- Repository permissions：
  - Contents: Read and write
  - Metadata: Read-only

不要开启不必要权限：

- Administration
- Actions
- Secrets
- Workflows
- Issues
- Pull requests

### Step 3：清除 macOS 钥匙串里的旧 GitHub 凭据

```bash
git credential-osxkeychain erase
```

输入：

```text
protocol=https
host=github.com

```

最后需要一个空行。

### Step 4：解决 HTTP/2 framing layer 问题

```bash
git config --global http.version HTTP/1.1
```

### Step 5：重新 push

```bash
cd "/Users/shy/Desktop/Obsidian Basement/Codex"
git push -u origin main
```

Username：

```text
ShyFabulous
```

Password：

```text
粘贴新的 GitHub token
```

终端不显示 token 字符是正常现象。

## 验证结果

最终出现：

```text
Writing objects: 100% ... done.
To https://github.com/ShyFabulous/Codex.git
* [new branch] main -> main
branch 'main' set up to track 'origin/main'.
```

说明：

- 本地 Vault 已成功推送到 GitHub。
- 远程 `main` 分支已建立。
- 本地 `main` 已追踪 `origin/main`。
- 后续可以直接使用 `git push` / `git pull`。

## 长期建议

优先使用：

```bash
brew install gh
gh auth login
```

或改用 SSH key，以减少 token 明文输入和钥匙串缓存问题。

