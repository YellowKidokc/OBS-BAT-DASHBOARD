#!/usr/bin/env python3
"""
Convert all Theophysics MD files to MDX for Astro site
"""

import os
import re
import html
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import unicodedata

# Paths
SOURCE = Path(r'O:\Theophysics_Master\TMSUB\GO FOLDER')
DEST = Path(r'C:\Users\lowes\Downloads\Obsidian-Cloudflare-Claude\Obsidian-Cloudflare-Claude-main\src\pages\papers')

# Skip patterns
SKIP_PATTERNS = [
    'TEMPLATE', 'COMBINE', 'Untitled', '.bat', '.ps1', '.zip',
    'node_modules', '.git', '__pycache__'
]

def clean_slug(name):
    """Create URL-safe slug from filename"""
    # Remove extension
    slug = Path(name).stem
    # Normalize unicode
    slug = unicodedata.normalize('NFKD', slug)
    slug = slug.encode('ascii', 'ignore').decode('ascii')
    # Replace spaces and underscores with hyphens
    slug = re.sub(r'[\s_]+', '-', slug)
    # Remove non-alphanumeric except hyphens
    slug = re.sub(r'[^a-zA-Z0-9-]', '', slug)
    # Collapse multiple hyphens
    slug = re.sub(r'-+', '-', slug)
    # Lowercase and trim
    slug = slug.lower().strip('-')
    return slug[:80]  # Limit length

