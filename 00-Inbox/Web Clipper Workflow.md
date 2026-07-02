---
type: workflow
system: web-clipper
tags:
  - workflow/web-clipper
---

# Web Clipper Workflow

## 保存位置

`00-Inbox/Downloaded`

## 模板

使用 [[90-Templates/Research Capture]]。

## 字段要求

- 标题：网页标题
- 来源：URL
- 作者：网页作者或机构
- 时间：抓取时间；如果能识别发布时间，也保留发布时间
- 正文：完整正文

## 后续处理

保存后运行：

```bash
python3 _system/scripts/research_cleaner.py
```

