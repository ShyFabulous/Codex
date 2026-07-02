---
type: guide
system: audit
tags:
  - workflow/kb-audit
---

# Knowledge Base Audit Guide

脚本位置：`_system/scripts/kb_audit.py`

## 检查范围

- 重复内容
- 分类冲突线索
- 异常文件名
- 空目录
- 垃圾文件
- 孤立 Markdown 文件
- 高频标签

## 输出位置

`_system/reports/kb-audit-*.md`

## 执行

```bash
python3 _system/scripts/kb_audit.py
```

