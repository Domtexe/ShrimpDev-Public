# -*- coding: utf-8 -*-
"""
[R2385] Docking Persist (safe, minimal):
1) main_gui.py: in _init_close_protocol() -> _on_close(): call dm.persist_all() before destroy()
2) modules/ui_toolbar.py: in the *effective* (lower) _action_restart(app) override: call dm.persist_all()

Backups -> _Archiv
Syntax check for touched files
Report -> docs/
"""

from __future__ import annotations
import re
import shutil
import py_compile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIV = ROOT / "_Archiv"
DOCS = ROOT / "docs"

MAIN_GUI = ROOT / "main_gui.py"
UI_TOOLBAR = ROOT / "modules" / "ui_toolbar.py"


def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def backup(path: Path, rid: str) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    b = ARCHIV / f"{path.name}.{rid}_{ts()}.bak"
    shutil.copy2(path, b)
    return b


def write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def patch_main_gui(src: str) -> tuple[str, bool]:
    """
    Insert dm.persist_all() in _init_close_protocol()'s _on_close() before destroy().
    """
    m2 = re.search(r"def\s+_on_close\(\)\s*->\s*None\s*:\s*\n", src)
    if not m2:
        return src, False

    pos = src.find("def _on_close", 0)
    if pos < 0:
        return src, False

    destroy_pos = src.find("self.destroy()", pos)
    if destroy_pos < 0:
        return src, False

    if "R2385: persist docking state before closing" in src:
        return src, False

    line_start = src.rfind("\n", 0, destroy_pos) + 1
    line_end = src.find("\n", destroy_pos)
    if line_end < 0:
        line_end = len(src)
    destroy_line = src[line_start:line_end]
    indent = destroy_line[:len(destroy_line) - len(destroy_line.lstrip(" "))]

    block = (
        f"{indent}# R2385: persist docking state before closing (best-effort)\n"
        f"{indent}try:\n"
        f"{indent}    dm = getattr(self, \"_dock_manager\", None)\n"
        f"{indent}    if dm is not None:\n"
        f"{indent}        dm.persist_all()\n"
        f"{indent}except Exception:\n"
        f"{indent}    pass\n\n"
    )

    new_src = src[:line_start] + block + src[line_start:]
    return new_src, True


def patch_ui_toolbar_restart(src: str) -> tuple[str, bool]:
    """
    Patch the *lower* override of _action_restart(app) (R2072 section).
    Insert dm.persist_all() right after _r2072_safe_call_save_state(app)
    """
    if "R2385: persist docking before restart" in src:
        return src, False

    start = src.find("# R2072_AOT_RESTART_START")
    if start < 0:
        start = 0

    matches = list(re.finditer(r"^def\s+_action_restart\s*\(\s*app\s*\)\s*:\s*", src, flags=re.M))
    if not matches:
        return src, False

    cand = [m for m in matches if m.start() >= start]
    m = cand[-1] if cand else matches[-1]
    block_start = m.start()

    call_pos = src.find("_r2072_safe_call_save_state(app)", block_start)
    if call_pos < 0:
        return src, False

    line_end = src.find("\n", call_pos)
    if line_end < 0:
        line_end = len(src)

    call_line_start = src.rfind("\n", 0, call_pos) + 1
    call_line = src[call_line_start:line_end]
    indent = call_line[:len(call_line) - len(call_line.lstrip(" "))]

    inject = (
        f"\n{indent}# R2385: persist docking before restart (best-effort)\n"
        f"{indent}try:\n"
        f"{indent}    dm = getattr(app, \"_dock_manager\", None)\n"
        f"{indent}    if dm is not None:\n"
        f"{indent}        dm.persist_all()\n"
        f"{indent}except Exception:\n"
        f"{indent}    pass\n"
    )

    new_src = src[:line_end] + inject + src[line_end:]
    return new_src, True


def main() -> int:
    rid = "R2385"
    DOCS.mkdir(parents=True, exist_ok=True)

    changed: list[str] = []
    backups: list[str] = []

    # main_gui.py
    if MAIN_GUI.exists():
        src = read(MAIN_GUI)
        new_src, ok = patch_main_gui(src)
        if ok:
            backups.append(str(backup(MAIN_GUI, rid)))
            write(MAIN_GUI, new_src)
            changed.append(str(MAIN_GUI))
    else:
        print(f"[{rid}] WARN: missing {MAIN_GUI}")

    # ui_toolbar.py
    if UI_TOOLBAR.exists():
        src = read(UI_TOOLBAR)
        new_src, ok = patch_ui_toolbar_restart(src)
        if ok:
            backups.append(str(backup(UI_TOOLBAR, rid)))
            write(UI_TOOLBAR, new_src)
            changed.append(str(UI_TOOLBAR))
    else:
        print(f"[{rid}] WARN: missing {UI_TOOLBAR}")

    # syntax checks
    for f in changed:
        try:
            py_compile.compile(f, doraise=True)
        except Exception as e:
            print(f"[{rid}] COMPILE FAIL: {f} -> {e!r}")
            # rollback touched files by restoring backups (best-effort)
            for b in backups:
                orig = Path(b)
                # backup file name: <origName>.R2385_<ts>.bak
                base_name = orig.name.split(f".{rid}_")[0]
                target = ROOT / base_name
                if target.exists():
                    try:
                        shutil.copy2(orig, target)
                    except Exception:
                        pass
            return 3

    report = DOCS / f"Report_{rid}_Docking_Persist_{ts()}.md"

    report_lines = [
        f"# Report {rid} – Docking Persist before Restart/Close",
        "",
        f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Changed files: {len(changed)}",
        *([f"  - {p}" for p in changed] if changed else ["  - (no changes)"]),
        "",
        "## Backups",
        *([f"- {b}" for b in backups] if backups else ["- (none)"]),
        "",
        "## Notes",
        "- main_gui: dm.persist_all() before destroy() (best-effort)",
        "- ui_toolbar: in effective restart override, dm.persist_all() after save_state",
        "",
    ]

    report.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"[{rid}] OK: Report {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
