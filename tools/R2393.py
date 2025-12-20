# -*- coding: utf-8 -*-
# [R2393] Patch ui_runner_products_tab.py: remove internal Toplevel creation in builder
# Minimal invasive: wrap/guard the popup window code so builder always uses parent.
from __future__ import annotations

from pathlib import Path
from datetime import datetime
import shutil
import py_compile
import re

RID = "R2393"
ROOT = Path(__file__).resolve().parents[1]
ARCHIV = ROOT / "_Archiv"
DOCS = ROOT / "docs"
TARGET = ROOT / "modules" / "ui_runner_products_tab.py"

def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(p: Path) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    b = ARCHIV / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b

def write_report(lines: list[str]) -> Path:
    DOCS.mkdir(parents=True, exist_ok=True)
    rp = DOCS / f"Report_{RID}_Artefakte_ToplevelFix_{ts()}.md"
    rp.write_text("\n".join(lines), encoding="utf-8")
    return rp

def main() -> int:
    lines = []
    lines.append(f"# Report {RID} – Artefakte Builder Toplevel Fix")
    lines.append("")
    lines.append(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Target: `{TARGET}`")
    lines.append("")

    if not TARGET.exists():
        rp = write_report(lines + ["## ERROR", "- Target missing."])
        print(f"[{RID}] FEHLER: Target fehlt. Report: {rp}")
        return 2

    bak = backup(TARGET)
    src = TARGET.read_text(encoding="utf-8", errors="replace")

    # Strategy:
    # Find the first occurrence of "win = tk.Toplevel(" inside build_runner_products_tab
    # and force builder to use parent as container:
    # - replace "win = tk.Toplevel(...)" block header with:
    #     win = parent.winfo_toplevel()
    #     # (no centering here)
    #
    # This avoids heavy refactor and keeps downstream code referencing "win" working.
    #
    # NOTE: If file has multiple Toplevel creations, we patch the one inside build_runner_products_tab only.

    # Narrow to function area (best-effort): locate "def build_runner_products_tab"
    m = re.search(r"^def\s+build_runner_products_tab\s*\(.*?\):", src, flags=re.M)
    if not m:
        rp = write_report(lines + ["## ERROR", "- build_runner_products_tab not found."])
        print(f"[{RID}] FEHLER: build_runner_products_tab nicht gefunden. Report: {rp}")
        return 2

    start = m.start()
    # take a window of text after function def to patch locally
    head = src[:start]
    tail = src[start:]

    # replace first "win = tk.Toplevel(" after this point
    rx = re.compile(r"(?m)^(?P<indent>\s*)win\s*=\s*tk\.Toplevel\s*\(.*?\)\s*$")
    mm = rx.search(tail)
    if not mm:
        rp = write_report(lines + ["## RESULT", "- No tk.Toplevel() assignment found inside builder (no-op).", f"- Backup: `{bak}`"])
        print(f"[{RID}] OK: no-op (no internal Toplevel found). Report: {rp}")
        return 0

    indent = mm.group("indent")
    repl = (
        f"{indent}# R2393: Builder must NOT create its own Toplevel (Docking manages windows)\n"
        f"{indent}# Use the existing toplevel that owns 'parent' (Notebook tab or DockManager undocked window)\n"
        f"{indent}win = parent.winfo_toplevel()\n"
        f"{indent}setattr(win, '_restored_from_docking', getattr(win, '_restored_from_docking', False))\n"
    )

    new_tail = tail[:mm.start()] + repl + tail[mm.end():]
    new_src = head + new_tail

    TARGET.write_text(new_src, encoding="utf-8")

    # Compile check
    try:
        py_compile.compile(str(TARGET), doraise=True)
        py_compile.compile(str(ROOT / "modules" / "module_docking.py"), doraise=True)
        py_compile.compile(str(ROOT / "main_gui.py"), doraise=True)
        ok = True
        err = ""
    except Exception as e:
        ok = False
        err = repr(e)

    if not ok:
        # rollback
        shutil.copy2(bak, TARGET)
        rp = write_report(lines + [
            "## FAIL",
            f"- Compile error after patch: {err}",
            f"- Rolled back from: `{bak.name}`",
        ])
        print(f"[{RID}] FEHLER: Compile fail, rollback done. Report: {rp}")
        return 3

    rp = write_report(lines + [
        "## OK",
        f"- Backup: `{bak.name}`",
        "- Patched: internal tk.Toplevel() replaced with parent.winfo_toplevel()",
        "- Expected effect: Artefakte window no longer forces centering; DockManager restore geometry wins.",
        "",
        "## Next",
        "- Restart ShrimpDev and test undock/restore behavior.",
    ])
    print(f"[{RID}] OK: Report {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
