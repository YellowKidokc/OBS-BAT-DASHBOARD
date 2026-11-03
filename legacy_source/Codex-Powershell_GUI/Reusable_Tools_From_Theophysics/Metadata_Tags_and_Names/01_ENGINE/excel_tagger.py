#!/usr/bin/env python3
"""
excel_tagger.py — Batch YAML tagger driven by the Theophysics Excel codebook.

Source of truth: Master Theophysics Obsidian VAULT_TAG_SYSTEM_v1.xlsx
Output per file: codes: [Pph, Xg, W07, N2, S3]  +  expanded tags: list

Usage:
    python excel_tagger.py                         # pick corpus from menu
    python excel_tagger.py --corpus LOGOS_V3       # jump straight to corpus
    python excel_tagger.py --file path/to/note.md  # tag one file
    python excel_tagger.py --recursive             # include subfolders

Controls inside each section:
    1 3 5        toggle by display number (space/comma separated, or run together)
    Pph          toggle by code name directly
    1.m          toggle code #1 with .m (mirror) modifier
    a            select all in this section
    n            clear all in this section
    Enter        next section
    b            back to previous section
    s            skip this section (leave as-is)
    d / done     jump straight to preview
    next         skip this file entirely (no write)
    q / quit     exit tagger
"""

import sys, io, os, re, uuid, argparse
from pathlib import Path
from collections import defaultdict, OrderedDict
from datetime import date

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

_EXCEL_CANDIDATES = [
    Path(r"O:\999_IGNORE\Obsidian Excel\Theophysics. Obsidian Excel^.xlsx"),
    Path(r"C:\Users\lowes\OneDrive\Desktop\Master Theophysics Obsidian VAULT_TAG_SYSTEM_v1.xlsx"),
]
EXCEL_PATH = next((p for p in _EXCEL_CANDIDATES if p.exists()), _EXCEL_CANDIDATES[0])
VAULT_ROOT = Path(r"O:\_Theophysics_v3")
SKIP_DIRS  = {".git", "__pycache__", "999_IGNORE", "node_modules", ".obsidian"}

# Prefixes where only ONE code applies at a time (picking a new one clears the old)
SINGLE_SELECT = {"S", "N", "W"}

# Section groups: (section_id, [prefixes], display_label)
# Edit this list to reorder, add, or remove sections.
SECTIONS = [
    ("CORE",       ["P", "N", "S"],           "Pillar / Tier / Status"),
    ("PAPER",      ["W"],                      "Paper Reference (W01–W12)"),
    ("FRAMEWORK",  ["X", "D", "L", "G"],       "Framework — Chi-vars / Laws / Logos"),
    ("LOGOS_FW",   ["U"],                      "Logos Framework Concepts"),
    ("THEOLOGY",   ["T", "H"],                 "Theology — Trinity / Subdomain"),
    ("PHYSICS",    ["Q"],                      "Physics"),
    ("PHILOSOPHY", ["F"],                      "Philosophy"),
    ("METHOD",     ["K", "J", "M", "C"],       "Classification / Method / Content"),
    ("OTHER",      ["B", "I", "V", "E", "A", "R"], "Math Symbols / Interdisciplinary / Other"),
]

PAGE_SIZE = 24   # max codes shown per page before pagination kicks in


# ── EXCEL LOADING ─────────────────────────────────────────────────────────────

def load_excel():
    try:
        import openpyxl
    except ImportError:
        print("openpyxl required:  pip install openpyxl"); sys.exit(1)
    if not EXCEL_PATH.exists():
        print(f"Excel not found:\n  {EXCEL_PATH}"); sys.exit(1)
    return openpyxl.load_workbook(EXCEL_PATH)


def load_codebook(wb):
    """dict: code → {prefix, full_concept, mnemonic, yaml_tag}"""
    ws = wb["CODEBOOK"]
    codes = OrderedDict()
    for row in ws.iter_rows(min_row=2, values_only=True):
        r = list(row) + [None] * 8
        category, prefix, code, concept, mnemonic, yaml_tag = r[:6]
        if code and concept and prefix:
            codes[str(code).strip()] = {
                "prefix":      str(prefix).strip(),
                "full_concept": str(concept).strip(),
                "mnemonic":    str(mnemonic or "").strip(),
                "yaml_tag":    str(yaml_tag or concept).strip(),
            }
    return codes


