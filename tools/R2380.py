# R2380 - Fix R2379 fallout + safe SingleWriter patch
# - Restore last compilable backup if current file broken
# - Patch ONLY save entry points with indent-safe replacement
# - Per-file: backup -> patch -> compile -> rollback on failure
# - Updates docs report + best-effort PIPELINE/MasterRules

import re
import sys
import py_compile
from pathlib import Path
from datetime import datetime

RID = "R2380"

FILES = {
    "config_loader": "modules/config_loader.py",
    "config_mgr":    "modules/config_mgr.py",
    "config_manager":"modules/config_manager.py",
}

def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def log(msg):
    print(f"[{RID}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {msg}")

def root_dir() -> Path:
    return Path(__file__).resolve().parent.parent

def archiv_dir(root: Path) -> Path:
    p = root / "_Archiv"
    p.mkdir(exist_ok=True)
    return p

def backup_file(root: Path, rel: str) -> Path:
    src = root / rel
    if not src.exists():
        return None
    dst = archiv_dir(root) / f"{src.name}.{RID}_{ts()}.bak"
    dst.write_bytes(src.read_bytes())
    return dst

def compile_ok(path: Path) -> bool:
    try:
        py_compile.compile(str(path), doraise=True)
        return True
    except Exception as e:
        log(f"COMPILE FAIL: {path} | {e.__class__.__name__}: {e}")
        return False

def find_latest_compilable_backup(root: Path, filename: str) -> Path | None:
    arch = archiv_dir(root)
    cands = sorted(arch.glob(f"{filename}.*.bak"), key=lambda p: p.stat().st_mtime, reverse=True)
    for bak in cands:
        tmp = arch / f"_tmp_{RID}_{filename}_{ts()}.py"
        try:
            tmp.write_bytes(bak.read_bytes())
            py_compile.compile(str(tmp), doraise=True)
            return bak
        except Exception:
            continue
        finally:
            try:
                tmp.unlink(missing_ok=True)
            except Exception:
                pass
    return None

def restore_backup_to(root: Path, rel: str, bak: Path) -> bool:
    dst = root / rel
    dst.write_bytes(bak.read_bytes())
    return True

def ensure_import_after_future(src: str, import_line: str) -> str:
    if import_line.strip() in src:
        return src
    lines = src.splitlines(True)
    insert_at = 0
    # keep __future__ at top
    for i, ln in enumerate(lines[:50]):
        if ln.startswith("from __future__ import"):
            insert_at = i + 1
            # continue scanning in case multiple __future__ lines
    # then after initial imports block
    if insert_at == 0:
        for i, ln in enumerate(lines[:80]):
            if ln.startswith("import ") or ln.startswith("from "):
                insert_at = i + 1
            elif i > 0 and insert_at > 0:
                break
    lines.insert(insert_at, import_line if import_line.endswith("\n") else import_line + "\n")
    return "".join(lines)

def replace_module_func_body(src: str, func_name: str, new_body_lines: list[str]) -> tuple[str, bool]:
    lines = src.splitlines(True)
    pat = re.compile(rf"^(\s*)def\s+{re.escape(func_name)}\s*\(.*\)\s*:\s*$")
    fi = None
    indent = ""
    for i, ln in enumerate(lines):
        m = pat.match(ln)
        if m:
            fi = i
            indent = m.group(1)
            break
    if fi is None:
        return src, False

    body_start = fi + 1
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
    new_block = []
    for b in new_body_lines:
        new_block.append(bi + b + "\n")

    out = lines[:body_start] + new_block + lines[end:]
    return "".join(out), True

def replace_class_method_body(src: str, class_name: str, func_name: str, new_body_lines: list[str]) -> tuple[str, bool]:
    lines = src.splitlines(True)
    class_pat = re.compile(rf"^(\s*)class\s+{re.escape(class_name)}\b.*:\s*$")
    func_pat = re.compile(rf"^(\s*)def\s+{re.escape(func_name)}\s*\(.*\)\s*:\s*$")

    ci = None
    class_indent = ""
    for i, ln in enumerate(lines):
        m = class_pat.match(ln)
        if m:
            ci = i
            class_indent = m.group(1)
            break
    if ci is None:
        return src, False

    fi = None
    func_indent = ""
    for i in range(ci + 1, len(lines)):
        ln = lines[i]
        # stop if next class at same indent
        if ln.startswith(class_indent) and ln.lstrip().startswith("class ") and (len(ln) - len(ln.lstrip()) == len(class_indent)):
            break
        m = func_pat.match(ln)
        if m:
            fi = i
            func_indent = m.group(1)
            break
    if fi is None:
        return src, False

    body_start = fi + 1
    end = body_start
    for j in range(body_start, len(lines)):
        ln = lines[j]
        if ln.strip() == "":
            end = j + 1
            continue
        ind = len(ln) - len(ln.lstrip())
        if ind <= len(func_indent):
            end = j
            break
        end = j + 1

    bi = func_indent + " " * 4
    new_block = []
    for b in new_body_lines:
        new_block.append(bi + b + "\n")

    out = lines[:body_start] + new_block + lines[end:]
    return "".join(out), True

