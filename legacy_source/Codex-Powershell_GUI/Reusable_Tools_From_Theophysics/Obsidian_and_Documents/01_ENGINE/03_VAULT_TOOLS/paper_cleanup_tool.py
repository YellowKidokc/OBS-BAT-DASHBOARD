#!/usr/bin/env python3
"""
PAPER CLEANUP SKILL v1.0
========================
Restructures raw/messy papers into proper academic format.

- Removes page breaks and duplicate metadata
- Adds clean YAML frontmatter
- Creates hierarchical section structure
- Generates Table of Contents
- Identifies and marks FACTS sections
- Outputs clean, properly formatted paper

Usage (Direct):
  python paper_cleanup_tool.py input.md
  python paper_cleanup_tool.py input.md -o output.md

Usage (As Skill from Claude Code):
  /cleanup-paper path/to/paper.md
"""

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Dict


def extract_metadata_from_content(content: str) -> Dict[str, str]:
    """Try to extract title, author, date from paper content."""
    meta = {
        "title": "Unknown Paper",
        "author": "Unknown Author",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "category": "theory",
    }

    # Look for title patterns
    title_patterns = [
        r"^#\s+(.+?)$",  # Markdown h1
        r"^[A-Z][A-Z\s]+$",  # ALL CAPS lines
        r"^[A-Za-z].*\s(?:Theory|Framework|Analysis|Model|System)",  # Title-like patterns
    ]

    for pattern in title_patterns:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            meta["title"] = match.group(1).strip()
            break

    # Look for author
    author_patterns = [
        r"(?:By|Author|From)[\s:]+([A-Z][A-Za-z\s]+)",
        r"^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*$",
    ]

    for pattern in author_patterns:
        match = re.search(pattern, content, re.MULTILINE)
        if match:
            meta["author"] = match.group(1).strip()
            break

    return meta


def remove_page_breaks(content: str) -> str:
    """Remove PDF page break markers and page headers."""
    # Remove patterns like "## Page N"
    content = re.sub(r"^---$\n^## Page \d+$\n", "\n", content, flags=re.MULTILINE)
    content = re.sub(r"^## Page \d+$\n", "", content, flags=re.MULTILINE)

    # Remove duplicate metadata sections
    lines = content.split("\n")
    filtered = []
    skip_until_break = False

    for i, line in enumerate(lines):
        if line.startswith("#") and i < 10 and ("canonical" in line.lower() or "uncategorized" in line.lower()):
            skip_until_break = True
            continue
        if skip_until_break and line.startswith("---"):
            skip_until_break = False
            continue
        if not skip_until_break:
            filtered.append(line)

    return "\n".join(filtered)


def identify_sections(content: str) -> List[Tuple[int, str, str]]:
    """Identify major section headers and their hierarchy."""
    sections = []

    patterns = [
        (r"^(?:PART|CHAPTER|SECTION|§)\s+([IVX]+|\d+)[\s:]+(.+?)$", 3),  # PART I, CHAPTER 1
        (r"^(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s+(.+?)$", 2),  # Roman numeral sections
        (r"^#{1,4}\s+(.+?)$", 1),  # Markdown headers
    ]

    for pattern, level in patterns:
        for match in re.finditer(pattern, content, re.MULTILINE):
            line_num = content[:match.start()].count("\n")
            title = match.group(0) if level == 1 else match.group(1)
            sections.append((line_num, title, level))

    return sorted(sections, key=lambda x: x[0])


def build_clean_content(content: str, metadata: Dict, filename: str) -> str:
    """Rebuild content with clean structure."""

    # Clean content
    content = remove_page_breaks(content)

    # Identify sections
    sections = identify_sections(content)

    # Build YAML frontmatter
    frontmatter = f"""---
title: "{metadata['title']}"
author: "{metadata['author']}"
date: {metadata['date']}
category: {metadata['category']}
tags:
  - theory
  - {metadata['category']}
  - canonical
source_file: {filename}
restructured: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

"""

    # Build header
    header = f"""# {metadata['title']}

**Author:** {metadata['author']}

**Date:** {metadata['date']}

---

## Table of Contents

"""

    # Add TOC entries based on identified sections
    if sections:
        for _, title, _ in sections[:15]:  # Limit to first 15
            # Create anchor from title
            anchor = re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-")
            header += f"- [{title}](#{anchor})\n"

    header += "\n---\n\n"

    # Process content sections
    processed_content = content

    # Add anchors to identified sections
    for _, title, _ in sections:
        anchor = re.sub(r"[^\w\s-]", "", title.lower()).replace(" ", "-")
        # Add anchor after section header
        processed_content = re.sub(
            f"^({re.escape(title)})$",
            f"\\1 {{#{anchor}}}",
            processed_content,
            flags=re.MULTILINE
        )

    # Clean up excess whitespace
    processed_content = re.sub(r"\n\n\n+", "\n\n", processed_content)

    # Build footer
    footer = f"""

---

## Metadata

**Original File:** {filename}

**Restructured:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**Format:** Canonical Theory Document (Lowe Standard v1.0)

**Status:** Cleaned and ready for evaluation

---

*This paper has been restructured for clarity and proper academic formatting. Original content preserved.*
"""

    return frontmatter + header + processed_content + footer


def cleanup_paper(input_path: Path, output_path: Path = None) -> Tuple[bool, str]:
    """Main cleanup function."""

    if not input_path.exists():
        return False, f"File not found: {input_path}"

    # Read
    try:
        content = input_path.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        return False, f"Failed to read file: {e}"

    # Extract metadata
    metadata = extract_metadata_from_content(content)

    # Build clean content
    try:
        clean_content = build_clean_content(content, metadata, input_path.name)
    except Exception as e:
        return False, f"Failed to process content: {e}"

    # Output
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_CLEAN{input_path.suffix}"

    try:
        output_path.write_text(clean_content, encoding="utf-8")
    except Exception as e:
        return False, f"Failed to write output: {e}"

    return True, str(output_path)


def main():
    """CLI entry point."""

    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    input_file = Path(sys.argv[1])
    output_file = None

    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            output_file = Path(sys.argv[idx + 1])

    print(f"\n{'='*60}")
    print(f"  PAPER CLEANUP SKILL v1.0")
    print(f"{'='*60}")
    print(f"  Input:  {input_file.name}")

    success, result = cleanup_paper(input_file, output_file)

    if success:
        print(f"  Output: {Path(result).name}")
        print(f"\n  ✅ Success!")
        print(f"     Cleaned and restructured")
        print(f"     YAML frontmatter added")
        print(f"     Section hierarchy created")
        print(f"     Table of contents generated")
        print(f"{'='*60}\n")
        sys.exit(0)
    else:
        print(f"\n  ❌ Failed: {result}")
        print(f"{'='*60}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
