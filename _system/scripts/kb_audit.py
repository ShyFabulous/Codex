#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
REPORTS = VAULT / "_system" / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

IGNORE_DIRS = {".git", ".obsidian", ".venv", "__pycache__", ".trash"}
BAD_NAME = re.compile(r"[\\:*?\"<>|]")
WIKILINK = re.compile(r"\[\[([^\]|#]+)")


def iter_files():
    for path in VAULT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        yield path


def iter_dirs():
    for path in VAULT.rglob("*"):
        if not path.is_dir():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        yield path


def sha(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def main() -> None:
    files = list(iter_files())
    md_files = [p for p in files if p.suffix.lower() == ".md"]
    by_hash = defaultdict(list)
    bad_names = []
    garbage = []
    tag_counter = Counter()
    link_targets = Counter()
    incoming = Counter()

    for path in files:
        if path.stat().st_size == 0:
            garbage.append(path)
        if BAD_NAME.search(path.name):
            bad_names.append(path)
        if path.suffix.lower() in {".tmp", ".cache", ".bak"}:
            garbage.append(path)
        try:
            by_hash[sha(path)].append(path)
        except OSError:
            pass

    md_names = {p.with_suffix("").name for p in md_files}
    for path in md_files:
        text = path.read_text(encoding="utf-8", errors="replace")
        for tag in re.findall(r"(?<!\w)#([\w/-]+)", text):
            tag_counter[tag] += 1
        for link in WIKILINK.findall(text):
            target = Path(link).name
            link_targets[target] += 1
            incoming[target] += 1

    duplicates = [paths for paths in by_hash.values() if len(paths) > 1]
    empty_dirs = [p for p in iter_dirs() if not any(p.iterdir())]
    orphan_md = [p for p in md_files if p.with_suffix("").name not in incoming and "Topic-Hubs" not in str(p)]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = [f"# Knowledge Base Audit Report", "", f"- Generated: {now}", f"- Vault: `{VAULT}`", ""]
    report += ["## Summary", "", f"- Files: {len(files)}", f"- Markdown files: {len(md_files)}", f"- Duplicate groups: {len(duplicates)}", f"- Bad filenames: {len(bad_names)}", f"- Empty directories: {len(empty_dirs)}", f"- Garbage/suspicious files: {len(garbage)}", f"- Orphan markdown files: {len(orphan_md)}", ""]

    def add_paths(title: str, paths):
        report.extend([f"## {title}", ""])
        if not paths:
            report.append("None.")
        else:
            for p in paths[:100]:
                report.append(f"- `{p.relative_to(VAULT)}`")
        report.append("")

    report.extend(["## Duplicate Files", ""])
    if duplicates:
        for group in duplicates[:50]:
            report.append("- " + " | ".join(f"`{p.relative_to(VAULT)}`" for p in group))
    else:
        report.append("None.")
    report.append("")

    add_paths("Bad Filenames", bad_names)
    add_paths("Empty Directories", empty_dirs)
    add_paths("Garbage or Suspicious Files", sorted(set(garbage)))
    add_paths("Orphan Markdown Files", orphan_md)

    report.extend(["## Top Tags", ""])
    if tag_counter:
        for tag, count in tag_counter.most_common(50):
            report.append(f"- `#{tag}`: {count}")
    else:
        report.append("No tags found.")
    report.append("")

    report_path = REPORTS / f"kb-audit-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
    report_path.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(report_path.relative_to(VAULT))


if __name__ == "__main__":
    main()

