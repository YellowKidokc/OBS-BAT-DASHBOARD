#!/usr/bin/env python3
"""BRANCH_AUDIT - which branches landed, which are floating.

  branch_audit.py ROOT_OR_REPO [more...] [--stale-days 21] [--no-fetch]

A path that is a repo is audited; any other folder is searched one level deep
for repos (e.g. D:\\GitHub). For every remote and local branch: commits ahead of
/ behind the default branch, last commit age, merged or not, PR state (gh).
Read-only: `git fetch` updates remote refs only.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import git, run, has_gh, default_branch, write_report, age_days  # noqa: E402


def find_repos(paths: list[str]) -> list[Path]:
    out = []
    for p in map(lambda x: Path(x).resolve(), paths):
        if (p / ".git").exists():
            out.append(p)
        elif p.is_dir():
            out += sorted(c for c in p.iterdir() if (c / ".git").exists())
    return out


def classify(b: dict, stale: int) -> str:
    if b["merged"]:
        return "LANDED (merged, safe to delete)"
    if b["pr"] == "MERGED":
        return "LANDED via PR (squash/rebase)"
    if b["ahead"] == 0:
        return "EMPTY (nothing beyond default)"
    if b["pr"] == "OPEN":
        return "IN REVIEW (open PR)"
    if b["pr"] == "CLOSED":
        return "ABANDONED? (PR closed unmerged)"
    if b["age"] > stale:
        return "FLOATING + STALE (no PR)"
    return "FLOATING (no PR)"


def audit(repo: Path, fetch: bool, stale: int, gh: bool) -> list[dict]:
    if fetch:
        git(repo, "fetch", "--prune", "--quiet", timeout=120)
    base = default_branch(repo)
    baseref = f"origin/{base}" if git(repo, "rev-parse", "-q", "--verify", f"origin/{base}")[0] == 0 else base
    prs = {}
    if gh:
        rc, out = run(["gh", "pr", "list", "--state", "all", "--limit", "300", "--json", "number,state,headRefName,url"], cwd=repo)
        if rc == 0:
            for p in json.loads(out or "[]"):
                prs.setdefault(p["headRefName"], p)
    _, merged_out = git(repo, "branch", "-a", "--merged", baseref, "--format=%(refname:short)")
    merged = set(merged_out.split())
    _, refs = git(repo, "for-each-ref", "--format=%(refname:short)|%(committerdate:iso-strict)|%(authorname)|%(subject)", "refs/remotes/origin", "refs/heads")
    seen, rows = set(), []
    for line in refs.splitlines():
        ref, date, author, subj = (line.split("|", 3) + [""] * 3)[:4]
        name = ref.removeprefix("origin/")
        if name in ("HEAD", "origin", base) or name in seen:
            continue
        seen.add(name)
        _, ab = git(repo, "rev-list", "--left-right", "--count", f"{ref}...{baseref}")
        ahead, behind = (int(x) for x in ab.split()) if ab and ab.split()[0].isdigit() else (0, 0)
        remote = git(repo, "rev-parse", "-q", "--verify", f"origin/{name}")[0] == 0
        pr = prs.get(name, {})
        b = {"repo": repo.name, "branch": name, "ahead": ahead, "behind": behind, "age": age_days(date),
             "author": author, "subject": subj[:70], "merged": ref in merged and ahead == 0 and ref != base,
             "where": "remote" if remote else "LOCAL ONLY", "pr": pr.get("state", ""), "pr_num": pr.get("number", "")}
        b["merged"] = ahead == 0 and ref in merged
        b["status"] = classify(b, stale)
        rows.append(b)
    return rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--stale-days", type=int, default=21)
    ap.add_argument("--no-fetch", action="store_true")
    a = ap.parse_args(argv)
    repos = find_repos(a.paths)
    gh = has_gh()
    order = ["FLOATING + STALE (no PR)", "FLOATING (no PR)", "ABANDONED? (PR closed unmerged)", "IN REVIEW (open PR)",
             "EMPTY (nothing beyond default)", "LANDED via PR (squash/rebase)", "LANDED (merged, safe to delete)"]
    all_rows = []
    for r in repos:
        print(f"Auditing {r.name} ...", flush=True)
        all_rows += audit(r, not a.no_fetch, a.stale_days, gh)
    counts = {s: sum(b["status"] == s for b in all_rows) for s in order}
    md = ["# BRANCH_AUDIT", "", f"{len(repos)} repos · {len(all_rows)} branches · stale = no commit in {a.stale_days} days",
          "" if gh else "> gh not installed or not signed in: PR states unknown, so squash-merged branches may show as FLOATING.", "",
          "| Status | Branches |", "|---|---|"] + [f"| {s} | {n} |" for s, n in counts.items() if n] + [""]
    for s in order:
        rows = sorted((b for b in all_rows if b["status"] == s), key=lambda b: (b["repo"], -b["ahead"]))
        if not rows:
            continue
        md += [f"## {s} ({len(rows)})", "", "| Repo | Branch | Ahead | Behind | Age (d) | Where | PR | Last commit |", "|---|---|---|---|---|---|---|---|"]
        md += [f"| {b['repo']} | `{b['branch']}` | {b['ahead']} | {b['behind']} | {b['age']} | {b['where']} | {('#' + str(b['pr_num']) + ' ' + b['pr']) if b['pr'] else ''} | {b['subject'].replace('|', '/')} |" for b in rows] + [""]
    print()
    for s, n in counts.items():
        if n:
            print(f"  {n:4}  {s}")
    print(f"\nReport: {write_report('branch_audit', chr(10).join(md))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
