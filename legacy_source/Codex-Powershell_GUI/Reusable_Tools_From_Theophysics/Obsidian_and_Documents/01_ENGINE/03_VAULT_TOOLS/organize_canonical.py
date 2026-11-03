#!/usr/bin/env python3
"""
Organize downloaded theory files into canonical categories.

This script reads theory files from the Downloaded/ folder and Bad/ folder,
categorizes them intelligently based on content and filename, and moves them
to the appropriate category folders in the Canonical/ directory.
"""

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

# Directories
DOWNLOADED_DIR = Path("O:/999_IGNORE/Obsidian Programs/Theory_Downloader/Downloaded")
BAD_DIR = Path("O:/999_IGNORE/Obsidian Programs/Theory_Downloader/Bad")
CANONICAL_DIR = Path("O:/_Theophysics_v3/Canonical")

# Category keywords for intelligent classification
CATEGORY_KEYWORDS = {
    "Physics/Quantum_Mechanics": [
        "quantum", "bell", "epr", "heisenberg", "uncertainty", "schrodinger",
        "wavefunction", "collapse", "measurement", "superposition", "entanglement",
        "decoherence", "copenhagen", "many-worlds", "qbism", "born rule",
        "gleason", "kochen-specker", "no-cloning", "quantum mechanics",
        "quantum field", "unitarity", "hilbert space"
    ],
    "Physics/General_Relativity": [
        "einstein", "relativity", "spacetime", "gravity", "metric tensor",
        "stress-energy", "geodesic", "schwarzschild", "black hole",
        "event horizon", "curvature", "gravitational"
    ],
    "Physics/Information_Physics": [
        "it from bit", "wheeler", "bekenstein", "landauer", "information physics",
        "participatory universe", "observer effect", "measurement problem",
        "physical information", "thermodynamics of computation"
    ],
    "Physics/Digital_Physics": [
        "digital physics", "computational universe", "zuse", "fredkin",
        "wolfram", "tegmark", "mathematical universe", "cellular automata",
        "church-turing", "algorithmic universe"
    ],
    "Physics/Holographic_Principle": [
        "holographic", "bekenstein bound", "'t hooft", "susskind",
        "ads/cft", "ads cft", "er=epr", "black hole thermodynamics",
        "entropy bound", "holographic duality"
    ],
    "Consciousness": [
        "consciousness", "qualia", "hard problem", "integrated information",
        "tononi", "phi", "iit", "global workspace", "binding problem",
        "penrose", "hameroff", "orch or", "orchestrated reduction",
        "neural correlates", "libet", "free will", "mary's room",
        "split brain", "default mode network"
    ],
    "Information_Theory": [
        "shannon", "information theory", "entropy", "kolmogorov",
        "algorithmic information", "mutual information", "channel capacity",
        "fisher information", "jaynes", "maximum entropy", "bayesian",
        "compression", "code", "signal", "noise", "boltzmann entropy"
    ],
    "Mathematics": [
        "godel", "incompleteness", "tarski", "undefinability",
        "curry-howard", "correspondence", "mathematical logic",
        "recursion", "computation", "turing", "chaos theory",
        "fractal", "self-similarity", "least action", "variational"
    ],
    "Philosophy": [
        "kuhn", "popper", "scientific revolution", "paradigm shift",
        "falsifiability", "pseudoscience", "philosophy of science",
        "epistemology", "metaphysics", "anthropic principle"
    ],
    "Theology": [
        "logos", "divine", "god", "theology", "omniscience", "omnipotence",
        "aquinas", "cosmological argument", "kalam", "ontological argument",
        "biblical", "canon", "revelation", "eternity"
    ]
}


def normalize_filename(filename: str) -> str:
    """Normalize filename to standard format."""
    # Remove extension
    name = Path(filename).stem
    # Replace multiple underscores with single
    name = re.sub(r'_+', '_', name)
    # Remove trailing/leading underscores
    name = name.strip('_')
    return name


