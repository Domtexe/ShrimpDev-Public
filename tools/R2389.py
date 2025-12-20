# -*- coding: utf-8 -*-
"""
[R2389] UI Center-Guard after Docking restore

- module_docking.py:
  mark restored windows with win._restored_from_docking = True

- ui_runner_products_tab.py:
  only center window if NOT restored from docking
"""

from pathlib import Path
from datetime import datetime
import shutil
import py_compile

RID = "R2389"

ROOT = Path(__file__).resolve().parents[1]
ARCHIV = ROOT / "_Archiv"
DOCS = ROOT / "docs"

F_DOCK = ROOT / "modules" / "module_docking.py"
F_RP   = ROOT / "modules" / "ui_runner_products_tab.py"


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(p: Path):
    ARCHIV.mkdir(parents=True, exist_ok=True)
    b = ARCHIV / f"{p.name}.{RID}_{ts()}.bak"
    shutil.copy2(p, b)
    return b


def patch_module_docking(src: str):
    marker = "_restored_from_docking"
    if marker in src:
        return src, False

    needle = "w.geometry(geo)"
    if needle not in src:
        return src, False

    insert = (
        "                w.geometry(geo)\n"
        "                # R2389: mark window as restored from docking\n"
        "                try:\n"
        "                    w._restored_from_docking = True\n"
        "                except Exception:\n"
        "                    pass\n"
    )

    return src.replace(needle, insert, 1), True


def patch_runner_products(src: str):
    marker = "_restored_from_docking"
    if marker in src:
        return src, False

    needle = "win.update_idletasks()"
    if needle not in src:
        return src, False

    block = (
        "win.update_idletasks()\n"
        "        # R2389: do not re-center if restored from docking\n"
        "        if not getattr(win, '_restored_from_docking', False):\n"
    )

    return src.replace(needle, block, 1), True


def main():
    DOCS.mkdir(parents=True, exist_ok=True)

    changed = []
    backups = []

    # --- module_docking.py ---
    src = F_DOCK.read_text(encoding="utf-8", errors="replace")
    patched, ok = patch_module_docking(src)
    if ok:
        backups.append(backup(F_DOCK))
        F_DOCK.write_text(patched, encoding="utf-8")
        changed.append(F_DOCK)

    # --- ui_runner_products_tab.py ---
    src = F_RP.read_text(encoding="utf-8", errors="replace")
    patched, ok = patch_runner_products(src)
    if ok:
        backups.append(backup(F_RP))
        F_RP.write_text(patched, encoding="utf-8")
        changed.append(F_RP)

    # syntax check
    for f in changed:
        py_compile.compile(str(f), doraise=True)

    report = DOCS / f"Report_{RID}_UI_Center_Guard_{ts()}.md"
    report.write_text(
        "\n".join([
            f"# Report {RID} – UI Center Guard after Docking restore",
            "",
            f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- Changed files: {len(changed)}",
            *[f"  - {p}" for p in changed],
            "",
            "## Effect",
            "- Undocked windows keep restored geometry",
            "- UI centering only on first open",
            "",
            "## Backups",
            *[f"- {b}" for b in backups],
            ""
        ]),
        encoding="utf-8"
    )

    print(f"[{RID}] OK: Report {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
