# -*- coding: utf-8 -*-
"""
[R2386] Docking Close Semantics (minimal, robust):
- Patch modules/module_docking.py:
  1) Ensure DockManager.close(key) sets open=0 in [Docking] and removes the window from _wins
  2) Ensure WM_DELETE_WINDOW in undock_readonly triggers self.close(key) (not withdraw-only)

Backups -> _Archiv
Syntax check
Report -> docs/
"""

from __future__ import annotations
import ast
import shutil
import py_compile
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIV = ROOT / "_Archiv"
DOCS = ROOT / "docs"
TARGET = ROOT / "modules" / "module_docking.py"

def ts() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def backup(path: Path, rid: str) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    b = ARCHIV / f"{path.name}.{rid}_{ts()}.bak"
    shutil.copy2(path, b)
    return b

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8")

def main() -> int:
    rid = "R2386"
    DOCS.mkdir(parents=True, exist_ok=True)

    if not TARGET.exists():
        print(f"[{rid}] FEHLER: Datei nicht gefunden: {TARGET}")
        return 2

    src = read(TARGET)
    b = backup(TARGET, rid)
    print(f"[{rid}] Backup: {b}")

    tree = ast.parse(src, filename=str(TARGET))
    lines = src.splitlines(True)

    # Locate class DockManager
    dock_cls = None
    for n in tree.body:
        if isinstance(n, ast.ClassDef) and n.name == "DockManager":
            dock_cls = n
            break
    if dock_cls is None:
        print(f"[{rid}] FEHLER: class DockManager nicht gefunden.")
        return 2

    # Locate methods
    close_fn = None
    undock_fn = None
    for n in dock_cls.body:
        if isinstance(n, ast.FunctionDef) and n.name == "close":
            close_fn = n
        if isinstance(n, ast.FunctionDef) and n.name == "undock_readonly":
            undock_fn = n

    if close_fn is None:
        print(f"[{rid}] FEHLER: DockManager.close() nicht gefunden.")
        return 2
    if undock_fn is None:
        print(f"[{rid}] FEHLER: DockManager.undock_readonly() nicht gefunden.")
        return 2

    # Helper: get indent of a given line (1-based)
    def indent_of(line_no: int) -> str:
        s = lines[line_no - 1]
        return s[:len(s) - len(s.lstrip(" "))]

    changed = False

    # --- Patch 1: Replace body of close() by minimal robust close semantics ---
    # We keep signature and doc, but replace body lines with our safe logic.
    close_def_line = close_fn.lineno
    close_body_start = close_fn.body[0].lineno if close_fn.body else close_def_line + 1

    # find end of close() by next def in class at same indent
    class_indent = indent_of(close_def_line)
    close_indent = indent_of(close_def_line)
    # scan forward from close_def_line to find next "def " at same indent
    end_line = len(lines) + 1
    for i in range(close_def_line, len(lines)):
        if i + 1 <= close_def_line:
            continue
        ln = lines[i]
        if not ln.strip():
            continue
        if ln.startswith(close_indent) and ln.lstrip().startswith("def "):
            end_line = i + 1
            break

    body_indent = close_indent + "    "
    new_close_body = (
        f"{body_indent}# R2386: close => open=0 persisted + remove from _wins (best-effort)\n"
        f"{body_indent}w = None\n"
        f"{body_indent}try:\n"
        f"{body_indent}    w = self._wins.get(key)\n"
        f"{body_indent}except Exception:\n"
        f"{body_indent}    w = None\n\n"
        f"{body_indent}# Capture last geometry if available\n"
        f"{body_indent}geo = \"\"\n"
        f"{body_indent}try:\n"
        f"{body_indent}    if w is not None:\n"
        f"{body_indent}        geo = str(w.wm_geometry())\n"
        f"{body_indent}except Exception:\n"
        f"{body_indent}    geo = \"\"\n\n"
        f"{body_indent}# Actually destroy/withdraw window and remove tracking\n"
        f"{body_indent}try:\n"
        f"{body_indent}    if w is not None:\n"
        f"{body_indent}        try:\n"
        f"{body_indent}            w.destroy()\n"
        f"{body_indent}        except Exception:\n"
        f"{body_indent}            try:\n"
        f"{body_indent}                w.withdraw()\n"
        f"{body_indent}            except Exception:\n"
        f"{body_indent}                pass\n"
        f"{body_indent}except Exception:\n"
        f"{body_indent}    pass\n\n"
        f"{body_indent}try:\n"
        f"{body_indent}    if hasattr(self, \"_wins\") and isinstance(self._wins, dict):\n"
        f"{body_indent}        self._wins.pop(key, None)\n"
        f"{body_indent}except Exception:\n"
        f"{body_indent}    pass\n\n"
        f"{body_indent}# Persist open=0 into [Docking]\n"
        f"{body_indent}try:\n"
        f"{body_indent}    from modules import config_loader\n"
        f"{body_indent}    cfg = config_loader.load()\n"
        f"{body_indent}    sec = \"Docking\"\n"
        f"{body_indent}    if not cfg.has_section(sec):\n"
        f"{body_indent}        cfg.add_section(sec)\n"
        f"{body_indent}    cfg.set(sec, key + \".open\", \"0\")\n"
        f"{body_indent}    cfg.set(sec, key + \".docked\", \"0\")\n"
        f"{body_indent}    if geo:\n"
        f"{body_indent}        cfg.set(sec, key + \".geometry\", geo)\n"
        f"{body_indent}    config_loader.save(cfg)\n"
        f"{body_indent}except Exception:\n"
        f"{body_indent}    pass\n"
    )

    # Replace close body lines (close_body_start..end_line-1)
    start0 = close_body_start - 1
    end0 = end_line - 1
    new_lines = lines[:start0] + [new_close_body] + lines[end0:]
    new_src = "".join(new_lines)

    if "R2386: close => open=0 persisted" not in src:
        src = new_src
        lines = src.splitlines(True)
        changed = True

    # --- Patch 2: In undock_readonly, ensure WM_DELETE_WINDOW calls self.close(key) ---
    # We do a text-level anchor replacement for the protocol assignment:
    # replace any "w.protocol('WM_DELETE_WINDOW', _on_close)" with "w.protocol(..., lambda: self.close(key))"
    if "lambda: self.close(key)" not in src:
        src2 = src.replace(
            "w.protocol('WM_DELETE_WINDOW', _on_close)",
            "w.protocol('WM_DELETE_WINDOW', lambda: self.close(key))"
        ).replace(
            'w.protocol("WM_DELETE_WINDOW", _on_close)',
            'w.protocol("WM_DELETE_WINDOW", lambda: self.close(key))'
        )
        if src2 != src:
            src = src2
            changed = True

    if not changed:
        print(f"[{rid}] OK: bereits gepatcht (no-op)")
        return 0

    write(TARGET, src)

    try:
        py_compile.compile(str(TARGET), doraise=True)
    except Exception as e:
        shutil.copy2(b, TARGET)
        print(f"[{rid}] COMPILE FAIL -> rollback: {e!r}")
        return 3

    report = DOCS / f"Report_{rid}_Docking_CloseOpenFlag_{ts()}.md"
    report.write_text(
        "\n".join([
            f"# Report {rid} – Docking close semantics",
            "",
            f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- Target: `{TARGET}`",
            f"- Backup: `{b}`",
            "",
            "## Changes",
            "- DockManager.close(key): sets [Docking] key.open=0 and removes window from _wins",
            "- undock_readonly: WM_DELETE_WINDOW routes to self.close(key)",
            "",
        ]),
        encoding="utf-8"
    )
    print(f"[{rid}] OK: Patch angewendet. Report: {report}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
