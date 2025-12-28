#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[R2866] PATCH (SAFE): Fix NameError frame_toolbar_right in ui_toolbar.build_toolbar_right

Symptom:
- Crash on startup:
  NameError: name 'frame_toolbar_right' is not defined (inside modules/ui_toolbar.py, build_toolbar_right)

Fix:
- Insert a small alias block at the top of build_toolbar_right() that resolves the first argument
  regardless of its parameter name (frame/parent/container/...) and binds it to frame_toolbar_right.

Safety:
- Backup file into _Archiv
- Patch is idempotent (marker)
- Compile check; rollback on failure
- Report written
"""

from __future__ import annotations

import os
import sys
import time
import traceback
from pathlib import Path


EXIT_OK = 0
EXIT_FAIL = 11


def _ts() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _write_report(report_path: Path, lines: list[str]) -> None:
    _ensure_dir(report_path.parent)
    report_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8", errors="replace")


def _backup_file(repo: Path, src: Path) -> Path:
    arch = repo / "_Archiv"
    _ensure_dir(arch)
    bak = arch / f"{src.name}.R2866_{_ts()}.bak"
    bak.write_bytes(src.read_bytes())
    return bak


def _py_compile(repo: Path, rel: str) -> tuple[bool, str]:
    import py_compile
    try:
        py_compile.compile(str(repo / rel), doraise=True)
        return True, "OK"
    except Exception as e:
        return False, f"{type(e).__name__}: {e}"


def _find_def_line(lines: list[str], def_name: str) -> int:
    target = f"def {def_name}("
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith(target) and (ln.startswith("def ") or ln.lstrip().startswith("def ")):
            return i
    return -1


def _find_docstring_end(lines: list[str], start_idx: int, indent: str) -> int:
    """
    If the first logical statement is a triple-quoted docstring, return the line index AFTER it.
    Otherwise return start_idx.
    """
    i = start_idx
    if i >= len(lines):
        return i

    s = lines[i].strip()
    if not (s.startswith('"""') or s.startswith("'''")):
        return i

    quote = s[:3]
    # Single-line docstring """x"""
    if s.count(quote) >= 2 and len(s) > 3:
        return i + 1

    # Multi-line docstring: seek closing
    i += 1
    while i < len(lines):
        if lines[i].strip().endswith(quote):
            return i + 1
        i += 1
    return start_idx  # fall back if malformed


def _apply_patch(ui_path: Path) -> tuple[bool, str]:
    marker = "# R2866: alias frame_toolbar_right"
    raw = ui_path.read_text(encoding="utf-8", errors="replace")
    lines = raw.splitlines()

    def_idx = _find_def_line(lines, "build_toolbar_right")
    if def_idx < 0:
        return False, "def build_toolbar_right(...) not found"

    # Determine body indent (assume next line defines indent; fallback to 4 spaces)
    body_indent = " " * 4
    if def_idx + 1 < len(lines):
        nxt = lines[def_idx + 1]
        # if there is an indented line, capture its leading whitespace
        if nxt.startswith((" ", "\t")):
            body_indent = nxt[: len(nxt) - len(nxt.lstrip())] or body_indent

    # Find insertion point: after possible docstring
    insert_at = def_idx + 1
    insert_at = _find_docstring_end(lines, insert_at, body_indent)

    # If marker already present anywhere in function vicinity, skip
    window_start = max(0, def_idx)
    window_end = min(len(lines), def_idx + 120)
    if any(marker in l for l in lines[window_start:window_end]):
        return True, "already patched"

    patch_block = [
        f"{body_indent}{marker}",
        f"{body_indent}_ftr = None",
        f"{body_indent}for _nm in ('frame_toolbar_right','frame','parent','container','master','root'):",
        f"{body_indent}    if _nm in locals():",
        f"{body_indent}        _ftr = locals().get(_nm)",
        f"{body_indent}        if _ftr is not None:",
        f"{body_indent}            break",
        f"{body_indent}if _ftr is not None:",
        f"{body_indent}    frame_toolbar_right = _ftr",
        f"{body_indent}del _ftr, _nm",
        f"{body_indent}",
    ]

    new_lines = lines[:insert_at] + patch_block + lines[insert_at:]
    ui_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8", errors="replace")
    return True, "patched"


def main(repo_root: Path) -> int:
    report: list[str] = []
    report.append(f"# Report R2866 ({_ts()})")
    report.append("")
    report.append("## Goal")
    report.append("Fix startup crash: NameError `frame_toolbar_right` in `modules/ui_toolbar.py` (`build_toolbar_right`).")
    report.append("")
    report.append("## Target")
    ui_rel = "modules/ui_toolbar.py"
    ui_path = repo_root / ui_rel
    report.append(f"- Repo: `{repo_root}`")
    report.append(f"- File: `{ui_path}`")
    report.append("")

    if not ui_path.exists():
        report.append("## ERROR")
        report.append(f"- File not found: `{ui_path}`")
        _write_report(repo_root / "Reports" / f"Report_R2866_{_ts()}.md", report)
        return EXIT_FAIL

    bak = _backup_file(repo_root, ui_path)
    report.append("## Backup")
    report.append(f"- `{bak}`")
    report.append("")

    try:
        ok, note = _apply_patch(ui_path)
        report.append("## Patch")
        report.append(f"- Result: `{ok}`")
        report.append(f"- Note: `{note}`")
        report.append("")
        if not ok:
            # restore
            ui_path.write_bytes(bak.read_bytes())
            report.append("## Rollback")
            report.append("- Patch failed -> restored from backup.")
            _write_report(repo_root / "Reports" / f"Report_R2866_{_ts()}.md", report)
            return EXIT_FAIL

        okc, msg = _py_compile(repo_root, ui_rel)
        report.append("## Compile Check")
        report.append(f"- `{ui_rel}`: **{okc}** ({msg})")
        report.append("")
        if not okc:
            ui_path.write_bytes(bak.read_bytes())
            report.append("## Rollback")
            report.append("- Compile failed -> restored from backup.")
            _write_report(repo_root / "Reports" / f"Report_R2866_{_ts()}.md", report)
            return EXIT_FAIL

        report.append("## Outcome")
        report.append("- Startup should no longer crash on missing `frame_toolbar_right` symbol.")
        report.append("")
        _write_report(repo_root / "Reports" / f"Report_R2866_{_ts()}.md", report)
        return EXIT_OK

    except Exception:
        # rollback
        try:
            ui_path.write_bytes(bak.read_bytes())
        except Exception:
            pass
        report.append("## EXCEPTION")
        report.append("```")
        report.append(traceback.format_exc().rstrip())
        report.append("```")
        report.append("")
        report.append("## Rollback")
        report.append("- Exception -> restored from backup (best-effort).")
        _write_report(repo_root / "Reports" / f"Report_R2866_{_ts()}.md", report)
        return EXIT_FAIL


if __name__ == "__main__":
    root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    raise SystemExit(main(root))
