from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RID = "R2692"


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    cp = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return cp.returncode, cp.stdout


def git(cwd: Path, *args: str) -> tuple[int, str]:
    return run(["git", *args], cwd)


def find_public_repo(root: Path) -> Path | None:
    # 1) explicit env override
    env = os.environ.get("SHRIMPDEV_PUBLIC_REPO", "").strip()
    if env:
        p = Path(env).expanduser().resolve()
        if (p / ".git").exists():
            return p

    # 2) common siblings (best-effort)
    candidates = [
        root.parent / "ShrimpDev-Public",
        root.parent / "ShrimpDev_Public",
        root.parent / "ShrimpDev_PUBLIC_EXPORT",
        root.parent / "ShrimpDev_PUBLIC",
    ]
    for c in candidates:
        if (c / ".git").exists():
            return c

    return None


def _rmtree(p: Path) -> None:
    if not p.exists():
        return
    shutil.rmtree(p, ignore_errors=True)


def _copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True)


def _copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def mirror_private_to_public(private_root: Path, public_root: Path) -> list[str]:
    """
    Deterministic mirror: allowlist copy from private->public.
    Intentionally excludes tools/, Reports/, runtime entrypoints, etc.
    Also removes Reports/ from public.
    """
    changes: list[str] = []

    # Remove public Reports always (policy)
    _rmtree(public_root / "Reports")
    changes.append("Removed public/Reports")

    allow_dirs = [
        "modules",
        "docs",
        "Pipeline",
        "Journal",
        "registry",
        ".github/workflows",
    ]
    allow_files = [
        "README.md",
        "CHANGELOG.md",
        "CURRENT_VERSION.txt",
        ".gitignore",
    ]

    # Mirror directories by replace-then-copy (keeps public clean)
    for rel in allow_dirs:
        src = private_root / rel
        dst = public_root / rel
        if src.exists():
            _rmtree(dst)
            _copy_tree(src, dst)
            changes.append(f"Mirrored dir: {rel}")

    # Mirror files (overwrite)
    for rel in allow_files:
        src = private_root / rel
        dst = public_root / rel
        if src.exists():
            _copy_file(src, dst)
            changes.append(f"Mirrored file: {rel}")

    return changes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()

    private_root = Path(a.root).resolve()
    reports = private_root / "Reports"
    reports.mkdir(parents=True, exist_ok=True)
    rep = reports / f"Report_{RID}_{stamp()}.md"

    pub = find_public_repo(private_root)

    lines: list[str] = []
    lines.append(f"[{RID}] PUSH PUBLIC (repo-only; includes mirror private->public)")
    lines.append(f"Time: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Private Root: {private_root}")
    lines.append(f"Public Repo: {pub if pub else '(not found)'}")
    lines.append("")

    if not pub:
        lines.append("ERROR: Could not locate public repo. Set env SHRIMPDEV_PUBLIC_REPO to its path.")
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 2

    # Ensure public is a git repo
    rc, out = git(pub, "rev-parse", "--is-inside-work-tree")
    lines.append("git rev-parse --is-inside-work-tree (public)")
    lines.append(out.rstrip())
    lines.append("")
    if rc != 0 or "true" not in out.lower():
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 3

    # MIRROR step
    try:
        mirror_log = mirror_private_to_public(private_root, pub)
        lines.append("=== mirror private -> public ===")
        lines.extend(mirror_log)
        lines.append("")
    except Exception as e:
        lines.append(f"ERROR during mirror: {e}")
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 4

    # Commit+push in public repo if changes exist
    rc, branch = git(pub, "rev-parse", "--abbrev-ref", "HEAD")
    branch = (branch or "").strip() if rc == 0 else "HEAD"

    rc, status = git(pub, "status", "--porcelain")
    lines.append("git status --porcelain (public)")
    lines.append(status.rstrip())
    lines.append("")
    if rc != 0:
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 5

    if not status.strip():
        lines.append("No changes in public repo after mirror. Nothing to commit/push.")
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] OK: Report: {rep}")
        return 0

    msg = f"{RID}: sync public mirror {stamp()}"
    rc, out = git(pub, "add", "-A")
    lines.append("git add -A (public)")
    lines.append(out.rstrip())
    lines.append("")
    if rc != 0:
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 6

    rc, out = git(pub, "commit", "-m", msg)
    lines.append(f'git commit -m "{msg}" (public)')
    lines.append(out.rstrip())
    lines.append("")
    if rc != 0 and "nothing to commit" not in (out or "").lower():
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 7

    rc, out = git(pub, "push", "origin", branch)
    lines.append(f"git push origin {branch} (public)")
    lines.append(out.rstrip())
    lines.append("")

    rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    if rc == 0:
        print(f"[{RID}] OK: Report: {rep}")
        return 0

    print(f"[{RID}] ERROR: Report: {rep}")
    return 8


if __name__ == "__main__":
    raise SystemExit(main())
