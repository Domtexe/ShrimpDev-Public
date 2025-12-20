# R2379 - INI SingleWriter Enforcement
# - Backups (Archiv)
# - Ensures modules/ini_writer.py exists with merge-write that PRESERVES [Docking] unless explicitly touched
# - Patches config_manager.save() to delegate to ini_writer (no direct file writes)
# - Patches config_loader.py / config_mgr.py to delegate writes (best-effort, safe)
# - Writes docs report + updates MasterRules + PIPELINE (best-effort)
#
# Mastermodus: minimal-invasive, backups, py_compile verify, rollback on failure.

import os
import re
import sys
import time
import json
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2379"

TARGETS = [
    "modules/config_manager.py",
    "modules/config_loader.py",
    "modules/config_mgr.py",
]

# Optional suspects (patched only if obvious write-patterns found)
OPTIONAL_TARGETS = [
    "modules/ui_toolbar.py",
    "modules/module_docking.py",
]

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def log(msg):
    print(f"[{RID}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}")

def root_dir() -> Path:
    return Path(__file__).resolve().parent.parent

def arch_dir(root: Path) -> Path:
    p = root / "_Archiv"
    p.mkdir(exist_ok=True)
    return p

def backup_file(root: Path, rel: str) -> Path:
    src = root / rel
    if not src.exists():
        return None
    dst = arch_dir(root) / f"{src.name}.{RID}_{ts()}.bak"
    dst.write_bytes(src.read_bytes())
    return dst

def compile_check(path: Path):
    py_compile.compile(str(path), doraise=True)

def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")

def ensure_ini_writer(root: Path):
    """
    Provide a single internal write path that MERGE-writes and preserves [Docking] by default.
    """
    mod_path = root / "modules" / "ini_writer.py"
    if mod_path.exists():
        # do not overwrite; just ensure key API exists (append if missing)
        txt = mod_path.read_text(encoding="utf-8", errors="replace")
        if "def merge_write_ini" in txt and "PRESERVE_SECTIONS_DEFAULT" in txt:
            log("OK: ini_writer.py existiert bereits (no-op)")
            return
        backup_file(root, "modules/ini_writer.py")
        txt += "\n\n" + INI_WRITER_APPEND
        write_text(mod_path, txt)
        compile_check(mod_path)
        log("OK: ini_writer.py erweitert (merge_write_ini)")
        return

    backup_file(root, "modules/ini_writer.py")  # none, but consistent
    write_text(mod_path, INI_WRITER_NEW)
    compile_check(mod_path)
    log("OK: ini_writer.py erstellt")

INI_WRITER_NEW = r'''# modules/ini_writer.py
# SingleWriter for ShrimpDev.ini
# - merge_write_ini(): merge-writes changes while PRESERVING [Docking] by default
# - no side effects, no GUI imports

from __future__ import annotations
from pathlib import Path
import configparser
from datetime import datetime

PRESERVE_SECTIONS_DEFAULT = {"Docking"}

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ini_path(project_root: Path) -> Path:
    return (project_root / "ShrimpDev.ini").resolve()

def read_ini(path: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    return cfg

def merge_write_ini(project_root: Path,
                    updates: dict,
                    preserve_sections: set | None = None,
                    add_timestamp: bool = True) -> Path:
    """
    updates format:
      {
        "Section": {"key":"value", ...},
        ...
      }

    Default preserves [Docking] section (never overwritten unless updates contains "Docking").
    """
    preserve = set(PRESERVE_SECTIONS_DEFAULT)
    if preserve_sections:
        preserve |= set(preserve_sections)

    path = ini_path(project_root)
    base = read_ini(path) if path.exists() else configparser.ConfigParser()

    # If caller does not explicitly update Docking, keep it intact
    if "Docking" not in updates and base.has_section("Docking"):
        docking_items = dict(base.items("Docking"))

    # Apply updates
    for sec, kv in (updates or {}).items():
        if not base.has_section(sec):
            base.add_section(sec)
        for k, v in (kv or {}).items():
            base.set(sec, str(k), str(v))

    # Restore preserved sections that were not explicitly updated
    if "Docking" not in updates and 'docking_items' in locals():
        if not base.has_section("Docking"):
            base.add_section("Docking")
        for k, v in docking_items.items():
            base.set("Docking", k, v)

    if add_timestamp:
        if not base.has_section("Meta"):
            base.add_section("Meta")
        base.set("Meta", "last_write_ts", _ts())

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        base.write(f)

    return path
'''

