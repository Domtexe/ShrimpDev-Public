# -*- coding: utf-8 -*-
"""
[R2382] Patch config_manager.py -> ShrimpDevConfigManager.save delegates to ini_writer (SingleWriter)

- Minimal patch: replace only the body of ShrimpDevConfigManager.save()
- Uses AST to locate exact method (no regex-fragile patching)
- Creates backup in _Archiv
- Syntax-checks the patched file
- Writes a report in docs/

Design choice:
- Exclude [Docking] from updates to avoid overwriting docking positions.
  ini_writer.merge_write_ini() already preserves Docking by default if not explicitly provided.
"""

from __future__ import annotations

import ast
import py_compile
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "modules" / "config_manager.py"
ARCHIV = ROOT / "_Archiv"
DOCS = ROOT / "docs"


def ts_compact() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")


def backup_file(src: Path, runner_id: str) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    b = ARCHIV / f"{src.name}.{runner_id}_{ts_compact()}.bak"
    shutil.copy2(src, b)
    return b


def find_save_span(src: str) -> tuple[int, int]:
    """
    Return (start_line_idx0, end_line_idx0_exclusive) for the body of:
      class ShrimpDevConfigManager: def save(self): <BODY>
    start is the first line AFTER the def line, end is the line BEFORE next def at same indent.
    """
    tree = ast.parse(src, filename=str(TARGET))

    cls_node = None
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == "ShrimpDevConfigManager":
            cls_node = n
            break
    if cls_node is None:
        raise RuntimeError("Class ShrimpDevConfigManager not found.")

    save_node = None
    for n in cls_node.body:
        if isinstance(n, ast.FunctionDef) and n.name == "save":
            save_node = n
            break
    if save_node is None:
        raise RuntimeError("Method ShrimpDevConfigManager.save not found.")

    # def line:
    def_line = save_node.lineno  # 1-based
    # body span:
    if not save_node.body:
        # empty save() -> insert after def line, until next def at same indent
        body_start = def_line + 1
    else:
        body_start = save_node.body[0].lineno

    # Determine end by scanning following class body items with same indentation in source
    lines = src.splitlines(True)  # keepends
    def_indent = len(lines[def_line - 1]) - len(lines[def_line - 1].lstrip(" "))

    # Find next "def " at same indent after def_line
    end_line = len(lines) + 1
    for i in range(def_line, len(lines)):  # i is 0-based index; corresponds to line i+1
        line = lines[i]
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(" "))
        if indent == def_indent and line.lstrip().startswith("def ") and (i + 1) > def_line:
            end_line = i + 1  # 1-based line of next def
            break

    # replace from body_start to end_line-1
    start0 = body_start - 1
    end0 = (end_line - 1) - 1 + 1  # convert inclusive->exclusive safely
    # simpler:
    end0 = end_line - 1  # 1-based last line of old body (exclusive uses end_line-1 as index)
    # But end0 should be 0-based exclusive:
    end0 = (end_line - 1)  # because slice uses 0-based; line N corresponds index N-1; exclusive is end_line-1
    return (start0, end0)


def build_new_body(def_indent: int) -> str:
    """
    Build the new save() body with indentation.
    """
    indent = " " * (def_indent + 4)

    body = f"""{indent}# SingleWriter delegation: write ONLY via modules/ini_writer.py
{indent}self.ensure_loaded(project_root=self._project_root if hasattr(self, "_project_root") else None)
{indent}cfg_path = self.get_config_path()
{indent}cfg = getattr(self, "_config", None)

{indent}# Nothing loaded -> nothing to save
{indent}if cfg is None:
{indent}    return

{indent}# Convert ConfigParser to nested dict, but never overwrite [Docking] here
{indent}updates = {{}}
{indent}for section in cfg.sections():
{indent}    if section.strip().lower() == "docking":
{indent}        continue
{indent}    updates[section] = dict(cfg.items(section))

{indent}# Write through single writer (supports both get_writer() and direct merge_write_ini)
{indent}try:
{indent}    from modules.ini_writer import get_writer
{indent}    w = get_writer()
{indent}    if hasattr(w, "merge_write_ini"):
{indent}        w.merge_write_ini(str(cfg_path), updates)
{indent}        return
{indent}except Exception:
{indent}    pass

{indent}from modules.ini_writer import merge_write_ini
{indent}merge_write_ini(str(cfg_path), updates)
{indent}return
"""
    return body


def main() -> int:
    runner_id = "R2382"
    DOCS.mkdir(parents=True, exist_ok=True)

    if not TARGET.exists():
        print(f"[{runner_id}] FEHLER: Datei nicht gefunden: {TARGET}")
        return 2

    src = read_text(TARGET)
    backup = backup_file(TARGET, runner_id)
    print(f"[{runner_id}] Backup: {backup}")

    # locate save() def indent
    lines = src.splitlines(True)
    # parse once to get def line and indent
    tree = ast.parse(src, filename=str(TARGET))
    cls_node = next((n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "ShrimpDevConfigManager"), None)
    if cls_node is None:
        print(f"[{runner_id}] FEHLER: ShrimpDevConfigManager nicht gefunden.")
        return 2
    save_node = next((n for n in cls_node.body if isinstance(n, ast.FunctionDef) and n.name == "save"), None)
    if save_node is None:
        print(f"[{runner_id}] FEHLER: save() nicht gefunden.")
        return 2

    def_line = save_node.lineno
    def_indent = len(lines[def_line - 1]) - len(lines[def_line - 1].lstrip(" "))

    start0, end0 = find_save_span(src)

    new_body = build_new_body(def_indent)

    # Ensure we don't leave old body hanging; replace slice
    new_lines = lines[:start0] + [new_body] + lines[end0:]
    new_src = "".join(new_lines)

    write_text(TARGET, new_src)

    # syntax check
    try:
        py_compile.compile(str(TARGET), doraise=True)
    except Exception as e:
        # rollback
        shutil.copy2(backup, TARGET)
        print(f"[{runner_id}] FEHLER: Syntax-Check fehlgeschlagen -> Rollback. ({e})")
        return 3

    # report
    stamp = ts_compact()
    report = DOCS / f"Report_R2382_SingleWriter_Delegation_{stamp}.md"
    report.write_text(
        "\n".join([
            f"# Report {runner_id} – SingleWriter Delegation config_manager.py",
            "",
            f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- Target: `{TARGET}`",
            f"- Backup: `{backup}`",
            f"- Patched: `ShrimpDevConfigManager.save()` delegates to ini_writer",
            f"- Note: `[Docking]` intentionally excluded from updates (preserved by ini_writer default).",
            "",
        ]),
        encoding="utf-8"
    )
    print(f"[{runner_id}] OK: Patch angewendet + Report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
