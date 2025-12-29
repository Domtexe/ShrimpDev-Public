# -*- coding: utf-8 -*-
"""
R2862 – SYNC: Private -> Public Export (+ optional git push)

Policy:
- Public export is a mirror for sharing; it must not be blocked by private-only artifacts.
- tools/Archiv is documentation, not executable code (may be excluded from export if desired).

Config:
- registry/public_export_root.txt (one line path) optional
- registry/public_export_excludes.txt optional (one glob pattern per line)

Default excludes are conservative and avoid typical junk/secrets.
"""

from __future__ import annotations

import fnmatch
import os
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Tuple

RUNNER_ID = "R2862"
EXIT_FAIL = 11


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now_stamp()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def read_text_safe(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def resolve_public_root(private_root: Path) -> Path:
    # 1) registry/public_export_root.txt
    reg = private_root / "registry" / "public_export_root.txt"
    if reg.exists():
        s = read_text_safe(reg).strip().strip('"')
        if s:
            return Path(s).expanduser().resolve()

    # 2) sibling default
    return (private_root.parent / "ShrimpDev_PUBLIC_EXPORT").resolve()


def load_excludes(private_root: Path) -> List[str]:
    # Default excludes: keep public clean + reduce risk
    defaults = [
        ".git/**",
        ".github/**/secrets*",
        "__pycache__/**",
        "*.pyc",
        "*.pyo",
        ".venv/**",
        "venv/**",
        ".mypy_cache/**",
        ".pytest_cache/**",
        ".ruff_cache/**",
        ".idea/**",
        ".vscode/**",
        "_Snapshots/**",
        "_OldStuff/**",
        "_Old/**",
        "_Temp/**",
        "temp/**",
        "tmp/**",
        "*.tmp",
        "*.log",
        "*.bak",
        "*.zip",
        "Reports/**",          # reports are private diagnostics; if you want them public remove this
        "registry/**",         # registry can contain local paths; keep private by default
        "ShrimpDev.ini",       # almost always machine-specific
    ]

    # Optional override/additions
    f = private_root / "registry" / "public_export_excludes.txt"
    if f.exists():
        for line in read_text_safe(f).splitlines():
            t = line.strip()
            if not t or t.startswith("#"):
                continue
            defaults.append(t)
    return defaults


def rel_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_excluded(rel: str, patterns: List[str]) -> bool:
    # match both "dir/**" and plain globs
    for pat in patterns:
        pat = pat.strip()
        if not pat:
            continue
        if fnmatch.fnmatch(rel, pat):
            return True
        # also allow "dir/**" to match "dir"
        if pat.endswith("/**") and rel == pat[:-3]:
            return True
    return False


@dataclass
class SyncStats:
    copied: int = 0
    skipped: int = 0
    deleted: int = 0
    errors: int = 0


def sync_tree(src_root: Path, dst_root: Path, excludes: List[str], report: List[str]) -> SyncStats:
    """
    One-way sync:
    - Copy/update from src -> dst
    - Remove files in dst that no longer exist in src (within exported scope)
    """
    stats = SyncStats()

    ensure_dir(dst_root)

    # 1) Build src set
    src_files: List[Tuple[str, Path]] = []
    for dirpath, dirnames, filenames in os.walk(src_root):
        dp = Path(dirpath)
        # prune excluded directories early
        rel_dp = rel_posix(dp, src_root)
        if rel_dp == ".":
            rel_dp = ""
        # prune children dirs
        pruned = []
        for d in list(dirnames):
            rel_dir = f"{rel_dp}/{d}".lstrip("/")
            if is_excluded(rel_dir, excludes) or is_excluded(rel_dir + "/**", excludes):
                pruned.append(d)
        for d in pruned:
            dirnames.remove(d)

        for fn in filenames:
            sp = dp / fn
            rel = rel_posix(sp, src_root)
            if is_excluded(rel, excludes):
                stats.skipped += 1
                continue
            src_files.append((rel, sp))

    # 2) Copy/update
    for rel, sp in src_files:
        dp = dst_root / rel
        try:
            ensure_dir(dp.parent)
            # copy if missing or different mtime/size
            if (not dp.exists()) or (sp.stat().st_size != dp.stat().st_size) or (int(sp.stat().st_mtime) != int(dp.stat().st_mtime)):
                shutil.copy2(sp, dp)
                stats.copied += 1
            else:
                stats.skipped += 1
        except Exception as e:
            stats.errors += 1
            report.append(f"- ERROR copy `{rel}`: {type(e).__name__}: {e}")

    # 3) Delete files that exist in dst but not in src (within exported scope)
    src_rel_set = set(rel for rel, _ in src_files)
    for dirpath, dirnames, filenames in os.walk(dst_root):
        dp = Path(dirpath)
        rel_dp = rel_posix(dp, dst_root)
        if rel_dp == ".":
            rel_dp = ""

        # prune excluded directories in dst too (we don't touch them)
        pruned = []
        for d in list(dirnames):
            rel_dir = f"{rel_dp}/{d}".lstrip("/")
            if is_excluded(rel_dir, excludes) or is_excluded(rel_dir + "/**", excludes):
                pruned.append(d)
        for d in pruned:
            dirnames.remove(d)

        for fn in filenames:
            fp = dp / fn
            rel = rel_posix(fp, dst_root)
            if is_excluded(rel, excludes):
                continue
            if rel not in src_rel_set:
                try:
                    fp.unlink()
                    stats.deleted += 1
                except Exception as e:
                    stats.errors += 1
                    report.append(f"- ERROR delete `{rel}`: {type(e).__name__}: {e}")

    return stats


def is_git_repo(p: Path) -> bool:
    return (p / ".git").exists() and (p / ".git").is_dir()


def run_git(p: Path, args: List[str]) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(p)] + args, capture_output=True, text=True)


