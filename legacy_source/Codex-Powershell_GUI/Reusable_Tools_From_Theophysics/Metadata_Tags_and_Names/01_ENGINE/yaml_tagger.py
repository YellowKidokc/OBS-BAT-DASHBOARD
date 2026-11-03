#!/usr/bin/env python3
"""
yaml_tagger.py — Interactive hierarchical YAML tag loader for Theophysics vault

Usage:
    python yaml_tagger.py                       # pick from current folder
    python yaml_tagger.py path/to/file.md       # tag a specific file
    python yaml_tagger.py path/to/folder/       # pick from folder

Controls (in tag menus):
    1 2 3 ...   toggle tags by number (space-separated or run together: 123)
    a           select ALL in this category
    n           clear ALL in this category
    Enter       next category
    b           back one category
    skip        skip the rest of this domain
    done        finish and confirm write

Taxonomy source: tags_taxonomy.yaml  (same folder as this script)
To add tags/categories/domains: edit that YAML file — no Python edits needed.
"""

import sys
import io
import os
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = Path(__file__).parent
TAXONOMY_FILE = SCRIPT_DIR / "tags_taxonomy.yaml"
MEDIA_DIR = Path(r"O:\00_MEDIA\Blue_Diagrams")  # adjust if junction moved


# ── LOAD TAXONOMY ─────────────────────────────────────────────────────────────

