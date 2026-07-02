#!/usr/bin/env python3
from __future__ import annotations

import re
import shutil
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
DOWNLOADED = VAULT / "00-Inbox" / "Downloaded"
CLEANED = VAULT / "00-Inbox" / "Cleaned"
RESEARCH = VAULT / "04-Research"

CATEGORY_RULES = [
    ("04-Research/AI/Models", ["gpt", "claude", "gemini", "llama", "model", "模型", "openai", "anthropic", "deepseek"]),
    ("04-Research/AI/Workflow", ["workflow", "工作流", "codex", "claude code", "cursor", "agent"]),
    ("04-Research/AI/MCP", ["mcp", "model context protocol"]),
    ("04-Research/AI/Tools", ["tool", "工具", "app", "插件"]),
    ("04-Research/Integrated-Circuits/Semiconductor-Equipment", ["asml", "lam research", "applied materials", "kla", "光刻", "刻蚀", "薄膜", "量测", "半导体设备"]),
    ("04-Research/Integrated-Circuits/Chip-Design", ["chip", "芯片", "asic", "eda", "soc", "gpu", "npu"]),
    ("04-Research/Compute-Infrastructure/GPU", ["gpu", "nvidia", "amd", "cuda", "hbm"]),
    ("04-Research/Compute-Infrastructure/Data-Center", ["data center", "datacenter", "数据中心", "算力", "电力", "液冷"]),
    ("04-Research/Marketing/SEO", ["seo", "搜索", "关键词"]),
    ("04-Research/Marketing/Growth", ["growth", "增长", "获客", "转化"]),
    ("04-Research/Finance/Macro", ["macro", "宏观", "利率", "通胀", "fomc", "fed"]),
    ("04-Research/US-Stocks/Market", ["nasdaq", "s&p", "美股", "us stocks", "earnings"]),
    ("04-Research/A-Shares/Market", ["a股", "沪深", "创业板", "科创板", "北交所"]),
]

TOPIC_RULES = {
    "topic/codex": ["codex"],
    "topic/claude-code": ["claude code"],
    "topic/prompt": ["prompt", "提示词"],
    "topic/workflow": ["workflow", "工作流"],
    "topic/agent": ["agent", "智能体"],
    "topic/mcp": ["mcp"],
    "topic/obsidian": ["obsidian"],
    "topic/github": ["github"],
    "topic/content-creation": ["公众号", "小红书", "博客", "课程", "content"],
    "topic/marketing": ["marketing", "营销", "增长"],
    "topic/seo": ["seo"],
    "topic/semiconductor": ["半导体", "集成电路", "asml", "tsmc", "smic"],
    "topic/compute-infrastructure": ["算力", "gpu", "数据中心", "hbm"],
    "topic/us-stocks": ["美股", "nasdaq", "s&p"],
    "topic/a-shares": ["a股", "沪深", "科创板"],
    "topic/finance": ["finance", "金融", "宏观", "估值"],
}

HUB_LINKS = {
    "topic/codex": "[[04-Research/Topic-Hubs/Codex Hub|Codex Hub]]",
    "topic/claude-code": "[[04-Research/Topic-Hubs/Claude Code Hub|Claude Code Hub]]",
    "topic/prompt": "[[04-Research/Topic-Hubs/Prompt Hub|Prompt Hub]]",
    "topic/workflow": "[[04-Research/Topic-Hubs/Workflow Hub|Workflow Hub]]",
    "topic/agent": "[[04-Research/Topic-Hubs/AI Agent Hub|AI Agent Hub]]",
    "topic/mcp": "[[04-Research/Topic-Hubs/MCP Hub|MCP Hub]]",
    "topic/obsidian": "[[04-Research/Topic-Hubs/Obsidian Hub|Obsidian Hub]]",
    "topic/github": "[[04-Research/Topic-Hubs/GitHub Hub|GitHub Hub]]",
    "topic/content-creation": "[[04-Research/Topic-Hubs/Content Creation Hub|Content Creation Hub]]",
    "topic/marketing": "[[04-Research/Topic-Hubs/Marketing Hub|Marketing Hub]]",
    "topic/seo": "[[04-Research/Topic-Hubs/SEO Hub|SEO Hub]]",
    "topic/semiconductor": "[[04-Research/Topic-Hubs/Semiconductor Hub|Semiconductor Hub]]",
    "topic/compute-infrastructure": "[[04-Research/Topic-Hubs/Compute Infrastructure Hub|Compute Infrastructure Hub]]",
    "topic/us-stocks": "[[04-Research/Topic-Hubs/US Stocks Hub|US Stocks Hub]]",
    "topic/a-shares": "[[04-Research/Topic-Hubs/A Shares Hub|A Shares Hub]]",
    "topic/finance": "[[04-Research/Topic-Hubs/Finance Hub|Finance Hub]]",
}