def git_has_changes(p: Path) -> bool:
    r = run_git(p, ["status", "--porcelain"])
    return bool((r.stdout or "").strip())


def git_has_remote(p: Path) -> bool:
    r = run_git(p, ["remote", "-v"])
    return bool((r.stdout or "").strip())


def main(root_arg: str) -> int:
    private_root = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} SYNC: Private -> Public Export")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Private: `{private_root}`")

    try:
        public_root = resolve_public_root(private_root)
        report.append(f"- Public: `{public_root}`")
        report.append("")

        excludes = load_excludes(private_root)
        report.append("## Excludes (effective)")
        for pat in excludes:
            report.append(f"- `{pat}`")
        report.append("")

        ensure_dir(public_root)

        report.append("## Sync")
        stats = sync_tree(private_root, public_root, excludes, report)
        report.append("")
        report.append("## Stats")
        report.append(f"- copied/updated: **{stats.copied}**")
        report.append(f"- skipped: **{stats.skipped}**")
        report.append(f"- deleted: **{stats.deleted}**")
        report.append(f"- errors: **{stats.errors}**")
        report.append("")

        # Optional git operations
        report.append("## Git (Public)")
        if is_git_repo(public_root):
            report.append("- Public folder is a git repo: OK")
            if git_has_changes(public_root):
                msg = f"{RUNNER_ID}: public export sync {now_stamp()}"
                run_git(public_root, ["add", "-A"])
                c = run_git(public_root, ["commit", "-m", msg])
                if (c.returncode != 0) and ("nothing to commit" not in (c.stdout or "").lower()) and ("nothing to commit" not in (c.stderr or "").lower()):
                    report.append(f"- WARN: commit rc={c.returncode}")
                    if (c.stdout or "").strip():
                        report.append("```text\n" + c.stdout.strip() + "\n```")
                    if (c.stderr or "").strip():
                        report.append("```text\n" + c.stderr.strip() + "\n```")
                else:
                    report.append(f"- commit: `{msg}` (or nothing-to-commit)")

                if git_has_remote(public_root):
                    p = run_git(public_root, ["push"])
                    report.append(f"- push rc={p.returncode}")
                    if (p.stdout or "").strip():
                        report.append("```text\n" + p.stdout.strip() + "\n```")
                    if (p.stderr or "").strip():
                        report.append("```text\n" + p.stderr.strip() + "\n```")
                else:
                    report.append("- SKIP: no git remote configured in public repo")
            else:
                report.append("- No changes to commit")
        else:
            report.append("- SKIP: public folder is not a git repo (.git missing)")
            report.append("- You can `git clone` your public repo into this folder once, then rerun R2862.")
        report.append("")

        rp = write_report(private_root, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0 if stats.errors == 0 else EXIT_FAIL

    except Exception as e:
        report.append(f"ERROR: {type(e).__name__}: {e}")
        rp = write_report(private_root, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL


if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