def load_taxonomy():
    """Load TAG_TAXONOMY and AUTO_DETECT from tags_taxonomy.yaml."""
    try:
        import yaml
    except ImportError:
        print("PyYAML not found. Install with:  pip install pyyaml")
        sys.exit(1)

    if not TAXONOMY_FILE.exists():
        print(f"Taxonomy file not found: {TAXONOMY_FILE}")
        sys.exit(1)

    with open(TAXONOMY_FILE, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    domains = data.get("domains", {})
    auto_detect = data.get("auto_detect", {})
    return domains, auto_detect


# ── IMAGE DISCOVERY ───────────────────────────────────────────────────────────

def discover_images():
    """Return list of image filenames from the media directory."""
    if not MEDIA_DIR.exists():
        return []
    exts = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
    imgs = sorted(
        f.name for f in MEDIA_DIR.iterdir()
        if f.suffix.lower() in exts
    )
    return imgs


# ── UTILITIES ─────────────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def sep(char="─", width=62):
    print(char * width)


def header(title):
    sep("═")
    print(f"  {title}")
    sep("═")


# ── FILE PICKING ──────────────────────────────────────────────────────────────

def pick_file(path_arg):
    if path_arg:
        p = Path(path_arg)
        if p.is_file():
            return p
        if not p.is_dir():
            p2 = p.with_suffix(".md")
            if p2.is_file():
                return p2
            print(f"  Not found: {path_arg}")
            path_arg = None

    folder = Path(path_arg) if path_arg else Path(".")
    md_files = sorted(folder.glob("*.md"))
    if not md_files:
        md_files = sorted(folder.glob("**/*.md"))[:60]

    if not md_files:
        print(f"No .md files found in {folder.resolve()}")
        sys.exit(1)

    header(f"PICK FILE — {folder.resolve()}")
    for i, f in enumerate(md_files, 1):
        print(f"  {i:>3}. {f.name}")
    sep()

    while True:
        raw = input("File number (or paste path): ").strip()
        if not raw:
            continue
        ptest = Path(raw)
        if ptest.is_file():
            return ptest
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(md_files):
                return md_files[idx]
        except ValueError:
            pass
        print("  Invalid — try again.")


# ── FRONTMATTER ───────────────────────────────────────────────────────────────

def parse_frontmatter(content):
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            fm_block = content[3:end].strip()
            body = content[end + 4:].lstrip("\n")
            return fm_block, body, True
    return "", content, False


def get_existing_tags(fm_block):
    tags = []
    in_tags = False
    for line in fm_block.split("\n"):
        if re.match(r"^tags\s*:", line):
            in_tags = True
            inline = re.search(r"\[(.+)\]", line)
            if inline:
                tags = [t.strip().strip("\"'") for t in inline.group(1).split(",")]
                in_tags = False
        elif in_tags:
            m = re.match(r"^\s+-\s+(.+)", line)
            if m:
                tags.append(m.group(1).strip().strip("\"'"))
            elif line.strip() and not line.startswith(" "):
                in_tags = False
    return [t for t in tags if t]


def get_existing_images(fm_block):
    """Extract images: list from frontmatter."""
    images = []
    in_images = False
    for line in fm_block.split("\n"):
        if re.match(r"^images\s*:", line):
            in_images = True
            inline = re.search(r"\[(.+)\]", line)
            if inline:
                images = [t.strip().strip("\"'") for t in inline.group(1).split(",")]
                in_images = False
        elif in_images:
            m = re.match(r"^\s+-\s+(.+)", line)
            if m:
                images.append(m.group(1).strip().strip("\"'"))
            elif line.strip() and not line.startswith(" "):
                in_images = False
    return [i for i in images if i]


def rebuild_frontmatter(fm_block, selected_tags, selected_images):
    """Rebuild frontmatter with updated tags: and images: fields."""
    lines = fm_block.split("\n")
    new_lines = []
    skip = False
    for line in lines:
        if re.match(r"^(tags|images)\s*:", line):
            skip = True
        elif skip:
            if re.match(r"^\s+-", line):
                continue
            else:
                skip = False
        if not skip:
            new_lines.append(line)

    # Append tags
    if selected_tags:
        new_lines.append("tags:")
        for t in sorted(selected_tags):
            new_lines.append(f"  - {t}")

    # Append images
    if selected_images:
        new_lines.append("images:")
        for img in selected_images:
            new_lines.append(f"  - {img}")

    return "\n".join(new_lines).strip()


def write_file(path, fm_block, body, selected_tags, selected_images, had_fm):
    new_fm = rebuild_frontmatter(fm_block, selected_tags, selected_images)
    new_content = f"---\n{new_fm}\n---\n\n{body}"
    path.write_text(new_content, encoding="utf-8")


# ── AUTO-DETECTION ────────────────────────────────────────────────────────────

def auto_detect(content, auto_kw):
    content_lower = content.lower()
    hits = set()
    for tag, keywords in auto_kw.items():
        if isinstance(keywords, list):
            for kw in keywords:
                if kw.lower() in content_lower:
                    hits.add(tag)
                    break
    return hits


# ── TAG SELECTION UI ──────────────────────────────────────────────────────────

def show_tag_category(domain, d_idx, d_total, cat, c_idx, c_total,
                       tags, selected, auto_hits):
    clear()
    sep("═")
    print(f"  DOMAIN [{d_idx+1}/{d_total}]  {domain}")
    print(f"  CATEGORY [{c_idx+1}/{c_total}]  {cat}")
    sep("═")
    for i, tag in enumerate(tags, 1):
        marker = "[x]" if tag in selected else "[ ]"
        star = " *" if tag in auto_hits else ""
        print(f"  {marker} {i:>2}.  {tag}{star}")
    sep()
    here = sum(1 for t in tags if t in selected)
    print(f"  Selected here: {here}/{len(tags)}   Total tags: {len(selected)}")
    if auto_hits.intersection(tags):
        print("  (* = detected in paper text)")
    sep()
    print("  [numbers] toggle  [a] all  [n] none  [Enter] next  [b] back")
    print("  [skip] skip domain  [done] finish")
    sep()


def select_tags(domains, existing_tags, auto_hits):
    selected = set(existing_tags)
    domain_names = list(domains.keys())
    d_idx = 0

    while d_idx < len(domain_names):
        domain = domain_names[d_idx]
        categories = domains[domain]
        cat_names = list(categories.keys())
        c_idx = 0

        while c_idx < len(cat_names):
            cat = cat_names[c_idx]
            tags = categories[cat]

            show_tag_category(domain, d_idx, len(domain_names),
                              cat, c_idx, len(cat_names),
                              tags, selected, auto_hits)

            cmd = input("> ").strip().lower()

            if cmd == "done":
                return selected
            elif cmd == "skip":
                break
            elif cmd == "":
                c_idx += 1
            elif cmd == "b":
                c_idx = max(0, c_idx - 1)
            elif cmd == "a":
                selected.update(tags)
            elif cmd == "n":
                selected -= set(tags)
            else:
                for n in re.findall(r"\d+", cmd):
                    idx = int(n) - 1
                    if 0 <= idx < len(tags):
                        tag = tags[idx]
                        if tag in selected:
                            selected.discard(tag)
                        else:
                            selected.add(tag)

        d_idx += 1

    return selected


# ── IMAGE SELECTION UI ────────────────────────────────────────────────────────

def show_image_page(images, selected_images, page, page_size=20):
    clear()
    header("IMAGE PICKER — select images to link in this paper")
    total_pages = (len(images) - 1) // page_size + 1
    start = page * page_size
    chunk = images[start: start + page_size]
    for i, img in enumerate(chunk, 1):
        marker = "[x]" if img in selected_images else "[ ]"
        print(f"  {marker} {start+i:>3}.  {img}")
    sep()
    print(f"  Page {page+1}/{total_pages}   Selected: {len(selected_images)}/{len(images)}")
    sep()
    print("  [numbers] toggle  [a] all on page  [n] none on page")
    print("  [p] prev page  [Enter] next page  [done] finish images")
    sep()
    return chunk, total_pages


def select_images(existing_images):
    images = discover_images()
    if not images:
        print(f"\n  No images found in {MEDIA_DIR}")
        input("  Press Enter to skip image selection...")
        return set(existing_images)

    selected = set(existing_images)
    page = 0
    page_size = 20

    while True:
        chunk, total_pages = show_image_page(images, selected, page, page_size)
        cmd = input("> ").strip().lower()

        if cmd == "done":
            break
        elif cmd == "":
            if page < total_pages - 1:
                page += 1
            else:
                break
        elif cmd == "p":
            page = max(0, page - 1)
        elif cmd == "a":
            selected.update(chunk)
        elif cmd == "n":
            selected -= set(chunk)
        else:
            start = page * page_size
            for n in re.findall(r"\d+", cmd):
                abs_idx = int(n) - 1
                rel_idx = abs_idx - start
                if 0 <= rel_idx < len(chunk):
                    img = chunk[rel_idx]
                elif 0 <= abs_idx < len(images):
                    img = images[abs_idx]
                else:
                    continue
                if img in selected:
                    selected.discard(img)
                else:
                    selected.add(img)

    return selected


# ── CONFIRM & WRITE ───────────────────────────────────────────────────────────

def confirm_write(file_path, selected_tags, selected_images):
    clear()
    header(f"FINAL SELECTION — {file_path.name}")
    print(f"\n  TAGS ({len(selected_tags)}):")
    if selected_tags:
        for t in sorted(selected_tags):
            print(f"    - {t}")
    else:
        print("    (none)")

    print(f"\n  IMAGES ({len(selected_images)}):")
    if selected_images:
        for img in sorted(selected_images):
            print(f"    - {img}")
    else:
        print("    (none)")
    sep()
    choice = input("  Write to file? [y / n / e(dit)]: ").strip().lower()
    if choice == "e":
        return "edit"
    return choice == "y"


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    file_path = pick_file(arg)

    domains, auto_kw = load_taxonomy()

    content = file_path.read_text(encoding="utf-8", errors="replace")
    fm_block, body, had_fm = parse_frontmatter(content)
    existing_tags = get_existing_tags(fm_block) if had_fm else []
    existing_images = get_existing_images(fm_block) if had_fm else []

    auto_hits = auto_detect(content, auto_kw)

    clear()
    header(f"YAML TAGGER — {file_path.name}")
    print(f"  Path:           {file_path}")
    print(f"  Frontmatter:    {'yes' if had_fm else 'no'}")
    print(f"  Existing tags:  {len(existing_tags)}")
    if existing_tags:
        for t in existing_tags:
            print(f"    - {t}")
    if auto_hits:
        print(f"\n  Auto-detected {len(auto_hits)} tags from content")
    print(f"  Existing images: {len(existing_images)}")
    sep()
    print("  Sections: [1] Tags  [2] Images  [3] Both  [Enter] Both")
    choice = input("  > ").strip()

    do_tags = choice in ("", "1", "3")
    do_images = choice in ("", "2", "3")
    if not do_tags and not do_images:
        do_tags = do_images = True

    selected_tags = set(existing_tags)
    selected_images = set(existing_images)

    while True:
        if do_tags:
            input("\n  Press Enter to begin tag selection...")
            selected_tags = select_tags(domains, list(selected_tags), auto_hits)

        if do_images:
            selected_images = select_images(list(selected_images))

        result = confirm_write(file_path, selected_tags, selected_images)
        if result == "edit":
            continue
        elif result:
            write_file(file_path, fm_block, body, selected_tags, selected_images, had_fm)
            print(f"\n  Written: {file_path}")
            print(f"  Tags: {len(selected_tags)}   Images: {len(selected_images)}")
        else:
            print("\n  Cancelled — file unchanged.")
        break


if __name__ == "__main__":
    main()
