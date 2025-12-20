# patchlib_guard.py  - schlankes Guard/AST-Toolkit (Py3.12)
from __future__ import annotations
import ast, io, os, re, shutil, sys, tempfile, tokenize
from dataclasses import dataclass
from typing import Optional, Tuple

ARCHIV_DIRNAME = "_Archiv"

@dataclass
class FileCtx:
    path: str
    original: str
    modified: str
    backup_path: Optional[str] = None

# ---------- IO / Backup ----------
def load_file(path: str) -> FileCtx:
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    return FileCtx(path=path, original=src, modified=src)

def ensure_archiv(root: str) -> str:
    ap = os.path.join(root, ARCHIV_DIRNAME)
    os.makedirs(ap, exist_ok=True)
    return ap

def backup(ctx: FileCtx) -> str:
    root = os.path.dirname(ctx.path)
    ap = ensure_archiv(root)
    base = os.path.basename(ctx.path)
    bak = os.path.join(ap, f"{base}.{int(__import__('time').time())}.bak")
    with open(bak, "w", encoding="utf-8") as f:
        f.write(ctx.original)
    ctx.backup_path = bak
    return bak

def commit(ctx: FileCtx) -> None:
    with open(ctx.path, "w", encoding="utf-8", newline="") as f:
        f.write(ctx.modified)

def rollback(ctx: FileCtx) -> None:
    if ctx.backup_path and os.path.exists(ctx.backup_path):
        shutil.copy2(ctx.backup_path, ctx.path)

# ---------- Gates ----------
def syntax_ok(src: str, file_hint: str="tmp") -> Tuple[bool, Optional[str]]:
    try:
        compile(src, file_hint, "exec")
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} (line {e.lineno})"

def future_at_top(src: str) -> bool:
    """__future__-Imports müssen ganz oben vor normalen Imports/Code stehen."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return False
    body = tree.body
    seen_non_doc = False
    for i, node in enumerate(body):
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
            # Modul-Docstring -> ok
            continue
        seen_non_doc = True
        if isinstance(node, ast.ImportFrom) and node.module == "__future__":
            # ok, aber muss direkt am Anfang sein: es dürfen nur Docstring/weitere __future__ davor liegen
            # überprüfe, ob vor i etwas anderes als Docstring/__future__ liegt
            for j in range(i):
                n = body[j]
                if isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str):
                    continue
                if isinstance(n, ast.ImportFrom) and n.module == "__future__":
                    continue
                return False
            return True
        else:
            # erstes Nicht-Doc/Nicht-__future__ bevor __future__ auftaucht -> falsch
            # Wenn gar kein __future__ vorkommt, werten wir True (wir fügen keines hinzu).
            break
    # kein __future__ im Code -> formal ok
    return True

def ensure_import(src: str, import_line: str) -> str:
    """fügt eine Import-Zeile hinzu, wenn sie fehlt; nach bestehenden Imports."""
    if re.search(rf"^\s*{re.escape(import_line)}\s*$", src, re.M):
        return src
    # Einfügeposition: nach Block von future- und normalen Imports
    lines = src.splitlines()
    insert_idx = 0
    past_header = False
    for i, ln in enumerate(lines):
        if i == 0 and ln.startswith("#!"):
            insert_idx = 1
            continue
        if ln.strip().startswith(("from __future__ import",)):
            insert_idx = i + 1
            continue
        if ln.strip().startswith(("import ", "from ")):
            insert_idx = i + 1
            continue
        # erste nicht-Import-Zeile -> hier abbrechen
        break
    lines.insert(insert_idx, import_line)
    return "\n".join(lines) + ("\n" if src.endswith("\n") else "")

# ---------- AST: Funktionen prüfen/ersetzen ----------
def has_function(src: str, name: str) -> bool:
    try:
        t = ast.parse(src)
    except SyntaxError:
        return False
    for n in t.body:
        if isinstance(n, ast.FunctionDef) and n.name == name:
            return True
    return False

def upsert_function(src: str, func_src: str, name: str) -> str:
    """Ersetzt od. ergänzt eine Top-Level-Funktion idempotent (per AST)."""
    try:
        mod = ast.parse(src)
    except SyntaxError:
        return src
    found_idx = None
    for idx, n in enumerate(mod.body):
        if isinstance(n, ast.FunctionDef) and n.name == name:
            found_idx = idx
            break
    new_func = ast.parse(func_src).body[0]
    if found_idx is None:
        mod.body.insert(_after_last_import(mod.body), new_func)
    else:
        mod.body[found_idx] = new_func
    ast.fix_missing_locations(mod)
    try:
        new_src = ast.unparse(mod)
    except Exception:
        # Fallback, falls unparse fehlschlägt
        return src
    return new_src + ("\n" if not new_src.endswith("\n") else "")

def _after_last_import(nodes):
    last = 0
    for i, n in enumerate(nodes):
        if isinstance(n, (ast.Import, ast.ImportFrom)) or (
            isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)
        ):
            last = i + 1
        else:
            break
    return last

# ---------- Safe write pipeline ----------
def guarded_apply(path: str, transform) -> Tuple[bool, str]:
    """
    transform(ctx: FileCtx) -> None (soll ctx.modified setzen)
    Pipeline: Backup -> Transform -> Gates (future/syntax) -> Commit or Rollback
    """
    ctx = load_file(path)
    backup(ctx)
    try:
        transform(ctx)
        ok, msg = syntax_ok(ctx.modified, file_hint=path)
        if not ok:
            rollback(ctx)
            return False, f"Syntax-Gate 🔴: {msg}"
        if not future_at_top(ctx.modified):
            rollback(ctx)
            return False, "Future-Gate 🔴: from __future__ nicht korrekt positioniert."
        commit(ctx)
        return True, "Commit ✅"
    except Exception as e:
        rollback(ctx)
        return False, f"Exception 🔴: {e}"