def load_prefix_key(wb):
    """dict: letter → {name, domain, mnemonic}"""
    ws = wb["PREFIX KEY"]
    prefixes = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        r = list(row) + [None] * 8
        name, letter, mnemonic, domain = r[:4]
        if letter:
            prefixes[str(letter).strip()] = {
                "name":     str(name or "").strip(),
                "domain":   str(domain or "").strip(),
                "mnemonic": str(mnemonic or "").strip(),
            }
    return prefixes


def load_folder_profiles(wb):
    """dict: corpus → {folder_path, module_name, required, optional}"""
    ws = wb["TAG_FOLDER_PROFILES"]
    profiles = {}
    for row in ws.iter_rows(min_row=2, values_only=True):
        r = list(row) + [None] * 12
        _, corpus, folder_path, _, module_name, required, optional, _, _, status, _ = r[:11]
        if corpus and str(status or "") == "active":
            profiles[str(corpus).strip()] = {
                "folder_path":  str(folder_path or "").strip(),
                "module_name":  str(module_name or "").strip(),
                "required":     [c.strip() for c in str(required or "").split(";") if c.strip()],
                "optional":     [c.strip() for c in str(optional or "").split(";") if c.strip()],
            }
    return profiles


def append_assignment(wb, file_path, selected_codes):
    """Append a row to TAG_ASSIGNMENTS and save the Excel."""
    ws = wb["TAG_ASSIGNMENTS"]
    ws.append([
        str(uuid.uuid4()),
        "note",
        str(file_path),
        " ".join(sorted(selected_codes)),
        "",
        "",
        "manual",
        1,
        "approved",
        "David",
        str(date.today()),
        "",
    ])
    try:
        wb.save(EXCEL_PATH)
    except PermissionError:
        print("  [warn] Excel file is open — assignment not saved to Excel (YAML was written)")


# ── FRONTMATTER ───────────────────────────────────────────────────────────────

def parse_frontmatter(content):
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[3:end].strip(), content[end + 4:].lstrip("\n"), True
    return "", content, False


def get_inline_list(fm_block, field):
    """Extract codes: [Pph, Xg] → ['Pph', 'Xg']"""
    m = re.search(rf"^{field}\s*:\s*\[(.+)\]", fm_block, re.MULTILINE)
    if m:
        return [v.strip() for v in m.group(1).split(",") if v.strip()]
    return []


def get_block_list(fm_block, field):
    """Extract tags:\n  - foo → ['foo']"""
    items, in_field = [], False
    for line in fm_block.split("\n"):
        if re.match(rf"^{field}\s*:", line):
            in_field = True
            inline = re.search(r"\[(.+)\]", line)
            if inline:
                return [v.strip().strip("\"'") for v in inline.group(1).split(",")]
        elif in_field:
            m = re.match(r"^\s+-\s+(.+)", line)
            if m:
                items.append(m.group(1).strip().strip("\"'"))
            elif line.strip() and not line.startswith(" "):
                in_field = False
    return items


def rebuild_frontmatter(fm_block, codes_sorted, expanded_tags, existing_tags):
    """Replace codes: and tags: fields; keep everything else."""
    lines, skip = fm_block.split("\n"), False
    new_lines = []
    for line in lines:
        if re.match(r"^(codes|tags)\s*:", line):
            skip = True
        elif skip:
            if re.match(r"^\s+-", line):
                continue
            else:
                skip = False
        if not skip:
            new_lines.append(line)

    # Compact codes on one line; wrap if many
    if codes_sorted:
        code_str = ", ".join(codes_sorted)
        if len(code_str) > 60:
            # Wrap into multiple continuation lines
            chunks, cur = [], []
            chars = 0
            for c in codes_sorted:
                if chars + len(c) + 2 > 60 and cur:
                    chunks.append("  " + ", ".join(cur) + ",")
                    cur, chars = [c], len(c)
                else:
                    cur.append(c); chars += len(c) + 2
            if cur:
                chunks.append("  " + ", ".join(cur))
            new_lines.append("codes:")
            new_lines.extend(chunks)
        else:
            new_lines.append(f"codes: [{code_str}]")

    # Full expanded tags
    all_tags = list(expanded_tags)
    for t in existing_tags:
        if t not in all_tags:
            all_tags.append(t)
    if all_tags:
        new_lines.append("tags:")
        for t in all_tags:
            new_lines.append(f"  - {t}")

    return "\n".join(new_lines).strip()


def write_file(path, fm_block, body, codes_sorted, expanded_tags, existing_tags, had_fm):
    new_fm = rebuild_frontmatter(fm_block, codes_sorted, expanded_tags, existing_tags)
    path.write_text(f"---\n{new_fm}\n---\n\n{body}", encoding="utf-8")


