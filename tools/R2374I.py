# R2374I – FINAL safe replacement of ShrimpDevConfigManager.save()
# - Does NOT inject any top-level imports (preserves __future__ rules)
# - Replaces ONLY the save() method body by hard block replacement
# - Backup + compile-check + rollback

import os
import sys
import shutil
import py_compile
from datetime import datetime

RID = "R2374I"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

TARGET_CLASS = "class ShrimpDevConfigManager"
TARGET_DEF = "def save"

# IMPORTANT: no leading indentation here; we apply indentation dynamically.
NEW_SAVE = [
    "def save(self) -> None:",
    '    """',
    "    Delegiert das Schreiben der Konfiguration an den zentralen INI-SingleWriter.",
    '    """',
    "    if self._config is None:",
    "        return",
    "",
    "    from modules.ini_writer import get_writer",
    "",
    "    writer = get_writer()",
    "",
    "    for sec in self._config.sections():",
    "        writer.update_many(",
    "            sec,",
    "            dict(self._config.items(sec)),",
    '            source="config_manager",',
    "        )",
    "",
    '    writer.save_merge_atomic(source="config_manager")',
]

def log(msg):
    print(f"[{RID}] {datetime.now():%Y-%m-%d %H:%M:%S} {msg}")

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def backup(path):
    arch = os.path.join(root_dir(), "_Archiv")
    os.makedirs(arch, exist_ok=True)
    dst = os.path.join(arch, os.path.basename(path) + f".{RID}_{TS}.bak")
    shutil.copy2(path, dst)
    log(f"Backup: {path} -> {dst}")
    return dst

def compile_ok(path):
    try:
        py_compile.compile(path, doraise=True)
        return True, ""
    except Exception as e:
        return False, repr(e)

def main():
    root = root_dir()
    path = os.path.join(root, "modules", "config_manager.py")

    if not os.path.isfile(path):
        log("FEHLER: config_manager.py nicht gefunden")
        return 2

    src_lines = open(path, "r", encoding="utf-8", errors="replace").read().splitlines()
    backup(path)

    out = []
    in_class = False
    in_save = False
    replaced = False
    save_indent = ""

    for line in src_lines:
        if line.startswith(TARGET_CLASS):
            in_class = True
            out.append(line)
            continue

        # detect save() def inside the class
        if in_class and (line.lstrip().startswith(TARGET_DEF)) and not replaced:
            save_indent = line[:len(line) - len(line.lstrip())]  # usually 4 spaces
            # write new save block with correct indent
            for idx, nl in enumerate(NEW_SAVE):
                if nl == "":
                    out.append("")
                elif idx == 0:
                    out.append(save_indent + nl)          # def save...
                else:
                    out.append(save_indent + nl)          # body already 4-spaced relative to def
            in_save = True
            replaced = True
            continue

        if in_save:
            # skip old save block until we hit next method def at same class-indent
            # In class, methods typically start with save_indent + "def "
            if save_indent and line.startswith(save_indent + "def ") and not line.lstrip().startswith(TARGET_DEF):
                in_save = False
                out.append(line)
            else:
                continue
        else:
            out.append(line)

    if not replaced:
        log("FEHLER: save()-Methode nicht ersetzt (Marker nicht gefunden)")
        return 2

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        # rollback
        bak = os.path.join(root, "_Archiv", os.path.basename(path) + f".{RID}_{TS}.bak")
        shutil.copy2(bak, path)
        return 2

    # report
    rep_dir = os.path.join(root, "docs")
    os.makedirs(rep_dir, exist_ok=True)
    report = os.path.join(rep_dir, f"Report_{RID}_Final_Save_Replacement.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Finaler save()-Ersatz\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Klasse: ShrimpDevConfigManager\n"
            f"- Aktion: save() vollständig ersetzt (keine Top-Level Imports)\n"
            f"- Schreibpfad: ini_writer.save_merge_atomic()\n"
        )

    log("OK: save() final ersetzt (no top-level import)")
    log("OK: Report geschrieben: " + report)
    return 0

if __name__ == "__main__":
    sys.exit(main())