def extract_title(content, filename):
    """Extract title from H1 or filename"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove wiki links [[page|text]] -> text, [[page]] -> page
        title = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', title)
        title = re.sub(r'\[\[([^\]]+)\]\]', r'\1', title)
        # Remove markdown formatting and pipes
        title = re.sub(r'[*_`\[\]|]', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title[:150]
    # Fallback to filename
    name = Path(filename).stem.replace('_', ' ').replace('-', ' ')
    # Remove leading numbers
    name = re.sub(r'^\d+\s*', '', name)
    return name.title()[:150]

def extract_description(content):
    """Extract first paragraph as description"""
    # Skip frontmatter if exists
    content = re.sub(r'^---[\s\S]*?---\s*', '', content)
    # Skip title
    content = re.sub(r'^#.+\n+', '', content)
    # Get first paragraph
    match = re.match(r'(.+?)(?:\n\n|\n#|$)', content, re.DOTALL)
    if match:
        desc = match.group(1).strip()
        # Clean markdown
        desc = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', desc)  # Links
        desc = re.sub(r'[*_`#>]', '', desc)  # Formatting
        desc = re.sub(r'\s+', ' ', desc)  # Whitespace
        return desc[:250]
    return ""

def escape_mdx(content):
    """Escape characters that break MDX parser"""
    # Remove dataview/dataviewjs code blocks (Obsidian-specific)
    content = re.sub(r'```dataview[\s\S]*?```', '', content)
    content = re.sub(r'```dataviewjs[\s\S]*?```', '', content)

    # Remove ALL image references (they reference local Obsidian vault paths)
    content = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'<!-- Image: \1 -->', content)  # ![alt](path)
    content = re.sub(r'!\[\[[^\]]+\]\]', '<!-- Image removed -->', content)  # ![[path]]
    # Remove markdown image imports
    content = re.sub(r'^import\s+.*\.(png|jpg|jpeg|gif|svg|webp).*$', '', content, flags=re.MULTILINE | re.IGNORECASE)

    # Convert wiki links [[page]] or [[page|text]] to regular text
    content = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', content)  # [[page|text]] -> text
    content = re.sub(r'\[\[([^\]]+)\]\]', r'\1', content)  # [[page]] -> page

    # Escape curly braces (MDX treats as JS expressions)
    content = content.replace('{', '&#123;')
    content = content.replace('}', '&#125;')

    # Escape < > that aren't HTML tags (math like |<psi|)
    content = re.sub(r'<(?![a-zA-Z/!])', '&lt;', content)
    content = re.sub(r'(?<![a-zA-Z"\'/=])>', '&gt;', content)

    # Escape pipes that look like they're in math (not in tables)
    content = re.sub(r'\|(?=[<>ψΨφΦχ])', '&#124;', content)
    content = re.sub(r'(?<=[>ψΨφΦχ])\|', '&#124;', content)

    return content

def get_category(filepath):
    """Extract category from folder structure"""
    rel = filepath.relative_to(SOURCE)
    parts = rel.parts[:-1]  # Exclude filename
    if parts:
        return ' > '.join(parts[:2])  # First 2 levels
    return "Papers"

def convert_file(md_path):
    """Convert single MD file to MDX"""
    try:
        # Read content
        content = md_path.read_text(encoding='utf-8', errors='ignore')

        # Skip if too short
        if len(content.strip()) < 50:
            return None, "Too short"

        # Extract metadata
        title = extract_title(content, md_path.name)
        description = extract_description(content)
        category = get_category(md_path)

        # Remove existing frontmatter
        content = re.sub(r'^---[\s\S]*?---\s*', '', content)

        # Remove first H1 (we'll use title from frontmatter)
        content = re.sub(r'^#\s+.+\n+', '', content, count=1)

        # Escape problematic characters
        content = escape_mdx(content)

        # Create slug
        slug = clean_slug(md_path.stem)
        if not slug:
            slug = f"paper-{hash(md_path.name) % 10000}"

        # Build MDX frontmatter
        # Escape quotes and backslashes in title/description for YAML
        safe_title = title.replace('\\', '\\\\').replace('"', "'").replace('\n', ' ')
        safe_desc = description.replace('\\', '\\\\').replace('"', "'").replace('\n', ' ')
        # Remove any remaining problematic characters
        safe_title = re.sub(r'[\x00-\x1f]', '', safe_title)
        safe_desc = re.sub(r'[\x00-\x1f]', '', safe_desc)

        mdx_content = f'''---
layout: ../../layouts/PaperLayout.astro
title: "{safe_title}"
description: "{safe_desc}"
category: "{category}"
author: "David Lowe"
---

{content}
'''

        return (slug, mdx_content), None

    except Exception as e:
        return None, str(e)

def main():
    print(f"Source: {SOURCE}")
    print(f"Destination: {DEST}")

    # Clear existing MD/MDX files (except index.astro and logos-principle)
    keep = {'index.astro', 'logos-principle.mdx'}
    for f in list(DEST.glob('*.mdx')) + list(DEST.glob('*.md')):
        if f.name not in keep:
            f.unlink()
    print("Cleared old MD/MDX files")

    # Find all MD files
    md_files = []
    for pattern in SKIP_PATTERNS:
        pass  # Will filter below

    for md_path in SOURCE.rglob('*.md'):
        # Skip if matches any skip pattern
        if any(p.lower() in str(md_path).lower() for p in SKIP_PATTERNS):
            continue
        md_files.append(md_path)

    print(f"Found {len(md_files)} MD files to convert")

    # Convert in parallel
    results = {'success': 0, 'failed': 0, 'skipped': 0}
    slugs_used = set()

    # Process files
    for i, md_path in enumerate(md_files):
        if i % 500 == 0:
            print(f"Processing {i}/{len(md_files)}...")

        result, error = convert_file(md_path)

        if error:
            results['skipped'] += 1
            continue

        if result:
            slug, content = result

            # Handle duplicate slugs
            original_slug = slug
            counter = 1
            while slug in slugs_used:
                slug = f"{original_slug}-{counter}"
                counter += 1
            slugs_used.add(slug)

            # Write MD file (not MDX - avoids JSX parsing issues)
            output_path = DEST / f"{slug}.md"
            try:
                output_path.write_text(content, encoding='utf-8')
                results['success'] += 1
            except Exception as e:
                results['failed'] += 1

    print(f"\n{'='*50}")
    print(f"CONVERSION COMPLETE")
    print(f"{'='*50}")
    print(f"Success: {results['success']}")
    print(f"Failed: {results['failed']}")
    print(f"Skipped: {results['skipped']}")
    print(f"Total MD files: {len(list(DEST.glob('*.md')))}")

if __name__ == '__main__':
    main()
