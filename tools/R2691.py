from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

RID = "R2691"


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    cp = subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return cp.returncode, cp.stdout


def git(cwd: Path, *args: str) -> tuple[int, str]:
    return run(["git", *args], cwd)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    a = ap.parse_args()

    root = Path(a.root).resolve()
    reports = root / "Reports"
    reports.mkdir(parents=True, exist_ok=True)
    rep = reports / f"Report_{RID}_{stamp()}.md"

    lines: list[str] = []
    lines.append(f"[{RID}] PUSH PRIVATE (repo-only)")
    lines.append(f"Time: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"Root: {root}")
    lines.append(f"Python: {sys.executable}")
    lines.append("")

    rc, out = git(root, "rev-parse", "--is-inside-work-tree")
    lines.append("git rev-parse --is-inside-work-tree")
    lines.append(out.rstrip())
    lines.append("")
    if rc != 0 or "true" not in out.lower():
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 2

    rc, branch = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    branch = (branch or "").strip() if rc == 0 else "HEAD"

    rc, status = git(root, "status", "--porcelain")
    lines.append("git status --porcelain")
    lines.append(status.rstrip())
    lines.append("")
    if rc != 0:
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 3

    if not status.strip():
        lines.append("No changes. Nothing to commit/push.")
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] OK: Report: {rep}")
        return 0

    msg = f"{RID}: autopush private {stamp()}"
    rc, out = git(root, "add", "-A")
    lines.append("git add -A")
    lines.append(out.rstrip())
    lines.append("")
    if rc != 0:
        rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
        print(f"[{RID}] ERROR: Report: {rep}")
        return 4

    rc, out = git(root, "commit", "-m", msg)
    lines.append(f'git commit -m "{msg}"')
    lines.append(out.rstrip())
    lines.append("")
    if rc != 0:
        # allow "nothing to commit" edge
        if "nothing to commit" not in (out or "").lower():
            rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
            print(f"[{RID}] ERROR: Report: {rep}")
            return 5

    rc, out = git(root, "push", "origin", branch)
    lines.append(f"git push origin {branch}")
    lines.append(out.rstrip())
    lines.append("")
    rep.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    if rc == 0:
        print(f"[{RID}] OK: Report: {rep}")
        return 0
    print(f"[{RID}] ERROR: Report: {rep}")
    return 6


if __name__ == "__main__":
    raise SystemExit(main())
