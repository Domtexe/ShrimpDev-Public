# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil
import py_compile


RUNNER_ID = "R2827"


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
        report.append("ERROR: ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    bak = backup(repo, ui)
    report.append(f"- Backup: `{bak}`")

    src = ui.read_text(encoding="utf-8", errors="replace")

    old_priv = "private_pushable = bool(has_private and private_root and _is_repo_pushable(private_root))"
    old_pub  = "public_pushable = bool(has_public and public_root and _is_repo_pushable(public_root))"

    new_priv = "private_pushable = bool(has_private and private_root and (Path(private_root) / '.git').exists())"
    new_pub  = "public_pushable = bool(has_public  and public_root  and (Path(public_root)  / '.git').exists())"

    if old_priv not in src or old_pub not in src:
        report.append("ERROR: Expected lines not found. Patch aborted.")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    src = src.replace(old_priv, new_priv)
    src = src.replace(old_pub,  new_pub)

    ui.write_text(src, encoding="utf-8")

    # Compile check
    try:
        py_compile.compile(str(ui), doraise=True)
        report.append("OK: py_compile passed")
    except Exception as exc:
        report.append(f"COMPILE FAIL: {exc}")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    report.append("SUCCESS: Push button gating relaxed to repo-exists logic")
    report.append("- Buttons depend on .git presence, not repo status")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