# ── FILE QUEUING ──────────────────────────────────────────────────────────────

def queue_files(folder_path, recursive=False):
    root = Path(folder_path) if Path(folder_path).is_absolute() else VAULT_ROOT / folder_path
    if not root.exists():
        print(f"  Folder not found: {root}"); return []
    if recursive:
        files = []
        for r, dirs, fnames in os.walk(root):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            files.extend(Path(r) / f for f in fnames if f.endswith(".md"))
        return sorted(files)
    return sorted(root.glob("*.md"))


# ── DISPLAY UTILITIES ─────────────────────────────────────────────────────────

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def sep(c="─", w=68):
    print(c * w)


def header(title, sub=""):
    sep("═")
    print(f"  {title}")
    if sub:
        print(f"  {sub}")
    sep("═")


def wrap_code_line(codes, width=64):
    """Stack selected codes vertically at ~64 chars per row."""
    if not codes:
        return "  (none selected)"
    lines, cur, chars = [], [], 0
    for c in sorted(codes):
        if chars + len(c) + 2 > width and cur:
            lines.append("  " + "  ".join(cur))
            cur, chars = [c], len(c)
        else:
            cur.append(c); chars += len(c) + 2
    if cur:
        lines.append("  " + "  ".join(cur))
    return "\n".join(lines)


# ── SECTION RENDERER + INPUT HANDLER ─────────────────────────────────────────