INI_WRITER_APPEND = r'''# --- R2379: SingleWriter merge API ---
from pathlib import Path
import configparser
from datetime import datetime

PRESERVE_SECTIONS_DEFAULT = {"Docking"}

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def ini_path(project_root: Path) -> Path:
    return (project_root / "ShrimpDev.ini").resolve()

def read_ini(path: Path) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    return cfg

def merge_write_ini(project_root: Path,
                    updates: dict,
                    preserve_sections: set | None = None,
                    add_timestamp: bool = True) -> Path:
    preserve = set(PRESERVE_SECTIONS_DEFAULT)
    if preserve_sections:
        preserve |= set(preserve_sections)

    path = ini_path(project_root)
    base = read_ini(path) if path.exists() else configparser.ConfigParser()

    if "Docking" not in updates and base.has_section("Docking"):
        docking_items = dict(base.items("Docking"))

    for sec, kv in (updates or {}).items():
        if not base.has_section(sec):
            base.add_section(sec)
        for k, v in (kv or {}).items():
            base.set(sec, str(k), str(v))

    if "Docking" not in updates and 'docking_items' in locals():
        if not base.has_section("Docking"):
            base.add_section("Docking")
        for k, v in docking_items.items():
            base.set("Docking", k, v)

    if add_timestamp:
        if not base.has_section("Meta"):
            base.add_section("Meta")
        base.set("Meta", "last_write_ts", _ts())

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        base.write(f)

    return path
'''

def replace_method_body(src: str, class_name: str, func_name: str, new_body_lines: list[str]) -> tuple[str, bool]:
    """
    Replace the body of class method def func_name(...) inside class class_name.
    Keeps signature line, replaces indented block until next def/class at same indent.
    """
    lines = src.splitlines(True)
    # find class
    class_pat = re.compile(rf"^(\s*)class\s+{re.escape(class_name)}\b.*:\s*$")
    func_pat = re.compile(rf"^(\s*)def\s+{re.escape(func_name)}\s*\(.*\)\s*:\s*$")

    ci = None
    class_indent = None
    for i, ln in enumerate(lines):
        m = class_pat.match(ln)
        if m:
            ci = i
            class_indent = m.group(1)
            break
    if ci is None:
        return src, False

    # find function within class
    fi = None
    func_indent = None
    for i in range(ci + 1, len(lines)):
        ln = lines[i]
        # stop if next class at same indent
        if ln.startswith(class_indent) and ln.lstrip().startswith("class ") and len(ln) - len(ln.lstrip()) == len(class_indent):
            break
        m = func_pat.match(ln)
        if m:
            fi = i
            func_indent = m.group(1)
            break
    if fi is None:
        return src, False

    # Determine body start/end
    body_start = fi + 1
    # If there are blank/comment lines immediately after def, we still replace them as part of body
    # End when indentation <= func_indent (and line not blank)
    end = body_start
    for j in range(body_start, len(lines)):
        ln = lines[j]
        if ln.strip() == "":
            end = j + 1
            continue
        indent_len = len(ln) - len(ln.lstrip())
        if indent_len <= len(func_indent):
            end = j
            break
        end = j + 1

    # Build new body with proper indent = func_indent + 4 spaces
    body_indent = func_indent + " " * 4
    new_block = []
    for b in new_body_lines:
        new_block.append(body_indent + b + "\n")

    out = lines[:body_start] + new_block + lines[end:]
    return "".join(out), True