def categorize_file(filepath: Path) -> Tuple[str, float]:
    """
    Categorize a file based on filename and content.

    Returns: (category, confidence_score)
    """
    filename = filepath.stem.lower()

    # Read first 2000 characters of content
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read(2000).lower()
    except Exception as e:
        print(f"⚠️  Could not read {filepath.name}: {e}")
        content = ""

    # Score each category
    scores = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Filename matches are worth more
            if keyword in filename:
                score += 5
            # Content matches
            if keyword in content:
                score += 1
        scores[category] = score

    # Find best match
    if not scores or max(scores.values()) == 0:
        return ("_UNCATEGORIZED", 0.0)

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]

    # Calculate confidence (0-1 scale)
    total_keywords = len(CATEGORY_KEYWORDS[best_category])
    confidence = min(best_score / total_keywords, 1.0)

    return (best_category, confidence)


def validate_file(filepath: Path) -> Tuple[bool, str]:
    """
    Validate that a file is complete and properly formatted.

    Returns: (is_valid, reason)
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check minimum length
        if len(content) < 200:
            return (False, "File too short (< 200 chars)")

        # Check for markdown headers
        if '#' not in content:
            return (False, "No markdown headers found")

        # Check for actual content (not just metadata)
        lines = content.split('\n')
        content_lines = [l for l in lines if l.strip() and not l.startswith('**') and not l.startswith('#')]
        if len(content_lines) < 5:
            return (False, "Insufficient content lines")

        return (True, "Valid")

    except Exception as e:
        return (False, f"Read error: {e}")


def process_file(filepath: Path, source_type: str) -> Dict:
    """
    Process a single file: validate, categorize, and prepare for moving.

    Returns: dict with file info and actions
    """
    result = {
        'filepath': filepath,
        'filename': filepath.name,
        'source': source_type,
        'valid': False,
        'category': None,
        'confidence': 0.0,
        'action': None,
        'reason': None
    }

    # Validate
    is_valid, reason = validate_file(filepath)
    result['valid'] = is_valid

    if not is_valid:
        result['action'] = 'SKIP'
        result['reason'] = reason
        return result

    # Categorize
    category, confidence = categorize_file(filepath)
    result['category'] = category
    result['confidence'] = confidence

    # Decide action
    if confidence > 0.3:
        result['action'] = 'MOVE'
        result['reason'] = f"High confidence ({confidence:.1%})"
    elif confidence > 0.1:
        result['action'] = 'REVIEW'
        result['reason'] = f"Low confidence ({confidence:.1%})"
    else:
        result['action'] = 'UNCATEGORIZED'
        result['reason'] = f"No clear category ({confidence:.1%})"

    return result


def move_file(result: Dict, dry_run: bool = True) -> bool:
    """
    Move file to target category folder.

    Returns: success
    """
    if result['action'] not in ['MOVE', 'REVIEW', 'UNCATEGORIZED']:
        return False

    filepath = result['filepath']
    category = result['category']

    # Determine target directory
    if category == "_UNCATEGORIZED":
        target_dir = CANONICAL_DIR / "_UNCATEGORIZED"
    else:
        target_dir = CANONICAL_DIR / category

    # Create directory if needed
    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    # Target path
    target_path = target_dir / filepath.name

    # Check for duplicates
    if target_path.exists():
        print(f"  ⚠️  Already exists: {target_path.name}")
        return False

    # Move file
    if dry_run:
        print(f"  [DRY RUN] Would move to: {category}/{filepath.name}")
        return True
    else:
        try:
            shutil.copy(filepath, target_path)
            print(f"  ✅ Moved to: {category}/{filepath.name}")
            return True
        except Exception as e:
            print(f"  ❌ Error moving {filepath.name}: {e}")
            return False


def generate_report(results: List[Dict]) -> str:
    """Generate summary report of processing."""

    total = len(results)
    valid = len([r for r in results if r['valid']])
    invalid = total - valid

    moved = len([r for r in results if r['action'] == 'MOVE'])
    review = len([r for r in results if r['action'] == 'REVIEW'])
    uncategorized = len([r for r in results if r['action'] == 'UNCATEGORIZED'])
    skipped = len([r for r in results if r['action'] == 'SKIP'])

    # Count by category
    categories = {}
    for r in results:
        if r['category']:
            categories[r['category']] = categories.get(r['category'], 0) + 1

    report = f"""
# CANONICAL ORGANIZATION REPORT

**Date:** {Path().absolute()}
**Total Files Processed:** {total}

---

## Summary

