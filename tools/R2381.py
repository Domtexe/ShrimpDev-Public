# -*- coding: utf-8 -*-
"""
[R2381] READ-ONLY Structure Scan: modules/config_manager.py
- Finds classes, methods, and likely INI write entrypoints
- Detects direct file writes (open/write), configparser.write(), pathlib writes, etc.
- Detects references to ShrimpDev.ini and ini_writer usage
- Produces markdown report under docs/
NO PATCHING. NO FILE MODIFICATION.
"""

from __future__ import annotations

import ast
import hashlib
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "modules" / "config_manager.py"
DOCS = ROOT / "docs"

WRITE_CALL_NAMES = {
    # file / pathlib
    "open", "write_text", "write_bytes",
    # configparser common
    "read", "read_file", "readfp", "read_string",
    "write",
    # json / yaml etc (just in case)
    "dump", "safe_dump",
}

SUSPICIOUS_ATTRS = {
    "write", "write_text", "write_bytes", "dump", "safe_dump",
}

INI_HINTS = [
    "ShrimpDev.ini", "shrimpdev.ini", ".ini",
]

def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def now_stamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def safe_read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def find_regex_lines(text: str, pattern: str) -> List[Tuple[int, str]]:
    out = []
    rx = re.compile(pattern)
    for i, line in enumerate(text.splitlines(), start=1):
        if rx.search(line):
            out.append((i, line.rstrip("\n")))
    return out

class ScanVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.classes: Dict[str, Dict[str, Any]] = {}
        self.functions: List[Dict[str, Any]] = []
        self.calls: List[Dict[str, Any]] = []
        self.strings: List[Dict[str, Any]] = []
        self.assigns: List[Dict[str, Any]] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        methods = []
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                methods.append({
                    "name": body_item.name,
                    "lineno": body_item.lineno,
                    "args": [a.arg for a in body_item.args.args],
                })
        self.classes[node.name] = {
            "lineno": node.lineno,
            "methods": methods,
        }
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        # module-level functions too
        self.functions.append({
            "name": node.name,
            "lineno": node.lineno,
            "args": [a.arg for a in node.args.args],
        })
        self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> Any:
        callee = self._callee_name(node.func)
        entry = {
            "lineno": getattr(node, "lineno", None),
            "callee": callee,
            "raw": ast.unparse(node) if hasattr(ast, "unparse") else "<call>",
        }
        if callee:
            self.calls.append(entry)
        self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> Any:
        if isinstance(node.value, str):
            v = node.value
            if any(h in v for h in INI_HINTS) or "ini_writer" in v:
                self.strings.append({"lineno": node.lineno, "value": v})
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign) -> Any:
        try:
            txt = ast.unparse(node) if hasattr(ast, "unparse") else None
        except Exception:
            txt = None
        self.assigns.append({
            "lineno": getattr(node, "lineno", None),
            "text": txt,
        })
        self.generic_visit(node)

    def _callee_name(self, func: ast.AST) -> str:
        # returns dotted-ish name
        if isinstance(func, ast.Name):
            return func.id
        if isinstance(func, ast.Attribute):
            base = self._callee_name(func.value)
            return f"{base}.{func.attr}" if base else func.attr
        return ""

