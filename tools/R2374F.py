# R2374F – Finaler, vollständiger Funktionsersatz von save()
# - Ersetzt NUR die Methode ShrimpDevConfigManager.save
# - Kein partieller Patch, kein Zeilen-Gefrickel
# - Backup + Compile-Check + Rollback

import os
import sys
import shutil
import py_compile
from datetime import datetime
import re

RID = "R2374F"
TS = datetime.now().strftime("%Y%m%d_%H%M%S")

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

    src = open(path, "r", encoding="utf-8", errors="replace").read()
    backup(path)

    # Import sicherstellen
    if "modules.ini_writer import get_writer" not in src:
        src = "from modules.ini_writer import get_writer\n" + src
        log("Import ini_writer ergänzt")

    # Vollständiger Ersatz der save()-Methode der Klasse ShrimpDevConfigManager
    pattern = re.compile(
        r"(class\s+ShrimpDevConfigManager\s*\([\s\S]*?\):[\s\S]*?)(^\s*def\s+save\s*\(.*?\)\s*:\s*\n)([\s\S]*?)(?=^\s*def\s+|\Z)",
        re.MULTILINE
    )

    m = pattern.search(src)
    if not m:
        log("FEHLER: save()-Methode in ShrimpDevConfigManager nicht gefunden")
        return 2

    class_head = m.group(1)
    save_header = m.group(2)
    indent = save_header.split("def")[0]

    new_save = (
        save_header +
        indent + "    # FINAL: Delegation an zentralen INI-Writer (Single Writer Policy)\n" +
        indent + "    writer = get_writer()\n" +
        indent + "    for sec in self._config.sections():\n" +
        indent + "        writer.update_many(\n" +
        indent + "            sec,\n" +
        indent + "            dict(self._config.items(sec)),\n" +
        indent + "            source=source or 'config_manager'\n" +
        indent + "        )\n" +
        indent + "    return writer.save_merge_atomic(source=source or 'config_manager')\n"
    )

    src_new = src[:m.start(2)] + new_save + src[m.end(3):]

    with open(path, "w", encoding="utf-8") as f:
        f.write(src_new)

    ok, err = compile_ok(path)
    if not ok:
        log("FEHLER: Kompilation fehlgeschlagen: " + err)
        shutil.copy2(
            os.path.join(root, "_Archiv", os.path.basename(path) + f".{RID}_{TS}.bak"),
            path
        )
        return 2

    report = os.path.join(root, "docs", f"Report_{RID}_ConfigManager_Final_Save.md")
    with open(report, "w", encoding="utf-8") as f:
        f.write(
            f"# {RID} – Finaler save()-Ersatz\n\n"
            f"- Zeit: {datetime.now():%Y-%m-%d %H:%M:%S}\n"
            f"- Klasse: ShrimpDevConfigManager\n"
            f"- Aktion: save() vollständig ersetzt\n"
            f"- Schreibpfad: ini_writer.save_merge_atomic()\n"
        )

    log("OK: save() final ersetzt")
    log("OK: Report geschrieben: " + report)
    return 0

if __name__ == "__main__":
    sys.exit(main())
