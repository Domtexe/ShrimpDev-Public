# -*- coding: utf-8 -*-
from __future__ import annotations

import shutil
from pathlib import Path
from datetime import datetime
from typing import List


RUNNER_ID = "R2825"


def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def read_reg(repo: Path, name: str) -> Path | None:
    fp = repo / "registry" / name
    if fp.exists():
        txt = fp.read_text(encoding="utf-8", errors="replace").strip()
        if txt:
            return Path(txt)
    return None


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(target, bak)
    return bak


def main() -> int:
    repo = repo_root()
    report: List[str] = []

    report.append(f"# {RUNNER_ID} Push Button Enable Fix")
    report.append(f"- Root: `{repo}`")
    report.append("")

    ui_file = repo / "modules" / "ui_toolbar.py"
    if not ui_file.exists():
        report.append("ERROR: ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    bak = backup(repo, ui_file)
    report.append(f"- Backup: `{bak}`")
    report.append("")

    src = ui_file.read_text(encoding="utf-8", errors="replace")

    marker = "# R2825_PUSH_STATE"
    if marker in src:
        report.append("- Already patched (marker found)")
        write_report(repo, report)
        return 0

    patch = f"""
{marker}
def _r2825_repo_exists(path_str):
    try:
        if not path_str:
            return False
        p = Path(path_str)
        return p.exists() and (p / ".git").exists()
    except Exception:
        return False
"""

    if "_update_push_states" not in src:
        report.append("ERROR: _update_push_states not found")
        write_report(repo, report)
        return 11

    src = src.replace(
        "def _update_push_states():",
        "def _update_push_states():\n" + patch
    )

    src = src.replace(
        "private_pushable =",
        "private_pushable = _r2825_repo_exists(private_root) and"
    )

    src = src.replace(
        "public_pushable =",
        "public_pushable = _r2825_repo_exists(public_root) and"
    )

    ui_file.write_text(src, encoding="utf-8")

    report.append("## Result")
    report.append("- Push enable logic now depends ONLY on:")
    report.append("  - registry/private_repo_root.txt + .git")
    report.append("  - registry/public_export_root.txt + .git")
    report.append("- Workspace ignored")
    report.append("- No heuristics")
    report.append("")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
