---
type: workflow
system: inbox
tags:
  - workflow/collection
---

# Research Collection Workflow

```text
Web / PDF / Newsletter / Social Post
        ↓
Web Clipper or MarkDownload
        ↓
00-Inbox/Downloaded
        ↓
Research Cleaner
        ↓
00-Inbox/Cleaned
        ↓
04-Research/<主分类>
        ↓
Topic Hub + 标签 + 内部链接
        ↓
05-Content / 97-AI-Memory / 98-AI-Context
```

执行清洗：

```bash
python3 _system/scripts/research_cleaner.py
```

执行巡检：

```bash
python3 _system/scripts/kb_audit.py
```

