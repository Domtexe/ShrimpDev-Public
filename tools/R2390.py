# -*- coding: utf-8 -*-
# R2390 - Crash-Recovery Runner (no fantasies)
# - backups current broken files
# - restores newest matching .bak from _Archiv
# - py_compile verifies
# - writes report to docs

from __future__ import annotations

import sys
import shutil
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2390"

ROOT = Path(__file__).resolve().parents[1]
ARCHIV = ROOT / "_Archiv"
DOCS = ROOT / "docs"
MODULES = ROOT / "modules"

TARGETS = [
    MODULES / "module_docking.py",
    MODULES / "ui_runner_products_tab.py",
]

def _ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _backup_current(src: Path) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    bak = ARCHIV / f"{src.name}.{RID}_{_ts()}.bak"
    shutil.copy2(src, bak)
    return bak

def _find_latest_archiv_backup(filename: str) -> Path | None:
    if not ARCHIV.exists():
        return None

    # Accept any runner suffix: <file>.R####_YYYYMMDD_HHMMSS.bak OR <file>.R####...bak
    candidates = list(ARCHIV.glob(f"{filename}.R*_*.bak"))
    if not candidates:
        # fallback: older naming variants
        candidates = list(ARCHIV.glob(f"{filename}.*.bak"))

    if not candidates:
        return None

    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]

def _write_report(lines: list[str]) -> Path:
    DOCS.mkdir(parents=True, exist_ok=True)
    rp = DOCS / f"Report_{RID}_Crash_Recovery_{_ts()}.md"
    rp.write_text("\n".join(lines), encoding="utf-8")
    return rp

def main() -> int:
    lines: list[str] = []
    lines.append(f"# Report {RID} – Crash-Recovery (Rollback)")
    lines.append("")
    lines.append(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Root: `{ROOT}`")
    lines.append("")

    if not ARCHIV.exists():
        rp = _write_report(lines + ["## ERROR", f"- _Archiv fehlt: `{ARCHIV}`"])
        print(f"[{RID}] FEHLER: _Archiv fehlt. Report: {rp}")
        return 2

    backups_made = []
    restores = []

    # 1) Backup current files (even if broken)
    for t in TARGETS:
        if t.exists():
            b = _backup_current(t)
            backups_made.append((t, b))
        else:
            lines.append("## WARN")
            lines.append(f"- Target fehlt (skip backup): `{t}`")
            lines.append("")

    # 2) Restore newest good backups from _Archiv
    ok = True
    for t in TARGETS:
        latest = _find_latest_archiv_backup(t.name)
        if latest is None:
            ok = False
            lines.append("## ERROR")
            lines.append(f"- Kein Backup gefunden in _Archiv für `{t.name}`")
            lines.append("")
            continue

        # restore
        shutil.copy2(latest, t)
        restores.append((t, latest))

    # 3) Syntax check
    lines.append("## Backups (current state)")
    for t, b in backups_made:
        lines.append(f"- `{t}` -> `{b.name}`")
    if not backups_made:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Restores (from _Archiv)")
    for t, src in restores:
        lines.append(f"- `{t.name}` <= `{src.name}`")
    if not restores:
        lines.append("- (none)")
    lines.append("")

    lines.append("## Syntax-Check (py_compile)")
    rc = 0
    try:
        # compile targets + main_gui import surface
        for t in TARGETS:
            if t.exists():
                py_compile.compile(str(t), doraise=True)
                lines.append(f"- OK: {t.name}")
        main_gui = ROOT / "main_gui.py"
        if main_gui.exists():
            py_compile.compile(str(main_gui), doraise=True)
            lines.append("- OK: main_gui.py")
    except Exception as e:
        rc = 3
        lines.append(f"- FAIL: {e!r}")

    rp = _write_report(lines)
    print(f"[{RID}] OK: Report {rp}")

    # if restore candidates missing, signal clearly
    if not ok:
        return 2
    return rc

if __name__ == "__main__":
    raise SystemExit(main())
