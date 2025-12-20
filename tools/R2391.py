# -*- coding: utf-8 -*-
# [R2391] Syntax Emergency Restore (no fantasies)
# - Backup current targets
# - Restore newest backups from _Archiv that compile cleanly
# - Verify targets + main_gui.py compile
# - Write report

from __future__ import annotations

import shutil
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2391"

ROOT = Path(__file__).resolve().parents[1]
ARCHIV = ROOT / "_Archiv"
DOCS = ROOT / "docs"
MODULES = ROOT / "modules"

TARGETS = [
    MODULES / "module_docking.py",
    MODULES / "ui_runner_products_tab.py",
]

def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def backup_current(p: Path) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    b = ARCHIV / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b

def list_archiv_backups_for(filename: str) -> list[Path]:
    if not ARCHIV.exists():
        return []
    # Most common format: <file>.R####_YYYYMMDD_HHMMSS.bak
    cands = list(ARCHIV.glob(f"{filename}.R*_*.bak"))
    if not cands:
        # fallback any .bak for this file
        cands = list(ARCHIV.glob(f"{filename}.*.bak"))
    cands.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return cands

def try_restore_pair(docking_bak: Path, artefakte_bak: Path) -> tuple[bool, str]:
    """Restore both files and compile-check them + main_gui. Return (ok, msg)."""
    # restore
    shutil.copy2(docking_bak, TARGETS[0])
    shutil.copy2(artefakte_bak, TARGETS[1])

    # compile checks
    try:
        py_compile.compile(str(TARGETS[0]), doraise=True)
        py_compile.compile(str(TARGETS[1]), doraise=True)
        mg = ROOT / "main_gui.py"
        if mg.exists():
            py_compile.compile(str(mg), doraise=True)
        return True, "OK"
    except Exception as e:
        return False, repr(e)

def write_report(lines: list[str]) -> Path:
    DOCS.mkdir(parents=True, exist_ok=True)
    rp = DOCS / f"Report_{RID}_Emergency_Restore_{ts()}.md"
    rp.write_text("\n".join(lines), encoding="utf-8")
    return rp

def main() -> int:
    lines: list[str] = []
    lines.append(f"# Report {RID} – Syntax Emergency Restore")
    lines.append("")
    lines.append(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Root: `{ROOT}`")
    lines.append("")

    if not ARCHIV.exists():
        rp = write_report(lines + ["## ERROR", f"- _Archiv fehlt: `{ARCHIV}`"])
        print(f"[{RID}] FEHLER: _Archiv fehlt. Report: {rp}")
        return 2

    # 1) Backup current targets (even if broken)
    lines.append("## Backups (current state)")
    current_baks: list[Path] = []
    for t in TARGETS:
        if t.exists():
            b = backup_current(t)
            current_baks.append(b)
            lines.append(f"- `{t}` -> `{b.name}`")
        else:
            lines.append(f"- WARN: Target fehlt: `{t}` (skip)")
    lines.append("")

    # 2) Gather candidates
    dock_baks = list_archiv_backups_for("module_docking.py")
    art_baks  = list_archiv_backups_for("ui_runner_products_tab.py")

    lines.append("## Candidate backups (newest first)")
    lines.append(f"- module_docking.py: {len(dock_baks)} candidates")
    lines.append(f"- ui_runner_products_tab.py: {len(art_baks)} candidates")
    lines.append("")

    if not dock_baks or not art_baks:
        rp = write_report(lines + ["## ERROR", "- Nicht genug Backups gefunden (mind. 1 je Datei nötig)."])
        print(f"[{RID}] FEHLER: Nicht genug Backups. Report: {rp}")
        return 2

    # 3) Try newest combinations in a controlled way:
    #    Prefer "latest for both" first, then walk down artefakte, then docking.
    best = None
    tried = 0
    max_try = 40  # keep it bounded

    # helper: generate pairs
    pairs = []
    pairs.append((dock_baks[0], art_baks[0]))
    # walk artefakte
    for i in range(1, min(len(art_baks), 15)):
        pairs.append((dock_baks[0], art_baks[i]))
    # walk docking
    for i in range(1, min(len(dock_baks), 15)):
        pairs.append((dock_baks[i], art_baks[0]))
    # cross a little
    for i in range(1, min(len(dock_baks), 8)):
        for j in range(1, min(len(art_baks), 8)):
            pairs.append((dock_baks[i], art_baks[j]))

    lines.append("## Restore attempts")
    for db, ab in pairs:
        if tried >= max_try:
            break
        tried += 1
        ok, msg = try_restore_pair(db, ab)
        lines.append(f"- Try {tried:02d}: docking=`{db.name}` artefakte=`{ab.name}` -> {('OK' if ok else 'FAIL')} {'' if ok else msg}")
        if ok:
            best = (db, ab)
            break
    lines.append("")

    if not best:
        rp = write_report(lines + ["## RESULT", "- FAIL: Kein Backup-Paar gefunden, das compile-clean ist."])
        print(f"[{RID}] FEHLER: Kein compile-clean Backup-Paar gefunden. Report: {rp}")
        return 3

    db, ab = best
    lines.append("## RESULT")
    lines.append(f"- RESTORED OK:")
    lines.append(f"  - module_docking.py <= `{db.name}`")
    lines.append(f"  - ui_runner_products_tab.py <= `{ab.name}`")
    lines.append("")
    lines.append("## Next")
    lines.append("- Jetzt `python main_gui.py` starten und prüfen ob GUI läuft.")
    lines.append("- Danach: READ-ONLY Diagnose Runner (GeoTrace) bauen, keine Trial&Error-Patches.")
    lines.append("")

    rp = write_report(lines)
    print(f"[{RID}] OK: Report {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