def run_section(sec_label, prefixes, codebook, prefix_key, selected,
                file_name, file_idx, file_total, start_page=0):
    """
    Show one section, handle all input, return (new_selected, action).
    action ∈ 'next' | 'prev' | 'done' | 'quit' | 'next_file'
    """
    # Build ordered code list for this section
    section_items = []   # [(code, info)]
    for prefix in prefixes:
        for code, info in codebook.items():
            if info["prefix"] == prefix:
                section_items.append((code, info))

    if not section_items:
        return selected, "next"

    page = start_page
    total_pages = max(1, (len(section_items) - 1) // PAGE_SIZE + 1)

    while True:
        clear()
        header(
            f"FILE [{file_idx}/{file_total}]  {file_name}",
            f"SECTION: {sec_label}"
            + (f"  [page {page+1}/{total_pages}]" if total_pages > 1 else ""),
        )

        # Selected codes summary at top
        print(f"\n  Selected so far ({len(selected)} codes):")
        print(wrap_code_line(selected))
        sep()

        # Codes for this page
        page_items = section_items[page * PAGE_SIZE: (page + 1) * PAGE_SIZE]
        idx_map = {}   # display_num → code
        cur_prefix = None

        for rel, (code, info) in enumerate(page_items, 1):
            abs_num = page * PAGE_SIZE + rel
            if info["prefix"] != cur_prefix:
                cur_prefix = info["prefix"]
                pinfo = prefix_key.get(cur_prefix, {})
                tag_type = " (pick one)" if cur_prefix in SINGLE_SELECT else ""
                print(f"\n  ── {cur_prefix}: {pinfo.get('domain', '')}{tag_type} ──")
            marker = "[x]" if code in selected else "[ ]"
            mn = f"  ({info['mnemonic']})" if info["mnemonic"] else ""
            print(f"  {marker} {abs_num:>3}.  {code:<8}  {info['full_concept']}{mn}")
            idx_map[abs_num] = code

        sep()
        hints = []
        if total_pages > 1:
            if page > 0:            hints.append("[p] prev page")
            if page < total_pages - 1: hints.append("[Enter] next page")
            else:                      hints.append("[Enter] next section")
        else:
            hints.append("[Enter] next section")
        hints += ["[b] back", "[s] skip", "[d] done", "[next] skip file", "[q] quit"]
        print("  " + "  ".join(hints))
        sep()

        cmd = input("  > ").strip()

        # ── Navigation commands ──────────────────────────────────────────────
        if cmd.lower() in ("q", "quit"):
            return selected, "quit"
        if cmd.lower() in ("d", "done"):
            return selected, "done"
        if cmd.lower() == "next":
            return selected, "next_file"
        if cmd.lower() in ("b", "back"):
            return selected, "prev"
        if cmd.lower() in ("s", "skip"):
            return selected, "next"
        if cmd == "":
            if total_pages > 1 and page < total_pages - 1:
                page += 1
                continue
            return selected, "next"
        if cmd.lower() == "p":
            if page > 0:
                page -= 1
            continue

        # ── Select all / clear all ───────────────────────────────────────────
        if cmd.lower() == "a":
            page_codes = {code for code, _ in page_items}
            for prefix in prefixes:
                if prefix in SINGLE_SELECT:
                    # Replace any existing code of this prefix with the last one
                    selected = {c for c in selected if codebook.get(c.split(".")[0], {}).get("prefix") != prefix}
            selected = selected | page_codes
            continue
        if cmd.lower() == "n":
            page_codes = {code for code, _ in page_items}
            selected = selected - page_codes
            continue

        # ── Toggle by number(s) or code name(s) ─────────────────────────────
        tokens = re.split(r"[\s,]+", cmd)
        changed = False
        for token in tokens:
            if not token:
                continue

            # Code name with optional modifier: "Pph" or "Pph.m"
            m = re.match(r"^([A-Za-z]{2,5}|[A-Za-zΓΩχΨΦΛΣ]{1,5})(\.([a-z]))?$", token)
            if m:
                base = m.group(1)
                mod  = m.group(3) or ""
                full = base + ("." + mod if mod else "")
                if base in codebook:
                    selected = _toggle(selected, base, full, codebook)
                    changed = True
                continue

            # Number with optional modifier: "3" or "3.m"
            m = re.match(r"^(\d+)(?:\.([a-z]))?$", token)
            if m:
                num  = int(m.group(1))
                mod  = m.group(2) or ""
                code = idx_map.get(num)
                if code:
                    full = code + ("." + mod if mod else "")
                    selected = _toggle(selected, code, full, codebook)
                    changed = True

        # Don't re-render on pure navigation — loop back to show updated state
        if changed:
            continue   # re-render the same page with updated markers


def _toggle(selected, base_code, full_code, codebook):
    """Toggle a code, enforcing single-select for S/N/W prefixes."""
    prefix = codebook.get(base_code, {}).get("prefix", "")
    # Remove any existing variant (base or base.x) from selected
    variants = {c for c in selected if c == base_code or c.startswith(base_code + ".")}
    if variants:
        # Already selected — deselect
        return selected - variants
    # Single-select: remove any other code with the same prefix first
    if prefix in SINGLE_SELECT:
        selected = {c for c in selected
                    if codebook.get(c.split(".")[0], {}).get("prefix") != prefix}
    return selected | {full_code}


# ── PREVIEW ───────────────────────────────────────────────────────────────────

def show_preview(file_path, selected, codebook, file_idx, file_total):
    clear()
    header(
        f"FILE [{file_idx}/{file_total}]  {file_path.name}",
        "PREVIEW — confirm before writing",
    )

    codes_sorted = sorted(selected)

    # Compact codes line (wrapping)
    print(f"\n  codes: [{', '.join(codes_sorted)}]")
    if len(", ".join(codes_sorted)) > 64:
        print()
        print(wrap_code_line(selected))

    # Expanded tags
    print("\n  tags:")
    for code in codes_sorted:
        base = code.split(".")[0]
        info = codebook.get(base, {})
        yaml_tag = info.get("yaml_tag", base.lower())
        mod = code.split(".")[1] if "." in code else ""
        suffix = f"  [{mod}]" if mod else ""
        print(f"    - {yaml_tag}{suffix}")

    sep()
    print(f"  {len(selected)} codes | [w / Enter] write  [e] edit  [next] skip  [q] quit")
    sep()


# ── MAIN TAGGER FOR ONE FILE ──────────────────────────────────────────────────

def tag_file(file_path, codebook, prefix_key, wb, file_idx, file_total):
    """
    Interactive tagger for one file.
    Returns: 'written' | 'skipped' | 'quit'
    """
    content = file_path.read_text(encoding="utf-8", errors="replace")
    fm_block, body, had_fm = parse_frontmatter(content)
    existing_codes = get_inline_list(fm_block, "codes")
    existing_tags  = get_block_list(fm_block, "tags")

    selected = set(existing_codes)
    history  = []   # stack of section indices for back navigation
    sec_idx  = 0

    while True:
        # ── Section loop ─────────────────────────────────────────────────────
        if sec_idx < 0:
            sec_idx = 0

        if sec_idx < len(SECTIONS):
            _, prefixes, label = SECTIONS[sec_idx]
            new_selected, action = run_section(
                label, prefixes, codebook, prefix_key,
                selected, file_path.name, file_idx, file_total,
            )
            selected = new_selected

            if action == "quit":
                return "quit"
            if action == "next_file":
                return "skipped"
            if action == "done":
                sec_idx = len(SECTIONS)   # jump to preview
            elif action == "next":
                history.append(sec_idx)
                sec_idx += 1
            elif action == "prev":
                sec_idx = history.pop() if history else 0
            continue

        # ── Preview loop ──────────────────────────────────────────────────────
        show_preview(file_path, selected, codebook, file_idx, file_total)
        cmd = input("  > ").strip().lower()

        if cmd in ("w", "", "write"):
            codes_sorted = sorted(selected)

            if not codes_sorted and not existing_codes:
                sep()
                print("  No codes selected. Nothing will be added.")
                print("  Type 'e' to keep editing, or 'w' again to write anyway.")
                sep()
                guard = input("  Continue without codes? [e/w]: ").strip().lower()
                if guard in ("e", "edit", ""):
                    sec_idx = 0
                    history = []
                    continue

            expanded = [
                codebook.get(c.split(".")[0], {}).get("yaml_tag", c.split(".")[0].lower())
                for c in codes_sorted
            ]
            write_file(file_path, fm_block, body, codes_sorted, expanded, existing_tags, had_fm)
            append_assignment(wb, file_path, codes_sorted)

            # Compact post-save summary
            clear()
            sep("═")
            print(f"  SAVED  {file_path.name}")
            sep("═")
            print(f"\n  codes: [{', '.join(codes_sorted)}]")
            print()
            print(wrap_code_line(selected))
            print()
            input("  Press Enter for next file...")
            return "written"

        elif cmd == "e":
            sec_idx = 0; history = []   # restart sections
        elif cmd == "next":
            return "skipped"
        elif cmd in ("q", "quit"):
            return "quit"


# ── CORPUS PICKER ─────────────────────────────────────────────────────────────

def pick_corpus(folder_profiles):
    clear()
    header("EXCEL TAGGER — Theophysics Vault")
    print()
    items = list(folder_profiles.items())
    for i, (corpus, info) in enumerate(items, 1):
        req = ", ".join(info["required"]) or "—"
        print(f"  {i:>2}.  {corpus:<22}  {info['folder_path']:<38}  req: {req}")
    sep()
    print("  Or type a folder path directly (relative to vault root).")
    sep()

    while True:
        raw = input("  Pick corpus number or path: ").strip()
        if not raw:
            continue
        try:
            idx = int(raw) - 1
            if 0 <= idx < len(items):
                corpus, info = items[idx]
                return corpus, info["folder_path"]
        except ValueError:
            pass
        # Direct path
        p = VAULT_ROOT / raw
        if p.is_dir():
            return "CUSTOM", raw
        print("  Not found — try again.")


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Theophysics Excel batch tagger")
    parser.add_argument("--corpus",    help="Corpus name from folder profiles (e.g. LOGOS_V3)")
    parser.add_argument("--file",      help="Tag a single file")
    parser.add_argument("--recursive", action="store_true", help="Recurse into subfolders")
    args = parser.parse_args()

    print("Loading Excel codebook...")
    wb             = load_excel()
    codebook       = load_codebook(wb)
    prefix_key     = load_prefix_key(wb)
    folder_profiles = load_folder_profiles(wb)
    print(f"  {len(codebook)} codes  |  {len(prefix_key)} prefixes  |  {len(folder_profiles)} folder profiles")

    # Queue files
    if args.file:
        files = [Path(args.file)]
        label = "single file"
    elif args.corpus:
        profile = folder_profiles.get(args.corpus)
        if not profile:
            print(f"Unknown corpus: {args.corpus}"); sys.exit(1)
        files = queue_files(profile["folder_path"], args.recursive)
        label = args.corpus
    else:
        corpus, folder_path = pick_corpus(folder_profiles)
        files = queue_files(folder_path, args.recursive)
        label = corpus

    if not files:
        print("No .md files found."); sys.exit(0)

    clear()
    header(f"EXCEL TAGGER — {label}", f"{len(files)} files queued")
    print()
    for i, f in enumerate(files[:10], 1):
        print(f"  {i:>3}. {f.name}")
    if len(files) > 10:
        print(f"       ... and {len(files) - 10} more")
    sep()
    input("  Press Enter to begin...")

    written = skipped = 0
    for i, file_path in enumerate(files):
        result = tag_file(file_path, codebook, prefix_key, wb, i + 1, len(files))
        if result == "written":
            written += 1
        elif result == "skipped":
            skipped += 1
        elif result == "quit":
            break

    clear()
    sep("═")
    print("  SESSION COMPLETE")
    sep("═")
    print(f"  Written:  {written}")
    print(f"  Skipped:  {skipped}")
    print(f"  Total:    {len(files)}")
    sep()


if __name__ == "__main__":
    main()


