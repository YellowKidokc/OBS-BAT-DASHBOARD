"""Shared helpers for read-only diagnostics. Reports go OUTSIDE the scanned target."""
from __future__ import annotations
import datetime as dt, os, shutil, subprocess
from pathlib import Path


def vaultops_home() -> Path:
    return Path(os.environ.get("VAULTOPS_HOME") or Path.home() / "VaultOps")


def write_report(tool: str, md: str) -> Path:
    d = vaultops_home() / "reports" / tool
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{tool}_{dt.datetime.now():%Y%m%d-%H%M%S}.md"
    p.write_text(md, encoding="utf-8")
    (d / f"{tool}_LATEST.md").write_text(md, encoding="utf-8")
    return p


def run(args: list[str], cwd: Path | None = None, timeout: int = 60) -> tuple[int, str]:
    try:
        r = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=timeout)
        return r.returncode, (r.stdout + r.stderr).rstrip()
    except FileNotFoundError:
        return 127, f"{args[0]} not installed"
    except subprocess.TimeoutExpired:
        return 124, f"timed out after {timeout}s"


def git(repo: Path, *a: str, timeout: int = 60) -> tuple[int, str]:
    return run(["git", "-C", str(repo), *a], timeout=timeout)


def has_gh() -> bool:
    return shutil.which("gh") is not None and run(["gh", "auth", "status"], timeout=15)[0] == 0


def default_branch(repo: Path) -> str:
    rc, out = git(repo, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if rc == 0 and "/" in out:
        return out.split("/", 1)[1]
    for b in ("main", "master"):
        if git(repo, "rev-parse", "--verify", "-q", f"refs/remotes/origin/{b}")[0] == 0:
            return b
    return "main"


def age_days(iso: str) -> int:
    try:
        return (dt.datetime.now(dt.timezone.utc) - dt.datetime.fromisoformat(iso.strip())).days
    except ValueError:
        return -1