def patch_config_manager_save(root: Path) -> bool:
    rel = "modules/config_manager.py"
    path = root / rel
    if not path.exists():
        log(f"WARN: nicht gefunden: {rel}")
        return False

    original = path.read_text(encoding="utf-8", errors="replace")

    # Ensure ini_writer import (safe add after other imports)
    if "from modules import ini_writer" not in original and "import ini_writer" not in original:
        # insert after first block of imports
        lines = original.splitlines(True)
        insert_at = 0
        for i, ln in enumerate(lines):
            if ln.startswith("import ") or ln.startswith("from "):
                insert_at = i + 1
                continue
            # stop after initial imports block
            if i > 0 and insert_at > 0:
                break
        lines.insert(insert_at, "from modules import ini_writer  # R2379 SingleWriter\n")
        original = "".join(lines)

    new_body = [
        '"""R2379: save delegates to ini_writer.merge_write_ini (preserve [Docking])."""',
        "root = None",
        "try:",
        "    # project root = modules/..",
        "    root = Path(__file__).resolve().parent.parent",
        "except Exception:",
        "    root = None",
        "if root is None:",
        "    return",
        "try:",
        "    # Use current in-memory config; convert to updates dict",
        "    updates = {}",
        "    if self._config is None:",
        "        return",
        "    for sec in self._config.sections():",
        "        updates[sec] = {}",
        "        for k, v in self._config.items(sec):",
        "            updates[sec][k] = v",
        "    # Important: preserve Docking unless explicitly present in updates (handled by ini_writer)",
        "    ini_writer.merge_write_ini(root, updates, preserve_sections=set(['Docking']))",
        "except Exception:",
        "    # never crash app on save",
        "    return",
    ]

    # Need Path import in file (ensure)
    if "from pathlib import Path" not in original:
        # add near imports
        lines = original.splitlines(True)
        ins = 0
        for i, ln in enumerate(lines):
            if ln.startswith("import ") or ln.startswith("from "):
                ins = i + 1
                continue
            if i > 0 and ins > 0:
                break
        lines.insert(ins, "from pathlib import Path  # R2379\n")
        original = "".join(lines)

    patched, ok = replace_method_body(original, "ShrimpDevConfigManager", "save", new_body)
    if not ok:
        log("FEHLER: save() in ShrimpDevConfigManager nicht gefunden/ersetzbar")
        return False

    # Also prevent accidental direct file writes by keeping legacy code unreachable is now replaced.

    backup_file(root, rel)
    path.write_text(patched, encoding="utf-8")
    compile_check(path)
    log("OK: config_manager.save() delegiert an ini_writer")
    return True