| Status | Count | Percentage |
|--------|-------|------------|
| **Valid Files** | {valid} | {valid/total*100:.1f}% |
| **Invalid Files** | {invalid} | {invalid/total*100:.1f}% |
| **Ready to Move** | {moved} | {moved/total*100:.1f}% |
| **Need Review** | {review} | {review/total*100:.1f}% |
| **Uncategorized** | {uncategorized} | {uncategorized/total*100:.1f}% |
| **Skipped** | {skipped} | {skipped/total*100:.1f}% |

---

## Files by Category

| Category | Count |
|----------|-------|
"""

    for cat in sorted(categories.keys()):
        count = categories[cat]
        report += f"| {cat} | {count} |\n"

    report += "\n---\n\n## Files Needing Review\n\n"

    review_files = [r for r in results if r['action'] == 'REVIEW']
    if review_files:
        for r in review_files:
            report += f"- `{r['filename']}` → {r['category']} ({r['confidence']:.1%} confidence)\n"
    else:
        report += "*None*\n"

    report += "\n---\n\n## Uncategorized Files\n\n"

    uncat_files = [r for r in results if r['action'] == 'UNCATEGORIZED']
    if uncat_files:
        for r in uncat_files:
            report += f"- `{r['filename']}` - {r['reason']}\n"
    else:
        report += "*None*\n"

    report += "\n---\n\n## Invalid Files\n\n"

    invalid_files = [r for r in results if not r['valid']]
    if invalid_files:
        for r in invalid_files:
            report += f"- `{r['filename']}` - {r['reason']}\n"
    else:
        report += "*None*\n"

    return report


def main():
    """Main execution function."""

    print("="*60)
    print("CANONICAL LIBRARY ORGANIZATION TOOL")
    print("="*60)
    print()

    # Check directories exist
    if not DOWNLOADED_DIR.exists():
        print(f"❌ Downloaded directory not found: {DOWNLOADED_DIR}")
        return

    if not BAD_DIR.exists():
        print(f"❌ Bad directory not found: {BAD_DIR}")
        return

    if not CANONICAL_DIR.exists():
        print(f"❌ Canonical directory not found: {CANONICAL_DIR}")
        return

    # Collect all markdown files
    print("📂 Scanning for markdown files...")

    downloaded_files = list(DOWNLOADED_DIR.rglob("*.md"))
    bad_files = list(BAD_DIR.glob("*.md"))

    print(f"  Found {len(downloaded_files)} files in Downloaded/")
    print(f"  Found {len(bad_files)} files in Bad/")
    print()

    # Process all files
    print("🔍 Processing files...")
    results = []

    for filepath in downloaded_files:
        result = process_file(filepath, "Downloaded")
        results.append(result)

        if result['action'] == 'MOVE':
            print(f"✅ {result['filename']} → {result['category']} ({result['confidence']:.0%})")
        elif result['action'] == 'REVIEW':
            print(f"⚠️  {result['filename']} → {result['category']} ({result['confidence']:.0%}) [REVIEW]")
        elif result['action'] == 'UNCATEGORIZED':
            print(f"❓ {result['filename']} - No clear category")
        else:
            print(f"❌ {result['filename']} - {result['reason']}")

    for filepath in bad_files:
        result = process_file(filepath, "Bad")
        results.append(result)

        if result['valid']:
            print(f"♻️  {result['filename']} (from Bad/) → {result['category']} ({result['confidence']:.0%})")
        else:
            print(f"❌ {result['filename']} (from Bad/) - {result['reason']}")

    print()

    # Generate report
    report = generate_report(results)
    report_path = CANONICAL_DIR / "ORGANIZATION_REPORT.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"📊 Report saved to: {report_path}")
    print()

    # Ask to proceed
    print("="*60)
    print("DRY RUN COMPLETE")
    print("="*60)
    print()
    print("This was a dry run. No files were moved.")
    print()
    response = input("Proceed with actual file moves? (yes/no): ").strip().lower()

    if response == 'yes':
        print()
        print("🚀 Moving files...")

        success_count = 0
        for result in results:
            if move_file(result, dry_run=False):
                success_count += 1

        print()
        print(f"✅ Successfully organized {success_count} files!")
        print(f"📁 Files are now in: {CANONICAL_DIR}")
    else:
        print()
        print("Operation cancelled. Review the report and run again.")

    print()
    print("="*60)
    print("COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
