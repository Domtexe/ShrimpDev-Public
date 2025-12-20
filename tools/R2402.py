from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import py_compile
import ast

RID = "R2402"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIV = ROOT / "_Archiv"

TARGETS = [
    ROOT / "modules" / "config_loader.py",
    ROOT / "modules" / "config_mgr.py",
]

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def backup_file(p: Path) -> Path:
    ARCHIV.mkdir(parents=True, exist_ok=True)
    bak = ARCHIV / f"{p.name}.{RID}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    bak.write_bytes(p.read_bytes())
    return bak

def _find_top_level_save_block(text: str) -> tuple[int, int] | None:
    """
    Liefert (start_line, end_line) der top-level Funktion def save(...)
    über AST lineno/end_lineno, damit wir nur den Block austauschen.
    """
    mod = ast.parse(text)
    for node in mod.body:
        if isinstance(node, ast.FunctionDef) and node.name == "save":
            if getattr(node, "lineno", None) and getattr(node, "end_lineno", None):
                return (int(node.lineno), int(node.end_lineno))
    return None

def _indent_of_line(line: str) -> str:
    return line[: len(line) - len(line.lstrip(" \t"))]

def patch_save_delegate(text: str, file_rel: str) -> tuple[str, str]:
    """
    Ersetzt NUR den Body der top-level def save(cfg): in config_loader/config_mgr
    durch Delegation an config_manager.get_manager().save()
    """
    rng = _find_top_level_save_block(text)
    if not rng:
        return text, f"WARN: no top-level def save(...) found in {file_rel} (no-op)"

    start, end = rng
    lines = text.splitlines()

    def_line = lines[start - 1]
    base_indent = _indent_of_line(def_line)
    body_indent = base_indent + "    "

    # Neuer Body: defensiv, niemals crashen, und cfg in mgr einklinken
    new_body = [
        f"{body_indent}# {RID}: SingleWriter delegation – DO NOT write INI directly here",
        f"{body_indent}try:",
        f"{body_indent}    from modules import config_manager as _cfgm  # type: ignore",
        f"{body_indent}    mgr = _cfgm.get_manager()",
        f"{body_indent}    # Bestehende cfg Instanz übernehmen (Kompatibilität zu bisherigen Call-Sites)",
        f"{body_indent}    try:",
        f"{body_indent}        mgr._config = cfg  # type: ignore[attr-defined]",
        f"{body_indent}    except Exception:",
        f"{body_indent}        pass",
        f"{body_indent}    mgr.save()",
        f"{body_indent}except Exception as _e:",
        f"{body_indent}    # Fallback: niemals GUI crashen (log best-effort)",
        f"{body_indent}    try:",
        f"{body_indent}        from modules.logic_actions import log_debug as _log_debug  # type: ignore",
        f"{body_indent}        _log_debug('[{RID}] save delegation failed: ' + repr(_e))",
        f"{body_indent}    except Exception:",
        f"{body_indent}        pass",
    ]

    # Block ersetzen: def-line bleibt, darunter ersetzen wir bis end
    # Wir lassen die ursprüngliche def-line stehen, ersetzen aber alles bis end.
    patched = []
    patched.extend(lines[:start])          # inkl def-line
    patched.extend(new_body)              # neuer Body
    patched.extend(lines[end:])           # Rest nach Funktionsblock

    # Newline am Ende erhalten
    out = "\n".join(patched)
    if text.endswith("\n"):
        out += "\n"
    return out, f"OK: patched def save(...) block lines {start}-{end}"

def main() -> int:
    report = []
    report.append(f"# Report {RID} – Delegate save() to ConfigManager (SingleWriter path)")
    report.append("")
    report.append(f"- Timestamp: {ts()}")
    report.append(f"- Root: `{ROOT}`")
    report.append("")

    changed = []
    backups = []

    for p in TARGETS:
        rel = str(p.relative_to(ROOT))
        if not p.exists():
            report.append(f"## `{rel}`")
            report.append("- MISSING (skip)")
            report.append("")
            continue

        original = p.read_text(encoding="utf-8", errors="replace")
        before_sha = sha256(p)

        patched, status = patch_save_delegate(original, rel)
        report.append(f"## `{rel}`")
        report.append(f"- sha256 before: `{before_sha}`")
        report.append(f"- action: {status}")

        if patched != original:
            bak = backup_file(p)
            p.write_text(patched, encoding="utf-8")
            after_sha = sha256(p)
            backups.append(str(bak))
            changed.append(rel)
            report.append(f"- backup: `{bak}`")
            report.append(f"- sha256 after: `{after_sha}`")
        else:
            report.append("- no change")

        report.append("")

    # Compile gate
    report.append("## Compile Gate")
    ok = True
    for p in TARGETS:
        if p.exists():
            try:
                py_compile.compile(str(p), doraise=True)
                report.append(f"- OK: {p}")
            except Exception as e:
                ok = False
                report.append(f"- FAIL: {p} :: {e!r}")

    out = DOCS / f"Report_{RID}_SingleWriter_Delegation_{stamp()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"[{RID}] OK: Report {out}")
    if not ok:
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