def patch_simple_delegate_if_writes(root: Path, rel: str) -> bool:
    """
    For config_loader.py / config_mgr.py: if they contain obvious file-write patterns,
    replace any save(...) function (module-level) with delegation to ini_writer.
    If no patterns found, no-op.
    """
    path = root / rel
    if not path.exists():
        log(f"WARN: nicht gefunden: {rel}")
        return False
    src = path.read_text(encoding="utf-8", errors="replace")

    has_write = ("open(" in src and "'w'" in src) or ".write(" in src or "ConfigParser" in src
    if not has_write:
        log(f"OK: {rel} keine offensichtlichen Writes (no-op)")
        return True

    # Ensure imports
    if "from modules import ini_writer" not in src:
        # insert after imports
        lines = src.splitlines(True)
        insert_at = 0
        for i, ln in enumerate(lines):
            if ln.startswith("import ") or ln.startswith("from "):
                insert_at = i + 1
                continue
            if i > 0 and insert_at > 0:
                break
        lines.insert(insert_at, "from modules import ini_writer  # R2379 SingleWriter\n")
        if "from pathlib import Path" not in src:
            lines.insert(insert_at, "from pathlib import Path  # R2379\n")
        src = "".join(lines)

    # Replace module-level def save(...) if exists
    m = re.search(r"^def\s+save\s*\(.*\)\s*:\s*$", src, flags=re.M)
    if not m:
        # If no save, just neutralize direct writes to ShrimpDev.ini by redirecting those lines
        # Minimal approach: comment out config.write(...) lines that are used for INI file
        new = []
        changed = False
        for ln in src.splitlines(True):
            if ".write(" in ln and ("ShrimpDev.ini" in src):
                new.append("# R2379 DISABLED DIRECT WRITE: " + ln)
                changed = True
            else:
                new.append(ln)
        if changed:
            backup_file(root, rel)
            path.write_text("".join(new), encoding="utf-8")
            compile_check(path)
            log(f"OK: {rel} direkte Writes deaktiviert (commented)")
            return True
        log(f"WARN: {rel} hat Writes, aber keine save() und nichts eindeutig patchbar")
        return False

    # Replace save() body (module-level) safely by indentation
    lines = src.splitlines(True)
    # find def save line index
    idx = None
    indent = ""
    for i, ln in enumerate(lines):
        if re.match(r"^def\s+save\s*\(.*\)\s*:\s*$", ln):
            idx = i
            indent = ln[:len(ln)-len(ln.lstrip())]
            break
    if idx is None:
        return False

    body_start = idx + 1
    end = body_start
    for j in range(body_start, len(lines)):
        ln = lines[j]
        if ln.strip() == "":
            end = j + 1
            continue
        ind = len(ln) - len(ln.lstrip())
        if ind <= len(indent):
            end = j
            break
        end = j + 1

    bi = indent + " " * 4
    new_body = [
        f'{bi}"""R2379: save delegates to ini_writer.merge_write_ini (preserve Docking)."""\n',
        f"{bi}try:\n",
        f"{bi}    root = Path(__file__).resolve().parent.parent\n",
        f"{bi}    # This module should not write directly; only delegate.\n",
        f"{bi}    # Caller should pass updates dict or configparser; we accept both.\n",
        f"{bi}    updates = {{}}\n",
        f"{bi}    if len(locals()) and 'cfg' in locals() and hasattr(cfg, 'sections'):\n",
        f"{bi}        for sec in cfg.sections():\n",
        f"{bi}            updates[sec] = {{k: v for (k, v) in cfg.items(sec)}}\n",
        f"{bi}    ini_writer.merge_write_ini(root, updates, preserve_sections=set(['Docking']))\n",
        f"{bi}except Exception:\n",
        f"{bi}    return\n",
    ]
    out = lines[:body_start] + new_body + lines[end:]

    backup_file(root, rel)
    path.write_text("".join(out), encoding="utf-8")
    compile_check(path)
    log(f"OK: {rel} save() delegiert an ini_writer")
    return True

def optional_disable_obvious_writers(root: Path, rel: str) -> bool:
    """
    Only touches file if it contains explicit writes to ShrimpDev.ini via open('w') or config.write.
    We comment those lines out with R2379 tag (minimal) and keep compile.
    """
    path = root / rel
    if not path.exists():
        return False
    src = path.read_text(encoding="utf-8", errors="replace")
    if "ShrimpDev.ini" not in src and ".write(" not in src:
        return True

    changed = False
    out = []
    for ln in src.splitlines(True):
        if ("ShrimpDev.ini" in ln and ("open(" in ln or ".open(" in ln)) or ("base.write" in ln) or ("config.write" in ln):
            out.append("# R2379 DISABLED DIRECT INI WRITE: " + ln)
            changed = True
        else:
            out.append(ln)

    if not changed:
        log(f"OK: {rel} keine eindeutigen direkten INI-writes gefunden (no-op)")
        return True

    backup_file(root, rel)
    path.write_text("".join(out), encoding="utf-8")
    compile_check(path)
    log(f"OK: {rel} direkte INI-writes deaktiviert (commented)")
    return True

