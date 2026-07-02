---
type: workflow
system: markdownload
tags:
  - workflow/markdownload
---

# MarkDownload Workflow

```text
MarkDownload
    ↓
00-Inbox/Downloaded
    ↓
Research Cleaner
    ↓
00-Inbox/Cleaned
    ↓
04-Research
    ↓
Topic Hub / Tags / Internal Links
```

## MarkDownload 建议配置

- Download mode: Markdown
- Include frontmatter: yes
- Save images: `00-Inbox/Attachments`
- Default download folder: `00-Inbox/Downloaded`

## 命名建议

`{{date:YYYY-MM-DD}} - {{title}}.md`

