---
type: guide
system: research-cleaner
tags:
  - workflow/research-cleaner
---

# Research Cleaner Guide

脚本位置：`_system/scripts/research_cleaner.py`

## 已支持

- 自动处理 `00-Inbox/Downloaded/*.md`
- 自动识别标题
- 自动识别第一个来源链接
- 自动选择主分类目录
- 自动生成 topic 标签
- 自动加入 Topic Hub 引用
- 自动整理 Markdown 空行、列表间距
- 保留全部原文
- 不删减、不总结、不改写观点

## 输出

- 清洗副本：`00-Inbox/Cleaned`
- 归档副本：`04-Research/<主分类>`

## 执行

```bash
python3 _system/scripts/research_cleaner.py
```