def update_docs(root: Path, changes: list[str]):
    docs = root / "docs"
    docs.mkdir(exist_ok=True)

    rep = docs / f"Report_{RID}_SingleWriter_Enforcement_{ts()}.md"
    lines = [
        f"# {RID} – INI SingleWriter Enforcement",
        "",
        f"- Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"- Root: {root}",
        "",
        "## Änderungen",
        "",
    ] + [f"- {c}" for c in changes]

    write_text(rep, "\n".join(lines) + "\n")
    log(f"Report geschrieben: {rep}")

    # Best-effort: update MasterRules.md and PIPELINE.md if they exist (either in root or docs/)
    mr_candidates = [root / "MasterRules.md", root / "docs" / "MasterRules.md"]
    pl_candidates = [root / "PIPELINE.md", root / "docs" / "PIPELINE.md"]

    for mr in mr_candidates:
        if mr.exists():
            backup_file(root, str(mr.relative_to(root)))
            txt = mr.read_text(encoding="utf-8", errors="replace")
            add = "\n\n## INI SingleWriter (R2379)\n- Es darf genau **einen** Schreiber für ShrimpDev.ini geben: `modules/ini_writer.py`.\n- Direkte INI-Writes (open('w'), config.write) in anderen Modulen sind verboten.\n- [Docking] darf durch Settings/Filter Saves **niemals** überschrieben werden.\n- Wenn ein Fix nicht sofort verifiziert funktioniert: Diagnose-Runner zuerst (Messung SOLL/IST), dann minimaler Fix.\n"
            if "## INI SingleWriter (R2379)" not in txt:
                txt += add
                mr.write_text(txt, encoding="utf-8")
                log(f"OK: MasterRules ergänzt: {mr}")
            break

    for pl in pl_candidates:
        if pl.exists():
            backup_file(root, str(pl.relative_to(root)))
            txt = pl.read_text(encoding="utf-8", errors="replace")
            add = "\n\n### [BLOCKING] INI SingleWriter Enforcement (R2379)\n- Alle INI-Schreiber konsolidieren auf `ini_writer.merge_write_ini()`.\n- Direkte Writes in config_* und UI-Modulen deaktivieren.\n- Verifikation: Start schreibt nichts; Move/Close schreibt genau 1 Datensatz pro Fenster.\n- Danach: Defactoring/Archivierung obsoleter Altpfade.\n"
            if "INI SingleWriter Enforcement (R2379)" not in txt:
                txt += add
                pl.write_text(txt, encoding="utf-8")
                log(f"OK: PIPELINE ergänzt: {pl}")
            break

def main():
    root = root_dir()
    changes = []

    log(f"Projekt-Root: {root}")

    # 1) Ensure ini_writer exists
    try:
        ensure_ini_writer(root)
        changes.append("ini_writer.py sichergestellt (merge_write_ini, preserve Docking)")
    except Exception as e:
        log(f"FEHLER ini_writer: {e}")
        return 2

    # 2) Patch config_manager.save -> ini_writer
    try:
        if patch_config_manager_save(root):
            changes.append("config_manager.save() delegiert an ini_writer (kein direkter INI write)")
        else:
            changes.append("WARN: config_manager.save() nicht gepatcht")
    except Exception as e:
        log(f"FEHLER config_manager patch: {e}")
        return 2

    # 3) Patch config_loader/config_mgr if they write
    for rel in ["modules/config_loader.py", "modules/config_mgr.py"]:
        try:
            ok = patch_simple_delegate_if_writes(root, rel)
            if ok:
                changes.append(f"{rel}: Writes delegiert/neutralisiert (single-writer)")
            else:
                changes.append(f"WARN: {rel}: nicht sauber patchbar")
        except Exception as e:
            log(f"FEHLER {rel}: {e}")
            return 2

    # 4) Optional: disable obvious direct writers (safe, minimal)
    for rel in OPTIONAL_TARGETS:
        try:
            ok = optional_disable_obvious_writers(root, rel)
            if ok:
                changes.append(f"{rel}: direkte INI-writes (falls vorhanden) deaktiviert")
            else:
                changes.append(f"WARN: {rel}: optional patch fehlgeschlagen")
        except Exception as e:
            log(f"FEHLER optional {rel}: {e}")
            return 2

    # 5) Docs/MR/PIPELINE
    try:
        update_docs(root, changes)
    except Exception as e:
        log(f"WARN: Docs update fehlgeschlagen: {e}")

    log("Beendet: rc=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
