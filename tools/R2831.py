# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil


RUNNER_ID = "R2831"


def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def repo_root() -> Path:
    # tools/R2831.py -> repo root is parent of tools/
    return Path(__file__).resolve().parent.parent


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def backup_file(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(target, bak)
    return bak


def main() -> int:
    repo = repo_root()
    report: List[str] = []

    report.append(f"# {RUNNER_ID} Registry Initializer")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Repo: `{repo}`")
    report.append("")

    reg = repo / "registry"
    ensure_dir(reg)

    priv_fp = reg / "private_repo_root.txt"
    pub_fp  = reg / "public_export_root.txt"

    # Backup existing registry files (if any)
    if priv_fp.exists():
        bak = backup_file(repo, priv_fp)
        report.append(f"- Backup private: `{bak}`")
    if pub_fp.exists():
        bak = backup_file(repo, pub_fp)
        report.append(f"- Backup public: `{bak}`")

    # Determine private root (this repo)
    private_root = repo

    # Determine public root (Sibling: ShrimpDev_PUBLIC_EXPORT)
    if repo.name == "ShrimpDev_REPO":
        public_root = repo.with_name("ShrimpDev_PUBLIC_EXPORT")
    else:
        public_root = repo.parent / "ShrimpDev_PUBLIC_EXPORT"

    ensure_dir(public_root)

    # Write registry
    priv_fp.write_text(str(private_root) + "\n", encoding="utf-8")
    pub_fp.write_text(str(public_root) + "\n", encoding="utf-8")

    report.append("## Written")
    report.append(f"- private_repo_root.txt -> `{private_root}`")
    report.append(f"- public_export_root.txt  -> `{public_root}`")
    report.append("")

    report.append("## Checks")
    report.append(f"- Private exists: **{private_root.exists()}**")
    report.append(f"- Private has .git: **{(private_root / '.git').exists()}**")
    report.append(f"- Public exists: **{public_root.exists()}**")
    report.append(f"- Public has .git: **{(public_root / '.git').exists()}**")
    report.append("")
    report.append("## Note")
    report.append("- No UI files modified.")
    report.append("- Workspace untouched.")
    report.append("- Next: UI will see registry roots.")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
