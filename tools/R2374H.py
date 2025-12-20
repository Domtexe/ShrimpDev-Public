# R2374H – FINAL safe replacement of ShrimpDevConfigManager.save()
# - Hard block replacement, no regex games, no AST
# - Uses explicit class + method markers
# - Backup + compile-check + rollback

import os
import sys
import shutil
import py_compile
from datetime import datetime

RID = "R2374H"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

TARGET_CLASS = "class ShrimpDevConfigManager"
TARGET_DEF = "def save"

NEW_SAVE = [
    "    def save(self) -> None:",
    "        \"\"\"",
    "        Delegiert das Schreiben der Konfiguration an den zentralen INI-SingleWriter.",
    "        \"\"\"",
    "        if self._config is None:",
    "            return",
    "",
    "        from modules.ini_writer import get_writer",
    "",
    "        writer = get_writer()",
    "",
    "        for sec in self._config.sections():",
    "            writer.update_many(",
    "                sec,",
    "                dict(self._config.items(sec)),",
    "                source=\"config_manager\",",
    "            )",
    "",
    "        writer.save_merge_atomic(source=\"config_manager\")",
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

    # ensure ini_writer import exists somewhere
    if not any("modules.ini_writer import get_writer" in l for l in src_lines):
        src_lines.insert(0, "from modules.ini_writer import get_writer")
        log("Import ini_writer ergänzt")

    out = []
    in_class = False
    in_save = False
    replaced = False

    for i, line in enumerate(src_lines):
        if line.startswith(TARGET_CLASS):
            in_class = True
            out.append(line)
            continue

        if in_class and line.lstrip().startswith(TARGET_DEF) and not replaced:
            # replace whole save() block
            indent = line[:len(line) - len(line.lstrip())]
            for nl in NEW_SAVE:
                out.append(indent + nl if nl else "")
            in_save = True
            replaced = True
            continue

        if in_save:
            # skip old save body until next method at same indent
            if line.startswith("    def ") and not line.lstrip().startswith(TARGET_DEF):
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
        f.write("\n".join(out))

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        shutil.copy2(
            os.path.join(root, "_Archiv", os.path.basename(path) + f".{RID}_{TS}.bak"),
            path
        )
        return 2

    report = os.path.join(root, "docs", f"Report_{RID}_Final_Save_Replacement.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Finaler save()-Ersatz\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Klasse: ShrimpDevConfigManager\n"
            f"- Aktion: save() vollständig ersetzt\n"
            f"- Schreibpfad: ini_writer.save_merge_atomic()\n"
        )

    log("OK: save() final und sicher ersetzt")
    log("OK: Report geschrieben: " + report)
    return 0

if __name__ == "__main__":
    sys.exit(main())
