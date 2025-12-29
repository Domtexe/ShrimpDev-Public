# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Tuple
import shutil
import py_compile
import re


RUNNER_ID = "R2836"


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
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
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


def find_line_index(lines: List[str], needle: str) -> int:
    for i, ln in enumerate(lines):
        if needle in ln:
            return i
    return -1


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

    lines = ui.read_text(encoding="utf-8", errors="replace").splitlines()

    marker = "R2836_TRACE_PUSH"
    if any(marker in ln for ln in lines):
        report.append("- Already instrumented (marker found)")
        write_report(repo, report)
        return 0

    # We will inject a tiny logger helper inside build_toolbar_right (indented by 4 spaces),
    # and instrument _set_btn_state and _update_push_states by adding trace calls.
    idx_build = find_line_index(lines, "def build_toolbar_right(")
    if idx_build < 0:
        report.append("ERROR: build_toolbar_right not found")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    # Insert helper shortly after build_toolbar_right header (after possible docstring start)
    insert_at = idx_build + 1
    helper = [
        "    # R2836_TRACE_PUSH",
        "    def _r2836_trace(msg: str) -> None:",
        "        try:",
        "            import os",
        "            from datetime import datetime",
        "            _root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))",
        "            _fp = os.path.join(_root, 'Reports', 'trace_push_buttons.log')",
        "            os.makedirs(os.path.dirname(_fp), exist_ok=True)",
        "            with open(_fp, 'a', encoding='utf-8', errors='replace') as f:",
        "                f.write(f\"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\\n\")",
        "        except Exception:",
        "            pass",
        "",
    ]

    # Avoid inserting inside a docstring block: we insert after the first non-empty line that isn't a triple quote start.
    # Simple heuristic: if the next non-empty line starts with '"""' or "'''", skip until closing triple quotes.
    j = insert_at
    while j < len(lines) and lines[j].strip() == "":
        j += 1
    if j < len(lines) and (lines[j].lstrip().startswith('"""') or lines[j].lstrip().startswith("'''")):
        quote = '"""' if lines[j].lstrip().startswith('"""') else "'''"
        j += 1
        while j < len(lines):
            if quote in lines[j]:
                j += 1
                break
            j += 1
        insert_at = j
    else:
        insert_at = insert_at

    lines = lines[:insert_at] + helper + lines[insert_at:]

    # Instrument _set_btn_state: find its def line within build_toolbar_right
    # We'll add a trace as first statement inside function body.
    pat_set = re.compile(r"^\s+def\s+_set_btn_state\s*\(")
    set_def_idx = -1
    for i, ln in enumerate(lines):
        if pat_set.search(ln):
            set_def_idx = i
            break
    if set_def_idx < 0:
        report.append("ERROR: _set_btn_state not found")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    # Insert after def line (next line)
    indent = " " * (len(lines[set_def_idx]) - len(lines[set_def_idx].lstrip()) + 4)
    trace_line = indent + "_r2836_trace(f\"set_btn_state name={name} enabled={enabled} busy={busy}\")"
    lines.insert(set_def_idx + 1, trace_line)

    # Instrument _update_push_states: add trace at start, and trace roots
    pat_upd = re.compile(r"^\s+def\s+_update_push_states\s*\(")
    upd_def_idx = -1
    for i, ln in enumerate(lines):
        if pat_upd.search(ln):
            upd_def_idx = i
            break
    if upd_def_idx < 0:
        report.append("ERROR: _update_push_states not found")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    indent2 = " " * (len(lines[upd_def_idx]) - len(lines[upd_def_idx].lstrip()) + 4)
    lines.insert(upd_def_idx + 1, indent2 + "_r2836_trace('update_push_states enter')")
    # Also try to trace resolved roots by inserting after lines that assign private_root/public_root
    for i in range(upd_def_idx + 1, min(len(lines), upd_def_idx + 200)):
        if "private_root" in lines[i] and "=" in lines[i] and "_resolve_repo_path" in lines[i]:
            lines.insert(i + 1, indent2 + "_r2836_trace(f\"private_root={private_root}\")")
            break
    for i in range(upd_def_idx + 1, min(len(lines), upd_def_idx + 220)):
        if "public_root" in lines[i] and "=" in lines[i] and "_resolve_repo_path" in lines[i]:
            lines.insert(i + 1, indent2 + "_r2836_trace(f\"public_root={public_root}\")")
            break

    ui.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")

    # Compile check
    try:
        py_compile.compile(str(ui), doraise=True)
        report.append("OK: py_compile passed")
    except Exception as exc:
        report.append(f"COMPILE FAIL: {exc}")
        restore(bak, ui)
        write_report(repo, report)
        return 11

    report.append("SUCCESS: Instrumentation installed")
    report.append("- Log file: Reports/trace_push_buttons.log")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