def slugify(name: str) -> str:
    name = re.sub(r"[\\/:*?\"<>|#^\\[\\]]+", " ", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name[:120] or "Untitled"


def extract_title(text: str, path: Path) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.M)
    if match:
        return match.group(1).strip()
    return path.stem


def extract_source(text: str) -> str:
    match = re.search(r"https?://[^\s>)\\]]+", text)
    return match.group(0) if match else ""


def choose_category(text: str) -> str:
    haystack = text.lower()
    scores = []
    for category, keywords in CATEGORY_RULES:
        score = sum(1 for k in keywords if k.lower() in haystack)
        if score:
            scores.append((score, category))
    if not scores:
        return "04-Research/Information-Sources"
    scores.sort(reverse=True)
    return scores[0][1]


def choose_topics(text: str) -> list[str]:
    haystack = text.lower()
    topics = []
    for topic, keywords in TOPIC_RULES.items():
        if any(k.lower() in haystack for k in keywords):
            topics.append(topic)
    return sorted(set(topics))


def normalize_markdown(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?m)^([ \t]*[-*+])\s{2,}", r"\1 ", text)
    text = re.sub(r"(?m)^([ \t]*\d+\.)\s{2,}", r"\1 ", text)
    return text.strip() + "\n"


def build_document(original: str, source_path: Path) -> tuple[str, str, str]:
    normalized = normalize_markdown(original)
    title = slugify(extract_title(normalized, source_path))
    source = extract_source(normalized)
    category = choose_category(normalized + " " + title)
    topics = choose_topics(normalized + " " + title)
    hub_links = [HUB_LINKS[t] for t in topics if t in HUB_LINKS]
    captured = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tags_yaml = "\n".join([f"  - {t}" for t in ["type/research", *topics]])
    hub_text = "\n".join([f"- {link}" for link in hub_links]) or "- [[04-Research/Topic-Hubs/Topic Index|Topic Index]]"
    frontmatter = f"""---
type: research
title: "{title.replace('"', "'")}"
source: "{source}"
captured: "{captured}"
main_category: "{category}"
tags:
{tags_yaml}
---
"""
    body = f"""{frontmatter}
# {title}

## Source

- Original file: `{source_path.name}`
- URL: {source or "未识别"}
- Captured: {captured}

## Topic Hubs

{hub_text}

## Original Content

{normalized}
"""
    return title, category, body


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    i = 2
    while True:
        candidate = path.with_name(f"{stem}-{i}{suffix}")
        if not candidate.exists():
            return candidate
        i += 1


def main() -> None:
    DOWNLOADED.mkdir(parents=True, exist_ok=True)
    CLEANED.mkdir(parents=True, exist_ok=True)
    processed = 0
    for source_path in sorted(DOWNLOADED.glob("*.md")):
        original = source_path.read_text(encoding="utf-8", errors="replace")
        title, category, body = build_document(original, source_path)
        cleaned_path = unique_path(CLEANED / f"{title}.md")
        research_dir = VAULT / category
        research_dir.mkdir(parents=True, exist_ok=True)
        research_path = unique_path(research_dir / f"{title}.md")
        cleaned_path.write_text(body, encoding="utf-8")
        shutil.copy2(cleaned_path, research_path)
        processed += 1
        print(f"cleaned: {source_path.name} -> {research_path.relative_to(VAULT)}")
    print(f"processed {processed} markdown file(s)")


if __name__ == "__main__":
    main()

