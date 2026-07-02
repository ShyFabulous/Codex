# Lessons Learned

用于记录踩坑、错误假设、修正后的流程。

## 2026-07-02：GitHub token 与 Obsidian Git 同步问题

- GitHub HTTPS push 不能使用账号密码，必须使用 token、GitHub CLI 或 SSH。
- Fine-grained token 必须显式授予目标仓库访问权和 `Contents: Read and write` 权限，否则会显示 token 没有任何仓库权限。
- macOS 钥匙串可能缓存旧 GitHub token，必要时用 `git credential-osxkeychain erase` 清理。
- `Error in the HTTP2 framing layer` 更像网络/HTTP2 链路问题，可通过 `git config --global http.version HTTP/1.1` 解决。
- Obsidian Git 的 `No upstream-branch is set` 可以通过 `git branch --set-upstream-to=origin/main main` 修复。

详细复盘：

- [[06-Projects/Knowledge Base Operations/GitHub Token Authentication Issue]]
- [[06-Projects/Knowledge Base Operations/Obsidian Git Upstream Branch Issue]]