def summarize_calls(calls: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    buckets: Dict[str, List[Dict[str, Any]]] = {
        "direct_open": [],
        "configparser_write": [],
        "pathlib_write": [],
        "ini_writer_usage": [],
        "other_suspicious": [],
    }
    for c in calls:
        callee = (c.get("callee") or "").lower()

        if callee == "open" or callee.endswith(".open"):
            buckets["direct_open"].append(c)
            continue

        if callee.endswith(".write") or callee == "write":
            buckets["configparser_write"].append(c)
            continue

        if callee.endswith(".write_text") or callee.endswith(".write_bytes"):
            buckets["pathlib_write"].append(c)
            continue

        if "ini_writer" in callee or callee.endswith("merge_write_ini") or callee.endswith("merge_write"):
            buckets["ini_writer_usage"].append(c)
            continue

        last = callee.split(".")[-1]
        if last in SUSPICIOUS_ATTRS or last in WRITE_CALL_NAMES:
            buckets["other_suspicious"].append(c)

    # trim huge lists but keep enough to be useful
    for k in list(buckets.keys()):
        buckets[k] = buckets[k][:80]
    return buckets

def main() -> int:
    if not TARGET.exists():
        print(f"[R2381] FEHLER: Datei nicht gefunden: {TARGET}")
        return 2

    DOCS.mkdir(parents=True, exist_ok=True)

    text = safe_read_text(TARGET)
    file_sha = sha256_file(TARGET)
    size = TARGET.stat().st_size

    parse_ok = True
    try:
        tree = ast.parse(text, filename=str(TARGET))
    except SyntaxError as e:
        parse_ok = False
        tree = None
        syn_err = f"{e.__class__.__name__}: {e.msg} (line {e.lineno}, col {e.offset})"
    except Exception as e:
        parse_ok = False
        tree = None
        syn_err = f"{e.__class__.__name__}: {e}"

    visitor = ScanVisitor()
    if parse_ok and tree is not None:
        visitor.visit(tree)

    # raw grep hints (works even if AST failed)
    grep_targets = {
        "INI path mentions": r"ShrimpDev\.ini|shrimpdev\.ini|\.ini",
        "configparser usage": r"\bconfigparser\b|\bConfigParser\b",
        "file write patterns": r"\bopen\s*\(|\.write_text\s*\(|\.write_bytes\s*\(|\.write\s*\(",
        "ini_writer mentions": r"\bini_writer\b|merge_write_ini|merge_write",
    }
    greps = {name: find_regex_lines(text, pat) for name, pat in grep_targets.items()}

    # identify likely "save" / "persist" / "flush" methods
    likely_entrypoints = []
    method_like = []
    if parse_ok:
        for cls, info in visitor.classes.items():
            for m in info["methods"]:
                n = m["name"].lower()
                if n in {"save", "persist", "write", "flush", "commit", "store", "sync"} or n.startswith("save_") or n.endswith("_save"):
                    method_like.append((cls, m["name"], m["lineno"], m["args"]))
        for fn in visitor.functions:
            n = fn["name"].lower()
            if n in {"save", "persist", "write", "flush", "commit", "store", "sync"} or n.startswith("save_") or n.endswith("_save"):
                likely_entrypoints.append(("__module__", fn["name"], fn["lineno"], fn["args"]))

    call_buckets = summarize_calls(visitor.calls) if parse_ok else {}

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = DOCS / f"Report_R2381_ConfigManager_Scan_{stamp}.md"

    lines: List[str] = []
    lines.append(f"# Report R2381 – config_manager.py Struktur-Scan (READ-ONLY)\n")
    lines.append(f"- Timestamp: {now_stamp()}\n")
    lines.append(f"- Target: `{TARGET}`\n")
    lines.append(f"- Size: {size} bytes\n")
    lines.append(f"- SHA256: `{file_sha}`\n")
    lines.append(f"- AST parse: {'OK' if parse_ok else 'FAILED'}\n")
    if not parse_ok:
        lines.append(f"- Parse error: `{syn_err}`\n")

    lines.append("\n## Klassen & Methoden\n")
    if parse_ok:
        if not visitor.classes:
            lines.append("_Keine Klassen gefunden._\n")
        else:
            for cls, info in sorted(visitor.classes.items(), key=lambda x: x[1]["lineno"]):
                lines.append(f"### {cls} (line {info['lineno']})\n")
                if not info["methods"]:
                    lines.append("_Keine Methoden._\n")
                else:
                    for m in sorted(info["methods"], key=lambda x: x["lineno"]):
                        lines.append(f"- `{m['name']}` (line {m['lineno']}), args={m['args']}\n")
                lines.append("")
    else:
        lines.append("_AST nicht verfügbar (Syntaxfehler) – nur Regex/Grep möglich._\n")

    lines.append("\n## Verdächtige Entry-Points (save/persist/write/...)\n")
    if parse_ok:
        if method_like:
            for cls, name, ln, args in sorted(method_like, key=lambda x: x[2]):
                lines.append(f"- `{cls}.{name}()` (line {ln}), args={args}\n")
        else:
            lines.append("_Keine typischen Save-Methodennamen gefunden._\n")

        if likely_entrypoints:
            lines.append("\n### Module-level\n")
            for _, name, ln, args in sorted(likely_entrypoints, key=lambda x: x[2]):
                lines.append(f"- `{name}()` (line {ln}), args={args}\n")
    else:
        lines.append("_Nicht verfügbar._\n")

    lines.append("\n## Call-Sites (Write/IO/ini_writer)\n")
    if parse_ok:
        for k, items in call_buckets.items():
            lines.append(f"### {k}\n")
            if not items:
                lines.append("_nichts gefunden._\n")
                continue
            for it in items:
                lines.append(f"- line {it.get('lineno')}: `{it.get('callee')}` → `{it.get('raw')}`\n")
            lines.append("")
    else:
        lines.append("_Nicht verfügbar._\n")

    lines.append("\n## Grep-Hits (funktioniert auch ohne AST)\n")
    for name, hits in greps.items():
        lines.append(f"### {name}\n")
        if not hits:
            lines.append("_keine Treffer._\n")
            continue
        for ln, ltxt in hits[:200]:
            lines.append(f"- line {ln}: `{ltxt}`\n")
        lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"[R2381] OK: Report geschrieben: {report}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
