#!/usr/bin/env python3
"""REPO_READY - one-line GO / NO-GO for a repo before handing work to an AI.

  repo_ready.py REPO [--no-fetch] [--tests]

Checks: uncommitted/untracked changes, current branch vs upstream (ahead/behind),
local branches never pushed or ahead of their upstream, stashes, merge/rebase in
progress, open PRs (gh, if signed in), and optionally runs the detected test
command. Read-only for the working tree: `git fetch` updates remote refs only.
"""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from _common import git, run, has_gh, default_branch, write_report  # noqa: E402


def detect_tests(repo: Path) -> list[str] | None:
    if (repo / "pyproject.toml").exists() or (repo / "pytest.ini").exists() or (repo / "tests").is_dir():
        return [sys.executable, "-m", "pytest", "-q", "-x"]
    if (repo / "package.json").exists():
        try:
            if "test" in json.loads((repo / "package.json").read_text(encoding="utf-8")).get("scripts", {}):
                return ["npm", "test", "--silent"]
        except ValueError:
            pass
    if (repo / "Cargo.toml").exists():
        return ["cargo", "test", "-q"]
    if (repo / "go.mod").exists():
        return ["go", "test", "./..."]
    return None


def check(repo: Path, fetch: bool, tests: bool) -> tuple[str, list[tuple[str, str, str]]]:
    rows = []  # (level, check, detail)  level: BLOCK / WARN / OK
    add = lambda lvl, c, d: rows.append((lvl, c, d))
    if git(repo, "rev-parse", "--git-dir")[0]:
        return "NO-GO", [("BLOCK", "Git repo", "Not a git repository")]
    if fetch:
        rc, out = git(repo, "fetch", "--prune", "--quiet", timeout=120)
        add("WARN" if rc else "OK", "Fetch", "Could not reach remote: " + out[:120] if rc else "Remote refs up to date")
    _, branch = git(repo, "branch", "--show-current")
    add("OK" if branch else "BLOCK", "Branch", branch or "Detached HEAD")
    gd = Path(git(repo, "rev-parse", "--absolute-git-dir")[1])
    for marker, label in (("MERGE_HEAD", "merge"), ("rebase-merge", "rebase"), ("rebase-apply", "rebase/am"), ("CHERRY_PICK_HEAD", "cherry-pick")):
        if (gd / marker).exists():
            add("BLOCK", "In progress", f"A {label} is in progress - finish or abort it")
    _, st = git(repo, "status", "--porcelain=v1")
    lines = [l for l in st.splitlines() if l]
    mod = [l for l in lines if not l.startswith("??")]
    unt = [l for l in lines if l.startswith("??")]
    add("BLOCK" if mod else "OK", "Uncommitted changes", f"{len(mod)} changed: " + ", ".join(l[3:] for l in mod[:6]) if mod else "Clean")
    if unt:
        add("WARN", "Untracked files", f"{len(unt)}: " + ", ".join(l[3:] for l in unt[:6]))
    rc, up = git(repo, "rev-parse", "--abbrev-ref", "@{upstream}")
    if rc:
        add("BLOCK", "Upstream", f"'{branch}' has never been pushed")
    else:
        _, ab = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{upstream}")
        ahead, behind = (int(x) for x in ab.split())
        if ahead:
            add("BLOCK", "Unpushed commits", f"{ahead} commit(s) on '{branch}' not on {up}")
        if behind:
            add("WARN", "Behind remote", f"{behind} commit(s) on {up} not pulled")
        if not ahead and not behind:
            add("OK", "In sync", f"'{branch}' matches {up}")
    _, refs = git(repo, "for-each-ref", "--format=%(refname:short)|%(upstream:short)|%(upstream:track)", "refs/heads")
    floating = []
    for r in refs.splitlines():
        name, upn, track = (r.split("|") + ["", ""])[:3]
        if name == branch:
            continue
        if not upn:
            floating.append(f"{name} (never pushed)")
        elif "ahead" in track:
            floating.append(f"{name} {track}")
    if floating:
        add("WARN", "Other local branches", f"{len(floating)}: " + "; ".join(floating[:8]))
    _, stash = git(repo, "stash", "list")
    if stash:
        add("WARN", "Stashes", f"{len(stash.splitlines())} stash(es) - work parked here")
    base = default_branch(repo)
    if branch and branch != base and git(repo, "rev-parse", "-q", "--verify", f"origin/{base}")[0] == 0:
        _, ab = git(repo, "rev-list", "--left-right", "--count", f"HEAD...origin/{base}")
        a, b = ab.split()
        if int(b):
            add("WARN", f"vs {base}", f"{a} ahead, {b} behind origin/{base} - may need a merge")
    if has_gh():
        rc, out = run(["gh", "pr", "list", "--state", "open", "--json", "number,title,headRefName,isDraft,mergeable"], cwd=repo)
        if rc == 0:
            prs = json.loads(out or "[]")
            mine = [p for p in prs if p["headRefName"] == branch]
            conflict = [p for p in prs if p.get("mergeable") == "CONFLICTING"]
            add("OK", "Open PRs", f"{len(prs)} open" + (f"; this branch -> #{mine[0]['number']}" if mine else ""))
            if conflict:
                add("WARN", "PR conflicts", ", ".join(f"#{p['number']}" for p in conflict))
    else:
        add("WARN", "Open PRs", "gh not installed or not signed in - PRs not checked")
    if tests:
        cmd = detect_tests(repo)
        if not cmd:
            add("WARN", "Tests", "No test command detected")
        else:
            rc, out = run(cmd, cwd=repo, timeout=900)
            add("BLOCK" if rc else "OK", "Tests", f"{' '.join(cmd[-3:])}: " + ("FAILED - " + out.splitlines()[-1][:150] if rc and out else "passed"))
    verdict = "NO-GO" if any(r[0] == "BLOCK" for r in rows) else ("GO (with warnings)" if any(r[0] == "WARN" for r in rows) else "GO")
    return verdict, rows


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repos", nargs="+")
    ap.add_argument("--no-fetch", action="store_true")
    ap.add_argument("--tests", action="store_true", help="also run the detected test suite")
    a = ap.parse_args(argv)
    md, worst = ["# REPO_READY", ""], 0
    icon = {"BLOCK": "✕", "WARN": "!", "OK": "✓"}
    for r in a.repos:
        repo = Path(r).resolve()
        verdict, rows = check(repo, not a.no_fetch, a.tests)
        worst = max(worst, 2 if verdict == "NO-GO" else 1 if "warn" in verdict else 0)
        print(f"\n{verdict:20} {repo}")
        for lvl, c, d in rows:
            if lvl != "OK":
                print(f"   {icon[lvl]} {c}: {d}")
        md += [f"## {verdict} — `{repo}`", "", "| | Check | Detail |", "|---|---|---|"]
        md += [f"| {icon[l]} | {c} | {d.replace('|', '/')} |" for l, c, d in rows] + [""]
    print(f"\nReport: {write_report('repo_ready', chr(10).join(md))}")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
