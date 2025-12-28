# R2865.py
# SAFE PATCH: Fix NameError frame_toolbar_right in modules/ui_toolbar.py by adding compat alias.
# - creates backup to _Archiv
# - writes report to Reports
# - compile-check; on failure auto-rollback

from __future__ import annotations

import datetime as _dt
import os
import re
import shutil
import sys
import py_compile
from pathlib import Path


CODE_OK = 0
CODE_FAIL = 11


def _now_stamp() -> str:
    return _dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def _write_report(report_path: Path, lines: list[str]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")


def _backup_file(root: Path, src: Path, runner_id: str) -> Path:
    arch = root / "_Archiv"
    arch.mkdir(parents=True, exist_ok=True)
    ts = _now_stamp()
    bak = arch / f"{src.name}.{runner_id}_{ts}.bak"
    shutil.copy2(src, bak)
    return bak


def _py_compile_one(path: Path) -> tuple[bool, str]:
    try:
        py_compile.compile(str(path), doraise=True)
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def _already_has_alias(block: str) -> bool:
    return bool(re.search(r"^\s*frame_toolbar_right\s*=\s*parent\s*$", block, re.M))


def patch_ui_toolbar(target: Path) -> tuple[bool, str]:
    txt = target.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines(True)

    # Find function def line
    # We patch immediately after "def build_toolbar_right(...):"
    pat = re.compile(r"^\s*def\s+build_toolbar_right\s*\(.*\)\s*:\s*$")
    idx = None
    for i, ln in enumerate(lines):
        if pat.match(ln):
            idx = i
            break

    if idx is None:
        return False, "Konnte 'def build_toolbar_right(...):' nicht finden."

    # Look ahead a bit to avoid duplicate insertion
    lookahead = "".join(lines[idx : min(len(lines), idx + 40)])
    if _already_has_alias(lookahead):
        return True, "Alias existiert bereits (no-op)."

    insert = (
        "    # Compat alias (legacy patches may reference this name)\n"
        "    frame_toolbar_right = parent\n"
        "\n"
    )

    # Insert right after def line (safe: before any code uses it)
    lines.insert(idx + 1, insert)

    new_txt = "".join(lines)
    if new_txt == txt:
        return True, "Keine Änderungen nötig (no-op)."

    target.write_text(new_txt, encoding="utf-8", errors="replace")
    return True, "Alias eingefügt."


def main(root: Path) -> int:
    runner_id = "R2865"
    ts = _now_stamp()

    reports_dir = root / "Reports"
    report_path = reports_dir / f"Report_{runner_id}_{ts}.md"

    target = root / "modules" / "ui_toolbar.py"

    out: list[str] = []
    out.append(f"# {runner_id} SAFE PATCH – ui_toolbar compat alias")
    out.append("")
    out.append(f"- Root: `{root}`")
    out.append(f"- Target: `{target}`")
    out.append("")

    if not target.exists():
        out.append("## FAIL")
        out.append("")
        out.append(f"Target not found: `{target}`")
        _write_report(report_path, out)
        print(f"[{runner_id}] FAIL: target not found")
        print(f"[{runner_id}] Report: {report_path}")
        return CODE_FAIL

    backup = _backup_file(root, target, runner_id)
    out.append("## Backup")
    out.append("")
    out.append(f"- Backup: `{backup}`")
    out.append("")

    ok, note = patch_ui_toolbar(target)
    out.append("## Patch")
    out.append("")
    out.append(f"- Result: **{ok}**")
    out.append(f"- Note: {note}")
    out.append("")

    # compile check (must pass)
    c_ok, c_msg = _py_compile_one(target)
    out.append("## Compile Check")
    out.append("")
    out.append(f"- py_compile: **{c_ok}**")
    out.append(f"- detail: `{c_msg}`")
    out.append("")

    if not ok or not c_ok:
        # rollback
        try:
            shutil.copy2(backup, target)
            rb_ok, rb_msg = _py_compile_one(target)
            out.append("## Rollback")
            out.append("")
            out.append("- Action: restored from backup")
            out.append(f"- rollback_compile_ok: **{rb_ok}**")
            out.append(f"- rollback_compile_detail: `{rb_msg}`")
            out.append("")
        except Exception as e:
            out.append("## Rollback")
            out.append("")
            out.append(f"- Rollback FAILED: {type(e).__name__}: {e}")
            out.append("")

        _write_report(report_path, out)
        print(f"[{runner_id}] FAIL (compile/patch). Rolled back.")
        print(f"[{runner_id}] Report: {report_path}")
        return CODE_FAIL

    _write_report(report_path, out)
    print(f"[{runner_id}] OK: {note}")
    print(f"[{runner_id}] Report: {report_path}")
    return CODE_OK


if __name__ == "__main__":
    # Root = repo root (tools/..)
    root_dir = Path(__file__).resolve().parent.parent
    raise SystemExit(main(root_dir))
