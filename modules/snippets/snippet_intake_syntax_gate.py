"""
Einfaches Syntax-Gate als Snippet:
- Kann in main_gui.py oder Intake-Loader genutzt werden, um vor dem Import zu prüfen.
- Keine harte Integration erzwungen (Runner 1244 tut bereits die Reparatur).
"""
from __future__ import annotations
from pathlib import Path
import ast

def intake_syntax_ok(project_root: Path | None = None) -> bool:
    try:
        root = Path(__file__).resolve().parents[2] if project_root is None else project_root
        p = root / "modules" / "module_code_intake.py"
        src = p.read_text(encoding="utf-8", errors="replace")
        ast.parse(src)
        return True
    except Exception:
        return False