def patch_module_save_delegate(root: Path, rel: str) -> bool:
    path = root / rel
    if not path.exists():
        log(f"WARN: fehlt: {rel}")
        return True

    src0 = path.read_text(encoding="utf-8", errors="replace")
    src = src0
    src = ensure_import_after_future(src, "from pathlib import Path  # R2380")
    src = ensure_import_after_future(src, "from modules import ini_writer  # R2380 SingleWriter")

    new_body = [
        '"""R2380: SingleWriter Delegation (preserve [Docking])."""',
        "try:",
        "    pr = Path(__file__).resolve().parent.parent",
        "    updates = {}",
        "    # optional: accept configparser-like objects passed as first arg 'cfg'",
        "    if 'cfg' in locals() and hasattr(cfg, 'sections'):",
        "        for sec in cfg.sections():",
        "            updates[sec] = {k: v for (k, v) in cfg.items(sec)}",
        "    ini_writer.merge_write_ini(pr, updates, preserve_sections=set(['Docking']))",
        "except Exception:",
        "    return",
    ]

    patched, ok = replace_module_func_body(src, "save", new_body)
    if not ok:
        log(f"OK: {rel} hat keine module-level save() (no-op)")
        return True

    bak = backup_file(root, rel)
    path.write_text(patched, encoding="utf-8")

    if not compile_ok(path):
        # rollback
        if bak:
            path.write_bytes(bak.read_bytes())
            log(f"ROLLBACK: {rel} restored from {bak.name}")
        return False

    log(f"OK: {rel} save() delegiert an ini_writer")
    return True

def patch_config_manager_class_save(root: Path, rel: str) -> bool:
    path = root / rel
    if not path.exists():
        log(f"WARN: fehlt: {rel}")
        return True

    src0 = path.read_text(encoding="utf-8", errors="replace")
    src = src0
    src = ensure_import_after_future(src, "from pathlib import Path  # R2380")
    src = ensure_import_after_future(src, "from modules import ini_writer  # R2380 SingleWriter")

    new_body = [
        '"""R2380: save delegates to ini_writer.merge_write_ini (preserve [Docking])."""',
        "try:",
        "    pr = Path(__file__).resolve().parent.parent",
        "    if getattr(self, '_config', None) is None:",
        "        return",
        "    updates = {}",
        "    for sec in self._config.sections():",
        "        updates[sec] = {}",
        "        for k, v in self._config.items(sec):",
        "            updates[sec][k] = v",
        "    ini_writer.merge_write_ini(pr, updates, preserve_sections=set(['Docking']))",
        "except Exception:",
        "    return",
    ]

    patched, ok = replace_class_method_body(src, "ShrimpDevConfigManager", "save", new_body)
    if not ok:
        log(f"FEHLER: {rel} -> ShrimpDevConfigManager.save nicht gefunden (Report folgt)")
        return False

    bak = backup_file(root, rel)
    path.write_text(patched, encoding="utf-8")

    if not compile_ok(path):
        if bak:
            path.write_bytes(bak.read_bytes())
            log(f"ROLLBACK: {rel} restored from {bak.name}")
        return False

    log(f"OK: {rel} ShrimpDevConfigManager.save delegiert an ini_writer")
    return True

def repair_if_broken(root: Path, rel: str) -> bool:
    path = root / rel
    if not path.exists():
        return True
    if compile_ok(path):
        return True
    # restore latest compilable backup
    bak = find_latest_compilable_backup(root, path.name)
    if not bak:
        log(f"FEHLER: Kein lauffähiges Backup gefunden für {path.name}")
        return False
    backup_file(root, rel)  # backup current broken
    restore_backup_to(root, rel, bak)
    if not compile_ok(path):
        log(f"FEHLER: Restore brachte keine Kompilation: {bak.name}")
        return False
    log(f"OK: {rel} restored from {bak.name}")
    return True

def write_report(root: Path, lines: list[str]):
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    rep = docs / f"Report_{RID}_SingleWriter_Fix_{ts()}.md"
    rep.write_text("\n".join(lines) + "\n", encoding="utf-8")
    log(f"Report geschrieben: {rep}")

def main():
    root = root_dir()
    report = []
    report.append(f"# {RID} – SingleWriter Fix (restore + safe patch)")
    report.append("")
    report.append(f"- Zeit: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: {root}")
    report.append("")

    # 1) Repair broken files first (esp. config_loader)
    for key, rel in FILES.items():
        ok = repair_if_broken(root, rel)
        report.append(f"- repair_if_broken {rel}: {'OK' if ok else 'FAIL'}")
        if not ok:
            write_report(root, report)
            return 2

    # 2) Patch config_loader / config_mgr module-level save
    ok1 = patch_module_save_delegate(root, FILES["config_loader"])
    ok2 = patch_module_save_delegate(root, FILES["config_mgr"])
    report.append(f"- patch save() {FILES['config_loader']}: {'OK' if ok1 else 'FAIL'}")
    report.append(f"- patch save() {FILES['config_mgr']}: {'OK' if ok2 else 'FAIL'}")

    # 3) Patch config_manager class save
    ok3 = patch_config_manager_class_save(root, FILES["config_manager"])
    report.append(f"- patch class save {FILES['config_manager']}: {'OK' if ok3 else 'FAIL'}")

    write_report(root, report)

    if not (ok1 and ok2 and ok3):
        return 2

    log("Beendet: rc=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())
