# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil
import py_compile


RUNNER_ID = "R2829"


def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


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


def restore(bak: Path, target: Path) -> None:
    if bak.exists():
        shutil.copy2(bak, target)


def main() -> int:
    repo = repo_root()
    report: List[str] = []

    ui = repo / "modules" / "ui_toolbar.py"
    if not ui.exists():
        report.append("ERROR: modules/ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    bak = backup(repo, ui)
    report.append(f"- Backup: `{bak}`")

    src = ui.read_text(encoding="utf-8", errors="replace")

    marker = "# R2829_NO_WORKSPACE_ROOTS"
    if marker in src:
        report.append("- Already applied (marker found)")
        write_report(repo, report)
        return 0

    # We ONLY change the resolver to registry-only. No injection into functions.
    old_block = (
        "def _resolve_repo_path(kind: str) -> str:\n"
    )

    if old_block not in src:
        report.append("ERROR: _resolve_repo_path definition not found")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    new_block = (
        "def _resolve_repo_path(kind: str) -> str:\n"
        "    # R2829_NO_WORKSPACE_ROOTS\n"
        "    # Registry is the single source of truth. No workspace/cwd fallbacks.\n"
        "    try:\n"
        "        from pathlib import Path\n"
        "        if kind == 'private':\n"
        "            fp = Path(__file__).resolve().parent.parent / 'registry' / 'private_repo_root.txt'\n"
        "        else:\n"
        "            fp = Path(__file__).resolve().parent.parent / 'registry' / 'public_export_root.txt'\n"
        "        if not fp.exists():\n"
        "            return ''\n"
        "        p = fp.read_text(encoding='utf-8', errors='replace').strip().strip('\"')\n"
        "        if not p:\n"
        "            return ''\n"
        "        root = Path(p)\n"
        "        if root.exists() and (root / '.git').exists():\n"
        "            return str(root)\n"
        "        return ''\n"
        "    except Exception:\n"
        "        return ''\n"
    )

    # Replace only the function header; keep body replacement controlled by indentation.
    # We replace the header line, then rely on the new body above to shadow old logic.
    src = src.replace(old_block, new_block, 1)

    ui.write_text(src, encoding="utf-8")

    try:
        py_compile.compile(str(ui), doraise=True)
        report.append("OK: py_compile passed")
    except Exception as exc:
        report.append(f"COMPILE FAIL: {exc}")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    report.append("SUCCESS:")
    report.append("- Workspace/cwd fallbacks disabled")
    report.append("- Registry is the only root source")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
